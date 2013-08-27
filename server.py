import SimpleHTTPServer, SocketServer
import urlparse
import subprocess
import os
import webbrowser

PORT = 8000

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
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    browser_name = query['browser'][0];
    self.wfile.write("<h2>Start Request for "+browser_name+"</h2>");
    self.wfile.close();

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
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.wfile.write("<h2>Cleanup Request</h2>");
    self.wfile.close();

    print "cleanup Firefox"
    os.system("rm -rf /Users/abhinav/Library/Application\ Support/Firefox/Profiles/cv3v4zkh.default-1377504414332/*")
    os.system("cp -r ~/abhinav/server/temp/cv3v4zkh.default-1377504414332 /Users/abhinav/Library/Application\ Support/Firefox/Profiles/")
    print "cleanup Safari"
    os.system("rm -rf ~/Library/Safari/*")
    os.system("cp -r ~/abhinav/server/temp/Safari ~/Library/")
    print "cleanup Chrome"
    os.system("rm -rf ~/Library/Application\ Support/Google/Chrome/Default/*")
    os.system("cp -r ~/abhinav/server/temp/Default ~/Library/Application\ Support/Google/Chrome/")



  def stop(self, query) :
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    browser_name = query['browser'][0];
    self.wfile.write("<h2>Stop Request for "+browser_name+"</h2>");
    self.wfile.close();
    print "ps ax | grep -i "+browser_name+" | grep -v grep | awk '{ print $1 }' | xargs kill -9"
    os.system("ps ax | grep -i "+browser_name+" | grep -v grep | awk '{ print $1 }' | xargs kill -9")


Handler = MyHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()