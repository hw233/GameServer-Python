#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import sys
import os

class cStdOut(object):	
	def __init__(self):
		self.oldStdOut=sys.stdout #旧的fd
		self.sLastText=''

	def write(self,sText):
		import platform
		import gevent.core
		import time

		if platform.system().upper()=="WINDOWS":
# 				sTime=time.strftime('[%H:%M:%S] ',time.localtime(gevent.core.time()))
			sText=sText.decode('utf-8').encode('gbk')

		self.sLastText = sText
		self.oldStdOut.write(sText)

sys.stdout=cStdOut()#重定向标准输出,主要是为了在windows把utf8转成gbk
#不能以/或\结尾,可以用相对路径
sys.path.append('.') #为了读取config.py文件
sys.path.append('pb2')
sys.path.append('pb2/backEnd_gate')
sys.path.append('pb2/backEnd_route')
sys.path.append('pb2/main_scene')
sys.path.append('pb2/main_fight')
sys.path.append('pb2/main_chat')
sys.path.append('pb2/terminal_main')
sys.path.append('pb2/terminal_scene')
sys.path.append('pb2/terminal_chat')
sys.path.append('pb2/backEnd_center')

sys.path.append('rpc')
sys.path.append('util')
sys.path.insert(0,'pyLib')#要用insert而不是append,因为要优先查找自有的模块
sys.path.append('data/py')
sys.path.append('data/manual')


#移除掉预加载的模块
sys.modules.pop('traceback',None)
#重新import模块
import traceback
#--不要在上插入代码,因为要保证尽早地把pyLib自已的模块import进来,比如修改过的traceback-----------------------



import u
print '模块查找路径: '
for s in sys.path:
	print '\t{}'.format(s)
print '\n'


print '工作目录: {}'.format(os.getcwd())


def start(lArgv):
	print '启动参数: {}'.format(' '.join(lArgv))
	if len(lArgv)<2:
		raise Exception,'启动时必须指明要启动哪个服务'
	sType=lArgv[1]
	if platform.system().upper()=="WINDOWS":#改一下cmd窗口标题
		os.system(u.trans('title {}'.format(' '.join(lArgv[1:]))))#除了xx/yy/zz.py之外,其他都显示到标题栏

	sys.stdin=gevent.fileobject.FileObject(sys.stdin)#使raw_input不会阻塞
	
	sys.stderr=cStdErr()#重定向标准错误.把错误内容拐骗到log中去.(默认的标准错误是输出到屏幕的)

	#每种服务都需要初始化的,且不依赖别的模块的,顺序无关的
