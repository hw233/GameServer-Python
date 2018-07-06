#-*-coding:utf-8-*-
'''其他指令
'''
#作者:马昭@曹县闫店楼镇

import instruction

@instruction.properties(sn='ra')
def rollAnnounce(ep,sContent='Announce'):
	'发布系统滚屏公告，参数：[文本内容]；短指令：ra'
	for iRoleId in role.gKeeper.getKeys():
		oChn=mainService.getEndPointByRoleId(iRoleId)
		oChn.rpcRollAnnounce(sContent)
		
def freboot(ep):
	'''强制重启
	'''
	for ep in mainService.gEndPointKeeper.getValues():
		ep.rpcReloginMsg("服务器已重启，请重新登录！", 1)

	shutServer.kickAllRole([ep])	#踢除不在忽略列表的角色,[ep]防止当前ep被kill,进而导致当前执行流也被kill
	shutServer.saveAllData()		#保存data
	shutServer.stopAllServer()		#通知所有的server
	os.system("sh run.sh")
	log.log("freboot", "success")

@instruction.properties(sn='rb')
def reboot(ep):#重启服务器(或许要用维护指令比较好)
	'重启服务器'


	ep.cancelPendingByRPCname('rpcSelectBox')
	bFail,uMsg=ep.rpcSelectBox('你是否要马上重启服务器??建议你在群里喊一声\'重启服务器\',如果2分钟内没人反对,才好正式重启\nQ否,我再想想\nQ是,立马重启')
	if bFail:
		print 'fail....',u.trans(uMsg.sReason)
		return
	print 'uMsg.iValue=='	,uMsg.iValue

@instruction.properties(sn='hu')
def hotUpdate(ep,sModpath):#热更新
	'热更新，参数：更新文件路径；短指令：hu'
	import hotUpdate #模块与指令同名了,放在这里可以解决
	if sModpath.endswith('.py'):
		ep.rpcTips('请去掉末尾的.py后缀')
		return
	hotUpdate.update(sModpath)
	ep.rpcTips('热更新{}成功.'.format(sModpath))
	ep.rpcMessage('热更新{}成功.'.format(sModpath))
	
@instruction.properties(sn='huall')
def hotUpdateAll(ep,sModpath):#热更新
	'''热更新全服
	'''
	import hotUpdate #模块与指令同名了,放在这里可以解决
	if sModpath.endswith('.py'):
		ep.rpcTips('请去掉末尾的.py后缀')
		return
	hotUpdate.update(sModpath)
# 	mainService.getSceneEP().rpcHotUpdate(sModpath)
	mainService.getChatEP().rpcHotUpdate(sModpath)
# 	mainService.getFightEP().rpcHotUpdate(sModpath)
	ep.rpcTips('热更新{}成功.'.format(sModpath))
	ep.rpcMessage('热更新{}成功.'.format(sModpath))

@instruction.properties(sn='huss')
def hotUpdateSceneService(ep,sModpath):#热更新
	'''热更场景服
	'''
	import hotUpdate #模块与指令同名了,放在这里可以解决
	if sModpath.endswith('.py'):
		ep.rpcTips('请去掉末尾的.py后缀')
		return
	import backEnd
	backEnd.gSceneEp4ms.rpcHotUpdate(sModpath)
	ep.rpcTips('场景服热更新{}成功.'.format(sModpath))
	ep.rpcMessage('场景服热更新{}成功.'.format(sModpath))

@instruction.properties(sn='hucs')
def hotUpdateCenterService(ep,sModpath):#热更新
	'''热更中心服
	'''
	import hotUpdate #模块与指令同名了,放在这里可以解决
	if sModpath.endswith('.py'):
		ep.rpcTips('请去掉末尾的.py后缀')
		return
	import client4center
	client4center.getCenterEndPoint().rpcHotUpdate2center(sModpath)
	ep.rpcTips('中心服热更新{}成功.'.format(sModpath))
	ep.rpcMessage('中心服热更新{}成功.'.format(sModpath))
	
