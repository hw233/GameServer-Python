#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import u
import entity
import keeper

if 'gMstProxy' not in globals():
	gMstProxy=u.cKeyMapProxy()

class cMonsterBase(entity.cEntity):#怪物基类,假设数据不是从策划数据表读的
	def __init__(self):
		entity.cEntity.__init__(self)
		gMstProxy.addObj(self,self.id)
		
	def ettType(self):#override
		return scene_pb2.INFO_MONSTER

	def trigger(self,ep,who):#override 被触碰了
		raise Exception,'客户端不应该发送怪物被触碰的消息吧.'

	@property
	def level(self):
		raise NotImplementedError,'请在子类override'

	def cls(self):
		raise NotImplementedError,'请在子类override'

	def ai(self):
		raise NotImplementedError,'请在子类override'

	def hp(self):
		raise NotImplementedError,'请在子类override'

	def hpMax(self):#血量上限
		raise NotImplementedError,'请在子类override'

	def mp(self):
		raise NotImplementedError,'请在子类override'

	def mpMax(self):#血量上限
		raise NotImplementedError,'请在子类override'

	def crit(self):
		raise NotImplementedError,'请在子类override'

	def att(self):
		raise NotImplementedError,'请在子类override'

	def hit(self):
		raise NotImplementedError,'请在子类override'

	def dodge(self):
		raise NotImplementedError,'请在子类override'

	def defense(self):
		raise NotImplementedError,'请在子类override'

	def monsType(self):
		raise NotImplementedError,'请在子类override'

	def monsSkill(self):
		raise NotImplementedError,'请在子类override'

	def scaleX(self):
		raise NotImplementedError,'请在子类override'

	def scaleY(self):
		raise NotImplementedError,'请在子类override'

	def hpAmount(self):
		raise NotImplementedError,'请在子类override'

	def isSmartMonster(self):
		raise NotImplementedError,'请在子类override'

	def isKillTarget(self):
		raise NotImplementedError,'请在子类override'

	def skillInfo(self):
		l=[]
		for iNo,iLevel in self.monsSkill().iteritems():
			msg=scene_pb2.mstSkill()
			msg.iNo=iNo
			msg.iLevel=iLevel
			l.append(msg)
		return l

	def _getPb2Msg(self):
		mstInfo=scene_pb2.mstInfo()
		mstInfo.iEttId=self.id
		if self.no():
			mstInfo.iNo=self.no()
		if self.name:
			mstInfo.sName=self.name
		if self.level:
			mstInfo.iLevel=self.level
		if self.cls():
			mstInfo.sClass=self.cls()
		if self.ai():
			mstInfo.sAi=self.ai()
		if self.hp():
			mstInfo.iHP=self.hp()  #怪物当前血量
		if self.hpMax():
			mstInfo.iMaxHp=self.hpMax()
		if self.mpMax():
			mstInfo.iMaxMp=self.mpMax()
		if self.mp():
			mstInfo.iMp=self.mp()
		if self.crit():
			mstInfo.iCrit=self.crit()
		if self.att():
			mstInfo.iAtt=self.att()
		# mstInfo.iSpirit=self.spirit()
		if self.hit():
			mstInfo.iHit=self.hit()
		if self.dodge():
			mstInfo.iDodge=self.dodge()
		if self.defense():
			mstInfo.iDef=self.defense()
		if self.monsType():
			mstInfo.iType=self.monsType() #是否是boss
		if self.hpAmount():
			mstInfo.iHpbar=self.hpAmount()
		mstInfo.skill.extend(self.skillInfo())
		mstInfo.fScaleX=self.scaleX()
		mstInfo.fScaleY=self.scaleY()
		mstInfo.bKillTarget=self.isKillTarget()
		mstInfo.iBgEft=self.getConfig('effect', 0)	#背景特效
		mstInfo.iApareType=self.getConfig('apareType',0)
		return mstInfo

	#场景广播包(每次要的时候都重新序列化整个消息，不缓存，1是因为副本内没有几个人，序列化次数不多,
	#2是因为hp,x,y之类的属性变化太快，缓存很快就过期)
	# def getSerialized1(self):
	# 	mstInfo=self._getPb2Msg()
	# 	ettEnter=scene_pb2.entityEnter()
	# 	ettEnter.iEttType=self.ettType()
	# 	# ettEnter.iEttType= scene_pb2.INFO_ESCORT if self.monsType() == c.MONSTER_ESCORT else scene_pb2.INFO_MONSTER
	# 	ettEnter.iX=self.x
	# 	ettEnter.iY=self.y
	# 	ettEnter.iSceneId=self.sceneId
	# 	ettEnter.ettInfo=mstInfo.SerializeToString()
	# 	return endPoint.makePacket('rpcEttEnter',ettEnter)

	# def getSerializedGroup(self):#override 场景广播包组
	# 	return [self.getSerialized1()]

	#扣除怪物血量
	def reduceMonsterHp(self,iHp,oAttacker):
		iRecord=iHp
		if iHp>self.iHp:
			iRecord=self.iHp
			self.iHp=0
		else :
			self.iHp=self.iHp-iHp
		#统计玩家杀怪血量
		oAttacker.triggerEvent(event.ATTACK_MONSTER,self)
		oInstance=oAttacker.getInstanceObj() #副本对象
		if not oInstance:
			return
		oInstance.flushScoreInfo(oAttacker.id,instance.HURT_TOTAL,iRecord)  #更新玩家击杀的血量
		geMonsterReduce(self,oAttacker,iHp)	#触发全局怪物扣血事件
		#怪物死亡触发
		if self.iHp<=0:
			oInstance.triggerMonsterDie(self,oAttacker)

	def addHp(self,iAdd,oAttacker=None):
		self.iHp+=iAdd
		if self.iHp<=0 and oAttacker:
			oInstance=oAttacker.getInstanceObj() #副本对象
			if oInstance:
				oInstance.triggerMonsterDie(self,oAttacker)
		return iAdd

	#获取怪物当前血量
	def monsterHp(self):
		return self.iHp

	#同步怪物属性包
	def synMonsterAttr(self,*sAttrName):
		mstInfo=scene_pb2.mstInfo()
		mstInfo.iEttId=self.id
		for sName in sAttrName:
			if sName=='hp':
				mstInfo.iHP=self.iHp
		return mstInfo

	def isDead(self):
		return self.iHp<=0

