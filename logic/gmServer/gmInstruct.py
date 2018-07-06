#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

#根据xx的要求
#用户的身份验证由'客户端'进行
#此处只检查的执行权限是根据IP地址来判断的

######################     查询        #############################

dRoleTypeToSql={	#查询类型:查询语句
	# 'a':'select roleId, name, lv from role_multi_field1{}',
	'i':'select roleId, name, lv, exp, gold, status, userSource, account, pro, createTime, loginTime, logoutTime from role_multi_field1 where roleId={}',
	'n':'select roleId, name, lv, exp, gold, status, userSource, account, pro, createTime, loginTime, logoutTime from role_multi_field1 where name like \'{}%\'',
	'l':'select roleId, name, lv, exp, gold, status, userSource, account, pro, createTime, loginTime, logoutTime from role_multi_field1 where lv={}'	
}

def quaryOnlineRole(**dParam):	#查询10个随机在线玩家

	lKeys = list(role.gKeeper.getKeys())
	print u.trans2gbk('查询十个玩家的请求到了'),len(lKeys)
	iChoiceCount,iRange=0,len(lKeys)-1 	#iChoiceCount选择个数,最大选择10个
	lQueryRes=[]
	lChoiceKeys=random.sample(lKeys, min(len(lKeys), 10))
	for tRoleID in lChoiceKeys:	
		oRole=role.gKeeper.getObj(*tRoleID)
		if oRole:
			iChoiceCount+=1
			lQueryRes.append({"roleId":tRoleID[0], "roleName":oRole.name, "roleLev":oRole.level, "exp":oRole.exp(), "dia":oRole.diamond, "gold":oRole.gold, "rest":oRole.rest()})	
		iRange-=1
		if iRange < 0 or iChoiceCount >= 10:
			break
	lQueryRes.insert(0, {'state':True})
	return json.dumps(lQueryRes)

def quaryRoleInfo(**dQueryParam):	#c查看指定角色的信息,此处可能存在实时性的问题
			
	print u.trans2gbk('查询玩家的请求到了')						#考虑数据库查完,在检查下角色是否在线,再直接拉取role上的数据
	if True:
		#dQueryParam['type']表示查询类型 
		#a:随机查询10个在线的角色, i表示查看指定id的角色,n表示查看指定名字的角色,l表示查看指定等级的角色

		sType=dQueryParam.get('type', '')
		#参数检查暂时不做,若有参数错误直接将错误信息返回查询方
		if sType=='a':	#查询在线的玩家随机取10个
			sRes = quaryOnlineRole(**dQueryParam)
			print u.trans2gbk('查询玩家的请求到了1.1')	
			return sRes
		print u.trans2gbk('查询玩家的请求到了1.2')	
		sParam=dQueryParam.get('d','')
		sSql=dRoleTypeToSql[sType].format(sParam.encode('utf-8'))
		# print sSql
		lQueryRes=[]
		print u.trans2gbk('查询玩家的请求到了1.3')	
		rs=db4ms.gConnectionPool.query(sSql).rows	#rs:[(roleId, name, lv)]
		print u.trans2gbk('查询玩家的请求到了1.4')	
		for (iRoleId, sName, iLv, iExp, iGold, iStatus, sUserSource, sAccount, iSchool, sCreateAt,sLoginAt, sLoginOutAt) in rs:
			# if iStatus==-1:
			# 	continue
			print u.trans2gbk('查询玩家的请求到了2')	
			crt=sCreateAt.strftime('%Y-%m-%d %H:%M:%S')
			lg =''
			lgo =''

			if sLoginOutAt:
				lg=sLoginOutAt.strftime('%Y-%m-%d %H:%M:%S')
			lgo=sLoginAt.strftime('%Y-%m-%d %H:%M:%S')
			state=''
			if iStatus==0:
				state="正常"
			elif iStatus== -1:
				state="已删除"
			else:
				state="其他"

			dProId2Name={1:'战士',2:'弓箭手',3:'法师',4:'刺客'}
			print u.trans2gbk('查询玩家的请求到了3')	
			dRes={"roleId":iRoleId, "roleName":sName, "roleLev":iLv, "exp":iExp, "gold":iGold, "status":state, "school":dProId2Name.get(iSchool), "createAt":crt,"account":sAccount,"loginAt":lg, "loginOutAt":lgo}
			oAccount = account.gJitKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, sUserSource, sAccount)
			dRes['vipLv']=oAccount.vipLv()
			oRole,oMutilFileRole=getRoleOrMutilFile(iRoleId)#找是否在线
			rm = resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)

			if oRole:
				dRes['online']='在线'
			else:
				dRes['online']='离线'
			dRes['power']=rm.iFightAbility
			tKeys=(iRoleId,)
			oCycData= block.blockCycle.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, *tKeys)
			# dRes['rest']=oCycData.day.fetch('rest',REST_MAX) if oCycData else REST_MAX	#体力
			oPest = block.active.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, *tKeys)
			iRest=oPest.fetch('rest', 0)
			dRes['rest'] = iRest
			print u.trans2gbk('查询玩家的请求到了4')	
			#钻石直接查询数据库
			tempRs=db4ms.gConnectionPool.query('select diamond from account_multi_field where userSource=\'{}\' and account=\'{}\''.format(sUserSource, sAccount)) 
			if len(tempRs.rows)>1:
				raise Exception,'行数过多,返回结果集应该只有1行'
			elif len(tempRs.rows)<1:#数据库中没有此行			
				return False
			print u.trans2gbk('查询玩家的请求到了5')	
			dRes['dia']=0 if len(tempRs.rows)<1 else tempRs.rows[0][0]	#钻石
			lQueryRes.append(dRes)
		lQueryRes.insert(0, {'state':True})
		print u.trans2gbk('查询玩家的请求到了6')	
		return json.dumps(lQueryRes)
	# except Exception:
	# 	l=[]
	# 	l.extend([{'state':False, 'desc':'参数错误'}, dQueryParam])
	# 	return json.dumps(l)
	