@instruction.properties(sn='mt')	
def maintain(ep):#系统停机维护,这个操作是不可逆的.
	'服务器停机维护处理；短指令：mt'

	if config.IS_INNER_SERVER:#内部测试服，关服务前要让全部人同意才关
		lJobs=[]
		for ep in mainService.gEndPointKeeper.getValues():
			job=gevent.spawn(ep.rpcSelectBox,'系统马上停机维护了,元芳，你怎么看?\nQ好吧,我同意马上停机\nQ再等一等,让我测完再停机.')
			lJobs.append(job)
		gevent.joinall(lJobs)
		for job in lJobs:
			bFail,uMsg=job.value
			if not bFail and uMsg.iValue==2:#超时不投票当同意，同意的更加是同意的
				ep.rpcTips('有人不同意马上停机')
				return

	shutServer.broadcastShutGSMsg()	#广播停服命令给所有角色
	shutServer.kickAllRole([ep])	#踢除不在忽略列表的角色,[ep]防止当前ep被kill,进而导致当前执行流也被kill
	shutServer.saveAllData()		#保存data
	shutServer.stopAllServer()		#通知所有的server
	
	ep.shutdown()#kill掉当前ep
	# misc.gbMaintain=True
	# oMsg=common_pb2.bytes_()
	# oMsg.sValue='游戏即将停机维护!请稍候登录,感谢广大玩家拥护.'
	# role.roleHelper.worldBroadcast('rpcTips',oMsg)
	# role.roleHelper.worldBroadcast('rpcSysPrompt',oMsg)
	
	# for oSingleton in block.singleton.glSingleton:#存盘各个singleton对象(各种排行榜,物品交易所,钻石交易所)
	# 	oSingleton._saveToDB()

	# #对factory.storageScheduler的func全部呼叫一次????????

	# #断开全部连接
	# lJob=[]
	# for iEndPointId,oChn in tuple(mainService.gEndPointKeeper.getIterItems()):
	# 	if iEndPointId!=ep.epId():#跳过自己,防止当前ep被kill,进而导致当前执行流也被kill
	# 		job=gevent.spawn(u.cFunctor(oChn.shutdown),5)
	# 		lJob.append(job)

	# gevent.joinall(lJob,None,True)
	# #把玩家,帐号,公会,邮箱,角色简要,房屋,仓库,物品店,宠物店
	# #等等实例踢出内存,会自动保存	
	# for oKeeper in productKeeper.glProductKeeper:
	# 	if oKeeper==account.gKeeper:#账号keeper最后再清理,因为remove角色时要访问账号对象(有依赖关系)
	# 		continue
	# 	oKeeper.removeAllObj()

	# account.gKeeper.removeAllObj()

	# for oServer in init.glServers:#各个服务不再监听端口
	# 	oServer.stop()
	# ep.shutdown()#kill掉当前ep

#修改在线人数上限.可以登录的vip上限
#踢某个玩家下线,踢除全部玩家下线

@instruction.properties(sn='kick')
def kickRole(ep,iRoleId):#踢角色下线
	oBeKickChn=mainService.getEndPointByRoleId(iRoleId)
	if not oBeKickChn:
		ep.rpcTips('{}不在线'.format(iRoleId))
		return 0
	oBeKickChn.rpcTips('您被系统请离了.')
	oBeKickChn.shutdown()
	ep.rpcTips('踢人下线成功')
	return 1
	
@instruction.properties(sn='fkick')
def forceKickRole(ep,iRoleId):#踢角色下线
	if kickRole(ep, iRoleId):
		role.removeRole(iRoleId)

def grant(ep,iRoleId,iGroup):#把某角色临时加入到gm权限组,下线即退出权限组
	'给角色临时gm权限，参数：角色id，权限组'
	if not ep.group()&instruction.ADMIN:#授权者本身不是管理员权限
		ep.rpcTips('你不是管理员,不能授权给别人.')
		return
	oOtherChn=mainService.getEndPointByRoleId(iRoleId)
	if not oOtherChn:
		ep.rpcTips('目标玩家不在线')
		return
	oOtherChn.iTempGroup=iGroup
	ep.rpcTips('授权成功')
	oOtherChn.rpcTips('你临时加入了{}组'.format(iGroup))

