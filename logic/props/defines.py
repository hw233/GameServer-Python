# -*- coding: utf-8 -*-

#===============================================================================
# 物品类型
#===============================================================================
ITEM_COMMON = 0 # 普通物品
ITEM_EQUIP = 1 # 装备
ITEM_GEM = 2 # 宝石
ITEM_BOX = 3 # 宝箱
# ITEM_DRUG = 4
ITEM_MEDICINE = 5 # 基础药
ITEM_MEDICINE_LEVEL = 6 # 等级药
ITEM_MEDICINE_RES = 7 # 储备药
ITEM_FOOD = 8 # 食品
ITEM_MAKE = 9 # 制造符
ITEM_LINEUP_BOOK = 10 # 阵法书
ITEM_PET_SKILL_BOOK = 11 # 异兽技能书
ITEM_BUDDY = 12 #伙伴碎片

#===============================================================================
# 属性类型
#===============================================================================

dAttrType = {
	"con": 1,
	"mag": 2,
	"str": 3,
	"res": 4,
	"spi": 5,
	"dex": 6,
	
	"hp": 7,
	"mp": 8,
	"sp": 9,
	"fuwen": 10,
	"phyDam": 11,
	"magDam": 12,
	"cure": 16,
	"phyDef": 13,
	"magDef": 14,
	"phyCrit": 17,
	"magCrit": 18,
	"phyReCrit": 19,
	"magReCrit": 20,
	
	"phyRest": 21,
	"magRest": 22,

	"hpMax": 23,
	'mpMax': 24,
	"spe": 15,
	"quality":25,
	"pos":26,
	"sealHit":27,
	"reSealHit":28,
}

#===============================================================================
# 按钮类型
#===============================================================================
BUTTON_WEAR=1#穿上
BUTTON_DOFF=2#卸下
BUTTON_USE=3#使用
BUTTON_SELL=4#出售
BUTTON_RESOLVE=5#分解
BUTTON_COMPOUND=6#合成
BUTTON_DISCARD=7#丢弃
BUTTON_REPAIRED=8#修理
BUTTON_STORAGE_IN=9#移入仓库
BUTTON_STORAGE_OUT=10#移出仓库
BUTTON_INLAY=11#镶嵌
BUTTON_STALL=12#摆摊出售
BUTTON_OPEN=16#开启(礼包专用)
BUTTON_GETBACK=101#取出
BUTTON_USE_PET=102#对宠物使用

#===============================================================================
# 容器类型
#===============================================================================
PACKAGE=0#背包
EQUIPCTN=1#装备区
STORAGE=2#仓库
NUMENBAG=3#临时背包

#===============================================================================
# 物品附加状态
#===============================================================================
ADDON_REPAIRED = 0x1 #待修理
ADDON_BIND = 0x2 # 绑定
ADDON_RARE = 0x4 # 绑定

#==================
#装备部位
EQUIP_HEAD  = 1 #头部
EQUIP_NECKLACE = 2 #项链
EQUIP_WEAPON = 3 #武器
EQUIP_CLOTHES = 4 #衣服
EQUIP_BELT = 5 #裤子
EQUIP_SHOES = 6 #鞋子

dEquipPos = {
	EQUIP_HEAD:"帽子",
	EQUIP_NECKLACE:"项链",
	EQUIP_WEAPON:"武器",
	EQUIP_CLOTHES:"衣服",
	EQUIP_BELT:"腰带",
	EQUIP_SHOES:"鞋子",
}


#===============================================================================
# 物品描述->属性
#===============================================================================
baseDescAttr = {
	"物理伤害":"phyDam",
	"法术伤害":"magDam",
	"治疗强度":"cure",
	"封印命中":"sealHit",
	"抵抗封印":"reSealHit",
	"物理防御":"phyDef",
	"法术防御":"magDef",
	"生命上限":"hpMax",
	"速度":"spe",
	"真气上限":"mpMax",
}

addDescAttr = {
	"体质":"con",
	"魔力":"mag",
	"力量":"str",
	"耐力":"res",
	"精神":"spi",
	"敏捷":"dex",
}

otherDescAttr = {
	"品质":"quality",
	"打造":"isMake",
}
