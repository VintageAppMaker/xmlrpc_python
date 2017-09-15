# -*- coding: cp949 -*-
import xmlrpclib
import base64
import os 

def encode(s):
    return base64.b64encode(s)

def decode(s):
    return base64.b64decode(s)

def main():
    proxy = xmlrpclib.ServerProxy("http://localhost:9090")
    os.system("cls")

    print ">>Backup download(zipfile=backup.zip)" 
    handle = open("backup.zip", "wb")
    handle.write(proxy.backup().data)
    handle.close()
    print "--------------------------" 

    print ">>file save(test.cfg)"
    print proxy.save(encode("test.cfg"), encode("msg=테스트입니다. 12329 aa") )
    print "--------------------------" 
    
    print ">>file view(a.txt)" 
    print decode ( proxy.view(encode("a.txt") ))
    print "--------------------------" 

    print ">>File list(txt, cfg, log)" 
    slist = decode(proxy.listfile())
    print slist
    print "--------------------------" 

    sarray = slist.split("\r\n") 
    sdelete = ""
    for s in sarray:
        if s.find(".zip") > 0:
            sdelete = s 

    print ">>file delete(%s)" % sdelete
    print sdelete
    print proxy.delete(encode(sdelete) )
    print "--------------------------" 

if __name__ == "__main__":
    main()
