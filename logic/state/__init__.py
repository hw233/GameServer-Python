#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
'''
#状态基类

import pst

class cState(pst.cEasyPersist):
	def __init__(self,iNo):
		pst.cEasyPersist.__init__(self)
		self.iNo=iNo
		self.iOwnerId=0
		self.iAtt=self.iDef=self.iCrit=self.iHit=self.iDodge=-1
		self.iHpMax=self.iMpMax=-1
		self.oTimerMng=timer.cTimerMng()#用于定时会消失的buff
		self.uTimerId=0

	def onBorn(self,*tArgs,**dArgs):#override
		pass

	@property
	def key(self):
		return self.iNo

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		
		return dData

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		
	def setup(self,who):
		iLeftTime=self.leftTime()
		if iLeftTime>0:
			func=u.cFunctor(self.onTimeout)#避免循环引用
			self.uTimerId=self.oTimerMng.run(func,iLeftTime)
		elif self.fetch('start') or self.fetch('end',0):
			self.onTimeout()

	def onTimeout(self):#超时时间到
		pass

	def leftTime(self):#剩余时间
		iLeft=self.fetch('end',0)-timeU.getStamp()
		return 0 if iLeft<0 else iLeft

	@property
	def ownerId(self):
		return self.iOwnerId

	@ownerId.setter
	def ownerId(self, ownerId):
		self.iOwnerId = ownerId

	def onAdd2container(self):
		pass

	def onRemoveFromContainer(self):
		pass

	@property
	def name(self):#名字
		return self.getConfig('name','')

	def desc(self):#通用描述
		return self.getConfig('desc','')

	def detail(self):
		return ''

	def getConfig(self,sKey,uDefault=0,iNo=0):
		if not iNo:
			iNo=self.iNo
		return stateData.getConfig(iNo,sKey,uDefault)

	def getMsg(self):
		msg=state_pb2.stateMsg()
		msg.iStateNo=self.iNo
		msg.sStateName=self.name
		msg.sDesc=self.desc()
		return msg    

	def hpMax(self):#生命值上限
		if self.iHpMax!=-1:
			return self.iHpMax          
		return 23452345

	def mpMax(self):#真气值上限
		if self.iMpMax!=-1:
			return self.iMpMax          
		return 2452

	def attack(self):#攻击
		if self.iAtt!=-1:
			return self.iAtt
		return 3424

	def defense(self):#防御
		if self.iDef!=-1:
			return self.iDef        
		return 234525

	def critical(self):#暴击
		if self.iCrit!=-1:
			return self.iCrit       
		return 21424

	def hit(self):#命中
		if self.iHit!=-1:
			return self.iHit            
		return 1313

	def dodge(self):#闪避
		if self.iDodge!=-1:
			return self.iDodge          
		return 35345

def create(iNo):
	if iNo not in gdStateModule:
		raise Exception,'不存在编号为{}的状态.'.format(iNo)
	return gdStateModule[iNo].cState(iNo)

def new(iNo,*tArgs,**dArgs):
	obj=create(iNo)
	obj.onBorn(*tArgs,**dArgs)
	return obj

if 'gdStateModule' not in globals():
	gdStateModule={}


gdTypeMapMod={  #类型编号 映射 模块
	# 1:main,		#主线称号
	# 2:sub,		#支线称号
	# 3:activity,	#活动称号
	
}


THIS_MODULE=__import__(__name__)

#自动用编号关联类,如果数据表中填0或没有填,或填了不存在的类型,则关联到基类
def init():
	for iNo,dInfo in stateData.gdData.iteritems():#关联称号
		if iNo in gdStateModule:
			continue
		iType=dInfo.get('Type',0)
		gdStateModule[iNo]=gdTypeMapMod.get(iType,THIS_MODULE)

import u
import timer

import timeU
#import stateData
#import state_pb2

#init()
'''

def init():
	print "state init..."
	import state.load

def create(iNo):
	return state.load.getModule(iNo).State()

def new(iNo,iTime=0):
	obj=create(iNo)
	if iTime:
		obj.setTime(iTime)
	return obj

def createAndLoad(iNo, data):
	obj = create(iNo)
	obj.load(data)
	return obj

def addState(who, iNo, iTime=0):
	obj = new(iNo, iTime)
	who.stateCtn.addItem(obj)
	writeLog("state/new", "%d new state %d" % (who.id, iNo))
	return obj

def removeState(who, iNo):
	stateObj = who.stateCtn.getItem(iNo)
	if stateObj:
		who.stateCtn.removeItem(stateObj)
		writeLog("state/remove", "%d remove state %d" % (who.id, iNo))

def checkRepairState(who):
	bRepair = False		# 是否有修理状态
	bRemove = True		# 是否需要移除修理状态
	if who.stateCtn.getItem(104):
		bRepair = True
	for equip in who.equipCtn.getAllWearEquip():
		if equip.getLife() <= equip.maxLife() * 0.2:
			bRemove = False
			if not bRepair:
				bRepair = True
				addState(who, 104)
				break
	if bRepair and bRemove:
		removeState(who, 104)

def checkDoublePointState(who):
	if who.doublePoint > 0 and not who.stateCtn.getItem(101):
		addState(who, 101)
	elif who.doublePoint == 0 and who.stateCtn.getItem(101):
		removeState(who, 101)
	else:
		who.stateCtn.updateItemByKey(101)

def onLogin(who, bRelogin):
	'''玩家登录时
	'''
	if not who.stateCtn.getItem(102):
		addState(who, 102)
	if not who.stateCtn.getItem(103):
		addState(who, 103)
	checkRepairState(who)

def onNewDay(who):
	'''玩家刷天时
	'''
	pass


from common import *
import state.load
