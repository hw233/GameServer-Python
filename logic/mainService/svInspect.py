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
	yield '>>>> 主逻辑服务 <<<<'
	yield '服务器当前时间:{}'.format(timeU.stamp2str())
	yield '进程启动时间:{}'.format(misc.gsProgressStartTime)
	yield '开区时间:{}'.format(block.parameter.parameter.getEpochTime())
	yield '最高人数上限:{}'.format(block.parameter.parameter.getMaxUserCount())

	yield '服务器id为:{}'.format(config.ZONE_ID)
	yield '服务器区号为:{}'.format(config.ZONE_NO)
	yield ''

	yield '<a href="{}">------------ 各种状态开关 ------------</a>'.format('/switch')
	yield '<a href="{}">-------------- 对象统计 --------------</a>'.format('/object')
	yield '<a href="{}">-------------- 资源统计 --------------</a>'.format('/resource')
	yield '<a href="{}">------------ 最近连接情况 ------------</a>'.format('/connection')

def resource():
	yield '>>>> 主逻辑服务 <<<<'
	yield '------------ 资源统计 ------------'
	yield '银币:'
	yield block.sysActive.gActive.resourceStat('gold','<br>')
	yield '<br>'
	yield '钻石:'
	yield block.sysActive.gActive.resourceStat('diamond','<br>')

def switch():
	yield '>>>> 主逻辑服务 <<<<'
	yield '------------ 各种状态开关 ------------'
	yield '服务器配置为:{}'.format('测试模式' if config.IS_INNER_SERVER else '生产模式')
	yield '仅内部员工可以登录:{}'.format(block.parameter.parameter.isStaffOnly())
	yield '物品交易所当前处于:{}状态'.format('关闭' if block.propsExchange.gExchange.isClose() else '打开')
	yield '元宝交易所当前处于:{}状态'.format('关闭' if block.diamondExchange.gExchange.isClose() else '打开')
	# yield '邮件提取附件服务当前处于:{}状态'.format('关闭' if mail.svcMail.isClose() else '打开')
	#yield '强化装备当前处于:{}状态'.format('关闭' if not svcPackage.canEnchance else '打开')
	#yield '升星功能当前处于:{}状态'.format('关闭' if not svcPackage.canUpStar else '打开')
	#yield '镶嵌功能当前处于:{}状态'.format('关闭' if not svcPackage.canInLay else '打开')
	yield 'gc当前处于:{}状态'.format('打开' if  gc.isenabled() else '关闭')
	#yield '徽章升级功能当前处于:{}状态'.format('关闭' if not svcPackage.canUplevel else '打开')
	

