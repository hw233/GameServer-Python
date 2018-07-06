#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
def application(env,start_response):
	#print 'env[\'PATH_INFO\']=',env['PATH_INFO']	
	if env['PATH_INFO'] == '/':
		start_response('200 OK',[('Content-Type','text/html;charset=utf-8')])#utf8没有杠,在ie认不得
		bodyContent = "".join(content())
		yield formatToHTML(bodyContent)
	else:
		start_response('404 Not Found',[('Content-Type','text/html')])
		#return ['<h1>Not Found</h1>']
		yield '<h1>Not Found</h1>'

def content():
	yield '''
<style> 
table{border-right:1px solid #F00;border-bottom:1px solid #F00} 
table td{border-left:1px solid #F00;border-top:1px solid #F00} 
</style> 
'''	
	for mod, funcList in instruction.getAllMethod():
		yield "<h1>%s</h1>" % (mod.__doc__.replace("\n", "<br/>") if mod.__doc__ else '程序员忘了写说明')
		yield '<table>'
		for func in funcList:
			yield '<tr>'
			yield '<td>'+func.func_name+'</td><td>'+(func.func_doc if func.func_doc else '程序员忘了写说明')+'</td>'
			yield '</tr>'
		yield '</table>'
		yield '<hr/>' #分隔线
	
def initServer():
	iPort=config.HELPER_PORT
	oServer=gevent.pywsgi.WSGIServer(('',iPort),application,log=sys.stdout)
	print 'starting helper server on port {}'.format(iPort)
	return oServer

import sys
import misc
import gevent
import u
import gevent.pywsgi
import instruction
import config
from common import *