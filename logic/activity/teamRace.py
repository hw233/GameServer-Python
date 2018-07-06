# -*- coding: utf-8 -*-
'''组队竞技场
'''
from activity.object import Activity as customActivity
import activity.object

gbTeamRaceDebug = False

#战斗结果
NO_WAR = 0
WAR_WIN = 1
WAR_FAIL = 2

#竞技状态
# TEAMRACE_NO = 0
TEAMRACE_END = 0
TEAMRACE_READY = 1
TEAMRACE_BEGIN = 2

# gdChineseNumStr = {
# 1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九",10:"十",
# }

#导表开始
class Activity(customActivity):

	npcInfo = {
		1001:{"名称":"进场人","造型":"4003(0,1,0,0,0)","染色":"0,0,0,0,0,0","位置":"1130,139,25,1","称谓":"组队竞技场","对白":"4009"},
	}

	eventInfo = {
	}

	rewardInfo = {
		1001:{"经验":lambda LV:LV*15},
		1002:{"经验":lambda LV:LV*200+20000,"宠物经验":lambda PLV:PLV*160+16000,"银币":lambda LV:LV*200+16000,"物品":[1001],"武勋值":10},
		1003:{"经验":lambda LV:LV*120+12000,"宠物经验":lambda PLV:PLV*96+9600,"银币":lambda LV:LV*120+9600,"物品":[1002],"武勋值":5},
		1004:{"物品":[1003],"武勋值":100},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":8,"物品":"202001","数量":"1","绑定":0,"传闻":0},
			{"权重":8,"物品":"202002","数量":"1","绑定":0,"传闻":0},
			{"权重":8,"物品":"202003","数量":"1","绑定":0,"传闻":0},
			{"权重":8,"物品":"202004","数量":"1","绑定":0,"传闻":0},
			{"权重":8,"物品":"202005","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225001","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225002","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225003","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225004","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225005","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225006","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225007","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225008","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225009","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225010","数量":"1","绑定":0,"传闻":0},
			{"权重":100,"物品":"225901","数量":"1","绑定":0,"传闻":0},
			{"权重":3,"物品":"225902","数量":"1","绑定":0,"传闻":0},
			{"权重":1,"物品":"225903","数量":"1","绑定":0,"传闻":0},
			{"权重":500,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":400,"物品":"230101","数量":"2","绑定":0,"传闻":0},
			{"权重":400,"物品":"230101","数量":"3","绑定":0,"传闻":0},
			{"权重":500,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":500,"物品":"230102","数量":"2","绑定":0,"传闻":0},
			{"权重":100,"物品":"230102","数量":"5","绑定":0,"传闻":0},
			{"权重":25,"物品":"230103","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234101","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234102","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234103","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234104","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234105","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234106","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234107","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234108","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234109","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234110","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234111","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234112","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234113","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234114","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234115","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234116","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234117","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234118","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234119","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234120","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234121","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234122","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234123","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234124","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234125","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234126","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234127","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234128","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234129","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234130","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234131","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234132","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234133","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234134","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234135","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234136","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234137","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234138","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234139","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234140","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234141","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234142","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234143","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234144","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234145","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234146","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234147","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234148","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234149","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234150","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234151","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234152","数量":"1","绑定":0,"传闻":0},
			{"权重":25,"物品":"234153","数量":"1","绑定":0,"传闻":0},
			{"权重":5,"物品":"234401","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234402","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234403","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234404","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234405","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234406","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234407","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234408","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234409","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234410","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234411","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234412","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234413","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234414","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234415","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234416","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234417","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234418","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234419","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":5,"物品":"234420","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":1006,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":4000,"物品":"0","数量":"0","绑定":0,"传闻":0},
		),
		1002:(
			{"权重":20,"物品":"202001","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"202002","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"202003","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"202004","数量":"1","绑定":0,"传闻":0},
			{"权重":20,"物品":"202005","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225001","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225002","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225003","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225004","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225005","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225006","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225007","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225008","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225009","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225010","数量":"1","绑定":0,"传闻":0},
			{"权重":135,"物品":"225901","数量":"1","绑定":0,"传闻":0},
			{"权重":8,"物品":"225902","数量":"1","绑定":0,"传闻":0},
			{"权重":3,"物品":"225903","数量":"1","绑定":0,"传闻":0},
			{"权重":223,"物品":"230101","数量":"1","绑定":0,"传闻":0},
			{"权重":300,"物品":"230101","数量":"2","绑定":0,"传闻":0},
			{"权重":300,"物品":"230101","数量":"3","绑定":0,"传闻":0},
			{"权重":200,"物品":"230102","数量":"1","绑定":0,"传闻":0},
			{"权重":300,"物品":"230102","数量":"3","绑定":0,"传闻":0},
			{"权重":300,"物品":"230102","数量":"5","绑定":0,"传闻":0},
			{"权重":300,"物品":"230103","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234101","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234102","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234103","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234104","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234105","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234106","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234107","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234108","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234109","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234110","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234111","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234112","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234113","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234114","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234115","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234116","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234117","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234118","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234119","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234120","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234121","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234122","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234123","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234124","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234125","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234126","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234127","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234128","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234129","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234130","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234131","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234132","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234133","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234134","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234135","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234136","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234137","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234138","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234139","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234140","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234141","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234142","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234143","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234144","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234145","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234146","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234147","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234148","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234149","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234150","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234151","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234152","数量":"1","绑定":0,"传闻":0},
			{"权重":35,"物品":"234153","数量":"1","绑定":0,"传闻":0},
			{"权重":2,"物品":"234201","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234202","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234203","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234204","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234205","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234206","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234207","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234208","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234209","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234210","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234211","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234212","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234213","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234214","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234215","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234216","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234217","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234218","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234219","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234220","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234221","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234222","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234223","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234224","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234225","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234226","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234227","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234228","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234229","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234230","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234231","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234232","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234233","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234234","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234235","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234236","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234237","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234238","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234239","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234240","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234241","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234242","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234243","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234244","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234245","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234246","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234247","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234248","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234249","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234250","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234251","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234252","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234253","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234401","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234402","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234403","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234404","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234405","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234406","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234407","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234408","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234409","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":2,"物品":"234410","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234411","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234412","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234413","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234414","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234415","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234416","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234417","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234418","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234419","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":10,"物品":"234420","数量":"1","绑定":0,"传闻":"SM5001"},
			{"权重":400,"物品":"246051","数量":"1","绑定":0,"传闻":0},
			{"权重":4000,"物品":"0","数量":"0","绑定":0,"传闻":0},
		),
		1003:(
			{"权重":1000,"物品":"225902","数量":"1","绑定":0,"传闻":0},
		),
	}

	groupInfo = {
	}

	chatInfo = {
		4001:'''#L1<14,24>*[组队竞技场]*02#n即将开始请仙友们做好准备组队进场''',
		4002:'''#L1<14,24>*[组队竞技场]*02#n开始进场，请参加活动的仙友组好队伍点击#C01$teamRaceNpc#n进入活动准备室，20:00后将无法再进场''',
		4003:'''#L1<14,24>*[组队竞技场]*02#n进场中，请参加活动的仙友组好队伍迅速点击#C01$teamRaceNpc#n进入活动准备室，20:00后将无法再进场''',
		4004:'''#L1<14,24>*[组队竞技场]*02#n即将开始，请参加活动的仙友组好队伍迅速点击#C01$teamRaceNpc#n进入活动准备室，20:00后将无法再进场''',
		4005:'''#L1<14,24>*[组队竞技场]*02#n还有一分钟开始，请参加活动的仙友把握最好的机会，组好队伍点击#C01$teamRaceNpc#n进入活动准备室，20:00后将无法再进场''',
		4006:'''#C01$roleName#n离场并退出组队''',
		4007:'''#C01$roleName#n离场并退出组队，队长给予#C01$roleName#n''',
		4008:'''你所在的队伍已被分配到#C01$pck#n，20:05开始匹配战斗，请做好准备''',
		4009:'''在这里可以参加组队竞技场，进入需要提前组队，活动按照队伍等级的最高等级分赛场''',
		4010:'''还没开始进场，19:40后再来吧！''',
		4011:'''队伍人数不足三人，组好三人或三人以上队伍再来''',
		4012:'''队伍中#C01$roleUnderLv#n的等级不足#C0430#n级无法参加组队竞技场''',
		4013:'''队伍中#C01$roleState#n已进过场并离场，无法再次进入''',
		4014:'''1.19:40分开始进场，进场后进入准备室等待分场\n2.进场后非战斗状态每分钟获得经验\n3.20:00开始按照队伍中最高的玩家等级，进行等级段分场\n4.赛场等级段：90-109化神组 70-89元婴组 50-69金丹组 30-49筑基组\n5.分场后每5分钟匹配一次每次战斗完都有奖励，匹配战斗失败2次退出竞技场，最后赛场冠军获得特殊称谓''',
		4015:'''经过艰苦奋战，#L1<14,24>*[组队竞技场]*02#n$groupName的冠军由#C01$teamRoleName#n夺得''',
		4016:'''队伍中有队员暂离无法进场''',
		4017:'''本轮匹配轮空''',
		5001:'''#C01$roleName#n在#L1<14,24>*[组队竞技场]*02#n中和队友干净利落的击败对手，获得$lnkProps''',
		6000:'''本场景无法传送，请点击#C04【退出场景】#n按钮离开''',
		6001:'''准备室队伍数已达到上限''',
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
		101:{"名称":"竞技场","资源":1130,"着陆点x":101,"着陆点y":63},
	}

	configInfo = {
		"准备室数量":2,
		"准备室队伍数量":4,
		"等级段队伍数量":4,
		"多开队伍数量":2,
		"分组名称":{1:"化神",2:"元婴",3:"金丹",4:"筑基"},
		"化神":(90,109),
		"元婴":(70,89),
		"金丹":(50,69),
		"筑基":(30,49),
		"匹配时间间隔":300,
		"合并判断数量":2,
		"战报数上限":50,
		"竞技积分系数":{0:50,1:25,2:10,3:5},
		"冠军称谓":{1:40404,2:40403,3:40402,4:40401},
	}
#导表结束
	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.week = cycleData.cCycWeek(2,self.__dirtyEventHandler)
		self.initRank()
		self.reset()
		if self.inEnterTime() and not self.week.fetch("teamRace", 0):
			self.setCreateRaceNpcTimer()

	def save(self):
		data = customActivity.save(self)
		dWeek=self.week.save()
		if dWeek:
			data['w']=dWeek
		return data
	
	def load(self, data):
		customActivity.load(self, data)
		self.week.load(data.pop('w',{}))

	def reset(self):
		self.state = TEAMRACE_END
		self.teamRaceNpcObj = None
		self.dEnterRaceRoleId = {}	#所有进过场的玩家
		self.dReadyRoom = {}		#准备室
		self.dReadySceneObj = {}
		self.dAllTeamId = {}		#所有队伍ID
		self.dAllRoleId = {}		#所有在场景内的角色ID
		self.dGroupInfo = {}		#分组
		self.dRaceSceneObj = {}		#分组场景

		self.dTeamLastRecord = {}	#记录队伍上一次对战的队伍ID
		self.dTeamWinRecord = {}	#队伍胜利场数
		self.dRaceWinRecord = {}	#记录哪些分组已结束

		self.dTeamRaceInfo = {}		#战报
		self.dRoleRaceInfo = {}		#队员的战报
		self.dTeamRoleScore = {}	#队伍队员综合实力

		self.dInFightTeamId = {}	#正在战斗的队伍
		self.dFightEndCoolTime = {}		#战斗结束匹配冷却时间

		self.dMatchFight = {}		#匹配结果

	def init(self):
		dGroupConfig = self.getConfigInfo("分组名称")
		for index, name in dGroupConfig.iteritems():
			rankObj = rank.getRankObjByName("rank_teamrace_point_{}".format(index))
			if not rankObj:
				continue
			rankObj.checkTeamRacePointChange()

	def getTermNo(self):
		'''第几期
		'''
		return self.fetch("termNo")
	
	def addTermNo(self, val):
		self.add("termNo", val)

	#===================================================
	#活动期间的排行榜
	def initRank(self):
		'''初始化活动期间的积分排行榜
		'''
		import rank.teamRaceActPoint
		self.dTeamRaceActRank = {}
		dGroupConfig = self.getConfigInfo("分组名称")
		for iGroupId, name in dGroupConfig.iteritems():
			rankObj = rank.teamRaceActPoint.cRanking(0, 0, "组队竞技积分-{}".format(name), "rank_teamRaceAct_{}".format(iGroupId), 200)
			if not rankObj._loadFromDB():
				rankObj._insertToDB(*rankObj.getPriKey())
			rankObj.startTimer()	#即时刷新不走定时器
			self.dTeamRaceActRank[iGroupId] = rankObj

	def resetRank(self):
		'''重置活动期间的积分排行榜
		'''
		for iGroupId, rankObj in self.dTeamRaceActRank.iteritems():
			self.log("resetRank|{}".format(iGroupId))
			rankObj.clearRank()

	def updateTeamRaceActRank(self, who):
		'''更新活动期间的积分排行榜
			若多个队伍积分一样，则按照获得这个积分的时间排序，若时间一样，则按照队伍整体实力排序
		'''
		teamObj = who.getTeamObj()
		if not teamObj:
			return
		iGroupId,iIndex = self.getTeamGroup(teamObj.id)
		rankObj = self.dTeamRaceActRank.get(iGroupId, None)
		if not rankObj:
			return
		
		iTeamRaceActPoint = who.day.fetch("teamRaceActPoint")
		iTeamTotalScore = self.getTeamScore(teamObj.id)
		iTeamPos = teamObj.getPos(who.id)
		iGainTime = getattr(teamObj, 'teamRaceFightEndTime', getSecond())
		rankObj.updateScore(who.id, who.name, iTeamRaceActPoint, who.level, who.school, pos=iTeamPos, teamTotalScore=iTeamTotalScore, teamId=teamObj.id, gainTime=iGainTime)

	def getTeamRaceActRank(self, who):
		'''获取排行榜
		'''
		teamObj = who.getTeamObj()
		if not teamObj:
			return None
		iGroupId,iIndex = self.getTeamGroup(teamObj.id)
		rankObj = self.dTeamRaceActRank.get(iGroupId, None)
		return rankObj

	#===================================================

	def log(self, content):
		customActivity.log(self, content)
		print content

	def inBeforeEnterTime(self):
		'''进场时间前
		'''
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		minute = datePart["minute"]

		if wday <= 5 and hour <=19 and minute < 40:
			return True
		return False

	def inAfterEnterTime(self):
		'''进场时间后
		'''
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]

		if wday >= 5 and hour >= 20:
			return True
		return False

	def inRaceTime(self):
		'''时间:19：40--22:00
		'''
		if gbTeamRaceDebug:
			return True
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		minute = datePart["minute"]

		if wday != 5:
			return False
		if (hour == 19 and minute >=40) or hour in (20, 21):
			return True
		return False

	def inEnterTime(self):
		'''进场时间:19：40--20:00
		'''
		if gbTeamRaceDebug:
			return True
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		minute = datePart["minute"]

		if wday != 5:
			return False
		if hour == 19 and minute >=40:
			return True
		return False

	def inMatchTime(self):
		'''匹配时间，20：05--21:55
		'''
		if gbTeamRaceDebug:
			return True
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		minute = datePart["minute"]
		if wday != 5:
			return False
		if (hour == 20 and minute >=5 ) or (hour == 21 and minute <= 55):
			return True
		return False

	def inNormalTime(self):
		'''是否活动正式时间
		'''
		if gbTeamRaceDebug:
			return True
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		if wday != 5:
			return False
		if hour not in (20, 21, ):
			return False
		return True

	def getLeftTime(self):
		'''活动剩余时间
		'''
		# if not self.inNormalTime():
		# 	return 0
		
		datePartNow = getDatePart()
		year = datePartNow["year"]
		month = datePartNow["month"]
		day = datePartNow["day"]
		endTime = getSecond(year, month, day, 22)
		return max(0, endTime - getSecond())

	def stopAllRaceTimer(self):
		'''停止所有定时器
		'''
		lTimerFlag = ["readyStart", "startEnterSysMsg_40", "startEnterSysMsg_50", "startEnterSysMsg_55",
			"startEnterSysMsg_59", "startMatch", "newMinuReward", "matchFight", "sendMatchInfo",
			]
		for flag in lTimerFlag:
			self.stopTimer(flag)

	def setCreateRaceNpcTimer(self):
		'''设置生成npc，传闻
		'''
		date = getDatePart()
		wday = date["wday"]
		curHour = date["hour"] 
		if wday != 5 and curHour != 19:
			return
		curMinute = date["minute"]

		lEndTime = []
		lEndTime.append(date["year"])	#年
		lEndTime.append(date["month"])	#月
		lEndTime.append(date["day"])	#日
		lEndTime.append(19)				#时
		lEndTime.append(30)				#分
		lEndTime.append(0)				#秒

		self.stopAllRaceTimer()
		if curMinute >=30:	#19:30开始活动预告
			self.readyStart(bResetRank=False)
		else:
			iEndTime = getSecond(*lEndTime)
			iLeftTime = iEndTime - getSecond()
			self.timerMgr.run(self.readyStart, iLeftTime, 0, "readyStart")

		#19：40活动开始进场
		lEndTime[4] = 40
		iEndTime = getSecond(*lEndTime)
		iLeftTime = iEndTime - getSecond()
		if iLeftTime > 0:
			self.timerMgr.run(functor(self.startEnterSysMsg, 4002), iLeftTime, 0, "startEnterSysMsg_40")
			self.timerMgr.run(self.setNewMinuReward, iLeftTime, 0, "setNewMinuReward")
		else:
			self.setNewMinuReward()

		#19:50公告
		lEndTime[4] = 50
		iEndTime = getSecond(*lEndTime)
		iLeftTime = iEndTime - getSecond()
		if iLeftTime:
			self.timerMgr.run(functor(self.startEnterSysMsg, 4003), iLeftTime, 0, "startEnterSysMsg_50")

		#19:55公告
		lEndTime[4] = 55
		iEndTime = getSecond(*lEndTime)
		iLeftTime = iEndTime - getSecond()
		if iLeftTime > 0:
			self.timerMgr.run(functor(self.startEnterSysMsg, 4004), iLeftTime, 0, "startEnterSysMsg_55")

		#19:59公告
		lEndTime[4] = 59
		iEndTime = getSecond(*lEndTime)
		iLeftTime = iEndTime - getSecond()
		if iLeftTime > 0:
			self.timerMgr.run(functor(self.startEnterSysMsg, 4005), iLeftTime, 0, "startEnterSysMsg_59")

	def startEnterSysMsg(self, iSysMsgId):
		'''公告
		'''
		message.sysAnnounce(self.getText(iSysMsgId))
		self.log("sysAnnounce:%s"%(iSysMsgId))

	def readyStart(self, bResetRank=True):
		'''19:30开始活动预告
		'''
		# if self.state != TEAMRACE_NO:
		# 	return
		self.log("readyStart")
		self.deleteRaceNpc()
		self.removeReadyScene()
		self.removeRaceScene()
		if bResetRank:
			self.resetRank()
		message.sysMessage((self.getText(4001)))
		self.reset()
		self.state = TEAMRACE_READY
		self.createEnterNpc()
		self.createReadyRoom()

	def getEnterNpcIdx(self):
		return 1001

	def getTeamRaceEnterNpc(self):
		return self.teamRaceNpcObj

	def newNpc(self, npcIdx, name, shape, who=None):
		'''创建Npc
		'''
		if npcIdx == self.getEnterNpcIdx():
			return cTeamRaceNpc(self)
		return customActivity.newNpc(self, npcIdx, name, shape, who)

	def createEnterNpc(self):
		'''显示进场NPC
		'''
		self.log("createEnterNpc")
		npcIdx = self.getEnterNpcIdx()
		npcObj = self.addNpc(npcIdx, "teamRaceEnterNpc")
		self.teamRaceNpcObj = npcObj

	def deleteRaceNpc(self):
		'''删除进场NPC
		'''
		if self.teamRaceNpcObj:
			self.log("deleteRaceNpc")
			self.removeNpcByTypeFlag("teamRaceEnterNpc")
			self.teamRaceNpcObj = None

	def getText(self, chatIdx, roleId=0, **kwargs):
		content = customActivity.getText(self, chatIdx, roleId)
		if "$groupName" in content or "$teamRoleName" in content:
			iGroupId, iIndex = kwargs.get("endGroup", (0,0))
			if iGroupId and iIndex:
				sGroupName = self.getGroupNameByIndex(iGroupId, iIndex)
				if "$groupName" in content:
					content = content.replace("$groupName", sGroupName)

				if "$teamRoleName" in content:
					iTeamId = self.dRaceWinRecord.get((iGroupId, iIndex), ())
					teamObj = team.getTeam(iTeamId)
					if teamObj:
						lTemp = []
						for roleId in teamObj.getInTeamList():
							roleObj = getRole(roleId)
							if not roleObj:
								continue
							lTemp.append(roleObj.name)
						content = content.replace("$teamRoleName", ",".join(lTemp))

		return content

	def transString(self, content, roleId=0):
		who = getRole(roleId)
		if who:
			teamObj = who.getTeamObj()
			if teamObj:
				if "$roleUnderLv" in content:
					lTemp = []
					for roleId in teamObj.getInTeamList():
						roleObj = getRole(roleId)
						if not roleObj:
							continue
						if roleObj.level < 30:
							lTemp.append(roleObj.name)

					content = content.replace("$roleUnderLv", ",".join(lTemp))

				if "$roleState" in content:
					lTemp = []
					for roleId in teamObj.getInTeamList():
						if roleId not in self.dEnterRaceRoleId:
							continue
						roleObj = getRole(roleId)
						if not roleObj:
							continue
						lTemp.append(roleObj.name)

					content = content.replace("$roleState", ",".join(lTemp))

				if "$pck" in content:
					sGroupName = self.getGroupNameByTeamId(teamObj.id)
					content = content.replace("$pck", sGroupName)

		if "$teamRaceNpc" in content:
			sTeamRaceNpcName = ""
			if self.teamRaceNpcObj:
				sTeamRaceNpcName = self.teamRaceNpcObj.name 
			content = content.replace("$teamRaceNpc", sTeamRaceNpcName)
		
		return customActivity.transString(self, content, pid=roleId)

	def checkTeamMemberLv(self, teamObj):
		'''检查所有队员等级
		'''
		for roleId in teamObj.getInTeamList():
			roleObj = getRole(roleId)
			if not roleObj:
				continue
			if roleObj.level < 30:
				return False	
		return True

	def checkTeamMemberState(self, teamObj):
		'''检查是否有队员进过场
		'''
		if gbTeamRaceDebug:
			return True
		for roleId in teamObj.getInTeamList():
			if roleId in self.dEnterRaceRoleId:
				return False
		return True

	def onOffline(self, who):
		'''处理在竞技场景内直接下线
		'''
		if who.id not in self.dAllRoleId:
			return
		self.leaveScene(who)
		self.dAllRoleId.pop(who.id, None)
		teamObj = who.getTeamObj()
		if not teamObj:
			return
		if teamObj.inTeamSize > 1:
			return
		#队伍最后一个人退出
		self.dAllTeamId.pop(teamObj.id, None)
		self.removeFormGroup(teamObj.id)
		iGroupId,iIndex = self.getTeamGroup(teamObj.id)
		self.log("onOffline |{},{}|{},{}".format(who.id, teamObj.id, iGroupId, iIndex))
		if iGroupId and iIndex:
			self.tryGroupEnd(iGroupId, iIndex)

	def getGameScene(self):
		'''活动场景
		'''
		return self.getSceneByIdx(101)

	def createScene(self, sceneIdx):
		'''创建场景
		'''
		sceneObj = customActivity.createScene(self, sceneIdx)
		info = self.getSceneInfo(sceneIdx)
		sceneObj.landX = info.get("着陆点x", -1)
		sceneObj.landY = info.get("着陆点y", -1)
		return sceneObj

	def createReadyScene(self):
		self.log("createReadyScene")
		sceneObj = self.addScene(101, "readyScene")
		sceneObj.eventOnEnter += self.onEnterScene#self.onEnterReadyScene
		sceneObj.eventOnLeave += self.onLeaveScene#self.onLeaveReadyScene
		sceneObj.denyTeam = "组队竞技"
		sceneObj.denyTeamAddMember = "组队竞技"
		sceneObj.denyTransfer = self.getText(6000)
		return sceneObj

	def removeReadyScene(self):
		self.log("removeReadyScene")
		self.dReadySceneObj = {}
		self.removeSceneByTypeFlag("readyScene")

	def createRaceScene(self):
		self.log("createRaceScene")
		sceneObj = self.addScene(101, "raceScene")
		sceneObj.eventOnEnter += self.onEnterScene#self.onEnterRaceScene
		sceneObj.eventOnLeave += self.onLeaveScene#self.onLeaveRaceScene
		sceneObj.denyTeam = "组队竞技"
		sceneObj.denyTransfer = self.getText(6000)
		return sceneObj

	def removeRaceScene(self):
		self.log("removeRaceScene")
		self.dRaceSceneObj = {}
		self.removeSceneByTypeFlag("raceScene")

	def setDenyQuitTeam(self, who, bSetDeny):
		if bSetDeny:
			who.denyQuitTeam = "组队竞技"
		else:
			delattr(who, "denyQuitTeam")

	def addEnterRole(self, who):
		self.dEnterRaceRoleId[who.id] = 1
		if who.id not in self.dRoleRaceInfo:
			raceInfo = {
				"countWin": 0, # 胜利场数
				"countFight": 0, # 战斗场数
				"racePoint": 0,	#竞技积分
			}
			self.dRoleRaceInfo[who.id] = raceInfo

	def onEnterScene(self, who, oldScene, newScene):
	# def onEnterReadyScene(self, who, oldScene, newScene):
		'''进入准备活动场景时
		'''
		if oldScene is newScene:
			return
		self.setDenyQuitTeam(who, True)
		self.addEnterRole(who)
		self.dAllRoleId[who.id] = 1

		if self.inRaceTime():
			rpcTeamRaceEnter(self, who)
		# if self.inNormalTime():
			rpcTeamRaceInfo(self, who)
			rpcTeamRaceTeamCount(self, who)
			rpcTeamRaceFightInfoList(self, who)

	def onLeaveScene(self, who, oldScene, newScene):
	# def onLeaveReadyScene(self, who, oldScene, newScene):
		'''离开准备活动场景时
		'''
		if oldScene is newScene:
			return
		self.setDenyQuitTeam(who, False)
		self.dAllRoleId.pop(who.id, None)
		rpcTeamRaceEnd(self, who)

	# def onEnterRaceScene(self, who, oldScene, newScene):
	# 	'''进入竞技活动场景时
	# 	'''
	# 	if oldScene is newScene:
	# 		return
	# 	self.setDenyQuitTeam(who, True)
	# 	self.addEnterRole(who)

	# def onLeaveRaceScene(self, who, oldScene, newScene):
	# 	'''离开竞技活动场景时
	# 	'''
	# 	if oldScene is newScene:
	# 		return
	# 	self.setDenyQuitTeam(who, False)

	def leaveScene(self, who):
		'''离开竞技场
		'''
		sceneId, x, y = who.getLastRealPos()
		self.transfer(who, sceneId, x, y)

	def createReadyRoom(self):
		'''创建准备室，准备室上限——10个，每个准备室最多64个队伍
		'''
		self.dReadyRoom = {}
		self.dReadySceneObj = {}
		iMaxCnt = self.getConfigInfo("准备室数量")
		for i in xrange(1, iMaxCnt+1):
			self.dReadyRoom[i] = {}
			self.dReadySceneObj[i] = self.createReadyScene()

			self.log("createReadyRoom|{}".format(i))

	def getReadyScene(self):
		'''顺序填满场景，第一个场景满了之后，后面的玩家加到第二个场景
		'''
		iMaxTeamCnt = self.getConfigInfo("准备室队伍数量")
		for i,dInfo in self.dReadyRoom.iteritems():
			if len(dInfo) >= iMaxTeamCnt:#每个准备室最多64个队伍
				continue
			return i
		return 0

	def addTeamEnter(self, teamObj, iReadyRoom):
		self.dReadyRoom[iReadyRoom][teamObj.id] = 1
		# for roleId in teamObj.getInTeamList():
		# 	self.dEnterRaceRoleId[roleId] = 1

	def calcAttrTeamScore(self, teamObj):
		'''保存队伍的整体综合实力评分
		'''
		iTotalScore = 0
		for roleId in teamObj.getInTeamList(): 
			memberObj = getRole(roleId)
			if not memberObj:
				continue
			iTotalScore += grade.gradeAll(memberObj)
		self.dTeamRoleScore[teamObj.id] = iTotalScore

	def getTeamScore(self, iTeamId):
		'''队伍所有队员综合实力之和
		'''
		if iTeamId not in self.dTeamRoleScore:
			teamObj = team.getTeam(iTeamId)
			if not teamObj:
				return 0
			self.calcAttrTeamScore(teamObj)
		return self.dTeamRoleScore.get(iTeamId, 0)

	def resetTeamScore(self, iTeamId):
		self.dTeamRoleScore.pop(iTeamId, None)

	def enterReadyScene(self, who, teamObj):
		'''进入组队竞技场
		'''
		iReadyRoom = self.getReadyScene()
		if not iReadyRoom:
			message.tips(who, self.getText(6001))
			return
		sceneObj = self.dReadySceneObj.get(iReadyRoom, None)
		if not sceneObj:
			return

		self.createTeamRaceInfo(teamObj.id)
		self.transfer(who, sceneObj.id, None, None)
		self.addTeamEnter(teamObj, iReadyRoom)
		teamObj.teamRaceLastResult = NO_WAR
		teamObj.denyQuitTeam = "组队竞技"

		self.calcAttrTeamScore(teamObj)
		self.dAllTeamId[teamObj.id] = 1

	def quitTeamRace(self, who):
		'''退出组队竞技场
		'''
		if who.inWar():
			return
		teamObj = who.getTeamObj()
		if not teamObj:
			return

		iTeamId = teamObj.id
		iGroupId,iIndex = self.getTeamGroup(iTeamId)
		if iGroupId and iIndex:
			if iTeamId in self.dMatchFight[iGroupId][iIndex]:
				message.tips(who, self.getText(4016, pid))
				return
		
		isLeader = teamObj.isLeader(who.id)
		# team.service.rpcTeamQuit(who, None)
		teamObj = teamObj.this()
		teamObj.remove(who.id)
		self.leaveScene(who)
		if teamObj.isReleased():
			team.platform.teamRelease(iTeamId)
			self.dAllTeamId.pop(iTeamId, None)
			self.removeFormGroup(iTeamId)
		else:
			#离场提示
			if isLeader:
				team.platformservice.updateTarget(teamObj)	
				leaderObj = getRole(teamObj.leader)
				sTips = "#C01{}#n离场并退出组队，队长给予#C01{}#n".format(who.name, leaderObj.name if leaderObj else "")
			else:
				sTips = "#C01{}#n离场并退出组队".format(who.name)
			team.platformservice.teamMemberChange(teamObj)
			team.platformservice.teamKickDuel(who.id, iTeamId, False)
			for pid in teamObj.getInTeamList():
				message.tips(pid, sTips) 

		self.resetTeamScore(iTeamId)
		if iGroupId and iIndex:
			self.tryGroupEnd(iGroupId, iIndex)

	#=================================================
	#竞技信息部分
	def getTeamRaceInfo(self, iTeamId):
		'''获取队伍竞技信息
		'''
		return self.dTeamRaceInfo.get(iTeamId, {})

	def getRoleRaceInfo(self, roleId):
		'''获取个人竞技信息
		'''
		return self.dRoleRaceInfo.get(roleId, {})

	def createTeamRaceInfo(self, iTeamId):
		'''创建竞技信息
		'''
		if iTeamId in self.dTeamRaceInfo:
			return
		raceInfo = {
			"countWin": 0, # 胜利场数
			"countFight": 0, # 战斗场数
			"fightInfoList": [], # 战报列表
		}
		self.dTeamRaceInfo[iTeamId] = raceInfo

	def updateTeamRaceInfo(self, teamObj, refresh=True, **attrList):
		'''更新竞技信息
		'''
		dTeamRaceInfo = self.dTeamRaceInfo.get(teamObj.id, None)
		if not dTeamRaceInfo:
			return

		refreshList = []
		for attrName, attrVal in attrList.iteritems():
			dTeamRaceInfo[attrName] = attrVal
			if attrName in ("countWin", "countFight",):
				refreshList.append(attrName)
				
		if refresh and refreshList:
			rpcTeamRaceInfoChange(self, teamObj, *refreshList)

	def addCountWin(self, teamObj, count=1, refresh=False):
		'''增加胜利场数
		'''
		dTeamRaceInfo = self.getTeamRaceInfo(teamObj.id)
		if dTeamRaceInfo:
			dTeamRaceInfo["countWin"] += count
		for roleId in teamObj.getInTeamList():
			dRoleRaceInfo = self.getRoleRaceInfo(roleId)
			if dRoleRaceInfo:
				dRoleRaceInfo["countWin"] += count
		if refresh:
			rpcTeamRaceInfoChange(self, teamObj, "countWin")
		
	def addCountFight(self, teamObj, count=1, refresh=False):
		'''增加战斗场数
		'''
		dTeamRaceInfo = self.getTeamRaceInfo(teamObj.id)
		if dTeamRaceInfo:
			dTeamRaceInfo["countFight"] += count
		for roleId in teamObj.getInTeamList():
			dRoleRaceInfo = self.getRoleRaceInfo(roleId)
			if dRoleRaceInfo:
				dRoleRaceInfo["countFight"] += count
		if refresh:
			rpcTeamRaceInfoChange(self, teamObj, "countFight")

	def addFightInfo(self, teamObj, result):
		'''增加战报
		'''
		dTeamRaceInfo = self.getTeamRaceInfo(teamObj.id)
		if not dTeamRaceInfo:
			return
				
		fightInfo = {
			"time": getSecond(),
			"times": dTeamRaceInfo["countFight"],
			"result": result,
		}
		fightInfoList = dTeamRaceInfo["fightInfoList"]
		fightInfoList.append(fightInfo)
		if len(fightInfoList) > self.getConfigInfo("战报数上限"):
			del fightInfoList[0]
		rpcTeamRaceFightInfoAdd(self, teamObj, fightInfo)

	#====================================================================
	#
	def onNewHour(self, day, hour, wday):
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		if wday != 5:
			return

		if hour == 19:
			#19:30分显示进场NPC
			self.setCreateRaceNpcTimer()

		elif hour == 20:
			#20:00删除进场NPC
			self.begin()

		elif hour == 22:
			self.end()

	#=================================================
	#分组部分
	def groupByLv(self):
		'''分组
		'''
		self.log("groupByLv start|{}".format(self.dReadyRoom))
		dGroupConfig = self.getConfigInfo("分组名称")
		dGroupLv = {}	#等级
		dGroupInfo = {}	#初次分组
		self.dGroupInfo = {}#最终分组结果
		for iGroupId,sGroupName in dGroupConfig.iteritems():
			dGroupLv[self.getConfigInfo(sGroupName)] = iGroupId
			dGroupInfo[iGroupId] = []
			self.dGroupInfo[iGroupId] = {}

		for iRoom,dTeamInfo in self.dReadyRoom.iteritems():
			for iTeamId in dTeamInfo:
				teamObj = team.getTeam(iTeamId)
				if not teamObj:
					continue
				iMaxLv = teamObj.getMaxLV()
				for uLv,iGroupId in dGroupLv.iteritems():
					if uLv[0] <= iMaxLv <= uLv[1]:
						dGroupInfo[iGroupId].append(iTeamId)
						break

		#如果某一个等级段的队伍数<32，则判定下一个等级段的队伍数是否>32
		#如果是，则将本等级段的队伍放到上一个等级段的场，如果不是，则两个等级段的队伍合并成一个场
		#如果没上一个等级段则并入下一个等级段
		iGroupLen = len(dGroupConfig)
		iJudgeLen = self.getConfigInfo("合并判断数量")
		for iGroupId,sGroupName in dGroupConfig.iteritems():
			if len(dGroupInfo[iGroupId]) >= iJudgeLen:
				continue
			# print "===iGroupId==",iGroupId,iJudgeLen,iGroupId < iJudgeLen-1
			if iGroupId == 1:	#没上一个等级段则并入下一个等级段
				sNextGroupId = iGroupId+1
				dGroupInfo[sNextGroupId].extend(dGroupInfo[iGroupId])
				dGroupInfo[iGroupId] = []
			elif iGroupId == iGroupLen:	#筑基组不合并，也不被合并
				pass
			elif iGroupId < iGroupLen-1:#1,2<3
				sMergeId = 0
				sNextGroupId = iGroupId+1
				if sNextGroupId == iGroupLen:#筑基组不合并，也不被合并
					pass
				else:
					iNextLen = len(dGroupInfo[sNextGroupId])
					if iNextLen > iJudgeLen:	#则将本等级段的队伍放到上一个等级段的场
						sLastGroupId = iGroupId-1	#上一个等级段
						if len(dGroupInfo[sLastGroupId]) == 0:
							sMergeId = sNextGroupId
						else:
							sMergeId = sLastGroupId
					else:
						sMergeId = sNextGroupId

					dGroupInfo[sMergeId].extend(dGroupInfo[iGroupId])
					dGroupInfo[iGroupId] = []

		#如果有等级段内的队伍数量>64队，则判定多出来的队伍数量是否>32队，如果不是，则放到64那里，如果是，则另开一个场
		#优先划分高等级的场，之后再依次划分低等级的
		iMaxTeamCnt = self.getConfigInfo("等级段队伍数量")
		iMultiCnt = self.getConfigInfo("多开队伍数量")
		for iGroupId,sGroupName in dGroupConfig.iteritems():
			lGroupInfo = dGroupInfo[iGroupId]
			iLen = len(lGroupInfo)
			iFull = iLen/iMaxTeamCnt	#满场数量
			iMoreOne = 1 				#是否要多开一场
			if iFull > 0:
				iMoreOne = 1 if (iLen-iFull*iMaxTeamCnt)%iMaxTeamCnt > iMultiCnt else 0

			iIndex = 1
			for i in xrange(iFull):
				iStart = i*iMaxTeamCnt
				end = (i+1)*iMaxTeamCnt
				if i == iFull:
					if not iMoreOne:#不需要多开一场
						end = len(lGroupInfo)
				self.dGroupInfo[iGroupId][iIndex] = lGroupInfo[iStart:end]
				iIndex += 1
			if iMoreOne:
				self.dGroupInfo[iGroupId][iIndex] = lGroupInfo[iFull*iMaxTeamCnt:]
		self.log("groupByLv end:%s|%s"%(dGroupInfo, self.dGroupInfo))

	def getGroupName(self, iGroupId):
		dGroupConfig = self.getConfigInfo("分组名称")
		if iGroupId not in dGroupConfig:
			raise Exception,"%s分组不存在"%iGroupId
		return dGroupConfig[iGroupId]

	def getGroupNameByTeamId(self, teamId):
		'''分组名称
		'''
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if teamId in lTeamId:
					sGroupName = self.getGroupName(iGroupId)
					if len(dGroupInfo) > 1:
						return "{}{}组".format(sGroupName, iIndex)
					else:
						return "{}组".format(sGroupName)
		return ""

	def getGroupNameByIndex(self, iGroupId, iIndex):
		if iGroupId not in self.dGroupInfo:
			# return ""
			raise Exception,"%s分组不存在"%(iGroupId)
		if iIndex not in self.dGroupInfo[iGroupId]:
			# return ""
			raise Exception,"%s分组不存在%s"%(iGroupId, iIndex)
		sGroupName = self.getGroupName(iGroupId)
		if len(self.dGroupInfo[iGroupId]) > 1:
			return "{}{}组".format(sGroupName, iIndex)
		else:
			return "{}组".format(sGroupName)

	def getTeamGroup(self, teamId):
		'''获取队伍在哪个分组
		'''
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if teamId in lTeamId:
					return iGroupId,iIndex
		return None,None

	def getGroupIndexByLv(self, iLv):
		'''获取个人积分排行榜分组
		'''
		dGroupConfig = self.getConfigInfo("分组名称")
		for iIndex, sGroupName in dGroupConfig.iteritems():
			tGroupLv = self.getConfigInfo(sGroupName)
			if tGroupLv[0] <= iLv <= tGroupLv[1]:
				return iIndex
		return 0

	def removeFormGroup(self, teamId):
		'''从分组中删除队伍
		'''
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if teamId in lTeamId:
					self.log("removeFormGroup|{}|{}|{}".format(teamId, iGroupId, iIndex))
					self.dGroupInfo[iGroupId][iIndex].remove(teamId)
					self.changeTeamCount(iGroupId, iIndex)
					return

	def createRaceSceneByGroup(self):
		'''根据分组情况创建场景
		'''
		dGroupConfig = self.getConfigInfo("分组名称")
		self.dRaceSceneObj = {}
		for iGroupId,sGroupName in dGroupConfig.iteritems():
			self.dRaceSceneObj[iGroupId] = {}

		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if not lTeamId:
					continue
				sceneObj = self.createRaceScene()
				self.dRaceSceneObj[iGroupId][iIndex] = sceneObj
				self.log("createRaceSceneByGroup|{}|{}".format(iGroupId,iIndex))

	def getRaceScene(self, iGroupId, iIndex):
		if iGroupId not in self.dRaceSceneObj:
			sGroupName = self.getGroupName(iGroupId)
			raise Exception,"组队竞技:{}分组场景不存在".format(sGroupName)
		if iIndex not in self.dRaceSceneObj[iGroupId]:
			sGroupName = self.getGroupName(iGroupId)
			raise Exception,"组队竞技:{}分组场景{}不存在".format(sGroupName, iIndex)
		return self.dRaceSceneObj[iGroupId][iIndex]

	def transRaceScene(self):
		'''把队伍传送到分组场景
		'''
		dTransGroup = {}
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			dTransGroup[iGroupId] = {}
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if not lTeamId:
					continue
				dTransGroup[iGroupId][iIndex] = []
				sceneObj = self.getRaceScene(iGroupId, iIndex)
				for iTeamId in lTeamId:
					teamObj = team.getTeam(iTeamId)
					if not teamObj:
						continue
					leaderObj = getRole(teamObj.leader)
					if not leaderObj:
						continue
					self.transfer(leaderObj, sceneObj.id, None, None)
					self.doScript(leaderObj, None, "TTP4008")
					dTransGroup[iGroupId][iIndex].append(iTeamId)
		self.log("transRaceScene|{}|{}".format(dTransGroup, self.dGroupInfo))
		self.dGroupInfo = dTransGroup


	def groupIsEnd(self, iGroupId, iIndex):
		'''判断某个分组是否已经结束
		'''
		if (iGroupId, iIndex) in self.dRaceWinRecord:
			return True
		return False

	def addGroupEnd(self, iGroupId, iIndex, iTeamId):
		'''增加分组结束记录
		'''
		self.dRaceWinRecord[(iGroupId, iIndex)] = iTeamId


	#=================================================
	#匹配战斗部分	
	def startMatch(self):
		'''20:05开始匹配，之后每隔5分钟匹配一次
		'''
		if not self.inMatchTime():
			return
		iEveryMatchTime = self.getConfigInfo("匹配时间间隔")
		self.timerMgr.run(self.startMatch, iEveryMatchTime, 0, "startMatch")

		self.match()

	def match(self):
		'''	匹配,只对同场景的队伍匹配，随机匹配
			除非场景中只剩2个队伍，否则前一次失败的队伍不会再遇到前一次的对手
		'''
		bHasMatch = False
		self.openMatch()
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				self.dMatchFight[iGroupId][iIndex] = {}
				if self.groupIsEnd(iGroupId, iIndex):#已经结束
					continue
				result = self.autoMatch(iGroupId, iIndex)
				if result:
					bHasMatch = True
		if bHasMatch:
			self.startTimer(self.sendMatchInfo, 6, "sendMatchInfo")	#5秒后显示结果
			self.startTimer(self.matchFight, 12, "matchFight")	#5秒后进入战斗，延迟N秒

	def autoMatch(self, iGroupId, iIndex):
		'''同场景的匹配，除非场景中只剩2个队伍，否则前一次失败的队伍不会再遇到前一次的对手
		'''
		self.dMatchFight[iGroupId][iIndex] = []
		iCurrSecond = getSecond()
		lShuffleMatch = []

		lAllTeamId = copy.copy(self.dGroupInfo[iGroupId][iIndex])	#同场景所有队伍ID
		shuffleList(lAllTeamId)
		
		#每个队伍最后一次对战记录
		lLastRecord = self.dTeamLastRecord[iGroupId][iIndex].items()
		shuffleList(lLastRecord)
		for lTeamId in lLastRecord:
			bAppend = True
			for iTeamId in lTeamId:
				if iTeamId in self.dInFightTeamId:#正在战斗中
					continue
				if lShuffleMatch in iTeamId:
					continue
				if self.dFightEndCoolTime.get(iTeamId, 0) > iCurrSecond():	#冷却中
					continue
				if bAppend:
					lShuffleMatch.append(iTeamId)
					bAppend = False
				else:
					lShuffleMatch.insert(0, iTeamId)

		for iTeamId in lAllTeamId:
			if iTeamId in lShuffleMatch:
				continue
			if self.dFightEndCoolTime.get(iTeamId, 0) > iCurrSecond:	#冷却中
					continue
			iRankIndex = rand(len(lShuffleMatch))
			lShuffleMatch.insert(iRankIndex, iTeamId)

		self.dMatchFight[iGroupId][iIndex] = lShuffleMatch
		self.log("autoMatch|{},{}|lAllTeamId={}|lLastRecord={}|lShuffleMatch={}".format(iGroupId, iIndex, lAllTeamId, lLastRecord, lShuffleMatch))
		if lShuffleMatch:
			return True
		return False

	def matchFight(self):
		'''匹配结果进入战斗
		'''
		for iGroupId,dMatchInfo in self.dMatchFight.iteritems():
			for iIndex,lTeamMatchId in dMatchInfo.iteritems():
				iCnt = len(lTeamMatchId)
				for i in xrange(0, iCnt, 2):
					if i+1 >= iCnt:
						break 
					iTeamId1 = lTeamMatchId[i]
					iTeamId2 = lTeamMatchId[i+1]
					self.startWar(iGroupId, iIndex, iTeamId1, iTeamId2)
				self.dMatchFight[iGroupId][iIndex] = []
		self.closeMatchUi()
	#=================================================
	#战斗部分
	def begin(self):
		'''开始
		'''
		if self.state == TEAMRACE_BEGIN:
			return
		self.week.set("teamRace", 1)
		self.state = TEAMRACE_BEGIN
		self.deleteRaceNpc()
		self.removeRaceScene()
		# self.addTermNo(1)
		self.groupByLv()
		self.createRaceSceneByGroup()
		self.transRaceScene()
		self.removeReadyScene()
		self.beginInit()
		iEveryMatchTime = self.getConfigInfo("匹配时间间隔")
		self.timerMgr.run(self.startMatch, iEveryMatchTime, 0, "startMatch")

		for iGroupId,dGroupScene in self.dRaceSceneObj.iteritems():
			for iIndex,sceneObj in dGroupScene.iteritems():
				for roleId in sceneObj.getRoleList():
					who = getRole(roleId)
					if not who:
						continue
					rpcTeamRaceEnter(self, who)
					rpcTeamRaceInfo(self, who)

					#加活跃
					if who.day.fetch("teamRaceEnter", 0):
						who.day.set("teamRaceEnter", 1)
						perPoint = activity.center.getPerActPoint(24)
						who.addActPoint(perPoint)

		#如果分组只有一队该队就自动结束
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				self.tryGroupEnd(iGroupId, iIndex)

	def beginInit(self):
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			self.dTeamLastRecord[iGroupId] = {}
			self.dMatchFight[iGroupId] = {}
			for iIndex,lTeamId in dGroupInfo.iteritems():
				self.dTeamLastRecord[iGroupId][iIndex] = {}
				self.dMatchFight[iGroupId][iIndex] = []

	def end(self):
		'''结束
		'''
		# if self.state not in (TEAMRACE_BEGIN, TEAMRACE_READY):
		# 	return
		self.state = TEAMRACE_END
		self.log("end start|{}|{}".format(self.dGroupInfo, self.dRaceWinRecord))
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if not self.groupIsEnd(iGroupId,iIndex):
					#还没分出冠军的场
					self.groupWarHaltEnd(lTeamId)

		self.haltRaceEnd()
		self.log("end end|{}|{}".format(self.dGroupInfo, self.dRaceWinRecord))
		self.stopAllRaceTimer()
		self.timerMgr.run(self.delayDuel, 1, 0, "delayDuel")

	def delayDuel(self):
		'''清理
		'''
		self.deleteRaceNpc()
		self.removeReadyScene()
		self.removeRaceScene()
		self.reset()

	def tryEnd(self):
		'''检查是否所有都结束了
		'''
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if not lTeamId:	#没有队伍了
					continue
				if not self.groupIsEnd(iGroupId,iIndex):
					#还有没分出冠军
					return
		self.end()

	def tryGroupEnd(self, iGroupId, iIndex):
		'''尝试结束某组
		'''
		# if not self.inNormalTime():
		# 	return
		if self.groupIsEnd(iGroupId,iIndex):
			return
		lTeamId = self.dGroupInfo[iGroupId][iIndex]
		if not lTeamId or len(lTeamId) > 1:
			return

		winnerTeamId = lTeamId[0]
		if winnerTeamId in self.dInFightTeamId:	#还在战斗，战斗结束再判断
			return
		self.log("tryGroupEnd|{}|{}|{}".format(iGroupId,iIndex,winnerTeamId))
		self.raceWin(iGroupId, iIndex, winnerTeamId)
		self.closeGroupMatchUi(iGroupId, iIndex)

	def startWar(self, iGroupId, iIndex, iTeamId1, iTeamId2):
		'''开始战斗
		'''
		teamObj1 = team.getTeam(iTeamId1)
		teamObj2 = team.getTeam(iTeamId2)
		if not teamObj1 or not teamObj2:
			self.log("start War|not find teamObj|{}|{}".format(iTeamId1, iTeamId2))
			return
		leaderObj1 = getRole(teamObj1.leader)
		leaderObj2 = getRole(teamObj2.leader)
		if not leaderObj1 or not leaderObj2:
			self.log("start War|not find team leader|{},{}|{},{}".format(iTeamId1, teamObj1.leader, iTeamId2, teamObj2.leader))
			return
		warObj = war.warctrl.createPKWar(leaderObj1, leaderObj2, self)

		self.dTeamLastRecord[iGroupId][iIndex][iTeamId1] = iTeamId2
		self.dTeamLastRecord[iGroupId][iIndex][iTeamId2] = iTeamId1

		warObj.teamReaceInfo = {
			TEAM_SIDE_1: {
				"teamId": teamObj1.id,
				"leaderId": leaderObj1.id,
				"leaderName": leaderObj1.name,

			},
			TEAM_SIDE_2: {
				"teamId": teamObj2.id,
				"leaderId": leaderObj2.id,
				"leaderName": leaderObj2.name,
			},	
		}
		self.dInFightTeamId[iTeamId1] = 1
		self.dInFightTeamId[iTeamId2] = 1

		self.addCountFight(teamObj1, 1)
		self.addCountFight(teamObj2, 1)
		self.log("startWar|{},{}|{},{}|{},{}".format(iGroupId, iIndex, leaderObj1.id, teamObj1.id, leaderObj2.id, teamObj2.id))

	def groupWarHaltEnd(self, lTeamId):
		'''结束每组的战斗
		'''
		for iTeamId in lTeamId:
			teamObj = team.getTeam(iTeamId)
			if not teamObj:
				continue
			leaderObj = getRole(teamObj.leader)
			if not leaderObj:
				continue
			if not leaderObj.inWar():
				continue

			w = leaderObj.warrior
			if w:
				warObj = w.war
				if warObj:
					self.customWarHaltEnd(warObj)

	def customWarHaltEnd(self, warObj):
		'''结束战斗
		'''
		teamReaceInfo = getattr(warObj, "teamReaceInfo", None)
		if not teamReaceInfo:
			return
		self.log("warHaltEnd|{}".format(teamReaceInfo))
		winner = self.customWarResult(warObj)
		warObj.winner = winner
		warObj.isEnd = True
		warObj.end()

	def customWarResult(self, warObj):
		'''强制结束战斗：
			如果在22:00还有队伍在战斗，则人数多的胜利(活着的玩家和宠物)，如相同，
			则生命多的胜利，如相同，则整体实力高的胜利，
			如相同，则队长ID小的胜利
		'''
		dWarriorCnt = {TEAM_SIDE_1:0, TEAM_SIDE_2:0}	#人数
		dWarriorHp = {TEAM_SIDE_1:0, TEAM_SIDE_2:0}		#生命
		for side in warObj.teamList:
			for w in warObj.teamList[side].values():
				if not (w.isRole() or w.isPet()):
					continue
				if w.isDead():
					continue
				dWarriorCnt[side] += 1
				dWarriorHp[side] += w.hp
		#人数
		if dWarriorCnt[TEAM_SIDE_1] > dWarriorCnt[TEAM_SIDE_2]:
			return TEAM_SIDE_1
		elif dWarriorCnt[TEAM_SIDE_1] < dWarriorCnt[TEAM_SIDE_2]:
			return TEAM_SIDE_2
		#生命
		if dWarriorHp[TEAM_SIDE_1] > dWarriorHp[TEAM_SIDE_2]:
			return TEAM_SIDE_1
		elif dWarriorHp[TEAM_SIDE_1] < dWarriorHp[TEAM_SIDE_2]:
			return TEAM_SIDE_2

		#综合实力
		dRoleScore = {TEAM_SIDE_1:0, TEAM_SIDE_2:0}		#生命
		for side in warObj.teamList:
			for w in warObj.teamList[side].values():
				who = getRole(w.getPID())
				if not who:
					continue
				dRoleScore[side] += grade.gradeAll(who)

		if dRoleScore[TEAM_SIDE_1] > dRoleScore[TEAM_SIDE_2]:
			return TEAM_SIDE_1
		elif dRoleScore[TEAM_SIDE_1] < dRoleScore[TEAM_SIDE_2]:
			return TEAM_SIDE_2

		#队长ID
		leaderId1 = warObj.teamReaceInfo[TEAM_SIDE_1]["leaderId"]
		leaderId2 = warObj.teamReaceInfo[TEAM_SIDE_2]["leaderId"]
		if leaderId1 < leaderId2:
			return TEAM_SIDE_1
		return TEAM_SIDE_2

	def haltRaceEnd(self):
		'''	如果在22:00还有场景未决出第一名，则胜利场次最多的队伍获胜，如果场次相同，
			则整体实力高的队伍获胜，如相同，则队长ID小的胜利
		'''
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if not lTeamId:
					continue
				if self.groupIsEnd(iGroupId,iIndex):
					continue
				self.customGroupRaceEnd(iGroupId, iIndex)

	def customGroupRaceEnd(self, iGroupId, iIndex):
		'''	如果在22:00还有场景未决出第一名，则胜利场次最多的队伍获胜，如果场次相同，
			则整体实力高的队伍获胜，如相同，则队长ID小的胜利
		'''
		winnerTeamId = 0
		#胜利场次
		dWinCnt = {}
		lTeamId = self.dGroupInfo[iGroupId][iIndex]
		for iTeamId in lTeamId:
			dWinCnt[iTeamId] = self.getWinCnt(iTeamId)
		if dWinCnt:
			winnerTeamId = max(dWinCnt)

		if not winnerTeamId:#整体实力
			dRoleScore = {}
			for iTeamId in lTeamId:
				teamObj = team.getTeam(iTeamId)
				if not teamObj:
					continue
				dRoleScore[iTeamId] = self.getTeamScore(teamObj.id)
			if dRoleScore:
				winnerTeamId = max(dRoleScore)

		if not winnerTeamId:#队长ID
			for iTeamId in lTeamId:
				teamObj = team.getTeam(iTeamId)
				if not teamObj:
					continue
				lTeamLeaderId.append(teamObj.leader)
			lTeamLeaderId.sort()
			winnerTeamId = lTeamLeaderId[0]
		self.log("customGroupRaceEnd|{}|{}|{}".format(iGroupId, iIndex, winnerTeamId))
		self.raceWin(iGroupId, iIndex, winnerTeamId) 

	def addWinRecord(self, teamId):
		'''增加胜利次数
		'''
		self.dTeamWinRecord[teamId] = self.dTeamWinRecord.get(teamId, 0) + 1 

	def getWinCnt(self, teamId):
		'''胜利次数
		'''
		return self.dTeamWinRecord.get(teamId, 0)

	def warWin(self, warObj, npcObj, warriorList):
		'''战斗胜利时
		'''
		customActivity.warWin(self, warObj, npcObj, warriorList)

		iTeamId = warObj.teamReaceInfo[warObj.winner]["teamId"]
		teamObj = team.getTeam(iTeamId)
		if not teamObj:
			return

		leaderObj = getRole(teamObj.leader)
		#奖励
		if leaderObj:
			self.doScript(leaderObj, None, "TR1002")
		
		self.addCountWin(teamObj, 1)
		self.log("onWarWin|{}".format(iTeamId))
		#增加胜利次数
		self.addWinRecord(iTeamId)
		teamObj.teamRaceLastResult = WAR_WIN

		#战报
		result = '你战胜了{}带领的队伍！'.format(warObj.teamReaceInfo[warObj.winner^1]["leaderName"])
		self.addFightInfo(teamObj, result)
		teamObj.teamRaceFightEndTime = getSecond()
		#积分
		for roleId in teamObj.getInTeamList():
			who = getRole(roleId)
			if not who:
				continue
			who.day.add("teamRaceActPoint", 10)
			self.updateTeamRaceActRank(who)
			who.addTeamRacePoint(10, "组队竞技场")
			rank.updateTeamRacePointRank(who)
		# 刷新数据给客户端
		rpcTeamRaceInfoChange(self, teamObj, "countFight", "countWin", "racePoint")

	def warFail(self, warObj, npcObj, warriorList):
		'''战斗失败时
		'''
		customActivity.warFail(self, warObj, npcObj, warriorList)
		iTeamId = warObj.teamReaceInfo[warObj.winner^1]["teamId"]
		teamObj = team.getTeam(iTeamId)
		if not teamObj:
			return
		leaderObj = getRole(teamObj.leader)
		#奖励
		if leaderObj:
			self.doScript(leaderObj, None, "TR1003")
		# 刷新数据给客户端
		rpcTeamRaceInfoChange(self, teamObj, "countFight")

		#战报
		result = '你被{}带领的队伍击败了。'.format(warObj.teamReaceInfo[warObj.winner]["leaderName"])
		self.addFightInfo(teamObj, result)

		#0:没有战斗 1：胜利 2：失败
		iLastWarResult = getattr(teamObj, "teamRaceLastResult", NO_WAR)	#上一场战斗结果
		self.log("onWarFail|{}|{}".format(iTeamId, iLastWarResult))
		if iLastWarResult == WAR_FAIL:
			#战斗失败2次则直接退出场景
			self.raceFail(teamObj)
		else:
			teamObj.teamRaceLastResult = WAR_FAIL

	def raceFail(self, teamObj):
		'''连续两次失败，直接退出场景
		'''
		teamId = teamObj.id
		self.log("raceFail|{}".format(teamId))
		self.removeFormGroup(teamObj.id)
		leaderObj = getRole(teamObj.leader)
		if leaderObj:
			self.leaveScene(leaderObj)
		self.dAllTeamId.pop(teamObj.id, None)

	def warEnd(self, warObj, npcObj):
		'''战斗结束
		'''
		teamReaceInfo = warObj.teamReaceInfo
		self.log("warEnd|{}".format(teamReaceInfo))
		winnerTeamId = teamReaceInfo[warObj.winner]["teamId"]
		failTeamId = teamReaceInfo[warObj.winner^1]["teamId"]
		self.dInFightTeamId[winnerTeamId] = 0
		self.dInFightTeamId[failTeamId] = 0
		self.checkRaceEnd(winnerTeamId)

		#战斗结束时，显示冷却倒数，胜利方5秒倒数，失败方10秒倒数：“匹配冷却：10”
		iCurrSecond = getSecond()
		self.dFightEndCoolTime[winnerTeamId] = iCurrSecond + 5
		self.dFightEndCoolTime[failTeamId] = iCurrSecond + 10

	def checkRaceEnd(self, teamId):
		'''	检查本场景是否结束了
			当场景中只剩下一个队伍时，本场景结束，该队伍请出场外，同时在系统发布传闻
		'''
		iGroupId,iIndex = self.getTeamGroup(teamId)
		if not iGroupId or not iIndex:
			return
		lTeamId = self.dGroupInfo[iGroupId][iIndex]
		if not lTeamId or len(lTeamId) > 1:
			return
		winnerTeamId = lTeamId[0]
		self.log("checkRaceEnd|{}|{}|{}".format(iGroupId,iIndex,winnerTeamId))
		self.raceWin(iGroupId, iIndex, winnerTeamId)

	def raceWin(self, iGroupId, iIndex, teamId):
		'''胜利
		'''
		if self.groupIsEnd(iGroupId,iIndex):
			return
		self.dAllTeamId.pop(teamId, None)
		teamObj = team.getTeam(teamId)
		if not teamObj:
			return
		leaderObj = getRole(teamObj.leader)
		if not leaderObj:
			return

		#奖励
		self.doScript(leaderObj, None, "TR1004")
		#称谓
		dTitleNo = self.getConfigInfo("冠军称谓")
		iTitleNo = dTitleNo.get(iGroupId, 0)
		if iTitleNo:
			for roleId in teamObj.getInTeamList():
				roleObj = getRole(roleId)
				if roleObj:
					title.newTitle(roleObj, iTitleNo)

		self.log("raceWin|{}|{}|{}".format(iGroupId,iIndex,teamId))
		self.addGroupEnd(iGroupId, iIndex, teamId)
		self.leaveScene(leaderObj)

		#系统发布传闻
		message.sysMessage((self.getText(4015, 0, endGroup=(iGroupId, iIndex))))

		self.tryEnd()

	#==============================================
	#积分部分
	def calcAttrTeamRacePoint(self, dTeamRacePoint):
		'''最近4周的竞技积分会按照时间乘以系数得到的总和
		'''
		dPointFactor = self.getConfigInfo("竞技积分系数")
		weekNo = getWeekNo()
		point = 0
		for _weekNo,val in dTeamRacePoint.iteritems():
			diff = weekNo - _weekNo
			point += dPointFactor.get(diff, 0) * val
		return int(point/100)

	def checkTeamRacePoint(self, dTeamRacePoint):
		'''只保存最近4周的组队竞技积分
		'''
		weekNo = getWeekNo()
		lTemp = []
		for _weekNo in dTeamRacePoint:
			if weekNo - _weekNo > 4:
				lTemp.append(_weekNo)
		if lTemp:
			for _weekNo in lTemp:
				dTeamRacePoint.pop(_weekNo, None)
			return True
		return False
	#===============================================
	#
	#下一分距离现在多少秒
	def howManySecondNextMinu(self):
		date = getDatePart()

		lEndTime = []
		lEndTime.append(date["year"])	#年
		lEndTime.append(date["month"])	#月
		lEndTime.append(date["day"])	#日
		lEndTime.append(date["hour"])	#时
		lEndTime.append(date["minute"]+1)#分
		lEndTime.append(0)				#秒

		iEndTime = getSecond(*lEndTime)
		iLeftTime = iEndTime - getSecond()
		return iLeftTime

	def setNewMinuReward(self):
		'''从进场到第三场战斗结束为主，非战斗状态下，每1分钟整点给经验
		'''
		if not self.inRewardTime():
			return
		iLeftTime = self.howManySecondNextMinu()
		self.timerMgr.run(self.newMinuReward, iLeftTime, 0, "newMinuReward")

	def inRewardTime(self):
		'''匹配时间，19:40--22:00
		'''
		if gbTeamRaceDebug:
			return True
		datePart = getDatePart()
		wday = datePart["wday"]
		hour = datePart["hour"]
		minute = datePart["minute"]
		if wday != 5:
			return False
		if (hour >= 19 and minute >= 40) and hour < 22:
			return True
		return False

	def newMinuReward(self):
		'''从进场到第三场战斗结束为主，非战斗状态下，每1分钟整点给经验
			观战不属于战斗
		'''
		if not self.inRewardTime():
			return
		self.setNewMinuReward()
		# self.log("newMinuReward")
		for iTeamId in self.dAllTeamId:
			if self.dInFightTeamId.get(iTeamId, 0):
				continue
			teamObj = team.getTeam(iTeamId)
			if not teamObj:
				continue
			for roleId in teamObj.getInTeamList():
				roleObj = getRole(roleId)
				if not roleObj:
					continue
				self.doScript(roleObj, None, "TR1001")

	def teamKick(self, teamObj, roleId):
		'''被踢出队伍时，传出场景
		'''
		self.resetTeamScore(teamObj.id)
		if roleId not in self.dAllRoleId:
			return
		who = getRole(roleId)
		if not who:
			return
		self.leaveScene(who)

	def matchCoolTime(self, iTeamId):
		'''冷却倒数时间
		'''
		iCurrSecond = getSecond()
		iCoolTime = self.dFightEndCoolTime.get(iTeamId, 0)
		return max(0, iCoolTime-iCurrSecond)

	def openMatch(self):
		'''打开匹配界面
		'''
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				if self.groupIsEnd(iGroupId, iIndex):#已经结束
					continue
				for iTeamId in lTeamId:
					if iTeamId in self.dInFightTeamId:#正在战斗中
						continue
					teamObj = team.getTeam(iTeamId)
					if teamObj:
						rpcTeamRaceOpenMatch(self, teamObj)

	def closeMatchUi(self):
		'''关闭所有匹配界面
		'''
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				for iTeamId in lTeamId:
					if iTeamId not in self.dInFightTeamId:#不在战斗中
						continue
					teamObj = team.getTeam(iTeamId)
					if teamObj:
						rpcTeamRaceCloseMatch(self, teamObj)

	def closeGroupMatchUi(self, iGroupId, iIndex):
		'''关闭某组匹配界面
		'''
		lTeamId = self.dGroupInfo[iGroupId][iIndex]
		for iTeamId in lTeamId:
			if iTeamId not in self.dInFightTeamId:#不在战斗中
				continue
			teamObj = team.getTeam(iTeamId)
			if teamObj:
				rpcTeamRaceCloseMatch(self, teamObj) 

	def sendMatchInfo(self):
		dTempMatch = {}
		for iGroupId,dMatchInfo in self.dMatchFight.iteritems():
			dTempMatch[iGroupId] = {}
			for iIndex,lTeamMatchId in dMatchInfo.iteritems():
				dTempMatch[iGroupId][iIndex] = []
				iCnt = len(lTeamMatchId)
				for i in xrange(0, iCnt, 2):
					if i+1 >= iCnt:
						break 
					iTeamId1 = lTeamMatchId[i]
					iTeamId2 = lTeamMatchId[i+1]
					teamObj1 = team.getTeam(iTeamId1)
					teamObj2 = team.getTeam(iTeamId2)
					if not teamObj1 or not teamObj2:
						continue
					rpcTeamRaceMatchInfo(self, teamObj1, teamObj2)
					dTempMatch[iGroupId][iIndex].append(iTeamId1)
					dTempMatch[iGroupId][iIndex].append(iTeamId2)

					
		#没有匹配到的关闭界面
		for iGroupId,dGroupInfo in self.dGroupInfo.iteritems():
			for iIndex,lTeamId in dGroupInfo.iteritems():
				lMatch = dTempMatch[iGroupId][iIndex]
				for iTeamId in lTeamId:
					if iTeamId in lMatch:
						continue
					teamObj = team.getTeam(iTeamId)
					if not teamObj:
						continue
					noMatchCloseUi(self, teamObj)

	def getTeamCountByTeam(self, teamObj):
		iGroupId,iIndex = self.getTeamGroup(teamObj.id)
		if not iGroupId or not iIndex:
			return None
		return self.getTeamCountByIndex(iGroupId, iIndex)

	def getTeamCountByIndex(self, iGroupId, iIndex):
		lTeamId = self.dGroupInfo[iGroupId][iIndex]
		return len(lTeamId)

	def changeTeamCount(self, iGroupId, iIndex):
		lTeamId = self.dGroupInfo[iGroupId][iIndex]
		teamCount = len(lTeamId)
		for iTeamId in lTeamId:
			teamObj = team.getTeam(iTeamId)
			if not teamObj:
				continue
			changeAllTeamCount(self, teamObj, teamCount)
	
	#===============================================
	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 100:
			txtList = []
			txtList.append("101-活动预告")
			txtList.append("102-开始活动")
			txtList.append("103-结束活动")
			txtList.append("104-匹配")
			#txtList.append("105-开始给经验")
			txtList.append("106-清空进场记录")
			txtList.append("108-设置准备室数量")
			txtList.append("109-设置准备室队伍数量")
			txtList.append("110-设置等级段队伍数量")
			txtList.append("111-设置多开队伍数量")
			txtList.append("112-设置合并判断数量")
			txtList.append("113-查看配置")
			txtList.append("114-清空积分")
			txtList.append("200-时间设置7点半前，开始挂定时器")
			message.dialog(who, "\n".join(txtList))

		elif cmdIdx == 101:
			self.week.set("teamRace", 0)
			self.readyStart()
			self.setNewMinuReward()

		elif cmdIdx == 102:
			self.begin()

		elif cmdIdx == 103:
			self.end()

		elif cmdIdx == 104:
			self.startMatch()

		elif cmdIdx == 105:
			self.setNewMinuReward()

		elif cmdIdx == 106:
			self.dEnterRaceRoleId = {}

		elif cmdIdx == 107:
			self.quitTeamRace(who)

		elif cmdIdx == 108:
			count = int(args[0])
			self.configInfo["准备室数量"] = count
		elif cmdIdx == 109:
			count = int(args[0])
			self.configInfo["准备室队伍数量"] = count
		elif cmdIdx == 110:
			count = int(args[0])
			self.configInfo["等级段队伍数量"] = count
		elif cmdIdx == 111:
			count = int(args[0])
			self.configInfo["多开队伍数量"] = count
		elif cmdIdx == 112:
			count = int(args[0])
			self.configInfo["合并判断数量"] = count

		elif cmdIdx == 113:
			txtList = []
			for k,v in self.configInfo.iteritems():
				txtList.append("{}:{}".format(k, v))
			message.dialog(who, "\n".join(txtList))

		elif cmdIdx == 114:#清空积分
			who.delete("teamRacePoint")
			who.day.delete("teamRaceActPoint")

		elif cmdIdx == 200:
			self.week.set("teamRace", 0)
			self.setCreateRaceNpcTimer()

		elif cmdIdx == 400:
			self.begin()
			self.startMatch()

		elif cmdIdx == 401:
			for iIndex, rankObj in self.dTeamRaceActRank.iteritems():
				self.log("rank|{}|{}".format(iIndex, rankObj.lRanking))

		elif cmdIdx == 402:
			# global gbTeamRaceDebug
			gbTeamRaceDebug = False

		elif cmdIdx == 403:
			# global gbTeamRaceDebug
			gbTeamRaceDebug = True

		elif cmdIdx == 404:
			self.week.set("teamRace", 0)
		

class cTeamRaceNpc(activity.object.Npc):
	
	def doLook(self, who):
		content = self.game.getText(4009)#self.getChat()
		selList = [1,2]
		content += '''
Q参加活动
Q规则说明'''
		
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)

	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		sel = selList[selectNo-1]
		if sel == 1:
			self.enterRace(who)
		elif sel == 2:
			#弹出规则界面
			# self.game.doScript(who, self, "D4014")
			openUIPanel.openCommonTips(who, 3019)
			
	def enterRace(self, who):
		'''进入竞技场
		'''
		teamObj = who.getTeamObj()
		if not self.game.inEnterTime():
			self.game.doScript(who, self, "D4010")
			return
		if not who.validInTeamSize(1):
			self.game.doScript(who, self, "D4011")
			return
		if teamObj.size != teamObj.inTeamSize:
			message.tips(who, "请先召回暂离队员才能进入副本")
			return False
		if not self.game.checkTeamMemberLv(teamObj):
			self.game.doScript(who, self, "D4012")
			return
		if not self.game.checkTeamMemberState(teamObj):
			self.game.doScript(who, self, "D4013")
			return

		#进场
		self.game.enterReadyScene(who, teamObj)



def getActivity():
	return activity.getActivity("teamRace")

# ================================================================
# 客户端发往服务端
# ================================================================

def rpcTeamRaceQuit(who, reqMsg):
	actObj = getActivity()
	actObj.quitTeamRace(who)

def rpcTeamRaceRankGet(who, reqMsg):
	'''请求竞技排行榜数据
	'''
	actObj = getActivity()
	iPage = reqMsg.iValue if reqMsg else 1
	sendTeamRaceActRank(actObj, who, iPage)

#===============================================================================
# 服务端发往客户端
#===============================================================================
def packetRankInfo(rankObj, iUid):
	msg = act_teamRace_pb2.rankMsg()
	msg.rankNo = rankObj.getRank(iUid)
	msg.name = rankObj.getRoleName(iUid)
	msg.schoolName = rankObj.title3(iUid)
	msg.teamRacePoint = rankObj.getValue(iUid)
	msg.iUid = iUid
	return msg

def packetMyInfo(who, tMyInfo):
	msg = act_teamRace_pb2.rankMsg()
	msg.rankNo = tMyInfo[0]
	msg.name = tMyInfo[1]
	msg.schoolName = tMyInfo[2]
	msg.teamRacePoint = tMyInfo[3]
	msg.iUid = who.id
	return msg

def sendTeamRaceActRank(actObj, who, iPage):
	'''发送竞技排行榜数据
	'''
	rankObj = actObj.getTeamRaceActRank(who)
	if not rankObj:
		return
	iStart = (iPage-1)*20
	iEnd = min(100, iPage*20)
	lRank = rankObj.ranking()[iStart:iEnd]
		
	#排行榜数据
	msgObj = act_teamRace_pb2.rankAllMsg()
	msgObj.rankList.extend([packetRankInfo(rankObj, iUid) for iUid in lRank])
	
	tMyInfo = rankObj.getMyRankInfo(who)
	msgObj.rankMy.CopyFrom(packetMyInfo(who, tMyInfo))

	who.endPoint.rpcTeamRaceRankSend(msgObj)

def rpcTeamRaceEnter(actObj, who):
	'''进入竞技场
	'''
	timeout = actObj.getLeftTime()
	msg = {
		"timeout": timeout,
		"state": actObj.state,
	}
	who.endPoint.rpcTeamRaceEnter(**msg)

def rpcTeamRaceEnd(actObj, who):
	'''结束竞技
	'''	
	who.endPoint.rpcTeamRaceEnd()

def rpcTeamRaceInfo(actObj, who):
	'''显示竞技信息
	'''
	teamObj = who.getTeamObj()
	if not teamObj:
		return
	raceInfo = actObj.getTeamRaceInfo(teamObj.id)
	if not raceInfo:
		return
	msg = {
		"countWin": raceInfo["countWin"], # 胜利场数
		"countFight": raceInfo["countFight"], # 战斗场数
		"racePoint": who.day.fetch("teamRaceActPoint", 0), # 竞技积分
	}
	who.endPoint.rpcTeamRaceInfo(**msg)

def rpcTeamRaceTeamCount(actObj, who):
	teamObj = who.getTeamObj()
	if not teamObj:
		return

	teamCount = actObj.getTeamCountByTeam(teamObj)
	if not teamCount:
		return
	# who.endPoint.rpcTeamRaceTeamCount(teamCount)

def changeAllTeamCount(actObj, teamObj, teamCount):
	for roleId in teamObj.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		# who.endPoint.rpcTeamRaceTeamCount(teamCount)

def rpcTeamRaceFightInfoList(actObj, who):
	'''发送全部战报
	'''
	teamObj = who.getTeamObj()
	if not teamObj:
		return
	raceInfo = actObj.getTeamRaceInfo(teamObj.id)
	if not raceInfo:
		return

	infoList = []
	for fightInfo in raceInfo["fightInfoList"]:
		infoList.append(packetFightInfo(fightInfo))
		
	if not infoList:
		return
		
	msgObj = act_teamRace_pb2.fightInfoList()
	msgObj.infoList.extend(infoList)
	who.endPoint.rpcTeamRaceFightInfoList(msgObj)

def packetFightInfo(fightInfo):
	msgObj = act_teamRace_pb2.fightInfo()
	msgObj.time = fightInfo["time"]
	msgObj.times = fightInfo["times"]
	msgObj.result = fightInfo["result"]
	return msgObj

def rpcTeamRaceFightInfoAdd(actObj, teamObj, fightInfo):
	'''增加战报
	'''
	msgObj = packetFightInfo(fightInfo)

	for roleId in teamObj.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		who.endPoint.rpcTeamRaceFightInfoAdd(msgObj)

def rpcTeamRaceInfoChange(actObj, teamObj, *attrNames):
	'''修改竞技信息
	'''
	for roleId in teamObj.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		dRoleRaceInfo = actObj.getRoleRaceInfo(roleId)
		if not dRoleRaceInfo:
			continue
		msg = {}
		for attrName in attrNames:
			if attrName == "racePoint":
				attrVal = who.day.fetch("teamRaceActPoint", 0)
			else:
				attrVal = dRoleRaceInfo[attrName]
			msg[attrName] = attrVal

		who.endPoint.rpcTeamRaceInfoChange(**msg)

def rpcTeamRaceOpenMatch(actObj, teamObj):
	'''打开匹配界面
	'''
	msg = act_teamRace_pb2.openMatch()
	msg.coolTime = actObj.matchCoolTime(teamObj.id)
	lRoleMsg = packageTeamRoleInfo(teamObj)
	msg.myTeamRoleInfo.extend(packageTeamRoleInfo(teamObj))

	for roleId in teamObj.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		who.endPoint.rpcTeamRaceOpenMatch(msg)

def rpcTeamRaceCloseMatch(actObj, teamObj):
	'''关闭匹配界面
	'''
	for roleId in teamObj.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		who.endPoint.rpcTeamRaceCloseMatch()

def packageRoleInfo(who):
	msg = act_teamRace_pb2.roleInfo()
	msg.roleId = who.id
	msg.name = who.name
	msg.shape = who.shape
	msg.level = who.level
	msg.school = who.school
	msg.fightPower = who.fightPower
	return msg

def packageTeamRoleInfo(teamObj):
	lRoleMsg = []
	for roleId in teamObj.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		lRoleMsg.append(packageRoleInfo(who))
	return lRoleMsg

def packageMatchRoleInfo(teamObj):
	lRoleMsg = packageTeamRoleInfo(teamObj)
	msgObj = act_teamRace_pb2.matchInfo()
	msgObj.roleInfoList.extend(lRoleMsg)
	return msgObj

def rpcTeamRaceMatchInfo(actObj, teamObj1, teamObj2):
	'''匹配对手信息
	'''
	msgObj1 = packageMatchRoleInfo(teamObj1)
	for roleId in teamObj2.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		who.endPoint.rpcTeamRaceMatchInfo(msgObj1)

	msgObj2 = packageMatchRoleInfo(teamObj2)
	for roleId in teamObj1.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		who.endPoint.rpcTeamRaceMatchInfo(msgObj2)

def noMatchCloseUi(actObj, teamObj):
	'''没有匹配到的关闭界面,全队玩家提示ID：4017 本轮匹配轮空
	'''
	for roleId in teamObj.getInTeamList():
		who = getRole(roleId)
		if not who:
			continue
		message.tips(who, actObj.getText(4017))
		who.endPoint.rpcTeamRaceCloseMatch()



import copy
from common import *
from war.defines import *
import activity
import message
import war.warctrl
import rank
import scene
import openUIPanel
import npc
import team
import grade
import act_teamRace_pb2
import title
import team.service
import team.platform
import team.platformservice
import cycleData