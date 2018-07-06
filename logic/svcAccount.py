#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import terminal_main_pb2
import endPoint
import misc
import config
import primitive
import lock4key
import account_pb2
#创建账号时的默认值
DIAMOND,VIP_LV,VIP_EXP=0,0,0

#创建角色时的默认值
GOLD,EXP=0,0
SCENE_NO,X,Y=11,333,343

VOUCHER=0

if config.IS_INNER_SERVER:
	FORBID_DEL_LV=100000
else:
	FORBID_DEL_LV=40 #禁止删除角色的等级

ROLE_MAX_AMOUNT=1 #一个账号下最大允许创建的角色数

NAME_MAX_LEN=12	#姓名最大长度
NAME_OUTFAM_LEN=5 #允许不要姓的最短名字长度
SIGN_LV_LEAST=10 #开放签到等级


class cService(account_pb2.terminal2main):
	@endPoint.result
	@lock4key.lockByEndPoint
	def rpcAccountLogin(self,ep,ctrlr,reqMsg):return rpcAccountLogin(self,ep,ctrlr,reqMsg) #

	@endPoint.result
	@lock4key.lockByEndPoint
	@lock4key.lockByAccount
	def rpcCreateRole(self,ep,oAccount,reqMsg):return rpcCreateRole(ep,oAccount,reqMsg) #

	@endPoint.result
	@lock4key.lockByEndPoint
	@lock4key.lockByAccount
	def rpcDelRole(self,ep,oAccount,reqMsg):return rpcDelRole(self,ep,oAccount,reqMsg) #

	@endPoint.result
	@lock4key.lockByEndPoint
	@lock4key.lockByAccount
	def rpcRoleLogin(self,ep,oAccount,reqMsg):return rpcRoleLogin(self,ep,oAccount,reqMsg) #

	@endPoint.result
	@lock4key.lockByEndPoint
	@lock4key.lockByAccount
	def rpcRandomName(self,ep,oAccount,reqMsg):return rpcRandomName(self,ep,oAccount,reqMsg)#随机名字

	@endPoint.result
	@lock4key.lockByEndPoint
	@lock4key.lockByAccount
	def rpcSwitchRole(self,ep,oAccount,reqMsg):return rpcSwitchRole(self,ep,oAccount,reqMsg) #

	@endPoint.result
	@lock4key.lockByEndPoint
	@lock4key.lockByAccount
	def rpcAccountLogOut(self,ep,oAccount,reqMsg):return rpcAccountLogOut(self,ep,oAccount,reqMsg)

	@endPoint.result
	@lock4key.lockByEndPoint
	def rpcSetRoleName(self,ep,who,reqMsg):return rpcSetRoleName(self,ep,who,reqMsg)#设置玩家名字

	@endPoint.result
	@lock4key.lockByEndPoint
	@lock4key.lockByAccount
	def rpcForceRemoveRole(self,ep,who,reqMsg):return rpcForceRemoveRole(self,ep,who,reqMsg)

	@endPoint.result
	@lock4key.lockByEndPoint
	#@lock4key.lockByAccount #此时没有账号对象
	def rpcReconnect(self,ep,ctrl,reqMsg):return rpcReconnect(self,ep,ctrl,reqMsg)	#断线重连
	
	@endPoint.result
	@lock4key.lockByEndPoint
	def rpcRobotLogin(self,ep,ctrlr,reqMsg):return rpcRobotLogin(self,ep,ctrlr,reqMsg)


def loadObj4roleLogin(iRoleId):#并发加载对象
	try:
		roleJob=myGreenlet.cGreenlet.spawn(role.gKeeper.getObjFromDB,factory.NO_ROW_INSERT_PRIME_KEY,iRoleId)
		resumeJob=myGreenlet.cGreenlet.spawn(resume.gKeeper.getObjFromDB,factory.NO_ROW_RETURN_NONE,iRoleId)
		mailBoxJob=myGreenlet.cGreenlet.spawn(mail.mailBoxKeeper.getObjFromDB,factory.NO_ROW_INSERT_PRIME_KEY,iRoleId)
		gevent.joinall([roleJob,resumeJob,mailBoxJob],None,True)
		who=roleJob.value
		oResume=resumeJob.value
		oMailBox=mailBoxJob.value
		return who,oResume,oMailBox
	except: #Exception		
		role.gKeeper.removeObj(iRoleId)		
		resume.gKeeper.removeObj(iRoleId)		
		mail.mailBoxKeeper.removeObj(iRoleId)
		raise
	

