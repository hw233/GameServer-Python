# -*- coding: utf-8 -*-

SYS_SENDER_ID = 0 # 系统发送者id

#===============================================================================
# 聊天频道
#===============================================================================
CHANNEL_WORLD = 1 # 世界频道
CHANNEL_SCHOOL = 2 # 门派频道
CHANNEL_TEAM = 3 # 队伍频道
CHANNEL_TEAM_MAKE = 31 # 组队频道
CHANNEL_GUILD = 4 # 仙盟频道
CHANNEL_GUILD_ANNOUNCE = 41 # 仙盟公告
CHANNEL_CURRENT = 5 # 当前频道
CHANNEL_SYS_ANNOUNCE = 6 # 系统频道
CHANNEL_SYS_MESSAGE = 61 # 传闻频道
CHANNEL_FIGHT = 7 # 战斗频道

channelNameList = {
	CHANNEL_WORLD: "世界频道",
	CHANNEL_SCHOOL: "门派频道",
	CHANNEL_TEAM: "队伍频道",
	CHANNEL_TEAM_MAKE: "组队频道",
	CHANNEL_GUILD: "仙盟频道",
	CHANNEL_GUILD_ANNOUNCE: "仙盟公告频道",
	CHANNEL_CURRENT: "当前频道",
	CHANNEL_SYS_ANNOUNCE: "系统频道",
	CHANNEL_SYS_MESSAGE: "传闻频道",
	CHANNEL_FIGHT: "战斗频道",
}

def getChannelName(channelId):
	return channelNameList[channelId]


#===============================================================================
# 属性与频道的对应关系
#===============================================================================
attrName2ChannelId = {
	"schoolId": CHANNEL_SCHOOL,
	"teamId": CHANNEL_TEAM,
	"guildId": CHANNEL_GUILD,
	"warId": CHANNEL_FIGHT,
}

channelId2AttrName = {}
for k, v in attrName2ChannelId.iteritems():
	channelId2AttrName[v] = k



