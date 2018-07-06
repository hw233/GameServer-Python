# coding: utf-8
'''
评分
'''
#导表开始
mapEquipBase = {
	"con":1.82,
	"mag":1.82,
	"str":1.82,
	"res":1.82,
	"spi":1.82,
	"dex":1.82,
	"hpMax":0.23,
	"mpMax":0,
	"phyDam":0.91,
	"magDam":0.91,
	"phyDef":0.73,
	"magDef":0.73,
	"spe":0.32,
	"cure":1.82,
	"sealHit":0.91,
	"reSealHit":0.23,
}
mapWeaponSchool = {
	11:"phyDam",
	12:"magDam",
	13:"phyDam",
	14:"sealHit",
	15:"magDam",
	16:"cure",
}
dPetAptitudeFactor = {
	"hpGen":0.05,
	"phyAttGen":0.175,
	"magAttGen":0.175,
	"phyDefGen":0.175,
	"magDefGen":0.175,
	"speGen":0.175,
	"grow":140,
}
dPetTypeFactor = {
	1:{"hpGen":1,"phyAttGen":0.8,"magAttGen":1.2,"phyDefGen":1,"magDefGen":1,"speGen":1,"grow":1},
	2:{"hpGen":1,"phyAttGen":1.2,"magAttGen":0.8,"phyDefGen":1,"magDefGen":1,"speGen":1,"grow":1},
	3:{"hpGen":1.2,"phyAttGen":0.9,"magAttGen":0.9,"phyDefGen":1,"magDefGen":1,"speGen":1,"grow":1},
}
#导表结束

# 装备属性评分系数mapEquipBase
# 武器对应门派属性mapWeaponSchool
# 异兽资质列表
lPetAptitude = ["hpGen", "phyAttGen", "magAttGen", "phyDefGen", "magDefGen", "speGen", "grow"]
# 异兽资质系数dPetAptitudeFactor
# 异兽类别系数dPetTypeFactor

def gradeAll(who):
	'''综合评分
	综合实力 = 人物评分 + 宠物评分
	此处宠物评分是玩家当前拥有(包括仓库)的评分最大的3只宠物的评分之和
	'''
	iScore = 0
	lPetScores = []
	for petObj in who.petCtn.getAllValues():
		lPetScores.append(gradePet(petObj))
	if len(lPetScores) < 3:
		lPetScores.extend([0 for i in xrange(3-len(lPetScores))])
	lPetScores.sort(reverse=True)
	petScore = sum(lPetScores[:3])
	return gradeRole(who) + petScore

def gradeRole(who):
	'''人物评分
	人物评分 = 等级评分 + 装备评分 + 技能评分 + 修炼评分 + 其他评分
	此处装备评分是6个部位的装备的评分之和
	'''
	return gradeRoleLv(who) + gradeRoleEquip(who) + gradeRoleSkill(who) + gradeRoleXiulian(who) + gradeRoleOther(who)

def gradeRoleLv(who):
	'''人物等级评分
	'''
	return who.level * 80

def gradeRoleEquip(who):
	'''人物穿戴装备评分
	'''
	iScore = 0
	for equipObj in who.equipCtn.getAllWearEquipByValid():
		iScore += gradeEquip(equipObj)
	return iScore

def gradeRoleSkill(who):
	'''人物技能评分
	'''
	iScore = 0
	for skObj in who.skillCtn.getAllValues():
		if not hasattr(skObj, "school"): # 非职业技能
			continue
		iScore += skObj.level
	# TODO 强身术等级
	return iScore

def gradeRoleXiulian(who):
	'''人物修炼评分
	修炼		<12	>=12
	人物攻修	14	28
	物防修炼	7	14
	法防修炼	7	14
	抗封修炼	7	14
	宠物攻修	7	14
	宠物物防	7	14
	宠物法防	7	14
	宠物抗封	7	14
	'''
	# TODO 修炼系统完成后接上
	return 0

def gradeRoleOther(who):
	'''人物其他评分
	'''
	return 0

def gradePet(oPet):
	'''异兽评分
	宠物评分 = 资质评分 + 技能评分 + 其他评分
	'''
	return gradePetAptitude(oPet) + gradePetSkill(oPet) + gradePetOther(oPet)

