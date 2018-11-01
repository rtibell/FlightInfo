from time import gmtime, strftime
from datetime import datetime
from datetime import timedelta
from datetime import date
import uuid

class FlightInfo:
    DEBUG = False

    def __init__(self, msg = None):
        if self.DEBUG:
            self.rawDataDict = {}
        self.sid = None # 2
        self.aid = None # 3
        self.hex = None # 4
        self.fid = None # 5
        self.cs = None # 10
        self.alt = None # 11
        self.gs = None # 12
        self.trk = None # 13
        self.lat = None # 14
        self.lng = None # 15
        self.vr = None # 16
        self.sq = -1 # 17
        self.alrt = -1 # 18
        self.emer = -1 # 19
        self.spi = -1 # 20
        self.gnd = -1 # 21
        self.created = None
        self.updated = None
        self.rec_created = self.getCurrTime()
        self.rec_updated = None
        self.oldchecksum = self.checksum(self.toChkString())
        self.tm_created = None
        self.path_id = uuid.uuid4()
        self.new_path = True
        #self.flight_dict = {}
        if msg is not None:
            self.addMessage(msg)

    def addMessage(self, msg):
        if msg is not None:
            self.oldchecksum = self.checksum(self.toChkString())
            if self.DEBUG:
                self.rawDataDict[msg[0]] = msg
            self.switchOnInfoType(msg)
            self.rec_updated = self.getCurrTime()
            date_time_created = datetime.strptime(self.rec_created, '%Y-%m-%d %H:%M:%S.%f')
            dt_now = datetime.now()
            nxt_created = date_time_created + timedelta(0,60*15)
            self.tm_created = date_time_created
            timediff = nxt_created - dt_now
            #print("hex: " + str(self.hex) + " cs: " + str(self.cs) + " diff: " + str(timediff.seconds) + " now:" + dt_now.strftime("%Y-%m-%d %H:%M:%S.%f") + "  created: " + nxt_created.strftime("%Y-%m-%d %H:%M:%S.%f"))
            if timediff.days < 0:
                if self.DEBUG:
                    print("now:" + dt_now.strftime("%Y-%m-%d %H:%M:%S.%f") + "  created: " + nxt_created.strftime("%Y-%m-%d %H:%M:%S.%f"))
                self.path_id = uuid.uuid4()
                self.rec_created = self.getCurrTime()
            

    def isRecordChanged(self):
        if self.cs == None:
            return False
        if self.alt == None:
            return False
        if self.lat == None:
            return False
        if self.lng == None:
            return False
        if self.trk == None:
            return False
        if self.oldchecksum == self.checksum(self.toChkString()):
            return False
        else:
            return True

    def dataWritten(self):
        self.new_path = False


    def switchOnInfoType(self, msg):
        switcher = {
            "SEL": self.doSEL,
            "ID":  self.doID,
            "AIR": self.doAIR,
            "STA": self.doSTA,
            "CLK": self.doCLK,
            "MSG": self.doMSG
        }
        switcher.get(msg[0], lambda mt: "Invalide information type msg:" + mt)(msg)
   
    def doSEL(self, msg):
        print('SEL n/a msg=', msg)

    def doID(self, msg):
        print('SEL n/a msg=', msg)

    def doAIR(self, msg):
        print('SEL n/a msg=', msg)

    def doSTA(self, msg):
        print('SEL n/a msg=', msg)

    def doCLK(self, msg):
        print('SEL n/a msg=', msg)

    def doMSG(self, msg):
        self.switchOnMsgType(msg)

    def switchOnMsgType(self, msg):
        switcher = {
            "1": self.doMSG_1,
            "2": self.doMSG_2,
            "3": self.doMSG_3,
            "4": self.doMSG_4,
            "5": self.doMSG_5,
            "6": self.doMSG_6,
            "7": self.doMSG_7,
            "8": self.doMSG_8,
        }
        switcher.get(msg[1], lambda: "Invalide message type")(msg)

    def doMSG_1(self, msg):
        #print('doing msg of type 1: ', msg)
        self.setBase(msg)
        self.cs = msg[10] if len(msg[10]) > 0 else self.cs

    def doMSG_2(self, msg):
        #print('doing msg of type 2: ', msg)
        self.setBase(msg)
        self.alt = msg[11] if len(msg[11]) > 0 else self.alt
        self.gs = msg[12] if len(msg[12]) > 0 else self.gs
        self.trk = msg[13] if len(msg[13]) > 0 else self.trk
        self.lat = msg[14] if len(msg[14]) > 0 else self.lat
        self.lng = msg[15] if len(msg[15]) > 0 else self.lng
        self.gnd = msg[21] if len(msg[21]) > 0 else self.gnd

    def doMSG_3(self, msg):
        #print('doing msg of type 3: ', msg)
        self.setBase(msg)
        self.alt = msg[11] if len(msg[11]) > 0 else self.alt
        self.lat = msg[14] if len(msg[14]) > 0 else self.lat
        self.lng = msg[15] if len(msg[15]) > 0 else self.lng
        self.alrt = msg[18] if len(msg[18]) > 0 else self.alrt
        self.emer = msg[19] if len(msg[19]) > 0 else self.emer
        self.spi = msg[20] if len(msg[20]) > 0 else self.spi
        self.gnd = msg[21] if len(msg[21]) > 0 else self.gnd

    def doMSG_4(self, msg):
        #print('doing msg of type 4: ', msg)
        self.setBase(msg)
        self.gs = msg[12] if len(msg[12]) > 0 else self.gs
        self.trk = msg[13] if len(msg[13]) > 0 else self.trk
        self.vr = msg[16] if len(msg[16]) > 0 else self.vr

    def doMSG_5(self, msg):
        #print('doing msg of type 5: ', msg)
        self.setBase(msg)
        self.alt = msg[11] if len(msg[11]) > 0 else self.alt
        self.alrt = msg[18] if len(msg[18]) > 0 else self.alrt
        self.spi = msg[20] if len(msg[20]) > 0 else self.spi
        self.gnd = msg[21] if len(msg[21]) > 0 else self.gnd

    def doMSG_6(self, msg):
        #print('doing msg of type 6: ', msg)
        self.setBase(msg)
        self.alt = msg[11] if len(msg[11]) > 0 else self.alt
        self.sq = msg[17] if len(msg[17]) > 0 else self.sq
        self.alrt = msg[18] if len(msg[18]) > 0 else self.alrt
        self.emer = msg[19] if len(msg[19]) > 0 else self.emer
        self.spi = msg[20] if len(msg[20]) > 0 else self.spi
        self.gnd = msg[21] if len(msg[21]) > 0 else self.gnd

    def doMSG_7(self, msg):
        #print('doing msg of type 7: ', msg)
        self.setBase(msg)
        self.alt = msg[11] if len(msg[11]) > 0 else self.alt
        self.gnd = msg[21] if len(msg[21]) > 0 else self.gnd

    def doMSG_8(self, msg):
        #print('doing msg of type 8: ', msg)
        self.setBase(msg)
        self.gnd = msg[21] if len(msg[21]) > 0 else self.gnd

    def setBase(self, msg):
        self.sid = msg[2] if len(msg[2]) > 0 else self.sid
        self.aid = msg[3] if len(msg[3]) > 0 else self.aid
        self.hex = msg[4] if len(msg[4]) > 0 else self.hex
        self.fid = msg[5] if len(msg[5]) > 0 else self.fid
        created = msg[6].replace("/", "-") + " " + msg[7] 
        self.created = created if len(created) > 20 else self.created
        updated = msg[8].replace("/", "-") + " " + msg[9] 
        self.updated = updated if len(updated) > 20 else self.updated

    @staticmethod
    def toCSVHeadString():
        str1 = 'sid;aid;hex;fid;cs;alt;gs;trk;lat;lan;vr;sq;alrt;emer;spi;gnd;rec_created;rec_updated;'
        return str1

    def toCSVString(self):
        str1 = '{};{};{};{};{};{};{};{};'.format(self.sid, self.aid, self.hex, self.fid, self.cs, self.alt, self.gs, self.trk)
        str2 = '{};{};{};{};{};{};{};{};'.format(self.lat, self.lng, self.vr, self.sq, self.alrt, self.emer, self.spi, self.gnd)
        str3 = '{};{};{};{}'.format(self.created, self.updated,self.rec_created, self.rec_updated)
        return str1 + ' ' + str2 + ' ' + str3

    def toSQLString(self):
        cmd1 = 'insert into flightinfo '
        cmd2 = '(sid, aid, hex, fid, cs, alt, gs, trk,'
        cmd3 = 'lat, lan, vr, sq, alrt, emer, spi, gnd,'
        cmd4 = 'created, updated, rec_created, rec_updated, path_id, new_path) values('
        str1 = '{}, {}, "{}", {}, "{}", {}, {}, {}, '.format(self.sid, self.aid, self.hex, self.fid, self.cs, self.alt, self.gs, self.trk)
        str2 = '"{}", "{}", {}, {}, {}, {}, {}, {}, '.format(self.lat, self.lng, self.vr, self.sq, self.alrt, self.emer, self.spi, self.gnd)
        str3 = '"{}", "{}", '.format(self.created, self.updated)
        str4 = '"{}", "{}",'.format(self.rec_created, self.rec_updated)
        str5 = '"{}",{})'.format(self.path_id, self.new_path)
        cmd5 = ';'
        return cmd1 + ' ' + cmd2 + ' ' + cmd3 + ' ' + cmd4 + ' ' + str1 + ' ' + str2 + ' ' + str3 + ' ' + str4 + ' ' + str5 + cmd5

    def toString(self):
        str1 = 'sid={} aid={} hex={} fid={} cs={} alt={} gs={} trk={}'.format(self.sid, self.aid, self.hex, self.fid, self.cs, self.alt, self.gs, self.trk)
        str2 = 'lat={} lan={} vr={} sq={} alrt={} emer={} spi={} gnd={}'.format(self.lat, self.lng, self.vr, self.sq, self.alrt, self.emer, self.spi, self.gnd)
        str3 = 'created={} updated={}'.format(self.created, self.updated)
        str4 = 'rec_created={} rec_updated={} path_id={} new_path={}'.format(self.rec_created, self.rec_updated, self.path_id, self.new_path)
        return str1 + ' ' + str2 + ' ' + str3 + ' ' + str4

    def toChkString(self):
        str1 = 'hex={} cs={} alt={} trk={}'.format(self.hex, self.cs, self.alt, self.trk)
        str2 = 'lat={} lan={}'.format(self.lat, self.lng)
        return str1 + ' ' + str2


    def toDict(self):
        message = {}
        message['sid'] = self.sid
        message['aid'] = self.aid
        message['hex'] = self.hex
        message['fid'] = self.fid
        message['cs'] = self.cs
        message['alt'] = self.alt
        message['gs'] = self.gs
        message['trk'] = self.trk
        message['lat'] = self.lat
        message['lng'] = self.lng
        message['vr'] = self.vr
        message['sq'] = self.sq
        message['alrt'] = self.alrt
        message['emer'] = self.emer
        message['spi'] = self.spi
        message['gnd'] = self.gnd
        message['rec_created'] = self.rec_created
        message['rec_updated'] = self.rec_updated
        return message


    def prt(self):
        print('sid={} aid={} hex={} fid={} cs={} alt={} gs={} trk={}'.format(self.sid, self.aid, self.hex, self.fid, self.cs, self.alt, self.gs, self.trk))
        print('lat={} lan={} vr={} sq={} alrt={} emer={} spi={} gnd={}'.format(self.lat, self.lng, self.vr, self.sq, self.alrt, self.emer, self.spi, self.gnd))
        print('rec_created={} rec_updated={}'.format(self.rec_created, self.rec_updated))

    # returns total as checksum
    # input - string
    def checksum(self, st):
        chk = '%4X' % (-(sum(ord(c) for c in st) % (256*256)) & 0xFFFF)
        return chk

    def getCurrTime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 

    def getCurrTimeCompact(self):
        return datetime.now().strftime("%Y%m%d-%H:%M:%S.%f") 