def rpcRoleLogin(self,oNewEp,oAccount,reqMsg):
	iRoleId=reqMsg.iValue
	roleLogin(oNewEp,oAccount,iRoleId)


def roleLogin(oNewEp,oAccount,iRoleId):
	if not(0<iRoleId<=c.MAX_ROLE_ID):
		oNewEp.rpcTips('角色id非法.id={}.'.format(iRoleId))
		return
	if not oAccount.hasRoleId(iRoleId):#检查角色id是不是属于这个账号之下的
		oNewEp.rpcTips('该角色不存在.')
		return
	sUserSource,sAccount=oAccount.userSourceAccount()
	#todo:检查角色是否被封停
	#with primitive.cLockByKey(dLock4roleLogin,iRoleId):
	#iPlayingRoleId=oAccount.playingRoleId()
	
	who=getRole(iRoleId)
	if who:
		bReLogin = getattr(who, "isLogined", False)
	else:
		bReLogin= False
	if who:
		oNewEp.setAssociativeRole(who)#角色关连channel
		who.cancelDestroyLater()#有可能角色掉线时被注册了延时移除,在这里要反注册	
	who,oResume,oMailBox=loadObj4roleLogin(iRoleId)
	if not bReLogin:
		for ctnObj in who.lLoginSetup:#容器物品setup
			ctnObj.callSetup4allItem()
	oAccount=account.get(sUserSource,sAccount)
	if not oAccount:
		return	
	oNewEp.setAssociativeRole(who)#角色关连channel		
	oAccount.setPlayingRoleId(iRoleId)	#设置账号的活跃角色
	if not bReLogin:#
		who.setUserSourceAccount(sUserSource,sAccount)
		# oAccount.setPlayingRoleId(iRoleId)	#设置账号的活跃角色
		oAccount.accountJson.set('actRoleId', iRoleId)	#存档账号的最近登录角色ID
		who.iLoginStamp=timeU.getStamp()
		db4ms.gConnectionPool.query(sql.UPDATE_ROLE_LOGINTINE, iRoleId)

	who.isClientInited = False # 客户端初始化标记
	who.reCalcAttr(False)#算属性
	oNewEp.rpcAvatarAttrInit(**role.roleHelper.makeAttrInitMsg(who))#发送角色基本属性
	del who.isClientInited
	role.login.beforeLogin(who,bReLogin)
	role.register.registerRoleToScene(who)#进入场景前先注册角色到场景服务器
	scene.m2ssCrateEntity(who, reg=False)
	scene.switchScene(who, who.sceneId, who.x, who.y)#进入场景
	
	if bReLogin:#上面把角色id关联到channel并切换完场景后,才可以调用onReLogin
		who.onReLogin()
	# else:#此步必须在rpcAvatarAttrInit之后,因为全局上线事件可能会引下发体力变化msg
	# 	role.geLogin(who)	#全局角色上线事件
	
	for oContainer in who.lLoginSend:
		oContainer.refresh()#发送物品列表,好友列表..到客户端

	if who.fetch("numenBag"):  #发送临时背包数据
		who.tempCtn.refresh()
		
	role.login.onLogin(who,bReLogin)
	who.isLogined=True
	role.register.registerRole(who) # 注册角色到其他服务器
	log.log('loginLogout','角色登录id={},name={}'.format(iRoleId,who.name))
	who.startTimer(functor(refreshByStep, who.id, 1), 1, "refreshByStep")
	
