#-*-coding:utf-8-*-

if 'gbOnce' not in globals():
	gbOnce=True
	if 'mainService' in SYS_ARGV:
		gdRankObj = {}
		gdRankObjNameMap = {}	#子类编号对应的排行榜

# def getRankDbKey(sRankChineseName):
# 	if sRankChineseName not in gRankNameMap:
# 		raise Exception,"排行榜不存在：{}".format(sRankChineseName)
# 	return gRankNameMap[sRankChineseName][0]

def newRankObj(mod, sRankChineseName, sRankName, iMainNo, iNo, iDisplaySize):
	if not mod or not sRankName:
		raise Exception,"排行榜‘{}’没有定义模块".format(iNo)
	if iNo in gdRankObj:
		raise Exception,"编号‘{}’排行榜已经存在".format(iNo)
	if sRankName in gdRankObjNameMap:
		raise Exception,"名字为‘{}’排行榜已经存在".format(sRankName)

	rankObj = mod.cRanking(iMainNo, iNo, sRankChineseName, sRankName, iDisplaySize)
	if not rankObj._loadFromDB():
		rankObj._insertToDB(*rankObj.getPriKey())
	rankObj.startTimer()
	gdRankObj[iNo] = rankObj
	gdRankObjNameMap[sRankName] = rankObj

	return rankObj


def initAllRank():
	print "initAllRank init..."
	global gdRankObj
	global gdRankObjNameMap
	gdRankObj = {}
	gdRankObjNameMap = {}	#子类编号对应的排行榜
	for iMainNo,v in RankClassifyData.gdData.iteritems():
		lRankNo = v.get("子类编号列表", [])
		for iRankNo in lRankNo:
			info = RankData.gdData.get(iRankNo, {})
			sMainName = v.get("主类名称", "")
			sSubName = info.get("子类名称", "")
			sRankChineseName = "{}_{}".format(sMainName, sSubName)
			# print "加载排行榜：",sRankChineseName
			iDisplaySize = info.get("显示人数", 100)
			dModInfo = rank.load.gdRankModInfo.get(iRankNo, {})
			mod = dModInfo.get("mod", None)
			sRankName = dModInfo.get("name", "")
			rankObj = newRankObj(mod, sRankChineseName, sRankName, iMainNo, iRankNo, iDisplaySize)

	#宠物分类排行榜
	for iPetNo in RankPetData.gdData.keys():
		sRankChineseName = "{}_{}".format("宠物分类排行榜", iPetNo)
		# print "加载排行榜：",sRankChineseName
		iDisplaySize = 100
		dModInfo = rank.load.gdRankModInfo.get("pet_classify", {})
		mod = dModInfo.get("mod", None)
		sRankName = dModInfo.get("name", "")
		sRankName = sRankName.format(iPetNo)
		rankObj = newRankObj(mod, sRankChineseName, sRankName, rank.defines.giPetScoreRankNo, iPetNo, iDisplaySize)

	#升级
	role.geUpLevel+=roleUpLevel

#===================================
#根据编号、名字获取排行榜对象
def getRankObjBySubNo(iRankNo):
	rankObj = gdRankObj.get(iRankNo, None)
	if not rankObj:
		raise Exception,"排行榜'{}'不存在".format(rank.load.getRankChineseName(iRankNo))
	return rankObj

def getRankObjByName(sRankName):
	rankObj = gdRankObjNameMap.get(sRankName, None)
	if not rankObj:
		raise Exception,"排行榜'{}'不存在".format(sRankName)
	return rankObj

def isUpdateRank(who, rankObj):
	'''判断是否退榜了，退榜了不用更新到排行榜
		判断等级是否可以上榜
	'''
	if not rankObj.canQuit():
		return True
	dRankQuit = who.fetch("rankQuit", {})
	iRankNo = rankObj.rankNo()
	return True if dRankQuit.get(iRankNo, 0) == 0 else False

def rankPetHighestScore(who):
	'''宠物历史最高评分是玩家当前拥有(包括仓库)的历史最高评分最大的3只宠物的评分之和
	'''
	dPetHighestScore = who.petCtn.fetch("petHightestScore", {})
	lPetScore = dPetHighestScore.values()
	lPetScore.sort(reverse=True)
	iPetHightestScore = sum(lPetScore[:3])
	return iPetHightestScore

