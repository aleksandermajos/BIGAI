//+------------------------------------------------------------------+
//|                                                            JAson |
//+------------------------------------------------------------------+
#property copyright "Copyright © 2006-2016"
#property version "1.06"
#property strict
//---
#include <JAson.mqh>
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnStart()
  {
   string in,out;
   CJAVal js(NULL,jtUNDEF); bool b;
   
//---
   Print("JASon Example Deserialization:");
//---
   in="{\"a\":[1,2]}"; out="";
   b=js.Deserialize(in);
   js.Serialize(out);
   Print(in+" -> "+out);
  
  in="{ \"array\": [ { \"symbol\": \"USDJPY\", \"type\": \"Buy\", \"lot\": 0.5, \"price_open\": 102.36, \"price_close\": 102.44, \"stop_loss\": 99.25, \"take_profit\": 103.25 }, { \"symbol\": \"EURUSD\", \"type\": \"Sell\", \"lot\": 0.2, \"price_open\": 1.1044, \"price_close\": 1.1252, \"stop_loss\": 1.1434, \"take_profit\": 1.0922 } ] }";
  //in="{ \"array\": [ { \"s\": 1 }, { \"s\": 2 } ] }";
  js.Clear(); out="";
	b=js.Deserialize(in);
	js.Serialize(out);
	Print(out);

	in="{\"description\":\"\\u041d\\u043e\\u0432\\u043e\\u0435 \\u0432 \\u0432\\u0435\\u0440\\u0441\\u0438\\u0438 v.2\"}";
	js.Clear(); out="";
   b=js.Deserialize(in);
   js.Serialize(out);
   Print(in+" -> "+out);
   
//---
   in="{\"a\":[{\"b\":1},{\"c\":2}]}"; out="";
   b=js.Deserialize(in);
   js.Serialize(out);
   Print(in+" -> "+out);
//---
   in="{\"res\":{\"tas\":[{\"mas1\":[{\"ma1\":{\"t\":1}}]}]}"; out="";
   b=js.Deserialize(in); js.Serialize(out);
   Print(in+" -> "+out);
//---
   string ma1="{\"ma1\":{\"t1\":1}}";
   string ma2="{\"ma2\":{\"t2\":1}}";
   string mas=StringFormat("{\"mas1\":[%s,%s]}", ma1, ma2);
   in=StringFormat("{\"tas\":[%s,%s]}",mas,mas); out="";
   b=js.Deserialize(in); js.Serialize(out);
   Print(in+" -> "+out);
//---

   Print("JASon Example Serialization:");
   js.Clear();
   out=""; js.Serialize(out);
//---
   js["Test"]=1.4;
   out=""; js.Serialize(out); Print(out);
//---
   Print("JASon Example Array access:");
   js["DirAccess"][0]=-1;
   js["DirAccess"][1]=22;
   string a[] = {"test", "add", "to array"};
   for (int i=0; i<3; ++i) js["ArrayAdd"].Add(a[i]);
   CJAVal* js_ac=js["ArrayCopy"];  // create element 'ArrayCopy' first
   js_ac.Set(js["DirAccess"].m_e);

   out=""; js.Serialize(out); Print(out);
//---
   CJAVal jb;
   jb["JS"].Set(js);
   out=""; jb.Serialize(out,false);
   Print(out);
//---
   jb["Arr"].Add(js);
   out=""; jb.Serialize(out,false);
   Print(out);
//---
   jb["Arr"].Add(js);
   out=""; jb.Serialize(out,false);
   Print(out);
//---
   b=jb.Deserialize(out);
   Print("deserialize=",b);
  }
//+------------------------------------------------------------------+
