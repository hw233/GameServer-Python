# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
	}

	eventInfo = {
	}

	rewardInfo = {
	}

	rewardPropsInfo = {
	}

	groupInfo = {
	}

	chatInfo = {
		2001:'''开启此获取途径需要先加入仙盟''',
		2002:'''开启此获取途径需要#c02等级≥$level#n''',
	}

	branchInfo = {
	}

	fightInfo = {
	}

	ableInfo = {
	}

	lineupInfo = {
	}

	sceneInfo = {
	}

	configInfo = {
	}

	activityData = {
		1:{"活动ID":1,"权重":90,"是否推荐":0,"任务类型":1,"任务名字":"降魔任务","是否可见":1,"活动等级":20,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":80,"每次活跃值":1,"总活跃":20,"完成类型":1,"完成条件":80,"任务图标":202008,"未开时描述":"$NONE$","时间描述":"全天","活动形式":2,"奖励物品编号":(202047,202048),"参加事件":"NPC","npc":10401,"任务编号":30101,"活动描述":"正邪运转，各地妖邪崛起，正是需要各路英雄结队除魔。每天除魔能获大量经验，并且有几率获得#C02厉魔录#n、#C02天魔录#n，降服法外妖魔，获取珍惜宝物。"},
		2:{"活动ID":2,"权重":100,"是否推荐":0,"任务类型":1,"任务名字":"师门任务","是否可见":1,"活动等级":15,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":20,"每次活跃值":1,"总活跃":20,"完成类型":1,"完成条件":20,"任务图标":202001,"未开时描述":"$NONE$","时间描述":"全天","活动形式":1,"奖励物品编号":200004,"参加事件":"NPC","npc":"schoolMaster","任务编号":30001,"活动描述":"师门任务繁琐，因此急需各派门人回去帮助。每天完成#C0420#n项师门任务，能获得大量经验及师父青睐，是短期内快速成长的最佳捷径。"},
		3:{"活动ID":3,"权重":80,"是否推荐":0,"任务类型":1,"任务名字":"秘册任务","是否可见":1,"活动等级":25,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":10,"每次活跃值":1,"总活跃":10,"完成类型":1,"完成条件":10,"任务图标":202048,"未开时描述":"$NONE$","时间描述":"全天","活动形式":1,"奖励物品编号":(202006,202008),"参加事件":"NPC","npc":10402,"任务编号":50201,"活动描述":"记载天地灵宝的秘册落在了他人手中，其中又不少与你有缘，把它夺回，按图挖宝吧！"},
		4:{"活动ID":4,"权重":70,"是否推荐":0,"任务类型":1,"任务名字":"封妖","是否可见":1,"活动等级":15,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":10,"每次活跃值":1,"总活跃":10,"完成类型":1,"完成条件":10,"任务图标":246010,"未开时描述":"$NONE$","时间描述":"全天","活动形式":3,"奖励物品编号":(230101,230102,230103),"参加事件":"FengYao","活动描述":"散落各地的妖人、魔物虽然危险不大，但依然为平民生活造成大量不便，讨伐他们同时也能获得经验、奖励，修道者可乐而不为？"},
		5:{"活动ID":5,"权重":50,"是否推荐":0,"任务类型":2,"任务名字":"单人竞技场","是否可见":1,"活动等级":20,"活动日期类型":2,"活动日期":6,"活动时间":(20,0,22,0),"所需活跃值":0,"可做次数":5,"每次活跃值":2,"总活跃":10,"完成类型":1,"完成条件":5,"任务图标":100000,"未开时描述":"20点开启","时间描述":"20:00~22:00","活动形式":1,"奖励物品编号":(200160,230101,230102,230103,234901),"参加事件":"NPC","npc":10207,"活动描述":"单人竞技场活动，可提前5分钟进场，前5场竞技更有丰厚奖励"},
		6:{"活动ID":6,"权重":60,"是否推荐":0,"任务类型":1,"任务名字":"离线降魔","是否可见":1,"活动等级":20,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":80,"每次活跃值":0,"总活跃":0,"完成类型":1,"完成条件":80,"任务图标":10003,"未开时描述":"$NONE$","时间描述":"全天","活动形式":2,"奖励物品编号":(202047,202048),"参加事件":"OPEN5","活动描述":"离线降魔，不与降魔任务共享次数"},
		11:{"活动ID":11,"权重":90,"是否推荐":0,"任务类型":1,"任务名字":"每日答题","是否可见":1,"活动等级":20,"活动日期类型":1,"活动日期":0,"活动时间":(12,0,24,0),"所需活跃值":0,"可做次数":10,"每次活跃值":1,"总活跃":10,"完成类型":1,"完成条件":10,"任务图标":10001,"未开时描述":"12点开启","时间描述":"12:00~24:00","活动形式":1,"奖励物品编号":(230102,230101,245001),"参加事件":"NPC","npc":10301,"活动描述":"每天12点可前往全知道人处进行答题，答题共有十道题目，答对六题或以上可领取特殊奖励"},
		12:{"活动ID":12,"权重":85,"是否推荐":0,"任务类型":1,"任务名字":"仙盟任务","是否可见":1,"活动等级":20,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":20,"每次活跃值":1,"总活跃":20,"完成类型":1,"完成条件":20,"任务图标":202008,"未开时描述":"$NONE$","时间描述":"全天","活动形式":3,"奖励物品编号":(200009,200051),"参加事件":"NPC","npc":"guildMaster","任务编号":30201,"活动描述":"加入仙盟后每天可在仙盟总管处接取仙盟任务，每天二十次，可获得丰厚经验"},
		13:{"活动ID":13,"权重":60,"是否推荐":0,"任务类型":1,"任务名字":"运镖任务","是否可见":1,"活动等级":35,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":55,"可做次数":3,"每次活跃值":2,"总活跃":6,"完成类型":1,"完成条件":3,"任务图标":241001,"未开时描述":"达55活跃","时间描述":"全天","活动形式":1,"奖励物品编号":200002,"参加事件":"NPC","npc":10209,"任务编号":30301,"活动描述":"每天活跃度≥#C0255#n后，可通过镖师处领取运镖任务，护送至目标点可获得丰厚奖励"},
		14:{"活动ID":14,"权重":80,"是否推荐":0,"任务类型":1,"任务名字":"幸运探宝","是否可见":1,"活动等级":25,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":10,"每次活跃值":1,"总活跃":10,"完成类型":1,"完成条件":10,"任务图标":230001,"未开时描述":"$NONE$","时间描述":"全天","活动形式":1,"奖励物品编号":(224101,200154,245001,246051),"参加事件":"NPC","npc":10211,"活动描述":"每天可在探宝仙子处传送进入宝物之地，通过投骰子在其中探索一番更能收获丰厚奖励"},
		15:{"活动ID":15,"权重":80,"是否推荐":0,"任务类型":1,"任务名字":"试炼幻境","是否可见":1,"活动等级":40,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":2,"每次活跃值":1,"总活跃":20,"完成类型":2,"完成条件":20,"任务图标":246051,"未开时描述":"$NONE$","时间描述":"全天","活动形式":1,"奖励物品编号":(202043,202044,202045,200153),"参加事件":"NPC","npc":10901,"活动描述":"每天进入幻境都可参与试炼获得奖励，通过竞速排行还能在每周获得排行奖励"},
		16:{"活动ID":16,"权重":90,"是否推荐":0,"任务类型":1,"任务名字":"竹林除妖","是否可见":1,"活动等级":45,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":1,"每次活跃值":10,"总活跃":10,"完成类型":1,"完成条件":1,"任务图标":246003,"未开时描述":"$NONE$","时间描述":"全天","活动形式":2,"奖励物品编号":(241305,241306,247002,247003,245001),"参加事件":"NPC","npc":10212,"活动描述":"每天可以完成一次的副本任务，奖励非常丰厚，推荐每日完成"},
		17:{"活动ID":17,"权重":100,"是否推荐":0,"任务类型":2,"任务名字":"天问初试","是否可见":1,"活动等级":20,"活动日期类型":2,"活动日期":6,"活动时间":(12,0,21,0),"所需活跃值":0,"可做次数":20,"每次活跃值":1,"总活跃":20,"完成类型":1,"完成条件":20,"任务图标":202006,"未开时描述":"12点开启","时间描述":"12:00~21:00","活动形式":1,"奖励物品编号":(202024,202025,246051,245001),"参加事件":"NPC","npc":"firstExam","活动描述":"每周六12点可前往天问初试考官处领取任务进行共计二十题的天问初试答题，成绩优秀者可获取金章之试的参与资格"},
		18:{"活动ID":18,"权重":100,"是否推荐":0,"任务类型":2,"任务名字":"金章之试","是否可见":1,"活动等级":20,"活动日期类型":2,"活动日期":6,"活动时间":(21,0,22,0),"所需活跃值":0,"可做次数":20,"每次活跃值":0,"总活跃":0,"完成类型":1,"完成条件":20,"任务图标":203001,"未开时描述":"21点开启","时间描述":"21:00~22:00","活动形式":1,"奖励物品编号":246051,"参加事件":"NPC","npc":"finalExam","活动描述":"在天问初试成绩优秀者可在当晚20:00获取金章之试参与资格，并前往金章之试考官处进行答题赢取独特称谓和丰厚奖励"},
		19:{"活动ID":19,"权重":80,"是否推荐":0,"任务类型":2,"任务名字":"天问献花","是否可见":1,"活动等级":20,"活动日期类型":2,"活动日期":6,"活动时间":(20,0,21,0),"所需活跃值":0,"可做次数":1,"每次活跃值":0,"总活跃":0,"完成类型":1,"完成条件":1,"任务图标":202032,"未开时描述":"20点开启","时间描述":"20:00~21:00","活动形式":1,"奖励物品编号":200010,"参加事件":"NPC","npc":10214,"活动描述":"周六晚上20点可前往天问主事处对有资格参与金章之试的玩家进行献花援助，献花有几率赢取海量积分大奖"},
		20:{"活动ID":20,"权重":80,"是否推荐":0,"任务类型":1,"任务名字":"入世修行","是否可见":1,"活动等级":50,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":200,"每次活跃值":0,"总活跃":0,"完成类型":1,"完成条件":200,"任务图标":202008,"未开时描述":"$NONE$","时间描述":"全天","活动形式":3,"奖励物品编号":(200157,245001,200158),"参加事件":"NPC","npc":10215,"任务编号":30601,"活动描述":"每周可领取一次入世修行，通过完成各种任务获得经验奖励，任务完成次数达到一定数量还可获得物品奖励"},
		21:{"活动ID":21,"权重":100,"是否推荐":0,"任务类型":2,"任务名字":"仙盟大战","是否可见":1,"活动等级":15,"活动日期类型":2,"活动日期":(2,4),"活动时间":(19,30,22,0),"所需活跃值":0,"可做次数":1,"每次活跃值":20,"总活跃":20,"完成类型":1,"完成条件":1,"任务图标":234902,"未开时描述":"20点开启","时间描述":"20:00~22:00","活动形式":3,"奖励物品编号":(200160,234201,234401,234904),"参加事件":"NPC","npc":"guildFight","活动描述":"提前一天以上报名，报名成功后将在周二、周四晚上20点共进行两场大战。仙盟大战分为精英组和普通组，精英组为三队随机对决，盟主和副盟主请提前配置精英组出战人员，普通组为仙盟双方全员大战。仙盟大战除了有丰厚个人奖励外，还可获得大量仙盟资金"},
		22:{"活动ID":22,"权重":90,"是否推荐":0,"任务类型":1,"任务名字":"幻波池","是否可见":1,"活动等级":55,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":1,"每次活跃值":10,"总活跃":10,"完成类型":1,"完成条件":1,"任务图标":246003,"未开时描述":"$NONE$","时间描述":"全天","活动形式":2,"奖励物品编号":(241306,241307,247003,247004,245001),"参加事件":"NPC","npc":10212,"活动描述":"每天可以完成一次的副本任务，奖励非常丰厚，推荐每日完成"},
		23:{"活动ID":23,"权重":70,"是否推荐":0,"任务类型":1,"任务名字":"邪道煞星","是否可见":1,"活动等级":30,"活动日期类型":1,"活动日期":0,"活动时间":(10,0,24,0),"所需活跃值":0,"可做次数":3,"每次活跃值":5,"总活跃":15,"完成类型":1,"完成条件":3,"任务图标":202006,"未开时描述":"10点开启","时间描述":"10:00~24:00","活动形式":2,"奖励物品编号":(200151,200152,200153,200155),"参加事件":"OPEN4","活动描述":"活动时间每个整点出现邪道煞星，组队击杀可以获得丰富奖励"},
		24:{"活动ID":24,"权重":70,"是否推荐":0,"任务类型":2,"任务名字":"组队竞技场","是否可见":1,"活动等级":30,"活动日期类型":2,"活动日期":5,"活动时间":(20,0,22,0),"所需活跃值":0,"可做次数":1,"每次活跃值":10,"总活跃":10,"完成类型":1,"完成条件":1,"任务图标":100000,"未开时描述":"20点开启","时间描述":"20:00~22:00","活动形式":2,"奖励物品编号":(200160,225902),"参加事件":"NPC","npc":96725,"活动描述":"组队竞技场活动，组队挑战服务器中相近实力的其他玩家，最终的冠军获得特殊称谓"},
		26:{"活动ID":26,"权重":70,"是否推荐":0,"任务类型":1,"任务名字":"北斗七星","是否可见":1,"活动等级":30,"活动日期类型":2,"活动日期":6,"活动时间":(0,0,24,0),"所需活跃值":0,"可做次数":7,"每次活跃值":2,"总活跃":14,"完成类型":1,"完成条件":7,"任务图标":100000,"未开时描述":"$NONE$","时间描述":"0:00~24:00","活动形式":1,"奖励物品编号":(200154,224201,224202,224203,224203),"参加事件":"NPC","npc":"triones","活动描述":"天上北斗七星下凡，找到北斗七星并成功完成北斗七星的考验可以获得北斗七星的奖励"},
		27:{"活动ID":27,"权重":70,"是否推荐":0,"任务类型":2,"任务名字":"五岳帝君","是否可见":1,"活动等级":30,"活动日期类型":2,"活动日期":7,"活动时间":0,"所需活跃值":0,"可做次数":5,"每次活跃值":2,"总活跃":10,"完成类型":1,"完成条件":5,"任务图标":100000,"未开时描述":"$NONE$","时间描述":"0:00~24:00","活动形式":2,"奖励物品编号":(200151,200152,200155),"参加事件":"NPC","npc":"fiveBoss","活动描述":"山川林泽皆有神灵，五岳则为其中之首。每逢良辰吉日，则五岳帝君分别化成人形，于人间观赏游玩。修行者若能找到泰山君、衡山君、华山君、嵩山君、恒山君这五位帝君的踪迹，并通过他们给予的测试，则能获得丰厚奖赏！"},
		102:{"活动ID":102,"权重":100,"是否推荐":0,"任务类型":1,"任务名字":"魔教入侵","是否可见":1,"活动等级":30,"活动日期类型":2,"活动日期":(2,4),"活动时间":(12,0,14,0),"所需活跃值":0,"可做次数":10,"每次活跃值":0,"总活跃":0,"完成类型":1,"完成条件":10,"任务图标":100404,"未开时描述":"12点开启","时间描述":"12:00~14:00","活动形式":2,"奖励物品编号":(230101,230102,200154,200159),"参加事件":"NPC","npc":"ACT(guildRobber,1001)","活动描述":"血神教挟恶重来，意图掳掠各仙盟物资，需及时返回领地，组队击退魔人。前十次战斗可获得经验与银币，击败自己仙盟的血神弟子获得额外仙盟贡献，击败其他仙盟的血神弟子则获得侠义值"},
		101:{"活动ID":101,"权重":100,"是否推荐":0,"任务类型":1,"任务名字":"大衍藏宝秘册","是否可见":0,"活动等级":99,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":99,"每次活跃值":0,"总活跃":0,"完成类型":1,"完成条件":99,"任务图标":202007,"未开时描述":"$NONE$","时间描述":"全天","活动形式":1,"奖励物品编号":(230001,230201,200155,200156),"活动描述":"大衍藏宝秘册"},
		25:{"活动ID":25,"权重":100,"是否推荐":0,"任务类型":2,"任务名字":"门派试炼","是否可见":1,"活动等级":40,"活动日期类型":2,"活动日期":(1,3),"活动时间":(20,0,22,0),"所需活跃值":0,"可做次数":1,"每次活跃值":20,"总活跃":20,"完成类型":1,"完成条件":1,"任务图标":202008,"未开时描述":"20点开启","时间描述":"20:00~22:00","活动形式":2,"奖励物品编号":(200152,234901,200159),"参加事件":"NPC","npc":"ACT(schoolFight,1001)","活动描述":"组队通过各大门派弟子的试炼，最快通过试炼的前三队伍可获得独特称谓。通过一次后再次挑战只会记录时间，无其他奖励。"},
		28:{"活动ID":28,"权重":80,"是否推荐":0,"任务类型":2,"任务名字":"仙盟迷宫","是否可见":1,"活动等级":20,"活动日期类型":2,"活动日期":(1,3,5),"活动时间":(12,30,14,0),"所需活跃值":0,"可做次数":1,"每次活跃值":0,"总活跃":0,"完成类型":1,"完成条件":1,"任务图标":230001,"未开时描述":"12点30开启","时间描述":"12:30~14:00","活动形式":1,"奖励物品编号":(230101,230102,200154,200159),"参加事件":"NPC","npc":"ACT(guildMaze,2001)","活动描述":"在规定时间内通过仙盟迷宫，捡取迷宫内的宝物"},
		29:{"活动ID":29,"权重":40,"是否推荐":0,"任务类型":1,"任务名字":"异兽任务","是否可见":0,"活动等级":15,"活动日期类型":1,"活动日期":0,"活动时间":0,"所需活跃值":0,"可做次数":1,"每次活跃值":0,"总活跃":0,"完成类型":1,"完成条件":1,"任务图标":202001,"未开时描述":"$NONE$","时间描述":"全天","活动形式":1,"奖励物品编号":"$NONE$","参加事件":"NPC","npc":10208,"任务编号":50001,"活动描述":"前往齐霞儿处接取异兽任务，完成后领取异兽。"},
	}

	rewardData = {
		1:{"所需活跃度":20,"展示物品编号":200101,"奖励物品编号":{221401:1,200008:1}},
		2:{"所需活跃度":40,"展示物品编号":200102,"奖励物品编号":{221403:1,200008:1}},
		3:{"所需活跃度":60,"展示物品编号":200103,"奖励物品编号":{200002:1000,200008:1}},
		4:{"所需活跃度":80,"展示物品编号":200104,"奖励物品编号":{200001:150000,200008:1}},
		5:{"所需活跃度":100,"展示物品编号":200105,"奖励物品编号":{230101:2,200008:1}},
	}

	jumpData = {
		101:{"名称":"商城","描述":"使用龙纹玉购买商品","链接类型":1,"链接目的":10,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":5},
		102:{"名称":"邪道煞星","描述":"每到整点，邪道煞星会出现在#C03天墉城#n、#C03峨眉山#n、#C03莽苍山#n、#C03封妖塔外#n、#C03云顶村#n五个地图上，当所有五行煞星都被击杀后，会出现顶级首领#C02天罗子#n","链接类型":2,"链接目的":1130,"活动日期类型":2,"是否需要仙盟":0,"活动日期":2,"活动时间":(1000,2400),"条件类型":1,"活动等级":30},
		103:{"名称":"竹林除妖","描述":"击杀赤血神君，拯救村民","链接类型":3,"链接目的":"NPC","npc":10212,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":45},
		104:{"名称":"幻波池","描述":"击杀玉娘子崔盈，通过幻波池试练","链接类型":3,"链接目的":"NPC","npc":10212,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":55},
		105:{"名称":"天问初试","描述":"依次完成20名考官的试练","链接类型":3,"链接目的":"NPC","npc":90001,"活动日期类型":2,"是否需要仙盟":0,"活动日期":6,"活动时间":(1200,2200),"条件类型":1,"活动等级":20},
		106:{"名称":"秘册任务","描述":"击杀盗匪获得#C02小衍藏宝秘册#n","链接类型":3,"链接目的":"NPC","npc":10402,"任务编号":50201,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":25},
		107:{"名称":"兑换","描述":"使用#C02青龙珠#n、#C02赤龙珠#n、#C02金龙珠#n、#C02黑龙珠#n、#C02黄龙珠#n兑换1张#C02大衍藏宝秘册#n","链接类型":3,"链接目的":"NPC","npc":10601,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":5},
		108:{"名称":"炼丹","描述":"消耗灵气获得物品，灵气在#C02乘骑坐骑#n时获得","链接类型":1,"链接目的":17,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		109:{"名称":"每日答题","描述":"连答10道题目获得奖励，连续答对题数越多，获得奖励越高","链接类型":3,"链接目的":"NPC","npc":10301,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(1200,2400),"条件类型":1,"活动等级":20},
		110:{"名称":"幻境试炼","描述":"挑战关卡，连续挑战，关卡数越高，难度越大，奖励越多","链接类型":3,"链接目的":"NPC","npc":10901,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":40},
		111:{"名称":"大衍藏宝秘册","描述":"到特定地点使用秘册获得丰厚奖励，大衍藏宝秘册可由#C02五色龙珠#n合成","链接类型":3,"链接目的":"NPC","npc":10601,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":5},
		112:{"名称":"鲜花商店","描述":"使用鲜花积分购买商品，鲜花积分可在每周六的#C02金章之试#n活动中投注成功后获得","链接类型":1,"链接目的":54,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		113:{"名称":"杂货店","描述":"使用银币购买商品","链接类型":1,"链接目的":20,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		114:{"名称":"降魔商店","描述":"使用降魔积分购买商品，击杀#C02厉魔#n、#C02天魔#n可获得降魔积分","链接类型":1,"链接目的":51,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		115:{"名称":"侠义商店","描述":"使用侠义值购买商品，带低10级的新手玩家进行降魔任务、协助其他玩家通过入世修行的战斗、每天击杀第4个及之后的邪道煞星、协助其他玩家通过主线剧情战斗等，都可获得侠义值","链接类型":1,"链接目的":52,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		116:{"名称":"武勋商店","描述":"使用武勋值购买商品，参加每周六#C02竞技场#n活动可获得武勋值","链接类型":1,"链接目的":53,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		117:{"名称":"门派商店","描述":"使用门派积分购买商品，完成每天师门任务可获得门派积分","链接类型":1,"链接目的":50,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":15},
		118:{"名称":"挑战厉魔","描述":"使用#C02厉魔录#n可进入厉魔挑战，每#C02120环#n降魔任务达成时有一定几率获得#C02厉魔录#n","链接类型":3,"链接目的":"NPC","npc":10401,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		119:{"名称":"挑战天魔","描述":"使用#C02天魔录#n可进入天魔挑战，每#C02600环#n降魔任务达成时有一定几率获得#C02天魔录#n","链接类型":3,"链接目的":"NPC","npc":10401,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		120:{"名称":"门派试练","描述":"连续挑战各门派精英高手，每一轮都可获得奖励，坚持轮数越多，获得奖励越丰厚","链接类型":3,"链接目的":"NPC","npc":10301,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(2000,2200),"条件类型":1,"活动等级":40},
		121:{"名称":"幸运探宝","描述":"投骰子移动，步步惊喜","链接类型":3,"链接目的":"NPC","npc":10211,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		122:{"名称":"单人竞技场","描述":"武无第二，胜者为王","链接类型":3,"链接目的":"NPC","npc":10207,"活动日期类型":2,"是否需要仙盟":0,"活动日期":6,"活动时间":(2000,2200),"条件类型":1,"活动等级":20},
		123:{"名称":"仙盟大战","描述":"仙盟对抗，精英组决胜败，普通组定荣耀，胜败皆可获得奖励","链接类型":3,"链接目的":"NPC","npc":10301,"活动日期类型":2,"是否需要仙盟":1,"活动日期":(2,4),"活动时间":(2000,2200),"条件类型":1,"活动等级":15},
		124:{"名称":"魔教入侵","描述":"击杀潜入仙盟的血神教弟子和血神教护法，可在本盟击杀，也可协助其他仙盟","链接类型":3,"链接目的":"NPC","npc":10301,"活动日期类型":2,"是否需要仙盟":1,"活动日期":(1,3,5),"活动时间":(1200,1400),"条件类型":1,"活动等级":15},
		125:{"名称":"月儿岛秘径图","描述":"使用#C02月儿岛秘径图#n挑战3个珍宝守护者，每天完成第10次#C02秘册任务#n时有一定几率获得#C02月儿岛秘径图#n","链接类型":3,"链接目的":"NPC","npc":10402,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":25},
		126:{"名称":"入世修行","描述":"200环连续任务，可获得大量经验及装备材料","链接类型":3,"链接目的":"NPC","npc":10215,"任务编号":30601,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":50},
		127:{"名称":"小衍藏宝秘册","描述":"到特定地点使用秘册获得奖励，每天完成#C02秘册任务#n可获得小衍藏宝秘册","链接类型":3,"链接目的":"NPC","npc":10402,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":25},
		128:{"名称":"副本","描述":"通关任一副本皆可获得此物品","链接类型":3,"链接目的":"NPC","npc":10212,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":45},
		129:{"名称":"银币商店","描述":"使用银币购买商品","链接类型":1,"链接目的":21,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		130:{"名称":"元宝商店","描述":"使用元宝购买商品","链接类型":1,"链接目的":22,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		131:{"名称":"烹饪","描述":"使用活力制作食品","链接类型":1,"链接目的":23,"活动日期类型":1,"是否需要仙盟":1,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		132:{"名称":"炼丹术","描述":"使用活力制作丹药","链接类型":1,"链接目的":24,"活动日期类型":1,"是否需要仙盟":1,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		133:{"名称":"打造技巧","描述":"使用活力制作打造符","链接类型":1,"链接目的":25,"活动日期类型":1,"是否需要仙盟":1,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		134:{"名称":"裁缝技巧","描述":"使用活力制作裁缝符","链接类型":1,"链接目的":26,"活动日期类型":1,"是否需要仙盟":1,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		135:{"名称":"炼金技巧","描述":"使用活力制作炼金符","链接类型":1,"链接目的":27,"活动日期类型":1,"是否需要仙盟":1,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		136:{"名称":"药店","描述":"使用银币购买药品","链接类型":1,"链接目的":19,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":1},
		137:{"名称":"降魔任务","描述":"获得大量经验，完成一定环数可额外获得#C02厉魔录#n和#C02天魔录#n","链接类型":3,"链接目的":"NPC","npc":10401,"任务编号":30101,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":20},
		138:{"名称":"装备打造","描述":"消耗材料打造装备，一定几率可获得珍品装备","链接类型":1,"链接目的":3,"活动日期类型":1,"是否需要仙盟":0,"活动日期":0,"活动时间":(0,2400),"条件类型":1,"活动等级":40},
		139:{"名称":"金章之试","描述":"连答20道题目获得奖励，耗时越少奖励越丰富","链接类型":3,"链接目的":"NPC","npc":90021,"活动日期类型":2,"是否需要仙盟":0,"活动日期":6,"活动时间":(2100,2200),"条件类型":1,"活动等级":20},
		140:{"名称":"组队竞技场","描述":"组队竞技，协同制敌","链接类型":3,"链接目的":"NPC","npc":96725,"活动日期类型":2,"是否需要仙盟":0,"活动日期":6,"活动时间":(2000,2200),"条件类型":1,"活动等级":30},
		141:{"名称":"五岳帝君","描述":"组队挑战5名帝君","链接类型":3,"链接目的":"NPC","npc":10301,"活动日期类型":2,"是否需要仙盟":0,"活动日期":6,"活动时间":(0,2400),"条件类型":1,"活动等级":30},
		142:{"名称":"北斗七星","描述":"七星汇聚，单人挑战","链接类型":3,"链接目的":"NPC","npc":10301,"活动日期类型":2,"是否需要仙盟":0,"活动日期":7,"活动时间":(0,2400),"条件类型":1,"活动等级":30},
	}
#导表结束
	
	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.actList = {}
		self.initAct()
		
	def onNewHour(self, day, hour, wday):
		import role
		role.callForAllRoles(refreshTaskNpc)

	def initAct(self):
		'''初始化活动
		'''
		self.actList = {}
		for actInfo in self.activityData.itervalues():
			actId = actInfo["活动ID"]
			actObj = ActInfo(actId)
			actObj.game = weakref.proxy(self)
			self.actList[actId] = actObj

		self.jumpList = {}
		for jumpId in self.jumpData:
			jumpObj = JumpInfo(jumpId)
			jumpObj.game = weakref.proxy(self)
			self.jumpList[jumpId] = jumpObj

	def getMsg(self, who):
		'''打包信息
		'''
		actList = []
		for actObj in self.actList.itervalues():
			if not actObj.vaildLevel(who):
				continue
			if not actObj.cntMax and not actObj.actPointMax:
				continue
			actList.append(actObj.getMsg(who))
		return actList
	
	def getCustomScriptHandler(self, script):
		'''自定义脚本处理
		'''
		for pattern, handler in gScriptHandlerList.iteritems():
			m = re.match(pattern, script)
			if not m:
				continue
			args = m.groups()
			return handler, args
		return None, None

	def joinEvent(self, who, actId):
		'''参加事件
		'''
		actObj = self.actList.get(actId)
		if not actObj.validDoEvent(who):
			return

		script = actObj.event
		handler, args = self.getCustomScriptHandler(script)
		if handler:
			handler(self, actObj, who, *args)
		else:
			raise Exception("无法解释的脚本:%s" % script)
		
	def jumpEvent(self, who, jumpId):
		'''途径事件
		'''
		jumpObj = self.jumpList.get(jumpId)
		if not jumpObj:
			return
		if not jumpObj.validDoEvent(who):
			return

		script = jumpObj.event
		handler, args = self.getCustomScriptHandler(script)
		if handler:
			handler(self, jumpObj, who, *args)
		else:
			raise Exception("无法解释的脚本:%s" % script)

	def onLogin(self, who, bRelogin):
		rpcOpen(who, None, False)
		checkActReward(who)
		rpcActTaskNpcList(who)
		
	def onUpLevel(self, who):
		refreshTaskNpc(who)
		
	def getTaskNpcList(self, who):
		'''可接任务npc列表
		'''
		if not hasattr(who, "acceptTaskList"):
			self.createAcceptTaskList(who)
		return who.acceptTaskList.keys()
			
	def createAcceptTaskList(self, who):
		'''创建可接任务 
		'''
		taskList = {}
		for actObj in self.actList.itervalues():
			if actObj.isTaskAccepted(who):
				npcObj = actObj.getTaskNpc(who)
				taskList[npcObj.id] = actObj
		who.acceptTaskList = taskList

	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 0:
			txtList = []
			txtList.append("1-参加降魔任务")
			txtList.append("2-参加师门任务")
			txtList.append("3-参加宝图任务")
			txtList.append("4-参加封妖活动")
			txtList.append("200-初始化活动")
			message.dialog(who, "\n".join(txtList))
		elif cmdIdx == 100:
			rewardId = args[0]
			import base_pb2
			msg = base_pb2.int32_()
			msg.iValue = rewardId
			rpcReward(who, msg)
		elif cmdIdx == 200:
			self.initAct()
			message.tips(who, "初始化活动成功")
		else:
			self.joinEvent(who, cmdIdx)

# ======================================================================
# 活动/任务/途径信息
# ======================================================================

class InfoBase(object):
	'''信息基类
	'''

	def __init__(self, idx):
		self.id = idx
	
	def getConfig(self, key, default=0):
		'''获取配置数据
		'''
		raise Exception("需要子类实现")

	@property
	def name(self):
		'''名字
		'''
		return self.getConfig("任务名字", "")

	@property
	def level(self):
		'''等级
		'''
		return self.getConfig("活动等级", 0)

	@property
	def event(self):
		'''事件
		'''
		return self.getConfig("参加事件", "")
	
	def vaildLevel(self, who):
		'''检查等级
		'''
		return  who.level >= self.level
	
	def validDoEvent(self, who):
		'''检查执行事件
		'''
		if not self.event:
			return False
		if not isinstance(self.event, str):
			return
		if not self.vaildLevel(who):
			return False
		return True
	
	def getTaskNpc(self, who):
		'''可接任务npc
		'''
		npcIdx = self.getConfig("npc", 0)
		if not npcIdx:
			return None
		if isinstance(npcIdx, int):
			return npc.getNpcByIdx(npcIdx)
		
		script = npcIdx
		for pattern, handler in npcHandlerList.iteritems():
			m = re.match(pattern, script)
			if m:
				args = m.groups()
				return handler(who, *args)
		
		return None
	
	def getTaskId(self):
		'''可接任务编号
		'''
		return self.getConfig("任务编号", 0)


class ActInfo(InfoBase):
	'''活动信息
	'''
	
	def getConfig(self, key, default=0):
		return Activity.activityData[self.id].get(key, default)
	
	@property
	def cntMax(self):
		'''可做次数
		'''
		return self.getConfig("可做次数", 0)

	@property
	def actPointMax(self):
		'''总活跃
		'''
		return self.getConfig("总活跃", 0)

	@property
	def perActPoint(self):
		'''每次活跃值
		'''
		return self.getConfig("每次活跃值", 0)

	def getMsg(self, who, notice=False):
		'''打包信息
		'''
		msg = act_center_pb2.actMsg()
		msg.actId = self.id
		if self.cntMax:
			msg.count = self.getCnt(who)
			msg.countMax = self.cntMax
		if self.actPointMax:
			msg.actPoint = self.getActPoint(who)
			msg.actPointMax = self.actPointMax
		return msg

	def getCnt(self, who, iWhichCyc=0):
		'''已做次数
		'''
		func = cntFunc.get(self.name)
		if func:
			return func(who, iWhichCyc)
		return 0

	def getActPoint(self, who):
		'''已得活跃
		'''
		func = actFunc.get(self.name)
		if func:
			actPoint = func(who) * self.perActPoint
		else:
			actPoint = self.getCnt(who) * self.perActPoint

		return min(self.actPointMax, actPoint)
	
	def isTaskAccepted(self, who):
		'''是否可接任务
		'''
		if not self.vaildLevel(who):
			return False
		if not self.validTime(who):
			return False
		
		taskId = self.getTaskId()
		if taskId:
			for taskObj in who.taskCtn.getAllValues():
				if taskObj.parentId == taskId:
					return False
			
			# 暂离的队员还是可以看到的
			teamObj = who.inTeam()
			if teamObj:
				for taskObj in teamObj.taskCtn.getAllValues():
					if taskObj.parentId == taskId:
						return False

		cntMax = self.cntMax
		if cntMax and self.getCnt(who) >= cntMax:
			return False
		
		actPointMax = self.actPointMax
		if actPointMax and self.getActPoint(who) >= actPointMax:
			return False
		
		npcObj = self.getTaskNpc(who)
		if not npcObj:
			return False

		return True
	
	def validTime(self, who):
		'''检查时间
		'''
		info = Activity.activityData[self.id]
		if not checkTime(info, True):
			return False
		return True

class JumpInfo(InfoBase):
	'''途径信息
	'''
	
	def getConfig(self, key, default=0):
		return Activity.jumpData[self.id].get(key, default)
	
	@property
	def name(self):
		'''名字
		'''
		return self.getConfig("名称", "")
	
	@property
	def event(self):
		'''事件
		'''
		return self.getConfig("链接目的", "")
	
	def validDoEvent(self, who):
		jumpInfo = Activity.jumpData[self.id]
		if not checkTime(jumpInfo):
			return
		if self.getConfig("是否需要仙盟") and not who.getGuildObj():
			return False
		return InfoBase.validDoEvent(self, who)
	


#===============================================================================
# 次数处理
#===============================================================================
def getPetTaskCnt(who, *args):
	npcObj = npc.getNpcByIdx(10208)
	if not npcObj:
		return 0
	hasCurTask,nextTaskLv = npcObj.hasLookPetTask(who)
	if not hasCurTask:
		return 1
	return 0
	

cntFunc = {
	"降魔任务":lambda who, iWhichCyc: who.day.fetch("demonRing", iWhichCyc=iWhichCyc),
	"离线降魔":lambda who, iWhichCyc: who.day.fetch("offlineRing", iWhichCyc=iWhichCyc),
	"师门任务":lambda who, iWhichCyc: who.day.fetch("schoolRing", iWhichCyc=iWhichCyc),
	"秘册任务":lambda who, iWhichCyc: who.day.fetch("mapRing", iWhichCyc=iWhichCyc),
	"封妖":lambda who, iWhichCyc: who.day.fetch("fengyaoKillCnt0", iWhichCyc=iWhichCyc),
	"单人竞技场":lambda who, iWhichCyc: who.day.fetch("raceFightCount", iWhichCyc=iWhichCyc),
	"仙盟任务":lambda who, iWhichCyc: who.day.fetch("guildRing", iWhichCyc=iWhichCyc),
	"运镖任务":lambda who, iWhichCyc: who.day.fetch("escort", iWhichCyc=iWhichCyc),
	"每日答题":lambda who, iWhichCyc: who.day.fetch("answerDayCnt", iWhichCyc=iWhichCyc),
	"试炼幻境":lambda who, iWhichCyc: who.day.fetch("flFail", iWhichCyc=iWhichCyc),
	"幸运探宝":lambda who, iWhichCyc: who.getCubeCount(iWhichCyc=iWhichCyc),
	"入世修行":lambda who, iWhichCyc: who.taskCtn.fetch("ringRing"),
	"天问初试":lambda who, iWhichCyc: len(who.week.fetch("FEComTime", {}, iWhichCyc=iWhichCyc)),
	"金章之试":lambda who, iWhichCyc: who.week.fetch("finalExamCnt", 0, iWhichCyc=iWhichCyc),
	"天问献花":lambda who, iWhichCyc: 1 if who.day.fetch("betFRecord", {}, iWhichCyc=iWhichCyc) else 0,
	"邪道煞星":lambda who, iWhichCyc: who.day.fetch("starKill", iWhichCyc=iWhichCyc),
	"北斗七星":lambda who, iWhichCyc: len(who.day.fetch("trionesKill", [], iWhichCyc=iWhichCyc)),
	"五岳帝君":lambda who, iWhichCyc: len(who.week.fetch("fiveBoss", [], iWhichCyc=iWhichCyc)),
	"异兽任务":getPetTaskCnt,
	"竹林除妖":lambda who, iWhichCyc: 1 if 1 in who.day.fetch("instanceActPoint", [], iWhichCyc=iWhichCyc) else 0,
	"幻波池":lambda who, iWhichCyc: 1 if 2 in who.day.fetch("instanceActPoint", [], iWhichCyc=iWhichCyc) else 0,
	"门派试炼":lambda who, iWhichCyc : 1 if who.day.fetch("schoolFightWB", iWhichCyc=iWhichCyc) else 0,
	"魔教入侵":lambda who, iWhichCyc: who.day.fetch("guildRobber", iWhichCyc=iWhichCyc),
	"仙盟迷宫":lambda who, iWhichCyc: who.day.fetch("guildMaze", iWhichCyc=iWhichCyc),
	"组队竞技场":lambda who, iWhichCyc : who.day.fetch("teamRaceEnter", 0, iWhichCyc=iWhichCyc),
}


#===============================================================================
# 活跃点处理
#===============================================================================


actFunc = {
	"试炼幻境":lambda who : who.day.fetch("flStage"),
}
# ======================================================================
# 事件相关的
# ======================================================================

def goAndLookNpc(gameObj, actObj, who):
	'''寻找点击NPC
	'''
	if actObj.id in (12, 21, 28, 102,): # 仙盟的活动
		if not who.getGuildObj():
			who.endPoint.rpcOpenUIPanel(67)
			return

	taskId = actObj.getTaskId()
	if taskId:
		taskObj = task.hasTask(who, taskId)
		if taskObj:
			taskObj.goAhead(who)
			return

	npcObj = actObj.getTaskNpc(who)
	if npcObj:
		scene.walkToEtt(who, npcObj)

def trans2FengYao(gameObj, actObj, who):
	'''传送到最适合的封妖场景
	'''
	actFengYao = activity.getActivity("fengyao")
	sceneId = actFengYao.getBestScene(who)
	if sceneId != who.sceneId:
		if not scene.tryTransfer(who, sceneId):
			return
	message.tips(who, "已移动至最合适的封妖场景")

def quickMakeTeam(gameObj, actObj, who, *args):
	'''便捷组队
	'''
	target = int(args[0])
	team.platformservice.quickMakeTeam(who, target)

def openUI(gameObj, actObj, who, *args):
	'''打开挂机界面
	'''
	linkId = int(args[0])
	who.endPoint.rpcOpenUIPanel(linkId)

# def goAndLookActNpc(gameObj, actObj, who, actStr, npcStr):
# 	'''点击活动Npc
# 	'''
# 	import activity
# 	actObj = activity.getActivity(actStr)
# 	if not actObj:
# 		return
# 	npcObj = actObj.getNpcByIdx(int(npcStr))
# 	if npcObj:
# 		scene.walkToEtt(who,npcObj)
# 	else:
# 		message.tips(who, "该活动还未开启")

gScriptHandlerList = {
	"NPC":goAndLookNpc,
	"FengYao":trans2FengYao,
	"TEAM(\d+)":quickMakeTeam,
	"OPEN(\d+)":openUI,
# 	"NPC\((\S+),(\S+)\)": goAndLookActNpc,
}

posNearByMaster = {
	11:(12, 44),
	12:(56, 7),
	13:(70, 51),
	14:(52, 43),
	15:(88, 67),
	16:(63, 95),
}

#===============================================================================
# #npc相关
#===============================================================================
def getActivityNpc(who, actName, npIdx):
	'''活动Npc
	'''
	import activity
	actObj = activity.getActivity(actName)
	if not actObj:
		return None
	if actName in ("guildMaze", "guildRobber"):
		return actObj.getActivityNpc(who, int(npIdx))
	return actObj.getNpcByIdx(int(npIdx))

def getSchoolMasterNpc(who):
	'''门派导师
	'''
	return npc.defines.getSchoolMaster(who.school)

def getGuildMasterNpc(who):
	'''仙盟总管
	'''
	guildObj = who.getGuildObj()
	if guildObj:
		return guildObj.getNpcByType("总管")
	return None

def getGuildFightNpc(who):
	'''盟战接引npc
	'''
	guildObj = who.getGuildObj()
	if guildObj:
		return guildObj.getNpcByType("帮战")
	return None

def getFirstExamNpc(who):
	'''乡试NPC
	'''
	import answer
	firstExamObj = answer.getAnswerFirstExamObj()
	return firstExamObj.getNpcObjByExamNo(1)

def getFinalExamNpc(who):
	'''殿试NPC
	'''
	import answer
	finalExamObj = answer.getAnswerFinalExamObj()
	return finalExamObj.getFinalExamNpc()

def getTrionesNpc(who):
	'''北斗七星
	'''
	actObj = activity.getActivity("triones")
	if actObj:
		return actObj.getEnvoyNpc()
	return None
	
def getFiveBossNpc(who):
	'''五岳帝君
	'''
	actObj = activity.getActivity("fiveBoss")
	if actObj:
		return actObj.getNpcByIdx(1001)
	return None

def getTeamRaceNpc(self, who):
	'''组队竞技场NPC
	'''
	actObj = activity.getActivity("teamRace")
	if actObj:
		return actObj.getTeamRaceEnterNpc()
	return None

npcHandlerList = {
	"ACT\((\S+),(\S+)\)": getActivityNpc,
	"schoolMaster": getSchoolMasterNpc,
	"guildMaster":getGuildMasterNpc,
	"guildFight":getGuildFightNpc,
	"firstExam":getFirstExamNpc,
	"finalExam":getFinalExamNpc,
	"triones":getTrionesNpc,
	"fiveBoss":getFiveBossNpc,
	"teamRace":getTeamRaceNpc,
}

# ======================================================================
# rpc相关的
# ======================================================================

def getActivityCenter():
	return activity.getActivity("center")

def rpcOpen(who, reqMsg, notify=True):
	'''打开活动中心
	'''
	if notify and who.level < 5:
		message.tips(who, "#C04{}级#n开启本系统".format(5))
		return

	msg = {}
	msg["actList"] = getActivityCenter().getMsg(who)
	msg["actPoint"] = packActPoint(who)
	msg["doublePoint"] = who.doublePoint
	msg["frozenDoublePoint"] = who.getFrozenDoublePoint()

	who.endPoint.rpcActCenterInfo(**msg)

def rpcJoin(who, reqMsg):
	'''参加活动
	'''
	actId = reqMsg.iValue
	centerObj = getActivityCenter()
	centerObj.joinEvent(who, actId)

def rpcReward(who, reqMsg):
	'''领取活跃奖励
	'''
	rewardId = reqMsg.iValue
	centerObj = getActivityCenter()
	if rewardId not in centerObj.rewardData:
		return

	rewardInfo = centerObj.rewardData[rewardId]
	if who.getActPoint() < rewardInfo["所需活跃度"]:
		return

	rewardList = who.day.fetch("actReward", [])
	if rewardId in rewardList:
		return

	rewardList.append(rewardId)
	who.day.set("actReward", rewardList)
	who.set("lastActReward", rewardList)

	for propsNo, propsCnt in rewardInfo["奖励物品编号"].iteritems():
		if propsNo == 200008:
			propsCnt = int((20 + who.level * 0.8) / 10) * 20
		launch.launchBySpecify(who, propsNo, propsCnt, False, "领取活跃奖励")
	who.endPoint.rpcActCenterMod(packActPoint(who))

def rpcGetDoublePoint(who, reqMsg):
	'''领取双倍点数
	'''
	fdp = who.getFrozenDoublePoint()
	if not fdp:
		return
	if who.doublePoint >= 80:
		message.tips(who, "高倍点数已非常充足，请使用完后再领取")
		return
	dp = min(fdp, 80 - who.doublePoint, 40)
	who.addDoublePoint(dp, "领取高倍点数", False)
	who.addFrozenDoublePoint(-dp, "领取高倍点数")
	centerChange(who, "doublePoint", "frozenDoublePoint")
	message.tips(who, "高倍点数已领取成功")

def rpcGetJumeData(who, reqMsg):
	jumpId = reqMsg.iValue
	gameObj = getActivityCenter()
	if gameObj:
		gameObj.jumpEvent(who, jumpId)
	
def centerChange(who, *attrName):
	msg = {}
	for attr in attrName:
		msg[attr] = getValByName(who, attr)

	who.endPoint.rpcActCenterModCenter(**msg)

def packActPoint(who):
	'''打包活跃信息
	'''
	msg = act_center_pb2.actPointMsg()
	msg.actPoint = who.getActPoint()
	msg.reward.extend(who.day.fetch("actReward", []))

	return msg

def rpcActTaskNpcList(who):
	'''可接任务npc列表
	'''
	gameObj = getActivityCenter()
	if not gameObj:
		return
	taskNpcList = gameObj.getTaskNpcList(who)
	msgObj = act_center_pb2.taskNpcList()
	msgObj.npcList.extend(taskNpcList)
	who.endPoint.rpcActTaskNpcList(msgObj)
	
# 	msgList = []
# 	for npcId in taskNpcList:
# 		npcObj = getNpc(npcId)
# 		msgList.append("%s:%s" % (npcId, npcObj.name))
# 	print "rpcActTaskNpcList", ",".join(msgList)
	
def refreshTaskNpc(who):
	'''刷新可接任务npc
	'''
	import gevent
	gevent.spawn(refreshTaskNpc2, who.id)
	
def refreshTaskNpc2(roleId):
	who = getRole(roleId)
	if not who:
		return
	gameObj = getActivityCenter()
	if not gameObj:
		return
	
	if hasattr(who, "acceptTaskList"):
		oldAcceptTaskList = who.acceptTaskList
		del who.acceptTaskList
	else:
		oldAcceptTaskList = {}
	gameObj.createAcceptTaskList(who)

	delNpcList = [] # 删除的
	addNpcList = [] # 增加的
	for npcId in oldAcceptTaskList:
		if npcId not in who.acceptTaskList:
			delNpcList.append(npcId)
	for npcId in who.acceptTaskList:
		if npcId not in oldAcceptTaskList:
			addNpcList.append(npcId)
			
	for npcId in delNpcList:
		who.endPoint.rpcActTaskNpcDel(npcId)
	for npcId in addNpcList:
		who.endPoint.rpcActTaskNpcAdd(npcId)
	
# 	delMsgList = []
# 	for npcId in delNpcList:
# 		npcObj = getNpc(npcId)
# 		delMsgList.append("%s:%s" % (npcId, npcObj.name))
# 
# 	addMsgList = []
# 	for npcId in addNpcList:
# 		npcObj = getNpc(npcId)
# 		addMsgList.append("%s:%s" % (npcId, npcObj.name))
# 	print "refreshTaskNpc DEL[%s] ADD:[%s]" % (",".join(delMsgList), ",".join(addMsgList))


# ======================================================================
# 时间相关的
# ======================================================================
def checkTime(info, checkHour=False):
	timetype = info.get("活动日期类型", 0)
	actDateList = info.get("活动日期")
	
	datePart = getDatePart()
	year = datePart["year"]  # 年
	month = datePart["month"]  # 月
	day = datePart["day"]  # 日
	hour = datePart["hour"] # 时
	minute = datePart["minute"] # 分
	wday = datePart["wday"]  # 星期几
	curTime = (year, month, day)  # 年,月,日
	
	if timetype == 1:  # 每天活动
		pass
	elif timetype == 2:  # 每周活动
		if isinstance(actDateList, int):
			if wday != actDateList:
				return False
		elif wday not in actDateList:
			return False
	elif timetype == 3:  # 具体日子
		if len(actDateList) == 4:
			startTime = [year] + list(actDateList[:2])
			endTime = [year] + list(actDateList[2:])
		else:
			startTime = actDateList[:3]
			endTime = actDateList[3:]
		if curTime < startTime:
			return False
		if curTime > endTime:
			return False
	elif timetype == 4:  # 单周活动
		weekNo = getWeekNo()
		if weekNo % 2 == 0:
			return False
		if wday not in actDateList:
			return False
	elif timetype == 5:  # 双周活动 
		weekNo = getWeekNo()
		if weekNo % 2 == 1:
			return False
		if wday not in actDateList:
			return False
	elif timetype == 6:  # 每月活动
		if day not in actDateList:
			return False
	
	if checkHour: # 检查小时
		if info.get("活动时间"):
			curHour = (hour, minute)
			beginHour = info["活动时间"][:2]
			endHour = info["活动时间"][2:]
			if curHour < beginHour or curHour > endHour:
				return False
	
	return True

def checkActReward(who):
	'''检查上次活跃奖励
	'''
	if who.day.fetch("actRewardCheck"):
		return
	who.day.set("actRewardCheck", 1)
	lastActPoint = who.day.fetch("actPoint", iWhichCyc=-1)
	lastActReward = who.day.fetch("actReward", [], -1)
	centerObj = getActivityCenter()
	propsObjList = []
	for rewardId, rewardInfo in centerObj.rewardData.iteritems():
		if rewardId in lastActReward or lastActPoint < rewardInfo["所需活跃度"]:
			continue
		for propsNo, amount in rewardInfo["奖励物品编号"].iteritems():
			if propsNo == 200008:
				amount = int((20 + who.level * 0.8) / 10) * 20
			propsObj = props.new(propsNo)
			if propsObj.isVirtual():
				propsObj.setValue(amount)
			else:
				propsObj.setStack(amount)
			propsObjList.append(propsObj)
	if not propsObjList:
		return
	title = "过期活跃奖励追发"
	content = "你好，由于你昨天的活跃奖励还没领取，所以现以邮件附件追发给你，邮件有时效，#C04请尽快领取#n。"
	mail.sendSysMail(who.id, title, content, propsObjList, 3600 * 24)


def getPerActPoint(actId):
	'''获得每次活跃点
	'''
	centerObj = getActivityCenter()
	actObj = centerObj.actList.get(actId)
	return actObj.perActPoint

def getCntMax(actId):
	'''获取可做次数
	'''
	centerObj = getActivityCenter()
	actObj = centerObj.actList.get(actId)
	return actObj.cntMax

def sendDoublePointForNewBie(who):
	who.addFrozenDoublePoint(40, "新手登录")
	wDay = getDatePart()["wday"]
	who.week.set("fdpwDay", wDay)
	
def afterHotUpdate():
	'''热更后初始化数据
	'''
	actObj = getActivityCenter()
	if actObj:
		actObj.initAct()

from common import *
import message
import npc
import npc.defines
import scene
import weakref
import re
import act_center_pb2
import task.school
import task.map
import task.demon
import activity.fengyao
import launch
import team.platformservice
import timerEvent
import mail
import props
import guild.service
import types
import activity.fiveBoss