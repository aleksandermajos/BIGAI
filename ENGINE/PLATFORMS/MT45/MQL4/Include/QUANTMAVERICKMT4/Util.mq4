//+------------------------------------------------------------------+
//|                                             QUANTMAVERICKMT4.mq4 |
//|                                Copyright 2019, QuantMaverick Ltd.|
//|                                                                  |
//+------------------------------------------------------------------+
struct _SYSTEMTIME {
  ushort wYear;         // 2014 etc
  ushort wMonth;        // 1 - 12
  ushort wDayOfWeek;    // 0 - 6 with 0 = Sunday
  ushort wDay;          // 1 - 31
  ushort wHour;         // 0 - 23
  ushort wMinute;       // 0 - 59
  ushort wSecond;       // 0 - 59
  ushort wMilliseconds; // 0 - 999
};
#import "kernel32.dll"
void GetSystemTime(_SYSTEMTIME &time);
void GetSystemTimeAsFileTime(ulong &SystemTimeAsFileTime);
#import

string AccountInformation() {
    string uRetval;
    uRetval = "{";
    uRetval += StringFormat("\"status\": \"%s\", ", "ok");
    uRetval += StringFormat("\"balance\": %f, ", AccountBalance()); // Decimal
    uRetval += StringFormat("\"credit\": %f, ", AccountCredit()); // Decimal
    uRetval += StringFormat("\"company\": \"%s\", ", AccountCompany());
    uRetval += StringFormat("\"currency\": \"%s\", ", AccountCurrency());
    uRetval += StringFormat("\"equity\": %f, ", AccountEquity()); // Decimal
    uRetval += StringFormat("\"free_margin\": %f, ", AccountFreeMargin()); // Decimal
    uRetval += StringFormat("\"free_margin_mode\": %f, ", AccountFreeMarginMode());
    uRetval += StringFormat("\"leverage\": %i, ", AccountLeverage());
    uRetval += StringFormat("\"margin\": %f, ", AccountMargin()); // Decimal
    uRetval += StringFormat("\"name\": \"%s\", ", AccountName());
    uRetval += StringFormat("\"number\": %i, ", AccountNumber());
    uRetval += StringFormat("\"profit\": %f, ", AccountProfit()); // Decimal
    uRetval += StringFormat("\"server\": \"%s\", ", AccountServer());
    uRetval += StringFormat("\"stopout_level\": %i, ", AccountStopoutLevel()); //?
    uRetval += StringFormat("\"stopout_mode\": %i", AccountStopoutMode()); //?
    uRetval += "}";
    return(uRetval);
}