# 	timeU.init()#初始化基准时间
# 	timerEvent.init()#各种定时事件初始化

	if sType in ('gateService',):#网关服务器		
		log.initDirStartThread('logGateService')
		jobRawInput=gevent.spawn(rawInput4test.proc)
		#下面顺序有些是有依赖的		
		oServer=gateService.gateServer4backEnd.initServer()
		
		job1=gevent.spawn(oServer.serve_forever)

		oServer=gateService.inspectServer4gs.initServer()#探查服务
		job2=gevent.spawn(oServer.serve_forever)
		
		oServer=gateService.backdoor4gs.initServer()#后门服务
		job3=gevent.spawn(oServer.serve_forever)
		gateService.waitAllBackEnd()#阻塞,等各个后端连过来再打开对客户端的端口
		oServer=gateService.server4gameClient.initServer()
		job4=gevent.spawn(oServer.serve_forever)

		gevent.joinall([job1,job2,job3,job4],None,True)

	elif sType in ('routeService',):#路由服务
		log.initDirStartThread('logRouteService')
		jobRawInput=gevent.spawn(rawInput4test.proc)
		#下面顺序有些是有依赖的		
		oServer=routeService.routeServer4backEnd.initServer()
		job1=gevent.spawn(oServer.serve_forever)

		# oServer=routeService.inspectServer4gs.initServer()#探查服务
		# job2=gevent.spawn(oServer.serve_forever)
		
		# oServer=routeService.backdoor4gs.initServer()#后门服务
		# job3=gevent.spawn(oServer.serve_forever)

		# oServer=routeService.server4gameClient.initServer()
		# job4=gevent.spawn(oServer.serve_forever)

		gevent.joinall([job1],None,True) #,job2,job3,job4

	elif sType in ('sceneService',):#单区场景服务		
		log.initDirStartThread('logSceneService')
		jobRawInput=gevent.spawn(rawInput4test.proc)
		gevent.signal(signal.SIGTERM, instruction.shutServer.onSceneServiceCaptureSigterm)
		#下面顺序有些是有依赖的		
		
		routeEp=client4route.blockConnect(backEnd_pb2.SCENE_SERVICE)#阻塞在这里,直到连接成功		
		backEnd.waitAllBackEndReport2route()#等待其他后端服务连到路由

		sceneService.initTimer()#设置定时器
		oServer=sceneService.inspectServer4ss.initServer()#探查服务
		glServers.append(oServer)
		lJobs = [gevent.spawn(oServer.serve_forever) for oServer in glServers]
		gateEp=client4gate.blockConnect(backEnd_pb2.SCENE_SERVICE,1)#最后才连到网关,阻塞在这里,直到连接成功
		gevent.joinall(lJobs,None,True)

	elif sType=='mainService':
		jobRawInput=gevent.spawn(rawInput4test.proc)
		gevent.signal(signal.SIGTERM, instruction.shutServer.onCaptureSigterm)
		
		log.initDirStartThread('logMainService')
		
		#下面顺序有些是有依赖的,比如parameter对象初始化必须等到数据库连接初始化后
			
		db4ms.init()#初始化mysql连接池,建数据库,建表,加列等等的操作.		
		#databaseLogin.init()#初始化登录服对应的mysql连接池
		
		#db4ms.gConnectionPool.setPrintSQL(True) #是否打印全部被执行的sql语句
		#db4ms.gConnectionPool.setLogSQL(True) #是否把全部被执行的sql语句写入log
		endPoint.gbPrintRPCname=True #是否打印每一个收到rpc名字

		#clientLogin.endPoint
		
		trie.init()#初始化敏感词过滤器
		logReport.init()#初始化报表日志记录器
		initDependDataBase()#依赖数据库的一些初始化,就放到这个函数里面

		routeEp=client4route.blockConnect(backEnd_pb2.MAIN_SERVICE)#阻塞在这里,直到连接成功		
		backEnd.waitAllBackEndReport2route()#等待其他后端服务连到路由
			
		client4center.blockConnect(backEnd_pb2.MAIN_SERVICE)#阻塞在这里,直到连接成功	

		scene.init()#初始化永久场景
		npc.init()#把npc放入永久场景
		door.init()#把传送门放入永久场景
		# client4center.connect2center(backEnd_pb2.MAIN_SERVICE)

		props.init()
		guild.init()
		task.init()
		buff.init()
		skill.init()
		perform.init()
		state.init()
		openLevel.init()
		listener.init()
		shop.init()
		collect.init()
		trade.init()
		activity.init()
		treasureShop.init()
		resume.init()
		friend.init()
		
		tougheningExp.init()
		answer.init()
		oServer=mainService.svInspect.initServer()#视察服务器
		glServers.append(oServer)

		oServer=gmServer.initServer()#gm服务
		glServers.append(oServer)

		oServer=svInstruction.initServer()#指令服务器
		glServers.append(oServer)

		oServer=backdoor.initServer()#后门服务器
		glServers.append(oServer)

		if config.IS_INNER_SERVER:
			oServer=svHelper.initServer()
			glServers.append(oServer)
		#loginClient.init()#连接到登录服务器
		lJobs = [gevent.spawn(oServer.serve_forever) for oServer in glServers]
		gateEp=client4gate.blockConnect(backEnd_pb2.MAIN_SERVICE,1)#最后才连到网关,阻塞在这里,直到连接成功
		gevent.joinall(lJobs,None,True)
	elif sType=='chatService':#聊天服务器
		log.initDirStartThread('logChatService')
		chatService.init()
		trie.init()
