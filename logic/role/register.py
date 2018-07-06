# -*- coding: utf-8 -*-
'''角色到其他服务器的注册、注释
'''

def registerRole(who):
	'''注册角色到其他服务器
	'''
	if not who.endPoint:
		return
	registerRoleToChat(who)
	
def registerRoleToChat(who):
	'''注册角色到聊天服
	'''
	roleMsgObj = main_chat_pb2.roleInfo()
	roleMsgObj.roleId = who.id
	roleMsgObj.shape = who.shape
	roleMsgObj.name = who.name
	roleMsgObj.level = who.level
# 	roleMsgObj.flagList.extend(who.getFlagList()) # 预留
	roleMsgObj.guildName = who.getGuildName()
	
	roleMsgObj.sceneId = who.sceneId
	roleMsgObj.schoolId = who.school
	roleMsgObj.teamId = who.getValByName("teamId")
	roleMsgObj.guildId = who.getGuildId()
	roleMsgObj.blackList.extend(who.friendCtn.lBlack)
	guildObj = who.getGuildObj()
	if guildObj:
		roleMsgObj.guildBan = guildObj.banList.get(who.id, (0,0))[1]

	msgObj = main_chat_pb2.registerRoleMsg()
	msgObj.epId = who.endPoint.epId()
	msgObj.roleMsg.CopyFrom(roleMsgObj)
	mainService.getChatEP().rpcRegisterRole(msgObj)
	
def registerRoleToScene(who):
	'''注册角色到场景服
	'''
	msgObj = main_scene_pb2.registerRoleMsg()
	msgObj.epId = who.endPoint.epId()
	msgObj.roleId = who.id
	mainService.getSceneEP().rpcRegisterRole(msgObj)
	
def unRegisterRole(who):
	'''从其他服务器中注销角色
	'''
	unRegisterRoleToChat(who)
	unRegisterRoleToScene(who)
	
def unRegisterRoleToChat(who):
	'''从聊天服中注销角色
	'''
	mainService.getChatEP().rpcUnRegisterRole(who.id)

def unRegisterRoleToScene(who):
	'''从场景服中注销角色
	'''
	mainService.getSceneEP().rpcUnRegisterRole(who.id)

def updateRole(who, **roleInfo):
	'''更新角色信息到其他服务器
	'''
	if not hasattr(who, "isLogined"): # 登录未完成前不发送
		return
	updateRoleToChat(who, **roleInfo)
	
def updateRoleToChat(who, **roleInfo):
	'''更新角色信息到聊天服
	'''
	msg = {"roleId": who.id,}
	msg.update(roleInfo)
	mainService.getChatEP().rpcUpdateRole(**msg)
	
	
import main_chat_pb2
import main_scene_pb2
import mainService