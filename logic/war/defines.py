# -*- coding: utf-8 -*-

# 战斗类型
WAR_COMMON = 0  # 普通战斗
WAR_PK = 1  # 玩家PK

# 战斗回合状态
TURN_STATE_NONE = 0 # 无
TURN_STATE_READY = 1 # 本轮准备，接受客户端下达出招指令
TURN_STATE_BEGIN = 2 # 本轮开始，设置AI，执行出招指令
TURN_STATE_END = 3 # 本轮结束，等待客户端播放动画

# 怪物类型
MONSTER_TYPE_NORMAL = 0  # 普通怪
MONSTER_TYPE_BOSS = 1  # 主怪
MONSTER_TYPE_FRIEND = 2  # 友军怪

# 站队
TEAM_SIDE_1 = 0  # 站队1
TEAM_SIDE_2 = 1  # 站队2

# 战士类型
WARRIOR_TYPE_NORMAL = 0  # 普通怪物
WARRIOR_TYPE_BOSS = 1  # Boss
WARRIOR_TYPE_ROLE = 2  # 玩家
WARRIOR_TYPE_PET = 3  # 宠物
WARRIOR_TYPE_WATCH = 4  # 观战
WARRIOR_TYPE_BUDDY = 5  # 助战伙伴
WARRIOR_TYPE_LINEUPEYE = 6  # 阵眼战士

# 战士状态
WARRIOR_STATUS_NORMAL = 0  # 正常
WARRIOR_STATUS_DEAD = 1  # 死亡

# 受击动作
ATTACKED_ACTION_NONE = 0 # 无
ATTACKED_ACTION_HIT = 1  # 被击中
ATTACKED_ACTION_DEFEND = 2  # 防御
ATTACKED_ACTION_DODGE = 3  # 躲闪
# ATTACKED_ACTION_DEAD = 4  # 死亡倒地
# ATTACKED_ACTION_REVIVE = 5  # 复活站立

# 受击效果
ATTACKED_EFFECT_CRIT = 1  # 暴击

# 攻击类型
ATTACK_TYPE_PHY = 1  # 普通物理攻击
ATTACK_TYPE_PERFORM_NONE = 20  # 法术.无
ATTACK_TYPE_PERFORM_MAG = 21  # 法术.魔法攻击
ATTACK_TYPE_PERFORM_PHY = 22  # 法术.物理近攻
ATTACK_TYPE_PERFORM_PHY_REMOTE = 23 # 法术.物理远攻

# 全部物理攻击类型列表
phyAttackTypeList = (ATTACK_TYPE_PHY, ATTACK_TYPE_PERFORM_PHY, ATTACK_TYPE_PERFORM_PHY_REMOTE)

TURN_TIME = 30  # 每轮时间
TURN_TIME_AUTO = 6 # 每轮自动间隔时间
MAX_BOUT = 255  # 回合数上限


# 特殊法术动画
MAGIC_PHY = 1  # 物理攻击
MAGIC_DEFEND = 2  # 防御
MAGIC_WAIT = 3  # 等待
MAGIC_PROTECT = 5  # 保护
MAGIC_ESCAPE_WIN = 6  # 逃跑成功
MAGIC_ESCAPE_FAIL = 7  # 逃跑失败
MAGIC_CAPTURE_WIN = 8  # 捕捉成功
MAGIC_CAPTURE_FAIL = 9  # 捕捉失败
MAGIC_SUMMON = 10  # 召唤
MAGIC_SUMMON_BACK = 11  # 召回
MAGIC_DIE = 12  # 死亡
MAGIC_USE_PROPS = 13  # 使用物品

magicNameList = {
	MAGIC_PHY: "物理攻击",
	MAGIC_DEFEND: "防御",
	MAGIC_WAIT: "等待",
	MAGIC_PROTECT: "保护",
	MAGIC_ESCAPE_WIN: "逃跑成功",
	MAGIC_ESCAPE_FAIL: "逃跑失败",
	MAGIC_CAPTURE_WIN: "捕捉成功",
	MAGIC_CAPTURE_FAIL: "捕捉失败",
	MAGIC_SUMMON: "召唤",
	MAGIC_SUMMON_BACK: "召回",
	MAGIC_DIE: "死亡",
	MAGIC_USE_PROPS: "使用物品",
}

# 指令类型
CMD_TYPE_PHY = 1  # 普通物理攻击
CMD_TYPE_MAG = 2  # 法术攻击
CMD_TYPE_SE = 3  # 特技攻击
CMD_TYPE_ITEM = 4  # 使用物品
CMD_TYPE_DEFEND = 5  # 防御
CMD_TYPE_WAIT = 6  # 等待
CMD_TYPE_PROTECT = 7  # 保护
CMD_TYPE_SUMMON = 8  # 召唤
CMD_TYPE_ESCAPE = 9  # 逃跑
CMD_TYPE_CAPTURE = 10  # 捕捉
CMD_TYPE_AI = 11  # AI指令

cmdTypeNameList = {
	CMD_TYPE_PHY: "物理攻击",
	CMD_TYPE_MAG: "法术攻击",
	CMD_TYPE_SE: "特技攻击",
	CMD_TYPE_ITEM: "使用物品",
	CMD_TYPE_DEFEND: "防御",
	CMD_TYPE_WAIT: "等待",
	CMD_TYPE_PROTECT: "保护",
	CMD_TYPE_SUMMON: "召唤",
	CMD_TYPE_ESCAPE: "逃跑",
	CMD_TYPE_CAPTURE: "捕捉",
}


# 战士站位
POS_ROLE = [1, 2, 3, 4, 5]  # 玩家
POS_MONSTER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # 怪物
POS_FRIEND = [1, 2, 3, 4, 5, 11, 12, 13, 14]  # 友军
POS_BUDDY = [1, 2, 3, 4, 5]  # 助战伙伴
POS_LINEUPEYE = [11,]  # 阵眼
