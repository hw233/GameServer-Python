# -*- coding: utf-8 -*-

# 目标类型
TASK_TARGET_TYPE_NONE = 0  # 无
TASK_TARGET_TYPE_ITEM = 1  # 寻物
TASK_TARGET_TYPE_NPC = 2  # 寻人
TASK_TARGET_TYPE_NPC_MULTI = 21  # 寻多人
TASK_TARGET_TYPE_FIGHT = 3  # 巡逻战斗
TASK_TARGET_TYPE_PET = 4  # 寻宠
TASK_TARGET_TYPE_COLLECT = 5  # 采集

targetTypeDesc = {
	"无":"TASK_TARGET_TYPE_NONE",
	"寻物":"TASK_TARGET_TYPE_ITEM",
	"寻人":"TASK_TARGET_TYPE_NPC",
	"寻多人":"TASK_TARGET_TYPE_NPC_MULTI",
	"巡逻战斗":"TASK_TARGET_TYPE_FIGHT",
# 	"寻宠":"TASK_TARGET_TYPE_PET",,
	"采集":"TASK_TARGET_TYPE_COLLECT",
}

def getTargetTypeDesc(name):
	if name not in targetTypeDesc:
		raise Exception("错误的任务目标类型名")
	return targetTypeDesc[name]

#===============================================================================
# 任务Npc类型
#===============================================================================
TASK_NPC_TYPE_NORMAL = 0 # 正常
TASK_NPC_TYPE_IDLE = 1 # 闲人
TASK_NPC_TYPE_PROPS = 2 # 地上物品