#'http://www.visualsvn.com/files/VisualSVN-Server-2.7.4.msi'
def downloadHttpFile(ep,sURL,sLocalPath):#磁盘文件不会阻塞(用了fileobject),网络io也不会阻塞(socket打了patch)
	'下载文件，参数：目标url，本地路径'
	oDiskFile=open(sLocalPath,'wb')
	#oDiskFile=gevent.fileobject.FileObject(oDiskFile)
	iSize=0
	while iSize<1024*1024*1024:
		s='AFASDF'*1100
		iSize+=len(s)			
		oDiskFile.write(s)
		
	oDiskFile.close()	
	ep.rpcTips('下载完成.')
	# oNetFile=urllib2.urlopen(sURL)
	# oDiskFile=open(sLocalPath,'wb')
	# oDiskFile=gevent.fileobject.FileObject(oDiskFile)
	# while True:
	# 	sBuff=oNetFile.read(100*1024)
	# 	if not sBuff:
	# 		oNetFile.close()
	# 		oDiskFile.close()
	# 		break
	# 	oDiskFile.write(sBuff)
	# ep.rpcTips('下载完成.')

#连接FTP下载文件，sRemotePath为从登陆后目录为起点(FTP代码目录)，sLocalDir为本机代码目录(文件直接拷贝替换至相应子目录)
def downloadFtpFile(ep,sRemotePath,bHotUpdate=False):
	'从FTP服务器下载文件，参数：目标文件url(默认为登录目录，目录分隔符使用"/")，本地路径(服务端代码目录)'
	try:
		sLocalDir=os.getcwd()
		f=MYFTP(FTP_HOSTADDR)
	except Exception:
		ep.rpcTips('FTP错误: 连接FTP服务器{}失败'.format(FTP_HOSTADDR))
		return
	try:
		f.login()
	except Exception:
		ep.rpcTips('FTP错误：登录FTP服务器{}失败'.format(FTP_HOSTADDR))
		f.quit()
		return
	iRemoteFileIdx=sRemotePath.rfind('/')
	sRemoteFile=sRemotePath[iRemoteFileIdx+1:]
	try:
		f.cwd(sRemotePath[:iRemoteFileIdx])	#切换到目标文件目录
	except Exception:
		ep.rpcTips('FTP错误：切换至目录{}失败'.format(sRemotePath[:iRemoteFileIdx]))
		f.quit()
		return
	if not sLocalDir.endswith('/'):
		sLocalDir=sLocalDir+'/'
	sLocalPath=sLocalDir+sRemotePath
	iLocalFileIdx=sLocalPath.rfind('/')
	sDirs=sLocalPath[:iLocalFileIdx+1]
	if not os.path.isdir(sDirs):
		os.makedirs(sDirs)
	if os.path.isfile(sLocalPath):	#若文件已存在,则将其备份,备份名：原名+年-月-日-小时-分-秒+.bak
		timenow=time.localtime()  
		datenow=time.strftime('%Y-%m-%d-%H-%M-%S',timenow)
		sExt=sRemoteFile[sRemoteFile.rfind('.'):]
		sBackUpName=''.join([sDirs,sRemoteFile[:-len(sExt)],'.',datenow,'.bak'])
		try:
			os.rename(sLocalPath,sBackUpName)
		except Exception:
			ep.rpcTips('文件正在使用中,备份失败')
			return
	try:
		oDiskFile=open(sLocalPath,'wb')
		oDiskFile=gevent.fileobject.FileObject(oDiskFile)
		f.retrbinary('RETR %s' % sRemoteFile,oDiskFile.write)	#开始下载目标文件
	except Exception:
		ep.rpcTips('FTP错误：下载目标文件{}失败'.format(sRemoteFile))
		f.quit()
		return
	ep.rpcTips('下载完成')
	f.quit()
	if bHotUpdate:
		iIdx=sRemotePath.rfind('.')
		sRemotePath=sRemotePath[:iIdx]
		if sRemotePath.endswith('__init__'):
			sRemotePath=sRemotePath[:-8]
		lTemp=[]
		for iIdx,sChar in enumerate(sModpath):
			if sChar in ('\\','/'):
				lTemp.append(iIdx)
		for iIdx in lTemp:
			sModpath[iIdx]='.'
		iIdx=sModpath.find('.')
		sModpath="'"+sModpath[iIdx+1:]+"'"
		hotUpdate.update(sModpath)

