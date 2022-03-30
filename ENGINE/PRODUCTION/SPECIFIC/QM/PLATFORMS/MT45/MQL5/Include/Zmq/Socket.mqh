//+------------------------------------------------------------------+
//|                                                       Socket.mqh |
//|                                          Copyright 2016, Li Ding |
//|                                            dingmaotu@hotmail.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2016, Li Ding"
#property link      "dingmaotu@hotmail.com"
#property strict

#include "Common.mqh"
#include "Context.mqh"
#include "SocketOptions.mqh"
#include "ZmqMsg.mqh"
//--- fd is SOCKET on Win32, which is defined as UINT_PTR
struct zmq_pollitem_t
  {
   intptr_t          socket;
   uintptr_t         fd;
   short             events;
   short             revents;
  };

//--- Socket types
#define ZMQ_PAIR 0
#define ZMQ_PUB 1
#define ZMQ_SUB 2
#define ZMQ_REQ 3
#define ZMQ_REP 4
#define ZMQ_DEALER 5
#define ZMQ_ROUTER 6
#define ZMQ_PULL 7
#define ZMQ_PUSH 8
#define ZMQ_XPUB 9
#define ZMQ_XSUB 10
#define ZMQ_STREAM 11

//--- Message options
#define ZMQ_MORE 1
#define ZMQ_SRCFD 2  // Deprecated
#define ZMQ_SHARED 3

//--- Send/recv options
#define ZMQ_DONTWAIT 1
#define ZMQ_SNDMORE 2

//--- Socket transport events (TCP, IPC and TIPC only)
#define ZMQ_EVENT_CONNECTED         0x0001
#define ZMQ_EVENT_CONNECT_DELAYED   0x0002
#define ZMQ_EVENT_CONNECT_RETRIED   0x0004
#define ZMQ_EVENT_LISTENING         0x0008
#define ZMQ_EVENT_BIND_FAILED       0x0010
#define ZMQ_EVENT_ACCEPTED          0x0020
#define ZMQ_EVENT_ACCEPT_FAILED     0x0040
#define ZMQ_EVENT_CLOSED            0x0080
#define ZMQ_EVENT_CLOSE_FAILED      0x0100
#define ZMQ_EVENT_DISCONNECTED      0x0200
#define ZMQ_EVENT_MONITOR_STOPPED   0x0400
#define ZMQ_EVENT_ALL               0xFFFF

//--- I/O multiplexing
#define ZMQ_POLLIN 1
#define ZMQ_POLLOUT 2
// We only use 0MQ sockets on Windows
// So POLLERR and POLLPRI is of no use
#define ZMQ_POLLERR 4
#define ZMQ_POLLPRI 8

#define ZMQ_POLLITEMS_DFLT 16

