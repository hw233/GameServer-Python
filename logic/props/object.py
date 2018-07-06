# -*- coding: utf-8 -*-
import pst

class cProps(pst.cEasyPersist):
	'''物品基类
	'''

	MSG_FIRST=('icon','stack','no','addon','stall')
	MSG_ALL=MSG_FIRST+('value','desc','bind')#,'name'	

	MSG_DETAIL=('value','desc','bind') #详细界面所要补充发送的

	def __init__(self,iNo):
		pst.cEasyPersist.__init__(self)
		self.iNo=iNo
		self.iUid=0
		self.iStack=1 #叠加数量
		#self.iBirthday=0 #生产日期
		#self.iPos=0
		self.iOwnerId=0

	def isVirtual(self):#是不是虚拟道具.(虚拟道具指元宝,银币,声望,贡献度等等.进包裹前会解开,变成数值)
		return False

	def isTaskProps(self):#是否是任务道具(任务道具与普通道具是放在不同包裹的)
		if 203001 <= self.no() < 204001:
			return 1
		return 0

	def isVisible(self): #是否可视的
		if self.isTaskProps():
			return False
		return True

	def helpText(self):#策划人员的帮助信息
		return '<{}>没有帮助信息'.format(self.name)

	def onBorn(self,*tArgs,**dArgs):
		self.iUid=block.sysActive.gActive.genPropsId()
		#self.iBirthday=timeU.getDayNo()#生产日期
	
	@property
	def kind(self):
		'''物品类型
		'''
		return props.defines.ITEM_COMMON

	@property
	def id(self):#唯一的id,各个区也不会相同
		return self.iUid

	def no(self):#编号
		return self.iNo
	
	@property
	def idx(self):
		return self.iNo

	@property
	def name(self):#名字
		return self.getConfig('名称','')

	def compareAtSameKind(self,oProps):#比较两个kind相同的物品,如果self要比oProps排得要前,返回负值,不变返回0,否则返回正值
		iNo1,iNo2=self.no(),oProps.no()
		if iNo1!=iNo2:
			return iNo1-iNo2 #按编号排序其实无意义,但是至少保证了相同编号的物品相临显示
		return oProps.stack()-self.stack()#从多到少排

	def icon(self):#图标
		return self.getConfig('图标',0)

	def unit(self):#单位
		return self.getConfig('单位','个')

	def canDiscard(self):#是否丢弃
		return self.getConfig('是否丢弃',0)

	def desc(self):#服务器描述
		#return self.getConfig('描述','')
		return ''

	def setStallCD(self, iDayNo):
		self.set("stall",iDayNo)

	def getStallCD(self):#服务器描述
		dayNo = self.fetch("stall")
		if not dayNo:
			return 0

		day = dayNo - getDayNo()
		if day <= 0:
			self.delete("stall")
			return 0

		return day

	def valueInfo(self):#效果信息
		return None

	def getAddon(self):
		#附加状态
		addon = 0
		if self.isBind():
			addon |= props.defines.ADDON_BIND
		return addon

	def getAnima(self):#炼化灵气
		return self.getConfig("炼化灵气",0)

	# def detail(self):#个性化信息
	# 	return self.getConfig('desc','')

	#def special(self):
	#	return ''

	# def color(self):
	# 	return self.getConfig('color',0)

	# def price(self):
	# 	return self.getConfig('价格',(0,0))

	def toLogStr(self):#写到log里的给客服看的
		l=[]
		l.append('id:{},编号:{},名字:{}'.format(self.id,self.no(),self.name))
		if self.iStack>1:
			l.append('数量:{}'.format(self.iStack))
		if self.fetch('bind',False):
			l.append('绑定')
		return ','.join(l)

	def canAutoCombine(self, targetPropsObj=None):#能不能自动堆叠,带附加属性都不可以叠
		if self.maxStack() == 1:
			return False
		if targetPropsObj:
			if targetPropsObj.no() != self.no():
				return False
			if targetPropsObj.isBind() != self.isBind():
				return False
			if targetPropsObj.stack() >= targetPropsObj.maxStack():
				return False
			if targetPropsObj.fetch("stall") != self.fetch("stall"):
				return False