def queryEquip(**dQueryParam):
	if True:
		#dQueryParam['type']表示查询类型 
		#a:随机查询10个在线的角色, i表示查看指定id的角色,n表示查看指定名字的角色,l表示查看指定等级的角色

		sroleType = dQueryParam.get('par1')
		srole = dQueryParam.get('par2')
		
		iRoleId = 0
		if sroleType=='i':
			iRoleId=int(srole)
		else:
			sSql='select roleId from role_multi_field1 where name={}'.format('\'' + srole.encode('utf-8') + '\'')
			rs=db4ms.gConnectionPool.query(sSql)
			if len(rs.rows)>1:
				raise Exception,'行数过多,返回结果集应该只有1行'
			elif len(rs.rows)<1:#数据库中没有此行
				return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
			(iRoleId,) = rs.rows[0]
		items = block.blockPackage.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
	
		
		reslut=[]
		index=0
		itemType={1:"武器",2:"帽子",3:"衣服",4:"项链",5:"裤子",6:"鞋子",7:"时装",8:"徽章"}
		for oProps in items.getAllValues():
			if oProps.uiType()!=c.PROPS_EQUIP:
				continue
			propsList=[]
			oMsg=oProps.getMsg(*oProps.MSG_FIRST)
			if oProps.wearPos() == 8:
				item ={'pos':oMsg.iPos, 'itemId':oMsg.iPropsId, 'itemName':oProps.name, 'itemType':itemType.get(oProps.wearPos()),'itemLev':oMsg.iUseLv,'enhanceLv':oProps.enhanceLv()}
			elif oProps.wearPos() == 7:
				item ={'pos':oMsg.iPos, 'itemId':oMsg.iPropsId, 'itemName':oProps.name, 'itemType':itemType.get(oProps.wearPos()),'itemLev':oMsg.iUseLv}
			else:
				item ={'pos':oMsg.iPos, 'itemId':oMsg.iPropsId, 'itemName':oProps.name, 'itemType':itemType.get(oProps.wearPos()),'itemLev':oMsg.iUseLv,'xkType':oProps.gemholds().get(oProps.wearPos()),'enhanceLv':oProps.enhanceLv(),'starLv':oProps.starLv()}
			propsList.append(item)
			reslut.append(propsList)
			reslut.append('&')
		
		reslut.insert(0, {'state':True})
		return json.dumps(reslut)

def accountLimit(**dparam):
	print u.trans2gbk('到账号限制了')
	reslut =[]
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)
	
def ipLimit(**dparam):
	print u.trans2gbk('到ip限制了')
	reslut =[]
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)
def cancelAccountLimit(**dparam):
	print u.trans2gbk('到取消账号限制了')
	reslut =[]
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)
def cancelIpLimit(**dparam):
	print u.trans2gbk('到取消ip限制了')
	reslut =[]
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)
def retention(**dParam):
	logDir = '../logMainServer/visit'
	startStr = dParam.get('par1')
	endStr = dParam.get('par2')
	startTimes = startStr.split('-')
	endTimes = endStr.split('-')
	
	begin = datetime.date(int(startTimes[0]),int(startTimes[1]),int(startTimes[2]))
	end = datetime.date(int(endTimes[0]),int(endTimes[1]),int(endTimes[2]))
	d = begin  
	delta = datetime.timedelta(days=1)  
	
	reslut = []#返回到后台数据
	reloginNum = 0
	while d <= end:  
		creates = {}#当天注册人数
		logins = {}#当天登陆人数
		retentions = {}#存每日留存率数据

		day = d.strftime("%Y-%m-%d") 
		sHour = ''
		for hour in range(0,24):
			
			if hour < 10:
				sHour = '0{}'.format(hour)
			else:
				sHour = '{}'.format(hour)
			fileName = 'visit.{}-{}.log'.format(day,sHour)
			fileDir = '{}/{}'.format(logDir,fileName)
			if os.path.exists(fileDir):
				f = open(fileDir)
				
				for line in f.readlines():
					ind = line.find('{')
					subStr = line[ind:]
					content = json.loads(subStr)
					
					if content.get('no') == 2:
						creates[content.get('rid')] = content.get('rid')
					if content.get('no') == 4 and content.get('act') == 1:
						logins[content.get('rid')] = content.get('rid')
						
				f.close()
		if len(creates) == 0:
			retentions['createNum'] = len(creates)	
			retentions['logNum'] = len(logins)
			retentions['days'] = day
			retentions['ret1'] = '-'
			retentions['ret2'] = '-'
			retentions['ret3'] = '-'
			retentions['ret4'] = '-'
			retentions['ret5'] = '-'
			retentions['ret6'] = '-'
			retentions['ret7'] = '-'
			retentions['ret15'] = '-'
			retentions['ret30'] = '-'
			reslut.append(retentions)
			reslut.append('&')
			d += delta
			continue

		#1-7日留存
		for index in range(1, 8):
			addDay = datetime.timedelta(days=index)
			nowDay = d + addDay
			subday = nowDay.strftime("%Y-%m-%d")
			for hour in range(0,24):
				fileName = 'visit.{}-{}.log'.format(subday,hour)
				fileDir = '{}/{}'.format(logDir,fileName)
				if os.path.exists(fileDir):
					f = open(fileDir)
				
					for line in f.readlines():
						indexs = line.find('{')
						subStr = line[indexs:]
						content = json.loads(subStr)
					
						if content.get('no') == 4 and content.get('act') == 1:
							if creates.has_key(content.get('rid')):
								reloginNum += 1
						
					f.close()
			retIndex = 'ret{}'.format(index)
			
			retentions[retIndex] =  ('%.2f'% (reloginNum * 100.0 / len(creates))) + '%'
			reloginNum = 0
		#15日留存
		addDay = datetime.timedelta(days=15)
		nowDay = d + addDay
		subday = nowDay.strftime("%Y-%m-%d")
		for hour in range(0,24):
			fileName = 'visit.{}-{}.log'.format(subday,hour)
			fileDir = '{}/{}'.format(logDir,fileName)
			if os.path.exists(fileDir):
				f = open(fileDir)
				
				for line in f.readlines():
					indexs = line.find('{')
					subStr = line[indexs:]
					content = json.loads(subStr)
					
					if content.get('no') == 4 and content.get('act') == 1:
						if creates.has_key(content.get('rid')):
							reloginNum += 1
						
				f.close()
		
			
		retentions['ret15'] =  ('%.2f'% (reloginNum * 100.0 / len(creates))) + '%'
		reloginNum = 0
		#30日留存
		addDay = datetime.timedelta(days=30)
		nowDay = d + addDay
		subday = nowDay.strftime("%Y-%m-%d")
		for hour in range(0,24):
			fileName = 'visit.{}-{}.log'.format(subday,hour)
			fileDir = '{}/{}'.format(logDir,fileName)
			if os.path.exists(fileDir):
				f = open(fileDir)
				
				for line in f.readlines():
					indexs = line.find('{')
					subStr = line[indexs:]
					content = json.loads(subStr)
					
					if content.get('no') == 4 and content.get('act') == 1:
						if creates.has_key(content.get('rid')):
							reloginNum += 1
						
				f.close()
		
			
		retentions['ret30'] = ('%.2f'% (reloginNum * 100.0 / len(creates))) + '%'
		reloginNum = 0


		retentions['logNum'] = len(logins)		
		retentions['days'] = day
		retentions['createNum'] = len(creates)	
		reslut.append(retentions)
		reslut.append('&')
		d += delta
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)
	# startDay = time.strptime(startStr, "%Y-%m-%d")#开始日期， 日期格式Y-M-D
	
	# print timeU.stamp2str(startDay)
	# endDay = time.strptime(endStr, "%Y-%m-%d")#结束日期， 日期格式Y-M-D
	
	
	return json.dumps({'state':False, 'desc':'查询失败'})
