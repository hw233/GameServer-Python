#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_pb2
import gevent.event
import gevent.hub

CONN_ID_SIZE=4 #连接id的大小
CONN_ID_COMMAND=0 #内部通道id,不代表真正的客户端连接

def waitAllBackEnd():
	gevent.hub.wait(gdBackEndReport2gateEvent.values())#阻塞,等各个后端连过来再打开对客户端的端口




import p
SERIALIZED_UNKNOWN=p.cPack().packInt(CONN_ID_SIZE,backEnd_pb2.UNKNOWN_SERVICE).getBuffer()

if 'gateService' in SYS_ARGV:
	gdBackEndReport2gateEvent={#给客户端连接的网关端口,必须等到后端各个backEnd连上来后才能打开.
		backEnd_pb2.MAIN_SERVICE:gevent.event.Event(),#'主服务'
		backEnd_pb2.CHAT_SERVICE:gevent.event.Event(),#'聊天服务'
		backEnd_pb2.SCENE_SERVICE:gevent.event.Event(),#'场景服务'
		#backEnd_pb2.FIGHT_SERVICE:gevent.event.Event(),#'战斗服务'
		
	}