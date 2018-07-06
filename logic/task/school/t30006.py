# -*- coding: utf-8 -*-
from task.defines import *
from task.school.t30001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''师门-拜访别派'''
	intro = '''拜访别派掌门$target，熟悉别派能力'''
	detail = '''在世界上行走，知己知彼很重要，熟悉其他门派的长短处更是重中之重。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1003,notSchool)'''
#导表结束

	def branchScript(self, who, npcObj, branchIdx, flag):
		'''分支脚本
		'''
		if flag == "notSchool":
			allinfo = []
			for info in self.getBranchInfo(branchIdx):
				if info["条件"] != who.school:
					allinfo.append(info)
			index = rand(len(allinfo))
			self.doScript(who, npcObj, allinfo[index]["脚本"])
		else:
			customTask.branchScript(self, who, npcObj, branchIdx, flag)		
	
from common import *
