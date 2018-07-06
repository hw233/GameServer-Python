# -*- coding: utf-8 -*-

GUILD_SQL = "SELECT guildId FROM guild"

#===============================================================================
# 职位
#===============================================================================
GUILD_JOB_CHAIRMAN = 1 # 盟主
GUILD_JOB_CHAIRMAN_VICE = 2 # 副盟主
GUILD_JOB_ELDER = 3 # 长老
GUILD_JOB_ELITE = 4 # 精英
GUILD_JOB_COMMON = 5 # 盟众
GUILD_JOB_APPRENTICE = 6 # 学徒

# 仙盟大战权限职位
FIGHT_JOB_LIST = [GUILD_JOB_CHAIRMAN, GUILD_JOB_CHAIRMAN_VICE]

guildJobName = {
	GUILD_JOB_CHAIRMAN: "盟主",
	GUILD_JOB_CHAIRMAN_VICE: "副盟主",
	GUILD_JOB_ELDER: "长老",
	GUILD_JOB_ELITE: "精英",
	GUILD_JOB_COMMON: "盟众",
	GUILD_JOB_APPRENTICE: "学徒",
}

# 仙盟建筑
BUILD_MAIN=1#聚义厅
BUILD_WAREHOUSE=2#库房
BUILD_WING=3#厢房
BUILD_TRAIN=4#训练场
BUILD_COIN=5#铸币场
BUILD_PET=6#异兽房

buildName = {
	BUILD_MAIN : "聚义厅",
	BUILD_WAREHOUSE : "库房",
	BUILD_WING : "厢房",
	BUILD_TRAIN : "训练场",
	BUILD_COIN : "铸币场",
	BUILD_PET : "异兽房",
}

# 仙盟初始建筑及等级
guildInitialBuild = {
	BUILD_MAIN:1,#聚义厅
	BUILD_WAREHOUSE:0,#库房
	BUILD_WING:0,#厢房
	BUILD_TRAIN:0,#训练场
	BUILD_COIN:0,#铸币场
	BUILD_PET:0,#异兽房
}

# 各职位对应的称谓ID
guildTitles = {
	GUILD_JOB_CHAIRMAN: 20106,
	GUILD_JOB_CHAIRMAN_VICE: 20105,
	GUILD_JOB_ELDER: 20104,
	GUILD_JOB_ELITE: 20103,
	GUILD_JOB_COMMON: 20102,
	GUILD_JOB_APPRENTICE: 20101,
}
