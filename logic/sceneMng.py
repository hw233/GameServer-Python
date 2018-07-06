#-*-coding:utf-8-*-
import scene.object

#临时场景管理器
#创建出的场景实例生命期由此管理器管理
class cTempSceneMng(object):
	def __init__(self,oHolder):
		self.oHolder=weakref.ref(oHolder)
		self.dNoMapScene={}

	def _getSceneTable(self):
		return sceneData.gdData

	def _createScene(self,iNo):
		info=self._getSceneTable()
		if iNo not in info:
			raise Exception,'场景表里没有编号为{}的场景数据'.format(iNo)
		return scene.new(info["类型"], 0, info["场景名"], info.get("资源名", 0), info.get("小地图资源名", 0))

	def makeScene(self,iNo):
		oScene=self._createScene(iNo)
		oScene.no = iNo
		#一个场景编号对应多个场景实例(1对多,实际上很少有这种需求)	
		self.dNoMapScene.setdefault(iNo,set()).add(oScene)
		return oScene

	def getSceneIdsByNo(self,iNo):#一个编号对应多个场景id,实际上用的时候大多数情况是1对1
		for oScene in self.dNoMapScene.get(iNo,()):
			yield oScene.id

	def removeSceneByObj(self,oScene):
		oScene=u.getRealObj(oScene)
		iNo=oScene.no
		if iNo in self.dNoMapScene:
			self.dNoMapScene[iNo].discard(oScene)

	def removeSceneById(self,iUId):
		raise Exception,'暂时不实现,不知有没有这个需求'

	def removeSceneByNo(self,iNo):
		# for oScene in self.dNoMapScene.get(iNo,()):
		# 	oScene.remove()			
		self.dNoMapScene.pop(iNo,None)
		raise Exception, '请程序员完善此函数'

	def removeAllScene(self):#移除全部场景
		# for iNo,s in self.dNoMapScene.iteritems():
		# 	for oScene in tuple(s):
		# 		oScene.remove()#要把全部人传送走
		self.dNoMapScene={}
		raise Exception, '请程序员完善此函数'
	
	def getAllSceneId(self):#返回所有场景的id
		for l in self.dNoMapScene.itervalues():
			for oScene in l:
				yield oScene.id

	def getHolder(self):
		return self.oHolder()			
		
#临时场景
class cTempScene(scene.object.Scene):
	def __init__(self):
		scene.object.Scene.__init__(self)
	
	def isTempScene(self):#override
		return True

	def getConfig(self,sKey,uDefault=0):#override
		return sceneData.getConfig(self.no(),sKey,uDefault)


import weakref
import u
import c
import log
import misc
import role
import entity
import sceneData
import scene