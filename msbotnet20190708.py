#! /usr/bin/env python2.7
# encoding=utf8
# Auther: msbotnet 

import socket
import binascii
import sys
import os


payload = "030000130ee000000000000100080000000000030001d602f0807f658201940401010401010101ff30190204000000000204000000020204000000000204000000010204000000000204000000010202ffff020400000002301902040000000102040000000102040000000102040000000102040000000002040000000102020420020400000002301c0202ffff0202fc170202ffff0204000000010204000000000204000000010202ffff02040000000204820133000500147c0001812a000800100001c00044756361811c01c0d800040008008002e00101ca03aa09040000ce0e000048004f005300540000000000000000000000000000000000000000000000000004000000000000000c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ca010000000000100007000100300030003000300030002d003000300030002d0030003000300030003000300030002d003000300030003000300000000000000000000000000000000000000000000000000004c00c000d0000000000000002c00c001b0000000000000003c02c0003000000726470647200000000008080636c6970726472000000a0c0726470736e640000000000c00300000c02f08004010001000300000802f080280300000c02f08038000603ef0300000c02f08038000603eb0300000c02f08038000603ec0300000c02f08038000603ed0300000c02f08038000603ee0300000b06d00000123400"
def verify(sock, port):
    while 1:
        buff = sock.recv(2048)
        if not buff:
                break
        b = bytearray(buff)
        print "[+] %s" % binascii.hexlify(b)
        detect_os(binascii.hexlify(b), port)
def detect_os(res, port):
    d = {
            "2000": "0300000b06d00000123400",
            "2003": "030000130ed000001234000300080002000000",
            "2008": "030000130ed000001234000200080002000000",
            "win7OR2008R2": "030000130ed000001234000209080002000000",
            "2008R2DC": "030000130ed000001234000201080002000000"
    }
    for key, value in d.iteritems():
        if value == res:
            print "[+] RDP Port is %s" % port
            sys.exit(0)

def scan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        sys.stdout.write('[+] Check Port %s \r' % port)
        sys.stdout.flush()
        if s.connect_ex((ip, port)) == 0:
            print "[+] Connect Success %s" % port
            s.send("\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
            verify(s, port)
            s.sendall(payload.decode("hex"))
            print " msbotnet！"
    except Exception, e:
        # raise e
        pass
    finally:
        s.close()
        import platform
        # "打开mstsc"
        if(platform.system()=="Windows"):
            os.system("6d736874612076627363726970743a6d7367626f782822796f757220746172676574206c696b652063616978756b756e21222c36342c2262616c636b73756e40414e613a22292877696e646f772e636c6f736529".decode("hex"))
            os.system("6d737473632e657865".decode("hex"))

def msg():
    print "%s [ip] [3389]" % sys.argv[0]
    print "%s [ip] [port] " % sys.argv[0]
if __name__ == '__main__':
    ip = ""

    if len(sys.argv) < 2:
        msg()
        exit()

    if len(sys.argv) == 2:
        port = 3389
    else:
        port = int(sys.argv[2])

    if sys.argv[1] == None:
        msg()
    else:
        ip = sys.argv[1]
    scan(ip,port)
