# -*- coding: utf-8 -*-
'''
仙盟服务
'''
import endPoint
import guild_pb2


class cService(guild_pb2.terminal2main):
	@endPoint.result
	def rpcGuildRequest(self, ep, who, reqMsg): return rpcGuildRequest(who, reqMsg)

	@endPoint.result
	def rpcGuildCreate(self, ep, who, reqMsg): return rpcGuildCreate(who, reqMsg)

	@endPoint.result
	def rpcGuildJoin(self, ep, who, reqMsg): return rpcGuildJoin(who, reqMsg)

	@endPoint.result
	def rpcGuildJoinCancel(self, ep, who, reqMsg): return rpcGuildJoinCancel(who, reqMsg)

	@endPoint.result
	def rpcGuildQuit(self, ep, who, reqMsg): return rpcGuildQuit(who, reqMsg)

	@endPoint.result
	def rpcGuildListReq(self, ep, who, reqMsg): return rpcGuildListReq(who, reqMsg)

	@endPoint.result
	def rpcGuildApplyAll(self, ep, who, reqMsg): return rpcGuildApplyAll(who, reqMsg)

	@endPoint.result
	def rpcGuildSearch(self, ep, who, reqMsg): return rpcGuildSearch(who, reqMsg)

	@endPoint.result
	def rpcGuildBack(self, ep, who, reqMsg): return rpcGuildBack(who, reqMsg)

	@endPoint.result
	def rpcGuildDismiss(self, ep, who, reqMsg): return rpcGuildDismiss(who, reqMsg)

	@endPoint.result
	def rpcGuildAppoint(self, ep, who, reqMsg): return rpcGuildAppoint(who, reqMsg)

	@endPoint.result
	def rpcGuildKick(self, ep, who, reqMsg): return rpcGuildKick(who, reqMsg)

	@endPoint.result
	def rpcGuildBan(self, ep, who, reqMsg): return rpcGuildBan(who, reqMsg)

	@endPoint.result
	def rpcGuildUnBan(self, ep, who, reqMsg): return rpcGuildUnBan(who, reqMsg)

	@endPoint.result
	def rpcGuildJoinAgree(self, ep, who, reqMsg): return rpcGuildJoinAgree(who, reqMsg)

	@endPoint.result
	def rpcGuildJoinReject(self, ep, who, reqMsg): return rpcGuildJoinReject(who, reqMsg)

	@endPoint.result
	def rpcGuildJoinInvite(self, ep, who, reqMsg): return rpcGuildJoinInvite(who, reqMsg)

	@endPoint.result
	def rpcGuildApplyList(self, ep, who, reqMsg): return rpcGuildApplyList(who, reqMsg)

	@endPoint.result
	def rpcGuildBuildList(self, ep, who, reqMsg): return rpcGuildBuildList(who, reqMsg)

	@endPoint.result
	def rpcGuildClearApply(self, ep, who, reqMsg): return rpcGuildClearApply(who, reqMsg)

	@endPoint.result
	def rpcGuildTenet(self, ep, who, reqMsg): return rpcGuildTenet(who, reqMsg)

	@endPoint.result
	def rpcGuildNotice(self, ep, who, reqMsg): return rpcGuildNotice(who, reqMsg)

	@endPoint.result
	def rpcGuildMail(self, ep, who, reqMsg): return rpcGuildMail(who, reqMsg)

	@endPoint.result
	def rpcGuildAdvertise(self, ep, who, reqMsg): return rpcGuildAdvertise(who, reqMsg)

	@endPoint.result
	def rpcGuildBuildUp(self, ep, who, reqMsg): return rpcGuildBuildUp(who, reqMsg)

	@endPoint.result
	def rpcGuildBonusGet(self, ep, who, reqMsg): return rpcGuildBonusGet(who, reqMsg)
	
#===============================================================================
# 仙盟大战相关
#===============================================================================
	@endPoint.result
	def rpcGuildFightInfoRequest(self, ep, who, reqMsg): return rpcGuildFightInfoRequest(who, reqMsg)
	
	@endPoint.result
	def rpcGuildFightAutoSignUpSet(self, ep, who, reqMsg): return rpcGuildFightAutoSignUpSet(who, reqMsg)
	
	@endPoint.result
	def rpcGuildFightSignUp(self, ep, who, reqMsg): return rpcGuildFightSignUp(who, reqMsg)

	@endPoint.result
	def rpcGuildFightTeamRequest(self, ep, who, reqMsg): return rpcGuildFightTeamRequest(who, reqMsg)
	
	@endPoint.result
	def rpcGuildFightTeamMemberSelect(self, ep, who, reqMsg): return rpcGuildFightTeamMemberSelect(who, reqMsg)
	
	@endPoint.result
	def rpcGuildFightTeamMemberCancel(self, ep, who, reqMsg): return rpcGuildFightTeamMemberCancel(who, reqMsg)
	
	@endPoint.result
	def rpcGuildFightSearch(self, ep, who, reqMsg): return rpcGuildFightSearch(who, reqMsg)
	
	@endPoint.result
	def rpcGuildFightResultRequest(self, ep, who, reqMsg): return rpcGuildFightResultRequest(who, reqMsg)


def checkGuildName(who, name):
	'''检查仙盟名称
	'''
	iLen = calLen(name)
	if iLen > 6:
		message.tips(who, "仙盟名称最多#C046个#n字，请重新输入")
		return False
	elif iLen < 2:
		message.tips(who, "仙盟名称不能少于#C042个#n字")
		return False
	if name in guild.gGuildName:
		message.tips(who, "仙盟名称已经被使用了，请重新输入")
		return
	if trie.fliter(name) != name or u.isInvalidText(name):
		message.tips(who, "仙盟名称不符合规定，请重新输入")
		return False
	return True

def checkGuildTenet(who, tenet):
	'''检查仙盟宗旨
	'''
	iLen = calLen(tenet)
	if iLen > 50:
		message.tips(who, "仙盟宗旨最多#C0450个#n字，请重新输入")
		return False
	elif iLen < 1:
		message.tips(who, "仙盟宗旨不能少于#C041个#n字")
		return False
	if trie.fliter(tenet) != tenet or u.isInvalidText(tenet):
		message.tips(who, "仙盟宗旨不符合规定，请重新输入")
		return False
	return True

def checkGuildNotice(who, notice):
	'''检查仙盟公告
	'''
	iLen = calLen(notice)
	if iLen > 50:
		message.tips(who, "仙盟公告最多#C0450个#n字，请重新输入")
		return False
	elif iLen < 1:
		message.tips(who, "仙盟公告不能少于#C041个#n字")
		return False
	if trie.fliter(notice) != notice or u.isInvalidText(notice):
		message.tips(who, "仙盟公告不符合规定，请重新输入")
		return False
	return True