def rankCompositeScore(who):
	'''	综合实力 = 人物历史最高评分 + 宠物历史最高评分
		宠物历史最高评分是玩家当前拥有(包括仓库)的历史最高评分最大的3只宠物的评分之和
	'''
	iHighestFightPower = who.fetch("highestScore", who.fightPower)
	iPetHightestScore = rankPetHighestScore(who)
	return iHighestFightPower+iPetHightestScore

#===========================================
#练级狂人榜
def updateLvRank(who):
	roleChangeInfo(who)
	rankObj = getRankObjByName("rank_lv")
	if not isUpdateRank(who, rankObj):
		return
	rankObj.updateScore(who.id, who.name, who.level, who.level, who.school, exp=who.exp)

def changeExpUpdateRank(who):
	rankObj = getRankObjByName("rank_lv")
	if not isUpdateRank(who, rankObj):
		return
	rankObj.updateExp(who)

#===============================================
#===============================================
#宠物排行榜
def updatePetScoreRank(who, petObj, updateHistory=True):
	if petObj.idx not in RankPetData.gdData:	#没有排行榜
		return

	#保存历史最高的分数
	if updateHistory:
		dPetHighestScore = who.petCtn.fetch("petHightestScore", {})
		iPetScore = petObj.getScore()
		dPetHighestScore[petObj.id] = max(iPetScore, dPetHighestScore.get(petObj.id, 0))
		who.petCtn.set("petHightestScore", dPetHighestScore)
	rankObj = getRankObjByName("rank_pet_score_all")
	if not isUpdateRank(who, rankObj):
		return
	rankObj.updateScore(petObj.id, who.name, petObj.getScore(), who.level, who.school, iRoleId=who.id, idx=petObj.idx, petName=petObj.name)

	#宠物分类排行榜
	dModInfo = rank.load.gdRankModInfo.get("pet_classify", {})
	sRankName = dModInfo.get("name", "")
	sRankName = sRankName.format(petObj.idx)
	rankObj = getRankObjByName(sRankName)
	rankObj.updateScore(petObj.id, who.name, petObj.getScore(), who.level, who.school, iRoleId=who.id, idx=petObj.idx, petName=petObj.name)

def allPetQuitRank(who):
	'''所有宠物退榜
	'''
	rankPetScoreObj = getRankObjByName("rank_pet_score_all")

	dModInfo = rank.load.gdRankModInfo.get("pet_classify", {})
	sRankName = dModInfo.get("name", "")
	for petObj in who.petCtn.getAllValues():
		sRankName = sRankName.format(petObj.idx)
		rankObj = getRankObjByName(sRankName)
		rankObj.removeRecordByUid(petObj.id)
		
		rankPetScoreObj.removeRecordByUid(petObj.id)

def allPetAddRank(who):
	'''所有宠物上榜
	'''
	for petObj in who.petCtn.getAllValues():
		updatePetScoreRank(who, petObj)

#===============================================
#===============================================
#装备排行榜
def updateEquipScoreRank(who, oEquip):
	iWeaPos = oEquip.wearPos()
	sRankName = rank.load.gdEquipPosRank.get(iWeaPos, "")
	rankObj = getRankObjByName(sRankName)
	if not isUpdateRank(who, rankObj):
		return
	rankObj.updateScore(who.id, who.name, oEquip.getScore(), who.level, who.school, idx=oEquip.idx, id=oEquip.id)

def removeEquipScoreRank(who, oEquip):
	'''卸下装备时，从排行榜删除
	'''
	iWeaPos = oEquip.wearPos()
	sRankName = rank.load.gdEquipPosRank.get(iWeaPos, "")
	rankObj = getRankObjByName(sRankName)
	rankObj.removeRecordByUid(who.id)

#===============================================
#===============================================
#战斗力排行榜
def updateRoleFightRank(who):
	'''角色战斗力改变，更新排行榜
	'''
	iHighestFightPower = rankCompositeScore(who)
	#总榜
	rankObj = getRankObjByName("rank_school_all")
	if isUpdateRank(who, rankObj):
		rankObj.updateScore(who.id, who.name, iHighestFightPower, who.level, who.school)

	#分榜
	sRankName = rank.load.gdSchoolRank.get(who.school, "")
	if sRankName not in gdRankObjNameMap:	#todo 临时修改，指令可以随意修改门派
		return
	rankObj = getRankObjByName(sRankName)
	if isUpdateRank(who, rankObj):
		rankObj.updateScore(who.id, who.name, iHighestFightPower, who.level, who.school)