def refreshByStep(roleId, step):
	'''延迟发送数据
	'''
	who = getRole(roleId)
	if not who:
		return
	
	if step == 1:
		lineup.service.rpcLineupList(who)
		role.login.onNewbieAfterLogin(who)
		ride.isride(who)
	elif step == 2:
		mail.service.mailListAll(who)
	else:
		return
	
	who.startTimer(functor(refreshByStep, roleId, step + 1), 1, "refreshByStep")

def rpcDelRole(self,ep,oAccount,reqMsg):#删除角色很容易出问题.比如这个角色是公会会长职位是否应该先交出去.
	iServiceNo=1
	json=oAccount.accountJson  
	mf=oAccount.accountMf
	sUserSource,sAccount=oAccount.sUserSource,oAccount.sAccount
	iRoleId=reqMsg.iValue
	if not oAccount.hasRoleId(iRoleId):#检查角色id是不是属于这个账号之下的
		return False		
	#被删除的角色正在线上/内存中
	
	#todo 角色删了,排行榜要不要处理
	#todo 如果玩家在公会里要处理
	#todo 双向好友,删除角色时也要从好友的好友列表中删除ME	

	oAccount.updateRoleStatus(iRoleId)#更新账号角色列表
	ep.rpcRoleList(getRoleListMsg(oAccount))#下发角色列表
	log.log('role','account{},被删角色id{}'.format(oAccount.userSourceAccount(),iRoleId))	
	ep.rpcTips('删除成功')


	try:
		loginClientEp=clientLogin.getEndPoint(iServiceNo)	#从登录服内存中删角色信息	
		loginClientEp.rpcDeleteRole(config.ZONE_NO,sUserSource,sAccount,iRoleId)		
	except Exception:
		u.logException()
	try:	
		databaseLogin.gConnectionPool.query(databaseLogin.DELETE_ROLE,iRoleId)#从登录服数据库删角色信息
	except Exception:
		u.logException()
	return True

def loadAccountObj(sUserSource,sAccount):
	tNoRowInsertValues=sUserSource,sAccount,DIAMOND,VIP_LV,VIP_EXP
	oAccount=account.gKeeper.getObjFromDB(tNoRowInsertValues,sUserSource,sAccount)			
	if not oAccount:
		raise Exception,'加载账号{},{}出错'.format(sUserSource,sAccount)
	return oAccount

def rpcAccountLogin(self,oNewEp,ctrlr,reqMsg,isRobot=False):
	#todo:检查客户端版本号	
	#合区会使同一帐号下的玩家的角色数量不受控,越来越多,客户端要智能地显示n个角色中	
	msg=account_pb2.accountLoginResp()
	msg.bSuccessed=False
	sUserSource,sAccount=reqMsg.sUserSource,reqMsg.sAccount	
	if not sAccount.strip():
		oNewEp.rpcTips('账号名不能为空')
		return msg
	if not sUserSource and not sAccount:#不能同时为空
		return msg
	if u.isInvalidText(sUserSource) or u.isInvalidText(sAccount):
		oNewEp.rpcTips('账号名不能有非法字符')
		return msg

	oOldEp=mainService.getEndPointByUserSourceAccount(sUserSource,sAccount)
	# if oOldEp==oNewEp: #客户端创建角色界面返回后再登录会过滤掉，导致登录不了
	# 	return #估计是短时间内收到多个包,忽略后面的网络包.

	#iServiceNo=reqMsg.iServiceNo
	# loginClientEp=clientLogin.getEndPoint(iServiceNo)
	# if not loginClientEp:
	# 	oNewEp.rpcTips('登录失败,游戏服无法连接到{}号登录服'.format(iServiceNo))
	# 	return
	if not block.parameter.parameter.isOpenForPlayer():	#后台运营控制是否允许登录
		oNewEp.rpcTips('服务器停机维护,请稍候登录')
		return msg
	sLoginAppId=reqMsg.sLoginAppId #本次登录使用的客户端标识   临时屏蔽 
	sRegisterAppId=reqMsg.sRegisterAppId  #注册战法牧账号时使用的客户端标识,
	iOStype=reqMsg.iOStype #客户端操作系统类型(安卓,ios,winPhone)
	#sToken=reqMsg.sToken #令牌(用令牌向login服务器或认证服务器发起rpc,检查这个玩家是否合法.)
	#loginClientEp.rpcAuth(sUserSource,sAccount,sToken)
	oNewEp.setGranted()
	
