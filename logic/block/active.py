# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
import pst
import block

# 玩家活跃数据
class cActive(block.cBlock, pst.cEasyPersist):
	def __init__(self, iRoleId):  # override
		self.iRoleId = iRoleId
		block.cBlock.__init__(self, '玩家活跃数据块', iRoleId)
		pst.cEasyPersist.__init__(self, self._dirtyEventHandler)
		self.setIsStm(sql.ACTIVE_INSERT)
		self.setDlStm(sql.ACTIVE_DELETE)
		self.setUdStm(sql.ACTIVE_UPDATE)
		self.setSlStm(sql.ACTIVE_SELECT)
		
		self._sceneId = self.x = self.y = 0
		self.lastSceneId = self.lastX = self.lastY = 0, 0, 0  # 最后所在永久场景的座标.

		self.hp = 0  # 生命
		self.mp = 0  # 真气

		self.reserveHp = 0  # 储备生命
		self.reserveMp = 0  # 储备真气
		
		self.huoli = 0  # 活力
		self.sp = 0  # 愤怒
		
		self.exp = 0  # 经验
		self.tradeCash = 0  # 元宝
		self.cash = 0  # 银币
		self.moneyCash = 0  # 龙纹玉
		self.diamond = 0  # 钻石
		self.doublePoint = 0  # 双倍点

	def onBorn(self):  # override
		oScene = scene.getScene(c.NEW_ROLE_BORN_NO)
		if not oScene:
			raise Exception, '编号为{}的永久场景不存在'.format(c.NEW_ROLE_BORN_NO)
		self.sceneId = self.lastSceneId = oScene.id
		self.x = self.lastX = c.NEW_ROLE_BORN_POS[0]
		self.y = self.lastY = c.NEW_ROLE_BORN_POS[1]
		self.markDirty()

	def load(self, dData):  # override
		pst.cEasyPersist.load(self, dData)

		self.lastSceneId = dData.pop("lastSceneId", c.NEW_ROLE_BORN_NO)
		self.lastX = dData.pop("lastX", c.NEW_ROLE_BORN_POS[0])
		self.lastY = dData.pop("lastY", c.NEW_ROLE_BORN_POS[1])

		lastSceneObj = scene.getScene(self.lastSceneId)
		if not lastSceneObj:
			raise Exception, '编号为{}的永久场景不存在'.format(self.lastSceneId)
		
		sceneId = dData.pop("sceneId", c.NEW_ROLE_BORN_NO)
		x = dData.pop("x", c.NEW_ROLE_BORN_POS[0])
		y = dData.pop("y", c.NEW_ROLE_BORN_POS[1])
		
		sceneObj = scene.getScene(sceneId)
		if not sceneObj or sceneObj.isTempScene():
			sceneId = self.lastSceneId
			x = self.lastX
			y = self.lastY
			
		self.sceneId = sceneId
		self.x = x
		self.y = y
		
		self.hp = max(1, dData.pop("hp", 0))
		self.mp = max(1, dData.pop("mp", 0))
		self.reserveHp = dData.pop("reserveHp", 0)
		self.reserveMp = dData.pop("reserveMp", 0)
		self.huoli = dData.pop("huoli", 0)
		self.sp = dData.pop("sp", 0)
		
		self.exp = dData.pop("exp", 0)
		self.tradeCash = dData.pop("tradeCash", 0)
		self.cash = dData.pop("cash", 0)
		self.moneyCash = dData.pop("moneyCash", 0)
		self.diamond = dData.pop("diamond", 0)
		self.doublePoint = dData.pop("doublePoint", 0)

	def save(self):
		dData = pst.cEasyPersist.save(self)
		
		dData["sceneId"] = self.sceneId
		dData["x"] = self.x
		dData["y"] = self.y
		
		dData["lastSceneId"] = self.lastSceneId
		dData["lastX"] = self.lastX
		dData["lastY"] = self.lastY

		dData["hp"] = self.hp
		dData["mp"] = self.mp
		dData['reserveHp'] = self.reserveHp
		dData['reserveMp'] = self.reserveMp
		dData["huoli"] = self.huoli
		dData["sp"] = self.sp
		
		dData["exp"] = self.exp
		dData["tradeCash"] = self.tradeCash
		dData["cash"] = self.cash
		dData["moneyCash"] = self.moneyCash
		dData["diamond"] = self.diamond
		dData["doublePoint"] = self.doublePoint

		return dData

	@property
	def sceneId(self):
		return self._sceneId
	
	@sceneId.setter
	def sceneId(self, iSceneId):
		oScene = scene.gSceneProxy.getProxy(iSceneId)
		if not oScene:
			raise Exception, '不可以设一个不存的场景id给玩家'
		self._sceneId = iSceneId  # 这句是用效代码,其他都是安全机制

		if oScene.isTempScene():  # 永久场景不会被销毁,所以不用捕捉永久场景的销毁行为
			who = getRole(self.iRoleId)
			if not who:
				raise Exception, '玩家不在内存中'		
			self.oSceneProxy = weakref.ref(oScene.this(), u.cFunctor(self.__tempSceneDeleter, who.name, oScene.name, oScene.id))
		
	def __tempSceneDeleter(self, wr, sRoleName, sSceneName, iSceneNo):  # 捕捉临时场景对象销毁行为
		oScene = scene.gSceneProxy.getProxy(self.sceneId)
		if oScene:
			return
		try:
			raise Exception, '请在场景{}:{}销毁之前,请把玩家(id:{},名字:{})的身上的场景id设为其他场景的id'.format(iSceneNo, sSceneName, self.iRoleId, sRoleName)
		except Exception:
			misc.logException()
		oBornScene = scene.getScene(c.NEW_ROLE_BORN_NO)
		if oBornScene:
			self.sceneId = oBornScene.id  # 补救一下,设为出生场景
		log.log('error', '请在场景{}销毁之前,请把玩家(id:{},名字:{})的身上的场景id设为其他场景的id'.format(sSceneName, self.iRoleId, sRoleName))

	def setLastRealPos(self, iSceneNo, x, y, bCheckEqual=True):  # 最后所在的永久场景坐标		
		if False:
			raise Exception, '场景编号{}是临时场景,不得存储'.format(iSceneNo)
		if (self.lastSceneId, self.lastX, self.lastY) == (iSceneNo, x, y):  # 新旧座标相同
			return
		if not bCheckEqual or iSceneNo != self.lastSceneId:
			self.markDirty()

		self.lastSceneId = iSceneNo
		self.lastX = x
		self.lastY = y
				
	# 获取最后一次永久场景的位置
	def getLastRealPos(self):
		return self.lastSceneId, self.lastX, self.lastY
				
	def _dirtyEventHandler(self):  # override
		factoryConcrete.activeFtr.schedule2tail4save(self.iRoleId)

	def _equal(self, sBackup, sData):  # override 判断两个dict是否相同
		dBackup, dData = ujson.loads(sBackup), ujson.loads(sData)
		for k in ("x", "y", "lastX", "lastY",): # 坐标数据不是即时保存的
			dBackup.pop(k, None)
			dData.pop(k, None)
		return dBackup == dData

from common import *
import jitKeeper
import misc
import config
import factoryConcrete
class cProductkeeper(jitKeeper.cJITproductKeeper):
	pass

if 'gKeeper' not in globals():
	if config.IS_INNER_SERVER:
		gKeeper = cProductkeeper(factoryConcrete.activeFtr)
	else:
		gKeeper = cProductkeeper(factoryConcrete.activeFtr)

import weakref
import ujson
import sql
import log

import u
import c
import scene


import role
import mainService
import svcAccount
