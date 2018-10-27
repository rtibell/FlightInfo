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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((INET_ADDRESS,INET_SOCKET))
    outfDat = open("flightFile_" + curTime +".dat","w+")
    outfLog = open("flightFile_" + curTime +".log","w+")
    outfCSV = open("flightFile_" + curTime +".csv","w+")
    outfSQL = open("flightFile_" + curTime +".sql","w+")
    outfCSV.write(FlightInfo.toCSVHeadString() + "\n")
    while True:
        data = s.recv(1024)
        outfLog.write(data + "\n")
        obj = rdData(data)
        if obj is None:
            break
        if obj.isRecordChanged():
            #print("change", obj.toString())
            outfDat.write(obj.toString() + "\n")
            outfCSV.write(obj.toCSVString() + "\n")
            outfSQL.write(obj.toSQLString() + "\n")
            writeToDB(obj.toSQLString())
    s.close()
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
