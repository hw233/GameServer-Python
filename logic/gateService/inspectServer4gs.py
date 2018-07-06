#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def application(env,start_response):
	#vip个数
	#日志列表

	#重启服务器
	#充值功能是否开放
	#邮箱提取附件功能是否关闭
	#到其他服务器的连接是否正常(支付转发,登录服,配置服)
	#本次启服时间,进程启动总时长
	sPath=env['PATH_INFO']
	if sPath in gdResult:
		start_response('200 OK',[('Content-Type','text/html;charset=utf8')])
		bodyContent = "<br/>".join(gdResult[sPath]())
		yield formatToHTML(bodyContent)
	else:
		start_response('404 Not Found',[('Content-Type','text/html')])
		yield '<h1>Not Found</h1>'

def index():
	#要不要统计一下流量呢?
	yield '>>>> 网关服务 <<<<'
	yield '服务器当前时间:{}'.format(timeU.stamp2str())
	yield '进程启动时间:{}'.format(misc.gsProgressStartTime)
	
	yield '服务器id为:{}'.format(config.ZONE_ID)
	yield '服务器区号为:{}'.format(config.ZONE_NO)
	yield ''

	yield '<a href="{}">------------ 各种状态开关 ------------</a>'.format('/switch')
	yield '<a href="{}">-------------- 对象统计 --------------</a>'.format('/object')
	yield '<a href="{}">-------------- 资源统计 --------------</a>'.format('/resource')
	yield '<a href="{}">------------ 最近连接情况 ------------</a>'.format('/connection')

def resource():
	yield '>>>> 网关服务 <<<<'
	yield '------------ 资源统计 ------------'

def switch():
	yield '>>>> 网关服务 <<<<'
	yield '------------ 各种状态开关 ------------'
	yield '服务器配置为:{}'.format('测试模式' if config.IS_INNER_SERVER else '生产模式')		
	yield 'gc当前处于:{}状态'.format('打开' if  gc.isenabled() else '关闭')
	

def objectStatistics():
	yield '>>>> 网关服务 <<<<'
	yield '-------------- 对象统计 --------------'
	yield '客户端连接数{}'.format(gateService.server4gameClient.gConnKeeper.amount())
	yield '待写日志条目数{}'.format(log.getNeedWriteSize())
	
	for (iBackEndType,),oBackEnd in gateService.gateServer4backEnd.gBackEndProxy.getAll().iteritems():
		sBackEndName=backEnd.gdServiceName[iBackEndType]
		iRecv=oBackEnd.reqQueue.qsize()
		iSend=oBackEnd.sendQueue.qsize()
		yield '后端:"{}"待处理队列长度{},待发送队列长度{}'.format(sBackEndName,iRecv,iSend)

def connection():
	yield '>>>> 网关服务 <<<<'
	yield '------------ 最近连接情况 ------------'
	for i in xrange(len(gateService.server4gameClient.gdeqRecentConnection)-1,-1,-1):
		sRecent=gateService.server4gameClient.gdeqRecentConnection[i]
		yield sRecent

def content():
	pass
		
def initServer():
	iPort=config.GATE_INSPECT_PORT
	oServer=gevent.pywsgi.WSGIServer(('',iPort),application,log=sys.stdout)#
	print 'starting inspect server for gateService on port {}'.format(iPort)
	return oServer

gdResult={
	'/':index,
	'/switch':switch,
	'/object':objectStatistics,
	'/connection':connection,
	'/resource':resource,
}

import sys
import gc
import misc
import log		
import gevent
import gevent.server
import u
import gevent.pywsgi

import timeU
import gateService
import gateService.server4gameClient
import gateService.gateServer4backEnd
import myGreenlet
import backEnd
import config
from common import *