def checkQuit(who, oGuild):
	'''检查退出仙盟
	'''
	oMember = oGuild.getMember(who.id)
	if not oMember:
		message.tips(who, "你不在这个仙盟的成员名单中")
		return False
	if oMember.getJob() == GUILD_JOB_CHAIRMAN and oGuild.getSize() > 1:
		message.tips(who, "盟主不能脱离仙盟，请先传位给一名仙盟成员")
		return False
	
	import scene
	sceneObj = scene.getScene(who.sceneId)
	if hasattr(sceneObj, "denyGuildQuit") and sceneObj.denyGuildQuit:
		message.tips(who, sceneObj.denyGuildQuit)
		return False
	
	return True

def checkAuthority(who):
	'''检查权限
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return False
	oMember = oGuild.getMember(who.id)
	if not oMember:
		return False
	if oMember.getJob() > GUILD_JOB_ELDER:
		return  False
	return True

def checkCreate(who, name, tenet):
	'''创建检查
	'''
	if who.level < 15:
		message.tips(who, "创建仙盟需要#C04≥15级#n")
		return False
	oGuild = who.getGuildObj()
	if oGuild:
		message.tips(who, "您已经在#C02{}#n了".format(oGuild.name))
		return False
	if not checkGuildName(who, name):
		return False
	if not checkGuildTenet(who, tenet):
		return False
	# TODO
	# message.tips(who, "不符合要求，需再充值#C02$count#n后即可建立仙盟")
	pid = who.id
	if not money.checkTradeCash(who, 3000):
		message.tips(who, "元宝不足")
		return False
	who = getRole(pid)
	if not who:
		return False
	return True

def getUpgradingNeed(oGuild, idx):
	'''获取仙盟建筑资金升级需求
	'''
	oBuilding = oGuild.getBuilding(idx)
	cost = oBuilding.getCost()
	maintainFund = oGuild.getMaintainFund()
	return cost + maintainFund * 7

def checkGuildUpgrade(who, oGuild, idx):
	'''检查建筑是否可以升级
	'''
	oMember = oGuild.getMember(who.id)
	if not oMember.getJob() in (GUILD_JOB_CHAIRMAN, GUILD_JOB_CHAIRMAN_VICE):
		message.tips(who, "你的权限不够，无法升级仙盟建筑")
		return False
	if oGuild.upgrading:
		message.tips(who, "其他建筑正在升级中，等待完成后再继续升级")
		return False
	oBuilding = oGuild.getBuilding(idx)
	if not oBuilding:
		return False
	elif oBuilding.getLevel() == 5:
		message.tips(who, "已升级到满级")
		return False
	oMain = oGuild.getBuilding(BUILD_MAIN)
	if idx == BUILD_MAIN:
		ttLv = 0
		for buildObj in oGuild.buildList.itervalues():
			if buildObj.idx == BUILD_MAIN:
				continue
			ttLv += buildObj.getLevel()
		if ttLv < oMain.getLevel() * 3:
			message.tips(who, "升级条件不符合，请先升级其他建筑")
			return False
	elif oBuilding.getLevel() >= oMain.getLevel():
			message.tips(who, "升级条件不符合，请先升级其他建筑")
			return False
	if oGuild.getFund() < getUpgradingNeed(oGuild, idx):
		message.tips(who, "仙盟资金不够，请先增加仙盟资金")
		return False
	return True

def checkGuildPosition(who, oGuild, pos):
	isFull = False
	posLen = len(oGuild.posMemberIds.get(pos, set()))
	if pos == GUILD_JOB_CHAIRMAN_VICE and posLen >= 1:
		isFull = True
	if pos == GUILD_JOB_ELDER and posLen >= 4:
		isFull = True
	elif pos == GUILD_JOB_ELITE and posLen >= 20:
		isFull = True
	if isFull:
		message.tips(who, "该职位人数已达上限，请调整后再任命")
		return False
	return True

def dismissConfirm(who):
	'''解散确认
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oMember = oGuild.getMember(who.id)
	if oMember.getJob() != GUILD_JOB_CHAIRMAN:
		return
	if not oGuild.fetch("dismissCheck"):
		return
	
	actObj = activity.getActivity("guildFight")
	if actObj and (actObj.inEnterTime() or actObj.inFightTime()):
		message.tips(who, "仙盟大战期间不可解散帮派")
		return
	
	guild.dismissGuild(oGuild.id)

def dismissCancel(who):
	'''取消解散
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oMember = oGuild.getMember(who.id)
	if oMember.getJob() != GUILD_JOB_CHAIRMAN:
		return
	iApply = oGuild.fetch("dismissApply")
	iCheck = oGuild.fetch("dismissCheck")
	if iApply:
		oGuild.delete("dismissApply")
	elif iCheck:
		oGuild.delete("dismissCheck")
	oGuild.set("dismissCancel", getSecond())
	message.tips(who, "你取消了仙盟解散")
	message.guildMessage(oGuild.id, "盟主#C01{}#n取消了仙盟解散".format(who.name))

def rpcGuildRequest(who, reqMsg):
	'''请求仙盟信息
	'''
	ti = getSecond()
	if ti - getattr(who, "rpcGuildRequest", 0) < 5:
		message.tips(who, "请求太频繁")
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		rpcGuildList(who)
	else:
		rpcGuildInfo(who)
		rpcGuildWelfareInfo(who)
	setattr(who, "rpcGuildRequest", ti)

def rpcGuildCreate(who, reqMsg):
	'''创建仙盟
	'''
	name = reqMsg.name
	tenet = reqMsg.tenet
	pid = who.id
	if not checkCreate(who, name, tenet):
		return
	who = getRole(pid)
	if not who:
		return
	who.addTradeCash(-3000, "创建仙盟消耗", None)
	guildId = GUId.gGuildId.nextId()	#公会ID生成器
	oGuild = guild.newGuild(guildId, name, tenet, pid)
	memberObj = guild.newMember(who, GUILD_JOB_CHAIRMAN)
	oGuild.addMember(memberObj)
	hl = oGuild.getHyperLink(pid)
	message.tips(who, "成功创建仙盟#C02{}#n".format(name))
	message.guildAnnounce(oGuild.id, "#C01{}#n创建了仙盟#C02{}#n，志同道合的玩家可前往加入{}".format(who.name, name, hl))
	title = "创建仙盟"
	content1 = "你成功创建了仙盟，从下周开始，每周一将会返还#IG#n#C02500#n，持续三周"
	content2 = "你成功创建了仙盟，这是返还的#IG#n#C02500#n"
	propsObj = props.new(200002)
	propsObj.setValue(500)
	mail.sendGuildMail(who.id, title, content1, [], 0)
	mail.sendSysMail(who.id, title, content2, [propsObj], 0)
	rpcGuildOperateRes(who, 1, True)
	rpcGuildInfo(who)
	rpcGuildWelfareInfo(who)

	import listener
	listener.doListen("创建仙盟", who, guildId=guildId)

def rpcGuildJoin(who, reqMsg):
	'''申请加入仙盟
	'''
	if who.level < 15:
		message.tips(who, "加入仙盟需要#C02≥15级#n")
		return
	oGuild = who.getGuildObj()
	if oGuild:
		message.tips(who, "你已有仙盟，无须申请加入")
		return
	guildId = reqMsg.iValue
	oGuild = guild.getGuild(guildId)
	if not oGuild:
		message.tips(who, "该仙盟不存在")
		return
	if oGuild.isApplied(who.id):
		message.tips(who, "你已经申请该仙盟了")
		return
	oGuild.addApplyMember(who.id, who.level, who.school, who.name)
	message.tips(who, "成功申请加入仙盟#C02{}#n".format(oGuild.name))
	pushGuildApplyInfo(oGuild)
	rpcGuildOperateRes(who, 2, True, guildId)

def rpcGuildJoinCancel(who, reqMsg):
	'''取消申请加入仙盟
	'''
	guildId = reqMsg.iValue
	oGuild = guild.getGuild(guildId)
	if not oGuild:
		return
	oGuild.removeApplyMember(who.id)
	pushGuildApplyInfo(oGuild)
	rpcGuildOperateRes(who, 7, True, guildId)

def rpcGuildQuit(who, reqMsg):
	'''退出仙盟
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "你还没加入任何仙盟")
		# rpcGuildOperateRes(who, 3, False)
		return
	if not checkQuit(who, oGuild):
		return
	# 只有帮主一人时
	# 是否脱离仙盟？脱离仙盟后本仙盟将会解散。（脱离后帮贡会被冻结，加入新仙盟后恢复）
	oMember = oGuild.getMember(who.id)
	pushGuildMemberChange(oGuild, 2, oMember)
	pushGuildMemberSizeNotify(oGuild)
	oGuild.removeMember(who.id)
	if len(oGuild.memberList) == 0:
		guild.dismissGuild(oGuild.id)
	else:
		log = "志不同，道不合，#C01{}#n离开了我们的仙盟".format(who.name)
		oGuild.addLog(log)
		message.guildMessage(oGuild.id, log)
	message.tips(who, "你已成功脱离仙盟")
	rpcGuildOperateRes(who, 3, True)

