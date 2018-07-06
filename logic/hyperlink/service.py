# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
import hyperlink_pb2
import endPoint

# 超链接
class cService(hyperlink_pb2.terminal2main):
	@endPoint.result
	def rpcHyperlink(self, ep, who, reqMsg):return rpcHyperlink(who, reqMsg)  # 查看超链接

def rpcHyperlink(who, reqMsg):
	roleId = reqMsg.iRoleId
	linkType = reqMsg.iType
	targetNo = reqMsg.iTargetNo
	targetId = None
	if 1 == linkType:
		msg = props_pb2.propsIdList()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.iPropsIds[0]
	elif 2 == linkType:
		msg = pet_pb2.petAttr()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.petId
	elif 3 == linkType:
		msg = task_pb2.taskMsg()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.id
	elif 4 == linkType:
		msg = team_pb2.teamInfo()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.teamId
	elif 5 == linkType:
		msg = hyperlink_pb2.roleInfo()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.roleId
	elif 6 == linkType:#帮派
		msg = guild_pb2.guildInfo()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.guildId
	elif 7 == linkType:
		msg = lineup_pb2.eyeMsg()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.eyeId
	elif 8 == linkType:#答题
		msg = answer_pb2.dayProblem()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.iProblemNo
	elif 9 == linkType:#珍品阁摆摊
		msg = treasureShop_pb2.goodsInfo()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.iStallId
	elif 10 == linkType:#成就
		msg = achv_pb2.achvMsg()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.id
	elif 11 == linkType:#珍品阁摊位
		msg = treasureShop_pb2.itemInfo()
		msg.ParseFromString(reqMsg.sSerialized)
		targetId = msg.iItemId

	targetRole = getRole(roleId)
	func = funcByType.get(linkType)
	if func:
		func(who, targetRole, targetId, targetNo)

# def sysPropsHyperlink(who, iPropsNo):
# 	'''系统配置物品超链接
# 	'''
# 	import props
# 	oProps = props.getCacheProps(iPropsNo)
# 	if not oProps:
# 		message.tips(who, "此物品不存在")
# 		return
# 	who.endPoint.rpcPropsHyperlink(oProps.getMsg4Item(None, *oProps.MSG_ALL))

def propsHyperlink(who, targetRole, propsId, propsNo):
	msgObj = None
	if targetRole:
		targetProps = targetRole.getProps(propsId)
		if targetProps:
			msgObj = targetProps.getMsg4Item(None, *targetProps.MSG_ALL)
			
	if not msgObj:  # 只显示客户端内容
		msgObj = props_pb2.itemMsg()
		msgObj.iPropsNo = propsNo

	who.endPoint.rpcPropsHyperlink(msgObj)

def petHyperlink(who, targetRole, petId, petNo):
	msgObj = None
	if targetRole:
		petObj = targetRole.petCtn.getItem(petId)
		if petObj:
			msgObj = pet.service.packPetData(petObj)
	
	if not msgObj:
		message.tips(who, "该链接已经失效")
		return
	
	who.endPoint.rpcPetHyperlink(msgObj)

def taskHyperlink(who, targetRole, taskId, *args):
	msgObj = None
	if targetRole:
		taskObj = targetRole.taskCtn.getItem(taskId)
		if taskObj:
			if getattr(taskObj, "taskHyperlink", None):
				taskObj.taskHyperlink(who, targetRole, taskId, *args)
				return
			msgObj = task.service.packet4Hyperlink(targetRole, taskObj)
		
	if not msgObj:
		message.tips(who, "该链接已经失效")
		return
	
	who.endPoint.rpcTaskHyperlink(msgObj)

def teamHyperlink(who, targetRole, teamId, *args):
	msg = None
	if targetRole:
		teamObj = targetRole.getTeamObj()
		if teamObj:
			msg = team.service.packTeam4Hyperlink(teamObj)

	if not msg:
# 		message.tips(who, "该链接已经失效")
		return

	who.endPoint.rpcTeamHyperlink(**msg)