string MarketInformation(string uSymbol) {
    string uRetval;

    // FixMe: coalesce
    uRetval = "{";
    uRetval += StringFormat("\"symbol\": \"%s\", ", uSymbol);
    uRetval += StringFormat("\"low\": %f, ", MarketInfo(uSymbol, MODE_LOW));
    uRetval += StringFormat("\"high\": %f, ", MarketInfo(uSymbol, MODE_HIGH));
    uRetval += StringFormat("\"time\": %d, ", MarketInfo(uSymbol, MODE_TIME));//fix
    uRetval += StringFormat("\"bid\": %f, ", MarketInfo(uSymbol, MODE_BID));
    uRetval += StringFormat("\"ask\": %f, ", MarketInfo(uSymbol, MODE_ASK));
    uRetval += StringFormat("\"point\": %f, ", MarketInfo(uSymbol, MODE_POINT));//fix?
    uRetval += StringFormat("\"digits\": %f, ", MarketInfo(uSymbol, MODE_DIGITS));//fix?
    uRetval += StringFormat("\"spread\": %f, ", MarketInfo(uSymbol, MODE_SPREAD));
    uRetval += StringFormat("\"stoplevel\": %f, ", MarketInfo(uSymbol, MODE_STOPLEVEL));
    uRetval += StringFormat("\"lotsize\": %f, ", MarketInfo(uSymbol, MODE_LOTSIZE));
    uRetval += StringFormat("\"tickvalue\": %f, ", MarketInfo(uSymbol, MODE_TICKVALUE));
    uRetval += StringFormat("\"ticksize\": %f, ", MarketInfo(uSymbol, MODE_TICKSIZE));
    uRetval += StringFormat("\"swaplong\": %f, ", MarketInfo(uSymbol, MODE_SWAPLONG));
    uRetval += StringFormat("\"swapshort\": %f, ", MarketInfo(uSymbol, MODE_SWAPSHORT));
    uRetval += StringFormat("\"starting\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_STARTING));//?
    uRetval += StringFormat("\"expiration\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_EXPIRATION));//?
    uRetval += StringFormat("\"tradeallowed\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_TRADEALLOWED));//?
    uRetval += StringFormat("\"minlot\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_MINLOT));//?
    uRetval += StringFormat("\"lotstep\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_LOTSTEP));//?
    uRetval += StringFormat("\"maxlot\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_MAXLOT));//?
    uRetval += StringFormat("\"swaptype\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_SWAPTYPE));//?
    uRetval += StringFormat("\"profitcalcmode\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_PROFITCALCMODE));//?
    uRetval += StringFormat("\"margincalcmode\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_MARGINCALCMODE));//?
    uRetval += StringFormat("\"margininit\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_MARGININIT));
    uRetval += StringFormat("\"marginmaintenance\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_MARGINMAINTENANCE));
    uRetval += StringFormat("\"marginhedged\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_MARGINHEDGED));
    uRetval += StringFormat("\"marginrequired\": \"%s\", ", (string)MarketInfo(uSymbol, MODE_MARGINREQUIRED));
    uRetval += StringFormat("\"freezelevel\": \"%s\"", (string)MarketInfo(uSymbol, MODE_FREEZELEVEL));
    uRetval += "}";
    return(uRetval);
}

string Transactions() {
    string uRetval = "";
    int total=OrdersTotal();
    if(total==0) return "{}";
    for(int pos=0;pos<total;pos++)
    {
     if(OrderSelect(pos,SELECT_BY_POS)==false) continue;
     uRetval += "{";
     uRetval += StringFormat("\"ticket\": %i, ", OrderTicket());
     uRetval += StringFormat("\"price\": %f, ", OrderOpenPrice());
     uRetval += StringFormat("\"time\": \"%s\", ", TimeToString(OrderOpenTime()));
     uRetval += StringFormat("\"symbol\": \"%s\", ", OrderSymbol());
     uRetval += StringFormat("\"size\": %0.3f", OrderLots());
     uRetval += "}";
    }
    return(uRetval);
}

string InstrumentInfo(string uSymbol) {
string uRetval;
uRetval =  "{";
    uRetval += StringFormat("\"symbol\": \"%s\", ", uSymbol);
    uRetval += StringFormat("\"points\": %f, ", MarketInfo(uSymbol, MODE_POINT));
    uRetval += StringFormat("\"digits\": %f, ", MarketInfo(uSymbol, MODE_DIGITS));
    uRetval += StringFormat("\"spread\": %f, ", MarketInfo(uSymbol, MODE_SPREAD));
    uRetval += StringFormat("\"contract_size\": %f, ", MarketInfo(uSymbol, MODE_LOTSIZE));
    uRetval += StringFormat("\"min_volume\": %f, ", MarketInfo(uSymbol, MODE_MINLOT));
    uRetval += StringFormat("\"max_volume\": %f, ", MarketInfo(uSymbol, MODE_MAXLOT));
    uRetval += StringFormat("\"swap_long\": %f, ", MarketInfo(uSymbol, MODE_SWAPLONG));
    uRetval += StringFormat("\"swap_short\": %f", MarketInfo(uSymbol, MODE_SWAPSHORT));
    uRetval += "}";
    return(uRetval);
}

string ChartName(string uSymbol, int iPeriod, long iWindowId) {
    string uRetval="{";
    uRetval += StringFormat("\"Terminal\": \"%s\", ","MT4" );
    uRetval += StringFormat("\"Broker\": \"%s\", ",AccountCompany());
    uRetval += StringFormat("\"Symbol\": \"%s\", ",uSymbol );
    uRetval += StringFormat("\"Period\": %i, ",iPeriod );
    uRetval += StringFormat("\"WindowID\": \"%X\"", iWindowId);
    uRetval += "}";
    return(uRetval);
}

string History(string uSymbol) {
string uRetval="";
    MqlRates rates[];
    ArraySetAsSeries(rates,true);
    int copied=CopyRates(Symbol(),0,0,100,rates);
    int size=fmin(copied,10);
    string format="%G,%G,%G,%G,%d";
    uRetval +="Time,O,H,L,C,V\n";
    for(int i=0;i<size;i++)
        {
         uRetval+=TimeToString(rates[i].time);
         uRetval+=", "+StringFormat(format,
                                  rates[i].open,
                                  rates[i].high,
                                  rates[i].low,
                                  rates[i].close,
                                  rates[i].tick_volume);
        uRetval +="\n";
    
      }
    return(uRetval);
}
string Price(string uSymbol)
{
string uRetval;
MqlTick last_tick;
SymbolInfoTick(uSymbol,last_tick);

uRetval =  "{";
    uRetval += StringFormat("\"symbol\": \"%s\", ", uSymbol);
    uRetval += StringFormat("\"time\": \"%s\", ", CurrentTime());
    uRetval += StringFormat("\"bid\": %f, ",last_tick.bid );
    uRetval += StringFormat("\"ask\": %f, ",last_tick.ask );
    uRetval += StringFormat("\"volumen\": %f ",last_tick.volume);
    uRetval += "}";
    return(uRetval);
}
string Portsnr(int SUBPUB,int REQREP)
{
string uRetval =  "{";
    uRetval += StringFormat("\"SubPubPort\": %i, ", SUBPUB);
    uRetval += StringFormat("\"ReqRepPort\": %i ", REQREP);
    uRetval += "}";
    return(uRetval);
}

string CurrentTime()
{
string uRetval;
_SYSTEMTIME st;
  GetSystemTime(st);
string ti = st.wYear+"-";
if (StringLen(st.wMonth) == 1) ti = ti+"0"+st.wMonth+"-";
else ti = ti+st.wMonth+"-";
if (StringLen(st.wDay) == 1) ti = ti+"0"+st.wDay+"T";
else ti = ti+st.wDay+" ";
if (StringLen(st.wHour) == 1) ti = ti+"0"+st.wHour+":";
else ti = ti+st.wHour+":";
if (StringLen(st.wMinute) == 1) ti = ti+"0"+st.wMinute+":";
else ti = ti+st.wMinute+":";
if (StringLen(st.wSecond) == 1) ti = ti+"0"+st.wSecond+".";
else ti = ti+st.wSecond+".";

if (StringLen(st.wMilliseconds) == 1) ti = ti+"00"+st.wMilliseconds;
if (StringLen(st.wMilliseconds) == 2) ti = ti+"0"+st.wMilliseconds;
else ti = ti+st.wMilliseconds;

uRetval =  ti;
return(uRetval);

}