def rpcGuildApplyAll(who, reqMsg):
	'''一键申请
	'''
	if who.level < 15:
		message.tips(who, "加入仙盟需要#C02≥15级#n")
		return
	oGuild = who.getGuildObj()
	if oGuild:
		message.tips(who, "你已有仙盟，无须申请加入")
		return

	now = getSecond()
	if hasattr(who,"guildApplyAllTime") and who.guildApplyAllTime - now < 5*60:
		message.tips(who,"一键申请速度过快，两次一键申请间隔为#C045分钟#n")
		return
	lGuildId = guild.gGuildKeeper.getKeys()
	lGuildId.sort()
	lNotMax = []
	for (iGuildId,) in lGuildId:
		oGuild = guild.gGuildKeeper.getObj(iGuildId)
		if oGuild.getSize() < oGuild.getMaxSize():
			lNotMax.append(oGuild)

	iLen = len(lNotMax)
	if iLen <= 20:
		for oGuild in lNotMax:
			oGuild.addApplyMember(who.id, who.level, who.school, who.name)
			pushGuildApplyInfo(oGuild)
	else:
		teamCount = max(1,iLen/10)
		perCount = (10 + teamCount - 1) / teamCount * 2
		randList = range(10)
		for teamNo in xrange(teamCount):
			lst = shuffleList(randList,perCount)
			for i in lst:
				index = i + teamNo*10
				oGuild = lNotMax[index]
				oGuild.addApplyMember(who.id, who.level, who.school, who.name)
				pushGuildApplyInfo(oGuild)

	who.guildApplyAllTime = now
	rpcGuildList(who)

def rpcGuildSearch(who, reqMsg):
	message.tips(who, "该功能尚未开放")

def rpcGuildBack(who, reqMsg):
	if who.inEscort():
		message.tips(who, "运镖中不能传送")
		return
	elif who.inTreasure():
		message.tips(who, "探宝中不能传送")
		return
	guildId = reqMsg.iValue
	if not guildId:
		oGuild = who.getGuildObj()
	else:
		oGuild = guild.getGuild(guildId)
	if not oGuild:
		message.tips(who, "该仙盟不存在")
		return
	elif not oGuild.scene:
		message.tips(who, "该仙盟场景不存在")
		return
	teamObj = who.inTeam()
	if teamObj and not teamObj.isLeader(who.id): # 在队，只有队长才能操作
		message.tips(who, "队伍中无法传送")
		return
	if not scene.tryTransfer(who, oGuild.scene.id, None, None):
		return

def rpcGuildDismiss(who, reqMsg):
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oMember = oGuild.getMember(who.id)
	if oMember.getJob() != GUILD_JOB_CHAIRMAN:
		return
	if oGuild.fetch("dismissApply"):
		message.tips(who, "仙盟已处于解散倒计时中")
		return
	if getSecond() - oGuild.fetch("dismissCancel") < 3600 * 168:
		message.tips(who, "取消解散后需间隔#C047天#n才可再次申请")
		return
	
	actObj = activity.getActivity("guildFight")
	if actObj and (actObj.inEnterTime() or actObj.inFightTime()):
		message.tips(who, "仙盟大战期间不可解散帮派")
		return
	
	title = "仙盟解散申请"
	content = "您已经发起解散仙盟行动，请在#C0472#n小时小时后前往仙盟管理员处确认解散，等待期间可选择取消"
	mail.sendGuildMail(who.id, title, content, [], 0)
	oGuild.set("dismissApply", getSecond())
	message.guildMessage(oGuild.id, "盟主已经发起了#C04仙盟解散#n，#C0472#n小时后，在盟主确认之后本盟将被解散，在此期间盟主可随时取消解散")
	message.tips(who, "已进入帮派解散流程")

def rpcGuildAppoint(who, reqMsg):
	if not checkAuthority(who):
		message.tips(who, "权限不足")
		return
	roleId = reqMsg.roleId
	pos = reqMsg.position
	if not pos in guildJobName:
		return
	elif pos == GUILD_JOB_APPRENTICE:
		message.tips(who, "不能任命为学徒")
		return
	oGuild = who.getGuildObj()
	oOperate = oGuild.getMember(who.id)
	oMember = oGuild.getMember(roleId)
	if not oOperate or not oMember:
		return
	elif oOperate.getJob() > oMember.getJob():
		message.tips(who, "权限不足")
		return
	elif not checkGuildPosition(who, oGuild, pos):
		return
	if pos == GUILD_JOB_CHAIRMAN:
		if getSecond() - oMember.fetch("joinTime") < 3600 * 72:
			message.tips(who, "该成员加入仙盟不足#C0472小时#n")
			return
		elif oMember.getJob() == GUILD_JOB_APPRENTICE:
			message.tips(who, "无法传位给学徒")
			return
		oGuild.appoint(oOperate.id, GUILD_JOB_COMMON)
		pushGuildUpdateInfo(oGuild, "chairman")
		pushGuildMemberChange(oGuild, 3, oOperate)
	oGuild.appoint(oMember.id, pos)
	log = "#C01{}#n将#C01{}#n任命为#C02{}#n".format(who.name, oMember.name, guildJobName[pos])
	oGuild.addLog(log)
	message.guildMessage(oGuild.id, log)
	pushGuildMemberChange(oGuild, 3, oMember)
	message.tips(who, "成功任命为{}".format(guildJobName[pos]))

