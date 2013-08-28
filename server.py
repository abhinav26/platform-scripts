import SimpleHTTPServer, SocketServer
import urlparse
import subprocess
import os
import webbrowser

PORT = 8000
PASSWORD="unlock\n"

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def do_GET(self):
    parsedParams = urlparse.urlparse(self.path)
    queryParsed = urlparse.parse_qs(parsedParams.query)
    if parsedParams.path == "/start":
      self.start(queryParsed)
    elif parsedParams.path == "/stop":
      self.stop(queryParsed)
    elif parsedParams.path == "/cleanup":
      self.clean()
    else:
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self);

  def start(self, query):
    if 'browser' not in query:
      self.wfile.write("No browser specified");
      return 
    browser_name = query['browser'][0];
    if 'proxy' in query and query['proxy'][0]=='true':
      command = "sudo -S networksetup -setsecurewebproxy \"Wi-Fi\" localhost 8080"
      os.popen("sudo -S %s"%(command), 'w').write(PASSWORD)
      command = "sudo -S networksetup -setwebproxy \"Wi-Fi\" localhost 8080"
      os.popen("sudo -S %s"%(command), 'w').write(PASSWORD)

    self.wfile.write("Start Request for "+browser_name);

    if browser_name == "firefox":
      os.system("cp -r /Users/abhinav/Library/Application\ Support/Firefox/Profiles/ ~/abhinav/server/temp/")
    elif browser_name == "safari":
      os.system("cp -r ~/Library/Safari ~/abhinav/server/temp/")
    url = "http://google.com"
    if browser_name == "chrome":
      os.system("cp -r ~/Library/Application\ Support/Google/Chrome/Default ~/abhinav/server/temp/")
      chrome_path = "/Applications/Google\ Chrome.app"
      os.system("open "+chrome_path+" "+url)
    else:
      controller = webbrowser.get(browser_name).open('http://www.google.com')

  def clean(self):
    self.wfile.write("Cleanup Request");

    print "cleanup Firefox"
    os.system("rm -rf /Users/abhinav/Library/Application\ Support/Firefox/Profiles/cv3v4zkh.default-1377504414332/*")
    os.system("cp -r ~/abhinav/server/temp/cv3v4zkh.default-1377504414332 /Users/abhinav/Library/Application\ Support/Firefox/Profiles/")
    print "cleanup Safari"
    os.system("rm -rf ~/Library/Safari/*")
    os.system("cp -r ~/abhinav/server/temp/Safari ~/Library/")
    print "cleanup Chrome"
    os.system("rm -rf ~/Library/Application\ Support/Google/Chrome/Default/*")
    os.system("cp -r ~/abhinav/server/temp/Default ~/Library/Application\ Support/Google/Chrome/")
    command ="networksetup -setsecurewebproxystate \"Wi-Fi\" off"
    os.popen("sudo -S %s"%(command), 'w').write(PASSWORD)
    command ="networksetup -setwebproxystate \"Wi-Fi\" off"
    os.popen("sudo -S %s"%(command), 'w').write(PASSWORD)


  def stop(self, query) :
    if 'browser' not in query:
      self.wfile.write("No browser specified");
      return 
    browser_name = query['browser'][0];
    self.wfile.write("Stop Request for "+browser_name);
    print "ps ax | grep -i " + browser_name + " | grep -v grep | awk '{ print $1 }' | xargs kill -9"
    os.system("ps ax | grep -i " + browser_name + " | grep -v grep | awk '{ print $1 }' | xargs kill -9")


Handler = MyHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
