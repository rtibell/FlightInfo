import socket
from datetime import datetime
from FlightInfo import FlightInfo
import MySQLdb as db

INET_ADDRESS="localhost"
INET_SOCKET=30003

global dict

dict = {}

def main():
    curTime = getCurrTimeCompact()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((INET_ADDRESS,INET_SOCKET))
    outfDat = open("flightFile_" + curTime +".dat","w+")
    outfLog = open("flightFile_" + curTime +".log","w+")
    outfCSV = open("flightFile_" + curTime +".csv","w+")
    outfSQL = open("flightFile_" + curTime +".sql","w+")
    outfCSV.write(FlightInfo.toCSVHeadString() + "\n")
    while True:

        for line in readlines(sock):
            data = line
            outfLog.write("|" + data + "|")
            obj = rdData(data)
            if obj is None:
                outfLog.write("None|" + "\n")
                break
            if obj.isRecordChanged():
                outfLog.write("Changed|" + "\n")
                #print("change", obj.toString())
                outfDat.write(obj.toString() + "\n")
                outfCSV.write(obj.toCSVString() + "\n")
                outfSQL.write(obj.toSQLString() + "\n")
                writeToDB(obj.toSQLString())
            else:
                outfLog.write("Not changed|" + "\n")
            
    sock.close()
    outfDat.close()
    outfLog.close()
    outfCSV.close()
    outfSQL.close()
    print('Final')
    print('=====')
    outDict = open("flightDict" + ".dat","a+")
    for k in dict.keys():
        outDict.write(dict[k].toString() + "\n")
        print(dict[k].toString())
    outDict.close()
    print('Done!')


def readlines(sock, recv_buffer=4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data
        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            yield line
    return


def writeToDB(sqlstring):
    cnx = db.Connection(user='d35632-flight', passwd='LuckyStr1ke',
                                 host='mysql7.space2u.com',
                                 db='d35632_flight')
    curs = cnx.cursor()
    curs.execute(sqlstring)
    cnx.commit()
    cnx.close()

def rdData(data):
    obj = None
    if len(data) == 0:
        return None
    lst = data.decode("utf-8").rstrip().replace('\n','').replace('\r','').split(',')
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