class cMonster(cMonsterBase):
	def __init__(self,iNo):
		cMonsterBase.__init__(self)
		self.iNo=iNo
		self.dDamage={}#各角色id对我的伤害
		self.dPositiveSkill={}
		self.dNegativeSkill={}
		self.iHp=self.getConfig('hp',0)  #怪物初始血量,不是maxhp,maxhp只是血量上限
		self.bKillTarget=False	#是否是指定击杀目标
		self.iMaxHp=self.getConfig('maxhp', 10)
		self.iAtt=self.getConfig('att',0)
		
	def no(self):#override
		return self.iNo

	def dir(self):#方向
		return self.iDir
		
	def setDir(self,iDir):
		self.iDir=iDir

	def hp(self):
		return self.iHp

	def hpMax(self):#血量上限
		return self.iMaxHp
		# return self.getConfig('maxhp',0)

	def mp(self):
		return self.getConfig('mp',0)

	def mpMax(self):#血量上限
		return self.getConfig('maxmp',0)

	def isBoss(self):
		return self.getConfig('kind',0)==c.MONSTER_BOSS

	@property
	def name(self):#override,从表中读
		return self.getConfig('name','')

	@property
	def shape(self):#override,从表中读
		return self.getConfig('shape',0)

	def att(self):#攻击
		return self.iAtt
		# return self.getConfig('att',0)

	def defense(self):#防御
		return self.getConfig('defense',0)

	def crit(self):#暴击
		return self.getConfig('crit',0)

	def spirit(self):#精神
		return self.getConfig('spirit',0)

	def hit(self):#命中
		return self.getConfig('hit',0)

	def dodge(self):#闪避
		return self.getConfig('dodge',0)

	def defense(self):#防御
		return self.getConfig('def',0)

	def monsType(self):
		return self.getConfig('kind',0)

	def exp(self):#杀死这个怪,奖励给玩家的经验值
		return self.getConfig('exp',0)

	def gold(self):#杀死这个怪,奖励给玩家的元宝
		return self.getConfig('gold',0)

	def point(self):#杀死这个怪,奖励给玩家的积分
		return self.getConfig('point',0)

	def cls(self):#怪物class
		return self.getConfig('class',0)

	@property
	def level(self):#怪物等级
		return self.getConfig('lv',0)

	def ai(self):#怪物ai
		return self.getConfig('ai','')

	def hpAmount(self):#血条数
		return self.getConfig('hpAmount','')

	def launch(self):#掉落组
		return self.getConfig('launchgroup',0)

	def getConfig(self, sKey, uDefault=0, iNo=0):
		if not iNo:
			iNo = self.no()
		return monsterData.getConfig(iNo, sKey, uDefault)

	def monsSkill(self):
		return {}

	def scaleX(self):
		return self.getConfig('scaleX',1)

	def scaleY(self):
		return self.getConfig('scaleY',1)

	def isSmartMonster(self):#怪物属性是否动态变化
		return False

	def isKillTarget(self):#
		return self.bKillTarget

	def setkillTarget(self, bIsKillTarget):
		self.bKillTarget=bIsKillTarget

def new(iNo,iSceneId,x,y):
	if iNo not in gdMstModule:
		raise Exception,'没有编号为{}的怪物或可破坏物'.format(iNo)
	else:
		obj=gdMstModule[iNo].cMonster(iNo)
	obj.sceneId = iSceneId
	obj.x = x
	obj.y = y
	#gdBuffMonster[iNo]=obj
	return obj

# def getBuffMonster(iNo):
# 	return gdBuffMonster.get(iNo)

# if 'gdBuffMonster' not in globals():
# 	gdBuffMonster={}

if 'gdMstModule' not in globals():
	gdMstModule={}
	geMonsterReduce=u.cEvent()	#怪物扣血事件

THIS_MODULE=__import__(__name__)
def init():
	pass


import scene_pb2
import role
import weakref
import event


import c
import endPoint
import instance
import u

init()