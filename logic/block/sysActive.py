#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import block.singleton
import misc
import config

if config.IS_INNER_SERVER:
	pass

#全局系统活跃参数
class cSysActive(block.singleton.cSingleton):
	def __init__(self):#override
		block.singleton.cSingleton.__init__(self,'系统活跃参数','sysActive')
		self.iLastPropId=0
		self.iLastPetId=0
		self.iLastRideId=0
		self.iLastVirtualSceneId=0

		self.hour=cycleData.cCycHour(2,self._dirtyEventHandler)#小时变量
		self.day=cycleData.cCycDay(2,self._dirtyEventHandler)#天变量
		self.week=cycleData.cCycWeek(2,self._dirtyEventHandler)#周变量
		self.month=cycleData.cCycMonth(2,self._dirtyEventHandler)#月变量			

	def genPropsId(self):#生成每个物品的唯一id,保证合区也不会冲突
		self.markDirty()
		self.iLastPropId=u.guIdWithPostfix(config.ZONE_NO,self.iLastPropId,True)
		#todo:检查生成的id是否已经被占用
		return self.iLastPropId

	def genPetId(self):#生成每个宠物的唯一id,保证合区也不会冲突
		self.markDirty()
		self.iLastPetId=u.guIdWithPostfix(config.ZONE_NO,self.iLastPetId,True)
		#todo:检查生成的id是否已经被占用
		return self.iLastPetId

	def genRideId(self):#生成每个坐骑的唯一id,保证合区也不会冲突
		self.markDirty()
		self.iLastRideId=u.guIdWithPostfix(config.ZONE_NO,self.iLastRideId,True)
		#todo:检查生成的id是否已经被占用
		return self.iLastRideId
	
	def genVirtualSceneId(self):
		'''生成虚拟场景id
		'''
		import scene
		self.markDirty()
		if self.iLastVirtualSceneId == 0:
			self.iLastVirtualSceneId = u.guIdWithPostfix(config.ZONE_NO, scene.gSaveVirtualSceneId, False)
		else:
			self.iLastVirtualSceneId = u.guIdWithPostfix(config.ZONE_NO, self.iLastVirtualSceneId, True)
		return self.iLastVirtualSceneId

	def onBorn(self):#override
		self.markDirty()
		self.iLastPropId=u.guIdWithPostfix(config.ZONE_NO)
		self.iLastPetId=u.guIdWithPostfix(config.ZONE_NO)
		self.iLastRideId=u.guIdWithPostfix(config.ZONE_NO)

	def load(self,dData):#override
		block.singleton.cSingleton.load(self,dData)
		self.iLastPropId=dData.pop('propsId',u.guIdWithPostfix(config.ZONE_NO))#正常存盘情况下,必须有这个key
		self.iLastPetId=dData.pop('petId',u.guIdWithPostfix(config.ZONE_NO))#正常存盘情况下,必须有这个key
		self.iLastRideId=dData.pop('rideId',u.guIdWithPostfix(config.ZONE_NO))#正常存盘情况下,必须有这个key
		self.iLastVirtualSceneId=dData.pop('virtualSceneId', 0)
	
		if not self.delete('correctClose',0):#不正常关机,id跳过一部分(虽不能真正解决问题,也可绕过部分问题)
			self.iLastPropId+=1000
			self.iLastPetId+=1000
			self.iLastRideId+=1000
			self.markDirty()
			log.log('info','启服了,发现上一次非正常停服')

		self.hour.load(dData.pop('h',{}))
		self.day.load(dData.pop('d',{}))
		self.week.load(dData.pop('w',{}))
		self.month.load(dData.pop('m',{}))

	def save(self):#override
		dData=block.singleton.cSingleton.save(self)
		dData['propsId']=self.iLastPropId
		dData['petId']=self.iLastPetId
		dData['rideId']=self.iLastRideId
		dData['virtualSceneId']=self.iLastVirtualSceneId

		dHour=self.hour.save()
		if dHour:
			dData['h']=dHour
		dDay=self.day.save()
		if dDay:
			dData['d']=dDay
		dWeek=self.week.save()
		if dWeek:
			dData['w']=dWeek
		dMonth=self.month.save()
		if dMonth:
			dData['m']=dMonth

		return dData


	def onStopServer(self):#正常停服维护要调用一下这个函数
		self.set('correctClose',1)

	def recordResource(self,sResourceType,iAdd):#记录资源投放与回收
		if sResourceType=='diamond':
			sFlag='deDiamond' if iAdd>0 else 'inDiamond'
		elif sResourceType=='gold':
			sFlag='deGold' if iAdd>0 else 'inGold'
		elif sResourceType=='voucher':
			sFlag='deVoucher' if iAdd>0 else 'inVoucher'
		else:
			raise Exception,'未知资源标识.'
		self.add(sFlag,iAdd)
		self.hour.add(sFlag,iAdd)
		self.day.add(sFlag,iAdd)
		self.week.add(sFlag,iAdd)
		self.month.add(sFlag,iAdd)

	def resourceStat(self,sResourceType,sSeparator=','):#资源投放与回收统计展现
		if sResourceType=='diamond':
			sOutFlag,sInFlag='deDiamond','inDiamond'
		elif sResourceType=='gold':
			sOutFlag,sInFlag='deGold','inGold'
		elif sResourceType=='voucher':
			sOutFlag,sInFlag='deVoucher','inVoucher'
		else:
			raise Exception,'未知资源标识.'

		l=[]

		iOut,iIn=self.fetch(sOutFlag),self.fetch(sInFlag)
		iHold=iOut+iIn
		l.append('系统总投放{},系统总回收{},玩家总持有量{}'.format(iOut,iIn,iHold))

		iOut,iIn=self.hour.fetch(sOutFlag),self.hour.fetch(sInFlag)
		iHold=iOut+iIn
		l.append('本小时投放{},本小时回收{},本小时玩家持有量{}'.format(iOut,iIn,iHold))

		iOut,iIn=self.day.fetch(sOutFlag),self.day.fetch(sInFlag)
		iHold=iOut+iIn
		l.append('今天投放{},今天回收{},今天玩家持有量{}'.format(iOut,iIn,iHold))

		iOut,iIn=self.week.fetch(sOutFlag),self.week.fetch(sInFlag)
		iHold=iOut+iIn
		l.append('本周投放{},本周回收{},本周玩家持有量{}'.format(iOut,iIn,iHold))

		iOut,iIn=self.month.fetch(sOutFlag),self.month.fetch(sInFlag)
		iHold=iOut+iIn
		l.append('本月投放{},本月回收{},本月玩家持有量{}'.format(iOut,iIn,iHold))

		return sSeparator.join(l)





def init():
	global gActive
	gActive=cSysActive()
	if not gActive._loadFromDB():
		gActive._insertToDB(*gActive.getPriKey())

import u
import misc
import timeU
import log
import cycleData
import config