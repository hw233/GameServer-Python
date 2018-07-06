# -*- coding: utf-8 -*-
import scene.object

class Scene(scene.object.VirtualScene):
	'''活动场景
	'''

	@property
	def kind(self):  # 场景类型
		return SCENE_TYPE_GUILD

from scene.defines import *