def varName(ep):#列举角色类的属性变量名(不包括函数名),列出来的都是可以用set指令改变的
	'列举角色属性的变量名'
	for sVarName,t in role.roleHelper.gdAttrInfo.iteritems():
		iFrom=t[0]
		if iFrom!=role.roleHelper.FUNC:#函数就不列出来了
			ep.rpcSysTips('{}'.format(sVarName))

import mainService
import timerEvent
import timeU
#查看ep状态
def inspectChn(ep):
	iMinuteNo=timeU.getMinuteNo()
	dChnIdMapRole={}
	log.log('inspect_channel', '\n\n当前在线人数{}.{}'.format(len(role.gKeeper.dObjs), role.gKeeper.dObjs.keys()))
	for oRole in role.gKeeper.dObjs.values():
		ep=mainService.getEndPointByRoleId(oRole.id)
		if ep:
			dChnIdMapRole[ep.epId()]=oRole.id
	log.log('inspect_channel','当前ep数{}'.format(len(mainService.gEndPointKeeper.dObjs)))
	for ep in mainService.gEndPointKeeper.dObjs.values():
		iRoleId=dChnIdMapRole.get(ep.epId(), 0)
		if hasattr(ep, 'iLastRequest'):
			log.log('inspect_channel', 'id:{},最后一次请求分钟在{}前,iRoleId:{}'.format(ep.epId(), iMinuteNo-getattr(ep,'iLastRequest',iMinuteNo),iRoleId))
		else:
			log.log('inspect_channel', 'id:{},iRoleId:{}'.format(ep.epId(),iRoleId))

def sysMail(ep, roleId, title, content, propsList="", validTime=0):
	'''发送系统邮件
	'''
	propsObjList = []
	propsList = str(propsList)
	if re.match("^\d+:\d+(,\d+:\d+)*$", propsList):
		propsList = eval("{" + propsList + "}")
		for propsNo, amount in propsList.items():
			propsObj = props.new(propsNo)
			if propsObj.isVirtual():
				propsObj.setValue(amount)
			else:
				propsObj.setStack(amount)
			propsObjList.append(propsObj)
	
	mail.sendSysMail(roleId, title, content, propsObjList, validTime)		
	
def tradeMail(ep, roleId, title, content, propsList="", validTime=0):
	'''发送交易邮件
	'''
	propsObjList = []
	propsList = str(propsList)
	if re.match("^\d+:\d+(,\d+:\d+)*$", propsList):
		propsList = eval("{" + propsList + "}")
		for propsNo, amount in propsList.items():
			propsObj = props.new(propsNo)
			propsObj.setStack(amount)
			propsObjList.append(propsObj)
	
	mail.sendTradeMail(roleId, title, content, propsObjList, validTime)
	
def guildMail(ep, roleId, title, content, propsList="", validTime=0):
	'''发送仙盟邮件
	'''
	propsObjList = []
	propsList = str(propsList)
	if re.match("^\d+:\d+(,\d+:\d+)*$", propsList):
		propsList = eval("{" + propsList + "}")
		for propsNo, amount in propsList.items():
			propsObj = props.new(propsNo)
			propsObj.setStack(amount)
			propsObjList.append(propsObj)
	
	mail.sendGuildMail(roleId, title, content, propsObjList, validTime)
	

@instruction.properties(gr=instruction.NOBODY,sn='am')
def accountMessage(ep,sPwd):
	'显示账户信息，参数：账户密码'
	if sPwd!='zmkm':
		return
	obj=ep.accountObj
	if obj:
		ep.rpcModalDialog('用户来源:{},账号:{}'.format(*obj.userSourceAccount()))


@instruction.properties(sn='owb')
def openWorldBoss(ep,iHour,iMinu,iPrMinu):
	import worldBoss
	worldBoss.OPEN_HOUR=iHour
	worldBoss.OPEN_MINU=iMinu
	worldBoss.PRE_MINU=iPrMinu
	ep.rpcTips('修改成功')
		
