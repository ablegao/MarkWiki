#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


import markdown
import web


sys.path.insert(0,os.path.join(os.path.dirname(__file__) ) )
PATH = os.path.dirname(__file__)

Header = '''<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><title> MarkwWike</title></head>
<style>
body{margin:30px 100px;}
</style>
<body>
<p><h1><a href="/">首页</a></h1></p>
'''

Footer = "</body><p>@copyright ablegao ,Markdown .  MarkwWike</p></html>"



urls = (
    '/', "MainHandler",
    '/(.*\.md)', 'ReadFileHandler',
    '/(.*)' , 'GetStaticFile',
)


class MainHandler:
    def GET(self):
        web.header('Content-Type', 'text/html')
        fileHeader = open(PATH + "/README.md" )
        html = fileHeader.read()
        html = Header + markdown.markdown(html) + Footer
        return html


class ReadFileHandler:
    def GET(self , url):
        web.header('Content-Type', 'text/html')
        url = PATH+"/"+url
        if False == os.path.exists(url) :
            html =  Header + "什么都没有~" + Footer
            return html
        fileHeader = open(url)
        html = fileHeader.read().replace("\n","\n\n")
        html = Header + markdown.markdown(html) + Footer
        return html

class GetStaticFile:
    def GET(self , url):
        url = PATH+"/"+url
        if False == os.path.exists(url) :
            html =  Header + "什么都没有~" + Footer
            return html
        fileHeader = open(url)
        return fileHeader.read()


if __name__ == "__main__":
    application = web.application(urls, globals()).run() #wsgifunc()
else:
    application = web.application(urls, globals()).wsgifunc()