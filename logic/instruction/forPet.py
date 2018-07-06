# -*- coding: utf-8 -*-
'''宠物相关指令
'''
import instruction

@instruction.properties(sn='pet')
def newpet(ep, shape, level, star=1, target=None):
	'获得一个宠物，参数：宠物编号'
	petObj = pet.new(shape, level, star)
	if pet.addPet(target, petObj):
		ep.rpcTips("得到了一个%s" % petObj.name)

def showpet(ep, target=None):
	'''显示身上所有宠物
	'''
	if target.petCtn.itemCount() <= 0:
		ep.rpcTips("身上没有任何宠物")
		return
	
	txtList = []
	for petObj in target.petCtn.getAllValues():
		txtList.append("%d %s/%s 等级:%d" % (petObj.id, petObj.name, petObj.shape, petObj.level))
	ep.rpcModalDialog("\n".join(txtList))

def petinfo(ep, petId, target=None):
	'''显示宠物的基本信息
	'''
	if not petId:
		ep.rpcTips("请指定宠物的ID")
		return
	txtList = []
	petObj = target.petCtn.getItem(petId)
	if not petObj:
		ep.rpcTips("找不到此宠物")
		return
	data = pet.service.packPetAttr(petObj)
	txtList.append("%d %s/%s 星级：%d" % (petObj.id, petObj.name, petObj.shape, petObj.getStar()))
	txtList.append("等级%d 经验%d/%d" %(petObj.level, petObj.exp, petObj.expNext))
	txtList.append("生命%d/%d 真气%d/%d" %(petObj.hp, petObj.hpMax, petObj.mp, petObj.mpMax))
	txtList.append("物理伤害%d 物理防御%d" %(petObj.phyDam, petObj.phyDef))
	txtList.append("法术伤害%d 法术防御%d" %(petObj.magDam, petObj.magDef))
	txtList.append("速度%d" %(petObj.spe))
	txtList.append("体质%d 魔力%d 力量%d" %(petObj.con, petObj.mag, petObj.str))
	txtList.append("耐力%d 精神%d 敏捷%d" %(petObj.res, petObj.spi, petObj.dex))
	txtList.append("寿命%d 技能潜力%d" %(petObj.getLife(), petObj.getSkillPoint()))
	txtList.append("生资%d 攻资%d 法资%d" %(data.hpGen, data.phyAttGen, data.magAttGen))
	txtList.append("物防资%d 法防资%d 速资%d" %(data.phyDefGen, data.magDefGen, data.speGen))
	txtList.append("成长%s" %(data.grow))
	ep.rpcModalDialog("\n".join(txtList))

def clearpet(ep, petId=0, target=None):
	'''清除宠物
	
	petId: 默认为0，表示清除所有宠物
	'''
	if petId:
		petObj = target.petCtn.getItem(petId)
		if not petObj:
			ep.rpcTips("找不到此宠物")
			return
		target.petCtn.removeItem(petObj)
	else:
		target.petCtn.clearAll()
	ep.rpcTips("OK")
		
def addpetexp(ep, petId, val, target=None):
	'''增加宠物经验
	'''
	petObj = target.petCtn.getItem(petId)
	if not petObj:
		ep.rpcTips("找不到此宠物")
		return
	petObj.addExp(val, "instruction")

def setpetlife(ep, petId, val, target=None):
	petObj = target.petCtn.getItem(petId)
	if not petObj:
		ep.rpcTips("找不到此异兽")
		return
	elif val < 0:
		ep.rpcTips("不能将异兽生命设置为负值")
		return
	iLife = petObj.getLife()
	iAdd = val - iLife
	petObj.addLife(iAdd, "instruction")
	ep.rpcTips("异兽%s的生命设置为%d" % (petObj.name, val))

def setpetskill(ep, petId, skId, level=1, target=None):
	'''设置宠物技能
	'''
	petObj = target.petCtn.getItem(petId)
	if not petObj:
		ep.rpcTips("找不到此宠物")
		return
	petObj.setSkill(skId, level)
	petObj.reCalcAttr()
	ep.rpcTips("宠物%s的%s等级设置为%d" % (petObj.name, skId, level))
	
def showpetskill(ep, petId, target=None):
	petObj = target.petCtn.getItem(petId)
	if not petObj:
		ep.rpcTips("找不到此宠物")
		return
	
	skillList = petObj.getSkillList()
	if not skillList:
		ep.rpcTips("此宠物没有任何技能")
	else:
		txtList = []
		for skillObj in skillList.itervalues():
			txtList.append("%d/%s" % (skillObj.id, skillObj.name))
		ep.rpcModalDialog("\n".join(txtList))
				
def clearpetskill(ep, petId, target=None):
	petObj = target.petCtn.getItem(petId)
	if not petObj:
		ep.rpcTips("找不到此宠物")
		return
	
	skillList = petObj.getSkillList().keys()
	for skId in skillList:
		petObj.setSkill(skId, 0)
	petObj.reCalcAttr()
	ep.rpcTips("OK")

def setpetstatus(ep, petId, status, target=None):
	'''设置异兽的状态(0普通1凝神)
	'''
	import role.defines
	petObj = target.petCtn.getItem(petId)
	if not petObj:
		ep.rpcTips("找不到此宠物")
		return
	if petObj.fetch("status") == status:
		ep.rpcTips("此异兽已经是这个状态了")
		return
	petObj.set("status", status)
	petObj.setColors({role.defines.SHAPE_PART_TYPE_BODY:1 if status == 0 else 2})#状态变更后颜色要调回默认的方案
	petObj.attrChange("status")
	if status == 0:
		ep.rpcTips("宠物由变异退化到普通资质，原染色效果已被清除")
	else:
		ep.rpcTips("宠物由普通进化到变异资质，原染色效果已被清除")

import pet
import skill
import pet.service