#账号是否在本区被封停


	if block.parameter.parameter.isStaffOnly() and not config.IS_INNER_SERVER:#只有员工可登且是生产环境
		if not cfg.staff.isStaff(sUserSource,sAccount):
			oNewEp.rpcModalDialog('游戏正在维护中,请稍候登录.')#请具体提示什么时候会开服.
			return msg
	if config.IS_INNER_SERVER:
		oNewEp.rpcTips('请注意:这是内部体验服.')
	elif block.parameter.parameter.isStaffOnly() and cfg.staff.isStaff(sUserSource,sAccount):
		oNewEp.rpcModalDialog('仅内部员工可登录;服务区号:{};服务器id:{}'.format(config.ZONE_NO,config.ZONE_ID),'内部员工才会有的状态提示')

	#从内存中拿账号
	#with primitive.cLockByKey(dLock4accountLogin,(sUserSource,sAccount)):#资源锁，防止正在加载账号的过程中执行下面那步从内存中拿账号
	if not cfg.gm.group(sUserSource,sAccount) and account.gKeeper.amount()>=block.parameter.parameter.getMaxUserCount():#这里要改为检查channel数
		oNewEp.rpcTips('游戏登录人数太多,请稍候登录')#gm不受此限制
		return msg


	if oOldEp and oOldEp!=oNewEp:
		#oOldEp.rpcShutdown('')
		oOldEp.rpcReloginMsg('你的账号在别处登录.', 2)
		oOldEp.shutdown()
		#上面shutdown下面就报weakly-referenced object no longer exists
		#oOldEp.resetAssociativeAccount()
		#oOldEp.resetAssociativeRole()#不要让旧ep还继续关联角色

	oAccount=account.get(sUserSource,sAccount)
	bInMemory=(oAccount is not None)
	if bInMemory:#账号已在内存,顶下线			
		oAccount.onReLogin()
	else:
		oAccount=loadAccountObj(sUserSource,sAccount)
		oAccount.setRegisterAppId(sRegisterAppId)
	#这几个信息每次登录都可能发生变化
	oAccount.setLoginAppId(sLoginAppId)
	oAccount.setOStype(iOStype)
	oAccount.setIP(oNewEp.ip())
	if isRobot:
		oAccount.accountJson.set("robot", 1)

	#oOldEp=mainService.getEndPointByUserSourceAccount(sUserSource,sAccount)#要重新获取,上下文切换后原来的oOldEp no longer exist
	#if not oOldEp or oOldEp!=oNewEp:#首次登录条件一定成立,顶号也可能成立
	oNewEp.setAssociativeAccount(oAccount)#关联的channel 	
	
	#内存泄露 若账号有活跃角色,此处oNewEp未关联该角色,role找不到释放时机
	#导致角色一直在内存中,此处暂不做处理,临时由role.gInspectTimer来移除该role
	#上面的临时方案改为设置角色的延时剔除,并且重置账号的iActiveRoleId=0
	#因为不重置账号的iActiveRoleId,在角色被移除时,会移除相应的账号
	oRole=getRole(oAccount.playingRoleId())	#取得活跃角色
	if oRole:
		oRole.setDestroyLater()	#设置角色的延时剔除
	oAccount.setPlayingRoleId(0)	#重置账号的活跃角色
	log.log('loginLogout','({},{})账号登录'.format(sUserSource,sAccount))
	myGreenlet.cGreenlet.spawn(doRoleLoginAfterAccountLogin, sUserSource, sAccount, isRobot)

	msg.bSuccessed=True
	msg.timeStamp=int(time.time() * 1000)
	return msg