def rpcGuildBan(who, reqMsg):
	roleId = reqMsg.iValue
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oOperate = oGuild.getMember(who.id)
	oMember = oGuild.getMember(roleId)
	if not oMember or not oOperate:
		return
	if oOperate.getJob() > oMember.getJob():
		return
	if not oGuild.setBan(oOperate.getJob(), roleId):
		message.tips(who, "该成员已经被禁言过了")
		return
	log = "#C01{}#n将#C01{}#n禁言1小时".format(who.name, oMember.name)
	# oGuild.addLog(log)
	message.guildMessage(oGuild.id, log)
	message.tips(who, "已把{}禁言1小时".format(oMember.name))
	pushGuildMemberChange(oGuild, 3, oMember)

def rpcGuildUnBan(who, reqMsg):
	roleId = reqMsg.iValue
	oGuild = who.getGuildObj()
	oOperate = oGuild.getMember(who.id)
	oMember = oGuild.getMember(roleId)
	if not oMember or not oOperate:
		return
	ret = oGuild.unBan(oOperate.getJob(),roleId)
	if ret == 0:
		message.tips(who, "该成员没有被禁言")
		return
	elif ret == -1:
		message.tips(who, "禁言人权限比你高，你无法解除禁言")
		return
	elif ret == roleId:
		log = "#C01{}#n将#C01{}#n的禁言解除了".format(who.name, oMember.name)
		# oGuild.addLog(log)
		message.guildMessage(oGuild.id, log)
		message.tips(who, "成功解除{}的禁言".format(oMember.name))
		pushGuildMemberChange(oGuild, 3, oMember)

def rpcGuildListReq(who, reqMsg):
	rpcGuildList(who)

def rpcGuildKick(who, reqMsg):
	'''踢出仙盟
	'''
	if not checkAuthority(who):
		message.tips(who, "权限不足")
		return
	roleId = reqMsg.iValue
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oMember = oGuild.getMember(roleId)
	if not oMember:
		message.tips(who, "该角色不在本帮")
		return
	
	actObj = activity.getActivity("guildFight")
	if actObj and (actObj.inEnterTime() or actObj.inFightTime()):
		message.tips(who, "仙盟大战期间不可踢人出帮")
		return
	targetName = oMember.name
	oTarget = getRole(roleId)
	if oTarget:
		message.tips(oTarget, "#C01{}#n将你逐出了仙盟".format(who.name))
	log = "#C01{}#n将#C01{}#n逐出了仙盟".format(who.name, targetName)
	oGuild.addLog(log)
	pushGuildMemberChange(oGuild, 2, oMember)
	pushGuildMemberSizeNotify(oGuild)
	oGuild.removeMember(roleId)
	message.guildMessage(oGuild.id, log)
	message.tips(who, "已把{}踢出仙盟".format(targetName))
	content = "你已被逐出仙盟#C07{}#n".format(oGuild.name)
	mail.sendGuildMail(roleId, "逐出仙盟", content, [], 0)
	message.message(roleId, content)

def rpcGuildJoinInvite(who, reqMsg):
	'''邀请入帮
	'''
	roleId = reqMsg.iValue
	oTarget = getRole(roleId)
	if not oTarget:
		message.tips(who, "对方不在线")
		return
	elif oTarget.getGuildId():
		message.tips(who, "对方已有仙盟")
		return
	elif oTarget.level < 15:
		message.tips(who, "加入仙盟需要#C04≥15级#n")
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "你还没有仙盟")
		return
	oOperate = oGuild.getMember(who.id)
	message.tips(who, "正在邀请对方加入#C02{}#n，请等待对方接受".format(oGuild.name))
	pid = who.id
	myGreenlet.cGreenlet.spawn(sendInvite, pid, roleId)

def sendInvite(pid, targetId):
	who = getRole(pid)
	if not who:
		return
	targetObj = getRole(targetId)
	if not targetObj:
		return
	if targetObj.getGuildId():
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	content = "#C06{}#n邀请你加入仙盟#C07{}#n，是否接受？\nQ拒绝#20\nQ接受".format(who.name, oGuild.name)
	message.confirmBoxNew(targetObj, functor(responseInvite, pid), content)
		
def responseInvite(targetObj, yes, pid):
	who = getRole(pid)
	if not who:
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	if targetObj.id in oGuild.memberList:
		return
	if not yes:
		message.tips(who, "#C01{}#n谢绝加入本盟".format(targetObj.name))
		return
	if not checkAuthority(who):
		oGuild.addApplyMember(targetObj.id, targetObj.level, targetObj.school, targetObj.name)
		message.tips(targetObj, "你同意加入#C02{}#n".format(oGuild.name))
		message.tips(who, "#C01{}#n同意加入本盟".format(targetObj.name))
	else:
		if oGuild.getSize() > oGuild.getMaxSize():
			oGuild.addApplyMember(targetObj.id, targetObj.level, targetObj.school, targetObj.name)
			message.tips(targetObj, "你同意加入#C02{}#n".format(oGuild.name))
			message.tips(who, "#C01{}#n同意加入本盟，请到申请列表中查看".format(targetObj.name))
		else:
			position = GUILD_JOB_APPRENTICE if targetObj.level < 40 else GUILD_JOB_COMMON
			memberObj = guild.newMember(targetObj, position)
			message.tips(targetObj, "#C01{}#n同意了你的入盟申请".format(oGuild.name))
			oGuild.addMember(memberObj)
			title = "加入仙盟"
			content = "你的申请已被通过，欢迎加入#C02{}#n".format(oGuild.name)
			log = "欢迎新成员#C01{}#n加入我们的仙盟".format(memberObj.name)
			oGuild.addLog(log)
			message.guildMessage(oGuild.id, log)
			mail.sendGuildMail(targetObj.id, title, content, [], 0)
			rpcGuildInfo(targetObj)
			rpcGuildWelfareInfo(targetObj)
			pushGuildMemberChange(oGuild, 1, memberObj)

