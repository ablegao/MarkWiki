#coding:utf-8
import tornado.ioloop
import tornado.web
import markdown
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

Header = '''<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><title> MarkwWike</title></head>
<style>
body{margin:30px 100px;}
</style>
<body>'''

Footer = "</body><p>@copyright ablegao ,Markdown .  MarkwWike</p></html>"
class MainHandler(tornado.web.RequestHandler):
    def get(self):

        fileHeader = open("./index.md" )
        html = fileHeader.read()
        html = Header + markdown.markdown(html) + Footer
        self.write(html)


class ReadFileHandler(tornado.web.RequestHandler):
    def get(self , url):
        url = "./"+url
        if False == os.path.exists(url) :
            self.write(Header)
            self.write("什么都没有！")
            self.write(Footer)
            return
        fileHeader = open(url)
        html = fileHeader.read()
        html = Header + markdown.markdown(html) + Footer
        self.write(html)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/(.*\.md)$" , ReadFileHandler),
    (r"/(.*)$", tornado.web.StaticFileHandler, dict(path="./")),
    ])

if __name__ == "__main__":
    application.listen(1111)
    tornado.ioloop.IOLoop.instance().start()