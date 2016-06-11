from bs4 import BeautifulSoup
from subprocess import call
from gi.repository import Notify
import urllib, urllib2

daytse = 'http://dayt.se/watch/game-of-thrones/s6/e6'
req = urllib2.Request(daytse, headers={ 'User-Agent': 'Mozilla/5.0' })
httpResponse = urllib2.urlopen(req)
if httpResponse.code == 200 :
	print "[+] Web page was downloaded successfully\n"
else :
	print "[+] There was an error in downloading the page\n"
html = httpResponse.read()
bs = BeautifulSoup(html,"lxml")
for link in bs.find_all('a') :
    if "torrent" in link['href']:
        url = link['href']
        print link['href']
    else:
        pass

file_name = url.split('/')[-1]
u = urllib2.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()
Notify.init("Transmission")
Notify.Notification.new("Torrent Successfully Downloaded!!").show()

print "[+] Firing up Torrent downloader!!\n"
call(["xdg-open", file_name])
Notify.Notification.new("Mr.Hamza you torrent is downloading").show()
Notify.uninit()
