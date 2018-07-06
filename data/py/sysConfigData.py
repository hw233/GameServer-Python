#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
def getConfig(sVal,uDefault=0):
	if sVal not in gdData:
		raise PlannerError,'没有名为{}的变量'.format(sVal)
	return gdData[sVal].get('exps',uDefault)

#导表开始
gdData={
	"sDeath":{"exps":100,"memo":"单人副本内死亡一次扣除评分"},
	"sHit":{"exps":5,"memo":"单人连击单次增加评分"},
	"sTime":{"exps":2000,"memo":"单人通关耗时参数"},
	"sKill":{"exps":1000,"memo":"单人连杀率参数"},
	"tDeath":{"exps":100,"memo":"组队副本内死亡一次扣除评分"},
	"tHit":{"exps":5,"memo":"组队连击单次增加评分"},
	"tTime":{"exps":2000,"memo":"组队通关耗时参数"},
	"tKill":{"exps":1000,"memo":"组队连杀率参数"},
	"tDamage":{"exps":3000,"memo":"组队输出参数"},
	"maxDeath":{"exps":5,"memo":"评分封顶死亡次数"},
	"starSingle":{"exps":[(0,1100),(1101,1900),(1901,2600),(2601,3300),(3301,4400),(4401,2**32-1)],"memo":"单人评分对应星星数"},
	"starTeam":{"exps":[(0,1100),(1101,2500),(2501,3800),(3801,4750),(4751,8570),(8571,2**32-1)],"memo":"组队评分对应星星数"},
	"maxTime":{"exps":0.5,"memo":"评分保底时间比"},
	"minHit":{"exps":50,"memo":"评分保底连击数"},
	"minDam":{"exps":10,"memo":"评分保底杀伤率(10%)"},
	"unlock3star":{"exps":5,"memo":"解锁噩梦难度所需对应精英副本的通关星数"},
	"unlock4star":{"exps":5,"memo":"解锁地狱难度所需对应噩梦副本的通关星数"},
	"rFreeTime":{"exps":10,"memo":"免费转盘每日次数"},
	"rFreeCoolDown":{"exps":300,"memo":"免费转盘冷却时间(秒)"},
	"rFriendCoolDown":{"exps":300,"memo":"友情转盘冷却时间(秒)"},
	"rFriendCost":{"exps":10,"memo":"友情转盘消耗的友情点数"},
	"rDiaCoolDown":{"exps":300,"memo":"钻石转盘冷却时间(秒)"},
	"rDiaCost":{"exps":10,"memo":"钻石转盘消耗"},
	"rTacitStar":{"exps":{0:0,2000:1,5000:2,10000:3,20000:4,50000:5},"memo":"默契值的星星数"},
	"dEquipHole":{"exps":{1:0,2:2,3:4,4:6,5:8},"memo":"装备镶嵌孔"},
	"bornScene":{"exps":1010,"memo":"正式出生场景编号(普雷利镇)"},
	"bornAddr":{"exps":(333,333),"memo":"正式出生场景坐标(非新手引导副本)"},
	"bornBarrier":{"exps":1,"memo":"新手出生副本编号"},
	"dEquipEffect":{"exps":{0:0,10:1,20:2,30:3,40:4},"memo":"武器发光按照强化等级"},
	"sweepOpenLv":{"exps":12,"memo":"扫荡功能开启等级"},
	"star":{"exps":(3,{1:-1},-1),"memo":"(最大星星数,{死亡次数:死亡减少星数},超过预估时间减少星数)"},
	"iCanEnhance":{"exps":1311,"memo":"开启强化的关卡"},
	"dStar":{"exps":{0:1,1:1,2:1,3:1},"memo":"星星影响翻牌的参数"},
	"d3rdSkill":{"exps":{1:30801,2:30202},"memo":"角色第三个技能{职业:技能编号}"},
	"climbID":{"exps":14,"memo":"闯塔的ID"},
	"challenge":{"exps":30,"memo":"闯塔开启等级"},
}
#导表结束