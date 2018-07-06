# -*- coding: utf-8 -*-
'''
探宝
'''
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
	}

	eventInfo = {
	}

	rewardInfo = {
		1001:{"探宝积分":20,"数量":20},
		2001:{"物品":[1001],"探宝积分":80,"数量":7},
		2002:{"银币":lambda :10000,"探宝积分":100,"数量":7},
		2003:{"经验":lambda LV:LV*700+8000,"宠物经验":lambda PLV:PLV*500+5500,"银币":lambda :10000,"物品":[1002],"数量":0},
		3001:{"经验":lambda LV:LV*80+1000,"宠物经验":lambda PLV:PLV*55+700,"物品":[1003],"探宝积分":200,"数量":3},
		4001:{"物品":[1003],"探宝积分":150,"数量":7},
		9001:{"经验":lambda LV:LV*80+1000,"宠物经验":lambda PLV:PLV*55+700,"物品":[1004]},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":150,"物品":"224101","数量":"1","绑定":0,"传闻":0},
			{"权重":150,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":150,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":150,"物品":"245001","数量":"1","绑定":0,"传闻":0},
			{"权重":150,"物品":"245051","数量":"2","绑定":0,"传闻":0},
			{"权重":250,"物品":"246051","数量":"1","绑定":0,"传闻":0},
		),
		1002:(
			{"权重":22,"物品":"230103","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234101","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234102","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234103","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234104","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234105","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234106","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234107","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234108","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234109","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234110","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234111","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234112","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234113","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234114","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234115","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234116","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234117","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234118","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234119","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234120","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234121","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234122","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234123","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234124","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234125","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234126","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234127","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234128","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234129","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234130","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234131","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234132","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234133","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234134","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234135","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234136","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234137","数量":"1","绑定":0,"传闻":0},
			{"权重":6,"物品":"234138","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234139","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234140","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234141","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234142","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234143","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234144","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234145","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234146","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234147","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234148","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234149","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234150","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234151","数量":"1","绑定":0,"传闻":0},
			{"权重":33,"物品":"234152","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"234153","数量":"1","绑定":0,"传闻":0},
			{"权重":1000,"物品":"0","数量":"0","绑定":0,"传闻":0},
		),
		1003:(
			{"权重":10,"物品":"224101","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":30,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":5,"物品":"230103","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234101","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234102","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234103","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234104","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234105","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234106","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234107","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234108","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234109","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234110","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234111","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234112","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234113","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234114","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234115","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234116","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234117","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234118","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234119","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234120","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234121","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234122","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234123","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234124","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234125","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234126","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234127","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234128","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234129","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234130","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234131","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234132","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234133","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234134","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234135","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234136","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234137","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234138","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234139","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234140","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234141","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234142","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234143","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234144","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234145","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234146","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234147","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234148","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234149","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234150","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234151","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234152","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234153","数量":"1","绑定":0,"传闻":0},
			{"权重":424,"物品":"200001","数量":"10000","绑定":0,"传闻":0},
			{"权重":400,"物品":"200001","数量":"20000","绑定":0,"传闻":0},
		),
		1004:(
			{"权重":10,"物品":"224101","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":30,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":5,"物品":"230103","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234101","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234102","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234103","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234104","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234105","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234106","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234107","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234108","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234109","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234110","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234111","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234112","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234113","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234114","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234115","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234116","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234117","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234118","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234119","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234120","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234121","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234122","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234123","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234124","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234125","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234126","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234127","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234128","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234129","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234130","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234131","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234132","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234133","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234134","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234135","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234136","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234137","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234138","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234139","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234140","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234141","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234142","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234143","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234144","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234145","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234146","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234147","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234148","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234149","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234150","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234151","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234152","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234153","数量":"1","绑定":0,"传闻":0},
			{"权重":824,"物品":"200001","数量":"10000","绑定":0,"传闻":0},
		),
		2001:(
			{"权重":100,"物品":"245001","数量":"1","绑定":0,"传闻":0},
		),
		2002:(
			{"权重":100,"物品":"230102","数量":"2","绑定":0,"传闻":0},
		),
		2003:(
			{"权重":100,"物品":"230101","数量":"1","绑定":0,"传闻":0},
		),
		2004:(
			{"权重":100,"物品":"224101","数量":"1","绑定":0,"传闻":0},
		),
		2005:(
			{"权重":100,"物品":"230101","数量":"3","绑定":0,"传闻":0},
		),
		3001:(
			{"权重":100,"物品":"245051","数量":"1","绑定":0,"传闻":0},
		),
		3002:(
			{"权重":100,"物品":"245051","数量":"2","绑定":0,"传闻":0},
		),
		3003:(
			{"权重":100,"物品":"245051","数量":"5","绑定":0,"传闻":0},
		),
		3004:(
			{"权重":100,"物品":"245051","数量":"8","绑定":0,"传闻":0},
		),
		3005:(
			{"权重":100,"物品":"245051","数量":"10","绑定":0,"传闻":0},
		),
	}

	groupInfo = {
		9001:(2001,2002,2003,),
		9002:(1001,1002,1003,1004,1005,1006,1007,),
	}

	chatInfo = {
		2401:'''宝物之地只可单人进入''',
		2402:'''宝物之地不可与他人组队而行''',
		2403:'''宝物之地内无法接受他人的组队邀请''',
		2404:'''所邀之人正在探宝中，不可组队''',
		2405:'''宝物之地内不可创建队伍''',
		2406:'''宝物之地内不可加入队伍''',
		2407:'''离宝物之地重置还有#C02$time#n分钟''',
		2408:'''请点击骰子，以投骰子决定移动步数''',
		2409:'''宝物之地内不可直接跳转离开''',
		2410:'''此处禁制开始重置变幻，你已被移出宝物之地''',
		2411:'''骰子点数为#C02$number#n，你将前进#C02$number#n步''',
		2412:'''你当前可用的投骰子次数为#C040次#n''',
		2413:'''请稍候片刻，等待行动结束便可继续探宝''',
		2414:'''此处光秃秃的好像什么也没有''',
		2415:'''你开启了一个普通宝箱并获得了里面的宝物''',
		2416:'''你发现了一个上锁宝箱，#C02答题正确#n才可开启''',
		2417:'''答题正确，你开启了该宝箱并获得了里面的宝物''',
		2418:'''答题错误，开启宝箱#C04失败#n''',
		2419:'''恭喜你抵达终点并获得了通关宝箱中的宝物''',
		2420:'''你惊醒了沉睡的怪物，准备战斗''',
		2421:'''你战胜了怪物，并获得了它的宝藏''',
		2422:'''你被怪物击败了，慌忙中后退了数步''',
		2423:'''你在路边捡到了一些零碎东西''',
		2424:'''你不慎踩到陷阱，被强大力量拉扯着后退数步''',
		2425:'''你遇到了几个捣乱的妖物，准备战斗''',
		2426:'''你误中诅咒，下次获取的银币数量将减半''',
		2427:'''你不慎触发了一个阵法，生命和真气都被抽空了''',
		2428:'''你不慎触发了一个阵法并被其抽走了#C025%#n的探宝积分''',
		2429:'''你触发了陷阱，下一次投掷骰子结果必定为#C021#n''',
		2430:'''你的探宝积分已达#C02$number#n，获得了丰厚的探宝奖励''',
		2431:'''你被传送到了起点，请重新探索一次吧！''',
		2432:'''你已进入宝物之地，点击#C02上方骰子#n则可开始探索寻宝''',
		2433:'''你入门时日太短，还不足以前往探宝。\n#C04（低于25级玩家无法参与探宝活动）#n''',
		2434:'''你已完成今天的幸运探宝，请于明天再来吧！''',
	}

	branchInfo = {
	}

	fightInfo = {
		1001:(
			{"类型":1,"名称":"宝藏看守者","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1001","数量":"1","技能":(5406,5416,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3004(0,1,0,0,0)","染色":"0,2,0,0,0","能力编号":"1002","数量":"2","技能":(5401,),"站位":(2,3,)},
			{"类型":0,"名称":"妖道","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1003","数量":"2","技能":(5411,),"站位":(4,5,)},
		),
		1002:(
			{"类型":1,"名称":"宝藏看守者","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1001","数量":"1","技能":(5407,5417,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3005(0,1,0,0,0)","染色":"0,2,0,0,0","能力编号":"1002","数量":"2","技能":(5402,),"站位":(2,3,)},
			{"类型":0,"名称":"妖道","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1003","数量":"2","技能":(5412,),"站位":(4,5,)},
		),
		1003:(
			{"类型":1,"名称":"宝藏看守者","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1001","数量":"1","技能":(5408,5418,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3006(0,1,0,0,0)","染色":"0,2,0,0,0","能力编号":"1002","数量":"2","技能":(5403,),"站位":(2,3,)},
			{"类型":0,"名称":"妖道","造型":"4506(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1003","数量":"2","技能":(5413,),"站位":(4,5,)},
		),
		1004:(
			{"类型":1,"名称":"宝藏看守者","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1001","数量":"1","技能":(5409,5419,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3007(0,1,0,0,0)","染色":"0,2,0,0,0","能力编号":"1002","数量":"2","技能":(5404,),"站位":(2,3,)},
			{"类型":0,"名称":"妖道","造型":"4508(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1003","数量":"2","技能":(5414,),"站位":(4,5,)},
		),
		1005:(
			{"类型":1,"名称":"宝藏看守者","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1001","数量":"1","技能":(5410,5420,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3008(0,1,0,0,0)","染色":"0,2,0,0,0","能力编号":"1002","数量":"2","技能":(5405,),"站位":(2,3,)},
			{"类型":0,"名称":"妖道","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1003","数量":"2","技能":(5415,),"站位":(4,5,)},
		),
		1006:(
			{"类型":1,"名称":"宝藏看守者","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1001","数量":"1","技能":(5406,5416,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3009(0,1,0,0,0)","染色":"0,2,0,0,0","能力编号":"1002","数量":"2","技能":(5401,),"站位":(2,3,)},
			{"类型":0,"名称":"妖道","造型":"4504(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1003","数量":"2","技能":(5411,),"站位":(4,5,)},
		),
		1007:(
			{"类型":1,"名称":"宝藏看守者","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1001","数量":"1","技能":(5407,5417,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3004(0,1,0,0,0)","染色":"0,2,0,0,0","能力编号":"1002","数量":"2","技能":(5402,),"站位":(2,3,)},
			{"类型":0,"名称":"妖道","造型":"4506(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"1003","数量":"2","技能":(5412,),"站位":(4,5,)},
		),
		2001:(
			{"类型":1,"名称":"妖兽首领","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2001","数量":"1","技能":(1321,1512,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3004(0,1,0,0,0)","染色":"0,3,0,0,0","能力编号":"2002","数量":"2","技能":(5401,),"站位":(2,3,)},
			{"类型":0,"名称":"妖兽","造型":"3005(0,1,0,0,0)","染色":"0,3,0,0,0","能力编号":"2003","数量":"2","站位":(4,5,)},
		),
		2002:(
			{"类型":1,"名称":"妖兽首领","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2001","数量":"1","技能":(1321,1512,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3006(0,1,0,0,0)","染色":"0,3,0,0,0","能力编号":"2002","数量":"2","技能":(5401,),"站位":(2,3,)},
			{"类型":0,"名称":"妖兽","造型":"3007(0,1,0,0,0)","染色":"0,3,0,0,0","能力编号":"2003","数量":"2","站位":(4,5,)},
		),
		2003:(
			{"类型":1,"名称":"妖兽首领","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0","能力编号":"2001","数量":"1","技能":(1321,1512,),"站位":(1,)},
			{"类型":0,"名称":"妖兽","造型":"3008(0,1,0,0,0)","染色":"0,3,0,0,0","能力编号":"2002","数量":"2","技能":(5401,),"站位":(2,3,)},
			{"类型":0,"名称":"妖兽","造型":"3009(0,1,0,0,0)","染色":"0,3,0,0,0","能力编号":"2003","数量":"2","站位":(4,5,)},
		),
	}

	ableInfo = {
		1001:{"等级":"LV","生命":"B*0.98","真气":"B*1","物理伤害":"B*0.81","法术伤害":"B*0.81","物理防御":"B*0.6","法术防御":"B*0.6","速度":"B*0.8","治疗强度":"B*0.56","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1002:{"等级":"LV","生命":"B*0.75","真气":"B*1","物理伤害":"B*0.45","法术伤害":"B*0.65","物理防御":"B*0.39","法术防御":"B*0.56","速度":"B*0.64","治疗强度":"B*0.45","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1003:{"等级":"LV","生命":"B*0.75","真气":"B*1","物理伤害":"B*0.65","法术伤害":"B*0.45","物理防御":"B*0.56","法术防御":"B*0.39","速度":"B*0.64","治疗强度":"B*0.45","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2001:{"等级":"LV+1","生命":"B*1.13","真气":"B*1","物理伤害":"B*0.97","法术伤害":"B*0.97","物理防御":"B*0.72","法术防御":"B*0.72","速度":"B*0.96","治疗强度":"B*0.67","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2002:{"等级":"LV","生命":"B*0.98","真气":"B*1","物理伤害":"B*0.56","法术伤害":"B*0.81","物理防御":"B*0.49","法术防御":"B*0.7","速度":"B*0.8","治疗强度":"B*0.56","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		2003:{"等级":"LV","生命":"B*0.98","真气":"B*1","物理伤害":"B*0.81","法术伤害":"B*0.56","物理防御":"B*0.7","法术防御":"B*0.49","速度":"B*0.8","治疗强度":"B*0.56","封印命中":"B*0","抵抗封印":"B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}

	lineupInfo = {
	}

	sceneInfo = {
		101:{"名称":"探宝","资源":1140},
	}

	configInfo = {
		1001:2,
		1002:10,
		1003:10,
		1004:4,
		1005:400,
		1006:1200,
		1007:1900,
		1008:2500,
		1009:3000,
		1010:1,
		1011:2,
		1012:3,
		1013:10,
		1014:30,
		1015:6,
		1016:25,
	}

	eventPoint = {
		1:{"坐标":[20,3],"移动方向":2},
		2:{"坐标":[25,4],"移动方向":3},
		3:{"坐标":[30,5],"移动方向":4},
		4:{"坐标":[34,6],"移动方向":5},
		5:{"坐标":[39,7],"移动方向":6},
		6:{"坐标":[44,8],"移动方向":7},
		7:{"坐标":[49,8],"移动方向":8},
		8:{"坐标":[54,7],"移动方向":9},
		9:{"坐标":[58,9],"移动方向":10},
		10:{"坐标":[57,11],"移动方向":11},
		11:{"坐标":[60,13],"移动方向":12},
		12:{"坐标":[62,16],"移动方向":13},
		13:{"坐标":[61,19],"移动方向":14},
		14:{"坐标":[60,23],"移动方向":15},
		15:{"坐标":[58,25],"移动方向":16},
		16:{"坐标":[51,25],"移动方向":17},
		17:{"坐标":[47,27],"移动方向":18},
		18:{"坐标":[52,30],"移动方向":19},
		19:{"坐标":[51,33],"移动方向":20},
		20:{"坐标":[46,35],"移动方向":21},
		21:{"坐标":[44,38],"移动方向":22},
		22:{"坐标":[49,40],"移动方向":23},
		23:{"坐标":[55,41],"移动方向":24},
		24:{"坐标":[58,44],"移动方向":25},
		25:{"坐标":[54,47],"移动方向":26},
		26:{"坐标":[48,48],"移动方向":27},
		27:{"坐标":[52,51],"移动方向":28},
		28:{"坐标":[54,56],"移动方向":29},
		29:{"坐标":[55,59],"移动方向":30},
		30:{"坐标":[61,65],"移动方向":31},
		31:{"坐标":[65,67],"移动方向":32},
		32:{"坐标":[62,70],"移动方向":33},
		33:{"坐标":[56,71],"移动方向":34},
		34:{"坐标":[33,57],"移动方向":35},
		35:{"坐标":[28,56],"移动方向":36},
		36:{"坐标":[26,53],"移动方向":37},
		37:{"坐标":[23,49],"移动方向":38},
		38:{"坐标":[18,47],"移动方向":39},
		39:{"坐标":[16,44],"移动方向":40},
		40:{"坐标":[13,41],"移动方向":41},
		41:{"坐标":[9,38],"移动方向":42},
		42:{"坐标":[8,35],"移动方向":43},
		43:{"坐标":[9,31],"移动方向":44},
		44:{"坐标":[11,27],"移动方向":45},
		45:{"坐标":[15,24],"移动方向":46},
		46:{"坐标":[11,20],"移动方向":1},
	}
#导表结束

	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.state = 0 # 活动状态, 0.已结束  1.进行中
		self.treasureInfoList = {} # 探宝信息列表
		self.pointInfo = {} # 探宝点-事件
		self.pointsList = [] # 事件点列表

	def getPointsList(self):
		'''事件点列表
		'''
		if not self.pointsList:
			self.pointsList = self.eventPoint.keys()
			self.pointsList.sort()
		if len(self.pointsList) < 2:
			raise Exception, "事件点配置出错"
		return self.pointsList

	def getPointConfig(self, idx, key, default=0):
		'''事件点配置信息
		'''
		if not idx in self.getPointsList():
			raise Exception, "事件点{}配置信息不存在".format(idx)
		return self.eventPoint[idx].get(key, default)

	def getStartPoint(self):
		'''起点
		'''
		return self.getPointsList()[0]

	def getTerminal(self):
		'''终点
		'''
		return self.getPointsList()[-1]

	def getBoxAmount(self):
		'''宝箱数量
		'''
		amount = 0
		amount += self.rewardInfo[2001].get("数量", 0)
		amount += self.rewardInfo[2002].get("数量", 0)
		amount += 1 # 通关宝箱
		return amount

	def initEventPoint(self):
		'''初始化事件点
		'''
		lEvent = [] # 事件列表
		for eventIdx, rewardInfo in self.rewardInfo.iteritems():
			eventCnt = rewardInfo.get("数量", 0)
			if eventCnt < 1:
				continue
			lEvent.extend([eventIdx] * eventCnt)
		lEvent = shuffleList(lEvent)
		lEvent.insert(0, 1001) # 起点
		lEvent.append(2003) # 终点
		self.pointInfo = {}
		for point in self.getPointsList():
			eventIdx = lEvent[point-1]
			self.pointInfo[point] = eventIdx

	def createScene(self, sceneIdx):
		'''创建虚拟场景
		'''
		info = self.getSceneInfo(sceneIdx)
		sceneObj = scene.new("活动", 0, info["名称"], info["资源"], info.get("小地图资源", 0), broadcastRole=1)
		sceneObj.idx = sceneIdx
		return sceneObj

	def init(self):
		sceneObj = self.addScene(101)
		sceneObj.eventOnEnter += onEnter
		sceneObj.eventOnLeave += onLeave
		sceneObj.denyTeam = "幸运探宝"
		sceneObj.denyTransfer = self.getText(2409)
		self.initEventPoint()

	def enterScene(self, who):
		'''进入探宝
		'''
		sceneObj = self.getGameScene()
		if not sceneObj:
			raise Exception, "探宝场景不存在"
		who.setTreasure()
		info = self.createTreasureInfo(who)
		curGrid = info["curGrid"]
		x, y = self.getPointConfig(curGrid, "坐标", [-1, -1])
		self.transfer(who, sceneObj.id, x, y)
		message.tips(who, self.getText(2432))
		self.updateRoleCnt()

	def leaveScene(self, who):
		'''离开探宝
		'''
		who.setTreasure(False)
		sceneId, x, y = who.getLastRealPos()
		self.transfer(who, sceneId, x, y)
		self.updateRoleCnt()

	def randomMove(self, who, step):
		'''随机步数移动
		'''
		info = self.getTreasureInfo(who.id)
		backMove = False
		if step > 0:
			who.addCubeCount(1)
			eventDone = False
		else:
			backMove = True
			eventDone = True
		response = self.checkNextGrid
		curGrid = info.get("curGrid", 1)
		midGrid = curGrid + (-1 if backMove else 1)
		nextGrid = max(curGrid + step, self.getStartPoint())
		nextGrid = min(nextGrid, self.getTerminal())
		self.updateTreasureInfo(who, True, curGrid=curGrid, nextGrid=nextGrid, eventDone=eventDone, midGrid=midGrid, backMove=backMove)
		sceneObj = self.getGameScene()
		x, y = self.getPointConfig(midGrid, "坐标", [-1, -1])
		scene.walkToPos(who, sceneObj.id, x, y, response)

	def moveStepByStep(self, who, midGrid):
		'''一步步移动
		'''
		sceneObj = self.getGameScene()
		x, y = self.getPointConfig(midGrid, "坐标", [-1, -1])
		scene.walkToPos(who, sceneObj.id, x, y, self.checkNextGrid)

	def checkNextGrid(self, who):
		'''检查是否到达目标点
		'''
		info = self.getTreasureInfo(who.id)
		nextGrid = info.get("nextGrid")
		midGrid = info.get("midGrid")
		backMove = info.get("backMove")
		if nextGrid != midGrid:
			midGrid += -1 if backMove else 1
			self.moveStepByStep(who, midGrid)
			info["midGrid"] = midGrid
		else:
			info["midGrid"] = 0
			if info.get("backMove"):
				self.doneEvent(who)
			else:
				self.triggerEvent(who)

	def getProgress(self, grid):
		'''进度
		'''
		ttPoint = len(self.getPointsList()) - 1
		surplus = grid - self.getStartPoint()
		pg = int(100 *surplus / ttPoint)
		return pg

	def triggerEvent(self, who):
		'''触发事件
		'''
		nextGrid = self.getNextGrid(who)
		if not nextGrid:
			return
		if self.isPointFinish(who, nextGrid):
			pg = self.getProgress(nextGrid)
			self.updateTreasureInfo(who, True, curGrid=nextGrid, nextGrid=0, eventDone=True, progress=pg)
			if nextGrid == self.getTerminal():
				self.timerMgr.run(functor(self.backToStart, who.id), 3, 0, "treasure_%s"%(who.id))
			return
		eventIdx = self.pointInfo.get(nextGrid)
		if not eventIdx:
			raise Exception, "{}格子事件不存在".format(nextGrid)
		func = eventHandlerList.get(eventIdx)
		if not func:
			raise Exception("触发事件时，找不到对应的处理函数:%s" % eventIdx)
		func(self, who)

	def doneEvent(self, who, isFinish=True):
		'''完成事件
		'''
		nextGrid = self.getNextGrid(who)
		if not nextGrid:
			return
		eventIdx = self.pointInfo.get(nextGrid)
		pg = self.getProgress(nextGrid)
		info = self.getTreasureInfo(who.id)
		doneList = info.get("doneList", set())
		box = info.get("box", 0)
		if isFinish:
			if not info.get("bossFail"):
				self.addTreasurePoint(who, eventIdx)
			doneList.add(nextGrid)
			if eventIdx in (2001, 2002, 2003):
				box -= 1
		self.updateTreasureInfo(who, True, curGrid=nextGrid, nextGrid=0, eventDone=True, progress=pg, box=box, bossFail=False, backMove=False)

	def isEventDone(self, who):
		'''事件是否完成
		'''
		info = self.getTreasureInfo(who.id)
		eventDone = info.get("eventDone", False)
		return eventDone

	def isPointFinish(self, who, grid):
		'''该格子事件是否已完成
		'''
		info = self.getTreasureInfo(who.id)
		doneList = info.get("doneList", set())
		return grid in doneList

	def treasurePointReward(self, who):
		'''积分奖励
		'''
		score = who.day.fetch("treasureP")
		dScoreReward = {400:3001, 1200:3002, 1900:3003, 2500:3004, 3000:3005}
		scoreList = dScoreReward.keys()
		scoreList.sort()
		info = self.getTreasureInfo(who.id)
		if info["scoreCnt"] >= len(scoreList):
			return
		value = scoreList[info["scoreCnt"]]
		if value > score:
			return
		info["scoreCnt"] += 1
		self.rewardProps(who, dScoreReward[value])
		txt = self.getText(2430).replace("$number", str(value))
		tipsAndMessage(who, txt)

	def addTreasurePoint(self, who, eventIdx):
		'''增加积分
		'''
		s = self.rewardInfo[eventIdx].get("探宝积分", 0)
		if not s:
			return
		dp = who.day.add("treasureP", s)
		wp = who.week.fetch("treasureP")
		message.message(who, "你在探索中获得了#C07{}#n探宝积分".format(s))
		self.treasurePointReward(who)
		if dp > wp:
			who.week.set("treasureP", dp)
			rank.updateTreasurePointRank(who)

	def getNextGrid(self, who):
		'''获取角色下一个事件点
		'''
		info = self.getTreasureInfo(who.id)
		nextGrid = info.get("nextGrid")
		return nextGrid

	def getTreasureInfo(self, roleId):
		'''获取探宝信息
		'''
		return self.treasureInfoList.get(roleId)

	def createTreasureInfo(self, who):
		'''创建探宝信息
		'''
		roleId = who.id
		treasureInfo = self.treasureInfoList.get(roleId)
		if not treasureInfo:
			treasureInfo = {
				"progress": 0, # 进度
				"box": self.getBoxAmount(), # 剩余宝箱
				"curGrid": self.getStartPoint(), # 当前格子
				"nextGrid": 0, # 下一格子
				"midGrid": 0, # 中间经过的格子
				"eventDone": True, # 事件完成
				"stepOne": False, # 投骰子必定为1
				"doneList": set(), # 完成事件的点列表
				"rewardList": set(), # 领取过的积分奖励
				"scoreCnt": 0, # 积分奖励领取次数
			}
			self.treasureInfoList[roleId] = treasureInfo
		return treasureInfo

	def updateTreasureInfo(self, who, refresh=True, **attrList):
		'''更新探宝信息
		'''
		treasureInfo = self.treasureInfoList.get(who.id)
		if not treasureInfo:
			return
		for attrName, attrVal in attrList.iteritems():
			treasureInfo[attrName] = attrVal
		if refresh:
			rpcTreasureInfo(who)
			rpcTreasureEventPoints(who)

	def rewardByMail(self, roleId, title, content, rwdIdx, validTime):
		'''通过邮件发奖励
		'''
		propsObjList = []
		info = self.getRewardPropsInfo(rwdIdx)
		idx = chooseKey(info, key="权重")
		if idx is None:
			return
		info = info[idx]
		if info["物品"] in ("", "0",):
			return
		propsNo, args, kwargs = misc.parseItemInfo(info["物品"])
		amount = int(self.transCodeForReward(info["数量"], "数量"))
		binded = info.get("绑定", 0)
		propsNo = self.transIdxByGroup(propsNo)
		propsObj = props.new(propsNo)
		if propsObj.isVirtual():
			propsObj.setValue(amount)
		else:
			propsObj.setStack(amount)
			if binded:
				propsObj.bind()
		propsObjList.append(propsObj)
		mail.sendSysMail(roleId, title, content, propsObjList, 0)

	def rankReward(self):
		'''排行榜奖励
		'''
		rankObj = rank.getRankObjByName("rank_treasure_point")
		lRank = rankObj.ranking()[:30]
		for idx, roleId in enumerate(lRank):
			if idx == 0:
				rewardIdx = 2001
			elif idx == 1:
				rewardIdx = 2002
			elif idx == 2:
				rewardIdx = 2003
			elif idx < 10:
				rewardIdx = 2004
			elif idx < 30:
				rewardIdx = 2005
			title = "探宝排行周奖励"
			content = "恭喜你在上周探宝排行中获得第{}名，这是给你的奖励".format(idx+1)
			self.rewardByMail(roleId, title, content, rewardIdx, 0)

	def clearRank(self):
		'''清空排行榜
		'''
		rankObj = rank.getRankObjByName("rank_treasure_point")
		rankObj.clearRank()

	def resetTreasure(self):
		'''重置探宝事件
		'''
		self.clearForEnd()
		self.initEventPoint()

	def resetNotify(self):
		'''重置通知
		'''
		self.timerMgr.run(self.resetNotify, 60, 0, "resetNotify")
		txt = self.getText(2407).replace("$time", str(60-getDatePart(partName="minute")))
		sceneObj = self.getGameScene()
		for roleId in sceneObj.getRoleList():
			message.tips(roleId, txt)

	def onNewHour(self, day, hour, wday):
		'''刷小时
		'''
		if hour == 23:
			self.timerMgr.run(self.resetNotify, 3000, 0, "resetNotify")
		elif hour == 0:
			self.resetTreasure()

	def onNewWeek(self, year, month, day, hour, wday):
		'''刷周
		'''
		self.rankReward()
		self.clearRank()

	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 100:
			txtList = []
			txtList.append("101-进入探宝")
			txtList.append("102-退出探宝")
			txtList.append("103-投骰子")
			message.dialog(who, "\n".join(txtList))
		elif cmdIdx == 101:
			self.enterScene(who)
		elif cmdIdx == 102:
			rpcTreasureQuit(who, None)
		elif cmdIdx == 103:
			rpcTreasureCubeThrow(who, None)
		elif cmdIdx == 104:
			rpcTreasureInfo(who)
		elif cmdIdx == 105:
			self.resetNotify()
		elif cmdIdx == 106:
			if self.timerMgr.hasTimerId("resetNotify"):
				self.timerMgr.cancel("resetNotify")
		elif cmdIdx == 107:
			answerObj = answer.getAnswerTreasureObj()
			answerObj.openAnswerTreasure(who, 7)
		elif cmdIdx == 108:
			self.backToStart(who.id)
		elif cmdIdx == 109:
			self.resetTreasure()
		elif cmdIdx == 110:
			self.initEventPoint()

	def getGameScene(self):
		'''活动场景
		'''
		return self.getSceneByIdx(101)
		
	def inGameScene(self, who):
		'''是否在活动场景
		'''
		sceneObj = self.getGameScene()
		if sceneObj and sceneObj.id == who.sceneId:
			return True
		return False

	def clearForEnd(self):
		'''结束清场
		'''
		if self.timerMgr.hasTimerId("resetNotify"):
			self.timerMgr.cancel("resetNotify")
		self.treasureInfoList = {}
		sceneObj = self.getGameScene()
		if not sceneObj:
			return
		for roleId in sceneObj.getRoleList():
			who = getRole(roleId)
			if not who:
				continue
			self.leaveScene(who)
			message.tips(who, self.getText(2410))

	def backToStart(self, pid):
		'''回到起点
		'''
		who = getRole(pid)
		if not who:
			return
		if self.timerMgr.hasTimerId("treasure_%s"%(pid)):
			self.timerMgr.cancel("treasure_%s"%(pid))
		sceneObj = self.getGameScene()
		sp = self.getStartPoint()
		x, y = self.eventPoint[sp]["坐标"]
		if self.inGameScene(who):
			scene.switchScene(who, sceneObj.id, x, y)
			message.tips(who, self.getText(2431))
			self.updateTreasureInfo(who, True, curGrid=sp, nextGrid=0, progress=0)

	def getRoleCnt(self):
		'''获取场景人数
		'''
		sceneObj = self.getGameScene()
		if not sceneObj:
			return 0
		return len(sceneObj.getRoleList())

	def onWarWin(self, warObj, npcObj, w):
		who = getRole(w.id)
		if not who:
			return
		nextGrid = self.getNextGrid(who)
		if not nextGrid:
			return
		eventIdx = self.pointInfo.get(nextGrid)
		if eventIdx == 3001:
			self.doScript(who, None, "R3001")
		elif eventIdx == 4001:
			self.doScript(who, None, "R9001")
		self.doneEvent(who)

	def onWarFail(self, warObj, npcObj, w):
		'''战斗失败时
		'''
		who = getRole(w.id)
		if not who:
			return
		nextGrid = self.getNextGrid(who)
		if not nextGrid:
			return
		eventIdx = self.pointInfo.get(nextGrid)
		if eventIdx == 3001:
			message.tips(who, self.getText(2422))
			info = self.getTreasureInfo(who.id)
			self.updateTreasureInfo(who, False, bossFail=True, curGrid=info["nextGrid"], nextGrid=0)
			step = rand(1, 6)
			self.randomMove(who, -step)
		else:
			self.doneEvent(who)

	def updateRoleCnt(self):
		sceneObj = self.getGameScene()
		for roleId in sceneObj.getRoleList():
			who = getRole(roleId)
			if not who:
				continue
			rpcTreasureInfo(who)
		
	def calCubeCountMax(self, who):
		'''计算骰子次数上限
		'''
		actPoint = who.day.fetch("actPoint", iWhichCyc=-1)
		initCube = self.configInfo.get(1003, 15) # 每日初始点
		perActAdd = self.configInfo.get(1004, 40) # 区间活跃点增加
		return initCube + actPoint / perActAdd

	def rewardExp(self, who, val):
		'''奖励角色经验
		'''
		roleId = who.id
		roleCnt = self.getRoleCnt()
		expPercent = self.configInfo.get(1001, 1)
		maxPercent = self.configInfo.get(1002, 5)
		addPer = min(expPercent * roleCnt / 100, maxPercent)
		val += int(val * addPer / 100.0)
		who.rewardExp(val, self.name)
		self.tmpReward[roleId]["经验"].append(val)

	def rewardCash(self, who, val):
		'''奖励银币
		'''
		info = self.getTreasureInfo(who.id)
		if info.get("cashHalf"):
			val /= 2
			info["cashHalf"] = None
		roleId = who.id
		who.rewardCash(val, self.name)
		self.tmpReward[roleId]["银币"].append(val)


def getActivity():
	return activity.getActivity("treasure")

def onEnter(who, oldScene, newScene):
	'''进入活动场景时
	'''
	if oldScene is newScene:
		return
	rpcTreasureStatus(who, 1)
	rpcTreasureInfo(who)
	rpcTreasureEventPoints(who)
	checkTreasureStatus(who)

def onLeave(who, oldScene, newScene):
	'''离开活动场景时
	'''
	if oldScene is newScene:
		return
	rpcTreasureStatus(who, 2)


# ================================================================
# 客户端发往服务端
# ================================================================
def validReceive(who):
	'''检查接收数据
	'''
	actObj = getActivity()
	if not actObj:
		return None
	if not actObj.inGameScene(who):
		return None
	if who.inWar():
		return None
	return actObj

def rpcTreasureQuit(who, reqMsg):
	'''退出探宝
	'''
	actObj = validReceive(who)
	if not actObj:
		return
	actObj.leaveScene(who)

def rpcTreasureRankGet(who, reqMsg):
	'''查看探宝排行榜
	'''
	message.tips(who, "查看探宝排行榜")

def rpcTreasureCubeThrow(who, reqMsg):
	'''投骰子
	'''
	actObj = validReceive(who)
	if not actObj:
		return
	info = actObj.getTreasureInfo(who.id)
	if not info or who.getLeftCubeCount() < 1:
		message.tips(who, actObj.getText(2412))
		return
	if info["curGrid"] == actObj.getTerminal():
		actObj.backToStart(who.id)
		return
	if not actObj.isEventDone(who):
		message.tips(who, actObj.getText(2413))
		# actObj.triggerEvent(who)
		return
	stepOne = info.get("stepOne", False)
	if stepOne:
		actObj.updateTreasureInfo(who, False, stepOne=False)
		step = 1
	else:
		step = rand(1, 6)
	who.endPoint.rpcTreasureCubeResult(step)
	actObj.updateTreasureInfo(who, False, step=step)

def rpcTreasureEffectDone(who, reqMsg):
	'''特效播放完毕
	'''
	actObj = validReceive(who)
	if not actObj:
		return
	info = actObj.getTreasureInfo(who.id)
	if not info:
		return
	if reqMsg.iValue != 1:
		return
	step = info.get("step")
	if not step:
		return
	text = actObj.getText(2411).replace("$number", str(step))
	message.tips(who, text)
	actObj.randomMove(who, step)
	cnt = who.getCubeCount()
	perPoint = activity.center.getPerActPoint(14)
	cntMax = activity.center.getCntMax(14)
	if cnt <= cntMax:
		who.addActPoint(perPoint)


#===============================================================================
# 服务端发往客户端
#===============================================================================
def rpcTreasureInfo(who):
	'''探宝信息
	'''
	actObj = getActivity()
	if not actObj:
		return
	info = actObj.getTreasureInfo(who.id)
	if not info:
		return
	msg = act_treasure_pb2.treasureInfo()
	msg.cubeCnt = who.getLeftCubeCount()
	msg.score = who.day.fetch("treasureP")
	msg.box = max(0, info["box"])
	msg.progress = info["progress"]
	msg.roleCnt = actObj.getRoleCnt()
	who.endPoint.rpcTreasureInfo(msg)

def rpcTreasureRankInfo(who):
	'''排行榜信息
	'''
	pass

def rpcTreasureStatus(who, status):
	who.endPoint.rpcTreasureStatus(status)

def rpcTreasureEventPoints(who):
	actObj = getActivity()
	if not actObj:
		return
	info = actObj.getTreasureInfo(who.id)
	doneList = info.get("doneList", set())
	msg = act_treasure_pb2.eventPointInfo()
	eps = []
	for k, v in actObj.pointInfo.iteritems():
		epMsg = act_treasure_pb2.eventInfo()
		epMsg.iPoint = k
		epMsg.iEventIdx = v if k not in doneList else 1001
		eps.append(epMsg)
	msg.points.extend(eps)
	who.endPoint.rpcTreasureEventPoints(msg)


#==================================================
# 事件处理逻辑
#==================================================
def checkTreasureStatus(who):
	'''玩家探宝状态检查
	主要是应付各种异常操作：断线、重连、寻路中退出
	'''
	actObj = getActivity()
	if not actObj:
		return
	info = actObj.getTreasureInfo(who.id)
	actObj.checkNextGrid(who)

def tipsAndMessage(who, content):
	message.tips(who, content)
	message.message(who, content)

def eventNone(actObj, who):
	content = actObj.getText(2414)
	tipsAndMessage(who, content)
	actObj.doneEvent(who)
	actObj.doScript(who, None, "R1001")

def eventBox(actObj, who):
	content = actObj.getText(2415)
	tipsAndMessage(who, content)
	actObj.doneEvent(who)
	actObj.doScript(who, None, "R2001")

def eventAnswer(actObj, who):
	content = actObj.getText(2416)
	tipsAndMessage(who, content)
	answerObj = answer.getAnswerTreasureObj()
	answerType = actObj.configInfo.get(1015, 7) # 题库类型
	answerObj.openAnswerTreasure(who, answerType)

def eventPass(actObj, who):
	content = actObj.getText(2419)
	tipsAndMessage(who, content)
	actObj.timerMgr.run(functor(actObj.backToStart, who.id), 3, 0, "treasure_%s"%(who.id))
	actObj.doScript(who, None, "R2003")
	actObj.doneEvent(who)

def eventBoss(actObj, who):
	content = actObj.getText(2420)
	tipsAndMessage(who, content)
	actObj.doScript(who, None, "F9001")

def eventRandom(actObj, who):
	eventIdx = chooseKey(randomEventRatio)
	if not eventIdx:
		raise Exception, "找不到随机事件序号"
	func = randomEventHandlerList.get(eventIdx)
	if not func:
		raise Exception, "触发随机事件时，找不到对应的处理函数:%s" % eventIdx
	func(actObj, who)

def randomEventBack(actObj, who):
	content = actObj.getText(2424)
	tipsAndMessage(who, content)
	info = actObj.getTreasureInfo(who.id)
	actObj.updateTreasureInfo(who, False, curGrid=info["nextGrid"], nextGrid=0)
	step = rand(1, 6)
	actObj.randomMove(who, -step)

def randomEventMonster(actObj, who):
	content = actObj.getText(2425)
	tipsAndMessage(who, content)
	actObj.doScript(who, None, "F9002")

def randomEventCash(actObj, who):
	content = actObj.getText(2426)
	tipsAndMessage(who, content)
	info = actObj.getTreasureInfo(who.id)
	info["cashHalf"] = True
	actObj.doneEvent(who)
	# TODO

def randomEventHPMP(actObj, who):
	content = actObj.getText(2427)
	tipsAndMessage(who, content)
	who.hp = 1
	who.mp = 1
	who.recover(True)
	# who.attrChange('hp','mp')
	actObj.doneEvent(who)

def randomEventScore(actObj, who):
	content = actObj.getText(2428)
	tipsAndMessage(who, content)
	info = actObj.getTreasureInfo(who.id)
	score = who.day.fetch("treasureP")
	score = int(score * 0.95)
	who.day.set("treasureP", score)
	actObj.doneEvent(who)

def randomEventStep(actObj, who):
	content = actObj.getText(2429)
	tipsAndMessage(who, content)
	actObj.updateTreasureInfo(who, False, stepOne=True)
	actObj.doneEvent(who)

def randomEventBonus(actObj, who):
	content = actObj.getText(2423)
	tipsAndMessage(who, content)
	actObj.doneEvent(who)
	actObj.doScript(who, None, "R4001")

eventHandlerList = {
	1001: eventNone,
	2001: eventBox,
	2002: eventAnswer,
	2003: eventPass,
	3001: eventBoss,
	4001: eventRandom,
}

randomEventRatio = {
	1: 50,
	2: 75,
	3: 50,
	4: 75,
	5: 50,
	6: 250,
	7: 450,
}

randomEventHandlerList = {
	1: randomEventBack,
	2: randomEventMonster,
	3: randomEventCash,
	4: randomEventHPMP,
	5: randomEventScore,
	6: randomEventStep,
	7: randomEventBonus,
}

from common import *
import activity
import activity.center
import message
import act_treasure_pb2
import rank
import scene
import answer
import mail
import props
import misc