#===============================================
#竞技排行榜
def updateRacePointRank(who):
	iRacePoint = who.getRacePoint()
	if not iRacePoint:
		return
	rankObj = getRankObjByName("rank_race_point")
	if not isUpdateRank(who, rankObj):
		return

	iHighestFightPower = rankCompositeScore(who)
	rankObj.updateScore(who.id, who.name, iRacePoint, who.level, who.school, history=rankObj.getValue(who.id))

#===============================================
#帮派排行榜
# def updateGuildFightRank(oGuild):
# 	rankObj = getRankObjByName("rank_guild")
# 	rankObj.updateScore(oGuild.getGuildId(), oGuild.name, iRacePoint, oGuild.level, 0)

# def removeGuildFightRank(oGuild):
# 	rankObj = getRankObjByName("rank_guild")
# 	rankObj.removeRecordByUid(oGuild.getGuildId())

#===============================================

#探宝排行榜
def updateTreasurePointRank(who):
	point = who.week.fetch("treasureP")
	if not point:
		return
	rankObj = getRankObjByName("rank_treasure_point")
	if not isUpdateRank(who, rankObj):
		return
	rankObj.updateScore(who.id, who.name, point, who.level, who.school, history=rankObj.getValue(who.id))

#试炼幻境排行榜
def updateFairylandPointRank(who):
	stageNo,time = who.week.fetch("flFast",(0,0))
	if not stageNo:
		return
	rankObj = getRankObjByName("rank_race_fairyland")
	if not isUpdateRank(who, rankObj):
		return
	rankObj.updateScore(who.id, who.name, stageNo, who.level, who.school, time=time)


#===============================================
#殿试排行榜
def updateFinalExamRank(who, com, comTime, firstExamTime):
	#com 完成情况
	#comTime 完成时间
	#firstExamTime 初试耗时
	rankObj = getRankObjByName("rank_finalExam")
	if not isUpdateRank(who, rankObj):
		return
	rankObj.updateScore(who.id, who.name, com, who.level, who.school, com=com, comTime=comTime, firstET=firstExamTime)


#===============================================
#组队积分排行榜
def updateTeamRacePointRank(who):
	actObj = activity.getActivity("teamRace")
	if not actObj:
		return
	iRankIndex = actObj.getGroupIndexByLv(who.level)
	if not iRankIndex:
		return
	rankObj = getRankObjByName("rank_teamrace_point_{}".format(iRankIndex))
	if not rankObj:
		return
	if not isUpdateRank(who, rankObj):
		return
	iTeamRacePoint = who.getTeamRacePoint()
	iScore = grade.gradeAll(who)
	dTeamRacePoint = who.fetch("teamRacePoint", {})
	rankObj.updateScore(who.id, who.name, iTeamRacePoint, who.level, who.school, score=iScore, teamRacePoint=dTeamRacePoint)

def changeTeamRacePointRank(who):
	'''升级时在哪个排行榜上榜会变化
	'''
	actObj = activity.getActivity("teamRace")
	if not actObj:
		return
	newIndex = actObj.getGroupIndexByLv(who.level)
	oldIndex = actObj.getGroupIndexByLv(who.level-1)
	if newIndex == oldIndex:
		return
	if oldIndex:
		oldRankObj = getRankObjByName("rank_teamrace_point_{}".format(oldIndex))
		if oldRankObj:#从旧榜删除
			oldRankObj.removeRecordByUid(who.id)
	#加入新榜
	updateTeamRacePointRank(who)

#===============================================

def roleUpLevel(who):
	updateLvRank(who)
	changeTeamRacePointRank(who)

#角色等级或名字改变
def roleChangeInfo(who):
	'''角色信息改变
	'''
	for _,rankObj in gdRankObj.iteritems():
		rankObj.roleChangeInfo(who)


import RankData
import RankPetData
import RankClassifyData
import role
import rank.load
import petData
import rank.defines
import activity
import grade