//+------------------------------------------------------------------+
//|                                                  Kupno_Hedge.mq4 |
//|                                                          BOSSAFX |
//|                                                   www.bossafx.pl |
//+------------------------------------------------------------------+
#property copyright "BOSSAFX"
#property link      "www.bossafx.pl"

#include <stdlib.mqh>
#include <stderror.mqh>



 double           Nominal_transakcji=1      ;

 int              Stop_loss=30               ;

 int              Take_profit=50             ;

 int              Max_odchylenie_od_ceny=2   ;             

 
 
 
 
 
 
 
 
 
 
 
 
 


//+------------------------------------------------------------------+
//| script program start function                                    |
//+------------------------------------------------------------------+
int start()
  {

            double Lot=Nominal_transakcji;
            int price_dev=Max_odchylenie_od_ceny;                       
            double TP=0;
            double SL=0;
                        
            if( Take_profit!= 0 )  TP=MarketInfo(Symbol(),MODE_ASK)+Take_profit*Point;
            if( Stop_loss !=0 )    SL=MarketInfo(Symbol(),MODE_BID)-Stop_loss*Point;
            
            int cmd;
            int blad;
  
           
            double max_lot=MarketInfo(Symbol(),MODE_MAXLOT);
            int order_ticket;
 
            
                 while( Lot >0 )
                 {  
                     if ( Lot > max_lot)
                     {
                        cmd=OrderSend(Symbol(),OP_BUY,max_lot,MarketInfo(Symbol(),MODE_ASK),price_dev,SL,TP );    //otwarcie pozycji kr�tkiej
                        Lot=Lot-max_lot;
                     }
                     else
                     {
                       cmd=OrderSend(Symbol(),OP_BUY,Lot,MarketInfo(Symbol(),MODE_ASK),price_dev,SL,TP ); 
                       Lot=0;
                     }
                      
                    
                      if (cmd == -1)        // w przypadku gdy zlecenie nie zostanie otwarte sprawdzamy  
                      {                                // co mog�o spowodowa� b�ad
                             blad=GetLastError();
                             switch(blad)
                             { 
                              case 4109:
                                   Alert(" Opcja \"Umo�liw handel\" jest wy��czona. ");
                                                      
                              break;
                              case 134:
                                   Alert(" Niewystarczaj�ca ilo�� wolnych �rodk�w do otwarcia zlecenia.");
                               
                              break;
                              default: 
                                   Alert("Wyst�pi� b��d numer: ",blad,"  \"",ErrorDescription(blad),"\"");
                             
                             }
                          break;
                      }
                     
                 }                                           
   return(0);
  }
//+------------------------------------------------------------------+


                 

