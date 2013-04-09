#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import markdown
import web

Header = '''<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"><title> MarkwWike</title></head>
<style>
body{margin:30px 100px;}
</style>
<body>'''

Footer = "</body><p>@copyright ablegao ,Markdown .  MarkwWike</p></html>"



urls = (
    '/', "MainHandler",
    '/(.*\.md)', 'ReadFileHandler',
    '/(.*)' , 'GetStaticFile',
)


class MainHandler:
    def GET(self):
        fileHeader = open("./README.md" )
        html = fileHeader.read()
        html = Header + markdown.markdown(html) + Footer
        return html


class ReadFileHandler:
    def GET(self , url):
        url = "./"+url
        if False == os.path.exists(url) :
            html =  Header + "什么都没有~" + Footer
            return html
        fileHeader = open(url)
        html = fileHeader.read()
        html = Header + markdown.markdown(html) + Footer
        return html

class GetStaticFile:
    def GET(self , url):
        url = "./"+url
        if False == os.path.exists(url) :
            html =  Header + "什么都没有~" + Footer
            return html
        fileHeader = open(url)
        return fileHeader.read()


if __name__ == "__main__":
    application = web.application(urls, globals()).run() #wsgifunc()