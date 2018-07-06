#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import misc
import config
import block.singleton


TREND_REFRESH_INTERVAL=30#趋势统一刷新间隔

#排行榜
class cRanking(block.singleton.cSingleton):
	if config.IS_INNER_SERVER: #排行榜刷新间隔(秒)
		REFRESH_INTERVAL=5
	else:
		REFRESH_INTERVAL=5*60

	def __init__(self,iMainNo,iRankNo,sChineseName,sName,iDisplaySize):#override	
		block.singleton.cSingleton.__init__(self,sChineseName,sName)
		self.iMainNo = iMainNo
		self.iRankNo = iRankNo

		#不能统一用角色ID，因为宠物榜一个角色可以有多个宠物上榜
		#iUid 有可能是角色ID，宠物ID
		self.dIdNameValue={} 	#{iUid:(名字,value),iUid:(名字,value),iUid:(名字,value)}
		self.lRanking=[] 		#[iUid,iUid,iUid],里面全是玩家id,优先按(战斗力/元宝/等级)排序,若相同,再按上榜时间先后顺序排序.
		self.dBuffer={} 		#缓冲,{iUid:(名字,value),iUid:(名字,value),iUid:(名字,value)}
		self.dLast={} 			#上次排行榜
		self.dHistory={} 		#历史排行榜,{iUid:索引,iUid:索引,iUid:索引} 
		self.oTimerMng=timer.cTimerMng()#定时器
		self.iDisplaySize=iDisplaySize #显示给玩家看的榜单人数上限
		self.iStoreSize=iDisplaySize*2 #实际排行榜上缓存的数量(上了榜人下榜了,后面的人补上)
		self.uTimerId=0
		self.iLastStamp=timeU.getStamp()

	def clearRank(self):
		'''清空排行榜：指令用
		'''
		self.dIdNameValue={}
		self.lRanking=[]
		self.dBuffer={}
		self.markDirty()

	def instructResort(self):
		'''执行二分插入：指令用
		'''
		self.lRanking = []
		for iUid in self.dIdNameValue.keys():
			findSort.binaryInsertRight(self.lRanking,iUid,self._valueComparer)

	def load(self,dData):#override
		block.singleton.cSingleton.load(self,dData)
		for tInfo in dData.pop('r',[]):
			if len(tInfo) == 2:
				iUid,iValue = tInfo
				dArgs = {}
			else:
				iUid,iValue,dArgs = tInfo
			self.lRanking.append(iUid)
			iRoleId = iUid
			if "iRoleId" in dArgs:
				iRoleId = dArgs["iRoleId"]
			
			dResumeData=getResumeDataFromDB(iRoleId)
			dResumeData=dResumeData.get("data", {})
			sName=dResumeData.get('name','')
			iLv=dResumeData.get('level',1)
			iSchool=dResumeData.get("school",1)
			self.dIdNameValue[iUid]=[sName,iValue,iLv,iSchool,dArgs]

	def save(self):#override
		dData=block.singleton.cSingleton.save(self)
		l=[]
		for iUid in self.lRanking:
			iValue=self.dIdNameValue[iUid][1]
			dArgs=self.dIdNameValue[iUid][4]
			if dArgs:
				l.append((iUid,iValue,dArgs))
			else:
				l.append((iUid,iValue))
		dData['r']=l
		if config.IS_INNER_SERVER:
			log.log('rank/save','{}|{}|{}'.format(self.chineseName(),dData,self.lRanking))
		return dData

	def timerUpdateRanking(self):#override 刷新排行榜
		bRet=self.updateRanking()
		if bRet:
			self.markDirty()#刷新榜单后要存盘
		return bRet

	def startTimer(self):#启动定时器,用于定时刷新排行榜
		self.uTimerId=self.oTimerMng.run(self.timerUpdateRanking,0, self.REFRESH_INTERVAL)

	def updateScore(self,iUid,sName,iNewValue,iLv,iSchool,**dArgs):#更新成绩
		#数值比最后一名的分数还低，就不加入排行了，会不会有问题？
		# if len(self.lRanking) >= self.iStoreSize:#排行榜已满
		# 	iLastRankUid = self.lRanking[-1]	#最后一名
		# 	if iLastRankUid != iUid:
		# 		if iNewValue < self.getValue(iLastRankUid):
		# 			return

		self.dBuffer[iUid]=[sName,iNewValue,iLv,iSchool,dArgs]#非实时刷新排行榜,等待定时器到了再刷

	def removeRecordByUid(self,iUid):#清除某角色的记录(删除一个角色时会调到这里)
		iIndex=self.findIndex(iUid)
		if iIndex!=len(self.lRanking):
			self.lRanking.pop(iIndex)
			
		self.dBuffer.pop(iUid,None)
		self.dHistory.pop(iUid,None)
		self.dIdNameValue.pop(iUid,None)

	def _valueComparer(self,iUid1,iUid2):#排序比较器
		iValue1=self.dIdNameValue[iUid1][1]
		iValue2=self.dIdNameValue[iUid2][1]
		if iValue1<iValue2:
			return 1
		elif iValue1>iValue2:
			return -1

		if iUid1 == iUid2:
			return 0
		return 1 if iUid1>iUid2 else -1

	def findIndex(self,iUid):#查找某个角色在榜上的位置,从0开始,不在榜上则返回pass the end
		if iUid not in self.lRanking:#没有上榜
			return len(self.lRanking)
		iIdx1=findSort.binarySearchLeft(self.lRanking,iUid,self._valueComparer)
		iIdx2=findSort.binarySearchRight(self.lRanking,iUid,self._valueComparer)
		if iIdx1==iIdx2:#没有找到
			if config.IS_INNER_SERVER:
				log.log('rank/error','findIndex error1 {}|{}|{}|{}|{}|{}'.format(self.chineseName(), iIdx1,iIdx2,iUid,self.lRanking,self.dIdNameValue))
				print iIdx1,iIdx2,iUid,self.lRanking
			raise Exception,'不可能找不到的,哪里数据不一致了吗?'

		for iIndex in xrange(iIdx1,iIdx2):#这个区间的玩家是战斗力/等级/元宝是相同的,只能按id遍历一下
			if self.lRanking[iIndex]==iUid:
				return iIndex
		if config.IS_INNER_SERVER:
			log.log('rank/error','findIndex error2 {}|{}|{}|{}|{}|{}'.format(self.chineseName(), iIdx1,iIdx2,iUid,self.lRanking,self.dIdNameValue))
			print iIdx1,iIdx2,iUid,self.lRanking
		raise Exception,'不可能找不到的,哪里数据不一致了吗?'

	def _checkRankValueComparer(self, iUid):
		#比较值
		if self.getValue(iUid)!=self.dBuffer[iUid][1]:
			return False
		#名字
		if self.getRoleName(iUid)!=self.dBuffer[iUid][0]:
			return False
		return True

	def checkRankValueChange(self):  #原本已经在榜,更新到最新数据
		for iUid in self.dBuffer.keys():
			if iUid not in self.dIdNameValue:
				#因为不在榜的时候 getValue返回0默认值,self.dBuffer[iUid][1],这样回造成玩家不上榜
				#特殊情况下,值为0也有可能上榜的
				continue
			iIndex=self.findIndex(iUid)
			if self._checkRankValueComparer(iUid):
			# if self.getValue(iUid)==self.dBuffer[iUid][1]:
				self.dBuffer.pop(iUid)
			elif iIndex<len(self.lRanking):
				self.lRanking.pop(iIndex)#找到某roleId在list的索引,pop索引速度快

	def updateRanking(self):#刷新排行榜
		if not self.dBuffer:#缓冲榜单没有变化
			return False
		#生成上次榜单的映射,用于反映每个玩家当前趋势(上升,持平,下降)
		self.dLast.clear()
		for iIndex,iUid in enumerate(self.lRanking):
			self.dLast[iUid]=iIndex

		#原本已经上榜的,先弹掉.以最新的成绩为准
		self.checkRankValueChange()
		if not self.dBuffer:
			return False

		self.dIdNameValue.update(self.dBuffer)#把最新有变化的名单合并到榜内名单(二分插入时马上用得到)
		#执行二分插入
		for iUid in self.dBuffer.keys():
			findSort.binaryInsertRight(self.lRanking,iUid,self._valueComparer)
		self.dBuffer.clear()
		#开始清理超出榜单上限的数据
		for iUid in self.lRanking[self.iStoreSize:]:			
			self.dIdNameValue.pop(iUid,None)
			self.dHistory.pop(iUid,None)
		
		self.lRanking=self.lRanking[:self.iStoreSize]#把多余的切掉

		iCurStamp=timeU.getStamp()
		iSub=iCurStamp-self.iLastStamp
		self.iLastStamp=iCurStamp
		for iIndex,iUid in enumerate(self.lRanking):
			if self.dLast.get(iUid,255)==255:
				continue
			if self.dLast[iUid]!=iIndex or iSub>=TREND_REFRESH_INTERVAL:
				self.dHistory[iUid]=self.dLast[iUid]
		# if config.IS_INNER_SERVER:
		log.log('rank/updateRanking','{}|{}|{}'.format(self.chineseName(),self.lRanking,self.dIdNameValue))
		return True

	def getRank(self,iUid):
		iRank = self.findIndex(iUid)+1
		if iRank > len(self.lRanking) or iRank > self.iDisplaySize:
			return 0
		return iRank
		# return self.findIndex(iUid)+1 if iUid in self.lRanking else 0
		#return self.findIndex(iUid)+1 if iUid in self.dIdNameValue else 0

	def getOldRank(self,iUid):
		return self.dHistory[iUid]+1 if iUid in self.dHistory else 0

	def getValue(self,iUid):
		return self.dIdNameValue[iUid][1] if iUid in self.dIdNameValue else 0

	def getRoleName(self,iUid):
		return self.dIdNameValue[iUid][0] if iUid in self.dIdNameValue else ''

	def getRoleLv(self,iUid):
		return self.dIdNameValue[iUid][2] if iUid in self.dIdNameValue else 1

	def getRoleSchool(self,iUid):
		return self.dIdNameValue[iUid][3] if iUid in self.dIdNameValue else 11

	def getRoleArgs(self, iUid):
		return self.dIdNameValue[iUid][4] if iUid in self.dIdNameValue else {}

	def ranking(self):
		return self.lRanking

	#===================================
	#
	def rankNo(self):
		return self.iRankNo

	def canQuit(self):
		'''是否可以退榜
		'''
		return self.getConfig("退榜", 0)

	def getConfig(self, key, default):
		return RankData.gdData.get(self.iRankNo, {}).get(key, default)

	def showLv(self):
		return self.getConfig("显示等级", 0)

	def quitRank(self, who):
		self.removeRecordByUid(who.id)

	def addRank(self, who):
		raise Exception,"排行榜：{} 不支持退榜".format(self.chineseName())

	def title2(self, iUid):
		return self.getRoleName(iUid)

	def title3(self, iUid):
		school = self.getRoleSchool(iUid)
		return role.defines.schoolList.get(school, "")

	def title4(self, iUid):
		return str(self.getValue(iUid))

	def getRoleId(self, iUid):
		iRoldId = self.getRoleArgs(iUid).get("iRoleId", 0)
		if not iRoldId:
			iRoldId = iUid
		return iRoldId

	def lookInfo(self, who, other, iUid):
		# raise Exception,"排行榜：{} 没有实现查看详情".format(self.chineseName())
		if who.id == other.id:
			message.tips(who, "不能查看自己")
			return
		dMsg = hyperlink.service.packetRole(other)
		who.endPoint.rpcRoleHyperlink(**dMsg)

	def getMyRankInfo(self, who):
		'''我的名次信息
		'''
		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		tMyInfo.append(role.defines.schoolList.get(who.school, ""))
		tMyInfo.append(rank.rankCompositeScore(who))
		return tMyInfo

	def roleChangeInfo(self, who):
		'''角色信息改变
		'''
		iUid = who.id
		if iUid in self.dIdNameValue:
			self.dIdNameValue[iUid][0] = who.name
			self.dIdNameValue[iUid][2] = who.level
			self.markDirty()

		if iUid in self.dBuffer:
			self.dBuffer[iUid][0] = who.name
			self.dBuffer[iUid][2] = who.level
		
	def getGuildName(self, roleId):
		#所在帮派
		oResume = resume.getResume(roleId)
		guildName = oResume.fetch('guildName', "—")
		if not guildName:
			guildName = "—"
		return guildName



def getResumeDataFromDB(iRoleId):#直接从数据库拿到数据,用于开服的时候初始化
		sSql=sql.RESUME_SELECT
		rs=db4ms.gConnectionPool.query(sSql,iRoleId)
		if len(rs.rows)>1:
			raise Exception,'行数过多,返回结果集应该只有1行'
		elif len(rs.rows)<1:#数据库中没有此行			
			return {}

		if len(rs.rows[0])!=1:
			raise Exception,'列数只能是1列'

		sData=rs.rows[0][0] 
		if sData:
			try:
				dData=ujson.loads(sData)#反序列化
			except Exception:
				u.reRaise('反序列化\'{}\'数据块时出错,主键为{}'.format('resume',iRoleId))
		else:
			dData={}
		return dData


import u
import sql
import db4ms
import findSort
import resume
import factory
import role
import copy
import timer
import timeU
import log
import ujson
import role.defines
import RankData
import RankClassifyData
import types
import rank
import hyperlink.service
import message