######################   gm指令    #############################

def getRoleOrMutilFile(iRoleId):#返回角色,和多列多列属性
	oRole=role.gKeeper.getObj(iRoleId)
	if oRole:
		return oRole, oRole.multiField1
	return oRole, multiFieldRole.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)

def setDiamond(**dParam):#设置钻石数量
	try:
		iRoleId,iDia=int(dParam.get('par1', -1)),int(dParam.get('par2', 0))
		if iDia==0 or iRoleId==-1:
			return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])
		sSql='select userSource, account, status from role_multi_field1 where roleId={}'.format(iRoleId)
		rs=db4ms.gConnectionPool.query(sSql)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行			
			return json.dumps([{'state':False, 'desc':'角色ID不对'}])
		(sUserSource, sAccount, iStatus) = rs.rows[0]
		if iStatus==-1:#该角色也被删除
			return json.dumps([{'state':False, 'desc':'角色ID不对'}])
		oAccount=account.gJitKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, sUserSource, sAccount)	#此处NO_ROW_RETURN_NONE
		if not oAccount:
			return json.dumps([{'state':False, 'desc':'角色ID没有对应的账号'}])
		iAddDia=iDia-oAccount.accountMf.iDiamond
		if iAddDia==0:
			return json.dumps([{'state':True}])
		if oAccount.iPlayingRoleId==0:
			oAccount.accountMf.addDiamond(iAddDia, 'gm系统设置', 'gm系统将你的钻石设置为{}'.format(iDia))
		else:
			oRole=role.gKeeper.getObj(oAccount.iPlayingRoleId)
			if not oRole:
				raise Exception, '账号的活跃角色为空'
			oRole.addDiamond(iAddDia, 'gm系统设置', 'gm系统将你的钻石设置为{}'.format(iDia))
		log.log('gm/diamond','gm系统通过ID为{}的角色设置账号 {},{}的钻石为{}'.format(iRoleId, sUserSource, sAccount, iDia))
		return json.dumps([{'state':True}])
	except Exception:
		print u.trans2gbk("setDiamond 出错了"),Exception
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])
		
def setRest(**dParam):#设置角色的当天的体力
	try:
		print u.trans2gbk("设置体力1")
		iRoleId,iRest=int(dParam.get('par1', -1)),int(dParam.get('par2', 0))
		oRole=role.gKeeper.getObj(iRoleId)
		print u.trans2gbk("设置体力2"),iRest
		if oRole:#角色在线
			print u.trans2gbk("设置体力3")
			oRole.addRest(iRest-oRole.rest(),'', None)
			log.log('gm/rest','gm系统设置角色ID为{}的体力为{}'.format(iRoleId, oRole.rest()))
		else:
			print u.trans2gbk("设置体力4")
			pass
			# oCycData=block.blockCycle.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, *(iRoleId,))
			# if not oCycData:
			# 	return json.dumps([{'state':False, 'desc':'角色ID不对'}])
			# oCycData.day.set('rest',min(iRest,REST_MAX))
		return json.dumps([{'state':True}])
	except Exception:
		print u.trans2gbk("设置体力 出错了")
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])

def setExp(**dParam):#增加角色的经验
	try:
		iRoleId,iExp=int(dParam.get('par1', -1)),int(dParam.get('par2', 0))
		if iExp<0:
			return json.dumps([{'state':False, 'desc':'不能将玩家的经验变为负数'}])
		oRole,oMutilFileRole=getRoleOrMutilFile(iRoleId)
		if not oMutilFileRole:
			return json.dumps([{'state':False, 'desc':'角色ID不对'}])
		if oMutilFileRole.iExp==iExp:
			return json.dumps([{'state':True}])
		iAddExp=iExp-oMutilFileRole.iExp
		if oRole:#角色在线
			oRole.addExp(iAddExp, '', None)
			ep=mainService.getEndPointByRoleId(*(int(iRoleId),))
			if ep:
				ep.rpcTips('gm系统将你经验设置为{}'.format(iExp))
		else:
			oMutilFileRole.iExp=iExp
		log.log('gm/exp','gm系统设置角色ID为{}的经验为{}'.format(iRoleId, iExp))
		return json.dumps([{'state':True}])
	except Exception:
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])

def setLv(**dParam):#设置角色的等级
	try:
		iRoleId,iLv=int(dParam.get('par1', -1)),int(dParam.get('par2', 0))
		if iLv<1:
			return json.dumps([{'state':False, 'desc':'不能将玩家的等级变为负数'}])
		oRole,oMutilFileRole=getRoleOrMutilFile(iRoleId)
		if not oMutilFileRole:
			return json.dumps([{'state':False, 'desc':'角色ID不对'}])
		if oMutilFileRole.level==iLv:
			return json.dumps([{'state':True}])
		oMutilFileRole.level=iLv
		if oRole:#角色在线
			oRole.attrChange('level','upNeedExp')
			oRole.reCalcAttr()
			oRole.accountObj.setLv(iRoleId,iLv )
			ep=mainService.getEndPointByRoleId(*(int(iRoleId),))
			if ep:
				ep.rpcTips('gm系统将你等级设置为{}'.format(iLv))
		log.log('gm/lv','gm系统设置角色ID为{}的等级为{}'.format(iRoleId, iLv))
		return json.dumps([{'state':True}])
	except Exception:
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])