def findSceneNo(who,sKeyword=''):
	'查找场景，参数：[场景名]'
	for iNo,info in sceneData.gdData.iteritems():
		if iNo>=100:#临时场景不显示
			continue
		if (not sKeyword) or (sKeyword in info['name']):
			notify.G2CMessage(who.id,'%d->%s'%(iNo,info['name']))

@instruction.properties(sn='ud')
def update(ep):
	'从svn更新文件'
	if not config.IS_INNER_SERVER:
		ep.rpcTips('生产环境不可以从svn进行update')
		return
	ep.rpcTips('正在update文件,请稍等')
	try:
		if platform.system().upper()=='WINDOWS':			
			ep.rpcTips('在私服上跳过update')#os.system('call update.bat')
			return		
		os.system('sh update.sh')
		f=file('update.result','r')
		lLine=f.read().split('\n')
		f.close()
		for sText in lLine:
			if not sText:
				continue
			m = re.match("^.*\.\w+$", sText)
			if not m:
				continue
			ep.rpcMessage(sText)
			ep.rpcTips(sText)
	except BaseException,e:
		u.reRaise('从svn服务器update数据到游戏服务器时发生异常.')

@instruction.properties(sn='cm')
def commit(ep):
	'向svn提交文件'
	if not config.IS_INNER_SERVER:
		ep.rpcTips('生产环境不可以commit')
		return
	ep.rpcTips('正在commit文件,请稍等')
	if platform.system().upper()=='WINDOWS':
		ep.rpcTips('在私服上,跳过Commit')#os.system('call commit.bat')
		return

	try:
		os.system('sh commit.sh')
		f=file('commit.result', 'r')
		lLine=f.read().split('\n')
		f.close()
	except BaseException,e:
		u.reRaise('数据commit至svn时发生异常.')
		
	for sText in lLine:
		if not sText:
			continue
		ep.rpcTips(sText)
	else:
		ep.rpcTips('commit成功.')

@instruction.properties(sn='ma')
def makeAll(ep):#生成全部策划数据
	'生成全部策划数据'
	if not config.IS_INNER_SERVER:
		ep.rpcTips('生产环境不可以makeAll')
		return
	update(ep)
	try:
		for func in makeData.getAllMethod():
			func(ep)
	except BaseException,e:
		sName=func.func_doc if func.func_doc else '\"未起名数据表\"'
		u.reRaise('生成{}异常,指令名是{}.'.format(sName,func.func_name))
	else:
		commit(ep)


FTP_HOSTADDR=('192.168.1.195',13157)

import ftplib

class MYFTP(ftplib.FTP):

	def connect(self, host='', port=0, timeout=-999):
		if host != '':
			self.host,self.port = host
		if timeout != -999:
			self.timeout = timeout
		self.sock = gevent.socket.create_connection((self.host, self.port), self.timeout)
		self.af = self.sock.family
		self.file = self.sock.makefile('rb')
		self.welcome = self.getresp()
		return self.welcome

def msg(ep, pid, content):
	'''信息提示
	'''
	message.message(pid, str(content))
	
def schoolmsg(ep, schoolId, content):
	'''门派传闻
	'''
	message.schoolMessage(schoolId, str(content))
	
def teammsg(ep, teamId, content):
	'''队伍传闻
	'''
	message.teamMessage(teamId, str(content))
	
def guildmsg(ep, guildId, content):
	'''仙盟传闻
	'''
	message.guildMessage(guildId, str(content))

def sysann(ep, content):
	'''系统公告
	'''
	message.sysAnnounce(str(content))
	
def sysmsg(ep, content):
	'''系统传闻
	'''
	message.sysMessage(str(content))
	
def sysannroll(ep, content):
	'''系统公告且滚动
	'''
	message.sysAnnounceRoll(str(content))
	
def sysmsgroll(ep, content):
	'''系统传闻且滚动
	'''
	message.sysMessageRoll(str(content))
	
def sysroleroll(ep, content):
	'''玩家公告
	'''
	message.sysRoleRoll(ep.roleId(), str(content))
	
def worldmsg(ep, content):
	'''世界传闻
	'''
	message.worldMessage(str(content))
	
def worldrolemsg(ep, content):
	'''玩家世界传闻
	'''
	message.worldRoleMessage(ep.roleId(), str(content))
	
