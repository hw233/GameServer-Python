# -*- coding: utf-8 -*-
import door

class cDoor(door.cDoor):#传送门
	def destScNo(self):
		guildObj = guild.getGuild(self.guildId)
		if self.targetSceneId == "$scene1":
			return guildObj.sceneId
		elif self.targetSceneId == "$scene2":
			return guildObj.scene2Id
		return 0

	def trigger(self,ep,who):#被触碰了
		print '你碰了个传送门'
		oScene=scene.getScene(self.destScNo())
		if not oScene:
			print '传送门不存在'
			return
		if not scene.tryTransfer(who,oScene.id,self.targetX,self.targetY):
			return
		if self.d:
			who.d = self.d
			who.attrChange('d')


import guild
import scene