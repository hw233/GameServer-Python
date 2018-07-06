# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
		1001:{"名称":"未知","造型":"2005(0,1,0,0,0)","位置":"1001,57,59,5","称谓":"接引人1"},
		1002:{"名称":"未知","造型":"2005(0,1,0,0,0)","位置":"1001,97,52,6","称谓":"接引人2"},
		1003:{"名称":"未知","造型":"2005(0,1,0,0,0)","位置":"1001,108,31,7","称谓":"接引人3"},
		1004:{"名称":"未知","造型":"2005(0,1,0,0,0)","位置":"1001,105,19,8","称谓":"接引人4"},
		1005:{"名称":"未知","造型":"2005(0,1,0,0,0)","位置":"1001,58,10,1","称谓":"接引人5"},
		1006:{"名称":"未知","造型":"2005(0,1,0,0,0)","位置":"1001,27,18,2","称谓":"接引人6"},
		1007:{"名称":"未知","造型":"2005(0,1,0,0,0)","位置":"1001,14,36,3","称谓":"接引人7"},
		1008:{"名称":"未知","造型":"2005(0,1,0,0,0)","位置":"1001,30,54,4","称谓":"接引人8"},
		2001:{"名称":"迷宫老朽","造型":"2010(0,1,0,0,0,0)","位置":"1001,43,23,6","称谓":"仙盟迷宫"},
		2002:{"名称":"迷宫老朽","造型":"2010(0,1,0,0,0,0)","位置":"1001,67,40,4","称谓":"仙盟迷宫"},
		3001:{"名称":"宝箱","造型":"8004(0,1,0,0,0)","位置":"1001,65,36,6","动作":5},
		3002:{"名称":"小宝箱","造型":"8004(0,1,0,0,0)","位置":"2010,0,0,6","动作":5},
	}

	eventInfo = {
		1001:{"点击":"$box"},
	}

	rewardInfo = {
		1001:{"经验":lambda LV:LV*400+1000,"宠物经验":lambda LV:LV*400+1000,"银币":lambda LV:LV*40+200,"物品":[1001,2001]},
		1002:{"经验":lambda LV:LV*500+2000,"宠物经验":lambda LV:LV*500+2000,"银币":lambda LV:LV*50+200,"物品":[1002,2002]},
		1003:{"经验":lambda LV:LV*600+3000,"宠物经验":lambda LV:LV*600+3000,"银币":lambda LV:LV*60+200,"物品":[1003,2003]},
		2001:{"银币":lambda :1000},
	}

	rewardPropsInfo = {
		2001:(
			{"权重":100,"物品":"200009","数量":"5","绑定":0,"传闻":0},
		),
		2002:(
			{"权重":100,"物品":"200009","数量":"10","绑定":0,"传闻":0},
		),
		2003:(
			{"权重":100,"物品":"200009","数量":"15","绑定":0,"传闻":0},
		),
		1001:(
			{"权重":90,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":90,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":90,"物品":"230102","数量":"2","绑定":0,"传闻":0},
			{"权重":90,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":70,"物品":"230103","数量":"1","绑定":0,"传闻":0},
			{"权重":60,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246001","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246002","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246003","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246004","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246005","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246006","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246007","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246008","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246009","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246010","数量":"1","绑定":0,"传闻":0},
		),
		1002:(
			{"权重":3,"物品":"234101","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234102","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234103","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234104","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234105","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234106","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234107","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234108","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234109","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234110","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234111","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234112","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234113","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234114","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234115","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234116","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234117","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234118","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234119","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234120","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234121","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234122","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234123","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234124","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234125","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234126","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234127","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234128","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234129","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234130","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234131","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234132","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234133","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234134","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234135","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234136","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234137","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234138","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234139","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234140","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234141","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234142","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234143","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234144","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234145","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234146","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234147","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234148","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234149","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234150","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234151","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234152","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234153","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":3,"物品":"234901","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":60,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":60,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":60,"物品":"230102","数量":"2","绑定":0,"传闻":0},
			{"权重":60,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":60,"物品":"230103","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246001","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246002","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246003","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246004","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246005","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246006","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246007","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246008","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246009","数量":"1","绑定":0,"传闻":0},
			{"权重":38,"物品":"246010","数量":"1","绑定":0,"传闻":0},
		),
		1003:(
			{"权重":5,"物品":"234101","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234102","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234103","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234104","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234105","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234106","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234107","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234108","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234109","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234110","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234111","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234112","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234113","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234114","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234115","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234116","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234117","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234118","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234119","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234120","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234121","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234122","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234123","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234124","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234125","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234126","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234127","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234128","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234129","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234130","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234131","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234132","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234133","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234134","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234135","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234136","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234137","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234138","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234139","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234140","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234141","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234142","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234143","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234144","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234145","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234146","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234147","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234148","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234149","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234150","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234151","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234152","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234153","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":5,"物品":"234901","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234401","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234402","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234403","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234404","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234405","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234406","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234407","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234408","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234409","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234410","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234411","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234412","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234413","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234414","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234415","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234416","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234417","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234418","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234419","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":4,"物品":"234420","数量":"1","绑定":0,"传闻":"SM6003"},
			{"权重":60,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":60,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":60,"物品":"230102","数量":"2","绑定":0,"传闻":0},
			{"权重":60,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":60,"物品":"230103","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246001","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246002","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246003","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246004","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246005","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246006","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246007","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246008","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246009","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"246010","数量":"1","绑定":0,"传闻":0},
		),
	}

	groupInfo = {
	}

	chatInfo = {
		1001:'''老朽我以八门阵法组成了一个迷宫，一共15层，看你们能不能破此迷宫寻得宝物\nQ进入迷宫\nQ规则说明''',
		1002:'''进入迷宫需要等级≥20''',
		1003:'''你不是此仙盟成员，无法进入迷宫''',
		1004:'''迷宫只能单人进入，请先离开队伍''',
		1005:'''休、生、伤、杜、景、死、惊、开，八门八变，只有生门能进入下一层。我是其中一个门接引人，你要从我这里进入下一层吗？\nQ进入此门''',
		1006:'''你进入了休门，被强制休息15秒，不能和接引人沟通''',
		1007:'''你进入了生门，成功进入下一层''',
		1008:'''你进入了伤门，触动了守门卫士''',
		1009:'''很遗憾你战败了，被传送回了第1层''',
		1010:'''你进入了杜门，被传送回了第$floor层''',
		1011:'''你进入了景门，被传送回了第$floor层''',
		1012:'''你进入了死门，被传送回了第$floor层''',
		1013:'''你进入了惊门，随机传送到了第$floor层''',
		1014:'''你进入了开门，被传送回了第$floor层''',
		1015:'''恭喜少侠通过考验。需要离开迷宫吗？\nQ离开迷宫\nQ再等等''',
		1016:'''1.玩家等级≥#C0220级#n，只能单人进入\n2.迷宫一共#C0215层#n，每层只有#C02生门#n能进入下一层\n3.迷宫第#C025、10、15层#n各有一个宝箱，大家齐心协力才能更快地通过迷宫''',
		6001:'''#L1<14,28>*[仙盟迷宫]*02#n将在#C0212:00#n准时开始，请各位仙友做好准备，前往等待活动开始''',
		6002:'''#L1<14,28>*[仙盟迷宫]*02#n已经开始，请准备好的仙友快进入迷宫，寻找迷宫内的宝物''',
		6003:'''$roleName在#L1<14,28>*[仙盟迷宫]*02#n中开启了大宝箱，获得了$lnkProps''',
	}

	branchInfo = {
	}

	fightInfo = {
		1001:(
			{"类型":0,"名称":"守门卫士","造型":"4502(0,1,0,0,0)","能力编号":"1001","数量":"3","技能":(1133,1211,1323,1413,1532,1623,),"站位":(1,4,5,)},
			{"类型":0,"名称":"守门卫士","造型":"4504(0,1,0,0,0)","能力编号":"1001","数量":"2","技能":(1133,1211,1323,1413,1532,1623,),"站位":(2,3,)},
		),
	}

	ableInfo = {
		1001:{"等级":"ALV","生命":"B*0.8","真气":"B*1","物理伤害":"B*0.5","法术伤害":"B*0.5","物理防御":"B*0.5","法术防御":"B*0.5","速度":"B*0.5","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}

	lineupInfo = {
	}

	sceneInfo = {
		1001:{"名称":"第$floor层","资源":2010,"小地图资源":2010,"着陆点x":61,"着陆点y":35},
	}

	configInfo = {
	}
#导表结束

	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.state = 0 # 活动状态, 0.已结束  1.进行中
		self.roleInfoList = {} # 角色信息列表
		self.guildAct = {}

	def beginNotify(self, nextTime):
		'''开启通知
		'''
		if nextTime == 300:
			self.timerMgr.run(functor(self.beginNotify, 240), nextTime, 0, "beginNotify")
			self.initGuildAct()
		elif nextTime == 240:
			self.timerMgr.run(functor(self.beginNotify, None), nextTime, 0, "beginNotify")
		else:
			self.timerMgr.run(self.begin, 60, 0, "begin")
		for guildObj in guild.gGuildKeeper.getIterValues():
			message.guildMessage(guildObj.id, self.getText(6001))

	def initGuildAct(self):
		'''初始化各仙盟活动对象
		'''
		self.roleInfoList = {}
		self.guildAct = {}
		for guildObj in guild.gGuildKeeper.getIterValues():
			actObj = cGuildAct(guildObj.id, self, self.__dirtyEventHandler)
			self.guildAct[guildObj.id] = actObj
			actObj.init()

	def actNotify(self):
		'''活动通知
		'''
		for guildId in self.guildAct.iterkeys():
			message.guildMessage(guildId, self.getText(6002))

	def begin(self):
		'''开始活动
		'''
		if self.state == 1:
			return
		self.state = 1
		self.timerMgr.run(self.actNotify, 0, 1800, "actNotify")
		self.refreshForBegin()

	def end(self):
		'''结束活动
		'''
		if self.timerMgr.hasTimerId("actNotify"):
			self.timerMgr.cancel("actNotify")
		self.state = 0
		self.clearForEnd()

	def onNewHour(self, day, hour, wday):
		if wday not in (1, 3, 5):
			return
		if hour == 11:
			self.timerMgr.run(functor(self.beginNotify, 300), 3000, 0, "beginNotify")
		elif hour == 12:
			if self.state != 1:
				self.begin()
		elif hour == 14:
			if self.state != 0:
				self.end()

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		currentMonsterType = getattr(self, "currentMonsterType", None)
		if currentMonsterType:
			cls = getMonsterTypeClass(self.currentMonsterType)
			return cls(self)
		return customActivity.newNpc(self, npcIdx, name, shape, who)

	def addNpc(self, npcIdx, typeFlag="npc", who=None):
		npcObj = template.Template.addNpc(self, npcIdx, typeFlag, who)
		if not typeFlag.startswith(("door", "box")):
			scene.switchSceneForNpc(npcObj, npcObj.sceneId, npcObj.x, npcObj.y, npcObj.d)
		return npcObj

	def createNpc(self, npcIdx, who=None):#override
		'''创建Npc
		'''
		npcObj = customActivity.createNpc(self, npcIdx, who)
		#npc场景ID设置为虚拟场景ID
		npcObj.sceneId = self.currentSceneId
		return npcObj

	def getActivityNpc(self, who, npcIdx):
		'''活动入口NPC
		'''
		guildId = who.getGuildId()
		if not guildId:
			return None
		guildAct = self.guildAct.get(guildId)
		if not guildAct:
			return None
		typeFlag = "actNpc{}".format(guildId)
		npcList = self.getNpcListByType(typeFlag)
		for npcObj in npcList:
			if npcObj.guildId == guildId and npcObj.idx == npcIdx:
				return npcObj
		return None

	def createActNpc(self, guildObj):
		self.currentSceneId = guildObj.sceneId
		guildId = guildObj.id
		self.currentMonsterType = 2001
		npcObj = self.addNpc(self.transIdxByGroup(2001), "actNpc{}".format(guildId))
		npcObj.guildId = guildId
		self.currentMonsterType = None

	def createFinalNpc(self, sceneId):
		self.currentSceneId = sceneId
		self.currentMonsterType = 2002
		npcObj = self.addNpc(self.transIdxByGroup(2002), "finalNpc")
		self.currentMonsterType = None

	def createBox(self, guildId, sceneId, floor):
		'''大宝箱
		'''
		self.currentSceneId = sceneId
		npcObj = self.addNpc(3001, "box")
		npcObj.eventIdx = 1001
		npcObj.floor = floor
		npcObj.guildId = guildId
		sceneObj = scene.getScene(sceneId)
		sceneObj.addEntity(npcObj, npcObj.x, npcObj.y, npcObj.d)

	def createTinyBox(self, guildAct):
		guildId = guildAct.guildId
		cnt = min(10, 20 - len(self.getNpcListByType("tinybox{}".format(guildId))))
		if cnt < 1:
			return
		sceneIds = shuffleList(guildAct.sceneInfo.values())
		for i in xrange(cnt):
			self.currentSceneId = sceneIds[i]
			npcObj = self.addNpc(3002, "tinybox{}".format(guildId))
			npcObj.eventIdx = 1001

	def createDoorNpc(self, guildId, sceneId, floor):
		'''门NPC
		'''
		self.currentSceneId = sceneId
		self.currentMonsterType = 1001
		doorType = shuffleList([1, 2, 3, 4, 5, 6, 7, 8])
		for i in xrange(8):
			npcObj = self.addNpc(self.transIdxByGroup(1001+i), "door")
			npcObj.floor = floor
			npcObj.doorType = doorType[i]
			npcObj.guildId = guildId
			sceneObj = scene.getScene(sceneId)
			sceneObj.addEntity(npcObj, npcObj.x, npcObj.y, npcObj.d)
		self.currentMonsterType = None

	def getDoorNpc(self, sceneId, guildId, idx):
		for npcObj in self.getNpcListByType("door"):
			if npcObj.idx != idx:
				continue
			if npcObj.sceneId == sceneId and npcObj.guildId == guildId:
				return npcObj

	def getBoxNpc(self, sceneId, guildId):
		for npcObj in self.getNpcListByType("box"):
			if npcObj.sceneId == sceneId and npcObj.guildId == guildId:
				return npcObj

	def createActScene(self, guildAct):
		'''生成活动场景
		'''
		for i in xrange(1, 16):
			sceneObj = self.addScene(1001, "gameScene")
			sceneObj.name = "第{}层".format(i)
			sceneObj.floor = i
			sceneObj.denyTeam = "仙盟迷宫"
			sceneObj.denyTransfer = "仙盟迷宫无法传送"
			sceneObj.eventOnEnter += onEnter
			guildAct.sceneInfo[i] = sceneObj.id
			if i in (5, 10, 15):
				self.createBox(guildAct.guildId, sceneObj.id, i)
			if i < 15:
				self.createDoorNpc(guildAct.guildId, sceneObj.id, i)
			else:
				self.createFinalNpc(sceneObj.id)

	def enterMaze(self, who, guildId):
		'''进入迷宫
		'''
		actObj = self.guildAct[guildId]
		sceneId = actObj.sceneInfo[1]
		self.transfer(who, sceneId, 61, 35)
		if not who.day.fetch("guildMaze"):
			who.day.set("guildMaze", 1)

	def clearForEnd(self):
		for sceneObj in self.getSceneListByType("gameScene"):
			for roleId in sceneObj.getRoleList():
				who = getRole(roleId)
				if not who:
					continue
				if who.inTeam() and not who.getTeamObj().isLeader(who.id):
					continue
				self.leaveScene(who)
		self.removeSceneAll()
		for actObj in self.guildAct.itervalues():
			actObj.clearForEnd()

	def leaveScene(self, who):
		'''离开场景
		'''
		if who.inWar(): # 如果还在战斗中，结束战斗
			who.war.kickWarrior(who.warrior)
		guildObj = who.getGuildObj()
		if guildObj:
			sceneId, x, y = guildObj.sceneId, 0, 0
		else:
			sceneId, x, y = 1130, 101, 63
		self.transfer(who, sceneId, x, y)
		self.changeRoleInfo(who.id, "inGame", 1)

	def refreshForBegin(self):
		if not self.guildAct:
			self.initGuildAct()
		for actObj in self.guildAct.itervalues():
			actObj.refreshForBegin()

	def customEvent(self, who, npcObj, eventName, *args):
		if eventName == "box": # 开宝箱
			self.openBox(who, npcObj)

	def openBox(self, who, npcObj):
		'''开宝箱
		'''
		boxes = self.getRoleInfoByKey(who.id, "boxes")
		floor = getattr(npcObj, "floor", None)
		if floor in boxes:
			message.tips(who, "你已经打开过这个宝箱了")
			return
		if floor == 5:
			idx = 1001
		elif floor == 10:
			idx = 1002
		elif floor == 15:
			idx = 1003
		else:
			idx = 2001
		self.reward(who, idx)
		if floor:
			boxes.add(floor)
			self.changeRoleInfo(who.id, "boxes", boxes)
			self.refreshBox2Role(who, npcObj, False)
			self.refreshFloorDoor2Role(who)
		if npcObj.typeFlag.startswith("tinybox"):
			self.removeNpc(npcObj)

	def getRoleInfo(self, roleId):
		'''角色信息
		'''
		return self.roleInfoList.get(roleId)

	def createRoleInfo(self, who):
		'''创建角色信息
		'''
		if not getattr(self, "roleInfoList", None):
			self.roleInfoList = {}
		roleId = who.id
		info = self.roleInfoList.get(roleId)
		if not info:
			info = {
				"doors": set(), # 进入过的门编号
				"boxes": set(), # 
				"inGame": 0, # 是否在迷宫中
			}
			self.roleInfoList[roleId] = info
		return info

	def changeRoleInfo(self, roleId, key, val):
		'''修改角色信息
		'''
		info = self.getRoleInfo(roleId)
		if not info:
			return
		info[key] = val

	def getRoleInfoByKey(self, roleId, key):
		'''根据键名获取角色信息
		'''
		info = self.getRoleInfo(roleId)
		if info:
			return info.get(key, 0)
		return 0

	def refreshDoor2Role(self, who, npcObj, isEnter=True):
		'''刷新门到角色
		'''
		npcObj.sSerialized1 = None
		doors = self.getRoleInfoByKey(who.id, "doors")
		if npcObj.id in doors:
			npcObj.name = DOOR_NAMES[npcObj.doorType-1]
		else:
			npcObj.name = "未知"
		if isEnter:
			who.endPoint.send(npcObj.getSerialized1())
		else:
			who.endPoint.rpcEttLeave(npcObj.id)

	def refreshBox2Role(self, who, npcObj, isEnter=True):
		'''刷新宝箱到角色
		'''
		if isEnter:
			who.endPoint.send(npcObj.getSerialized1())
		else:
			who.endPoint.rpcEttLeave(npcObj.id)

	def refreshFloorDoor2Role(self, who):
		for i in xrange(8):
			npcObj = self.getDoorNpc(who.sceneId, who.getGuildId(), 1001+i)
			if not npcObj:
				continue
			self.refreshDoor2Role(who, npcObj)

	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 101:
			if self.state != 1:
				self.initGuildAct()
				self.begin()
			else:
				message.tips(who, "活动已经开启")
		elif cmdIdx == 102:
			if self.state != 0:
				self.end()
			else:
				message.tips(who, "活动已经结束")
		elif cmdIdx == 103:
			floor = int(args[0])
			guildAct = self.guildAct.get(who.getGuildId())
			sceneId = guildAct.sceneInfo.get(floor)
			self.transfer(who, sceneId, 61, 35)


import activity.object

class cNpc2001(activity.object.Npc):
	'''活动npc2001
	'''
	def doLook(self, who):
		content = getActivity().getText(1001)
		selList = [1, 2]
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)

	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.enterMaze(who)
		elif sel == 2:
			self.mazeDesc(who)

	def enterMaze(self, who):
		'''进入迷宫
		'''
		actObj = getActivity()
		if who.level < 20:
			self.say(who, actObj.getText(1002))
			return
		elif who.getGuildId() != self.guildId:
			self.say(who, actObj.getText(1003))
			return
		elif who.getTeamObj():
			self.say(who, actObj.getText(1004))
			return
		elif getActivity().state != 1:
			self.say(who, "活动还未开启")
			return
		getActivity().enterMaze(who, self.guildId)

	def mazeDesc(self, who):
		'''迷宫规则说明
		'''
		actObj = getActivity()
		self.say(who, actObj.getText(1016))


class cNpc2002(activity.object.Npc):
	'''活动npc2002
	'''
	def doLook(self, who):
		content = getActivity().getText(1015)
		selList = [1]
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)

	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.leaveMaze(who)

	def leaveMaze(self, who):
		'''离开迷宫
		'''
		getActivity().leaveScene(who)


class cNpcDoor(activity.object.Npc):
	'''NPC门
	'''
	def doLook(self, who):
		actObj = getActivity()
		ti = getattr(who, "guildMazeForbid", None)
		if ti and ti > getSecond():
			self.say(who, actObj.getText(1006))
			return
		doors = actObj.getRoleInfoByKey(who.id, "doors")
		if self.id in doors:
			self.name = DOOR_NAMES[self.doorType-1]
		else:
			self.name = "未知"
		content = getActivity().getText(1005)
		selList = [1]
		content += "\nQ离开迷宫"
		selList.append(2)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)

	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.enterDoor(who)
		elif sel == 2:
			self.leaveScene(who)

	def enterDoor(self, who):
		'''进入此门
		'''
		actObj = getActivity()
		doors = actObj.getRoleInfoByKey(who.id, "doors")
		doors.add(self.id)
		actObj.changeRoleInfo(who.id, "doors", doors)
		if self.doorType == DOOR_XIU:
			ti = getSecond() + 15
			who.guildMazeForbid = ti
			self.say(who, actObj.getText(1006))
			self.transfer(who, self.sceneId, self.floor)
		elif self.doorType == DOOR_SHENG:
			self.say(who, actObj.getText(1007))
			self.transfer2NextFloor(who)
		elif self.doorType == DOOR_SHANG:
			self.say(who, actObj.getText(1008))
			self.triggerWar(who)
		elif self.doorType == DOOR_DU:
			floor = self.transfer2PreFloor(who, 3)
			self.say(who, actObj.getText(1010).replace("$floor", str(floor)))
		elif self.doorType == DOOR_JING:
			floor = self.transfer2PreFloor(who, 1)
			self.say(who, actObj.getText(1011).replace("$floor", str(floor)))
		elif self.doorType == DOOR_SI:
			floor = self.transfer2GroundFloor(who)
			self.say(who, actObj.getText(1012).replace("$floor", str(floor)))
		elif self.doorType == DOOR_JING2:
			floor = self.transfer2RandomFloor(who)
			self.say(who, actObj.getText(1013).replace("$floor", str(floor)))
		elif self.doorType == DOOR_KAI:
			floor = self.transfer2PreFloor(who, 2)
			self.say(who, actObj.getText(1014).replace("$floor", str(floor)))

	def transfer2PreFloor(self, who, cnt):
		guildId = who.getGuildId()
		guildAct = getActivity().guildAct[guildId]
		floor = max(1, self.floor - cnt)
		if self.floor >= 5 and floor < 5:
			floor = 5
		elif self.floor >= 10 and floor < 10:
			floor = 10
		nextSceneId = guildAct.sceneInfo.get(floor)
		if not nextSceneId:
			message.tips(who, "没有下一层了")
			return
		self.transfer(who, nextSceneId, floor)
		return floor

	def transfer2GroundFloor(self, who):
		guildId = who.getGuildId()
		guildAct = getActivity().guildAct[guildId]
		if self.floor < 5:
			floor = 1
		elif self.floor < 10:
			floor = 5
		elif self.floor < 15:
			floor = 10
		nextSceneId = guildAct.sceneInfo.get(floor)
		if not nextSceneId:
			message.tips(who, "没有下一层了")
			return
		self.transfer(who, nextSceneId, 1)
		return floor

	def transfer2RandomFloor(self, who):
		guildId = who.getGuildId()
		guildAct = getActivity().guildAct[guildId]
		floor = self.floor + rand(-3, 3)
		if self.floor < 5:
			floor = 5 if floor > 5 else max(1, floor)
		elif self.floor < 10:
			floor = 10 if floor > 10 else max(5, floor)
		elif self.floor < 15:
			floor = 15 if floor > 15 else max(10, floor)
		nextSceneId = guildAct.sceneInfo.get(floor)
		if not nextSceneId:
			message.tips(who, "没有下一层了")
			return
		self.transfer(who, nextSceneId, floor)
		return floor

	def transfer2NextFloor(self, who):
		guildId = who.getGuildId()
		guildAct = getActivity().guildAct[guildId]
		floor = self.floor + 1
		nextSceneId = guildAct.sceneInfo.get(floor)
		if not nextSceneId:
			message.tips(who, "没有下一层了")
			return
		self.transfer(who, nextSceneId, floor)

	def transfer(self, who, sceneId, floor):
		getActivity().transfer(who, sceneId, 61, 35)

	def leaveScene(self, who):
		'''离开迷宫
		'''
		getActivity().leaveScene(who)

	def triggerWar(self, who):
		getActivity().fight(who, self, 1001)

	def onWarEnd(self, warObj):
		activity.object.Npc.onWarEnd(self, warObj)
		isWin = False
		if warObj.winner == war.defines.TEAM_SIDE_1:
			isWin = True
		for w in warObj.teamList[war.defines.TEAM_SIDE_1].values():
			if not w.isRole():
				continue
			who = getRole(w.id)
			if isWin:
				self.transfer(who, self.sceneId, self.floor)
				continue
			self.say(who, getActivity().getText(1009))
			sceneId = getActivity().guildAct[who.getGuildId()].sceneInfo[1]
			self.transfer(who, sceneId, 1)


monsterType2Class = {
	1001: cNpcDoor,
	2001: cNpc2001,
	2002: cNpc2002,
}

def getMonsterTypeClass(monsterType):
	return monsterType2Class[monsterType]


import pst
class cGuildAct(pst.cEasyPersist):
	'''仙盟活动
	'''
	def __init__(self, guildId, gameObj, dirtyEventHandler):
		pst.cEasyPersist.__init__(self, dirtyEventHandler)
		self.guildId = guildId
		self.gameObj = gameObj
		self.timerMgr = timer.cTimerMng()
		self.sceneInfo = {} # {floor:sceneId}

	def getGuildObj(self):
		return guild.getGuild(self.guildId)

	def initNpc(self):
		self.gameObj.createActNpc(self.getGuildObj())

	def init(self):
		self.initNpc()

	def clearNpc(self):
		for npcObj in self.gameObj.getNpcListByType("actNpc{}".format(self.guildId))[:]:
			self.gameObj.removeNpc(npcObj)

	def clearForEnd(self):
		if self.timerMgr.hasTimerId("refreshTinyBox"):
			self.timerMgr.cancel("refreshTinyBox")
		self.clearNpc()
		self.sceneInfo = {}

	def refreshTinyBox(self):
		self.gameObj.createTinyBox(self)

	def refreshForBegin(self):
		self.gameObj.createActScene(self)
		self.timerMgr.run(self.refreshTinyBox, 600, 600, "refreshTinyBox")


def onEnter(who, oldScene, newScene):
	'''进入活动场景时
	'''
	actObj = getActivity()
	actInfo = actObj.createRoleInfo(who)
	actObj.changeRoleInfo(who.id, "inGame", 1)
	floor = newScene.floor
	sceneId = newScene.id
	guildId = who.getGuildId()
	actObj = activity.guildMaze.getActivity()
	doors = actObj.getRoleInfoByKey(who.id, "doors")
	boxes = actObj.getRoleInfoByKey(who.id, "boxes")
	if floor in (5, 10, 15) and floor not in boxes:
		npcObj = actObj.getBoxNpc(sceneId, guildId)
		if not npcObj:
			return
		actObj.refreshBox2Role(who, npcObj)
		return
	if floor < 15:
		actObj.refreshFloorDoor2Role(who)

def getActivity():
	return activity.getActivity("guildMaze")

# 休、生、伤、杜、景、死、惊、开
DOOR_XIU = 1
DOOR_SHENG = 2
DOOR_SHANG = 3
DOOR_DU = 4
DOOR_JING = 5
DOOR_SI = 6
DOOR_JING2 = 7
DOOR_KAI = 8

DOOR_NAMES = ["休门", "生门", "伤门", "杜门", "景门", "死门", "惊门", "开门",]


from common import *
import timer
import guild
import message
import activity
import scene
import scene_pb2
import war.defines
import entity
import template