def bian(ep, shapeId, *shapeParts):
	who = getRole(ep.iRoleId)
	if not who:
		return
	if not isinstance(shapeId, int):
		ep.rpcTips("造型只能为整数")
		return
	for p in shapeParts:
		if not isinstance(p, int):
			ep.rpcTips("套装只能为整数")
			return
		
	if not shapeParts:
		shapeParts = who.shapeParts
	else:
		oldShapeParts = who.shapeParts
		oldCount = len(oldShapeParts)
		shapeParts = list(shapeParts)
		newCount = len(shapeParts)
		
		if newCount < oldCount:
			shapeParts.extend(oldShapeParts[newCount:])
		elif newCount > oldCount:
			shapeParts = shapeParts[:oldCount]
	
	who.shapeTmp = shapeId
	who.shapePartsTmp = {i:v for i, v in enumerate(shapeParts)}
	who.attrChange("shape", "shapeParts")
	ep.rpcTips("变身成功")

def setcolor(ep, *colorList):
	'''设置人物部位颜色
	'''
	who = getRole(ep.iRoleId)
	if not who:
		return
	who.setColors({i:color for i, color in enumerate(colorList)})

def setpart(ep, iPart, iScheme):
	'''设置人物部位方案
	'''
	who = getRole(ep.iRoleId)
	if not who:
		return
	who.setShapeParts(iPart, iScheme)

def startRobot(ep, count=0):
	'''启动机器人
	'''
	if not isinstance(count, int):
		ep.rpcTips("机器人数量必须是整数")
		return
	
	log.log("robot", "start robot %d" % count)
	os.system("sh startRobot.sh %s" % count)
	ep.rpcTips("启动机器人成功")
	
def stopRobot(ep):
	'''关闭机器人
	'''
	log.log("robot", "stop robot")
	for who in role.gKeeper.getValues():
		if not who.isRobot():
			continue
# 		who.endPoint.shutdown()
		role.removeRole(who.id)
	os.system("sh stopRobot.sh")
	ep.rpcTips("关闭机器人成功")
	
def calRobot(ep):
	'''统计机器人
	'''
	robotList = {}
	for who in role.gKeeper.getValues():
		if not who.isRobot():
			continue
		sceneId = who.sceneId
		if sceneId not in robotList:
			robotList[sceneId] = 0
		robotList[sceneId] += 1
	
	if robotList:
		txt = "\n".join(["场景:%d  人数:%d" % (sceneId, count) for sceneId, count in robotList.items()])
		txt += "\n总计:%d" % sum(robotList.values())
		ep.rpcTips(txt)
	else:
		ep.rpcTips("没有机器人")
		
def reloadMapData(ep):
	update(ep)
	scene.mapdata.loadMapData()
	ep.rpcTips("重新加载地图数据成功")

def ocsearch(ep):
	who = getRole(ep.iRoleId)
	if not who:
		return
	import collect.service4terminal
	import collect_pb2
	msg = collect_pb2.location()
	msg.fPosX = str(113.40188782209007)
	msg.fPosY = str(23.124088332887687)
	collect.service4terminal.rpcCollectSearch(who, msg)
	# collect.service4terminal.rpcCollectAround(who, msg)

def oclocation(ep, x, y):
	who = getRole(ep.iRoleId)
	if not who:
		return
	import collect.service4terminal
	import collect_pb2
	msg = collect_pb2.location()
	msg.fPosX = str(x)
	msg.fPosY = str(y)
	collect.service4terminal.rpcCollectUpdateLocation(who, msg)
	message.tips(who,"设置坐标为(%s,%s)" % (msg.fPosX,msg.fPosY))
	
def ocmarker(ep, iEventId):
	who = getRole(ep.iRoleId)
	if not who:
		return
	import collect.service4terminal
	import collect_pb2
	msg = collect_pb2.markerInfo()
	msg.iEventId = iEventId
	collect.service4terminal.rpcCollectMarker(who, msg)

def ocdel(ep, iEventId, iEventType):
	who = getRole(ep.iRoleId)
	if not who:
		return
	import collect.service4terminal
	import collect_pb2
	msg = collect_pb2.delEventInfo()
	msg.iEventId = iEventId
	msg.iEventType = iEventType
	collect.service4terminal.rpcCollectDelEvent(who, msg)