def setGold(**dParam):	#增加指定角色ID的元宝
	try:
		iAdd=int(dParam.get('par2', 0))
		if iAdd<0:
			return json.dumps([{'state':False, 'desc':'不能把玩家的元宝变为负数'}])
		oRole,oMutilFileRole=getRoleOrMutilFile(int(dParam.get('par1', -1)))
		if not oMutilFileRole:
			return json.dumps([{'state':False, 'desc':'角色ID不对'}])
		if oMutilFileRole.iGold == iAdd:
			return json.dumps([{'state':True}])
		if oRole:	#角色在线
			oRole.addTradeCash(iAdd-oMutilFileRole.iGold, 'gm设置元宝', 'gm指令设置你的元宝为{}'.format(iAdd))
		else:
			oMutilFileRole.iGold=iAdd
		log.log('gm/gold','gm系统设置角色ID为{}的元宝为:{}'.format(int(dParam.get('par1', -1)), iAdd))
		return json.dumps([{'state':True}])	
	except Exception:
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])

def kickRole(**dParam):	#踢角色下线命令
	try:
		iRoleId=int(dParam.get('par1', -1))
		oRole=role.gKeeper.getObj(iRoleId)
		if not oRole:	#角色不在线
			return json.dumps([{'state':True}])
		oBeKickChn=mainService.getEndPointByRoleId(*(int(iRoleId),))
		if oBeKickChn:	#角色掉线了
			oBeKickChn.rpcTips('您被系统请离了.')
			oBeKickChn.shutdown()
		role.gKeeper.removeObj(iRoleId)
		log.log('gm/kick','gm系统将角色ID为{}踢下线了'.format(iRoleId))
		return json.dumps([{'state':True}])
	except Exception:
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])



def forRole(**dParam):
	try:
		iRoleId=int(dParam.get('par1', 0))
		sInstruct=dParam.get('par2', '')
		sInstruct=sInstruct.strip()#再以空白分开
		oChn=ep(iRoleId)
		instruction.realInstruction(oChn,sInstruct)
		sTips=getattr(oChn,'sContent','')
		print u.trans2gbk(sTips)
		return json.dumps([{'state':True, 'desc:':sTips}])
	except Exception:
		return json.dumps([{'state':False, 'desc':''}])

def restDCycData(**dParam):#清除角色的天数据
	return restCycData('d', **dParam)

def restHCycData(**dParam):#清除角色的小时数据
	return restCycData('h', **dParam)

def restWCycData(**dParam):#清除角色的周数据
	return restCycData('w', **dParam)

def restMCycData(**dParam):#清除角色的月数据
	return restCycData('m', **dParam)

def restCycData(sType, **dParam):#重置周期数据 sType数据类型
	dTypeMapAttr={#{类型:[role上对应的属性名字,cycData上对应的属性名字]}
		'w':['week', 'cycWeek'],
		'd':['day', 'cycDay'],
		'm':['month', 'cycMonth'],
		'h':['hour', 'cycHour'],
	}
	if sType not in dTypeMapAttr:
		return json.dumps([{'state':False, 'desc':'没有该类型的数据'}, dParam]) 
	try:
		iRoleId,iWeekNo=int(dParam.get('par1', -1)),int(dParam.get('par2', 0))
		if iWeekNo>0:
			return json.dumps([{'state':False, 'desc':'今天不能清除后面周期的数据吧'}]) 
		if iRoleId==-1:
			return json.dumps([{'state':False, 'desc':'角色ID错误'}])
		oRole=role.gKeeper.getObj(iRoleId)
		if oRole:#角色在线
			getattr(oRole, dTypeMapAttr[sType][0]).clear(iWeekNo)
		else:
			oCycData=block.blockCycle.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
			if not oCycData:
				return json.dumps([{'state':False, 'desc':'角色ID错误'}])
			getattr(oCycData, dTypeMapAttr[sType][1]).clear(iWeekNo)
		log.log('gm/{}'.format(dTypeMapAttr[sType][0]), 'gm系统将角色ID为{}的前{}个周期的数据清空了'.format(iRoleId,iWeekNo))
		return json.dumps([{'state':True}])
	except Exception:
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])	

#服务器相关
giCarrySatus=0	#gm设置的服务器状态

def openServer(**dParam):#开启服务器(不是开启进程),只是能让角色登录到游戏服
	if not block.parameter.parameter.isOpenForPlayer():
		block.parameter.parameter.setOpenForPlayer(1)
		log.log('gm/closeServer', 'gm系统开启当前服务器')
	return json.dumps([{'state':True}])

def closeServer(**dParam):#关闭游戏服(不是关闭进程),只是不能让玩家登入到游戏服,也登录的角色直接踢下线
	block.parameter.parameter.setOpenForPlayer(0)

	instruction.shutServer.broadcastShutGSMsg()
	instruction.shutServer.kickAllRole()
	log.log('gm/closeServer', 'gm系统关闭当前服务器')
	return json.dumps([{'state':True}])

def setGsMaxUser(**dParam):
	#设置服务器在线人数上限,只设置上限,不做其他处理
	iMaxUser=int(dParam.get('par1', block.parameter.DEFAULT_MAX_USER))
	block.parameter.parameter.setMaxUserCount(iMaxUser)
	return json.dumps([{'state':True}]) 

def setGmCarrySatues(**dParam):
	iCarrySatus=int(dParam.get('par1', 0))
	if iCarrySatus not in (0, FULL, IDLE, NORMAL):
		return json.dumps([{'state':False, 'desc':'状态参数不正确'}])
	global giCarrySatus
	giCarrySatus=iCarrySatus
	return gameServerInfo(**dParam)