def gradePetAptitude(oPet):
	'''异兽资质评分
	资质评分 = ∑(各资质数值 * 资质系数 * 类型系数)
	生命资质	法攻资质	物攻资质	物防资质	法防资质	速度资质	成长
	0.05	0.175	0.175	0.175	0.175	0.175	140
	宠物类型	生命资质	法攻资质	物攻资质	物防资质	法防资质	速度资质	成长
	1	1	0.8	1.2	1	1	1	1
	2	1	1.2	0.8	1	1	1	1
	3	1.2	0.9	0.9	1	1	1	1
	'''
	iScore = 0
	iType = oPet.getConfig("类别")
	for aptitude in lPetAptitude:
		iScore += oPet.getValByName(aptitude) * dPetAptitudeFactor[aptitude] * dPetTypeFactor[iType][aptitude]
	return int(iScore)

def gradePetSkill(oPet):
	'''异兽技能评分
	宠物技能表增加“评分”字段，程序根据宠物拥有的技能读取对应的评分值
	'''
	iScore = 0
	skillList = oPet.getSkillList()
	for skillObj in skillList.itervalues():
		iScore += skillObj.score
	return iScore

def gradePetOther(oPet):
	'''异兽其他评分
	'''
	return 0

def gradeEquip(oEquip):
	'''装备评分
	装备评分 = 装备基础评分 + 宝石评分
	'''
	return gradeEquipBase(oEquip) + gradeEquipGem(oEquip)

def gradeEquipBase(oEquip):
	'''装备基础评分
	装备基础评分 = 装备上各个属性的值 * 属性评分系数 + 各个装备特技特效的评分
	生命	真气	物攻	法攻	治疗强度	物防	法防	速度	体质	力量	法力	耐力	精神	敏捷
	0.23	0	0.91	0.91	1.82	0.73	0.73	0.32	1.82	1.82	1.82	1.82	1.82	1.82
	'''
	iScore = 0
	for sKey, iValue in oEquip.fetch("baseAttr").iteritems():
		# 武器评分特殊，分门派计算物攻、法攻、治疗强度中的一个
		if oEquip.wearPos() == EQUIP_WEAPON:
			iSchool = oEquip.school()
			if sKey in ["phyDam", "magDam", "cure","sealHit"] and sKey != mapWeaponSchool[iSchool]:
				continue
		iScore += iValue * mapEquipBase.get(sKey, 0)
	for sKey, iValue in oEquip.fetch("addAttr", {}).iteritems():
		iScore += iValue * mapEquipBase.get(sKey, 0)
	iSe = oEquip.fetch("spEffect")
	if iSe:
		iScore += int(skillEquipData.getConfig(iSe, "评分"))
	iSk = oEquip.fetch("spSkill")
	if iSk:
		iScore += int(skillEquipData.getConfig(iSk, "评分"))
	return int(iScore)

def gradeEquipGem(oEquip):
	'''装备宝石评分
	宝石等级*评分系数(12)
	'''
	gems = oEquip.gems()
	if not gems:
		return 0
	iScore = 0
	for iHole, [iNo, iAmount] in gems.iteritems():
		iLevel = int(math.log(iAmount, 2)) + 1
		iScore += iLevel * 12
	return iScore

def gradeBuddy(buddyObj):
	'''伙伴评分
	'''
	return gradeBuddyAttr(buddyObj) + gradeBuddySkill(buddyObj)

def gradeBuddyAttr(buddyObj):
	'''伙伴属性评分
	'''
	iScore = 0
	for attr,ration in mapEquipBase.iteritems():
		iScore += ration * buddyObj.getAttr(attr)
	return int(iScore)

def gradeBuddyAttrByData(attrData):
	iScore = 0
	for attr,ration in mapEquipBase.iteritems():
		value = attrData.get(attr,0)
		iScore += ration * value
	return int(iScore)

def gradeBuddySkill(buddyObj):
	'''伙伴技能评分
	'''
	iScore = 0
	for skillObj in buddyObj.getValidSkillList().itervalues():
		if hasattr(skillObj,"score"):
			iScore += skillObj.score
	return int(iScore)

import math
import skill
from props.defines import *
import sesksData
import skillEquipData