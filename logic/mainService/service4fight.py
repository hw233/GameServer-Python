#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import main_fight_pb2
import endPoint
import misc

class cService(main_fight_pb2.fight2main):
	@endPoint.result
	def rpcHelloMain_iAmFight(self,ep,ctrlr,reqMsg):return rpcHelloMain_iAmFight(self,ep,ctrlr,reqMsg)

def rpcHelloMain_iAmFight(self,ep,ctrlr,reqMsg):#	
	print 'rpcHelloMain_iAmFight 被call'

	return True


if 'gbOnce' not in globals():
	gbOnce=True
	if 'mainService' in SYS_ARGV:
		pass
import c
import timeU
import u
import log
