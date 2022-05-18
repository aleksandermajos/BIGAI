//+------------------------------------------------------------------+
//|                                                QUANTMAVERICK.mq4 |
//|                                                    QUANTMAVERICK |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright "QUANTMAVERICK"
#property link      ""
#property version   "1.00"
#property strict

#include <Zmq/Zmq.mqh>
#include <QUANTMAVERICKMT4/Util.mq4>
#include <QUANTMAVERICKMT4/Util2.mq5>
#include <JAson.mqh>
#include <Trade\Trade.mqh>

Context context;
Socket socPUB(context,ZMQ_PUB);
Socket socREP(context,ZMQ_REP);
string TO_SEND = "";
string LAST_REQ = "";
input int SUBPUB_PORT  =2027;
input int REQREP_PORT  =2028;

string OpenTran(string Message)
{
bool Opened = false;
CJAVal jo(NULL, jtUNDEF); bool b;
b=jo.Deserialize(Message);
string key=jo["key"].ToStr();
string symbol = jo["symbol"].ToStr();
string operation = jo["operation"].ToStr();
double volume = jo["volume"].ToDbl();
double price = jo["price"].ToDbl();
int slippage = jo["slippage"].ToInt();
int TP = jo["TP"].ToInt();
int SL = jo["SL"].ToInt();


//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request={0};
   MqlTradeResult  result={0};
    
//--- parameters of request

   request.action   =TRADE_ACTION_DEAL;                     // type of trade operation
   request.symbol   = symbol;                              // symbol
   request.volume   = volume;                                   // volume of 0.1 lot
   if (operation == "OP_BUY") request.type = ORDER_TYPE_BUY;
   if (operation == "OP_SELL") request.type = ORDER_TYPE_SELL;
   request.price    =SymbolInfoDouble(symbol,SYMBOL_ASK); // price for opening
   request.deviation=slippage;                                    // allowed deviation from the price
                   
//--- send the request
   if(!OrderSend(request,result))
      PrintFormat("OrderSend error %d",GetLastError());     // if unable to send the request, output the error code
   else Opened = true;
//--- information about the operation
   PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);

string Result = "";
if(Opened) Result = "true";
else Result = "false";

string uRetval =  "{";
    uRetval += StringFormat("\"Result\": %s ",Result);
    uRetval += "}";
    return(uRetval);
}

string CloseTran(string Message)
{
CTrade trade;
bool closed = false;
CJAVal jo(NULL, jtUNDEF); bool b;
b=jo.Deserialize(Message);
string key=jo["key"].ToStr();
int slippage = jo["slippage"].ToInt();
int ticket = jo["ticket"].ToInt();

closed = trade.PositionClose(ticket,slippage);

string Result = "";
if(closed) Result = "true";
else Result = "false";

string uRetval =  "{";
    uRetval += StringFormat("\"Result\": %s ",Result);
    uRetval += "}";
    return(uRetval);
}

string ReqRepReply(string Message) 
{
    LAST_REQ = Message;
    string Result = "";
    //Result = Result+ChartName(Symbol(), Period(), ChartID());
    if(StringFind(Message,"CHARTNAME",0) != -1) Result = Result+ChartName(Symbol(), PeriodSeconds(PERIOD_CURRENT), ChartID());
    if(StringFind(Message,"PORTSNR",0) != -1) Result = Result+Portsnr(SUBPUB_PORT,REQREP_PORT);
    if(StringFind(Message,"ACCOUNTINFO",0) != -1) Result = Result+AccountInformation();
    if(StringFind(Message,"INSTRUMENTINFO",0) != -1) Result = Result+InstrumentInfo(Symbol());
    if(StringFind(Message,"HISTORY",0) != -1) Result = Result+History(Symbol());
    if(StringFind(Message,"PRICE",0) != -1) Result = Result+Price(Symbol());
    if(StringFind(Message,"TRANSACTIONS",0) != -1) Result = Result+Transactions();
    if(StringFind(Message,"OPEN",0) != -1) Result = Result+OpenTran(Message);
    if(StringFind(Message,"CLOSE",0) != -1) Result = Result+CloseTran(Message);
    return Result;
    
}
string Change_TO_SEND()
{
TO_SEND = ReqRepReply(LAST_REQ);
return TO_SEND;
}
void Updete_TO_SEND()
{
TO_SEND = ReqRepReply("CHARTNAME.PRICE");
}
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetMillisecondTimer(100);
   socPUB.bind("tcp://*:"+SUBPUB_PORT);
   socREP.bind("tcp://*:"+REQREP_PORT);
   LAST_REQ="CHARTNAME";
   TO_SEND = ReqRepReply(LAST_REQ);
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
 // EventKillTimer();
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
Updete_TO_SEND();
Print(TO_SEND);
ZmqMsg message(TO_SEND);
socPUB.send(message);

ZmqMsg request;
socREP.recv(request,true);
string Message = request.getData();
if(Message == NULL) Message = "";
if(Message != "")
{
Print("Received NEW message : "+Message);
TO_SEND = ReqRepReply(Message);
ZmqMsg reply(TO_SEND);
LAST_REQ = Message;
socREP.send(reply);
}
}
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
{
Updete_TO_SEND();
Print(TO_SEND);
ZmqMsg message(TO_SEND);
socPUB.send(message);

ZmqMsg request;
socREP.recv(request,true);
string Message = request.getData();
if(Message == NULL) Message = "";
if(Message != "")
{
Print("Received NEW message : "+Message);
TO_SEND = ReqRepReply(Message);
ZmqMsg reply(TO_SEND);
LAST_REQ = Message;
socREP.send(reply);
}
}
//+------------------------------------------------------------------+
//| Tester function                                                  |
//+------------------------------------------------------------------+
double OnTester()
  {
//---
   double ret=0.0;
//---

//---
   return(ret);
  }
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
  {
//---
   
  }
//+------------------------------------------------------------------+
