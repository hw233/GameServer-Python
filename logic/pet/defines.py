# -*- coding: utf-8 -*-

PET_FLAG_BIND = 0x01 # 绑定
PET_FLAG_BB = 0x02 # 宝宝
PET_FLAG_COLOR = 0x04 # 异兽
PET_FLAG_FIGHT = 0x08 # 参战
PET_FLAG_XXX = 0x10 # xxx
PET_FLAG_XXX = 0x20 # xxx
PET_FLAG_XXX = 0x40 # xxx
PET_FLAG_XXX = 0x80 # xxx

PET_COMMON = 0
PET_HOLY = 1

# 洗炼属性描述
washDescList = {
"额外生命资质上限" : "hpGenWashNew",
"额外物攻资质上限" : "phyAttGenWashNew",
"额外法攻资质上限" : "magAttGenWashNew",
"额外物防资质上限" : "phyDefGenWashNew",
"额外法防资质上限" : "magDefGenWashNew",
"额外速度资质上限" : "speGenWashNew",
"额外成长资质上限" : "growWashNew",
"技能点" : "skillPointNew",
}

# 额外资质属性
genExtAttrList = ("hpGenExt", "phyAttGenExt", "magAttGenExt", "phyDefGenExt", "magDefGenExt", "speGenExt")

genExtMinNameList = ("额外生命资质最低值", "额外物攻资质最低值", "额外法攻资质最低值", "额外物防资质最低值", "额外法防资质最低值", "额外速度资质最低值")

genExtMaxNameList = ("额外生命资质上限", "额外物攻资质上限", "额外法攻资质上限", "额外物防资质上限", "额外法防资质上限", "额外速度资质上限")