def objectStatistics():
	yield '>>>> 主逻辑服务 <<<<'
	yield '-------------- 对象统计 --------------'
	yield '在内存角色数{}'.format(role.gKeeper.amount())	
	yield '待踢出内存的角色数{}'.format(role.gTimingWheel.callbackAmount())
	yield '在内存账号数{}'.format(account.gKeeper.amount())
	yield '玩家endPoint数{}'.format(mainService.gEndPointKeeper.amount())
	yield '待存盘对象数{}'.format(factory.storageScheduler.callBackAmount())
	yield '待写日志条目数{}'.format(log.getNeedWriteSize())
	
	yield '队伍总个数{}'.format(team.gTeamList.amount())
	yield '关卡副本总个数{}'.format(instance.gWeakRefMng.amount())
	
	yield '邮箱个数{}'.format(mail.mailBoxKeeper.amount())
	yield '角色简要个数{}'.format(resume.gKeeper.amount())
	yield '好友容器个数{}'.format(block.blockFriend.gKeeper.amount())
	yield '离线包裹个数{}.(其实包裹主人可能在线)'.format(block.blockPackage.gKeeper.amount())
	
	yield '数据库空闲连接数{},数据库总连接数{},可允许连接上限{}'.format(db4ms.gConnectionPool.idleConnectionAmount(),db4ms.gConnectionPool.connectionAmount(),db4ms.gConnectionPool.MAX_CONNECTION_SIZE)
	yield '平均等待分配sql连接时间:{:.2f}毫秒'.format(db4ms.gConnectionPool.avgWaitApply())
	yield '平均每个sql执行时间:{:.2f}毫秒'.format(db4ms.gConnectionPool.avgExeSQL())
	
	iAmount,iReal=scene.gSceneProxy.amount(),scene.gRealSceneKeeper.amount()
	yield '场景总个数{},其中永久场景个数{},临时场景个数{}'.format(iAmount,iReal,iAmount-iReal)
	yield '实体总个数{},npc:{},传送门:{}'.format(entity.gEntityProxy.amount(),npc.gNPCproxy.amount(),door.gDoorProxy.amount())

	iRecv,iSend,iWorker=0,0,0
	for ep in mainService.gEndPointKeeper.getValues():
		iRecv+=ep.reqQueue.qsize()
		#iSend+=ep.sendQueue.qsize() 没有sendQueue
		iWorker+=len(ep.sWorkerJobGroup)
	yield '待处理队列长度{},待发送队列长度{},并发的协程数{}'.format(iRecv,iSend,iWorker)
	yield '总共协程个数{}'.format(myGreenlet.gGreenletMng.amount())

	eps = client4gate.getGateEp4ms()
	iRecv = eps.reqQueue.qsize()
	iSend = eps.sendQueue.qsize()
	iWorker = len(eps.sWorkerJobGroup)
	yield 'gateEp待处理队列长度{},待发送队列长度{},并发的协程数{}'.format(iRecv,iSend,iWorker)


	eps = client4route.getRouteEp4ms()
	iRecv = eps.reqQueue.qsize()
	iSend = eps.sendQueue.qsize()
	iWorker = len(eps.sWorkerJobGroup)
	yield 'routeEp待处理队列长度{},待发送队列长度{},并发的协程数{}'.format(iRecv,iSend,iWorker)


def connection():
	yield '>>>> 主逻辑服务 <<<<'
	yield '------------ 最近连接情况 ------------'
	deq=client4gate.service4gate.gdeqRecentConnection
	for i in xrange(len(deq)-1,-1,-1):
		sRecent=deq[i]
		yield sRecent

def content():
	pass
	#每一个安全区的玩家个数
	


	#调试代码
	# yield 'lSellOrderByTime=%s'%block.propsExchange.gExchange.lSellOrderByTime
	# yield 'dSellOrderByPropsId=%s'%block.propsExchange.gExchange.dSellOrderByPropsId
	# yield 'dSellOrderByPrice=%s'%block.propsExchange.gExchange.dSellOrderByPrice
	# yield 'dSellOrderByRoleId=%s'%block.propsExchange.gExchange.dSellOrderByRoleId
	
	# yield '============================='
	# yield 'dBuyOrderByOrderId=%s'%block.diamondExchange.gExchange.dBuyOrderByOrderId
	# yield 'dBuyOrderByRoleId=%s'%block.diamondExchange.gExchange.dBuyOrderByRoleId
	# yield 'dBuyOrderByPrice=%s'%block.diamondExchange.gExchange.dBuyOrderByPrice
	# yield '------------------'
	# yield 'dSellOrderByOrderId=%s'%block.diamondExchange.gExchange.dSellOrderByOrderId
	# yield 'dSellOrderByRoleId=%s'%block.diamondExchange.gExchange.dSellOrderByRoleId
	# yield 'dSellOrderByPrice=%s'%block.diamondExchange.gExchange.dSellOrderByPrice
	
	# yield 'lOrderByTime=%s'%block.diamondExchange.gExchange.lOrderByTime
	
def initServer():
	iPort=config.MAIN_INSPECT_PORT
	oServer=gevent.pywsgi.WSGIServer(('',iPort),application,log=sys.stdout)#
	print 'starting inspect server on port {}'.format(iPort)
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
import db4ms
import role
import mainService
import client4route
import client4gate.service4gate
import block.parameter
import block.sysActive
import factory
import account
import team
import scene
import entity
import npc
# import monster
import door
import mail
import resume
import instance
import block.propsExchange
import block.diamondExchange
import block.blockPackage
#import svcPackage


import myGreenlet
import block.blockFriend
import config
from common import *