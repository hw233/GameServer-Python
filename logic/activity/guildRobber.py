# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
		1001:{"名称":"谢缨","造型":"1121(1,1,1,1,1,0,0)","位置":"3020,26,20,4","称谓":"正道联络人"},
		1002:{"名称":"谢琳","造型":"1221(1,1,1,1,1,0,0)","位置":"3020,19,16,4","称谓":"物资管理人"},
		1003:{"名称":"血神教弟子","造型":"4502(0,1,0,0,0,0,0)","位置":"3020,0,0,0"},
		1004:{"名称":"血神教弟子","造型":"4504(0,1,0,0,0,0,0)","位置":"3020,0,0,0"},
		1005:{"名称":"血神教弟子","造型":"4502(0,1,0,0,0,0,0)","位置":"3020,0,0,0"},
		1006:{"名称":"血神教弟子","造型":"4504(0,1,0,0,0,0,0)","位置":"3020,0,0,0"},
		1007:{"名称":"东护法白翎","造型":"4506(0,1,0,0,0,0,0)","位置":"3020,0,0,0","称谓":"血神教东护法"},
		1008:{"名称":"南护法崔晋","造型":"4502(0,1,0,0,0,0,0)","位置":"3020,0,0,0","称谓":"血神教南护法"},
		1009:{"名称":"西护法金泰","造型":"4502(0,1,0,0,0,0,0)","位置":"3020,0,0,0","称谓":"血神教西护法"},
		1010:{"名称":"北护法翘翘","造型":"4509(0,1,0,0,0,0,0)","位置":"3020,0,0,0","称谓":"血神教北护法"},
		2001:{"名称":"息壤","造型":"8002(0,1,0,0,0,0,0)","位置":"3020,0,0,0","特效":1604,"动作":5},
		2002:{"名称":"建木","造型":"8001(0,1,0,0,0,0,0)","位置":"3020,0,0,0","特效":1604,"动作":5},
		3001:{"名称":"宝箱","造型":"8004(0,1,0,0,0,0,0)","位置":"3020,0,0,0","特效":1604,"动作":5},
	}

	eventInfo = {
		1001:{"点击":"SB1002","回复":"1:$checkSF9003;2:D1003","成功":"DONE,R1001","失败":"D1003"},
		1002:{"点击":"SB1009","回复":"1:$checkSF9004;2:D1010","成功":"DONE,R1001","失败":"D1010"},
		2001:{"点击":"$pick"},
		3001:{"点击":"R1001"},
	}

	rewardInfo = {
		1001:{"经验":lambda LV:LV*85+900,"宠物经验":lambda PLV:PLV*85+900,"银币":lambda LV:LV*20+2500,"物品":[1001]},
		1002:{"经验":lambda ALV:ALV*110+1500,"宠物经验":lambda ALV:ALV*110+1500,"银币":lambda ALV:ALV*40+3500,"物品":[1002]},
		1003:{"经验":lambda LV:LV*42+450,"宠物经验":lambda PLV:PLV*42+450,"银币":lambda LV:LV*10+1200},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":80,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":80,"物品":"230102","数量":"2","绑定":0,"传闻":0},
			{"权重":80,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":60,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246001","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246002","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246003","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246004","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246005","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246006","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246007","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246008","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246009","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246010","数量":"1","绑定":0,"传闻":0},
			{"权重":300,"物品":"0","数量":"0","绑定":0,"传闻":0},
		),
		1002:(
			{"权重":1,"物品":"234101","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234102","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234103","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234104","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234105","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234106","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234107","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234108","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234109","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234110","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234111","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234112","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234113","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234114","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234115","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234116","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234117","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234118","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234119","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234120","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234121","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234122","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234123","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234124","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234125","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234126","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234127","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234128","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234129","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234130","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234131","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234132","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234133","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234134","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234135","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234136","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234137","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":1,"物品":"234138","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234139","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234140","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234141","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234142","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234143","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234144","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234145","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234146","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234147","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234148","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234149","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234150","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234151","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234152","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234153","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":2,"物品":"234901","数量":"1","绑定":0,"传闻":"SM2001"},
			{"权重":40,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":40,"物品":"230102","数量":"2","绑定":0,"传闻":0},
			{"权重":40,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":35,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246001","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246002","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246003","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246004","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246005","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246006","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246007","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246008","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246009","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"246010","数量":"1","绑定":0,"传闻":0},
			{"权重":300,"物品":"0","数量":"0","绑定":0,"传闻":0},
		),
	}

	groupInfo = {
		9001:(1003,1004,1005,1006,),
		9002:(1007,1008,1009,1010,),
		9003:(1001,1002,1003,1004,),
		9004:(1021,1022,1023,1024,),
	}

	chatInfo = {
		1001:'''血神教即将来袭，需结伴对敌，不可掉以轻心！若暂时无人结伴，可在驻地内拾取散落物资交给我小妹谢琳，也能换取少量奖励。''',
		1002:'''拦阻我血神教行事之人，死！\nQ进入战斗\nQ考虑片刻''',
		1003:'''哼，回一边躲着去吧！''',
		1004:'''不是这仙盟的人，就别多管闲事！\n（队长需是本仙盟玩家才能挑战）''',
		1005:'''想为这仙盟的人出头？也不看看自己分量！\n（队伍中本仙盟成员不足3人，无法挑战）''',
		1006:'''只凭一两个人就想来挑战我？\n（队伍人数不足3人，无法挑战）''',
		1007:'''带着这种手无缚鸡之力的家伙，也想来挑战我？\n（#C01$player#n未达到30级，不能挑战）''',
		1008:'''多谢拾回散落物资，今次仙盟若得保全，$player你当记一功。''',
		1009:'''竟敢伤我血神教徒，不可饶恕！\nQ进入战斗\nQ只是路过''',
		1010:'''哼，无用之辈，快滚！''',
		2001:'''#C01$roleName#n在抵抗#L1<14,102>*[魔教入侵]*02#n时奋勇杀敌，幸运地从#C02魔教护法#n手中夺到$lnkProps''',
		2002:'''今日击杀血神教弟子奖励已达上限，无法再获得更多奖励！''',
		2003:'''已有队伍正在挑战，请寻找其他弟子''',
		2004:'''新成立仙盟于一周内魔教入侵失利，暂不扣除仙盟资金，望各位大力聚集同道，不可再让魔教得逞！''',
		2005:'''尚未达到30级，无法拾取活动物品''',
		2006:'''你上交的建木数量已达上限，无法继续拾取''',
		2007:'''你上交的息壤数量已达上限，无法继续拾取''',
		2008:'''获得散落的仙盟物资：建木''',
		2009:'''获得散落的仙盟物资：息壤''',
		2010:'''获得$number经验''',
		2011:'''获得$number仙盟贡献''',
		2012:'''获得$number宠物经验''',
		2013:'''获得$number银币''',
		2014:'''获得$goods''',
		2015:'''血神教教众溃败而逃，遗落大量宝箱，仙盟成员可在五分钟后拾取宝箱奖励！''',
		2016:'''你已获得宝箱奖励''',
		2017:'''#C01$player#n打开宝箱，瞬间霞光万道瑞气千条，恭喜#C01$player#n获得了珍贵的#C02$item#n！''',
		2018:'''你已获得宝箱奖励，无法再次拾取''',
		2019:'''你不是此仙盟成员，无法拾取宝箱''',
	}

	branchInfo = {
	}

	fightInfo = {
		1001:(
			{"类型":1,"名称":"血神教弟子","造型":"4502(0,1,0,0,0,0,0)","能力编号":"1001","数量":"1","技能":(1112,1312,1521,),"站位":(1,)},
			{"类型":0,"名称":"新进弟子","造型":"4504(0,1,0,0,0,0,0)","能力编号":"1002","数量":"3","技能":(1311,),"站位":(2,7,9,)},
			{"类型":0,"名称":"御灵","造型":"4001(0,1,0,0,0,0,0)","能力编号":"1003","数量":"3","技能":(1511,),"站位":(3,8,10,)},
		),
		1002:(
			{"类型":1,"名称":"血神教弟子","造型":"4504(0,1,0,0,0,0,0)","能力编号":"1001","数量":"1","技能":(1112,1312,1521,),"站位":(1,)},
			{"类型":0,"名称":"精锐弟子","造型":"4502(0,1,0,0,0,0,0)","能力编号":"1002","数量":"3","技能":(1111,),"站位":(2,7,9,)},
			{"类型":0,"名称":"女贼","造型":"4506(0,1,0,0,0,0,0)","能力编号":"1003","数量":"3","技能":(1511,),"站位":(3,8,10,)},
		),
		1003:(
			{"类型":1,"名称":"血神教弟子","造型":"4502(0,1,0,0,0,0,0)","能力编号":"1001","数量":"1","技能":(1112,1312,1521,),"站位":(1,)},
			{"类型":0,"名称":"护法弟子","造型":"4504(0,1,0,0,0,0,0)","能力编号":"1002","数量":"3","技能":(1311,),"站位":(2,7,9,)},
			{"类型":0,"名称":"血气","造型":"4001(0,1,0,0,0,0,0)","能力编号":"1003","数量":"3","技能":(1511,),"站位":(3,8,10,)},
		),
		1004:(
			{"类型":1,"名称":"血神教弟子","造型":"4504(0,1,0,0,0,0,0)","能力编号":"1001","数量":"1","技能":(1112,1312,1521,),"站位":(1,)},
			{"类型":0,"名称":"守门弟子","造型":"4502(0,1,0,0,0,0,0)","能力编号":"1002","数量":"3","技能":(1111,),"站位":(2,7,9,)},
			{"类型":0,"名称":"蛊女","造型":"4508(0,1,0,0,0,0,0)","能力编号":"1003","数量":"3","技能":(1511,),"站位":(3,8,10,)},
		),
		1021:(
			{"类型":1,"名称":"$npc","造型":"$npc","能力编号":"2001","数量":"1","技能":(1133,1321,1322,1323,1512,1532,1533,),"站位":(1,)},
			{"类型":0,"名称":"护法女侍","造型":"4002(0,1,0,0,0,0,0)","能力编号":"2002","数量":"2","技能":(1111,1311,),"站位":(7,8,)},
			{"类型":0,"名称":"护法女侍","造型":"4002(0,1,0,0,0,0,0)","能力编号":"2003","数量":"1","技能":(1411,1421,1422,1423,),"站位":(6,)},
			{"类型":0,"名称":"护法童子","造型":"4001(0,1,0,0,0,0,0)","能力编号":"2004","数量":"2","技能":(1511,),"站位":(2,3,)},
			{"类型":0,"名称":"护法童子","造型":"4001(0,1,0,0,0,0,0)","能力编号":"2005","数量":"1","技能":(1221,1222,1223,1231,1232,1233,),"站位":(4,)},
			{"类型":0,"名称":"护法童子","造型":"4001(0,1,0,0,0,0,0)","能力编号":"2006","数量":"1","技能":(1621,1622,1623,1631,1632,1633,),"站位":(5,)},
		),
		1022:(
			{"类型":1,"名称":"$npc","造型":"$npc","能力编号":"2001","数量":"1","技能":(1133,1321,1322,1323,1512,1532,1533,),"站位":(1,)},
			{"类型":0,"名称":"护法门人","造型":"4504(0,1,0,0,0,0,0)","能力编号":"2002","数量":"2","技能":(1111,1311,),"站位":(7,8,)},
			{"类型":0,"名称":"护法门人","造型":"4504(0,1,0,0,0,0,0)","能力编号":"2003","数量":"1","技能":(1411,1421,1422,1423,),"站位":(6,)},
			{"类型":0,"名称":"随行女魔","造型":"4508(0,1,0,0,0,0,0)","能力编号":"2004","数量":"2","技能":(1511,),"站位":(2,3,)},
			{"类型":0,"名称":"随行女魔","造型":"4508(0,1,0,0,0,0,0)","能力编号":"2005","数量":"1","技能":(1221,1222,1223,1231,1232,1233,),"站位":(4,)},
			{"类型":0,"名称":"随行女魔","造型":"4508(0,1,0,0,0,0,0)","能力编号":"2006","数量":"1","技能":(1621,1622,1623,1631,1632,1633,),"站位":(5,)},
		),
		1023:(
			{"类型":1,"名称":"$npc","造型":"$npc","能力编号":"2001","数量":"1","技能":(1133,1321,1322,1323,1512,1532,1533,),"站位":(1,)},
			{"类型":0,"名称":"护法宠物","造型":"3007(0,1,0,0,0,0,0)","能力编号":"2002","数量":"2","技能":(1111,1311,),"站位":(7,8,)},
			{"类型":0,"名称":"护法宠物","造型":"3007(0,1,0,0,0,0,0)","能力编号":"2003","数量":"1","技能":(1411,1421,1422,1423,),"站位":(6,)},
			{"类型":0,"名称":"宠物护卫","造型":"4504(0,1,0,0,0,0,0)","能力编号":"2004","数量":"2","技能":(1511,),"站位":(2,3,)},
			{"类型":0,"名称":"宠物护卫","造型":"4504(0,1,0,0,0,0,0)","能力编号":"2005","数量":"1","技能":(1221,1222,1223,1231,1232,1233,),"站位":(4,)},
			{"类型":0,"名称":"宠物护卫","造型":"4504(0,1,0,0,0,0,0)","能力编号":"2006","数量":"1","技能":(1621,1622,1623,1631,1632,1633,),"站位":(5,)},
		),
		1024:(
			{"类型":1,"名称":"$npc","造型":"$npc","能力编号":"2001","数量":"1","技能":(1133,1321,1322,1323,1512,1532,1533,),"站位":(1,)},
			{"类型":0,"名称":"护法草灵","造型":"3006(0,1,0,0,0,0,0)","能力编号":"2002","数量":"2","技能":(1111,1311,),"站位":(7,8,)},
			{"类型":0,"名称":"护法草灵","造型":"3006(0,1,0,0,0,0,0)","能力编号":"2003","数量":"1","技能":(1411,1421,1422,1423,),"站位":(6,)},
			{"类型":0,"名称":"随身侍女","造型":"4506(0,1,0,0,0,0,0)","能力编号":"2004","数量":"2","技能":(1511,),"站位":(2,3,)},
			{"类型":0,"名称":"随身侍女","造型":"4506(0,1,0,0,0,0,0)","能力编号":"2005","数量":"1","技能":(1221,1222,1223,1231,1232,1233,),"站位":(4,)},
			{"类型":0,"名称":"随身侍女","造型":"4506(0,1,0,0,0,0,0)","能力编号":"2006","数量":"1","技能":(1621,1622,1623,1631,1632,1633,),"站位":(5,)},
		),
	}

	ableInfo = {
		1001:{"等级":"ALV+1","生命":"B*1.13","真气":"B*1","物理伤害":"B*0.97","法术伤害":"B*0.97","物理防御":"B*0.72","法术防御":"B*0.72","速度":"B*0.96","治疗强度":"B*0.67","封印命中":"B*0","抵抗封印":"B*0.96","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1002:{"等级":"ALV","生命":"B*0.9","真气":"B*1","物理伤害":"B*0.81","法术伤害":"B*0.56","物理防御":"B*0.7","法术防御":"B*0.49","速度":"B*0.8","治疗强度":"B*0.56","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1003:{"等级":"ALV","生命":"B*0.9","真气":"B*1","物理伤害":"B*0.56","法术伤害":"B*0.81","物理防御":"B*0.49","法术防御":"B*0.7","速度":"B*0.8","治疗强度":"B*0.56","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2001:{"等级":"ALV+1","生命":"B*1.5","真气":"B*1","物理伤害":"B*1.1","法术伤害":"B*1.1","物理防御":"B*0.82","法术防御":"B*0.82","速度":"B*1.09","治疗强度":"B*0.76","封印命中":"B*0","抵抗封印":"B*1.09","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2002:{"等级":"ALV","生命":"B*0.9","真气":"B*1","物理伤害":"B*0.81","法术伤害":"B*0.56","物理防御":"B*0.7","法术防御":"B*0.49","速度":"B*0.8","治疗强度":"B*0.56","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2003:{"等级":"ALV","生命":"B*0.9","真气":"B*1","物理伤害":"B*0.81","法术伤害":"B*0.81","物理防御":"B*0.6","法术防御":"B*0.6","速度":"B*0.85","治疗强度":"B*0.56","封印命中":"B*0.8","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2004:{"等级":"ALV","生命":"B*0.9","真气":"B*1","物理伤害":"B*0.56","法术伤害":"B*0.81","物理防御":"B*0.49","法术防御":"B*0.7","速度":"B*0.8","治疗强度":"B*0.56","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2005:{"等级":"ALV","生命":"B*0.9","真气":"B*1","物理伤害":"B*0.81","法术伤害":"B*0.81","物理防御":"B*0.6","法术防御":"B*0.6","速度":"B*0.8","治疗强度":"B*0.56","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2006:{"等级":"ALV","生命":"B*0.9","真气":"B*1","物理伤害":"B*0.56","法术伤害":"B*0.56","物理防御":"B*0.6","法术防御":"B*0.6","速度":"B*0.8","治疗强度":"B*0.8","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}

	lineupInfo = {
	}

	sceneInfo = {
	}

	configInfo = {
		1001:(100,10000),
		1002:(150,15000),
		1003:20,
		1004:5,
		1005:30,
		1006:10,
		1007:3,
		1008:5,
		1009:30,
		1010:10,
		1011:50,
		1012:10,
		1013:1,
		1014:3,
		1015:3,
		1016:2,
		1017:5,
		1018:20,
		1019:20,
	}

	batchInfo = {
		1:{"每批数量":5,"同时存在":10},
		2:{"每批数量":6,"同时存在":12},
		3:{"每批数量":7,"同时存在":14},
		4:{"每批数量":8,"同时存在":16},
		5:{"每批数量":9,"同时存在":18},
	}
#导表结束

	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.state = 0 # 活动状态, 0.已结束  1.进行中
		self.guildAct = {} # 仙盟活动对象

	def inNormalTime(self):
		'''是否活动正式时间
		'''
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		if wday not in (2, 4):
			return False
		if hour not in (12, 13,):
			return False
		return True

	def init(self):
		if self.inNormalTime():
			self.begin()

	def begin(self):
		'''开始活动
		'''
		self.state = 1
		self.timerMgr.run(self.actNotify, 0, 1800, "actNotify")
		if not self.guildAct:
			self.initGuildAct()
		self.refreshForBegin()

	def end(self):
		'''结束活动
		'''
		self.timerMgr.cancelAll()
		self.state = 0
		message.sysMessageRoll("魔教入侵结束，血神教弟子已经退去，各位可继续潜心修行，行侠仗义。")
		self.clearForEnd()

	def beginNotify(self, nextTime):
		'''开启通知
		'''
		if nextTime == 1200:
			self.timerMgr.run(functor(self.beginNotify, 540), nextTime, 0, "beginNotify")
			minute = 30
		elif nextTime == 540:
			self.timerMgr.run(functor(self.beginNotify, None), nextTime, 0, "beginNotify")
			minute = 10
		else:
			minute = 1
		txt = "密探来报，$time分钟后将有大批血神教弟子袭击仙盟，请尽速返回仙盟！".replace("$time", str(minute))
		message.sysMessageRoll(txt)

	def endNotify(self, nextTime):
		'''结束通知
		'''
		if nextTime == 300:
			minute = getDatePart(partName="minute")
			nextTime = 300
			if minute == 50:
				nextTime = 120
			self.timerMgr.run(functor(self.endNotify, nextTime), 300, 0, "endNotify")
			minute = 60 - minute
		elif nextTime == 120:
			minute = getDatePart(partName="minute")
			nextTime = 120
			if minute == 57:
				nextTime = None
			self.timerMgr.run(functor(self.endNotify, nextTime), 120, 0, "endNotify")
			minute = 60 - minute
		else:
			minute = 1
		txt = "剩余#C02$time#n分钟，尚有#C02$number#n个血神教弟子在仙盟中作乱，尽快击败他们！".replace("$time", str(minute))
		for actObj in self.guildAct.itervalues():
			actObj.endNotify(txt)

	def actNotify(self):
		'''活动通知
		'''
		txt = "血神教弟子已入侵仙盟，速度击败他们！"
		message.sysMessageRoll(txt)

	def onNewHour(self, day, hour, wday):
		'''强盗活动时间点：11点活动开始前的一些公告
		12~14点刷怪时间
		14点~15点间活动结束后的处理
		'''
		if wday not in (2, 4):
			return
		if self.inNormalTime():
			if self.state == 0:
				self.begin()
		else:
			if self.state != 0:
				self.end()
		if hour == 11:
			self.timerMgr.run(functor(self.beginNotify, 1200), 1800, 0, "beginNotify")
			self.timerMgr.run(self.initGuildAct, 2700, 0, "initGuildAct")
		elif hour == 13:
			self.timerMgr.run(functor(self.endNotify, 300), 2700, 0, "endNotify")
		elif hour == 15:
			self.guildAct = {} # 释放活动对象

	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 101:
			if self.state != 1:
				if self.timerMgr.hasTimerId("initGuildAct"):
					self.timerMgr.cancel("initGuildAct")
				self.begin()
			else:
				message.tips(who, "活动已经开启")
		elif cmdIdx == 102:
			if self.state != 0:
				self.end()
				for actObj in self.guildAct.itervalues():
					actObj.timerMgr.cancelAll()
					actObj.clearNpc()
				self.guildAct = {}
			else:
				message.tips(who, "活动已经结束")
		elif cmdIdx == 103:
			guildAct = self.guildAct.get(who.getGuildId())
			if not guildAct:
				return
			message.message(who, "当今波数为：{}".format(guildAct.fetch("wave")))
			# message.message(who, "当今波数为：{},设置为{}".format(guildAct.fetch("wave"), args[0]))
			# guildAct.set("wave", args[0])
		elif cmdIdx == 104:
			guildAct = self.guildAct.get(who.getGuildId())
			if not guildAct:
				return
			guildAct.createSeniorMonster()

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		currentMonsterType = getattr(self, "currentMonsterType", None)
		if currentMonsterType:
			cls = getMonsterTypeClass(self.currentMonsterType)
			return cls(self)
		return customActivity.newNpc(self, npcIdx, name, shape, who)

	def createMonster(self, guildId, monsterType, monsterCnt):
		'''创建妖怪
		'''
		self.currentMonsterType = monsterType
		if monsterType == 1:
			npcIdx = 9001 # 弟子分组
			eventIdx = 1001
		else:
			npcIdx = 9002
			eventIdx = 1002
		typeFlag = "guild%d" % guildId
		for i in xrange(monsterCnt):
			npcObj = self.addNpc(self.transIdxByGroup(npcIdx), typeFlag)
			npcObj.monsterType = monsterType
			npcObj.eventIdx = eventIdx
			npcObj.guildId = guildId
			self.guildAct[guildId].onAddMonster(npcObj)
		self.currentMonsterType = None

	def getMonsterList(self, guildId, monsterType):
		'''已存在的妖怪
		'''
		monsterList = []
		typeFlag = "guild%d" % guildId
		for npcObj in self.getNpcListByType(typeFlag):
			if npcObj.monsterType != monsterType:
				continue
			monsterList.append(npcObj)
		return monsterList

	def getMaterialList(self, guildId, materialType):
		'''已存在的物资
		'''
		materialList = []
		typeFlag = "material{}{}".format(materialType, guildId)
		for npcObj in self.getNpcListByType(typeFlag):
			if npcObj.materialType != materialType:
				continue
			materialList.append(npcObj)
		return materialList

	def addNpc(self, npcIdx, typeFlag="npc", who=None):
		npcObj = template.Template.addNpc(self, npcIdx, typeFlag, who)
		if not typeFlag.startswith("material"):
			scene.switchSceneForNpc(npcObj, npcObj.sceneId, npcObj.x, npcObj.y, npcObj.d)
		return npcObj

	def createNpc(self, npcIdx, who=None):#override
		'''创建Npc
		'''
		npcObj = customActivity.createNpc(self, npcIdx, who)
		#npc场景ID设置为虚拟场景ID
		npcObj.sceneId = self.currentSceneId
		return npcObj

	def onRemoveNpc(self, npcObj):
		guildId = getattr(npcObj, "guildId", None)
		if guildId:
			self.guildAct[guildId].onRemoveMonster(npcObj)
		typeFlag = getattr(npcObj, "typeFlag", None)
		if typeFlag and typeFlag.startswith("material"):
			self.refreshMaterial2Member(npcObj, False)
			guildObj = guild.getGuild(guildId)
			if guildObj:
				guildObj.scene.removeEntity(npcObj)
		else:
			npcObj.tryRemove()

	def createWaveMonster(self, guildObj, monsterCnt):
		'''刷新活动所有仙盟的第一波怪
		'''
		self.currentSceneId = guildObj.sceneId
		self.createMonster(guildObj.id, 1, monsterCnt)

	def createSeniorMonster(self, guildObj):
		'''刷新护法怪
		'''
		self.currentSceneId = guildObj.sceneId
		self.createMonster(guildObj.id, 2, 1)

	def createMaterial(self, guildObj, count, mtype):
		'''刷物质
		'''
		self.currentSceneId = guildObj.sceneId
		guildId = guildObj.id
		typeFlag = "material{}{}".format(mtype, guildId)
		for i in xrange(count):
			npcIdx = 2000 + mtype
			npcObj = self.addNpc(npcIdx, typeFlag)
			if not npcObj:
				continue
			npcObj.guildId = guildId
			npcObj.eventIdx = 2001
			npcObj.materialType = mtype
			guildObj.scene.addEntity(npcObj, npcObj.x, npcObj.y, npcObj.d)
			self.refreshMaterial2Member(npcObj)

	def getActivityNpc(self, who, npcIdx):
		'''活动入口NPC
		'''
		guildId = who.getGuildId()
		if not guildId:
			return None
		guildAct = self.guildAct.get(guildId)
		if not guildAct:
			return None
		typeFlag = "actNpc1{}".format(guildId)
		npcList = self.getNpcListByType(typeFlag)
		for npcObj in npcList:
			if npcObj.guildId == guildId and npcObj.idx == npcIdx:
				return npcObj
		return None

	def createActNpc(self, guildObj):
		'''创建活动功能NPC
		'''
		self.currentSceneId = guildObj.sceneId
		guildId = guildObj.id
		for i in xrange(1, 3):
			npcIdx = 1000 + i
			self.currentMonsterType = npcIdx
			npcObj = self.addNpc(npcIdx, "actNpc{}{}".format(i, guildId))
			npcObj.guildId = guildId
		self.currentMonsterType = None

	def initGuildAct(self):
		'''初始化各仙盟活动对象
		'''
		self.guildAct = {}
		for guildObj in guild.gGuildKeeper.getIterValues():
			actObj = cGuildAct(guildObj.id, self, self.__dirtyEventHandler)
			self.guildAct[guildObj.id] = actObj
			actObj.init()
			guildObj.scene.eventOnEnter += onEnter

	def refreshMaterial2Member(self, npcObj, isEnter=True):
		'''刷新物质到仙盟成员
		'''
		guildId = npcObj.guildId
		sceneId = npcObj.sceneId
		sceneObj = scene.getScene(sceneId)
		if not sceneObj:
			return
		for roleId in sceneObj.getRoleList():
			who = getRole(roleId)
			if not who or who.getGuildId() != guildId:
				continue
			if isEnter:
				who.endPoint.send(npcObj.getSerialized1())
			else:
				who.endPoint.rpcEttLeave(npcObj.id)

	def refreshForBegin(self):
		'''开始刷怪
		'''
		for actObj in self.guildAct.itervalues():
			actObj.refreshForBegin()

	def clearForEnd(self):
		for actObj in self.guildAct.itervalues():
			guildObj = guild.getGuild(actObj.guildId)
			if not guildObj:
				continue
			guildObj.scene.eventOnEnter -= onEnter
			actObj.clearForEnd()

	def handleCheck(self, pid, npcId, eventName):
		who = getRole(pid)
		if not who:
			return
		npcObj = getNpc(npcId)
		if not npcObj:
			return
		if not self.handleTeamConfirm(who, npcObj):
			return
		self.doScript(who, npcObj, eventName)

	def handleTeamConfirm(self, who, npcObj):
		teamObj = who.getTeamObj()
		if not teamObj or teamObj.inTeamSize < 3:
			npcObj.say(who, self.getText(1006))
			return False
		elif not teamObj.isLeader(who.id):
			return False
		elif who.getGuildId() != npcObj.guildId:
			npcObj.say(who, self.getText(1004))
			return False
		lLevelCheck = []
		# lGuildCheck = [] # 取消必须3个本仙盟成员限制
		for pid in teamObj.getInTeamList():
			obj = getRole(pid)
			if not obj:
				return False
			if obj.level < 30:
				lLevelCheck.append(obj.name)
			# if obj.getGuildId() == npcObj.guildId:
			# 	lGuildCheck.append(obj)
		if lLevelCheck:
			msg = "、".join(lLevelCheck)
			txt = self.getText(1007).replace("$player", msg)
			npcObj.say(who, txt)
			return False
		# if len(lGuildCheck) < 3:
		# 	npcObj.say(who, self.getText(1005))
		# 	return False
		return True

	def onStartWar(self, w):
		if getattr(w.war.gameNpc, "onStartWar", None):
			w.war.gameNpc.onStartWar(w)

	def onWarWin(self, warObj, npcObj, w):
		customActivity.onWarWin(self, warObj, npcObj, w)
		if hasattr(npcObj, "onWarWin"):
			npcObj.onWarWin(warObj, w)

	def warWin(self, warObj, npcObj, warriorList):
		'''战斗胜利
		'''
		for w in warriorList:
			if not w.isRole():
				continue
			who = getRole(w.id)
			if not who:
				continue
			if not self.inGame(who):
				continue
			self.onWarWin(warObj, npcObj, w)
			if hasattr(npcObj, "monsterType") and npcObj.monsterType == ROBBER_TYPE_NORMAL:
				who.day.add("guildRobber", 1)

	def boxReward(self, who, rwdIdx, npcObj):
		if who.getGuildId() != npcObj.guildId:
			message.tips(who, "你不是此仙盟成员，无法拾取宝箱")
			return
		if who.day.fetch("grbox") > 0:
			message.tips(who, "你已获得宝箱奖励，无法再次拾取")
			return
		customActivity.reward(self, who, rwdIdx, npcObj)
		who.day.add("grbox", 1)
		message.tips(who, "你已获得宝箱奖励")
		self.removeNpc(npcObj)

	def reward(self, who, rwdIdx, npcObj=None):
		if npcObj.typeFlag.startswith("box"):
			return self.boxReward(who, rwdIdx, npcObj)
		checkReward = getattr(npcObj, "checkReward", None)
		if checkReward and not npcObj.checkReward(who, self):
			return
		customActivity.reward(self, who, rwdIdx, npcObj)

	def rewardExtra(self, who, npcObj):
		'''额外奖励
		'''
		# 只获得额外贡献或侠义值，这个3应该读全局配置的信息TODO
		# 获得奖励=击杀奖励*（100-int(当天已击杀的怪物数量/10)*10）%
		robberCnt = who.day.fetch("guildRobber")
		extra = int(3 * (100 - int(robberCnt/10) * 10) * 0.01)
		if npcObj.guildId == who.getGuildId():
			who.addGuildPoint(extra, "击杀仙盟强盗")
		else:
			who.addHelpPoint(extra, "帮助击杀仙盟强盗")

	def customEvent(self, who, npcObj, eventName, *args):
		if eventName == "pick": # 拾取
			self.doPick(who, npcObj)
			return
		m = re.match("check(\S+)", eventName)
		if m:
			subEvent = m.group(1)
			myGreenlet.cGreenlet.spawn(self.handleCheck, who.id, npcObj.id, subEvent)

	def canPickup(self, who, npcObj):
		if getattr(npcObj, "picking", None):
			message.tips(who, "该物资正在被其他人拾取")
			return False
		if who.level < 30:
			message.tips(who, self.getText(2005))
			return False
		elif who.getGuildId() != npcObj.guildId:
			message.tips(who, "非本仙盟成员无法拾取")
			return False
		if npcObj.idx == 2001:
			propsNo = 203002
			propsName = "息壤"
		else:
			propsNo = 203003
			propsName = "建木"
		handinCnt = who.day.fetch("guildM{}".format(propsNo))
		packageCnt = who.propsCtn.getPropsAmountByNos(propsNo)[0]
		if handinCnt + packageCnt + 1 >= 30:
			message.tips(who, "你上交的{}数量已达上限，无法继续拾取".format(propsName))
			return False
		return True

	def doPick(self, who, npcObj):
		'''拾取
		'''
		if not self.canPickup(who, npcObj):
			return

		npcId = npcObj.id
		npcObj.picking = True
		message.progressBar(who, functor(self.responsePick, npcId), "拾取中", 0, 30, True)
		
	def responsePick(self, who, isDone, npcId):
		npcObj = self.getNpcById(npcId)
		if not npcObj:
			return
		if not isDone:
			npcObj.picking = False
			return
	
		propsNo = 203002 if npcObj.idx == 2001 else 203003
		teamObj = who.getTeamObj()
		if teamObj:
			roleList = teamObj.getInTeamList()
		else:
			roleList = [who.id]
		for pid in roleList:
			who = getRole(pid)
			if who.level < 30:
				message.tips(who, "低于30级玩家无法获得该物品")
				continue
			elif who.getGuildId() != npcObj.guildId:
				continue
			launch.launchBySpecify(who, propsNo, 1, True)
			message.tips(who, "获得散落的仙盟物资：{}".format(npcObj.name))
		self.removeNpc(npcObj)

	def validFight(self, who, npcObj, fightIdx):
		if hasattr(npcObj, "validFight"):
			return npcObj.validFight(who, fightIdx)
		return customActivity.validFight(self, who, npcObj, fightIdx)

	def getBatchMonsterCount(self, guildLv):
		'''每批怪物刷新数量
		'''
		return self.batchInfo.get(guildLv, {}).get("每批数量", 0)

	def getBatchMonsterMax(self, guildLv):
		'''怪物同时存在最大数量
		'''
		return self.batchInfo.get(guildLv, {}).get("同时存在", 0)


def onEnter(who, oldScene, newScene):
	npcs = newScene.dEttByType.get(entity.ETT_TYPE_NPC)
	for npcId in npcs:
		oEtt = newScene.getEntityById(npcId)
		if not oEtt or getattr(oEtt, "guildId", None) != who.getGuildId():
			continue
		if not getattr(oEtt, "typeFlag", None):
			continue
		if not oEtt.typeFlag.startswith("material"):
			continue
		who.endPoint.send(oEtt.getSerialized1())


import activity.object

class cNpc1001(activity.object.Npc):
	'''活动npc1001
	'''
	def doLook(self, who):
		content = getActivity().getText(1001)
		selList = []
		content += "\nQ便捷组队"
		selList.append(1)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.speedyTeam(who)

	def speedyTeam(self, who):
		'''打开便捷组队界面
		'''
		if who.level < 30:
			message.tips(who, "未达到30级，无法参与活动")
			return
		team.platformservice.quickMakeTeam(who, 7)
		message.tips(who, "你已加入魔教入侵活动的自动匹配")

class cNpc1002(activity.object.Npc):
	'''活动npc1002
	'''
	def doLook(self, who):
		content = "若暂时无人结伴，可在驻地内拾取散落物资交给我，也能换取少量奖励。\nQ上交物资"
		selList = [1]
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)

	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.handInMaterials(who)

	def handInMaterials(self, who):
		'''上交物资
		'''
		if who.getGuildId() != self.guildId:
			return
		propsNoListNeeded = [203002, 203003]
		propsObjList = list(who.propsCtn.getPropsGroupByNo(*propsNoListNeeded))
		if not propsObjList:
			message.tips(who, "你没有物资可上交")
			return
		propsIdList = [propsObj.id for propsObj in propsObjList]
		tt1, tt2 = 0, 0
		for propsId in propsIdList:
			propsObj = who.propsCtn.getItem(propsId)
			if not propsObj:
				continue
			idx = propsObj.idx
			if idx not in propsNoListNeeded:
				continue
			amount = propsObj.stack()
			if who.day.fetch("guildM{}".format(propsObj.idx)) >= 30:
				message.tips(who, "你上交的{}数量已达上限".format(propsObj.name))
				who.propsCtn.addStack(propsObj, -amount)
				continue
			who.propsCtn.addStack(propsObj, -amount)
			who.day.add("guildM{}".format(idx), amount)
			if idx == propsNoListNeeded[0]:
				tt1 += amount
			else:
				tt2 += amount
		tt = min(30, tt1) + min(30, tt2)
		if not tt:
			return
		self.handInReward(who, tt)

	def handInReward(self, who, ttCnt):
		txt = self.game.getText(1008).replace("$player", who.name)
		self.say(who, txt)
		gp = self.game.configInfo[1016] * ttCnt
		who.addGuildPoint(gp, "上交物资")
		info = self.game.getRewardInfo(1003)
		for _type in info.iterkeys():
			if _type in ("传闻",):
				continue
			val = info[_type]
			if not val:
				continue
			val = self.game.transCodeForReward(val, _type, who)
			self.game.rewardByType(who, val * ttCnt, _type)


GRIDPOSFUN = {
	0: lambda x, y: (x+1, y),
	1: lambda x, y: (x+1, y-1),
	2: lambda x, y: (x, y-1),
	3: lambda x, y: (x-1, y-1),
	4: lambda x, y: (x-1, y),
	5: lambda x, y: (x-1, y+1),
	6: lambda x, y: (x, y+1),
	7: lambda x, y: (x+1, y+1),
}

class cNormalMonster(activity.object.Npc):
	'''普通怪
	'''
	def __init__(self, gameObj):
		activity.object.Npc.__init__(self, gameObj)
		self.timerMgr = timer.cTimerMng()
		self.timerMgr.run(self.randomMove, rand(10), 10, "randomMove")

	def remove(self):
		self.timerMgr.cancelAll()
		activity.object.Npc.remove(self)

	def randomMove(self):
		sceneId, x, y = self.sceneId, self.x, self.y
		if not scene.getScene(sceneId):
			self.timerMgr.cancelAll()
			return
		idxList = shuffleList([0, 1, 2, 3, 4, 5, 6, 7])
		for i in idxList:
			x, y = GRIDPOSFUN[i](x, y)
			if scene.validPos(sceneId, x, y):
				self.x, self.y = x, y
				scene.m2ssEntityMove(self)
				break
			x, y = self.x, self.y

	def validFight(self, who, fightIdx):
		if self.inWar():
			message.tips(who, "已有队伍正在挑战")
			return 0
		return 1

	def isWarEndDel(self, warObj):
		'''战斗结束，玩家胜利才删除
		'''
		if warObj.winner == TEAM_SIDE_1:
			return True
		return False 

	def onStartWar(self, w):
		who = getRole(w.id)
		if who and who.day.fetch("guildRobber") > 30:
			message.tips(who, "今日击杀血神教弟子奖励已达上限，无法再获得更多奖励！")

	def onWarEnd(self, warObj):
		activity.object.Npc.onWarEnd(self, warObj)
		if not self.isWarEndDel(warObj):
			return
		names = []
		for w in warObj.teamList[TEAM_SIDE_1].values():
			if not w.isRole():
				continue
			names.append(w.name)
		cnt = len(getActivity().getMonsterList(self.guildId, 1)) - 1
		if cnt > 0:
			txt = "#C01{}#n顺利击败一伙血神教弟子，还剩#C02{}#n伙魔人正在作恶！".format("、".join(names), cnt)
			message.guildMessage(self.guildId, txt)
		self.game.removeNpc(self)

	def checkReward(self, who, game):
		robberCnt = who.day.fetch("guildRobber")
		if robberCnt > 30:
			return False
		elif robberCnt > 10:
			game.rewardExtra(who, self)
			return False
		game.rewardExtra(who, self)
		return True


class cSeniorMonster(activity.object.Npc):
	'''高级怪
	'''
	def validFight(self, who, fightIdx):
		if self.inWar():
			message.tips(who, "已有队伍正在挑战")
			return 0
		return 1

	def isWarEndDel(self, warObj):
		'''战斗结束，玩家胜利才删除
		'''
		if warObj.winner == TEAM_SIDE_1:
			return True
		return False 

	def onWarEnd(self, warObj):
		activity.object.Npc.onWarEnd(self, warObj)
		if not self.isWarEndDel(warObj):
			return
		guildObj = guild.getGuild(self.guildId)
		txt = "恭喜#C02$union#n上下一心，成功击杀前来寻仇的血神教护法，匡扶正道，为人间又除一大患！".replace("$union", guildObj.name)
		message.sysMessageRoll(txt)
		self.game.removeNpc(self)

	def checkReward(self, who, game):
		game.rewardExtra(who, self)
		return True

#===============================================================================
# 妖怪相关
#===============================================================================
ROBBER_TYPE_NORMAL = 1 # 普通妖
ROBBER_TYPE_SENIOR = 2 # 护法妖

monsterType2Class = {
	ROBBER_TYPE_NORMAL: cNormalMonster,
	ROBBER_TYPE_SENIOR: cSeniorMonster,
	1001: cNpc1001,
	1002: cNpc1002,
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
		self.state = 0 # 活动状态, 0.已结束  1.进行中
		self.currentMonsterList = [] # 怪物列表

	def getGuildObj(self):
		return guild.getGuild(self.guildId)

	def init(self):
		self.initNpc()

	def refreshForBegin(self):
		guildObj = self.getGuildObj()
		if not guildObj:
			return
		self.state = 1
		self.refreshMonster()

	def initNpc(self):
		'''初始化功能NPC
		'''
		self.gameObj.createActNpc(self.getGuildObj())

	def clearNpc(self):
		for i in xrange(1, 3):
			for npcObj in self.gameObj.getNpcListByType("actNpc{}{}".format(i, self.guildId))[:]:
				self.gameObj.removeNpc(npcObj)

	def clearMonster(self):
		for i in xrange(1, 3):
			for npcObj in self.gameObj.getMonsterList(self.guildId, i)[:]:
				self.gameObj.removeNpc(npcObj)

	def clearMaterial(self):
		for i in xrange(1, 3):
			for npcObj in self.gameObj.getNpcListByType("material{}{}".format(i, self.guildId))[:]:
				self.gameObj.removeNpc(npcObj)

	def clearBox(self):
		for npcObj in self.gameObj.getNpcListByType("box{}".format(self.guildId))[:]:
			self.gameObj.removeNpc(npcObj)

	def createWaveMonster(self, monsterCnt):
		self.gameObj.createWaveMonster(self.getGuildObj(), monsterCnt)
		if self.fetch("wave") == 20:
			txt = "血神教弟子已全数到来，大家严阵以待！"
		else:
			txt = "新一批血神教弟子来袭！大家万万不可松懈！"
		message.guildMessage(self.guildId, txt)

	def createSeniorMonster(self):
		self.gameObj.createSeniorMonster(self.getGuildObj())
		txt = "来犯的血神教弟子均被清除，得知消息的血神教护法前来报复，大家小心应付！"
		message.guildMessage(self.guildId, txt)
		self.set("senior", 2)

	def refreshMonster(self):
		'''刷新妖怪
		'''
		guildObj = self.getGuildObj()
		if not guildObj:
			return
		self.add("wave", 1)
		lv = guildObj.level
		monsterCnt = self.gameObj.getBatchMonsterCount(lv)
		monsterCntMax = self.gameObj.getBatchMonsterMax(lv)
		monsterList = self.gameObj.getMonsterList(self.guildId, 1)
		monsterCntHas = len(monsterList)
		monsterCnt = min(monsterCnt, monsterCntMax-monsterCntHas)
		if monsterCnt > 0:
			self.createWaveMonster(monsterCnt)
		self.refreshMaterial()
		if self.fetch("senior") == 1:
			self.createSeniorMonster()
		if self.fetch("wave") >= 20:
			return
		self.timerMgr.run(self.refreshMonster, 300, 0, "refreshMonster")

	def refreshMaterial(self):
		'''刷物资
		'''
		materialCnt = self.getGuildObj().getAllOnlineCount()
		for i in xrange(1, 3):
			materialCntMax = 20
			materialList = self.gameObj.getMaterialList(self.guildId, i)
			materialCntHas = len(materialList)
			count = min(materialCnt, materialCntMax-materialCntHas)
			if count > 0:
				self.gameObj.createMaterial(self.getGuildObj(), count, i)

	def refreshBox(self):
		'''刷宝箱
		'''
		count = self.getGuildObj().getAllOnlineCount() / 2 # 活跃人数*0.5
		sceneId = self.getGuildObj().sceneId
		actObj = getActivity()
		actObj.currentSceneId = sceneId
		for i in xrange(count):
			npcObj = actObj.addNpc(3001, "box{}".format(self.guildId))
			npcObj.eventIdx = 3001
			npcObj.guildId = self.guildId
		# self.log("%d refreshBox %d" % (guildId, count))
		if count > 0:
			message.guildMessage(self.guildId, "成批宝箱已出现在仙盟驻地，大家赶快拾取宝物！")
			self.timerMgr.run(self.clearBox, 1500, 0, "clearBox")

	def clearForEnd(self):
		if self.state == 0:
			return
		self.state = 0
		if self.timerMgr.hasTimerId("refreshMonster"):
			self.timerMgr.cancel("refreshMonster")
		name = self.getGuildObj().name
		normalCnt = len(self.gameObj.getMonsterList(self.guildId, 1))
		seniorCnt = len(self.gameObj.getMonsterList(self.guildId, 2))
		self.clearMonster()
		self.timerMgr.run(self.clearNpc, 900, 0, "clearNpc")
		self.clearMaterial()
		if normalCnt or seniorCnt:
			self.failPunish(normalCnt, seniorCnt)
		else:
			self.winBonus()

	def failPunish(self, normalCnt, seniorCnt):
		guildObj = self.getGuildObj()
		if getSecond() - guildObj.fetch("birth") < 3600 * 24 * 7:
			message.guildMessage(self.guildId, getActivity().getText(2004))
			return
		lv = guildObj.level
		nf = self.gameObj.configInfo[1001] # 普通怪计算参数
		sf = self.gameObj.configInfo[1002] # 高级怪计算参数
		fund = (lv * nf[0] + nf[1]) * normalCnt + (lv * sf[0] + sf[1]) * seniorCnt
		txt = "由于防卫太过薄弱，仙盟被血神教掠走#C02{}#n资金，望各位下次努力，不可再让魔道得逞！".format(fund)
		self.getGuildObj().addFund(-fund)
		self.getGuildObj().addLog(txt)
		message.guildMessage(self.guildId, txt)

	def winBonus(self):
		txt = "血神教教众溃败而逃，遗落大量宝箱，仙盟成员可在五分钟后拾取宝箱奖励！"
		message.guildMessage(self.guildId, txt)
		self.timerMgr.run(self.refreshBox, 300, 0, "refreshBox")

	def onAddMonster(self, npcObj):
		if not getattr(self, "currentMonsterList", None):
			self.currentMonsterList = []
		monsterType = getattr(npcObj, "monsterType", None)
		if monsterType == ROBBER_TYPE_NORMAL:
			self.currentMonsterList.append(npcObj.id)

	def onRemoveMonster(self, npcObj):
		if npcObj.id in self.currentMonsterList:
			self.currentMonsterList.remove(npcObj.id)
			kmc = self.add("killMonsterCnt", 1)
			if not self.fetch("senior") and kmc > 50 and rand(100) < 10+(kmc-50)*3:
				self.set("senior", 1)
			if len(self.currentMonsterList) == 0 and self.gameObj.state == 1:
				if self.fetch("wave") == 20:
					message.guildMessage(self.guildId, "来袭的血神教弟子全数败退，仙盟已转危为安！")
					self.clearForEnd()
				else:
					self.refreshMonster()

	def endNotify(self, txt):
		'''结束通知
		'''
		count = len(self.currentMonsterList)
		if not count:
			return
		txt = txt.replace("$number", str(count))
		message.guildMessage(self.guildId, txt)


def getActivity():
	return activity.getActivity("guildRobber")


import re
import timer
import activity
import team.platformservice
import message
import guild
from common import *
from war.defines import *
import myGreenlet
import launch
import scene
import template
import entity
