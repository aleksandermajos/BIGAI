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
    uRetval += StringFormat("\"balance\": %f, ", AccountInfoDouble(ACCOUNT_BALANCE)); // Decimal
    uRetval += StringFormat("\"credit\": %f, ",AccountInfoDouble(ACCOUNT_CREDIT)); // Decimal
    uRetval += StringFormat("\"company\": \"%s\", ", AccountInfoString(ACCOUNT_COMPANY));
    uRetval += StringFormat("\"currency\": \"%s\", ", AccountInfoString(ACCOUNT_CURRENCY));
    uRetval += StringFormat("\"equity\": %f, ",AccountInfoDouble(ACCOUNT_EQUITY)); // Decimal
    uRetval += StringFormat("\"free_margin\": %f, ",AccountInfoDouble(ACCOUNT_MARGIN_FREE)); // Decimal
    uRetval += StringFormat("\"free_margin_mode\": %f, ",0);
    uRetval += StringFormat("\"leverage\": %i, ",AccountInfoInteger(ACCOUNT_LEVERAGE));
    uRetval += StringFormat("\"margin\": %f, ",  AccountInfoDouble(ACCOUNT_MARGIN)); // Decimal
    uRetval += StringFormat("\"name\": \"%s\", ",AccountInfoString(ACCOUNT_NAME));
    uRetval += StringFormat("\"number\": %i, ", AccountInfoInteger(ACCOUNT_LOGIN));
    uRetval += StringFormat("\"profit\": %f, ", AccountInfoDouble(ACCOUNT_PROFIT)); // Decimal
    uRetval += StringFormat("\"server\": \"%s\", ", AccountInfoString(ACCOUNT_SERVER));
    uRetval += StringFormat("\"stopout_level\": %i, ", 0); //?
    uRetval += StringFormat("\"stopout_mode\": %i", 0); //?
    uRetval += "}";
    return(uRetval);
}

string MarketInformation(string uSymbol) {
    string uRetval;

    uRetval = "{";
    uRetval += StringFormat("\"symbol\": \"%s\", ", uSymbol);
    uRetval += StringFormat("\"low\": %f, ", 0);
    uRetval += StringFormat("\"high\": %f, ", 0);
    uRetval += StringFormat("\"time\": %d, ", 0);//fix
    uRetval += StringFormat("\"bid\": %f, ", 0);
    uRetval += StringFormat("\"ask\": %f, ", 0);
    uRetval += StringFormat("\"point\": %f, ", 0);//fix?
    uRetval += StringFormat("\"digits\": %f, ", 0);//fix?
    uRetval += StringFormat("\"spread\": %f, ", 0);
    uRetval += StringFormat("\"stoplevel\": %f, ", 0);
    uRetval += StringFormat("\"lotsize\": %f, ", 0);
    uRetval += StringFormat("\"tickvalue\": %f, ", 0);
    uRetval += StringFormat("\"ticksize\": %f, ",0);
    uRetval += StringFormat("\"swaplong\": %f, ", 0);
    uRetval += StringFormat("\"swapshort\": %f, ",0);
    uRetval += StringFormat("\"starting\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"expiration\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"tradeallowed\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"minlot\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"lotstep\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"maxlot\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"swaptype\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"profitcalcmode\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"margincalcmode\": \"%s\", ", 0);//?
    uRetval += StringFormat("\"margininit\": \"%s\", ", 0);
    uRetval += StringFormat("\"marginmaintenance\": \"%s\", ",0);
    uRetval += StringFormat("\"marginhedged\": \"%s\", ", 0);
    uRetval += StringFormat("\"marginrequired\": \"%s\", ", 0);
    uRetval += StringFormat("\"freezelevel\": \"%s\"", 0);
    uRetval += "}";
    return(uRetval);
}

string InstrumentInfo(string uSymbol) {
string uRetval;
 
uRetval =  "{";
    uRetval += StringFormat("\"symbol\": \"%s\", ", uSymbol);
    uRetval += StringFormat("\"points\": %f, ", SymbolInfoDouble(Symbol(),SYMBOL_POINT));
    uRetval += StringFormat("\"digits\": %f, ", SymbolInfoInteger(Symbol(),SYMBOL_DIGITS));
    uRetval += StringFormat("\"spread\": %f, ", SymbolInfoInteger(Symbol(),SYMBOL_SPREAD));
    uRetval += StringFormat("\"contract_size\": %f, ", SymbolInfoDouble(Symbol(),SYMBOL_TRADE_CONTRACT_SIZE));
    uRetval += StringFormat("\"min_volume\": %f, ", SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_MIN));
    uRetval += StringFormat("\"max_volume\": %f, ", SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_MAX));
    uRetval += StringFormat("\"swap_long\": %f, ", SymbolInfoDouble(Symbol(),SYMBOL_SWAP_LONG));
    uRetval += StringFormat("\"swap_short\": %f",SymbolInfoDouble(Symbol(),SYMBOL_SWAP_SHORT) );
    uRetval += "}";
    return(uRetval);
}

string ChartName(string uSymbol, int iPeriod, long iWindowId) {
    iPeriod = iPeriod/60;
    string uRetval="{";
    uRetval += StringFormat("\"Terminal\": \"%s\", ","MT5" );
    uRetval += StringFormat("\"Broker\": \"%s\", ",AccountInfoString(ACCOUNT_COMPANY));
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

uRetval =  "{";
    uRetval += StringFormat("\"symbol\": \"%s\", ", uSymbol);
    uRetval += StringFormat("\"time\": \"%s\", ", ti);
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