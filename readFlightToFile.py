import socket
from datetime import datetime
from FlightInfo import FlightInfo


INET_ADDRESS="localhost"
INET_SOCKET=30003

global dict

dict = {}

def main():
    curTime = getCurrTimeCompact()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((INET_ADDRESS,INET_SOCKET))
    outf = open("flightFile_" + curTime +".dat","w+")
    while True:
        obj = rdData(s)
        if obj is None:
            break
        if obj.isRecordChanged():
            print("change", obj.toString())
            outf.write(obj.toString() + "\n")
    s.close()
    outf.close()
    print('Final')
    print('=====')
    outDict = open("flightDict" + ".dat","a+")
    for k in dict.keys():
        outDict.write(dict[k].toString() + "\n")
        print(dict[k].toString())
    outDict.close()
    print('Done!')

def rdData(s):
    data = s.recv(1024)
    obj = None
    if len(data) == 0:
        return None
    lst = data.decode("utf-8").rstrip().split(',')
    ky = lst[4]
    if ky in dict.keys():
        obj = dict[ky]
        obj.addMessage(lst)
    else:
        obj = FlightInfo(lst)
        dict[ky] = obj
    return obj

def getCurrTimeCompact():
    return datetime.now().strftime("%Y%m%d-%H:%M:%S")


if __name__ == "__main__":
    main()