######################发放################################
def issueCurrency(**dParam):#发放二级货币
	if True:
		sroleType = dParam.get('roletype')
		srole = dParam.get('role')
		sitem = dParam.get('item')
		sitemNum = dParam.get('itemNum')
		sSql = ''
 		if sroleType == 'n':#角色名查询
 			sSql='select userSource, account, status from role_multi_field1 where name={}'.format('\'' + srole.encode('utf-8') + '\'')
		else:
			sSql='select userSource, account, status from role_multi_field1 where roleId={}'.format(int(srole))
		rs=db4ms.gConnectionPool.query(sSql)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行
			return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
		(sUserSource, sAccount, iStatus) = rs.rows[0]
		if iStatus==-1:#该角色也被删除
			return json.dumps([{'state':False, 'desc':'角色ID不对'}])
		oAccount=account.gJitKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, sUserSource, sAccount)	#此处NO_ROW_RETURN_NONE
		if not oAccount:
			return json.dumps([{'state':False, 'desc':'角色ID没有对应的账号'}])
		if oAccount.lRoleList[0]!=0:
			oRole,oMutilFileRole=getRoleOrMutilFile(oAccount.lRoleList[0])
			if sitem=='jb':	 
				if not oRole:
					oMutilFileRole.iGold += int(sitemNum)
				else:
					oRole.addTradeCash(int(sitemNum),'gm后台发放')
					
				log.log('gm/gold','gm系统通过ID为{}的角色账号 {},{}增加元宝{}'.format(srole, sUserSource, sAccount, sitemNum))
			elif sitem=='zs':
				if not oRole:
					oAccount.accountMf.addDiamond(int(sitemNum), 'gm系统设置', 'gm系统将你的钻石增加了{}'.format(int(sitemNum)))
				else:
					oRole.addDiamond(int(sitemNum),'gm后台发放')
				
			else:
				pass

			return json.dumps([{'state':True}])
	# except Exception:
	# 	return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])

	return json.dumps({'state':False, 'desc':'发放失败'})

def addGm(**dParam):
	sRoleType = dParam.get('roletype')
	sRole = dParam.get('role')
	sUser = dParam.get('user').encode('utf-8')
	sReason = dParam.get('reason').encode('utf-8')
	iRoleId = 0
	if sRoleType == 'i':
		iRoleId = int(sRole)
	else:
		sSql='select roleId from role_multi_field1 where name={}'.format('\'' + sRole.encode('utf-8') + '\'')
		rs=db4ms.gConnectionPool.query(sSql)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行
			return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
		(iRoleId,) = rs.rows[0]
	cfg.gm.addGmAccountByRoleId(iRoleId, sUser, sReason)
	return json.dumps([{'state':True, 'desc':'成功'}, dParam])

def cancelGm(**dParam):
	print u.trans2gbk("到取消gm账号了")
	sRoleType = dParam.get('roletype')
	sRole = dParam.get('role')
	iRoleId = 0
	if sRoleType == 'i':
		iRoleId = int(sRole)
	else:
		sSql='select roleId from role_multi_field1 where name={}'.format('\'' + sRole.encode('utf-8') + '\'')
		rs=db4ms.gConnectionPool.query(sSql)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行
			return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
		(iRoleId,) = rs.rows[0]
	cfg.gm.delGmAccountByRoleId(iRoleId)
	print u.trans2gbk('到取消gm账号了sRoleType:'),sRoleType, "iRoleId:",iRoleId
	return json.dumps([{'state':True, 'desc':'成功'}, dParam])
def queryRank(**dParam):
	print u.trans2gbk('到排行榜查询了')
	sRankType = dParam.get('ranktype')
	print 'ranktype::',sRankType
	result = []
	for i in range(1,10):
		dRes = {'ranking':i,'role':'xx','amount':i*10}
		result.append(dRes)
	result.insert(0, {'state':True})
	return json.dumps(result)

def addWhiteList(**dParam):
	sAccount = dParam.get('account')
	sEndAt = dParam.get('endAt')
	sql = 'INSERT INTO whitelist (account,endAt)VALUES(\'{}\',\'{}\')'.format(sAccount, sEndAt)
	db4ms.gConnectionPool.query(sql)
	svcAccount.loadWhiteList()
	result = []
	result.insert(0, {'state':True})
	return json.dumps(result)

def cancelWhiteList(**dParam):
	sAccount = dParam.get('account')
	sql = 'delete from whitelist where account = \'{}\''.format(sAccount)
	print 'sql ::',sql
	db4ms.gConnectionPool.query(sql)
	svcAccount.removeWhiteList(sAccount)
	result = []
	result.insert(0, {'state':True})
	return json.dumps(result)

def queryHero(**dParam):
	print u.trans2gbk('到英雄查询了')

	sroleType = int(dParam.get('roleSelect'))
	srole = dParam.get('roleInput')
	print sroleType,srole
	iRoleId = 0
	if sroleType==1:
		iRoleId=int(srole)
	else:
		sSql='select roleId from role_multi_field1 where name={}'.format('\'' + srole.encode('utf-8') + '\'')
		rs=db4ms.gConnectionPool.query(sSql)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行
			return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
		(iRoleId,) = rs.rows[0]

	#通过iRoleId 获得玩家的英雄列表（玩家不在线）
	reslut=[]
	heros = factoryConcrete.epicFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
	for hero in heros.getAllValues():
		item = {}
		item['heroLv'] = hero.getLv()
		item['heroName'] = hero.name
		print u.trans2gbk('英雄等级：'),hero.getLv(),u.trans('英雄名：'),hero.name
		reslut.append(item)
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)


def queryFb(**dParam):
	sDate = dParam.get('date')
	reslut=[]
	barrierType={5:"沉默森林",9:"凯德拉飞艇",7:"寂静修道院",6:"古代武器仓库"}
	dAtt = {}

	taskDir='{}/logMainServer/ddic/enterInstance'.format(os.path.dirname(os.getcwd()))
	print 'taskDir::',taskDir
	for parent, packages,filenames in os.walk(taskDir):
		for fileName in filenames:
			if sDate in fileName:
				fileDir = '{}/{}'.format(parent,fileName)
				fileObj=open(fileDir, 'r')
				while True:
					sInstance=fileObj.readline()
					if not sInstance:
						break
					
					lList = sInstance.split('\t')
					barrierKind = int(lList[10])
					if barrierKind in barrierType:
						if barrierKind not in dAtt:
							d = {}
							drole = {}
							daccount = {}
							drole[lList[1]] = lList[1]
							daccount[lList[3]] = lList[3]
							d['num'] = 1
							d['role'] = drole
							d['account'] = daccount
							dAtt[barrierKind] = d
						else:
							dOld = dAtt[barrierKind]
							dOld['num'] += 1
							dOldRole = dOld['role']
							dOldAccount = dOld['account']
							dOldRole[lList[1]] = lList[1]
							dOldAccount[lList[3]] = lList[3]

	for i in barrierType:
		item = {}
		
		if i not in dAtt:
			continue
		dd = dAtt[i]
		item['accountNum'] = len(dd['account'])
		item['fbName'] = barrierType.get(i)
		item['roleNum'] = len(dd['role'])
		item['times'] = dd['num']
		reslut.append(item)
			
		
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)