def roleHyperlink(who, targetRole, *args):
	msg = None
	if targetRole:
		msg = packetRole(targetRole)
		
	if not msg:
# 		message.tips(who, "该链接已经失效")
		return

	who.endPoint.rpcRoleHyperlink(**msg)

def guildJoinHyperlink(who, targetRole, guildId, roleId):
	msg = common_pb2.int32_()
	msg.iValue = guildId
	guild.service.rpcGuildJoin(who, msg)

def eyeHyperlink(who, targetRole, eyeId, eyeNo):
	msgObj = None
	roleLv = 1
	if targetRole:
		roleLv = targetRole.level
		eyeObj = targetRole.eyeCtn.getItem(eyeId)
		if eyeObj:
			msgObj = lineup.service.packetEyeMsg(eyeObj)

	if not msgObj:
		msgObj = lineup_pb2.eyeMsg()
		msgObj.eyeNo = eyeNo

	msgObj.roleLv = roleLv
	who.endPoint.rpcEyeHyperlink(msgObj)

def answerHyperlink(who, targetRole, answerNo, *args):
	if targetRole:
		answer.service.rpcGuildHelpHyperlink(who, targetRole, answerNo, *args)

def achvHyperlink(who, targetRole, achvId, *args):
	achv.service.rpcAchvHyperlink(who, targetRole, achvId, *args)

def treasureShopHyperlink(who, targetRole, iStallId, *args):
	dGoods = treasureShop.gTreasureShop.hasGoods(iStallId)
	if not dGoods:
		message.tips(who, "该物品链接已失效")
		return

	if who.id == dGoods["ownerId"]:
		openUIPanel.openTSSellUI(who,iStallId)
	else:
		openUIPanel.openTSBuyUI(who,iStallId)

def itemHyperlink(who, targetRole, iItemId, *args):
	dRoleItem = treasureShop.gTreasureShop.getRoleItem(targetRole.id)
	if dRoleItem and iItemId in dRoleItem:
		dGoods = treasureShop.gTreasureShop.getGoods(dRoleItem[iItemId])
		if dGoods:
			targetProps = dGoods["obj"]
			if isinstance(targetProps,props.equip.cProps):
				msgObj = targetProps.getMsg4Item(None, *targetProps.MSG_ALL)
				who.endPoint.rpcPropsHyperlink(msgObj)
			else:
				msgObj = lineup.service.packetEyeMsg(targetProps.eyeObj)
				who.endPoint.rpcEyeHyperlink(msgObj)
			return 

	message.tips(who, "该物品链接已失效")


funcByType = {
	1:propsHyperlink,  # 物品超链接
	2:petHyperlink,  # 宠物超链接
	3:taskHyperlink,  # 任务超链接
	4:teamHyperlink,  # 队伍超链接
	5:roleHyperlink,  # 角色超链接
	6:guildJoinHyperlink,  # 申请入帮超链接
	7:eyeHyperlink,  # 阵眼超链接
	8:answerHyperlink,  # 答题帮派求助超链接
	9:treasureShopHyperlink, #珍品阁超链接
	# 9:ringTaskHyperlink,  # 任务链求助超链接，需要客户端支持，暂时借用任务链接
	10:achvHyperlink,  # 成就超链接
	11:itemHyperlink,  #摊位超链接
}

def packetRole(oRole):
	msg = {}
	msg["roleId"] = oRole.id
	msg["shape"] = oRole.shape
	msg["name"] = oRole.name
	msg["level"] = oRole.level
	msg["guildName"] = oRole.getGuildName()
	msg["school"] = oRole.school

	teamObj = oRole.getTeamObj()
	if teamObj:
		msg["teamId"] = teamObj.id
	return msg


from common import *
import message
import pet.service
import task.service
import team.service
import props_pb2
import guild.service
import common_pb2
import answer.service
import lineup_pb2
import lineup.service
import pet_pb2
import task_pb2
import team_pb2
import guild_pb2
import hyperlink_pb2
import answer_pb2
import achv_pb2
import achv.service 
import treasureShop_pb2
import openUIPanel
import treasureShop
import props.equip