def rpcGuildJoinAgree(who, reqMsg):
	'''同意入帮申请
	'''
	if not checkAuthority(who):
		message.tips(who, "权限不足")
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		message.tips(who, "仙盟不存在")
		return
	if oGuild.getSize() >= oGuild.getMaxSize():
		message.tips(who, "仙盟人数已达上限")
		return
	roleId = reqMsg.iValue
	oResume = resume.getResume(roleId)
	guildId = oResume.fetch("guildId")
	oGuild.removeApplyMember(roleId)
	if guildId:
		message.tips(who, "该玩家已经加入仙盟了")
	else:
		oTarget = getRole(roleId)
		if oTarget:
			position = GUILD_JOB_APPRENTICE if oTarget.level < 40 else GUILD_JOB_COMMON
			memberObj = guild.newMember(oTarget, position)
			message.tips(oTarget, "#C01{}#n同意了你的入帮申请".format(oGuild.name))
		else:
			roleInfo = {}
			level = oResume.fetch("level")
			position = GUILD_JOB_APPRENTICE if level < 40 else GUILD_JOB_COMMON
			roleInfo["roleId"] = roleId
			roleInfo["name"] = oResume.fetch("name")
			roleInfo["level"] = level
			roleInfo["school"] = oResume.fetch("school")
			roleInfo["shape"] = oResume.fetch("shape")
			memberObj = guild.newMemberByData(roleInfo)
			memberObj.setJob(position)
		oGuild.addMember(memberObj)
		title = "加入仙盟"
		content = "你的申请已被通过，欢迎加入#C07{}#n".format(oGuild.name)
		log = "欢迎新成员#C01{}#n加入本盟".format(memberObj.name)
		oGuild.addLog(log)
		message.guildMessage(oGuild.id, log)
		mail.sendGuildMail(roleId, title, content, [], 0)
		if oTarget:
			rpcGuildInfo(oTarget)
			rpcGuildWelfareInfo(oTarget)
		pushGuildMemberSizeNotify(oGuild)
		pushGuildMemberChange(oGuild, 1, memberObj, roleId)
	pushGuildApplyChange(oGuild, 2, roleId)

def rpcGuildJoinReject(who, reqMsg):
	'''拒绝入帮申请
	'''
	if not checkAuthority(who):
		message.tips(who, "权限不足")
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	roleId = reqMsg.iValue
	oResume = resume.getResume(roleId)
	guildId = oResume.fetch("guildId")
	oGuild.removeApplyMember(roleId)
	if not guildId:
		oTarget = getRole(roleId)
		if oTarget:
			message.tips(oTarget, "#C01{}#n拒绝了你的入帮申请".format(oGuild.name))
	pushGuildApplyChange(oGuild, 2, roleId)

def rpcGuildApplyList(who, reqMsg):
	'''请求申请入帮列表
	'''
	rpcGuildApplyInfo(who)

def rpcGuildBuildList(who, reqMsg):
	'''请求仙盟建筑列表
	'''
	rpcGuildBuildInfo(who)

def rpcGuildClearApply(who, reqMsg):
	'''清空申请列表
	'''
	if not checkAuthority(who):
		message.tips(who, "权限不足")
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oGuild.clearApplyList()
	pushGuildApplyChange(oGuild, 1, 0)

def rpcGuildTenet(who, reqMsg):
	'''修改仙盟宗旨
	'''
	if not checkAuthority(who):
		message.tips(who, "权限不足")
		return
	tenet = reqMsg.sValue
	if not checkGuildTenet(who, tenet):
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oGuild.setTenet(tenet)
	rpcGuildOperateRes(who, 4, True)
	pushGuildUpdateInfo(oGuild, "tenet")

def rpcGuildNotice(who, reqMsg):
	'''修改仙盟公告
	'''
	if not checkAuthority(who):
		message.tips(who, "权限不足")
		return
	notice = reqMsg.sValue
	if not checkGuildNotice(who, notice):
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oGuild.setNotice(notice)
	rpcGuildOperateRes(who, 5, True)
	pushGuildUpdateInfo(oGuild, "notice")

def rpcGuildMail(who, reqMsg):
	'''仙盟邮件
	'''
	if not checkAuthority(who):
		message.tips(who, "权限不足")
		return
	content = reqMsg.sValue
	if trie.fliter(content) != content or u.isInvalidText(content):
		message.tips(who, "输入字符含有非法词汇，请修改后再确定")
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	if not hasattr(oGuild, "mailTime"):
		oGuild.mailTime = 0
	ti = getSecond()
	if ti - oGuild.mailTime < 300:
		message.tips(who, "两次发送仙盟邮件需间隔#C045分钟#n")
		return
	for oMember in oGuild.memberList.itervalues():
		mail.sendGuildMail(oMember.id, "仙盟群体邮件", content, [], 0)
	oGuild.mailTime = ti
	message.tips(who, "已向所有成员发送邮件")
	rpcGuildOperateRes(who, 6, True)

def rpcGuildAdvertise(who, reqMsg):
	'''仙盟宣传
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	if not hasattr(oGuild, "advertiseTime"):
		oGuild.advertiseTime = 0
	ti = getSecond()
	if ti - oGuild.advertiseTime < 3600:
		message.tips(who, "你已经宣传过了，两次宣传之间需要间隔#C041小时#n")
		return
	hl = oGuild.getHyperLink(who.id)
	content = "仙盟#C02{}#n正在广发英雄帖，希望有识之士前来共同发展。{}".format(oGuild.name, hl)
	message.guildAnnounce(oGuild.id, content)
	message.tips(who, "成功在无仙盟成员的仙盟频道宣传")
	oGuild.advertiseTime = ti

def rpcGuildBuildUp(who, reqMsg):
	'''升级仙盟建筑
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	idx = reqMsg.idx
	if not checkGuildUpgrade(who, oGuild, idx):
		return
	oBuilding = oGuild.getBuilding(idx)
	cost = oBuilding.getCost()
	oGuild.addFund(-cost)
	oGuild.buildingUpgrade(idx)
	pushGuildUpdateInfo(oGuild, "build", "fund")
	rpcGuildOperateRes(who, 8, True)

def rpcGuildBonusGet(who, reqMsg):
	'''领取仙盟分红
	'''
	if who.week.fetch("guildPoint", iWhichCyc=-1) < 200:
		message.tips(who, "需上周仙盟贡献达到200点才有仙盟分红")
		return
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oMember = oGuild.getMember(who.id)
	bonus = oMember.getBonus()
	if not bonus:
		message.tips(who, "没有帮派分红")
		return
	who.addCash(bonus, "仙盟分红领取")
	who.week.set("guildBonus", 1)
	message.tips(who, "你领取了仙盟分红，获得#R<{},3,2>#n".format(bonus))
	rpcGuildWelfareInfo(who)

def rpcGuildOperateRes(who, operate, result, args=0):
	'''仙盟相关操作结果
	'''
	msg = guild_pb2.operateInfo()
	msg.idx = operate
	msg.result = result
	msg.args = args
	who.endPoint.rpcGuildOperateRes(msg)