def ocfight(ep, iEventId):
	'''收集玩法战斗
	'''
	who = getRole(ep.iRoleId)
	if not who:
		return

	import collect.service4terminal
	import collect_pb2
	msg = collect_pb2.triggerEvent()
	msg.fPosX = str(113.40188782209007)
	msg.fPosY = str(23.124088332887687)
	msg.iEventId = int(iEventId)
	
	collect.service4terminal.rpcCollectFight(who, msg)

@instruction.properties(sn='ocne')
def ocNewOwnEvent(ep, iEventCnt=1, iAngle=45, iDistance=50):
	'''收集玩法：指定事件数量、角度、距离
	'''
	who = getRole(ep.iRoleId)
	if not who:
		return
	import client4center
	oCenterEP = client4center.getCenterEndPoint()
	msg = {}
	msg["iType"] = 1
	msg["iRoleId"] = who.id
	msg["iEventCnt"] = iEventCnt
	msg["iAngle"] = iAngle
	msg["iDistance"] = iDistance
	oCenterEP.rpcMainCollectTest(**msg)
	ep.rpcTips("生成指定事件成功")

def ocenter(ep, iEnter):
	who = getRole(ep.iRoleId)
	if not who:
		return
	# setattr(who, "enterCollect", iEnter)
	sStr = "进入" if iEnter else "退出"
	ep.rpcTips("设置{}收集玩法成功".format(sStr))
	# print getattr(who, "enterCollect", 0)
	reqMsg = common_pb2.int32_()
	reqMsg.iValue = 1 if iEnter else 0
	import collect.service4terminal
	collect.service4terminal.rpcCollectEnter(who, reqMsg)
	

@instruction.properties(sn='occe')
def ocClearEvent(ep):
	'''收集玩法：指定事件数量、角度、距离
	'''
	who = getRole(ep.iRoleId)
	if not who:
		return
	import client4center
	oCenterEP = client4center.getCenterEndPoint()
	msg = {}
	msg["iType"] = 2
	msg["iRoleId"] = who.id
	oCenterEP.rpcMainCollectTest(**msg)
	ep.rpcTips("清除指定事件成功")

@instruction.properties(sn='clr')
def ClearRank(ep, uRankNo):
	'''清空排行榜
	'''
	if uRankNo == "All":
		for iRankNo,rankObj in rank.gdRankObj.iteritems():
			rankObj.clearRank()
		ep.rpcTips("清空所有排行榜成功")
	else:
		rankObj = rank.getRankObjBySubNo(uRankNo)
		if not rankObj:
			ep.rpcTips("排行榜不存在")
			return
		rankObj.clearRank()
		ep.rpcTips("清空排行榜成功")

@instruction.properties(sn='rrs')
def RankResort(ep, uRankNo):
	'''排行榜重新排序
	'''
	if uRankNo == "All":
		for iRankNo,rankObj in rank.gdRankObj.iteritems():
			rankObj.instructResort()
		ep.rpcTips("重置所有排行榜成功")
	else:
		rankObj = rank.getRankObjBySubNo(uRankNo)
		if not rankObj:
			ep.rpcTips("排行榜不存在")
			return
		rankObj.instructResort()
		ep.rpcTips("重置排行榜成功")

@instruction.properties(sn='si')
def signIn(ep, content):
	who = getRole(ep.iRoleId)
	if not who:
		return
	import signIn
	signIn.signInInstruction(ep, who, content)

#playEttEffect(who, effectNo, ettId)'''播放实体特效	ok
@instruction.properties(sn='spee')
def showPlayEttEffect(ep,effectNo=None):
	if not effectNo:
		ep.rpcTips("请输入特效id")
		return
	who=getRole(ep.iRoleId)
	scene.playEttEffect(who, effectNo, who.id)

#playSceneEffect(who, effectNo, sceneId, x=0, y=0)播放场景特效
@instruction.properties(sn='spse')
def showPlaySceneEffect(ep,effectNo=None, x=0, y=0):
	who=getRole(ep.iRoleId)
	if not effectNo:
		ep.rpcTips("请输入特效id")
		return
	who=getRole(ep.iRoleId)
	scene.playSceneEffect(who, effectNo, who.id, x, y)