# 		for sKey in self.save().iterkeys():
# 			if sKey not in ("st","id", "bind"):#如果有属性不属于这几个,不可以叠加
# 				return False
		return True

	def stack(self):#叠加数量
		return self.iStack

	def maxStack(self):#最大叠加数量
		i=self.getConfig('叠加上限',1)
		# if not 1<=i<=999:
		# 	raise Exception,'堆叠数量只能是1~999,{}个是非法的.'.format(i)
		return i

	def getConfig(self,sKey,uDefault=0,iNo=0):
		if not iNo:
			iNo=self.no()
		return propsData.getConfig(iNo,sKey,uDefault)

	def setStack(self,iStack):
		self.iStack=iStack
		self.markDirty()

	def bind(self, isBinded=True):
		'''绑定或解绑
		'''
		if isBinded:
			self.set("bind", 1)
		else:
			self.delete("bind")
		self.markDirty()

	def isBind(self):#是否绑定
		return self.getConfig('绑定',0)==1 or self.fetch('bind',0)

	def isRare(self):#是否珍品
		return False

	def dumpsWithNo(self):#把物品编号与存盘数据dump成字符串,一般在写log时用
		return '{}={}'.format(self.no(),ujson.dumps(self.save()))

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		dData['id']=self.id
		if self.iStack>1:
			dData['st']=self.iStack
		#if self.iBirthday:
		#	dData['bd']=self.iBirthday
		return dData

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		self.iUid=dData.pop('id')
		self.iStack=dData.pop('st',1)
		#self.iBirthday=dData.pop('bd',0)	

	def getMsg4Item(self,oPackage,*tArgs):		
		itemMsg=props_pb2.itemMsg()
		self.setItemMsg(itemMsg,oPackage,*tArgs)
		return itemMsg

	def setItemMsg(self, itemMsg, oPackage, *tArgs):
		lNotFill=[]
		for arg in tArgs:
			if 'pos'==arg:
				itemMsg.iPos=oPackage.getPropsPos(self)
			elif 'button' == arg:
				itemMsg.buttons.extend(self._buttons())
			else:
				lNotFill.append(arg)		
		itemMsg.iPropsNo=self.no()
		itemMsg.sSerialized=self.getCommonMsg(*lNotFill).SerializeToString()

	def getMsg4Package(self,oPackage,*tArgs):
		packageItemMsg=props_pb2.packageItemMsg()
		self.setMsg4Package(packageItemMsg,oPackage,*tArgs)
		return packageItemMsg

	def setMsg4Package(self, packageItemMsg, oPackage, *tArgs):
		lNotFill=[]
		for arg in tArgs:
			if 'package'==arg:
				pass
			else:
				lNotFill.append(arg)				
		packageItemMsg.iPropsNo=self.no()
		packageItemMsg.iPackageNo=1 if not self.isTaskProps() else 2
		packageItemMsg.sSerialized=self.getCommonMsg(*lNotFill).SerializeToString()
		return packageItemMsg

	def getCommonMsg(self,*tArgs):#获取通用的道具信息
		msg=props_pb2.propsMsg()
		msg.iPropsId=self.id #必须得有的
		for arg in tArgs:
			if 'no' == arg:
				msg.iNo=self.no()
			elif 'icon' == arg:
				pass
				#msg.iPropsIcon=self.icon()
			elif 'stack' == arg:
				msg.iPropsStack=self.iStack
			elif 'name' == arg:
				#msg.sPropsName=self.name
				pass
			elif 'detail' == arg:
				pass
				# msg.sDesc=self.desc()
				#section=msg.section.add()
				#section.sTitle=self.desc()
				#msg.sPropsType = self.name
			elif 'desc'==arg:
				sDesc=self.desc()
				if sDesc:
					msg.sDesc=sDesc
			elif 'price' == arg:
				pass
				# if self.uiType()==c.PROPS_EQUIP:
				# 	lPrice=self.consumeReturn()
				# 	msg.iGold=int(lPrice[0])
				# 	msg.iDiamond=int(lPrice[1])
				# else:
				#msg.iGold,msg.iDiamond=self.price()
			elif 'bind'==arg:
				pass
			elif 'level'==arg:
				msg.iUseLv=self.level
			elif 'value'==arg:
				info = self.valueInfo()
				if info:
					msg.valueInfo.CopyFrom(info)
			elif arg=='addon':
				msg.addon = self.getAddon()
			elif arg=="stall":
				stallCD = self.getStallCD()
				if stallCD:
					msg.stallCD = stallCD
			else:
				raise Exception,'{}不知是什么域'.format(arg)
		return msg

	@property
	def key(self):#唯一的key
		return self.id

	@property
	def ownerId(self):#拥有者id
		return self.iOwnerId
	
	@ownerId.setter
	def ownerId(self, ownerId):
		self.iOwnerId = ownerId

	# def pos(self):#在包裹里的位置,装在身上的位置
	# 	return self.iPos

	# def setPos(self,iPos):
	# 	self.iPos=iPos

	def use(self, who):#使用
		who.endPoint.rpcTips("该功能尚未开放，敬请期待")
		pass

	def shortcut(self,who):#快捷使用
		return self.getConfig("快捷使用",0)

	def onAdd2container(self):#当增加到容器时
		pass

	def onRemoveFromContainer(self):#当从容器里删除时
		pass	

	def _buttons(self):#主人点开详细面板上有哪些按钮
		return [props_pb2.USE,]
	
	def getEffect(self):
		'''效果
		'''
		who = None
		if self.ownerId:
			who = getRole(self.ownerId)
			
		if not hasattr(self, "effect"):	
			self.effect = {}
			for name, val in self.getConfig("效果").iteritems():
				self.effect[name] = self.transCode(val, who)

		return self.effect
	
	def transCode(self, code, who=None):
		import common
		return common.transCode(self, code, who)
	
	def getValueByVarName(self, varName, who=None):
		if varName == "LV":
			if who:
				return who.level
			return 0
		if varName == "PL":
			return getattr(self, "quality", 0)
		if varName == "RND":
			return rand
		raise Exception("策划填的变量{}无法解析".format(varName))
	
	def getHyperLink(self):
		roleId = 0
		if self.ownerId:
			who = getRole(self.ownerId)
			if who:
				roleId = who.id
		
		return "#L2<{},1,{},{}>*[{}]*02#n".format(roleId, self.no(), self.id, self.name)
		
	
import props_pb2
import block
import props.defines
import propsData
import ujson
import giftBagData
from common import *