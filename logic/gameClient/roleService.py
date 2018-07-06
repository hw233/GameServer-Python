#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import role_pb2
import endPoint
import misc

class cService(role_pb2.main2terminal):
	@endPoint.result
	def rpcRespCalculator(self,ep,ctrlr,reqMsg):
		print 'iAddend:-------------------------------'
		print 'hpMax:',reqMsg.hpMaxCalc.iAddend
		print 'mpMax:',reqMsg.mpMaxCalc.iAddend
		print 'phyDam:',reqMsg.phyDamCalc.iAddend
		print 'magDam:',reqMsg.magDamCalc.iAddend
		print 'phyDef:',reqMsg.phyDefCalc.iAddend
		print 'magDef:',reqMsg.magDefCalc.iAddend
		print 'spe:',reqMsg.speCalc.iAddend
		print 'iAddend:-------------------------------'
		print 'fFactor:-------------------------------'
		print 'hpMax:',reqMsg.hpMaxCalc.fFactor
		print 'mpMax:',reqMsg.mpMaxCalc.fFactor
		print 'phyDam:',reqMsg.phyDamCalc.fFactor
		print 'magDam:',reqMsg.magDamCalc.fFactor
		print 'phyDef:',reqMsg.phyDefCalc.fFactor
		print 'magDef:',reqMsg.magDefCalc.fFactor
		print 'spe:',reqMsg.speCalc.fFactor
		print 'fFactor:-------------------------------'
		print 'sExpression:-------------------------------'
		print 'hpMax:',reqMsg.hpMaxCalc.sExpression
		print 'mpMax:',reqMsg.mpMaxCalc.sExpression
		print 'phyDam:',reqMsg.phyDamCalc.sExpression
		print 'magDam:',reqMsg.magDamCalc.sExpression
		print 'phyDef:',reqMsg.phyDefCalc.sExpression
		print 'magDef:',reqMsg.magDefCalc.sExpression
		print 'spe:',reqMsg.speCalc.sExpression
		print 'sExpression:-------------------------------'