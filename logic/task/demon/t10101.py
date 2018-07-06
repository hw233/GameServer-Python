# -*- coding: utf-8 -*-
from task.defines import *
from task.object import TeamTask as customTask

MAX_RING = 10 # 每轮最大环数

#导表开始
class Task(customTask):
	type = 200
	parentId = 10101
	targetType = TASK_TARGET_TYPE_FIGHT
	title = '''降魔任务'''
	intro = '''捉拿$target'''
	detail = '''帮钟馗捉拿逃出去的野鬼。'''
	initScript = '''N1001,E(1001,1001)'''

	npcInfo = {
		1001:{"名称":"$name","造型":"1111(1,1,1,1,1)","位置":"$pos"},
		1002:{"名称":"$name","造型":"1111(1,1,1,1,1)","位置":"$pos"},
	}

	eventInfo = {
		1001:{"点击":"F1001","成功":"DONE,TR1001"},
		1002:{"点击":"F1002","成功":"DONE,TR1002"},
	}

	rewardInfo = {
		1001:{"经验":"LV*5+100","宠物经验":"PLV*2+100","银币":"999","物品":"1001"},
		1002:{"经验":"LV*5+100","宠物经验":"PLV*2+100","银币":"999","物品":"1002"},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":50,"物品":"202021","数量":"5","绑定":0},
			{"权重":25,"物品":"202022","数量":"3","绑定":1},
			{"权重":25,"物品":"202023","数量":"1","绑定":0},
		),
		1002:(
			{"权重":50,"物品":"202001","数量":"5","绑定":1},
			{"权重":25,"物品":"202002","数量":"3","绑定":0},
			{"权重":25,"物品":"202003","数量":"1","绑定":0},
		),
	}

	groupInfo = {
	9001:("子时","丑时","寅时","卯时","辰时","巳时","午时","未时","申时","酉时","戌时","亥时",),
	9002:("一刻","二刻","三刻","四刻","五刻","六刻","七刻","八刻",),
	9003:("诌鬼","假鬼","奸鬼","捣大鬼","冒失鬼","挖渣鬼","仔细鬼","讨吃鬼","地哩鬼","叫街鬼","偷尸鬼","含碜鬼","倒塌鬼","涎脸鬼","滴料鬼","发贱鬼","急急鬼","耍碗鬼","低达鬼","遭瘟鬼","轻薄鬼","浇虚鬼","绵缠鬼","黑眼鬼","龌龊鬼","温斯鬼","不通鬼","诓骗鬼","急赖鬼","心病鬼","醉死鬼","抠掏鬼","伶俐鬼","急突鬼","丢谎鬼","乜斜鬼","撩桥鬼","色中饿鬼",)
	}

	chatInfo = {
		1001:'''需要队伍人数大于等于3''',
		1002:'''$roleName等级不足20,无法继续任务''',
		8001:'''降魔服妖，替天行道乃是我们分内之事，你们赶快去击败为祸的$target吧！''',
	}

	branchInfo = {
	}

	fightInfo = {
		1001:(
			{"类型":1,"名称":"$npc","造型":"1111","能力编号":"1001","数量":"1","技能":(1111,1112,)},
			{"类型":0,"名称":"绑匪","造型":"1122","能力编号":"1002","数量":"1","技能":(401,)},
			{"类型":0,"名称":"杀手","造型":"1111","能力编号":"1002","数量":"2","技能":(401,)},
		),
		1002:(
			{"类型":1,"名称":"$npc","造型":"1111","能力编号":"1001","数量":"1","技能":(1111,1112,)},
			{"类型":0,"名称":"绑匪","造型":"1122","能力编号":"1002","数量":"1","技能":(401,)},
			{"类型":0,"名称":"杀手","造型":"1111","能力编号":"1002","数量":"2","技能":(401,)},
		),
	}

	ableInfo = {
		1001:{"等级":"15","生命":"B*1","真气":"B*1","物理伤害":"B*0.6","法术伤害":"B*0.6","物理防御":"B*0.5","法术防御":"B*0.5","速度":"B*0.6","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1002:{"等级":"25","生命":"B*1","真气":"B*1","物理伤害":"B*0.6","法术伤害":"B*0.6","物理防御":"B*0.5","法术防御":"B*0.5","速度":"B*0.6","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}
#导表结束

	def onBorn(self, who, npcObj, **kwargs):
		customTask.onBorn(self, who, npcObj, **kwargs)
		if kwargs.get("ring"):
			self.set("ring", kwargs["ring"])
	
	def getRing(self):
		return self.fetch("ring") + 1

	def onMissionDone(self, who, npcObj):
		if self.id == 10101:
			for obj in self.getRoleList():
				obj.day.add("demonRing", 1)
	
			ring = self.getRing()
			if ring < 10:  # 自动给下一环
				taskObj = task.newTask(who, npcObj, self.id, ring=ring)
			else:
				if rand(100) < 50: # 厉魔任务
					taskObj = task.newTask(who, npcObj, self.id+1)

			task.service.transTargetPos(who,taskObj)

	def transNpcInfo(self, npcIdx, info, who=None):
		if "$name" in info["名称"]:
			info["名称"] = self.createRandName()
		if "$pos" in info["位置"]:
			info["位置"] = self.createRandPos()
		
		return customTask.transNpcInfo(self, npcIdx, info, who)
			
	def createRandName(self):
		lst1 = self.getGroupInfo(9001)
		lst2 = self.getGroupInfo(9002)
		lst3 = self.getGroupInfo(9003)
		return lst1[rand(len(lst1))] + lst2[rand(len(lst2))] + lst3[rand(len(lst3))]
	
	def createRandPos(self):
		posList = ("1010,48,119,0", "1010,54,108,0", "1010,64,92,0")
		return posList[rand(len(posList))]
	
	def validDoEventScript(self, who, npcObj, key):
		if key in ("点击", "回复"):
			if not who.validInTeamSize(3):
				self.doScript(who, npcObj, "TM1001")
				return 0
			for obj in self.getRoleList():
				if obj.level < 20:
					self.doScript(obj, npcObj, "TM1002")
					return 0
		return customTask.validDoEventScript(self, who, npcObj, key)
		
from common import *
import copy
import task
import task.service