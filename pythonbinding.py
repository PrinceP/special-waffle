import ctypes
from ctypes import *
class SimpleMQData(Structure):
    _fields_ = [("data",POINTER(POINTER(c_char))),
                ("length",POINTER(c_int)),
                ("count", c_int),
                ("usrDataIdx", c_int),
                ("msgCtxt", c_void_p)] 
class SimpleMQConfig(Structure):
    _fields_ = [("nodename",POINTER(c_char))]
class SimpleMQPort(Structure):
    _fields_ = [("portname",POINTER(c_char)),
                ("porttype",POINTER(c_char)),
                ("portinfo",c_void_p)]



name = create_string_buffer(b"testnode")
mq_type=create_string_buffer(b"zmq")
port_info = create_string_buffer(b"{\"port\": \"output\", \"type\": \"producer\", \"zmq\": {\"addresses\": [\"tcp://127.0.0.1:5100\"], \"connection\": \"bind\", \"socketType\" : \"PUB\"}}")
config = SimpleMQConfig(name)
mqcontext=ctypes.c_void_p()
mqData=SimpleMQData(None,None,0,0,None)

print(config.nodename[0])



simplemqlibrary = ctypes.cdll.LoadLibrary('/opt/SimpleMQ/libs/libSimpleMQ.so')
# int  simpleMQPortConnect(void *mqCtxt, SimpleMQPort *mqPort);
simpleMQPortConnected = simplemqlibrary.simpleMQPortConnected
simpleMQPortConnected.argtypes = [c_void_p,POINTER(c_char)]	
simpleMQPortConnected.restype = c_int
name = create_string_buffer(b"5100")

#int  simpleMQPortConnect(void *mqCtxt, SimpleMQPort *mqPort)
simpleMQPortConnect = simplemqlibrary.simpleMQPortConnect
simpleMQPortConnect.argtypes = [c_void_p,POINTER(SimpleMQPort)]
simpleMQPortConnect.restype = c_int
# void *NewSimpleMQ(const char *mqType, void *mqConfig);
NewSimpleMQ = simplemqlibrary.NewSimpleMQ
NewSimpleMQ.argtypes = [c_char_p,c_void_p]
NewSimpleMQ.restype = c_void_p
# int  DeleteSimpleMQ(void *mqCtxt);

DeleteSimpleMQ = simplemqlibrary.DeleteSimpleMQ
DeleteSimpleMQ.argtypes = [c_void_p]
DeleteSimpleMQ.restype = c_int

# void DeleteSimpleMQData(SimpleMQData* data);
DeleteSimpleMQData = simplemqlibrary.DeleteSimpleMQData
DeleteSimpleMQData.argtypes = [POINTER(SimpleMQData)]
DeleteSimpleMQData.restype = None
#SimpleMQData* NewSimpleMQData(int count, ...);
NewSimpleMQData = simplemqlibrary.NewSimpleMQData
NewSimpleMQData.restype = POINTER(SimpleMQData)
#int simpleMQSend(void *mqCtxt, char* port, SimpleMQData *data);
simpleMQSend = simplemqlibrary.simpleMQSend
simpleMQSend.argtypes=[c_void_p,c_char_p,POINTER(SimpleMQData)]
simpleMQSend.restype=c_int
#int simpleMQRecv(void *mqCtxt, char* port, SimpleMQData **data);
simpleMQRecv = simplemqlibrary.simpleMQRecv
simpleMQRecv.argtypes=[c_void_p,c_char_p,POINTER(POINTER(SimpleMQData))]
simpleMQRecv.restype=c_int
#SimpleMQPort *NewZMQPort(const char *json_str)
NewZMQPort = simplemqlibrary.NewZMQPort
NewZMQPort.argtypes=[c_char_p]
NewZMQPort.restype=POINTER(SimpleMQPort)
mqPortPointer = NewZMQPort(port_info)

print(mqPortPointer)
mqData = NewSimpleMQData(2,name,5,name,5)

# int  simpleMQPortRegMsgHandler(void *mqCtxt, char* channel, SimpleMQMsgHandler msgHandler);

#SimpleMQPortRegMsgHandler = simplemqlibrary.simpleMQPortRegMsgHandler;
mqcontext = NewSimpleMQ(mq_type,ctypes.byref(config))
result_portconnect = simpleMQPortConnect(mqcontext,mqPortPointer)
print(result_portconnect)

result2=simpleMQSend(mqcontext,name,mqData)
result3=simpleMQRecv(mqcontext,name,byref(mqData))
result = simpleMQPortConnected(mqcontext,name)
result1 = DeleteSimpleMQ(mqcontext)

#DeleteSimpleMQData(ctypes.byref(mqData))
DeleteSimpleMQData(mqData)

print(result,result1,result2)

