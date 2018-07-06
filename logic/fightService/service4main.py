#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import main_fight_pb2
import endPoint
import misc

class cService(main_fight_pb2.main2fight):
	@endPoint.result
	def rpcHelloFight_iAmMain(self,ep,ctrlr,reqMsg):return rpcHelloFight_iAmMain(self,ep,ctrlr,reqMsg)
	
	@endPoint.result
	def rpcHotUpdate(self, ep, ctrlr, reqMsg):return rpcHotUpdate(ep, ctrlr, reqMsg)

def rpcHelloFight_iAmMain(self,ep,ctrlr,reqMsg):#	
	print 'rpcHelloFight_iAmMain 被call'

	return True


def rpcHotUpdate(ep, ctrlr, reqMsg):
	import hotUpdate
	modPath = reqMsg.sValue
	hotUpdate.update(modPath)

import c
import timeU
import u
import log
