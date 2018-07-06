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
	yield '>>>> 场景服务 <<<<'
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
	yield '>>>> 场景服务 <<<<'
	yield '------------ 资源统计 ------------'

def switch():
	yield '>>>> 场景服务 <<<<'
	yield '------------ 各种状态开关 ------------'
	yield '服务器配置为:{}'.format('测试模式' if config.IS_INNER_SERVER else '生产模式')		
	yield 'gc当前处于:{}状态'.format('打开' if  gc.isenabled() else '关闭')
	

def objectStatistics():
	yield '>>>> 场景服务 <<<<'
	yield '-------------- 对象统计 --------------'
	yield '玩家endPoint数{}'.format(sceneService.gEndPointKeeper.amount())	
	yield '待写日志条目数{}'.format(log.getNeedWriteSize())
	


	iRecv=0
	for ep in sceneService.gEndPointKeeper.getValues():
		iRecv+=ep.reqQueue.qsize()
		#iWorker+=len(ep.sWorkerJobGroup)
	yield '待处理队列长度{}'.format(iRecv) #并发的协程数{} iWorker=0
	yield '总共协程个数{}'.format(myGreenlet.gGreenletMng.amount())

	yield '脚本场景对象数量:{}'.format(sceneService.scene4ss.gSceneKeeper.amount())
	yield '脚本实体对象数量:{}'.format(sceneService.entity4ss.gEntityKeeper.amount())
	
	eps = client4gate.getGateEp4ss()
	iRecv = eps.reqQueue.qsize()
	iSend = eps.sendQueue.qsize()
	iWorker = len(eps.sWorkerJobGroup)
	yield 'gateEp待处理队列长度{},待发送队列长度{},并发的协程数{}'.format(iRecv,iSend,iWorker)


	eps = client4route.getRouteEp4ss()
	iRecv = eps.reqQueue.qsize()
	iSend = eps.sendQueue.qsize()
	iWorker = len(eps.sWorkerJobGroup)
	yield 'routeEp待处理队列长度{},待发送队列长度{},并发的协程数{}'.format(iRecv,iSend,iWorker)

	yield '----底层队列--------------'
	sAoiState = zfmPyEx.aoiState()
	lAoiState = sAoiState.split("\n")
	for s in lAoiState:
		yield s

def connection():
	yield '>>>> 场景服务 <<<<'
	yield '------------ 最近连接情况 ------------'
	deq=client4gate.service4gate.gdeqRecentConnection4Scene
	for i in xrange(len(deq)-1,-1,-1):
		sRecent=deq[i]
		yield sRecent

def content():
	pass
		
def initServer():
	iPort=config.SCENE_INSPECT_PORT
	oServer=gevent.pywsgi.WSGIServer(('',iPort),application,log=sys.stdout)#
	print 'starting inspect server for scene service on port {}'.format(iPort)
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
import sceneService
import myGreenlet
import config
from common import *
import client4gate
import client4route
import sceneService.scene4ss
import sceneService.entity4ss
import zfmPyEx