def doRoleLoginAfterAccountLogin(sUserSource, sAccount, isRobot):
	'''帐号登陆后直接进行角色登陆
	'''
	ep = mainService.getEndPointByUserSourceAccount(sUserSource, sAccount)
	if not ep:
		return
	oAccount=account.get(sUserSource,sAccount)
	if not oAccount:
		return
	if len(oAccount.lRoleList) >= 1:
		#已经有角色直接登录
		iRoleId = oAccount.lRoleList[0]
		roleLogin(ep, oAccount, iRoleId)
	else:
		if isRobot: # 机器人首次登录直接创建角色并登录
			createAndLoginRobot(ep, oAccount)
		else:
			ep.rpcRoleList(getRoleListMsg(oAccount))#下发角色列表

def getRoleListMsg(oAccount):
	roleList=account_pb2.roleList()
	iLatelyRoleId=oAccount.accountJson.fetch('actRoleId', 0)	#
	lRoleIds=oAccount.lRoleList
	for iRoleId in lRoleIds:
		info=oAccount.dRoleList[iRoleId]
		roleInfo=roleList.roles.add()
		roleInfo.iRoleId=iRoleId
		roleInfo.sRoleName=info.get('name',c.BORN_NAME)
		roleInfo.iRoleLevel=info.get('level',0)
		roleInfo.iRoleSchool=info.get("school",11)
	return roleList

def rpcSetRoleName(self,ep,who,reqMsg):
	if who.name!=c.BORN_NAME:
		return False
	sName=reqMsg.iValue
	sInvalid=u.isInvalidText(sName)
	if sInvalid:
		ep.rpcTips('您输入的{}为非法字符，请重新输入!'.format(sInvalid))
		return False
	sName=u.trim(sName) #过滤两端空白字符,包括全角空格\xa1(有bug,要用正则表达式来过滤)	
	if not sName:
		return False
	if len(unicode(sName,'utf-8'))>NAME_MAX_LEN:
		ep.rpcTips('角色昵称最长只能{}个字'.format(NAME_MAX_LEN))
		return False

	for sSymbol in ('#','^','\"','\''):#染色符号,表情符号不可以.单引号双引号最好也不让
		if sSymbol in sName:
			ep.rpcTips('角色名称不能含有{}'.format(sSymbol))
			return False
	#角色名称敏感字拦截		
	if False and sName!=trie.fliter(sName):
		ep.rpcTips('角色名称中含有敏感词,请重试!')
		return False
		
	for sSymbol in (' ','\x0a','\x0d'):#把各字符间的空格,回车换行去掉
		sName=sName.replace(sSymbol,'')

	if sName in randNameData.gsRoleName:
		ep.rpcTips('{}已经被占用,请另起一个名字.'.format(sName))
		return False
	randNameData.gsRoleName.add(sName)
	who.accountObj.addRoleName(who.id,sName)
	who.set("name",sName)
	who.attrChange("name")
	return True