def queryPet(**dParam):
	print u.trans2gbk('到宠物查询了')
	sroleType = int(dParam.get('roleSelect'))
	srole = dParam.get('roleInput')
	print sroleType,srole
	iRoleId = 0
	if sroleType==1:
		iRoleId=int(srole)
	else:
		sSql='select roleId from role_multi_field1 where name={}'.format('\'' + srole.encode('utf-8') + '\'')
		rs=db4ms.gConnectionPool.query(sSql)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行
			return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
		(iRoleId,) = rs.rows[0]

	print 'iRoleId::', iRoleId
	reslut=[]
	pets = factoryConcrete.petCtnFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
	lfightPet = pets.getFightPetGroup()
	for pet in pets.getAllValues():
		ipetNo = pet.no() #宠物类型 1~6
		item = {}
		item['petLv'] = pet.level
		item['petName'] = pet.name
		item['advanceLv'] = pet.advanceLv()
		if ipetNo in lfightPet:
			item['isfight'] = '上阵'
		else:
			item['isfight'] = '下阵'
		reslut.append(item)
	
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)

def queryOnlinetime(**dParam):
	print u.trans2gbk('到在线时长查询了'),os.getcwd()
	sDate = dParam.get('date')
	sroleType = dParam.get('roleSelect')
	sroleInput = dParam.get('roleInput')
	print 'sdate::',sDate,'sroleType:',sroleType,'sroleInput:',sroleInput
	taskDir='{}/logMainServer/visit'.format(os.path.dirname(os.getcwd()))

	reslut = []
	if sroleInput != 'all':
		itimes = 0
		sroleName =''
		saccount = ''
		for parent, packages,filenames in os.walk(taskDir):
		
			for fileName in filenames:
				print u.trans2gbk('日期：：'),sDate, u.trans(' 遍历的文件名：：：'),fileName
				if sDate in fileName:
					print u.trans2gbk('存在了要查询的文件')
					fileDir = '{}/{}'.format(parent,fileName)
					fileObj=open(fileDir, 'r')
					while True:
						line=fileObj.readline() 
						if not line:
							print u.trans2gbk('文件无记录')
							break
						ind = line.find('{')
						subStr = line[ind:]
						content = json.loads(subStr)
						if content.get('no') == 4 and content.get('act') == 2:
							if content.get('rn') == sroleInput or content.get('rid') == sroleInput:
								itimes += content.get('ot')
								sroleName = content.get('rn')
								saccount = content.get('uid')

		item = {}
		
		item['roleName'] = sroleName
		item['account'] = saccount
		item['time'] = itimes
		reslut.append(item)	
		reslut.insert(0, {'state':True})
		return json.dumps(reslut)
	
	iTotal = 0
	dRole = {}
	dAccount = {}
	iDeadTimes = 0
	
	dtime = {}
	dAccount = {}
	# print ',,,:',len(os.walk(taskDir))
	for parent, packages,filenames in os.walk(taskDir):
		print 'parent:',parent,'filenames:',filenames
		for fileName in filenames:
			print u.trans2gbk('日期：：'),sDate, u.trans(' 遍历的文件名：：：'),fileName
			if sDate in fileName:
				print u.trans2gbk('存在了要查询的文件')
				fileDir = '{}/{}'.format(parent,fileName)
				fileObj=open(fileDir, 'r')
				while True:
					line=fileObj.readline() 
					if not line:
						print u.trans2gbk('文件无记录')
						break
					ind = line.find('{')
					subStr = line[ind:]
					content = json.loads(subStr)
								
					if content.get('no') == 4 and content.get('act') == 2:
						print u.trans2gbk('有登出日志记录')
						if content.get('rn') not in dtime:
							print u.trans2gbk('第一次插入：'),content.get('rn')
							dtime[content.get('rn')] = int(content.get('ot'))
						else:
							dtime[content.get('rn')] += int(content.get('ot'))
						dAccount[content.get('rn')] = content.get('uid')
	print 'dtime:::',dtime
	for roleName,itime in dtime.iteritems():
		item = {}
		
		item['roleName'] = roleName
		item['account'] = dAccount.get(roleName)
		item['time'] = itime
		reslut.append(item)					

		
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)

def querySkill(**dParam):
	print u.trans2gbk('到到技能查询了')
	sroleType = int(dParam.get('roleSelect'))
	srole = dParam.get('roleInput')
	print sroleType,srole
	iRoleId = 0
	if sroleType==1:
		iRoleId=int(srole)
	else:
		sSql='select roleId from role_multi_field1 where name={}'.format('\'' + srole.encode('utf-8') + '\'')
		rs=db4ms.gConnectionPool.query(sSql)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行
			return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
		(iRoleId,) = rs.rows[0]

	#通过iRoleId获取玩家技能列表，（玩家不在线）
	skills = factoryConcrete.skillFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
	reslut=[]
	
	for skill in skills.getAllValues():
		item = {}
		item['skillLv'] = skill.level
		item['skillName'] = skill.name
		print u.trans2gbk('技能等级：'),skill.level,u.trans('技能名：'),skill.name
		reslut.append(item)
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)

	# reslut=[]
	# for i in range(1,10):
	# 	item = {}
	# 	item['skillLv'] = i
	# 	item['skillName'] = 'name'+str(i)
	# 	reslut.append(item)
			
		
	# reslut.insert(0, {'state':True})
	# return json.dumps(reslut)


