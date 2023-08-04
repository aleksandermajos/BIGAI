using System;
using System.Linq;
using cAlgo.API;
using cAlgo.API.Indicators;
using cAlgo.API.Internals;
using cAlgo.Indicators;
using NetMQ;
using NetMQ.Sockets;
using System.Text;
using Newtonsoft.Json.Linq;

namespace cAlgo
{
    public partial class QUANTMAVERICK : Robot
    {
        public string ChartName(string uSymbol, int iPeriod, string iWindowId)
        {
            

            string TF = "";
            if (TimeFrame.ToString() == "Hour")
                TF = "60";

            string uRetval = "{";
            uRetval += "\"Terminal\":" + "\"CTRADER\""+",";
            uRetval += "\"Broker\":" + "\"" + Account.BrokerName + "\"" + ",";
            uRetval += "\"Symbol\":" + "\"" + Symbol.Code.ToString().Substring(0,6) + "\"" + ",";
            uRetval += "\"Period\":" + "\"" + TF + "\"" + ",";
            uRetval += "\"WindowID\":" + "\"" + iWindowId + "\"";
            uRetval += "}";
            return (uRetval);
        }

        public string Price(string uSymbol)
        {
            string ti = "";
            ti = this.Server.Time.Year + "-";
            if (this.Server.Time.Month.ToString().Length == 1) ti = ti + "0" + this.Server.Time.Month + "-";
            else ti = ti + this.Server.Time.Month + "-";
            if (this.Server.Time.Day.ToString().Length == 1) ti = ti + "0" + this.Server.Time.Day + "T";
            else ti = ti + this.Server.Time.Day + " ";
            if (this.Server.Time.Hour.ToString().Length == 1) ti = ti + "0" + this.Server.Time.Hour + ":";
            else ti = ti + this.Server.Time.Hour + ":";
            if (this.Server.Time.Minute.ToString().Length == 1) ti = ti + "0" + this.Server.Time.Minute + ":";
            else ti = ti + this.Server.Time.Minute + ":";
            if (this.Server.Time.Second.ToString().Length == 1) ti = ti + "0" + this.Server.Time.Second + ".";
            else ti = ti + this.Server.Time.Second + ".";

            if (this.Server.Time.Millisecond.ToString().Length == 1) ti = ti + "00" + this.Server.Time.Millisecond;
            if (this.Server.Time.Millisecond.ToString().Length == 2) ti = ti + "0" + this.Server.Time.Millisecond;
            else ti = ti + this.Server.Time.Millisecond;
            this.utcNow = DateTime.UtcNow;
            string uRetval = "{";
            uRetval += "\"symbol\":" + "\""+ Symbol.Code.ToString().Substring(0, 6) + "\"" + ",";
            uRetval += "\"time\":" + "\"" +ti+"\"" + ",";
            uRetval += "\"bid\":" + Symbol.Bid + ",";
            uRetval += "\"ask\":" + Symbol.Ask + ",";
            uRetval += "\"volumen\":" + Symbol.VolumeMax;
            uRetval += "}";
            return (uRetval);
        }

        public string Portsnr(int SUBPUB, int REQREP)
        {
            string uRetval = "{";
            uRetval += "\"SubPubPort\":" + "2027" + ",";
            uRetval += "\"ReqRepPort\":" + "2028";
            uRetval += "}";
            return (uRetval);
        }

        public string AccountInformation()
        {
            string uRetval;
            uRetval = "{";
            uRetval += "\"status\":" + "\"ok\"" + ",";
            uRetval += "\"balance\":" + Account.Balance + ",";
            uRetval += "\"currency\":" + "\""+Account.Currency + "\"" + ",";
            uRetval += "\"equity\":" + Account.Equity + ",";
            uRetval += "\"margin\":" + Account.Margin + ",";
            uRetval += "\"server\":" + "\"h20.p.ctrader.com\"";
            uRetval += "}";
            return (uRetval);
        }

