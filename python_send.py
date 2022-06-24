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
test_data = create_string_buffer(b"test_simplemq")
mq_type=create_string_buffer(b"zmq")
port_info = create_string_buffer(b"{\"port\": \"output\", \"type\": \"producer\", \"zmq\": {\"addresses\": [\"tcp://127.0.0.1:5003\"], \"connection\": \"bind\", \"socketType\" : \"PUB\"}}")
config = SimpleMQConfig(name)
mqcontext=ctypes.c_void_p()
simplemqlibrary = ctypes.cdll.LoadLibrary('/opt/SimpleMQ/libs/libSimpleMQ.so')
#SimpleMQData* NewSimpleMQData(int count, ...);
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
#int simpleMQSend(void *mqCtxt, char* port, SimpleMQData *data);
simpleMQSend = simplemqlibrary.simpleMQSend
simpleMQSend.argtypes=[c_void_p,c_char_p,POINTER(SimpleMQData)]
simpleMQSend.restype=c_int
#SimpleMQPort *NewZMQPort(const char *json_str)


DeleteSimpleMQ = simplemqlibrary.DeleteSimpleMQ
DeleteSimpleMQ.argtypes = [c_void_p]
DeleteSimpleMQ.restype = c_int


DeleteSimpleMQData = simplemqlibrary.DeleteSimpleMQData
DeleteSimpleMQData.argtypes = [POINTER(SimpleMQData)]
DeleteSimpleMQData.restype = None


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
while(1):
    #NewSimpleMQData = simplemqlibrary.NewSimpleMQData
    #NewSimpleMQData.restype = POINTER(SimpleMQData)
    mqData = NewSimpleMQData(2,test_data,13,test_data,13)
    #mqData = NewSimpleMQData(1,test_data,13)

    result2=simpleMQSend(mqcontext,create_string_buffer(b"output"),mqData)
    
    print('Send status is ')
    print(result2)
    print('\n')
    jsondata = mqData[0].data[0]
    json_length = mqData[0].length[0]
    json_string = jsondata[:json_length]
    print(json_string)

    DeleteSimpleMQData(mqData)