def rpcGuildList(who):
	'''仙盟列表
	'''
	msg = guild_pb2.guildList()
	guildList = []
	for guildObj in guild.gGuildKeeper.getIterValues():
		guildOv = guild_pb2.guildOverview()
		guildOv.guildId = guildObj.getGuildId()
		guildOv.level = guildObj.level
		guildOv.vitality = guildObj.getVitality()
		guildOv.size = guildObj.getSize()
		guildOv.maxSize = guildObj.getMaxSize()
		guildOv.name = guildObj.name
		guildOv.tenet = guildObj.getTenet()
		chairmanId = guildObj.getChairmanId()
		oChairman = guildObj.getMember(chairmanId)
		if not oChairman:
			continue
		chairman = packGuildMember(oChairman)
		guildOv.chairman.CopyFrom(chairman)
		if who.getGuildObj():
			isApply = False
		else:
			isApply = guildObj.isApplied(who.id)
		guildOv.isApply = isApply
		guildList.append(guildOv)
	msg.guilds.extend(guildList)
	who.endPoint.rpcGuildList(msg)

def rpcGuildInfo(who):
	'''仙盟详细信息
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oMember = oGuild.getMember(who.id)
	if oMember and not oMember.isRequested:
		oMember.isRequested = True
	msg = packGuildInfo(oGuild)
	who.endPoint.rpcGuildInfo(msg)

def rpcGuildApplyInfo(who):
	'''入帮申请信息
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	msg = packGuildApplyList(oGuild)
	who.endPoint.rpcGuildApplyInfo(msg)

def rpcGuildBuildInfo(who):
	'''仙盟建筑信息
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	msg = packGuildBuildList(oGuild)
	who.endPoint.rpcGuildBuildInfo(msg)

def rpcGuildWelfareInfo(who):
	'''帮派福利信息
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	oMember = oGuild.getMember(who.id)
	if not oMember:
		return
	msg = guild_pb2.welfareInfo()
	msg.bonus = oMember.getBonus() if who.week.fetch("guildPoint", iWhichCyc=-1) >= 200 else 0
	msg.isBonusGet = bool(who.week.fetch("guildBonus"))
	who.endPoint.rpcGuildWelfareInfo(msg)

def rpcGuildInfoUpdate(who, *attr):
	'''更新仙盟信息
	'''
	oGuild = who.getGuildObj()
	if not oGuild:
		return
	msg = guild_pb2.guildInfo()
	msg.guildId = oGuild.getGuildId()
	attrs = ["level", "vitality", "name", "tenet", "birth", "online", "size", "maxSize", "notice", "fund", "bonus",
				"apprenticeMax", "apprenticeSize", "apprenticeOnline", "chairmanId"]
	for name in attrs:
		if name in attr:
			setattr(msg, name, oGuild.getValByName(name))
	if "chairman":
		msg.chairman = oGuild.chairmanName
	if "build" in attr:
		msg.build.CopyFrom(packGuildBuildList(oGuild))
	if "log" in attr:
		msg.log.CopyFrom(packGuildLogList(oGuild))
	if "maintain" in attr:
		msg.maintain = oGuild.getMaintainFund()
	who.endPoint.rpcGuildInfoUpdate(msg)

def rpcGuildMemberNotify(who, idx, oMember):
	'''仙盟成员变动通知
	@idx通知类型1增加2删除3修改
	@member成员信息
	'''
	msg = guild_pb2.memberNotify()
	msg.idx = idx
	msg.member.CopyFrom(packGuildMember(oMember))
	who.endPoint.rpcGuildMemberNotify(msg)

def rpcGuildApplyNotify(who, idx, roleId):
	'''仙盟申请变动通知
	@idx:通知类型1清空2删除
	@roleId:申请人ID
	'''
	msg = guild_pb2.applyNotify()
	msg.idx = idx
	if roleId:
		msg.roleId = roleId
	who.endPoint.rpcGuildApplyNotify(msg)

def packGuildInfo(oGuild):
	'''打包仙盟详细信息
	'''
	attrs = ["guildId", "level", "vitality", "name", "tenet", "birth", "online", "size", "maxSize", "notice", "fund", "bonus", "chairmanId"]
	msg = guild_pb2.guildInfo()
	msg.chairman = oGuild.chairmanName
	for attr in attrs:
		setattr(msg, attr, oGuild.getValByName(attr))
	msg.maintain = oGuild.getMaintainFund()
	msg.member.CopyFrom(packGuildPageMember(oGuild))
	msg.apply.CopyFrom(packGuildApplyList(oGuild))
	msg.build.CopyFrom(packGuildBuildList(oGuild))
	msg.log.CopyFrom(packGuildLogList(oGuild))
	msg.apprenticeOnline = oGuild.getApprenticeOnline()
	msg.apprenticeSize = oGuild.getApprenticeSize()
	msg.apprenticeMax = oGuild.getApprenticeMax()
	return msg

def packGuildPageMember(oGuild, iPage=1):
	'''打包仙盟分页成员信息
	'''
	msg = guild_pb2.guildMember()
	msg.page = iPage
	msg.totalPage = 1
	members = []
	for oMember in oGuild.memberList.values():
		memberMsg = packGuildMember(oMember)
		members.append(memberMsg)
	msg.members.extend(members)
	return msg

def packGuildSingleMember(oMember):
	msg = guild_pb2.guildMember()
	members = []
	memberMsg = packGuildMember(oMember)
	members.append(memberMsg)
	msg.members.extend(members)
	return msg

def packGuildMember(oMember):
	'''打包仙盟成员信息
	'''
	oGuild = guild.getGuild(oMember.ownerId)
	msg = guild_pb2.member()
	msg.roleId = oMember.id
	msg.level = oMember.level
	msg.name = oMember.name
	msg.school = oMember.school
	msg.shape = oMember.shape
	msg.position = oMember.getJob()
	msg.joinTime = oMember.fetch("joinTime")
	msg.offlineTime = oMember.getOfflineTime()
	msg.shapeParts.extend(oMember.shapeParts)
	msg.colors.extend(oMember.colors)
	msg.curContri = oMember.fetch("curContri")
	msg.totalContri = oMember.fetch("totalContri")
	weekRing = oMember.fetch("guildRing")
	msg.guildTask.extend([weekRing, 140])
	weekFight = oMember.fetch("guildFight")
	msg.guildFight.extend([weekFight, 3])
	msg.activeDays = oMember.fetch("activeDays")
	msg.fightCnt = oMember.fetch("ttGuildFight")
	msg.banTalk = oMember.id in oGuild.banList
	return msg

def packGuildApplyList(oGuild):
	'''打包入帮申请信息
	'''
	msg = guild_pb2.applyList()
	applyList = []
	for roleId, roleInfo in oGuild.applyList.iteritems():
		applyInfo = guild_pb2.applyInfo()
		applyInfo.roleId = roleId
		applyInfo.level = roleInfo["level"]
		applyInfo.school = roleInfo["school"]
		applyInfo.name = roleInfo["name"]
		applyList.append(applyInfo)
	msg.applys.extend(applyList)
	return msg

