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
#include <QUANTMAVERICKMT4/hash.mqh>
#include <QUANTMAVERICKMT4/json.mqh>

Context context;
Socket SUBLISTENERPORTS(context,ZMQ_SUB);
Socket socPUB(context,ZMQ_PUB);
Socket socREP(context,ZMQ_REP);
int SUBPUB_PORT = 0;
int REQREP_PORT = 0;
bool NEWPORTS = false;
string TO_SEND = "";
string LAST_REQ = "";


string ReqRepReply(string Message) 
{
    LAST_REQ = Message;
    string Result = "";
    //Result = Result+ChartName(Symbol(), Period(), ChartID());
    if(StringFind(Message,"CHARTNAME",0) != -1) Result = Result+ChartName(Symbol(), Period(), ChartID());
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
string OpenTran(string Message)
{
int number = 0;
string time_start = "";
string time_stop = "";
JSONParser *parser = new JSONParser();
JSONValue *jv = parser.parse(Message);

    if (jv == NULL) { Print("error:"+(string)parser.getErrorCode()+parser.getErrorMessage());} 
    else {
Print("PARSED:"+jv.toString());
if (jv.isObject())
{ // check root value is an object. (it can be an array)
JSONObject *jo = jv;
string key = jo.getString("key");
string symbol = jo.getString("symbol");
string operation = jo.getString("operation");
double volume = jo.getDouble("volume");
double price = jo.getDouble("price");
int slippage = jo.getInt("slippage");
int TP = jo.getInt("TP");
int SL = jo.getInt("SL");

time_start = CurrentTime();

number = OrderSend(symbol,operation,volume,price,slippage,TP,SL);

time_stop = CurrentTime();
}
delete jv;
}
delete parser;


string Result = "";
if(number != 0) Result = "true";
else Result = "false";

string uRetval =  "{";
    uRetval += StringFormat("\"Result\": %s, ",Result);
    uRetval += StringFormat("\"time_start\": \"%s\", ", time_start);
    uRetval += StringFormat("\"time_stop\": \"%s\" ", time_stop);
    uRetval += "}";
    return(uRetval);
}

string CloseTran(string Message)
{
bool closed = false;
JSONParser *parser = new JSONParser();
JSONValue *jv = parser.parse(Message);

    if (jv == NULL) { Print("error:"+(string)parser.getErrorCode()+parser.getErrorMessage());} 
    else {
Print("PARSED:"+jv.toString());
if (jv.isObject())
{ // check root value is an object. (it can be an array)
JSONObject *jo = jv;
string key = jo.getString("key");
int ticket = jo.getInt("ticket");
double volume = jo.getDouble("volume");
int slippage = jo.getInt("slippage");

closed = OrderClose(ticket,volume,Ask,slippage,Red);
}
delete jv;
}
delete parser;


string Result = "";
if(closed) Result = "true";
else Result = "false";

string uRetval =  "{";
    uRetval += StringFormat("\"Result\": %s ",Result);
    uRetval += "}";
    return(uRetval);
}

string Change_TO_SEND()
{
TO_SEND = ReqRepReply(LAST_REQ);
return TO_SEND;
}
bool Change_Ports(string Ports)
{
string sep=" ";
ushort u_sep;
       u_sep=StringGetCharacter(sep,0); 
string result[];
int k=StringSplit(Ports,u_sep,result);

SUBPUB_PORT = result[2];
REQREP_PORT = result[3];
socPUB.bind("tcp://*:"+SUBPUB_PORT);
socREP.bind("tcp://*:"+REQREP_PORT);
TO_SEND = ReqRepReply("");
NEWPORTS = true;
return true;
}
bool CheckToChangePorts()
{
ZmqMsg ports("");
  SUBLISTENERPORTS.recv(ports,true);
  string Ports = ports.getData();
  Print(TO_SEND);
  if(Ports != "" && NEWPORTS == false) Change_Ports(Ports);
  return true;
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
   //EventSetMillisecondTimer(100);
   SUBLISTENERPORTS.connect("tcp://localhost:2025");
   SUBLISTENERPORTS.subscribe("");
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
if(NEWPORTS == false) CheckToChangePorts();
else{
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
}
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
{
if(NEWPORTS == false) CheckToChangePorts();
else{
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
