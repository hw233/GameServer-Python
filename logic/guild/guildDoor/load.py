# -*- coding: utf-8 -*-

if "moduleList" not in globals():
	moduleList  = {}

def getModuleList():
	return moduleList


#仙盟door导表开始
import guild.guildDoor.d101
import guild.guildDoor.d102

moduleList[101] = guild.guildDoor.d101
moduleList[102] = guild.guildDoor.d102
#仙盟door导表结束