def packGuildBuildList(oGuild):
	msg = guild_pb2.buildList()
	buildList = []
	for idx, buildObj in oGuild.buildList.iteritems():
		buildInfo = guild_pb2.buildMsg()
		buildInfo.idx = idx
		buildInfo.level = buildObj.getLevel()
		cost = buildObj.getCost()
		if cost > 0:
			buildInfo.cost = buildObj.getCost()
			buildInfo.need = getUpgradingNeed(oGuild, idx)
		ti = buildObj.getTime()
		if ti > 0:
			buildInfo.time = ti
		buildInfo.top = buildObj.getLevel() >= 5
		buildList.append(buildInfo)
	msg.build.extend(buildList)
	return msg

def packGuildLogList(oGuild):
	msg = guild_pb2.logList()
	msg.log.extend(oGuild.fetch("log", [])[-50:]) # 只发后50条
	return msg

def pushGuildMemberSizeNotify(oGuild):
	'''仙盟成员数量变动通知
	'''
	updateInfoList = ["online", "size", "maxSize", "apprenticeMax", "apprenticeSize", "apprenticeOnline"]
	for roleId, oMember in oGuild.memberList.iteritems():
		who = getRole(roleId)
		if who and oMember.isRequested:
			rpcGuildInfoUpdate(who, *updateInfoList)

def pushGuildUpdateInfo(oGuild, *infoName):
	'''推送更新信息到客户端
	'''
	for roleId, oMember in oGuild.memberList.iteritems():
		who = getRole(roleId)
		if who and oMember.isRequested:
			rpcGuildInfoUpdate(who, *infoName)

def pushGuildMemberChange(oGuild, changeType, oTarget, iExclude=0):
	'''更新成员变化到客户端
	'''
	for roleId, oMember in oGuild.memberList.iteritems():
		if roleId == iExclude:
			continue
		who = getRole(roleId)
		if who and oMember.isRequested:
			rpcGuildMemberNotify(who, changeType, oTarget)

def pushGuildApplyChange(oGuild, changeType, applyId):
	'''更新申请信息到客户端
	'''
	for roleId, oMember in oGuild.memberList.iteritems():
		who = getRole(roleId)
		if who and oMember.isRequested:
			rpcGuildApplyNotify(who, changeType, applyId)

def pushGuildApplyInfo(oGuild):
	for roleId, oMember in oGuild.memberList.iteritems():
		who = getRole(roleId)
		if who and oMember.isRequested:
			rpcGuildApplyInfo(who)

#===============================================================================
# 仙盟大战相关
#===============================================================================
def validFightReceive(func):
	'''检查接收仙盟大战相关数据
	'''
	def _func(who, reqMsg):
		print "\nvalidFightReceive", func.__name__, "roleId:%d" % who.id, str(reqMsg).replace("\n", ",")
		guildObj = who.getGuildObj()
		if not guildObj:
			return
		actObj = activity.getActivity("guildFight")
		if not actObj:
			return
		func(guildObj, actObj, who, reqMsg)
	return _func

def validFightSend(func):
	'''检查发送仙盟大战相关数据
	'''
	def _func(who, *args, **kwargs):
		print "\nvalidFightSend", func.__name__, "roleId:%d" % who.id, args, kwargs
		guildObj = who.getGuildObj()
		if not guildObj:
			return
		actObj = activity.getActivity("guildFight")
		if not actObj:
			return
		func(guildObj, actObj, who, *args, **kwargs)
	return _func

@validFightReceive
def rpcGuildFightInfoRequest(guildObj, actObj, who, reqMsg):
	'''请求仙盟大战信息
	'''
	rpcGuildFightInfo(who)
	
@validFightReceive
def rpcGuildFightAutoSignUpSet(guildObj, actObj, who, reqMsg):
	'''设置自动报名
	'''
	isAutoSignUp = reqMsg.bValue
	if guildObj.getJob(who.id) not in FIGHT_JOB_LIST:
		message.tips(who, "你的权限不足")
		return
	if guildObj.getFund() < guildObj.getMaintainFund() * 7:
		message.tips(who, "帮派资金大于帮派7天维护消耗才可自动报名")
		return
	guildObj.guildFight.setAutoSignUp(isAutoSignUp)
	rpcGuildFightInfoChange(who, "isAutoSignUp")
	if isAutoSignUp:
		message.tips(who, "已启动自动报名，本周仙盟大战结束后开始生效")
	else:
		message.tips(who, "已取消自动报名仙盟大战")
	
@validFightReceive
def rpcGuildFightSignUp(guildObj, actObj, who, reqMsg):
	'''仙盟大战报名
	'''
	if guildObj.getJob(who.id) not in FIGHT_JOB_LIST:
		message.tips(who, "你的权限不足")
		return
	if actObj.trySignUp(guildObj, who, "手动"):
		rpcGuildFightInfoChange(who, "isSignUp")

@validFightReceive
def rpcGuildFightTeamRequest(guildObj, actObj, who, reqMsg):
	'''请求仙盟大战精英队
	'''
	rpcGuildFightTeam(who)
	
@validFightReceive
def rpcGuildFightTeamMemberSelect(guildObj, actObj, who, reqMsg):
	'''选择精英
	'''
	roleId = reqMsg.roleId
	teamNo = reqMsg.teamNo
	if guildObj.getJob(who.id) not in FIGHT_JOB_LIST:
		message.tips(who, "你的权限不足")
		return
	if len(guildObj.guildFight.fightTeam[teamNo]) >= 5:
		message.tips(who, "当前精英组已满5人")
		return
	if guildObj.guildFight.getFightTeamNo(roleId):
		message.tips(who, "该成员已经是精英组成员了")
		return
	memberObj = guildObj.getMember(roleId)
	if not memberObj:
		message.tips(who, "该成员已退帮，请另选精英")
		return

	guildObj.guildFight.addFightTeamMember(roleId, teamNo)
	rpcGuildFightTeamMemberAdd(who, roleId, teamNo)
	if actObj.inEnterTime() or actObj.inFightTime():
		message.tips(who, "新的精英成员配置将在仙盟大战结束后生效")

@validFightReceive
def rpcGuildFightTeamMemberCancel(guildObj, actObj, who, reqMsg):
	'''取消精英
	'''
	roleId = reqMsg.roleId
	teamNo = reqMsg.teamNo
	if guildObj.getJob(who.id) not in FIGHT_JOB_LIST:
		message.tips(who, "你的权限不足")
		return
	guildObj.guildFight.removeFromFightTeam(roleId)
	rpcGuildFightTeamMemberDelete(who, roleId, teamNo)
	if actObj.inEnterTime() or actObj.inFightTime():
		message.tips(who, "新的精英成员配置将在仙盟大战结束后生效")
	