def rpcCreateRole(ep,oAccount,reqMsg,loginFunc=None):
	iServiceNo=1 #临时方案	
		
	if oAccount.roleAmount()>=ROLE_MAX_AMOUNT:#硬上限(外层必须要有锁,否则可能角色数量会超出)
		ep.rpcTips('创建失败,角色数量不能超过{}个.'.format(ROLE_MAX_AMOUNT))
		return False
		
	iSchool,iShape=reqMsg.iSchool,reqMsg.iShape #职业,角色名字#造型
	if iSchool not in role.defines.schoolList:
		ep.rpcTips('本门派尚未开启')
		return False
	if iShape in role.defines.maleList:
		iGender = 1
	elif iShape in role.defines.femaleList:
		iGender = 2
	else:
		ep.rpcTips('所选造型不存在')
		return False
	if iShape/100 != iSchool:  #造型和职业不匹配，非法值
		return False

	iRoleId=GUId.gRoleId.nextId()#角色ID生成器
	sUserSource,sAccount=oAccount.userSourceAccount()
	oCenterEP = client4center.getCenterEndPoint()
	bFail,oMsg = oCenterEP.rpcGetName(iGender,iRoleId) #randNameData.getName(iRoleId,iGender)
	if bFail:
		log.log("createRoleError","账号:({},{})向中心服请求名字时失败".format(sUserSource,sAccount))
		return False
	sName = oMsg.sValue

	with lock4roleName:#查询角色名有没有被占用 和 插入数据库 必须是一个原子操作.
		oAccount=account.get(sUserSource,sAccount)#因为上面有锁,锁会发生上下文切换,局部变量需要重新获取
		if not oAccount:
			ep.rpcTips('创建角色失败,帐号未登录')
			return False
		
		tInsertValues=oAccount.sRegisterAppId,sUserSource,sAccount,iRoleId,sName,EXP,c.INIT_LV,iSchool,0,GOLD,0,0,0,VOUCHER		
		who=role.gKeeper.getObjFromDB(tInsertValues,iRoleId)#创建角色时也把整个对象在内存中hold住,很大概率玩家马上就登这个角色		
		who.set("name",sName)
		who.set("level",c.INIT_LV)
		who.set("school",iSchool)
		who.set("shape",iShape)
		who.set("shapeParts", role.defines.randShapeParts(iShape))
		if oAccount.isRobot():
			who.set("robot", 1)

		who.setDestroyLater()#设为延时移除,避免玩家不登录这个角色,这个对象就一直在内存中死不去
		oCenterEP.rpcConfirmName(iRoleId)

	resume.gKeeper.getObjFromDB(factory.NO_ROW_INSERT_PRIME_KEY,iRoleId)#创建基本角色摘要(名字、职业、等级)	
	offlineHandler.gKeeper.getObjFromDB(factory.NO_ROW_INSERT_PRIME_KEY,iRoleId)#创建离线玩家对象
		
	oAccount.addRoleInfo(iRoleId,sName,iSchool,c.INIT_LV,0,0,0,0,1)#角色创建后将其加入账号 0:初始升星特效
	notifyLoginServiceCreateRole(iServiceNo,sUserSource,sAccount,iRoleId)
	#oAccount.setPlayingRoleId(iRoleId)
	who.setUserSourceAccount(oAccount.sUserSource,oAccount.sAccount)
	
	who.reCalcAttr(False)	

	ep=mainService.getEndPointByUserSourceAccount(sUserSource,sAccount)
	ep.rpcTips('角色创建成功.')

	myGreenlet.cGreenlet.spawn(doLoginAfterCreate, loginFunc, sUserSource, sAccount, iRoleId)

	log.log("create","账号:({},{})创建角色:{},名字:{},职业:{},造型:{},IP:{}".format(sUserSource,sAccount,iRoleId,sName,iSchool,iShape,oAccount.sIP))
	return True

def doLoginAfterCreate(loginFunc, sUserSource, sAccount, iRoleId):
	'''创建后执行登陆
	'''
	ep = mainService.getEndPointByUserSourceAccount(sUserSource, sAccount)
	if not ep:
		return
	oAccount=account.get(sUserSource,sAccount)
	if not oAccount:
		return
	if loginFunc:
		loginFunc(ep, oAccount, iRoleId)
	else:
		roleLogin(ep, oAccount, iRoleId)

def notifyLoginServiceCreateRole(iServiceNo,sUserSource,sAccount,iRoleId):#通知通录服创建了一个角色
	return
	try:
		loginClientEp=clientLogin.getEndPoint(iServiceNo)		
		loginClientEp.rpcCreateRole(config.ZONE_NO,sUserSource,sAccount,iRoleId)
	except Exception:
		log.log('error','create role notify login server fail,sUserSource={},sAccount={},iRoleId={}'.format(sUserSource,sAccount,iRoleId))
		misc.logException()
	try:
		databaseLogin.gConnectionPool.query(databaseLogin.CREATE_ROLE,iRoleId,config.ZONE_NO,sUserSource,sAccount)#增加角色信息到登录服数据库
	except Exception:
		log.log('error','create role insert login server database fail,sUserSource={},sAccount={},iRoleId={}'.format(sUserSource,sAccount,iRoleId))
		misc.logException()	