# 		endPoint.gbPrintRPCname=True #是否打印每一个收到rpc名字
		
		routeEp=client4route.blockConnect(backEnd_pb2.CHAT_SERVICE)#阻塞在这里,直到连接成功		
		backEnd.waitAllBackEndReport2route()#等待其他后端服务连到路由

		client4center.blockConnect(backEnd_pb2.CHAT_SERVICE)#阻塞在这里,直到连接成功	

		oServer = chatService.backdoor4cs.initServer()
		glServers.append(oServer)
		oServer=chatService.inspectServer4cs.initServer()
		glServers.append(oServer)
		
		lJobs = [gevent.spawn(server.serve_forever) for server in glServers]
		gateEp=client4gate.blockConnect(backEnd_pb2.CHAT_SERVICE,1)#最后才连到网关,阻塞在这里,直到连接成功
		gevent.joinall(lJobs,None,True)

	elif sType=='centerService':#中心服务器
		log.initDirStartThread('logCenterService')
		jobRawInput=gevent.spawn(rawInput4test.proc)
		#下面顺序有些是有依赖的		
		db4center.init()#初始化mysql连接池,建数据库,建表,加列等等的操作.		
		randNameData.loadUsedName()#加载已被使用的名字库

		collect.init()
		centerService.audio.init()

		oServer=centerService.cs4backEnd.initServer()
		glServers.append(oServer)
		oServer = centerService.audioServer.initServer()
		glServers.append(oServer)
		
		lJobs = [gevent.spawn(oServer.serve_forever) for oServer in glServers]
		gevent.joinall(lJobs,None,True)

	elif sType=='gameClient':#游戏客户端,测试用
		log.initDirStartThread('logGameClient')
		gameClient.start(*lArgv[2:2+2])
	elif sType=='robot':#机器人客户端,测试性能用
		log.initDirStartThread('logRobot')
		scene.init()
		robot.init()
		robot.start(*lArgv[2:2+2])
	else:
		pass
	log.closeAll()#如果不执行这句,进程不会关闭,应该是挂在log线程那里了


def initDependDataBase():#初始化依赖数据库的
	
	GUId.init()#初始化id生成器
	rank.initAllRank()
	
	
	block.parameter.init()#全局系统参数
	block.sysActive.init()#系统活跃数据
	block.propsExchange.init()#拍卖场从数据库加载初始化
	block.diamondExchange.init()#元宝交易所从数据库加载初始化

if 'glServers' not in globals():
	glServers=[]

class cStdErr(object):
	def __init__(self):
		self.oldStdErr=sys.stderr

	def write(self,sText):
		#import log
		print sText, #最后加上逗号,阻止自动加回车
		#self.oldStdErr.write(sText) #最后加上逗号,阻止自动加回车
		log.log('exception',sText,None)
		
import log


sys.setcheckinterval(2**31-1)#据说不使用多线程的情况下,设大此值,可以极大提高解释器性能 (不用使用sys.maxint,在32位与64位系统中sys.maxint值是不相同的.)
import platform
os.environ['GEVENT_RESOLVER']='ares' #dns模块使用ares,这句要尽早执行,抢在第一次调用gevent.get_hub()之前

import gevent
MAIN_GREENLET=gevent.getcurrent()
import gevent.fileobject

#if platform.system().upper()=="WINDOWS":
#	sys.stdout=gevent.fileobject.FileObject(sys.stdout)#这个有什么作用呢??
	#(在linux下会输出不及时,n次print会集中一次性输出,特别是启动有错print时会什么也看不到)
	#后来发现在windows下也会精分
import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_time()
gevent.monkey.patch_ssl()

import gc
import timeU
import signal
import mainService.svInspect
import sceneService.inspectServer4ss
import props
import block.parameter
import block.sysActive
import block.propsExchange
import block.diamondExchange
import rank

import GUId
import scene
import npc
import door
import task
import activity
import buff
import skill
import perform
import timerEvent
import misc
import role
import db4ms
import clientLogin
import guild
import gmServer
import instruction.shutServer
import gateService.server4gameClient
import gateService.gateServer4backEnd
import routeService.routeServer4backEnd
import client4route
import client4gate

import svcAccount
import chatService.inspectServer4cs
import chatService.backdoor4cs
import centerService.audioServer

import svInstruction
import backdoor
import endPoint
import robot
import svHelper
import gameClient
import timer
import trie
import logReport

import initCall
import rawInput4test

#import config_pb2
import config
import databaseLogin
import backEnd
import backEnd_pb2
import chatService
import state
import randNameData

import client4center
import centerService.cs4backEnd
import db4center
import gateService.inspectServer4gs
import gateService.backdoor4gs
import openLevel
import listener
import shop
import collect
import trade
import answer
import treasureShop
import resume
import friend
import centerService.audio
import tougheningExp

if config.IS_INNER_SERVER:
	gc.set_debug(gc.DEBUG_LEAK)#这个设定的作用是:在collect后,会把循环引用对象移到gc.garbage,方便分析

	#def collect():
	#	print 
	#	gc.collect()
	
	goTimerMng=timer.cTimerMng()
	guTimerId=goTimerMng.run(lambda:gc.collect(),10,10)#每10秒一次gc