@validFightReceive
def rpcGuildFightSearch(guildObj, actObj, who, reqMsg):
	'''精英搜索
	'''
	keyword = reqMsg.keyword
	if not keyword:
		return
	
	memberList = guildObj.searchMemberList(keyword)
	rpcGuildFightSearchResult(who, memberList)
	
@validFightReceive
def rpcGuildFightResultRequest(guildObj, actObj, who, reqMsg):
	'''请求仙盟大战战报
	'''
	rpcGuildFightResult(who)


@validFightSend
def rpcGuildFightInfo(guildObj, actObj, who):
	'''仙盟大战信息
	'''
	state = actObj.getTimeState() # 仙盟大战阶段状态, 1.报名期 2.公示期 3.入场期 4.开战期
	isSignUp = actObj.isSignUp(guildObj.id)
	isAutoSignUp = guildObj.guildFight.isAutoSignUp()
	pkList = packetPKInfo(actObj, guildObj.id)

	msgObj = guild_pb2.fightInfo()
	msgObj.state = state
	msgObj.isSignUp = isSignUp
	msgObj.isAutoSignUp = isAutoSignUp
	msgObj.pkList.CopyFrom(pkList)
	who.endPoint.rpcGuildFightInfo(msgObj)
	print "\nrpcGuildFightInfo", msgObj

@validFightSend
def rpcGuildFightInfoChange(guildObj, actObj, who, *attrNames):
	'''修改仙盟大战信息
	'''
	msg = {}
	for attrName in attrNames:
		attrVal = guildObj.getValByName(attrName)
		msg[attrName] = attrVal
	who.endPoint.rpcGuildFightInfoChange(**msg)
	print "\nrpcGuildFightInfoChange", msg
	
def packetPKInfo(actObj, guildId):
	'''对手匹配信息
	'''
	guildNameList = []
	for pkList in actObj.getGroupByGuild(guildId):
		for guildIdPK in pkList:
			guildObjPK = guild.getGuild(guildIdPK)
			if guildObjPK:
				guildName = guildObjPK.name
			else:
				guildName = ""
			guildNameList.append(guildName)
				
	msgObj = guild_pb2.pkInfo()
	if guildNameList:
		msgObj.guildNameList.extend(guildNameList)
	return msgObj

@validFightSend
def rpcGuildFightTeam(guildObj, actObj, who):
	'''仙盟大战精英队
	'''
	memberMsgList = []
	for teamNo, memberList in guildObj.guildFight.fightTeam.iteritems():
		for memberId in memberList:
			memberMsg = packetFightTeamMember(guildObj, actObj, memberId, teamNo)
			if memberMsg:
				memberMsgList.append(memberMsg)
		
	msgObj = guild_pb2.fightTeam()
	if memberMsgList:
		msgObj.memberList.extend(memberMsgList)
	who.endPoint.rpcGuildFightTeam(msgObj)
	print "\nrpcGuildFightTeam", msgObj
	
def packetFightTeamMember(guildObj, actObj, memberId, teamNo=0):
	'''仙盟大战精英队队员
	'''
	memberObj = guildObj.getMember(memberId)
	if not memberObj:
		return None
	if memberObj.isOnline:
		state = 1
	else:
		state = 0
		
	if not teamNo:
		teamNo = guildObj.guildFight.getFightTeamNo(memberId)
		
	who = getRole(memberObj.id)
	if who and actObj.inGameScene(who):
		isAbsent = False
	else:
		isAbsent = True

	msgObj = guild_pb2.fightTeamMember()
	msgObj.roleId = memberObj.id
	msgObj.shape = memberObj.shape
	msgObj.name = memberObj.name
	msgObj.level = memberObj.level
	msgObj.school = memberObj.school
	msgObj.fightPower = memberObj.fetch("fightPower")
	msgObj.state = state
	msgObj.offlineTime = memberObj.fetch("offlineTime")
	msgObj.teamNo = teamNo
	msgObj.isAbsent = isAbsent
	return msgObj

@validFightSend
def rpcGuildFightTeamMemberAdd(guildObj, actObj, who, roleId, teamNo):
	'''增加精英
	'''
	msgObj = packetFightTeamMember(guildObj, actObj, roleId, teamNo)
	if msgObj:
		who.endPoint.rpcGuildFightTeamMemberAdd(msgObj)
	print "\nrpcGuildFightTeamMemberAdd", msgObj

@validFightSend
def rpcGuildFightTeamMemberDelete(guildObj, actObj, who, roleId, teamNo):
	'''删除精英
	'''
	msgObj = guild_pb2.fightTeamMember()
	msgObj.roleId = roleId
	msgObj.teamNo = teamNo
	who.endPoint.rpcGuildFightTeamMemberDelete(msgObj)
	print "\nrpcGuildFightTeamMemberDelete", msgObj

@validFightSend	
def rpcGuildFightSearchResult(guildObj, actObj, who, memberList):
	'''精英搜索结果
	'''
	memberMsgList = []
	for memberObj in memberList:
		memberMsg = packetFightTeamMember(guildObj, actObj, memberObj.id)
		if memberMsg:
			memberMsgList.append(memberMsg)
	
	msgObj = guild_pb2.searchResult()
	if memberMsgList:
		msgObj.memberList.extend(memberMsgList)
	who.endPoint.rpcGuildFightSearchResult(msgObj)
	print "\nrpcGuildFightSearchResult", msgObj

@validFightSend	
def rpcGuildFightResult(guildObj, actObj, who):
	'''仙盟大战战报
	'''
	msgObj = packetFightResult(guildObj)
	who.endPoint.rpcGuildFightResult(msgObj)
	print "\nrpcGuildFightResult", msgObj
	
def packetFightResult(guildObj):
	'''战报
	'''
	guildFight = guildObj.guildFight
	pkResultList = []
	for pkResult in guildFight.getPKResultList():
		pkResultMsg = packetPKResult(pkResult)
		pkResultList.append(pkResultMsg)

	msgObj = guild_pb2.fightResult()
	if pkResultList:
		msgObj.pkResultList.extend(pkResultList)
	msgObj.fightCount = guildFight.getFightCount()
	msgObj.winCount = guildFight.getWinCount()
	return msgObj

def packetPKResult(pkResult):
	'''战况
	'''
	score = pkResult["score"]
	score = "%d:%d" % (score[0], score[1])

	msgObj = guild_pb2.pkResult()
	msgObj.time = pkResult["time"] # 仙盟大战日期
	msgObj.result = pkResult["result"] # 战果
	msgObj.targetGuildName = pkResult["pkGuildName"] # 对手帮派名称
	msgObj.score = score # 比分
	msgObj.teamResultList.extend(pkResult["teamResultList"]) # 精英组结果
	return msgObj
	


from common import *
from guild.defines import *
import message
import money
import guild
import GUId
import resume
import trie
import mail
import u
import scene
import props
import myGreenlet
import activity
