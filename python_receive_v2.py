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

class mqAppCtxt(Structure):
    _fields_ = [("mqCtxt",c_void_p),
            ("gmPort",POINTER(SimpleMQPort)),
            ("mqConnectorCtxt",c_void_p),
            ("metricCollectorCtxt",c_void_p)]

##------------------------------------
g_mqAppCtxt = mqAppCtxt()
mqconnectorlibrary = ctypes.CDLL('/opt/MQConnector/libs/libMQConnector.so')
NewMQConnector = mqconnectorlibrary.NewMQConnector
NewMQConnector.argtypes = [c_char_p,c_void_p,c_void_p]
NewMQConnector.restype = c_void_p
DeleteMQConnector=mqconnectorlibrary.DeleteMQConnector
DeleteMQConnector.argtypes=[c_void_p]
DeleteMQConnector.restype=c_int
mqConnectorStart = mqconnectorlibrary.mqConnectorStart
mqConnectorStart.argtypes = [c_void_p]
mqConnectorStart.restype = c_int

#---------------------------------------



name = create_string_buffer(b"testnode1")
test_data = create_string_buffer(b"receive_test")
mq_type=create_string_buffer(b"zmq")
port_info = create_string_buffer(b"{\"port\": \"input\", \"type\": \"consumer\", \"zmq\": {\"addresses\": [\"tcp://127.0.0.1:5003\"], \"connection\": \"connect\", \"socketType\" : \"SUB\"}}")

config = SimpleMQConfig(name)
mqcontext=ctypes.c_void_p()
simplemqlibrary = ctypes.cdll.LoadLibrary('/opt/SimpleMQ/libs/libSimpleMQ.so')
NewSimpleMQData = simplemqlibrary.NewSimpleMQData
NewSimpleMQData.restype = POINTER(SimpleMQData)
mqData = NewSimpleMQData(2,test_data,13,test_data,13)


#int  simpleMQPortConnect(void *mqCtxt, SimpleMQPort *mqPort)
simpleMQPortConnect = simplemqlibrary.simpleMQPortConnect
simpleMQPortConnect.argtypes = [c_void_p,POINTER(SimpleMQPort)]
simpleMQPortConnect.restype = c_int


# void *NewSimpleMQ(const char *mqType, void *mqConfig);
NewSimpleMQ = simplemqlibrary.NewSimpleMQ
NewSimpleMQ.argtypes = [c_char_p,c_void_p]
NewSimpleMQ.restype = c_void_p


#int simpleMQRecv(void *mqCtxt, char* port, SimpleMQData **data);
simpleMQRecv = simplemqlibrary.simpleMQRecv
simpleMQRecv.argtypes=[c_void_p,c_char_p,POINTER(POINTER(SimpleMQData))]
simpleMQRecv.restype=c_int


DeleteSimpleMQData = simplemqlibrary.DeleteSimpleMQData
DeleteSimpleMQData.argtypes = [POINTER(SimpleMQData)]
DeleteSimpleMQData.restype = None



DeleteSimpleMQ = simplemqlibrary.DeleteSimpleMQ
DeleteSimpleMQ.argtypes = [c_void_p]
DeleteSimpleMQ.restype = c_int

#SimpleMQPort *NewZMQPort(const char *json_str)
NewZMQPort = simplemqlibrary.NewZMQPort
NewZMQPort.argtypes=[c_char_p]
NewZMQPort.restype=POINTER(SimpleMQPort)
mqPortPointer = NewZMQPort(port_info)
print(mqPortPointer)

mqcontext = NewSimpleMQ(mq_type,ctypes.byref(config))
result_portconnect = simpleMQPortConnect(mqcontext,mqPortPointer)


print('\nPort connect Status is')
print(result_portconnect)
print('\n')

#port_info = create_string_buffer(b"input")

while True:
    #mqData = NewSimpleMQData(2,test_data,13,test_data,13)
    #mqcontext = NewSimpleMQ(mq_type,ctypes.byref(config))
    #result_portconnect = simpleMQPortConnect(mqcontext,mqPortPointer)
    port_info = create_string_buffer(b"input")

    mqData = NewSimpleMQData(1,test_data,13)
    #result2 = simpleMQRecv(mqcontext,create_string_buffer(b"input"),ctypes.byref(mqData))
    result2 = simpleMQRecv(mqcontext,port_info,ctypes.byref(mqData))
    print('Recv status is ')
    print(result2)
    print('\n')
    
    DeleteSimpleMQData(mqData)
    #DeleteSimpleMQ(mqcontext)
    del port_info