def rpcRandomName(self,ep,oAccount,reqMsg):#随机名字
	i=0
	tPersonName=randNameData.tPersonName
	iLastNameLen=len(tPersonName)
	while i<200:
		i+=1
		sLastName=tPersonName[random.randint(0,iLastNameLen-1)]	#取得名字
		iLength = len(unicode(sLastName,'utf-8'))
		if iLength >= NAME_OUTFAM_LEN and sLastName not in gsRoleName:	#名字未被使用且长度>=NAME_OUTFAM_LEN
			ep.rpcSendName(sLastName)
			return;
		iLength=NAME_MAX_LEN-iLength	#最大姓长度
		if iLength<=0:#名字已达到最大长度,不需要在去筛选姓了
			continue
		lKeys=[x for x in randNameData.gdSurName.keys() if x <= iLength] 
		iKey=lKeys[random.randint(0,len(lKeys)-1)] 
		tSurname=randNameData.gdSurName.get(iKey);
		if tSurname:
			sFirstName=tSurname[random.randint(0,len(tSurname)-1)]	#取得姓
			sName=sLastName + sFirstName
			if sName not in gsRoleName and len(unicode(sName,'utf-8'))<=NAME_MAX_LEN:
				ep.rpcSendName(sName)
				return;
	ep.rpcSendName(sLastName)	#while失败返回sLastName

def rpcReconnect(self,oNewEp,ctrl,reqMsg):#断线重连	
	iRoleId=reqMsg.iValue
	#print 'rpcReconnect.. .' ,iRoleId
	oOldEp=mainService.getEndPointByRoleId(iRoleId)
	oRole=getRole(iRoleId)
	if not oRole:
		return False
	if oOldEp:#旧的ep还存在
		oOldEp.resetAssociativeRole()	#解除ep和角色的绑定关系
		oOldEp.resetAssociativeAccount()
		oOldEp.rpcReloginMsg('您的账号在别处登录了.', 2)
		oOldEp.shutdown()	# 
		#此处不主动从keeper移除oOldEp	
	print 'rpcReconnect newEp Id:', oNewEp.epId()	
	oNewEp.setAssociativeAccount(oRole.accountObj)
# 	oNewEp.setAssociativeRole(oRole)
	oNewEp.setGranted()
# 	oRole.cancelDestroyLater()#有可能角色掉线时被注册了延时移除,在这里要反注册
	#if getattr(oRole,'iDisConnectStamp', 0):
	#	oRole.onReLogin()	#触发重连事件
# 	roleLogin(oNewEp, oRole.accountObj, iRoleId)
	gevent.spawn(roleLoginForReconnect, oNewEp, iRoleId)
	return True

def roleLoginForReconnect(oNewEp, iRoleId):
	oRole=getRole(iRoleId)
	roleLogin(oNewEp, oRole.accountObj, iRoleId)

def rpcHandshake(self,newEp,reqMsg):#握手(暂时未想好,后期实现)
	iOldEpId=reqMsg.iOldEpId
	iNewEpId=newEp.epId()
	if iOldEpId==0:#是首次登录
		newEp.endPointId(iNewEpId)
		return

	#是重连动作
	oOldEp=mainService.gEndPointKeeper.getObj(iOldEpId)
	if not oOldEp:
		#重连得太晚了,对象都被清掉了
		#todo:告诉客户端退到登录界面去重新输入账号密码,重走整个流程
		return
	newEp.copy(oOldEp)#从旧channel对象中复制各种变量到新的channel对象中来.
	newEp.endPointId(iNewEpId)#新channel的id发给客户端
	

	#角色对象,账号对象都关联着channelId,也要相应地修改.
	obj=oOldEp.accountObj
	if obj:
		obj.setEndPointId(iNewEpId)

	obj=oOldEp.roleObj
	if obj:
		obj.setEndPointId(iNewEpId)