#broadcastEttEffect(effectNo, ettId):广播播放实体特效 ok
@instruction.properties(sn='sbee')
def showBroadcastEttEffect(ep, effectNo=None, ettId=None):
	if not effectNo:
		ep.rpcTips("请输入特效id")
		return
	elif not ettId:
		ep.rpcTips("请输入播放特效的实体id")
		return
	print("751---",effectNo, ettId)
	scene.broadcastEttEffect(effectNo, ettId)

#broadcastSceneEffect(effectNo, sceneId, x, y):广播播放场景特效
@instruction.properties(sn='sbse')
def showBroadcastSceneEffect(ep, effectNo=None, sceneId=None, x=0, y=0):
	if not effectNo:
		ep.rpcTips("请输入特效id")
		return
	elif not sceneId:
		ep.rpcTips("请输入播放特效的场景id")
		return
	scene.broadcastSceneEffect(effectNo, sceneId, x, y)

def answer(ep, content, *args):
	who = getRole(ep.iRoleId)
	if not who:
		return
	import answer
	answer.testInstruction(ep, who, content, *args)

@instruction.properties(sn='expt')
def tougheningExpTest(ep, content, *args):
	who = getRole(ep.iRoleId)
	if not who:
		return
	import tougheningExp
	tougheningExp.testInstruction(ep, who, content, *args)
	
def printtask(ep):
	who=getRole(ep.iRoleId)
	txtList = []
	for taskObj in who.taskCtn.getAllValues():
		txtList.append("{},{},{}".format (taskObj.id, taskObj.parentId,taskObj.title))
	ep.rpcModalDialog("\n".join(txtList))

def newride(ep, shape, star=1):
	target = getRole(ep.iRoleId)
	'获得一个坐骑，参数：坐骑编号'
	rideObj = ride.new(shape)
	if ride.addRide(target, rideObj,star):
		ep.rpcTips("得到了一个%s" % rideObj.name)


def addride(ep):
	who=getRole(ep.iRoleId)
	import rideData
	for rideObj in who.rideCtn.getAllValues():
		print rideObj.state
		if rideObj.idx == 6001 and rideObj.state==2:
			nextRide = rideData.getData(rideObj.idx,"下一只坐骑")
			who.stopTimer("rideHatchComplete")
			rideObj.rideHatchComplete(nextRide)
			message.tips(who, "祭炼成功")
			return
	message.tips(who, "该指令只能孵化第一只坐骑")

def showride(ep):
	'''显示身上所有宠物
	'''
	target = getRole(ep.iRoleId)
	if target.rideCtn.itemCount() <= 0:
		ep.rpcTips("身上没有任何坐骑")
		return
	
	txtList = []
	for rideObj in target.rideCtn.getAllValues():
		txtList.append("%d %s/状态:%s 编号:%d" % (rideObj.id, rideObj.name, rideObj.state, rideObj.idx))
	ep.rpcModalDialog("\n".join(txtList))

def clearride(ep, rideId=0):
	'''清除坐骑
	rideId: 默认为0，表示清除所有坐骑
	'''
	target = getRole(ep.iRoleId)
	if rideId:
		rideObj = target.rideCtn.getItem(rideId)
		if not rideObj:
			ep.rpcTips("找不到此坐骑")
			return
		target.rideCtn.removeItem(rideObj)
	else:
		target.rideCtn.clearAll()
	ep.rpcTips("OK")

def setguide(ep, guideNo):
	who = getRole(ep.iRoleId)
	if not who:
		return
	import guide.service
	guide.service.changeGuideNo(who, int(guideNo))


from common import *
import os
import platform
import gevent
import gevent.fileobject
import urllib2
import gevent.socket
import time
import shutServer
import timeU
import u
import log
import c
import misc
import npc
import scene
import makeData
import mainService
import role
import role.roleHelper
import account
import common_pb2
import props_pb2
import productKeeper
import factory
import mail
import types
import rank

import block.singleton
import init
import config
import message
import scene.mapdata
import props
import re
import ride