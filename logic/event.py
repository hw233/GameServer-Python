#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def increase():
	global i
	i+=1
	return i

if 'avoidHotUpdateFlag' not in globals():
	avoidHotUpdateFlag=True
	i=0

	CHAT									=increase()	#聊天,频道	参数:频道编号
	JOIN_GUILD								=increase()	#加入公会	参数:无
	TRADE									=increase()	#交易	参数:交易的物品信息{物品编号:数量,物品编号:数量,,,}
	WEAR_EQUIP								=increase()	#穿上装备 参数:装备类型
	EQUIP_ENHANCE							=increase()	#装备强化 参数:装备部位(可不填,为任意装备)
	EQUIP_DISSOLVE							=increase() #装备分解 参数:装备编号(可不填,为任意装备)
	EQUIP_STAR                              =increase() #装备升星 参数:装备编号(可不填,为任意装备)
	EQUIP_UNLOCK                            =increase() #背包解锁 参数:装备编号(可不填,为任意面板)
	EQUIP_INLAY                             =increase() #背包解锁 参数:装备编号(可不填,为任意面板)
	GEM_UGDATE                              =increase() #宝石合成
	EQUIP_MINT								=increase()	#装备铸造

	SKILL_UPLEVEL							=increase()	#技能升级 参数:技能编号
	BUY_ITEM_BILLING						=increase()	#在商城购买一个ib道具	参数:道具编号
	ENTER_FB								=increase()	#进入副本 参数:
	EXIT_FB									=increase()	#离开副本 参数:
	ROLE_UP									=increase()	#角色升级 参数:已升至的等级
	LOGIN									=increase()	#登录
	KILL_MONSTER							=increase()	#杀死一只怪物
	ATTACK_MONSTER							=increase() #攻击某只怪物
	PASS_FB									=increase()	#闯副本成功
	NPC_TALK								=increase()	#和npc对话
	MINE_TRIGGER							=increase() #触发地雷

	AUCTION_ON_SELL							=increase()	#拍卖物品上架
	AUCTION_OFF_SELL						=increase()	#拍卖物品下架
	COLLECT_GOODS							=increase()	#收集物品
	SUBTASK									=increase()	#子任务
	
	FIGHTING								=increase() #战斗力达到xxx
	FRIEND									=increase()	#好友数达到xxx
	USE_PROPS								=increase()	#使用一个道具	参数:道具编号
	USE_GOLD                                =increase() #使用元宝
	USE_DIAMOND                             =increase() #使用钻石
	GET_RENOEM								=increase()	#获取名望

	PVE										=increase() #挑战赛
	PVP										=increase() #竞技场
	ROULETTE								=increase() #大转盘
	PRAISE_OUT								=increase() #给别人点赞
	PRAISE_IN								=increase() #收取别人给点的赞
	HIRE_ACTIVE								=increase() #雇佣别人
	HIRE_PASSIVE							=increase() #被别人雇佣
	SHARE									=increase() #分享
	LV										=increase() #升级到xxx
	TOWER									=increase() #闯塔
	ANSWER									=increase()	#答题
	JOIN_WBOSS								=increase()	#参加屠龙活动
	FINISH_REWARD							=increase()	#完成悬赏任务

	PET_LV									=increase()	#宠物升级(特训)
	NEW_PET									=increase()	#获得新宠物
	PET_ADVANCE								=increase()	#宠物进阶

	NEW_EPIC								=increase()	#激活史诗英雄

	NEW_DUPLICATE							=increase()	#激活新的纹章组合

if 'gdEvent' not in globals():
	gdEvent={}

def addObserver(iEvent,func):#增加观察者
	if iEvent not in gdEvent:
		gdEvent[iEvent]=u.cEvent()
	gdEvent[iEvent]+=func



def removeObserver(iEvent,func):#清除观察者
	if iEvent not in gdEvent:
		return
	gdEvent[iEvent]-=func
	if gdEvent[iEvent].observerCount()<=0:#一个观察者都没,把事件也清掉吧
		gdEvent.pop(iEvent,None)


def triggerEvent(iEvent,*tArgs,**dArgs):#触发事件
	if iEvent in gdEvent:
		gdEvent[iEvent](iEvent,*tArgs,**dArgs)

		
		
import u