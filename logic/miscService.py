#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import terminal_main_pb2
import endPoint
#terminal_main_below.terminal2main
#杂项

class cService(terminal_main_pb2.terminal2main):

	@endPoint.result
	def rpcServerTime(self, ep, who, reqMsg): return rpcServerTime(who, reqMsg)#ntp网络对时(打击外挂会用到)

def rpcServerTime(who, reqMsg):#ntp网络对时
	clientTime = reqMsg.iValue
	ti = time.time()

	import timerEvent
	if timerEvent.gTempTime is not None:
		ti += timerEvent.gTempTime
	localTime  = int(ti * 1000)
	timeList   = common_pb2.int64Pair()

	timeList.iValue1 = clientTime
	timeList.iValue2 = localTime
	
	return timeList

import time
import common_pb2