//+------------------------------------------------------------------+
//|                                             QUANTMAVERICKMT4.mq4 |
//|                                Copyright 2019, QuantMaverick Ltd.|
//|                                                                  |
//+------------------------------------------------------------------+

string Transactions() {
    string uRetval = "";
     for(int i=0;i<PositionsTotal();i++)
        {
        PositionGetSymbol(i);
        uRetval += "{";
        uRetval += StringFormat("\"ticket\": %i, ", PositionGetInteger(POSITION_TICKET));
        uRetval += StringFormat("\"price\": %f, ", PositionGetDouble(POSITION_PRICE_OPEN));
        uRetval += StringFormat("\"time\": \"%s\", ", TimeToString(PositionGetInteger(POSITION_TIME)));
        uRetval += StringFormat("\"symbol\": \"%s\", ", PositionGetString(POSITION_SYMBOL));
        uRetval += StringFormat("\"size\": %0.3f", PositionGetDouble(POSITION_VOLUME));
        uRetval += "}";
        }
    
    

     

    return(uRetval);
}