        public string InstrumentInfo(string uSymbol)
        {
            string uRetval;
            uRetval = "{";
            uRetval += "\"symbol\":" + "\"" + Symbol.Code + "\"" + ",";
            uRetval += "\"points\":" + 5 + ",";
            uRetval += "\"digits\":" + Symbol.Digits + ",";
            uRetval += "\"spread\":" + Symbol.Spread + ",";
            uRetval += "\"contract_size\":" + Symbol.LotSize + ",";
            uRetval += "\"min_volume\":" + Symbol.VolumeMin + ",";
            uRetval += "\"max_volume\":" + Symbol.VolumeMax + ",";
            uRetval += "\"swap_long\":" + "0" + ",";
            uRetval += "\"swap_short\":" + "0";
            uRetval += "}";
            return (uRetval);
        }

        public string History(string uSymbol)
        {
            string uRetval = "";
            uRetval += "Time,O,H,L,C,V\n";
            for (int i = 0; i < MarketSeries.Close.Count - 1; i++)
            {
                uRetval += MarketSeries.OpenTime[i] + ",";
                uRetval += MarketSeries.Open[i] + ",";
                uRetval += MarketSeries.High[i] + ",";
                uRetval += MarketSeries.Low[i] + ",";
                uRetval += MarketSeries.Close[i] + ",";
                uRetval += MarketSeries.TickVolume[i];
                uRetval += "\n";

            }
            return (uRetval);
        }

        public string Transactions(string uSymbol)
        {
            string uRetval = "";
            foreach (var position in Positions)
            {
                uRetval += "{";
                uRetval += "\"ticket\":" + "\"" + position.Label + "\"" + ",";
                uRetval += "\"price\":" + position.EntryPrice + ",";
                uRetval += "\"time\":" + "\"" + position.EntryTime + "\"" + ",";
                uRetval += "\"symbol\":" + "\"" + Symbol.Code.ToString().Substring(0, 6) + "\"" + ",";
                uRetval += "\"size\":" + position.Volume;
                uRetval += "}";
            }

            
            
            
            return (uRetval);
        }

        public string OpenTrans(string Message)
        {
            bool Opened = false;
            TradeType ope = new TradeType();
            JObject o = JObject.Parse(Message);
            string key = o.GetValue("key").ToObject<string>();
            string sym = o.GetValue("symbol").ToObject<string>();
            var symbol = MarketData.GetSymbol(sym);
            string operation = o.GetValue("operation").ToObject<string>();
            if (operation == "OP_SELL") ope = (TradeType)1;
            if (operation == "OP_BUY") ope = (TradeType)0;

            double vol = o.GetValue("volume").ToObject<double>();
            long volume = (long)(vol * 100000);

            double price = o.GetValue("price").ToObject<double>();
            double slippage = o.GetValue("slippage").ToObject<double>();
            int TP = o.GetValue("TP").ToObject<int>();
            int SL = o.GetValue("SL").ToObject<int>();

            TradeResult result = ExecuteMarketOrder(ope, symbol, volume,GenerateTicket());
            Opened = result.IsSuccessful;

            string uRetval = "";
            uRetval = "{";
            uRetval += "\"Result\":" + Opened;
            uRetval += "}";
            return uRetval;
        }

        public string CloseTrans(string Message)
        {
            bool Closed = false;
            JObject o = JObject.Parse(Message);
            string key = o.GetValue("key").ToObject<string>();
            string ticket = o.GetValue("ticket").ToObject<string>();
            double vol = o.GetValue("volume").ToObject<double>();
            long volume = (long)vol * 1000;
            double slippage = o.GetValue("slippage").ToObject<double>();

            var position = Positions.Find(ticket);
            TradeResult result = ClosePosition(position);
            Closed = result.IsSuccessful;

            string uRetval = "";
            uRetval = "{";
            uRetval += "\"Result\":" + Closed;
            uRetval += "}";
            return (uRetval);
        }

        string GenerateTicket()
        {
            var chars = "0123456789";
            var stringChars = new char[8];
            var random = new Random();

            for (int i = 0; i < stringChars.Length; i++)
            {
                stringChars[i] = chars[random.Next(chars.Length)];
            }

            var finalString = new String(stringChars);

            return finalString;
        }

    }
}
