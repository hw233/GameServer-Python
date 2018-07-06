# -*- coding: utf-8 -*-

if "moduleList" not in globals():
	moduleList  = {}

def getModuleList():
	return moduleList

#仙盟npc导表开始
import guild.guildNpc.n101
import guild.guildNpc.n102

moduleList[101] = guild.guildNpc.n101
moduleList[102] = guild.guildNpc.n102
#仙盟npc导表结束