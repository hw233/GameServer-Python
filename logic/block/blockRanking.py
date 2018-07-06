# #-*-coding:utf-8-*-
# #作者:马昭@曹县闫店楼镇
# import misc
# import config
# import block.singleton
# import rank

# if config.IS_INNER_SERVER:
# 	DISPLAY_SIZE=20
# else:
# 	DISPLAY_SIZE=20

# #排行榜
# class cRanking(block.singleton.cSingleton,rank.cRanking):
# 	def __init__(self,sChineseName,sName,iDisplaySize):#override
# 		block.singleton.cSingleton.__init__(self,sChineseName,sName)
# 		rank.cRanking.__init__(self,iDisplaySize)

# 	def updateRanking(self):#override 刷新排行榜
# 		bRet=rank.cRanking.updateRanking(self)
# 		if bRet:
# 			self.markDirty()#刷新榜单后要存盘
# 		return bRet

# 	def load(self,dData):#override
# 		block.singleton.cSingleton.load(self,dData)
# 		for iRoleId,iValue in dData.pop('r',[]):
# 			self.lRanking.append(iRoleId)
# 			dData=getResumeDataFromDB(iRoleId)
# 			sName=dData.get('name','')
# 			iLv=dData.get('level',1)
# 			iSchool=dData.get("school",1)
# 			self.dIdNameValue[iRoleId]=(sName,iValue,iLv,iSchool)


# 	def save(self):#override
# 		dData=block.singleton.cSingleton.save(self)
# 		l=[]
# 		for iRoleId in self.lRanking:
# 			iValue=self.dIdNameValue[iRoleId][1]
# 			l.append((iRoleId,iValue))
# 		dData['r']=l
# 		return dData

# def init():#启动服务器时初始化
# 	global gFightRank
# 	gFightRank=initRank('战斗力排行榜','fightRank',DISPLAY_SIZE,'fa')
# 	global gGoldRank
# 	gGoldRank=initRank('元宝排行榜','goldRank',DISPLAY_SIZE,'gold')
# 	global gLvRank
# 	gLvRank=initRank('等级排行榜','lvRank',DISPLAY_SIZE,'lv')

# #排行榜更新，删除角色调用
# def updRank(iRoleId):
# 	gFightRank.removeRecordByRoleId(iRoleId)
# 	gFightRank.updateRanking()
# 	gLvRank.removeRecordByRoleId(iRoleId)
# 	gLvRank.updateRanking()
# 	gGoldRank.removeRecordByRoleId(iRoleId)
# 	gGoldRank.updateRanking()

# def initRank(sChineseName,sName,iDisplaySize,sValue):
# 	oRank=cRanking(sChineseName,sName,iDisplaySize)
# 	if not oRank._loadFromDB():
# 		oRank._insertToDB(*oRank.getPriKey())

# 	oRank.startTimer()
# 	return oRank

# 	#测试代码,伪数据
# 	# import random
# 	# for i in xrange(1,100):
# 	# 	iRoleId=i
# 	# 	sName='name:{}'.format(i)
# 	# 	iValue=random.randint(1000,2000)
# 	# 	gFightRank.updateScore(iRoleId,sName,iValue)
# 	# 	print i
# 	# gFightRank.markDirty()

# def getResumeDataFromDB(iRoleId):#直接从数据库拿到数据,用于开服的时候初始化
# 		sSql=sql.RESUME_SELECT
# 		rs=db4ms.gConnectionPool.query(sSql,iRoleId)
# 		if len(rs.rows)>1:
# 			raise Exception,'行数过多,返回结果集应该只有1行'
# 		elif len(rs.rows)<1:#数据库中没有此行			
# 			return {}

# 		if len(rs.rows[0])!=1:
# 			raise Exception,'列数只能是1列'

# 		sData=rs.rows[0][0] 
# 		if sData:
# 			try:
# 				dData=ujson.loads(sData)#反序列化
# 			except Exception:
# 				u.reRaise('反序列化\'{}\'数据块时出错,主键为{}'.format('resume',iRoleId))
# 		else:
# 			dData={}
# 		return dData

# import findSort
# import u
# import db4ms
# import role
# import copy
# import timer
# import sql
# import ujson