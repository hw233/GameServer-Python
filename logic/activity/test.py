# -*- coding: utf-8 -*-
from activity.object import Activity as customActivity

#导表开始
class Activity(customActivity):

	npcInfo = {
		1001:{"名称":"旁门散人","造型":"1001(0,0,0,0,0,0)","位置":"1010,10,10,0","称谓":"百晓副本"},
		1002:{"名称":"店小二","造型":"1002(0,0,0,0,0,0)","位置":"1010,50,77,1"},
	}

	eventInfo = {
		1001:{"点击":"DONE,R1001,D1001"},
		1002:{"点击":"F9007","成功":"DONE,R1002,D1003"},
		1003:{"点击":"TAKE","成功":"DONE,R1002,D1004","失败":"D1002"},
	}

	rewardInfo = {
		1001:{"经验":"LV*5+100","宠物经验":"PLV*2+100","银币":"999","物品":"1001"},
		1002:{"经验":"LV*5+100","宠物经验":"PLV*2+100","银币":"999","物品":"1001,1002"},
		2002:{"物品":"1002"},
		2003:{"物品":"1002"},
	}

	rewardPropsInfo = {
		1001:(
			{"权重":50,"物品":"202021","数量":"5","绑定":0},
			{"权重":25,"物品":"202022","数量":"3","绑定":1,"传闻":1001},
			{"权重":25,"物品":"202023","数量":"1","绑定":0},
		),
		1002:(
			{"权重":50,"物品":"202001","数量":"5","绑定":1},
			{"权重":25,"物品":"202002","数量":"3","绑定":0},
			{"权重":25,"物品":"202003","数量":"1","绑定":0},
		),
	}

	groupInfo = {
	9001:(202001,202002,202003,202004,202005,),
	9002:(20101,20102,20103,20201,),
	9003:(2021,2031,),
	9004:(202001,202002,202003,202004,202005,),
	9005:(202001,202002,202003,202004,202005,),
	9006:(202001,202002,202003,202004,202005,),
	9007:(1001,1002,1003,)
	}

	chatInfo = {
		1001:'''嗯，此事我已经明了，请先回去吧。''',
		1002:'''少侠没有带来所需物品''',
		1003:'''东西已经拿到了，回去吧。''',
		1004:'''很好很好，为师急需这个。''',
		1111:'''今天已完成了20环师门任务，继续做的师门经验会大幅减少，是否继续接任务？\nQ是\nQ否#20''',
	}

	branchInfo = {
		1001:(
			{"条件":0,"脚本":"L(9004,2)"},
			{"条件":10,"脚本":"L(9005,1)"},
			{"条件":20,"脚本":"L(9006,1)"},
		),
	}

	fightInfo = {
		1001:(
			{"类型":1,"名称":"强盗","造型":"1111","能力编号":"1002","数量":"1","技能":(1111,)},
			{"类型":0,"名称":"绑匪","造型":"1122","能力编号":"1001","数量":"1","技能":(401,)},
			{"类型":0,"名称":"杀手","造型":"1111","能力编号":"1001","数量":"2","技能":(102,103,)},
		),
		1002:(
			{"类型":1,"名称":"女飞贼","造型":"1122","能力编号":"1002","数量":"1","技能":(401,)},
			{"类型":0,"名称":"帮凶","造型":"1111","能力编号":"1001","数量":"1","技能":(1112,)},
			{"类型":0,"名称":"路过的","造型":"1111","能力编号":"1001","数量":"2","技能":(401,)},
			{"类型":0,"名称":"凑热闹的","造型":"1111","能力编号":"1001","数量":"2","技能":(401,)},
		),
		1003:(
			{"类型":1,"名称":"男少侠","造型":"1111","能力编号":"1003","数量":"1","技能":(1111,)},
			{"类型":0,"名称":"女少侠","造型":"1122","能力编号":"1003","数量":"1","技能":(401,)},
		),
	}

	ableInfo = {
		1001:{"等级":"LV","生命":"B*1","真气":"B*1","物理伤害":"B*0.5","法术伤害":"B*0.5","物理防御":"B*0.4","法术防御":"B*0.4","速度":"B*0.4","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1002:{"等级":"LV+1","生命":"B*1","真气":"B*1","物理伤害":"B*0.6","法术伤害":"B*0.6","物理防御":"B*0.5","法术防御":"B*0.5","速度":"B*0.6","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
		1003:{"等级":"LV+2","生命":"B*1","真气":"B*1","物理伤害":"B*0.6","法术伤害":"B*0.6","物理防御":"B*0.5","法术防御":"B*0.5","速度":"B*0.6","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	}
#导表结束

	def __init__(self, _id, name):
		customActivity.__init__(self, _id, name)
		self.list = [101,102,103,]
			
	def save(self):
		data = customActivity.save(self)
		data["list"] = self.list
		return data
	
	def load(self, data):
		customActivity.load(self, data)
		self.list = data["list"]
		
	def testCmd(self, who, cmdIdx, *args):
		if cmdIdx == 100:
			txtList = []
			txtList.append("201-学习帮派技能")
			txtList.append("202-使用帮派技能")
			txtList.append("203-查看包裹里的药品")
			txtList.append("204-炼丹")
			txtList.append("301-查看包裹里的阵法")
			txtList.append("302-学习阵法")
			txtList.append("303-提升阵法")
			txtList.append("401-请求阵法列表")
			txtList.append("501-进度条")
			txtList.append("502-宠物改名")
			txtList.append("601-银币不足")
			txtList.append("602-元宝不足")
			txtList.append("701-查看包裹里的装备")
			txtList.append("702-设置装备的耐久")
			message.dialog(who, "\n".join(txtList))
		elif cmdIdx == 201:
			try:
				skId = int(args[0])
			except:
				message.tips(who, "参数:技能编号")
				return
			skill.upgrade.doSkillGuildLearn(who, skId)
		elif cmdIdx == 202:
			try:
				skId = int(args[0])
			except:
				message.tips(who, "参数:技能编号")
				return
			skill.upgrade.doSkillGuildUse(who, skId)
		elif cmdIdx == 203:
			txtList = []
			for obj in who.propsCtn.dPosMapProps.itervalues():
				if obj.kind != ITEM_MEDICINE_LEVEL:
					continue
				txtList.append("id:%s 物品:%s 数量:%s " % (obj.id, obj.no(), obj.stack()))
			message.dialog(who, "\n".join(txtList))
		elif cmdIdx == 204:
			propsIdList = {}
			for propsId in args:
				propsIdList[propsId] = propsIdList.get(propsId, 0) + 1
				
			skId = 504
			level = who.querySkillLevel(skId)
			if not level:
				return
			skObj = skill.new(skId)
			skObj.level = level
	
			if propsIdList:
				skill.upgrade.doSkillMakeMedicine(who, skObj, propsIdList)
			else:
				skill.upgrade.doSkillMakeMedicineByCash(who, skObj)
		elif cmdIdx == 205:
			for i in xrange(20):
				print scene.randSpace(1070)
		elif cmdIdx == 301:
			txtList = []
			for obj in who.propsCtn.dPosMapProps.itervalues():
				if (224001 <= obj.no() <= 224010) or obj.no() in (224101,): 
					txtList.append("id:%s 物品:%s 数量:%s " % (obj.id, obj.no(), obj.stack()))
			message.dialog(who, "\n".join(txtList))
		elif cmdIdx == 302:
			lineupId = args[0]
			lineup.upgrade.learn(who, lineupId)
		elif cmdIdx == 303:
			lineupObj = who.lineupCtn.getItem(args[0])
			propsIdList = {}
			for propsId in args[1:]:
				propsIdList[propsId] = propsIdList.get(propsId, 0) + 1
			lineup.upgrade.upgrade(who, lineupObj, propsIdList)
		elif cmdIdx == 401:
			lineup.service.rpcLineupListQuest(who, None)
		elif cmdIdx == 502:
			if len(args) < 1:
				message.tips(who, "测试指令:act test 502 宠物ID 新宠物名字")
				return
			petId = int(args[0])
			petName = args[1]
			dMsg = pet_pb2.petAttr()
			dMsg.petId = petId
			dMsg.name = petName
			pet.service.rpcPetRename(who, dMsg)
			# sInput = message.inputBox(who, "改名", "输入异兽新的名字：(最多6个字)")
			# if not sInput:
			# 	return
			# print 'pet rename:%s' % sInput
			# petObj = who.petCtn.getItem(petId)
			# if not petObj:
			# 	message.tips(who, "该宠物不存在")
			# 	return
			# if calLen(nameNew) > 12:
			# 	message.tips(who, "名字过长，改名失败，请重新输入")
			# 	return
			# if trie.fliter(nameNew) != nameNew:
			# 	message.tips(who, "名字不符合规定，改名失败，请重新输入")
			# 	return
			# petObj.set("name", sInput)
			# petObj.attrChange("name")
			# message.tips(who, "异兽改名成功")
		elif cmdIdx == 503:
			dMsg = pet_pb2.items()
			dMsg.petId = int(args[0])
			dMsg.itemId = int(args[1])
			dMsg.useCnt = int(args[2])
			pet.service.rpcPetUseItem(who, dMsg)
		elif cmdIdx == 504:
			petObj = who.petCtn.getItem(int(args[0]))
			if not petObj:
				return
			sch = pet.service.packPetPointScheme(petObj)
			message.dialog(who, str(sch))
		elif cmdIdx == 505:
			dMsg = pet_pb2.points()
			dMsg.petId = int(args[0])
			dMsg.con = int(args[1])
			dMsg.mag = int(args[2])
			dMsg.str = int(args[3])
			dMsg.res = int(args[4])
			dMsg.spi = int(args[5])
			dMsg.dex = int(args[6])
			pet.service.rpcPetAttrPointScheme(who, dMsg)
		elif cmdIdx == 601:
			try:
				cash = args[0]
			except:
				message.tips(who, "参数:花费银币")
				return
			money.checkCash(who,cash)
		elif cmdIdx == 602:
			try:
				tradeCash = args[0]
			except:
				message.tips(who, "参数:花费元宝")
				return
			money.checkTradeCash(who,tradeCash)
		elif cmdIdx == 701:
			txtList = []
			for obj in who.propsCtn.getAllValues():
				if obj.kind != ITEM_EQUIP:
					continue
				txtList.append("id:%s 物品:%s " % (obj.id, obj.name))
			message.dialog(who, "\n".join(txtList))
		elif cmdIdx == 702:
			try:
				iEquipId = args[0]
				iLife = args[1]
			except:
				message.tips(who, "参数:装备id 设置耐久")
				return
			oEquip = who.propsCtn.getItem(iEquipId)
			if not oEquip:
				message.tips(who,"背包没有该物品，错误的装备id")
				return
			oEquip.set("life",iLife)
			who.endPoint.rpcModProps(oEquip.getMsg4Package(who.propsCtn,*("life","addon")))
		elif cmdIdx == 991:
			import guild.service
			guild.service.rpcGuildFightInfoRequest(who, None)
		elif cmdIdx == 992:
			import guild.service
			reqMsg = Msg()
			reqMsg.bValue = int(args[0])
			guild.service.rpcGuildFightAutoSignUpSet(who, reqMsg)
		elif cmdIdx == 993:
			import guild.service
			reqMsg = Msg()
			guild.service.rpcGuildFightTeamRequest(who, reqMsg)
		elif cmdIdx == 994:
			import guild.service
			reqMsg = Msg()
			reqMsg.keyword = str(args[0])
			guild.service.rpcGuildFightSearch(who, reqMsg)
		elif cmdIdx == 995:
			import guild.service
			reqMsg = Msg()
			guild.service.rpcGuildFightResultRequest(who, reqMsg)
		elif cmdIdx == 996:
			import guild.service
			reqMsg = Msg()
			reqMsg.roleId = args[0]
			reqMsg.teamNo = args[1]
			guild.service.rpcGuildFightTeamMemberSelect(who, reqMsg)
		elif cmdIdx == 997:
			import guild.service
			reqMsg = Msg()
			reqMsg.roleId = 111
			reqMsg.teamNo = 1
			guild.service.rpcGuildFightTeamMemberCancel(who, reqMsg)
		elif cmdIdx == 998:
			import guild.service
			reqMsg = Msg()
			guild.service.rpcGuildFightSignUp(who, reqMsg)
		elif cmdIdx == 999:
			who.buddyCtn.removeItemByKey(3002)
		

class Msg(object):
	pass


from props.defines import *
import message
import skill.upgrade
import scene
import lineup.upgrade
import lineup.service
import pet_pb2
import pet.service
import money