def queryNewer(**dParam):
	print u.trans2gbk('到新手引导查询了')
	sroleType = int(dParam.get('roleSelect'))
	srole = dParam.get('roleInput')
	print sroleType,srole
	reslut=[]
	if srole != 'all':
		iRoleId = 0
		sRoleName = ''
		if sroleType==1:
			iRoleId=int(srole)
		else:
			sSql='select roleId from role_multi_field1 where name={}'.format('\'' + srole.encode('utf-8') + '\'')
			rs=db4ms.gConnectionPool.query(sSql)
			if len(rs.rows)>1:
				raise Exception,'行数过多,返回结果集应该只有1行'
			elif len(rs.rows)<1:#数据库中没有此行
				return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
			(iRoleId,) = rs.rows[0]
			sRoleName = srole.encode('utf-8')
		lazys = factoryConcrete.lazyFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
		newbie = lazys.fetch('ng',[])
		inNewbie = lazys.fetch('newbie')
		print 'newbie::::::::::::::',newbie,'inNewbie:::::',inNewbie
		isFinish = '停留在飞艇关'
		print 'len(newbie):',len(newbie),'len(newbieGuideData.gdData):',len(newbieGuideData.gdData)
		if len(newbie) > 1:
			isFinish = '已到达新手村'
		item = {}
		item['roleId'] = iRoleId
		item['roleName'] = sRoleName
		item['stopAt'] = isFinish
		reslut.append(item)
		reslut.insert(0, {'state':True})
		return json.dumps(reslut)
	else:
		sql = "select roleId,name from role_multi_field1" #查询等级人数分
		rs=db4ms.gConnectionPool.query(sql)

		for iRoleId,name in rs.rows:
			lazys = factoryConcrete.lazyFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)
			if lazys == None:
				continue
			newbie = lazys.fetch('ng',[])
			inNewbie = lazys.fetch('newbie')
			print 'newbie::::::::::::::',newbie,'inNewbie:::::',inNewbie
			isFinish = '停留在飞艇关'
			print 'len(newbie):',len(newbie),'len(newbieGuideData.gdData):',len(newbieGuideData.gdData)
			if len(newbie) > 1:
				isFinish = '已到达新手村'
			item = {}
			item['roleId'] = iRoleId
			item['roleName'] = name
			print 'name:::',name
			item['stopAt'] = isFinish
			reslut.append(item)
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)

def sendItem(**dParam):
	print u.trans2gbk('到发放物品了')
	sroleType = dParam.get('roleType')
	srole = dParam.get('roleInput')
	iItemId = int(dParam.get('itemId'))
	iItemNum = int(dParam.get('itemNum'))
	print sroleType,srole
	iRoleId = 0
	if sroleType=='i':
		iRoleId=int(srole)
	else:
		sSql='select roleId from role_multi_field1 where name={}'.format('\'' + srole.encode('utf-8') + '\'')
		rs=db4ms.gConnectionPool.query(sSql)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行
			return json.dumps([{'state':False, 'desc':'角色名或ID不对'}])
		(iRoleId,) = rs.rows[0]

	oRole=role.gKeeper.getObj(iRoleId)
	reslut=[]
	if oRole:#角色在线
		oLaunchMng = launchMng.cLaunchMngNew('gm投放')
		oLaunchMng.launchBySpecify(oRole,iItemId,iItemNum,(), {}, False)
	else:	
		oRole=factoryConcrete.roleFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE,iRoleId)
		oLaunchMng = launchMng.cLaunchMngNew('gm投放')
		oLaunchMng.launchBySpecify(oRole,iItemId,iItemNum,(), {}, False)
		oRole._saveToDB()
		reslut.insert(0, {'state':True})
		return json.dumps(reslut)
	reslut.insert(0, {'state':True})
	return json.dumps(reslut)
def reloadNotice(**dParam):

	print u.trans2gbk('到加载公告通知了')
	
	return json.dumps([{'state':True, 'desc':'成功'}, dParam])

gdCmdMapFunc={
	'kickRole':kickRole,	#踢角色下线

	'setGold':setGold,		#设置角色的元宝
	'setLv':setLv,			#设置角色的等级
	'setExp':setExp,		#设置角色的经验
	'setRest':setRest,		#设置角色当天的体力
	'setDiamond':setDiamond,#设置账号的钻石数量

	'restWCycData':restWCycData,	#清除角色的星期数据
	'restHCycData':restHCycData,	#清除角色的小时数据
	'restDCycData':restDCycData,	#清除角色的天数据
	'restMCycData':restMCycData,	#清除角色的月数据

	'openGS':openServer,	#开启服务器(不是开启进程),只是能让角色登录到游戏服
	'closeGS':closeServer,	#关闭游戏服(不是关闭进程),只是不能让玩家登入到游戏服,也登录的角色直接踢下线
	'gsMU':setGsMaxUser,	#设置服务器在线人数上限
	'gsSct':setGmCarrySatues,#设置服务器的状态
	'forRole':forRole,      #游戏服的指令
	'equip':queryEquip, #查询玩家的装备
	'retention':retention,#留存率查询
	
	'addGm':addGm,
	'cancelGm' : cancelGm,
	'queryRank' : queryRank,
	'addWhiteList':addWhiteList,
	'cancelWhiteList' : cancelWhiteList,
	'queryHero':queryHero,
	'queryPet':queryPet,
	'queryNewer':queryNewer,
	'querySkill':querySkill,
	'queryOnlinetime':queryOnlinetime,
	'queryFb':queryFb,
	'sendItem':sendItem,
	'reloadNotice':reloadNotice,
}	

#指令
def command(**dParam):
	# dParam={"cmd":"cmd","param1":"111","param2":"10000"}
	print u.trans2gbk('进入command'), dParam

	func=gdCmdMapFunc.get(dParam.get('cmd', None), None)
	if func:
		sResult=func(**dParam)
		log.log('ddic/gm', '\t{}\t{}'.format(dParam.get('cmd', None), sResult))
		return sResult
	return json.dumps([{'state':False, 'desc:':'gm没有对应的指令'}])


######################公告#############################

def notice(**dParam):
	sContent=dParam.get('context', None)
	if not sContent:
		return json.dumps([{'state':True}])
	sContent=sContent.encode('utf-8')
	for (iRoleId,) in role.gKeeper.getKeys():
		oChn=mainService.getEndPointByRoleId(iRoleId)
		if oChn:
			oChn.rpcAnnounce(1, sContent)
	print u.trans2gbk(sContent)
	return json.dumps([{'state':True}])

######################统计#############################
def gameServerInfo(**dParam):#游戏服的信息
	dRes={'state':True}
	dRes['gamer']=role.gKeeper.amount()	#在线人数
	dRes['maxGamer']=block.parameter.parameter.getMaxUserCount()	#最大在线人数
	dRes['openGS']=block.parameter.parameter.isOpenForPlayer()	#是否处于开服(允许角色登录)状态
	dRes['zoneNo']=config.ZONE_NO	#区号
	global giCarrySatus
	dRes['carry']=giCarrySatus or getGsSate(dRes['gamer'], dRes['maxGamer'])
	return json.dumps([dRes])	

