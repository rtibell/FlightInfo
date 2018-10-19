import socket
from FlightInfo import FlightInfo


INET_ADDRESS="localhost"
INET_SOCKET=30003

global dict

dict = {}

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((INET_ADDRESS,INET_SOCKET))
    outf = open("flightFile.dat","w")
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
    for k in dict.keys():
        print(dict[k].toString())
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



if __name__ == "__main__":
    main()
