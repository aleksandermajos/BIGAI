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
    [Robot(TimeZone = TimeZones.UTC, AccessRights = AccessRights.FullAccess)]
    public partial class QUANTMAVERICK : Robot
    {
        [Parameter(DefaultValue = 0.0)]
        public double Parameter { get; set; }
        static NetMQContext ctx = NetMQContext.Create();
        private NetMQSocket SOCPUB = ctx.CreatePublisherSocket();
        private NetMQSocket SOCREP = ctx.CreateResponseSocket();
        byte[] msgbyte;
        string msg = "";
        string msg_rcv = "";
        TimeSpan onems = TimeSpan.FromMilliseconds(1);
        int SUBPUB_PORT;
        int REQREP_PORT;
        object oko;
        string TO_SEND = "";
        string LAST_REQ = "";
        DateTime utcNow;
        string WindowID = "";

        string GenerateWindowID()
        {
            var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            var stringChars = new char[16];
            var random = new Random();

            for (int i = 0; i < stringChars.Length; i++)
            {
                stringChars[i] = chars[random.Next(chars.Length)];
            }

            var finalString = new String(stringChars);

            return finalString;
        }
        string ReqRepReply(string Message)
        {
            this.LAST_REQ = Message;
            string Result = "";
            if (Message.IndexOf("CHARTNAME") != -1)
                Result += ChartName(Symbol.ToString(), 240, this.WindowID);
            if (Message.IndexOf("PRICE") != -1)
                Result += Price(Symbol.ToString());
            if (Message.IndexOf("INSTRUMENTINFO") != -1)
                Result += InstrumentInfo(Symbol.ToString());
            if (Message.IndexOf("HISTORY") != -1)
                Result += History(Symbol.ToString());
            if (Message.IndexOf("ACCOUNTINFO") != -1)
                Result += AccountInformation();
            if (Message.IndexOf("TRANSACTIONS") != -1)
                Result += Transactions(Symbol.ToString());
            if (Message.IndexOf("OPEN") != -1)
                Result += OpenTrans(Message);
            if (Message.IndexOf("CLOSE") != -1)
                Result += CloseTrans(Message);
            msg = Result;
            return Result;

        }

        string Change_TO_SEND()
        {
            this.TO_SEND = ReqRepReply(this.LAST_REQ);
            return TO_SEND;
        }

        void Updete_TO_SEND()
        {
            this.TO_SEND = ReqRepReply("CHARTNAME.PRICE");
        }
        protected override void OnStart()
        {

            using (NetMQContext ctx0 = NetMQContext.Create())
            {
                using (var SUBLISTENERPORTS = ctx0.CreateSubscriberSocket())
                {
                    Print("IN CONSTRUCTION:");
                    string topic = "";
                    Chart chart;
                    this.oko = Symbol.Bid;
                    SUBLISTENERPORTS.Connect("tcp://localhost:2025");
                    SUBLISTENERPORTS.Subscribe(topic);
                    string messageTopicReceived = SUBLISTENERPORTS.ReceiveFrameString();
                    string messageReceived = SUBLISTENERPORTS.ReceiveFrameString();
                    this.msg = messageReceived;
                    string[] words = msg.Split(' ');
                    this.SUBPUB_PORT = System.Convert.ToInt32(words[2]);
                    this.REQREP_PORT = System.Convert.ToInt32(words[3]);
                    this.SOCPUB.Bind("tcp://*:" + this.SUBPUB_PORT);
                    this.SOCREP.Bind("tcp://*:" + this.REQREP_PORT);
                    this.WindowID = GenerateWindowID();
                    Timer.Start(1);
                }
            }
        }

        protected override void OnTick()
        {
            Updete_TO_SEND();
            Print("SENDING:");
            SOCPUB.Send(this.TO_SEND, dontWait: true);
            bool ok = SOCREP.TryReceiveFrameString(out this.msg_rcv);
            if (this.msg_rcv != null)
            {
                Print("Received new message!");
                this.TO_SEND = ReqRepReply(this.msg_rcv);
                SOCREP.Send(this.TO_SEND, dontWait: true);
                this.msg_rcv = null;
            }

        }
        protected override void OnTimer()
        {
            Updete_TO_SEND();
            Print("SENDING:");
            SOCPUB.Send(this.TO_SEND, dontWait: true);
            bool ok = SOCREP.TryReceiveFrameString(out this.msg_rcv);
            if (this.msg_rcv != null)
            {
                Print("Received new message!");
                this.TO_SEND = ReqRepReply(this.msg_rcv);
                SOCREP.Send(this.TO_SEND, dontWait: true);
                this.msg_rcv = null;
            }

        }
        protected override void OnStop()
        {

        }
    }


}