def getGsSate(iOnline, iMax):
	if iOnline >= iMax * FULL_PER:
		return FULL
	if iOnline >= iMax * NORMAL_PER:
		return NORMAL
	return IDLE

######################  邮件  #########################
SELECT_ALL_ROLEID='select roleId, status from role_multi_field1'

def send(iRoleId):
	lItems=[]
	oProp=props.new(200)
	oProp.setStack(100)
	lItems.append(oProp)
	lItems.append((77, 100))
	mail.sendSysMail(iRoleId, '123', '123', None, *lItems)

def sendMailByRoleId(**dParam):#发送邮件给指定ID的角色,要么全部成功要么全部失败
	print u.trans2gbk('根据玩家id发送邮件了')
	try:
		sRoleIds=set(json.loads(dParam.get('accepter',[])))
		print u.trans2gbk('根据玩家id发送邮件了1')
		rs=db4ms.gConnectionPool.query(SELECT_ALL_ROLEID).rows
		sAllRoleIds=set([tData[0] for tData in rs if tData[1]!=-1]) 
		print 'sRoleIds:',sRoleIds,'sAllRoleIds:',sAllRoleIds
		if sRoleIds-sAllRoleIds:
			print u.trans2gbk('根据玩家id发送邮件了2')
			return json.dumps([{'state':False, 'desc:':'没有指定ID:{}的角色信息'.format(sRoleIds-sAllRoleIds)}])
		bRight,uData=_checkProps(**json.loads(dParam.get("slave", {})))
		if not bRight:
			print u.trans2gbk('根据玩家id发送邮件了3')
			return uData
		lItems=uData 
		# lItems, dItem=[], json.loads(dParam.get("slave", {}))
		# for sPropsNo in dItem: #检查物品编号是否正确	
		# 	iPropsNo,iItem=int(sPropsNo),int(dItem[sPropsNo])
		# 	if iPropsNo in c.VIR_ITEM:
		# 		lItems.append((iPropsNo,iItem))
		# 		continue
		# 	if iPropsNo in propsData.gdData or iPropsNo in equipData.gdData:
		# 		oProp=props.new(200)
		# 		oProp.setStack(10)
		# 		lItems.append(oProp)
		# 		continue
		# 	return json.dumps([{'state':False, 'desc:':'没有编号为{}的物品'.format(iPropsNo)}])
		for iRoleId in sRoleIds:#进度显示暂时不做
			mail.sendSysMail(iRoleId, dParam.get('emailTitle', 'gm').encode('utf-8'), dParam.get('emailContent', 'gm').encode('utf-8'), None, *lItems)
		return 	json.dumps([{'state':True,'desc':'发送成功'}])
	except Exception:
		print u.trans2gbk('根据玩家id发送邮件了4')
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])	

def _checkProps(**dItem):#检查物品编号是否正确	
	lItems=[]
	for sPropsNo in dItem: #检查物品编号是否正确	
		iPropsNo,iItem=int(sPropsNo),int(dItem[sPropsNo])
		if iPropsNo in c.VIR_ITEM:
			lItems.append((iPropsNo,iItem))
			continue
		if iPropsNo in propsData.gdData or iPropsNo in equipData.gdData:
			oProp=props.new(iPropsNo)
			oProp.setStack(iItem)
			lItems.append(oProp)
			continue
		return False, json.dumps([{'state':False, 'desc:':'没有编号为{}的物品'.format(iPropsNo)}])
	return True, lItems		

			
def sendMailToAllRole(**dParam):#给全服所有角色发送邮件
	try:
		rs=db4ms.gConnectionPool.query(SELECT_ALL_ROLEID).rows
		lAllRoleIds=[tData[0] for tData in rs if tData[1]!=-1]
		
		bRight,uData=_checkProps(**json.loads(dParam.get("slave", {})))
		if not bRight:
			return uData
		lItems=uData 

		for iRoleId in lAllRoleIds:
			mail.sendSysMail(iRoleId, dParam.get('emailTitle', 'gm').encode('utf-8'), dParam.get('emailContent', 'gm').encode('utf-8'), None, *lItems)
		return 	json.dumps([{'state':True,'desc':'发送成功'}])
	except Exception:
		return json.dumps([{'state':False, 'desc':'参数错误'}, dParam])		

def sendMail(**dParam):
	print u.trans2gbk('到发送邮件总入口了')
	iType=dParam.get('iType', None)
	if not iType or iType not in ('1', '2', '3'):
		return json.dumps([{'state':False, 'desc:':'需要指定发送邮件的类型'}])
	if iType=='1':#指定角色ID
		return sendMailByRoleId(**dParam)
	elif iType=='2':#指定条件
		# print 'mail:', dParam
		pass
	elif iType=='3':#给全服所有角色发送邮件
		return sendMailToAllRole(**dParam)
	return json.dumps([{'state':True}])

def getOnLineGamer(**dParam):
	return ('area{}\{};'.format(config.ZONE_NO, role.gKeeper.amount()))

class ep(object):
	def __init__(self,iRoleId):
		self.iRoleId=iRoleId
		self.bGm=True

	def group(self):
		return instruction.ADMIN

	def rpcModalDialog(self,sContent,*tArgs,**dArgs):
		self.sContent=sContent

	def rpcTips(self,sContent):
		self.sContent=sContent

	def selfDescription(self,*tArgs,**dArgs):
		return 'gm系统,角色id为:{}'.format(self.iRoleId)


#服务器状态(服务器负载状态)
FULL, FULL_PER=1, 0.85 	#爆满(在线人数/上限 >= 85%)
NORMAL, NORMAL_PER=2, 0.3 #正常(30% <= 在线人数/上限 <85%)
IDLE=3	#空闲(在线人数/上限 < 30%)

import equipData
import propsData
import mail
import db4ms
import rand
import json
import role
import log
import random
import u
import c
import factory

import mainService
import multiFieldRole
import block.blockCycle
import block.parameter
import block.active
import account
import common_pb2
import gevent
import gevent.socket
import misc
import instruction.shutServer
import props
import instruction
import resume
import timeU
import time
import props.equip
import datetime
import props_pb2
import os
import sys


import cfg.gm
import svcAccount
import factoryConcrete
import launchMng
import config