def rpcSwitchRole(self,ep,oAccount,reqMsg):#切换角色,退回到角色列表界面
	ep.resetAssociativeRole()
	#role.gKeeper.removeObj(oAccount.playingRoleId())
	#因为有一定概率再次切换回本角色,所以不从内存中移除角色
	iPlayingRoleId=oAccount.playingRoleId()
	# oAccount.setPlayingRoleId(0)
	oRole=getRole(iPlayingRoleId)	
	if oRole:
		oRole.setDestroyLater()#延迟踢出内存
	ep.rpcRoleList(getRoleListMsg(oAccount))#发送角色列表

def rpcAccountLogOut(self,ep,oAccount,reqMsg):#退出游戏(移除账号,移除角色)
	iRoleId=oAccount.playingRoleId()
	tUserSource=oAccount.userSourceAccount()
	if iRoleId:
		role.gKeeper.removeObj(iRoleId)
	account.gKeeper.removeObj(*tUserSource)
	log.log('loginLogout', 'rpcAccountLogOut')	#记录登出日志
	ep.shutdown()

def rpcForceRemoveRole(self,ep,who,reqMsg):#强制清理角色(测试机器人用)
	iRoleId=who.id
	if iRoleId:
		role.gKeeper.removeObj(iRoleId)
		ep.resetAssociativeRole()
	return iRoleId

def rpcRobotLogin(self, ep, ctrl, reqMsg):
	'''机器人登录
	'''
	if not config.IS_INNER_SERVER:
		return
	
	accountName = reqMsg.accountName
	reqMsg = account_pb2.accountLoginReq()
	reqMsg.sAccount = accountName
	reqMsg.sUserSource = "100"
	reqMsg.iOStype = 2 #android
	reqMsg.sLoginAppId = "aaaa"
	reqMsg.sRegisterAppId = "bbbb"
	reqMsg.sToken = ""
	rpcAccountLogin(self, ep, ctrl, reqMsg, isRobot=True)
	
def createAndLoginRobot(ep, oAccount):
	'''创建机器人角色并登录
	'''
	data = robotData.getRandAttrData()
	school = data["门派"]
	shapeList = data["造型"]
	shape = shapeList[rand(len(shapeList))]
	
	
	reqMsg = account_pb2.createRoleReq()
	reqMsg.iSchool = school
	reqMsg.iShape = shape
	rpcCreateRole(ep, oAccount, reqMsg, functor(robotFirstLogin, data))
		
def robotFirstLogin(ep, oAccount, roleId, data):
	'''机器人首次登录
	'''
	who = getRole(roleId)
	if not who:
		return
		
	sceneList = data["场景"]
	sceneId = sceneList[rand(len(sceneList))]
	x, y = scene.randSpace(sceneId)
	who.sceneId = sceneId
	who.x = x
	who.y = y
	
	roleLogin(ep, oAccount, roleId)
	
	levelList = data["等级"]
	level = levelList[rand(len(levelList))]
	level = level + rand(10)
	for i in xrange(level):
		who.exp += who.expNext
		who.upLevel()

import time

from common import *
import c
import factory
import factoryConcrete
import timeU
import trie
import scene_pb2
import scene
import sql
import db4ms
import gevent.lock
import GUId
import u
import log
import account
import block.parameter
import cfg.staff
import role
import mainService
import account_pb2
import clientLogin
import resume
import random
import randNameData
import mail
import mail.service
import lineup.service

import rank
import guild
import guild_pb2
import npcData
import productKeeper
import common_pb2
import cfg.gm
import role.roleHelper
import friend.svcFriend
import block.blockPackage
import databaseLogin
import team
import role.login
import myGreenlet
import config
import backEnd
import role.defines
import role.register
import client4center
import robotData
import offlineHandler
import ride
if 'gbOnce' not in globals():
	gbOnce=True
	if 'mainService' in SYS_ARGV:
		lock4roleName=gevent.lock.RLock()
		dLock4accountLogin={}
		dLock4roleLogin={}