#import "libzmq.dll"
//+------------------------------------------------------------------+
//| Sockets                                                          |
//+------------------------------------------------------------------+
intptr_t zmq_socket(intptr_t context,int type);
int zmq_close(intptr_t s);
int zmq_bind(intptr_t s,const char &addr[]);
int zmq_connect(intptr_t s,const char &addr[]);
int zmq_unbind(intptr_t s,const char &addr[]);
int zmq_disconnect(intptr_t s,const char &addr[]);
int zmq_send(intptr_t s,const uchar &buf[],size_t len,int flags);
int zmq_send_const(intptr_t s,const uchar &buf[],size_t len,int flags);
int zmq_recv(intptr_t s,uchar &buf[],size_t len,int flags);
int zmq_socket_monitor(intptr_t s,const char &addr[],int events);
//+------------------------------------------------------------------+
//| Message                                                          |
//+------------------------------------------------------------------+
int zmq_msg_send(zmq_msg_t &msg,intptr_t s,int flags);
int zmq_msg_recv(zmq_msg_t &msg,intptr_t s,int flags);
//+------------------------------------------------------------------+
//| I/O multiplexing                                                 |
//+------------------------------------------------------------------+
int zmq_poll(zmq_pollitem_t &items[],int nitems,long timeout);
//+------------------------------------------------------------------+
//| Message proxying                                                 |
//+------------------------------------------------------------------+
int zmq_proxy(intptr_t frontend_ref,intptr_t backend_ref,intptr_t capture_ref);
int zmq_proxy_steerable(intptr_t frontend_ref,intptr_t backend_ref,intptr_t capture_ref,intptr_t control_ref);
#import
//+------------------------------------------------------------------+
//| Wraps a 0MQ socket                                               |
//+------------------------------------------------------------------+
class Socket: public SocketOptions
  {
public:
   //--- it is not recommended to use this constructor directly: use Context factory methods instead
                     Socket(const Context &ctx,int type):SocketOptions(zmq_socket(ctx.ref(),type)){}
   virtual          ~Socket() {if(0!=zmq_close(m_ref)){Debug(StringFormat("Failed to close socket 0x%0X",m_ref));}}

   // for better cooperation between objects
   intptr_t          ref() const {return m_ref;}

   bool              valid() const {return m_ref!=0;}

   //--- see Zmq::error() if any of the following command failed
   //--- connection management
   bool              bind(string addr);
   bool              unbind(string addr);
   bool              connect(string addr);
   bool              disconnect(string addr);

   //--- send and receive packets
   bool              recv(uchar &buf[],bool nowait=false);
   bool              send(const uchar &buf[],bool nowait=false,bool more=false);
   bool              sendConst(const uchar &buf[],bool nowait=false,bool more=false);

   bool              send(ZmqMsg &msg,bool nowait=false,bool more=false);
   bool              recv(ZmqMsg &msg,bool nowait=false);

   void              register(zmq_pollitem_t &pollitem,bool read=false,bool write=false);
   void              register(zmq_pollitem_t &pollitems[],int index,bool read=false,bool write=false);

   //--- monitor socket events
   bool              monitor(string addr,int events);

   //--- proxy
   static bool       proxy(Socket *frontend,Socket *backend,Socket *capture);
   static bool       proxySteerable(Socket *frontend,Socket *backend,Socket *capture,Socket *control);

   //--- poll
   static int        poll(zmq_pollitem_t &arr[],long timeout);
  };
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::bind(string addr)
  {
   char arr[];
   StringToUtf8(addr,arr);
   bool res=(0==zmq_bind(m_ref,arr));
   ArrayFree(arr);
   return res;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::unbind(string addr)
  {
   char arr[];
   StringToUtf8(addr,arr);
   bool res=(0==zmq_unbind(m_ref,arr));
   ArrayFree(arr);
   return res;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::connect(string addr)
  {
   char arr[];
   StringToUtf8(addr,arr);
   bool res=(0==zmq_connect(m_ref,arr));
   ArrayFree(arr);
   return res;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::disconnect(string addr)
  {
   char arr[];
   StringToUtf8(addr,arr);
   bool res=(0==zmq_disconnect(m_ref,arr));
   ArrayFree(arr);
   return res;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::recv(uchar &buf[],bool nowait=false)
  {
   int options=0;
   if(nowait) options|=ZMQ_DONTWAIT;
   return 0==zmq_recv(m_ref,buf,ArraySize(buf),options);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::send(const uchar &buf[],bool nowait=false,bool more=false)
  {
   int options=0;
   if(nowait) options|=ZMQ_DONTWAIT;
   if(more) options|=ZMQ_SNDMORE;
   return 0==zmq_send(m_ref,buf,ArraySize(buf),options);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::sendConst(const uchar &buf[],bool nowait=false,bool more=false)
  {
   int options=0;
   if(nowait) options|=ZMQ_DONTWAIT;
   if(more) options|=ZMQ_SNDMORE;
   return 0==zmq_send_const(m_ref,buf,ArraySize(buf),options);
  }
//+------------------------------------------------------------------+
//| Send a zmq_msg_t through a socket                                |
//+------------------------------------------------------------------+
bool Socket::send(ZmqMsg &msg,bool nowait=false,bool more=false)
  {
   int flags=0;
   if(nowait) flags|=ZMQ_DONTWAIT;
   if(more) flags|=ZMQ_SNDMORE;
   return -1!=zmq_msg_send(msg,m_ref,flags);
  }
//+------------------------------------------------------------------+
//| Receive a zmq_msg_t from a socket                                |
//+------------------------------------------------------------------+
bool Socket::recv(ZmqMsg &msg,bool nowait=false)
  {
   int flags=0;
   if(nowait) flags|=ZMQ_DONTWAIT;
   return -1!=zmq_msg_recv(msg,m_ref,flags);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::monitor(string addr,int events)
  {
   uchar str[];
   StringToUtf8(addr,str);
   bool res=(0==zmq_socket_monitor(m_ref,str,events));
   ArrayFree(str);
   return res;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void Socket::register(zmq_pollitem_t &pollitem,bool read=false,bool write=false)
  {
   ZeroMemory(pollitem);
   pollitem.socket=m_ref;
   if(read) pollitem.events|=ZMQ_POLLIN;
   if(write) pollitem.events|=ZMQ_POLLOUT;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void Socket::register(zmq_pollitem_t &pollitems[],int index,bool read=false,bool write=false)
  {
   ZeroMemory(pollitems[index]);
   pollitems[index].socket=m_ref;
   if(read) pollitems[index].events|=ZMQ_POLLIN;
   if(write) pollitems[index].events|=ZMQ_POLLOUT;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::proxy(Socket *frontend,Socket *backend,Socket *capture)
  {
   intptr_t frontend_ref= CheckPointer(frontend)==POINTER_DYNAMIC?frontend.ref():0;
   intptr_t backend_ref = CheckPointer(backend)==POINTER_DYNAMIC?backend.ref():0;
   intptr_t capture_ref=CheckPointer(capture)==POINTER_DYNAMIC?capture.ref():0;
   return 0==zmq_proxy(frontend_ref, backend_ref, capture_ref);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool Socket::proxySteerable(Socket *frontend,Socket *backend,Socket *capture,Socket *control)
  {
   intptr_t frontend_ref= CheckPointer(frontend)==POINTER_DYNAMIC?frontend.ref():0;
   intptr_t backend_ref = CheckPointer(backend)==POINTER_DYNAMIC?backend.ref():0;
   intptr_t capture_ref=CheckPointer(capture)==POINTER_DYNAMIC?capture.ref():0;
   intptr_t control_ref=CheckPointer(control)==POINTER_DYNAMIC?control.ref():0;
   return 0==zmq_proxy_steerable(frontend_ref, backend_ref, capture_ref, control_ref);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int Socket::poll(zmq_pollitem_t &arr[],long timeout)
  {
   return zmq_poll(arr,ArraySize(arr),timeout);
  }
//+------------------------------------------------------------------+
