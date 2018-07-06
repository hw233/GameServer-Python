#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

# import login.httpSvc4gameClient
import gmInstruct

#拥有全部权限的IP集合
gsFullAuthority=set(['127.0.0.1','192.168.1.216', '192.168.1.217'])
gbOpenForAny=True	#是否向所有人开放

# #路径映射函数
gdCmdMapFunc={#{模块:[处理函数,拥有该模块执行权限的IP集合]
	'/role':[gmInstruct.quaryRoleInfo, set()],	#角色信息相关
	'/gm':[gmInstruct.command, set()],			#gm指令
	'/notice':[gmInstruct.notice, set()],		#公告
	'/gsInfo':[gmInstruct.gameServerInfo, set()],	#服务器信息
	'/mail':[gmInstruct.sendMail, set()],	#邮件
	'/issuecurrency':[gmInstruct.issueCurrency,set()],	# 发放二级货币
	# '/account':gmInstruct,	#账号相关
}

#解析http请求参数,返回字典
def parseHttpParam(sQueryString):
	try:
		sQueryString=urllib.unquote(sQueryString).decode('utf-8', 'replace')
	except Exception:
		pass
	try:
		return json.loads(sQueryString, 'utf-8'), True	#上面的转码可能失败,此处再次尝试进行load
	except Exception:
		return '', False

def application(env,start_response):
	sPath=env['PATH_INFO']
	oHandler=env['HANDLER']
	sFullPath=oHandler.path

	sMethod=env['REQUEST_METHOD']
	if sMethod=='POST':	#post请求方式
		iLength= int(env.get('CONTENT_LENGTH', '0'))
		if iLength!=0:
			sQueryString= env['wsgi.input'].read(iLength)	#post请求的数据	
		else:
			sQueryString='{}'	#防止parseHttpParam参数未定义,所以随便给个{}
	elif sMethod=='GET':
		sQueryString=env['QUERY_STRING'] or '{}'
	else:	#HEAD
		pass
	
	try:		
		func=gdCmdMapFunc.get(sPath,[None])[0]
		start_response('200 OK',[('Content-Type','text/html;charset=utf8')])
		if func:
			#检查权限
			sRemoteIP=env['REMOTE_ADDR']
			if sRemoteIP not in gsFullAuthority and sRemoteIP not in gdCmdMapFunc[sPath][1] and not gbOpenForAny:
				return json.dumps([{'state':False, 'desc':'你没有该权限'}])
			dParam, bSucc = parseHttpParam(sQueryString)
			#print 'sQueryString:', sQueryString, type(sQueryString), 'and succ::',bSucc, 'and dParam::',dParam
			if bSucc:
				sResult=func(**dParam)
				# print 'sResult:', sResult
			else:
				sResult='<h1>error</h1>'
		else:
			sErrorMsg=env['HTTP_HOST']
			if sPath != '/':
				sErrorMsg += sPath
			if sQueryString:
				sErrorMsg = '{}?{}'.format(sErrorMsg, sQueryString)

			sResult='<h1>Url Error:{}</h1>'.format(sErrorMsg)
			#start_response('404 Not Found',[('Content-Type','text/html')])
		# start_response('200 OK',[('Content-Type','text/html;charset=utf8')])
		return formatToHTML(sResult)
	except Exception:
		sResult='server raise exception'
		raise
	finally:	
		pass	
		# log.log('requestRespond','request={},respond={}'.format(sFullPath.decode('utf-8'),sResult))

import gevent.pywsgi
class WSGIHandler(gevent.pywsgi.WSGIHandler):
	def get_environ(self):#override 为了使得application处理时能拿得到handler对象
		dEnv=gevent.pywsgi.WSGIHandler.get_environ(self)
		dEnv['HANDLER']=self
		return dEnv

def initServer():
	iHTTPport=config.GM_PORT	
	oServer=gevent.pywsgi.WSGIServer(
		('',iHTTPport),
		application,
		log=sys.stdout,
		handler_class=WSGIHandler
		)#
	print 'starting web gm server on port {}'.format(iHTTPport)
	return oServer

import timeU

if 'gbOnce' not in globals():
	gbOnce=True

	if 'mainService' in SYS_ARGV:
		pass

import sys
import gc

import urllib
import log
import misc
import gevent
import gevent.server
import u
import json
import config
from common import *
#import config_pb2

#import db4ms
