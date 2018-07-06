# -*- coding: utf-8 -*-
'''
任务相关物品
'''
import props.object

class cProps(props.object.cProps):
	def use(self, who):#override
		if task.hasTask(who, self.taskId):
			return False
		npcObj = npc.getNpcByIdx(self.npcId)
		if not npcObj:
			return False
		taskObj = task.newTask(who, npcObj, self.taskId)
		taskObj.doScript(who, npcObj, "D8001")
		who.propsCtn.addStack(self,-1)
		return True


import npc
import task
