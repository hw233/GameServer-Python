#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import endPointWithoutSocket
import timeU

class cPlayerEndPoint(endPointWithoutSocket.cEndPointWithoutSocket):
	def __init__(self,*tArgs,**dArgs):#override
		endPointWithoutSocket.cEndPointWithoutSocket.__init__(self,*tArgs,**dArgs)
		self.iCreateStamp=timeU.getStamp()#创建时间
		self.iRoleId = 0

	def _getEP2send(self):#override
		return client4gate.getGateEp4ss()

	def setAssociativeRole(self, iRoleId):  # 为endPoint设置关联的角色id
		self.resetAssociativeRole()  # 先重置一下再说
		self.iRoleId = iRoleId
		gRoleIdMapEndPoint.addObj(self, self.iRoleId)

	def resetAssociativeRole(self):  # 重置,不再关联角色id
		if 0 == self.iRoleId:
			return
		gRoleIdMapEndPoint.removeProxy(self.iRoleId)

	def _onDisConnected(self):#override
		endPointWithoutSocket.cEndPointWithoutSocket._onDisConnected(self)
		# print '一个backEnd连接断开了'
		gEndPointKeeper.removeObj(self.iEndPointId)
		gRoleIdMapEndPoint.removeProxy(self.iRoleId)

import c
import misc
import log
import u
import keeper
import client4gate
import config
import scene.mapdata

def sceneServerLog(path='', str=''):
	if not config.IS_INNER_SERVER:
		return
	if not path:
		path = "aoiLog"
	log.log(path, str)
	# print str

class cProxyManager(misc.cEndPointProxyManager):
	def _getEndPoint(self,iEndPointId):#override
		return gEndPointKeeper.getObj(iEndPointId)


def initTimer():#设置定时器
	scene.mapdata.loadMapData()
	import sceneService.asyncAoi
	sceneService.asyncAoi.initTimer()
	# sceneService.asyncAoi.initAoiAsyncWatch()

# def testF():
# 	print gevent.getcurrent()
# 	#gevent.sleep(2)

# watcher =gevent.get_hub().loop.check()#idleprepare
# watcher.start(testF)

if 'gbOnce' not in globals():
	gbOnce=True

	if 'sceneService' in SYS_ARGV:
		gEndPointKeeper=keeper.cKeeper()#end point id 映射 endPoint
		gRoleIdMapEndPoint=cProxyManager()#角色id映射end point,value是proxy



