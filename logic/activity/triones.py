# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity
'''北斗七星
'''

gbTrionesDebug = False

#导表开始
class Activity(customActivity):

	npcInfo = {
		1001:{"名称":"贪狼星君","造型":"4006(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"$rpos","称谓":"天枢"},
		1002:{"名称":"巨门星君","造型":"4007(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"$rpos","称谓":"天璇"},
		1003:{"名称":"禄存星君","造型":"4508(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"$rpos","称谓":"天玑"},
		1004:{"名称":"文曲星君","造型":"4003(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"$rpos","称谓":"天权"},
		1005:{"名称":"廉贞星君","造型":"4002(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"$rpos","称谓":"玉衡"},
		1006:{"名称":"武曲星君","造型":"4001(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"$rpos","称谓":"开阳"},
		1007:{"名称":"破军星君","造型":"4004(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"$rpos","称谓":"瑶光"},
		1008:{"名称":"北斗使者","造型":"2009(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"1130,100,71,6","对白":"4001"},
	}

	eventInfo = {
	}

	rewardInfo = {
		1001:{"经验":lambda LV:LV*170+15000,"宠物经验":lambda PLV:PLV*119+10500,"银币":lambda LV:LV*100+10000,"物品":[1001]},
		1002:{"经验":lambda LV:LV*204+18000,"宠物经验":lambda PLV:PLV*142+12600,"银币":lambda LV:LV*110+11000,"物品":[1001]},
		1003:{"经验":lambda LV:LV*238+21000,"宠物经验":lambda PLV:PLV*166+14700,"银币":lambda LV:LV*120+12000,"物品":[1001]},
		1004:{"经验":lambda LV:LV*272+24000,"宠物经验":lambda PLV:PLV*190+16800,"银币":lambda LV:LV*130+13000,"物品":[1001]},
		1005:{"经验":lambda LV:LV*306+27000,"宠物经验":lambda PLV:PLV*214+18900,"银币":lambda LV:LV*140+14000,"物品":[1001]},
		1006:{"经验":lambda LV:LV*340+30000,"宠物经验":lambda PLV:PLV*238+21000,"银币":lambda LV:LV*150+15000,"物品":[1001]},
		1007:{"经验":lambda LV:LV*374+33000,"宠物经验":lambda PLV:PLV*261+23100,"银币":lambda LV:LV*160+16000,"物品":[1001]},
		1008:{"物品":[1002]},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":100,"物品":"202024","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"202025","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224103","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224103","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224103","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224104","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224104","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224104","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224105","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224105","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224105","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224106","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224106","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224106","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224107","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224107","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224107","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224108","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224201","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224202","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224203","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224204","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":100,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"230101","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"230101","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"230102","数量":"5","绑定":0,"传闻":0},
			{"权重":35,"物品":"234101","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234102","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234103","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234104","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234105","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234106","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234107","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234108","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234109","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234110","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234111","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234112","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234113","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234114","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234115","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234116","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234117","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234118","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234119","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234120","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234121","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234122","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234123","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234124","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234125","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234126","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234127","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234128","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234129","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234130","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234131","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234132","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234133","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234134","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234135","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234136","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234137","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234138","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234139","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234140","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234141","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234142","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234143","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234144","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234145","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234146","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234147","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234148","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234149","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234150","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234151","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234152","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234153","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":35,"物品":"234901","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":50,"物品":"245001","数量":"1","绑定":0,"传闻":0},
			{"权重":80,"物品":"245001","数量":"3","绑定":0,"传闻":0},
			{"权重":80,"物品":"245001","数量":"5","绑定":0,"传闻":0},
			{"权重":50,"物品":"245051","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":5000,"物品":"0","数量":"0","绑定":0,"传闻":0},
		),
		1002:(
			{"权重":100,"物品":"202024","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"202025","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224103","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224103","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224103","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224104","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224104","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224104","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224105","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224105","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224105","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224106","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224106","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224106","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224107","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224107","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"224107","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"224108","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224201","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224202","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224203","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"224204","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":100,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"230101","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"230101","数量":"5","绑定":0,"传闻":0},
			{"权重":100,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":100,"物品":"230102","数量":"5","绑定":0,"传闻":0},
			{"权重":35,"物品":"234101","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234102","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234103","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234104","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234105","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234106","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234107","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234108","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234109","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234110","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234111","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234112","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234113","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234114","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234115","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234116","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234117","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234118","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234119","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234120","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234121","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234122","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234123","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234124","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234125","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234126","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234127","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234128","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234129","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234130","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234131","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234132","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234133","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234134","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234135","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234136","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234137","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234138","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234139","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234140","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234141","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234142","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234143","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234144","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234145","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234146","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234147","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234148","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234149","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234150","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234151","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234152","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234153","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":35,"物品":"234901","数量":"1","绑定":0,"传闻":"SM5002"},
			{"权重":50,"物品":"245001","数量":"1","绑定":0,"传闻":0},
			{"权重":80,"物品":"245001","数量":"3","绑定":0,"传闻":0},
			{"权重":80,"物品":"245001","数量":"5","绑定":0,"传闻":0},
			{"权重":50,"物品":"245051","数量":"1","绑定":0,"传闻":0},
			{"权重":50,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":5000,"物品":"0","数量":"0","绑定":0,"传闻":0},
		),
	}

	groupInfo = {
		9001:(1030,1060,1130,1140,2030,2040,1040,2010,),
	}

	chatInfo = {
		4001:'''北斗七星下凡，有能之士可以在我这里领取任务，击败北斗七星可以获得丰富奖励！''',
		4002:'''没有一定实力是没办法接受北斗七星的考验的，回去潜心修炼#C04等级≥30级#n后再来吧！''',
		4003:'''北斗七星的考验需要你自己去面对，退出组队才能领取考验。''',
		4004:'''1.#C02等级≥30#n才能参加活动，#C02无需组队#n\n2.北斗七星会在任一地图出现，并且同一地图只会出现一个星君\n3.可按任意顺序挑战，全部挑战成功还可获得额外奖励''',
		4005:'''#L1<14,26>*[北斗七星]*02#n下凡游历，仙友们速度去#C03$enpc#n处领取任务寻找并战胜北斗七星获得丰富奖励，据闻在$sceneList出现北斗七星的踪迹''',
		4006:'''我们北斗七星下凡，你们这些修仙之人蜂拥而至，不就为了宝物吗？来吧，我接受你的挑战！''',
		4007:'''我等从不与无名之辈交手，先去#C03$enpc#n那领到任务后再过来吧！''',
		4008:'''你已经通过我的考验并得到奖励了，切忌贪心不足。''',
		4009:'''不敢一个人面对我吗？退出组队再来吧！''',
		4010:'''已有#C02$number#n个玩家进入挑战，已达到星君挑战上限，#C03$monster#n已离开此处''',
		4011:'''#L1<14,26>*[北斗七星]*02#n的下凡时间已结束，北斗七星已全部返回天庭，望各位仙友下次继续踊跃参与''',
		4012:'''北斗七星散落在地图各处，需要你自己去寻找，也可以留意每个半点和整点刷新的怪物位置传闻''',
		4013:'''恭喜你，已通过所有北斗七星的考验，获得通关奖励！''',
		5001:'''#C01$roleName#n在#L1<14,26>*[北斗七星]*02#n中挑战北斗成功，获得北斗认可，获得一个$lnkProps''',
		5002:'''#C01$roleName#n在#L1<14,26>*[北斗七星]*02#n中击败所有北斗七星，北斗七星甘败涂地，献出一个$lnkProps求饶''',
		6001:'''你身上已有任务，快去寻找北斗七星通过它们的考验吧。''',
		6002:'''你本周已完成过北斗七星的考验。''',
		6003:'''北斗七星下凡时间已结束，任务已取消。''',
	}

	branchInfo = {
	}

	fightInfo = {
		1001:(
			{"类型":1,"名称":"贪狼星君","造型":"4006(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1001","数量":"1","技能":(1212,1232,1221,5213,),"站位":(1,)},
			{"类型":0,"名称":"昆仑素女","造型":"3009(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1002","数量":"1","技能":(1621,1631,5108,),"站位":(6,)},
			{"类型":0,"名称":"护法金刚","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1003","数量":"1","技能":(1112,1131,5101,),"站位":(7,)},
			{"类型":0,"名称":"北斗卫兵","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1004","数量":"1","技能":(1531,1521,5102,),"站位":(8,)},
			{"类型":0,"名称":"五仙教徒","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1005","数量":"1","技能":(1421,1412,1432,),"站位":(9,)},
			{"类型":0,"名称":"翩翩公子","造型":"4504(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1006","数量":"1","技能":(1222,1213,1211,),"站位":(10,)},
		),
		1002:(
			{"类型":1,"名称":"巨门星君","造型":"4007(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1001","数量":"1","技能":(1131,1132,5201,5203,),"站位":(1,)},
			{"类型":0,"名称":"昆仑素女","造型":"3009(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1002","数量":"1","技能":(1621,1631,5108,),"站位":(6,)},
			{"类型":0,"名称":"护法金刚","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1003","数量":"1","技能":(1112,1131,5101,),"站位":(7,)},
			{"类型":0,"名称":"北斗卫兵","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1004","数量":"1","技能":(1531,1521,5102,),"站位":(8,)},
			{"类型":0,"名称":"五仙教徒","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1005","数量":"1","技能":(1421,1412,1432,),"站位":(9,)},
			{"类型":0,"名称":"翩翩公子","造型":"4504(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1006","数量":"1","技能":(1222,1213,1211,),"站位":(10,)},
		),
		1003:(
			{"类型":1,"名称":"禄存星君","造型":"4508(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1001","数量":"1","技能":(1612,1621,1623,1631,),"站位":(1,)},
			{"类型":0,"名称":"昆仑素女","造型":"3009(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1002","数量":"1","技能":(1621,1631,5108,),"站位":(6,)},
			{"类型":0,"名称":"护法金刚","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1003","数量":"1","技能":(1112,1131,5101,),"站位":(7,)},
			{"类型":0,"名称":"北斗卫兵","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1004","数量":"1","技能":(1531,1521,5102,),"站位":(8,)},
			{"类型":0,"名称":"五仙教徒","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1005","数量":"1","技能":(1421,1412,1432,),"站位":(9,)},
			{"类型":0,"名称":"翩翩公子","造型":"4504(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1006","数量":"1","技能":(1222,1213,1211,),"站位":(10,)},
		),
		1004:(
			{"类型":1,"名称":"文曲星君","造型":"4003(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1001","数量":"1","技能":(1213,1221,1222,1233,),"站位":(1,)},
			{"类型":0,"名称":"昆仑素女","造型":"3009(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1002","数量":"1","技能":(1621,1631,5108,),"站位":(6,)},
			{"类型":0,"名称":"护法金刚","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1003","数量":"1","技能":(1112,1131,5101,),"站位":(7,)},
			{"类型":0,"名称":"北斗卫兵","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1004","数量":"1","技能":(1531,1521,5102,),"站位":(8,)},
			{"类型":0,"名称":"五仙教徒","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1005","数量":"1","技能":(1421,1412,1432,),"站位":(9,)},
			{"类型":0,"名称":"翩翩公子","造型":"4504(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1006","数量":"1","技能":(1222,1213,1211,),"站位":(10,)},
		),
		1005:(
			{"类型":1,"名称":"廉贞星君","造型":"4002(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1001","数量":"1","技能":(1412,1421,1423,1431,),"站位":(1,)},
			{"类型":0,"名称":"昆仑素女","造型":"3009(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1002","数量":"1","技能":(1621,1631,5108,),"站位":(6,)},
			{"类型":0,"名称":"护法金刚","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1003","数量":"1","技能":(1112,1131,5101,),"站位":(7,)},
			{"类型":0,"名称":"北斗卫兵","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1004","数量":"1","技能":(1531,1521,5102,),"站位":(8,)},
			{"类型":0,"名称":"五仙教徒","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1005","数量":"1","技能":(1421,1412,1432,),"站位":(9,)},
			{"类型":0,"名称":"翩翩公子","造型":"4504(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1006","数量":"1","技能":(1222,1213,1211,),"站位":(10,)},
		),
		1006:(
			{"类型":1,"名称":"武曲星君","造型":"4001(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1001","数量":"1","技能":(1512,1521,5210,5213,),"站位":(1,)},
			{"类型":0,"名称":"昆仑素女","造型":"3009(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1002","数量":"1","技能":(1621,1631,5108,),"站位":(6,)},
			{"类型":0,"名称":"护法金刚","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1003","数量":"1","技能":(1112,1131,5101,),"站位":(7,)},
			{"类型":0,"名称":"北斗卫兵","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1004","数量":"1","技能":(1531,1521,5102,),"站位":(8,)},
			{"类型":0,"名称":"五仙教徒","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1005","数量":"1","技能":(1421,1412,1432,),"站位":(9,)},
			{"类型":0,"名称":"翩翩公子","造型":"4504(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1006","数量":"1","技能":(1222,1213,1211,),"站位":(10,)},
		),
		1007:(
			{"类型":1,"名称":"破军星君","造型":"4004(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1001","数量":"1","技能":(1321,1323,5209,5201,),"站位":(1,)},
			{"类型":0,"名称":"昆仑素女","造型":"3009(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1002","数量":"1","技能":(1621,1631,5108,),"站位":(6,)},
			{"类型":0,"名称":"护法金刚","造型":"4005(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1003","数量":"1","技能":(1112,1131,5101,),"站位":(7,)},
			{"类型":0,"名称":"北斗卫兵","造型":"4502(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1004","数量":"1","技能":(1531,1521,5102,),"站位":(8,)},
			{"类型":0,"名称":"五仙教徒","造型":"4509(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1005","数量":"1","技能":(1421,1412,1432,),"站位":(9,)},
			{"类型":0,"名称":"翩翩公子","造型":"4504(0,1,0,0,0)","染色":"0,0,0,0,0,0","能力编号":"1006","数量":"1","技能":(1222,1213,1211,),"站位":(10,)},
		),
	}

	ableInfo = {
		1001:{"等级":"LV","生命":"TF*B*1.02","真气":"TF*B*1","物理伤害":"TF*B*1.1","法术伤害":"TF*B*1.1","物理防御":"TF*B*0.82","法术防御":"TF*B*0.82","速度":"TF*B*1.09","治疗强度":"TF*B*0.76","封印命中":"TF*B*0","抵抗封印":"TF*B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1002:{"等级":"LV","生命":"TF*B*0.9","真气":"TF*B*1","物理伤害":"TF*B*0.67","法术伤害":"TF*B*0.67","物理防御":"TF*B*0.72","法术防御":"TF*B*0.72","速度":"TF*B*0.96","治疗强度":"TF*B*0.96","封印命中":"TF*B*0","抵抗封印":"TF*B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1003:{"等级":"LV","生命":"TF*B*0.9","真气":"TF*B*1","物理伤害":"TF*B*0.97","法术伤害":"TF*B*0.67","物理防御":"TF*B*0.84","法术防御":"TF*B*0.59","速度":"TF*B*0.96","治疗强度":"TF*B*0.67","封印命中":"TF*B*0","抵抗封印":"TF*B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1004:{"等级":"LV","生命":"TF*B*0.9","真气":"TF*B*1","物理伤害":"TF*B*0.67","法术伤害":"TF*B*0.97","物理防御":"TF*B*0.59","法术防御":"TF*B*0.84","速度":"TF*B*0.96","治疗强度":"TF*B*0.67","封印命中":"TF*B*0","抵抗封印":"TF*B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1005:{"等级":"LV","生命":"TF*B*0.9","真气":"TF*B*1","物理伤害":"TF*B*0.97","法术伤害":"TF*B*0.97","物理防御":"TF*B*0.72","法术防御":"TF*B*0.72","速度":"TF*B*1.02","治疗强度":"TF*B*0.67","封印命中":"TF*B*0.8","抵抗封印":"TF*B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1006:{"等级":"LV","生命":"TF*B*0.9","真气":"TF*B*1","物理伤害":"TF*B*0.97","法术伤害":"TF*B*0.97","物理防御":"TF*B*0.72","法术防御":"TF*B*0.72","速度":"TF*B*0.96","治疗强度":"TF*B*0.67","封印命中":"TF*B*0","抵抗封印":"TF*B*0.8","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}

	lineupInfo = {
	}

	sceneInfo = {
	}

	configInfo = {
		"战斗上限":5,
	}

	monsterFactor = {
		1:{"数值系数":0.85},
		2:{"数值系数":0.9},
		3:{"数值系数":0.95},
		4:{"数值系数":1},
		5:{"数值系数":1.05},
		6:{"数值系数":1.1},
		7:{"数值系数":1.15},
	}
#导表结束
	
	def init(self):
		self.reset()
		if self.inNormalTime():
			self.begin()

	def reset(self):
		self.tTempMonsterPos = None
		self.envoyNpcObj = None
		self.trionesMonsterObj = {}
		self.dRandScenePos = {}

	def inNormalTime(self):
		'''是否活动正式时间
		'''
		if gbTrionesDebug:
			return True
		datePart = getDatePart()
		wday = datePart["wday"]
		if wday != 6:
			return False
		return True

	def onNewHour(self, day, hour, wday):
		if wday == 6 and hour == 0:
			self.begin()
		if wday == 1 and hour == 0:
			self.end()

	def transString(self, content, pid=0):	#override
		if "$enpc" in content:
			info = self.getNpcInfo(1008)
			content = content.replace("$enpc", info.get("名称", ""))

		if "$sceneList" in content:
			lTemp = []
			for monsterIdx in xrange(1001,1008):
				lTemp.append("#C03{}#n".format(self.trionesMonsterSceneName(monsterIdx)))
			content = content.replace("$sceneList", "、".join(lTemp))

		return customActivity.transString(self, content, pid)

	def transCode(self, code, _type="", who=None):	#override
		'''数值转化公共接口
		'''
		if isinstance(code, str): # 字符串公式
			if "TF" in code:
				iFactor = 1
				if who:
					#taskObj = task.hasTask(who, task.triones.TRIONES_TASK_PARENT_ID)
					#if taskObj:
					lKillMonster = who.day.fetch("trionesKill", [])
					iFactor = self.monsterFactor.get(len(lKillMonster)+1, {}).get("数值系数", 1)
				code = code.replace("TF", str(iFactor))

		return customActivity.transCode(self, code, _type, who) 

	#===================================================
	#NPC
	def transNpcInfo(self, npcIdx, info, who=None):
		if "$rpos" in info["位置"]:
			if self.tTempMonsterPos:
				sceneId, x, y = self.tTempMonsterPos
				self.tTempMonsterPos = None
			else:
				sceneId, x, y = self.getRandScenePos()
			info["位置"] = "%s,%s,%s,0" % (sceneId, x, y)
		return customActivity.transNpcInfo(self, npcIdx, info, who)

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		if npcIdx == 1008:
			return EnvoyNpc(self)
		elif npcIdx in xrange(1001, 1008):
			return TrionesMonsterNpc(self)
		return customActivity.newNpc(self, npcIdx, name, shape, who)

	def createEnvoyNpc(self):
		'''创建活动使者NPC
		'''
		npcObj = self.addNpc(1008, "envoyNpc")
		self.envoyNpcObj = npcObj

	def removeEnvoyNpc(self):
		'''删除活动使者NPC
		'''
		self.envoyNpcObj = None
		self.removeNpcByTypeFlag("envoyNpc")

	def getEnvoyNpc(self):
		return self.envoyNpcObj

	def createAllTrionesMonsterNpc(self):
		'''创建7只怪物
		'''
		self.trionesMonsterObj = {}
		for monsterIdx in xrange(1001, 1008):
			self.createTrionesMonsterNpc(monsterIdx)

	def createTrionesMonsterNpc(self, monsterIdx):
		npcObj = self.addNpc(monsterIdx, "trionesMonsterNpc")
		self.trionesMonsterObj[monsterIdx] = npcObj
		self.dRandScenePos[monsterIdx] = npcObj.sceneId

	def removeTrionesMonsterNpc(self):
		'''删除7只怪物
		'''
		self.trionesMonsterObj = {}
		self.removeNpcByTypeFlag("trionesMonsterNpc")

	def getRandScenePos(self):
		'''随机7个场景分配7只怪物，每个场景只会有一个怪物
		'''
		lst = self.getGroupInfo(9001)
		lRandScene = []
		lCurScene = self.dRandScenePos.values()
		for sceneId in lst:
			if sceneId in lCurScene:
				continue
			lRandScene.append(sceneId)
		if not lRandScene:
			raise Exception,"北斗七星,随机场景为空"
		
		iSceneId = lRandScene[rand(len(lRandScene))]
		x, y = scene.randSpace(iSceneId)
		return iSceneId, x, y


	def trionesMonsterSceneName(self, monsterIdx):
		'''怪物所在场景名字
		'''
		iSceneId = self.dRandScenePos.get(monsterIdx)
		sceneObj = scene.getScene(iSceneId)
		if sceneObj:
			return sceneObj.name
		return ""

	def changeMonsterPos(self, npcObj):
		'''怪物达到攻击上限后（5次），会随机跳到当前场景的其他位置，30%的几率跳到其他没有怪物的场景
		'''
		dRatio = {1:70, 2:30}
		idx = chooseKey(dRatio)
		
		if idx == 1:#当前场景的其他位置
			iSceneId = npcObj.sceneId
			x, y = scene.randSpace(iSceneId)
		else:
			iSceneId, x, y = self.getRandScenePos()

		npcObj.switchPos(iSceneId, x, y)
		npcObj.onChangePos()
		# #场景服不支持NPC移动
		# self.tTempMonsterPos = (iSceneId, x, y)
		# self.removeNpc(npcObj)
		# self.createTrionesMonsterNpc(npcObj.idx)
		
	#=========================================================
	#活动
	def begin(self):
		'''开始
		'''
		self.removeEnvoyNpc()
		self.removeTrionesMonsterNpc()
		self.createEnvoyNpc()
		self.createAllTrionesMonsterNpc()
		self.halfHourMessage()

	def end(self):
		'''结束
		'''
		self.removeEnvoyNpc()
		self.removeTrionesMonsterNpc()
		#传闻
		message.sysMessage(self.getText(4011))


	def halfHourMessageTimer(self):
		'''活动时间每隔半个小时刷新一次系统传闻
		'''
		if not self.inNormalTime():
			return
		iLeftTime = self.nextHalfHourSecond()
		if iLeftTime > 0:
			self.startTimer(self.halfHourMessage, iLeftTime, "halfHourMessage")

	def halfHourMessage(self):
		if not self.inNormalTime():
			return
		self.halfHourMessageTimer()
		#传闻
		message.sysMessage(self.getText(4005))

	def nextHalfHourSecond(self):
		'''下一个30分或整点的秒数
		'''
		date = getDatePart()
		lEndTime = []
		lEndTime.append(date["year"])	#年
		lEndTime.append(date["month"])	#月
		lEndTime.append(date["day"])	#日
		minu = date["minute"]
		if minu >= 30:
			lEndTime.append(date["hour"]+1)	#时
			lEndTime.append(0)	#分
		else:
			lEndTime.append(date["hour"])	#时
			lEndTime.append(30)	#分
		lEndTime.append(0)				#秒
		iEndTime = getSecond(*lEndTime)
		iLeftTime = iEndTime - getSecond()
		return iLeftTime

	def giveTask(self, who):
		'''给任务
		'''
		who.day.set("trionesTask", 1)
		task.triones.giveTrionesTask(who)

	#===========================================
	#战斗
	def enterFight(self, who, npcObj):	
		'''进入战斗
		'''
		self.doScript(who, npcObj, "F{}".format(npcObj.idx))

		npcObj.addFightCnt()

	def onWarWin(self, warObj, npcObj, w):#override
		'''战斗胜利时
		'''
		who = getRole(w.id)
		if not who:
			return
		#改变任务进度
		self.changeTaskProgress(who, npcObj)

	def changeTaskProgress(self, who, npcObj):
		#给奖励,活动时间结束没任务也要给
		self.doScript(who, None, "R{}".format(npcObj.idx))
		#改变任务进度
		taskObj = task.hasTask(who, task.triones.TRIONES_TASK_PARENT_ID)
		if not taskObj:
			return
		if self.addKillMonster(who, npcObj.idx):
			task.service.rpcTaskChange(who, taskObj, "intro", "detail")
		#检查是否所有怪物杀完
		lKillMonster = who.day.fetch("trionesKill", [])
		for monsterIdx in xrange(1001, 1008):
			if monsterIdx not in lKillMonster:
				return
		#所有怪物杀完
		self.doScript(who, None, "R1008")
		message.tips(who, self.getText(4013, who.id))
		task.removeTask(who, taskObj.id)

		#加活跃
		perPoint = activity.center.getPerActPoint(26)
		who.addActPoint(perPoint)

	def hasKillMonster(self, who, monsterIdx):
		lKillMonster = who.day.fetch("trionesKill", [])
		return monsterIdx in lKillMonster

	def addKillMonster(self, who, monsterIdx):
		lKillMonster = who.day.fetch("trionesKill", [])
		if monsterIdx in lKillMonster:
			return False
		lKillMonster.append(monsterIdx)
		who.day.set("trionesKill", lKillMonster)
		return True


	#============================================

	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 100:
			txtList = []
			txtList.append("101-开始")
			txtList.append("102-结束")
			txtList.append("103-怪物位置")
			txtList.append("104-前往怪物位置")
			txtList.append("200-半小时系统传闻")
			txtList.append("201-清除任务进度")
			txtList.append("202-重置任务领取")
			message.dialog(who, "\n".join(txtList))

		elif cmdIdx == 101:
			self.begin()

		elif cmdIdx == 102:
			self.end()

		elif cmdIdx == 103:
			txtList = []
			for monsterIdx,npcObj in self.trionesMonsterObj.iteritems():
				txtList.append("{},{}--位置({},{},{}),已被挑战{}次".format(npcObj.name, monsterIdx, npcObj.sceneId, npcObj.x, npcObj.y, npcObj.iCurrFightCnt))
			if txtList:
				message.dialog(who, "\n".join(txtList))
			else:
				message.tips(who, "活动没开启")

		elif cmdIdx == 104:
			monsterIdx = int(args[0])
			npcObj = self.trionesMonsterObj.get(monsterIdx, None)
			if not npcObj:
				message.tips(who, "{}怪物不存在".format(monsterIdx))
				return
			scene.tryTransfer(who.id, npcObj.sceneId, npcObj.x, npcObj.y)

		elif cmdIdx == 200:
			self.halfHourMessage()

		elif cmdIdx == 201:
			who.day.set("trionesKill", [])
			taskObj = task.hasTask(who, task.triones.TRIONES_TASK_PARENT_ID)
			if taskObj:
				task.service.rpcTaskChange(who, taskObj, "intro", "detail")
				message.tips(who, "清除任务进度成功")
			else:
				message.tips(who, "你没有北斗七星任务")

		elif cmdIdx == 202:
			who.day.set("trionesTask", 0)
			who.day.set("trionesKill", [])
			message.tips(who, "重置任务领取成功")

		elif cmdIdx == 203:
			npcObj = self.trionesMonsterObj.get(1001, None)
			if not npcObj:
				message.tips(who, "1001NPC不存在")
				return
			self.changeMonsterPos(npcObj)

		elif cmdIdx == 402:
			taskObj = task.hasTask(who, task.triones.TRIONES_TASK_PARENT_ID)
			if not taskObj:
				message.tips(who, "你没有北斗七星任务")
				return
			for monsterIdx,npcObj in self.trionesMonsterObj.iteritems():
				self.changeTaskProgress(who, npcObj)

		# elif cmdIdx == 400:
		# 	global gbTrionesDebug
		# 	gbTrionesDebug = True

		# elif cmdIdx == 401:
		# 	global gbTrionesDebug
		# 	gbTrionesDebug = False		



import activity.object

class EnvoyNpc(activity.object.Npc):
	'''活动使者npc
	'''
	def doLook(self, who):
		content = self.game.getText(4001)
		selList = [1,2]
		content += '''
Q开始活动
Q规则说明'''
		
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)

	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.start(who)
		elif sel == 2:
			self.game.doScript(who, self, "D4004")

	def start(self, who):
		'''
		'''
		if task.hasTask(who, task.triones.TRIONES_TASK_PARENT_ID):
			self.game.doScript(who, self, "D6001")
			return
		if who.day.fetch("trionesTask", 0):
			self.game.doScript(who, self, "D6002")
			return
		if not self.game.inNormalTime():
			return
		if who.level < 30:
			self.game.doScript(who, self, "D4002")
			return
		teamObj = who.getTeamObj()
		if teamObj:
			self.game.doScript(who, self, "D4003")
			return
		self.game.giveTask(who)




class TrionesMonsterNpc(activity.object.Npc):
	'''怪物
	'''
	def __init__(self, gameObj):
		activity.object.Npc.__init__(self, gameObj)

		self.iCurrFightCnt = 0
		self.iChangePosUid = 1 	#每次变换位置加1

	def onChangePos(self):
		'''改变位置
		'''
		self.iCurrFightCnt = 0
		self.iChangePosUid += 1

	def switchPos(self, sceneId, x, y):
		'''切换位置
		'''
		# print "switchPos",self.sceneId,self.x,self.y,sceneId, x, y
		self.remove()
		sceneObj = scene.getScene(sceneId)
		if sceneObj:
			self.sceneId = sceneId
			self.x = x
			self.y = y
			sceneObj.addEntity(self, sceneId, x, y)

	def addFightCnt(self):
		self.iCurrFightCnt += 1

		if self.iCurrFightCnt >= self.game.configInfo.get("战斗上限", 0):
			self.game.changeMonsterPos(self)

	def transString(self, content):
		if "$number" in content:
			content = content.replace("$number", str(self.game.configInfo.get("战斗上限", 0)))
		if "$monster" in content:
			content = content.replace("$monster", self.name)
		return content
		
	def doLook(self, who):
		content = self.game.getText(4006)
		selList = [1,]
		content += '''
Q北斗七星'''
		who.trionesMstLookInfo = (self.idx, self.iChangePosUid)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)

	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.fight(who)

	def fight(self, who):
		'''进入战斗
		'''
		iMstIdx,iPosUid = getattr(who, "trionesMstLookInfo", (0, 0))
		if self.idx != iMstIdx or self.iChangePosUid != iPosUid:
			self.say(who, self.transString(self.game.getText(4010)))
			return

		taskObj = task.hasTask(who, task.triones.TRIONES_TASK_PARENT_ID)
		if not taskObj:
			self.game.doScript(who, self, "D4007")
			return

		if self.game.hasKillMonster(who, self.idx):
			self.game.doScript(who, self, "D4008")
			return

		teamObj = who.getTeamObj()
		if teamObj:
			self.game.doScript(who, self, "D4009")
			return

		self.game.enterFight(who, self)


def getActivity():
	return activity.getActivity("triones")


from common import *
import activity
import openUIPanel
import task
import message
import scene
import task.triones
import task.service
import activity.center