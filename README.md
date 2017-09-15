# xmlrpc_python

Python xmlrpc를 이용한 서버설정 & data백업

[원본블로그](http://blog.naver.com/adsloader/50151040100)

![](/data/xmlrpc.gif)


- server

~~~python
# -*- coding: cp949 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import os 
import base64
import time
import sys
import zipfile

# zip 관리 클래스 
class ZipUtilities:

    def __init__ (self):
        pass

    def isOkFile(self, sName):
        if os.path.splitext(sName)[1].lower() in (".log", ".cfg", ".txt"):
            return True 
        else:
            return False 

    def toZip(self, path, filename):
        sname = path + "\\"+ filename

        zip_file = zipfile.ZipFile(sname, 'w', compression=zipfile.ZIP_DEFLATED)
        for f in os.listdir(path):
            if os.path.isfile(f):
	        if self.isOkFile(f): 
                    zip_file.write(f)
        
        zip_file.close()
    
    def MakeFileName(self, str):
        s = str
        now = time.localtime()
        wday = ("월", "화", "수", "목", "금", "토", "일")
        sName = "%s %d-%d-%d %d.%d.%d(%s).zip" % ( s, now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, wday[now.tm_wday])
        return sName

# log file을 삭제, 리스트업,  
class BackupManager:
    def __init__ (self):
	self.rootpath = os.getcwd()
	self.url  = "localhost"
	self.port = 9090 

    def encode(self, s):
        return base64.b64encode(s)
    
    def decode(self, s):
        return base64.b64decode(s)

    def delete(self, filename):
	print ">>delete remote call.(%s)" % self.decode(filename)
        os.unlink(self.decode(filename))
        return ""

    def view(self, filename):
	print ">>view remote call.(%s)" % self.decode(filename)
	f = open(self.decode(filename), "r")
	s = f.read()
	f.close()
        return self.encode(s) 	
    
    def backup(self):
	print ">>backup remote call."
        try:
            z = ZipUtilities()
	    s = z.MakeFileName("backup_")
	    z.toZip(self.rootpath, s)

	    handle =  open(s, "rb")
            return xmlrpclib.Binary(handle.read())
        
        except:
	    print "error during backup\r\n"

    def save(self, sName, sText):
	print ">>save remote call.(%s)" % self.decode(sName)
        try:
            
	    handle =  open(self.decode(sName), "wb")
	    handle.write(self.decode(sText))
            handle.close()

            return "" 
        
        except:
	    print "error during save\r\n"
	
    def listfile(self):
	print "listfile remote call."
	s = ""
        for file in os.listdir(self.rootpath):
	   s = s  + "\r\n"+ file

	return self.encode(s) 
    
    def run(self):
        server = SimpleXMLRPCServer((self.url, self.port))
        print "Listening on port %d..." % self.port
        
        # API 등록
        server.register_function(self.delete,   'delete')
        server.register_function(self.save  ,   'save')
        server.register_function(self.view  ,   'view')
        server.register_function(self.backup,   'backup')
        server.register_function(self.listfile, 'listfile')
        server.serve_forever()
     
def main():
    bm = BackupManager()
    bm.run()
    
if __name__ == "__main__":
    main()

~~~

- client

~~~python
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

~~~
