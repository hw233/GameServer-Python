#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇


def waitAllBackEndReport2route():#阻塞,直到各个后端连到路由
	if 'mainService' in SYS_ARGV:
		gevent.hub.wait(gtAllReport2route4ms)

	if 'sceneService' in SYS_ARGV:
		gevent.hub.wait(gtAllReport2route4ss)

	if 'fightService' in SYS_ARGV:
		gevent.hub.wait(gtAllReport2route4fs)

	if 'chatService' in SYS_ARGV:
		gevent.hub.wait(gtAllReport2route4cs)
		

import backEnd_pb2

gdServiceName={
	backEnd_pb2.UNKNOWN_SERVICE:'未知服务',
	backEnd_pb2.MAIN_SERVICE:'主服务',
	backEnd_pb2.SCENE_SERVICE:'场景服务',
	backEnd_pb2.FIGHT_SERVICE:'战斗服务',
	backEnd_pb2.CHAT_SERVICE:'聊天服务',
}

import gevent.hub
import gevent.event
import c
import misc
import log
import u

import backEndEndPoint

import main_scene_pb2
import main_fight_pb2
import main_chat_pb2

import mainService.service4scene
import sceneService.service4main
import fightService.service4main
import mainService.service4fight
import mainService.service4chat
import chatService.service4main

if 'gbOnce' not in globals():
	gbOnce=True	
	bDebugMode=True

	if 'mainService' in SYS_ARGV:
		ssReport2gateEv4ms=gevent.event.Event()
		csReport2gateEv4ms=gevent.event.Event()
		fsReport2gateEv4ms=gevent.event.Event()
		#t1=(ssReport2gateEv4ms,csReport2gateEv4ms)#,fsReport2gateEv4ms

		ssReport2routeEv4ms=gevent.event.Event()
		csReport2routeEv4ms=gevent.event.Event()
		fsReport2routeEv4ms=gevent.event.Event()
		gtAllReport2route4ms=(ssReport2routeEv4ms,csReport2routeEv4ms)#,fsReport2routeEv4ms

		#gtAllReported4ms=t1+gtAllReport2route4ms

		dProtocol={'service':(mainService.service4scene.cService,),'stub':(main_scene_pb2.main2scene_Stub,)}
		gSceneEp4ms=backEndEndPoint.cEndPoint4ms(bDebugMode,dProtocol)
		gSceneEp4ms.setEndPointId(backEnd_pb2.SCENE_SERVICE)#设置数据投递的目标
		gSceneEp4ms.start()

		dProtocol={'service':(mainService.service4fight.cService,),'stub':(main_fight_pb2.main2fight_Stub,)}
		gFightEp4ms=backEndEndPoint.cEndPoint4ms(bDebugMode,dProtocol)
		gFightEp4ms.setEndPointId(backEnd_pb2.FIGHT_SERVICE)#设置数据投递的目标
		gFightEp4ms.start()

		dProtocol={'service':(mainService.service4chat.cService,),'stub':(main_chat_pb2.main2chat_Stub,)}
		gChatEp4ms=backEndEndPoint.cEndPoint4ms(bDebugMode,dProtocol)
		gChatEp4ms.setEndPointId(backEnd_pb2.CHAT_SERVICE)#设置数据投递的目标
		gChatEp4ms.start()
		
	if 'sceneService' in SYS_ARGV:
		msReport2gateEv4ss=gevent.event.Event()	
		csReport2gateEv4ss=gevent.event.Event()
		fsReport2gateEv4ss=gevent.event.Event()
		#t1=(msReport2gateEv4ss,csReport2gateEv4ss)#,fsReport2gateEv4ss

		msReport2routeEv4ss=gevent.event.Event()
		csReport2routeEv4ss=gevent.event.Event()
		fsReport2routeEv4ss=gevent.event.Event()
		gtAllReport2route4ss=(msReport2routeEv4ss,csReport2routeEv4ss)#,fsReport2routeEv4ss

		#gtAllReported4ss=t1+gtAllReport2route4ss

		dProtocol={'service':(sceneService.service4main.cService,),'stub':(main_scene_pb2.scene2main_Stub,)}
		gMainEp4ss=backEndEndPoint.cEndPoint4ss(bDebugMode,dProtocol)	
		gMainEp4ss.setEndPointId(backEnd_pb2.MAIN_SERVICE)#设置数据投递的目标
		gMainEp4ss.start()

	if 'fightService' in SYS_ARGV:
		msReport2gateEv4fs=gevent.event.Event()
		ssReport2gateEv4fs=gevent.event.Event()
		csReport2gateEv4fs=gevent.event.Event()
		#t1=(msReport2gateEv4fs,ssReport2gateEv4fs)#,csReport2gateEv4fs

		msReport2routeEv4fs=gevent.event.Event()
		ssReport2routeEv4fs=gevent.event.Event()
		csReport2routeEv4fs=gevent.event.Event()
		gtAllReport2route4fs=(msReport2routeEv4fs,ssReport2routeEv4fs)#,csReport2routeEv4fs

		#gtAllReported4fs=t1+gtAllReport2route4fs

		dProtocol={'service':(fightService.service4main.cService,),'stub':(main_fight_pb2.fight2main_Stub,)}
		gMainEp4fs=backEndEndPoint.cEndPoint4fs(bDebugMode,)
		gMainEp4fs.setEndPointId(backEnd_pb2.MAIN_SERVICE)#设置数据投递的目标
		gMainEp4fs.start()

	if 'chatService' in SYS_ARGV:
		msReport2gateEv4cs=gevent.event.Event()
		ssReport2gateEv4cs=gevent.event.Event()
		fsReport2gateEv4cs=gevent.event.Event()
		#t1=(msReport2gateEv4cs,ssReport2gateEv4cs)#,fsReport2gateEv4cs

		msReport2routeEv4cs=gevent.event.Event()
		ssReport2routeEv4cs=gevent.event.Event()
		fsReport2routeEv4cs=gevent.event.Event()
		gtAllReport2route4cs=(msReport2routeEv4cs,ssReport2routeEv4cs)#,fsReport2routeEv4cs

		#gtAllReported4cs=t1+gtAllReport2route4cs

		dProtocol={'service':(chatService.service4main.cService,),'stub':(main_chat_pb2.chat2main_Stub,)}
		gMainEp4cs=backEndEndPoint.cEndPoint4cs(bDebugMode,dProtocol)
		gMainEp4cs.setEndPointId(backEnd_pb2.MAIN_SERVICE)#设置数据投递的目标
		gMainEp4cs.start()

