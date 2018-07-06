#-*-coding:utf-8-*-
import rank.object

class cRanking(rank.object.cRanking):
	'''殿试排行榜
	'''

	def clearFinalExamRank(self):
		'''清空再排行
		'''
		self.dIdNameValue={}
		self.lRanking=[]
		# self.dBuffer={}
		self.markDirty()

	def startTimer(self):#启动定时器,用于定时刷新排行榜
		'''不用自动排行
		'''
		pass

	#override
	#排序按玩家的金章之试成绩进行排行，按已答完>未答完>未参加的顺序排行
	#已答完：耗时小的排在前面，若耗时相同则按初试耗时小的排在前面，若也相同则ID小的排在前面
	#未答完 成绩按已答题的时间+未答题的数量*30S算，耗时小的在前面，若耗时相同则按初试耗时小的在前面
	#未参加：成绩按70分钟计算，初试耗时小的排在前面，若相同则ID小的排在前面
	def _valueComparer(self, iUid1, iUid2):#排序比较器
		args1 = self.dIdNameValue[iUid1][4]
		args2 = self.dIdNameValue[iUid2][4]

		com1 = args1.get("com", 99)
		com2 = args2.get("com", 99)
		if com1<com2:
			return -1
		elif com1>com2:
			return 1

		comTime1 = args1.get("comTime", 9999)
		comTime2 = args2.get("comTime", 9999)
		if comTime1<comTime2:
			return -1
		elif comTime1>comTime2:
			return 1

		firstET1 = args1.get("firstET", 9999)
		firstET2 = args2.get("firstET", 9999)
		if firstET1<firstET2:
			return -1
		elif firstET1>firstET2:
			return 1

		if iUid1 == iUid2:
			return 0
		return 1 if iUid1>iUid2 else -1

	def _checkRankValueComparer(self, iUid):#override
		dRoleArgs = self.getRoleArgs(iUid)

		com1 = dRoleArgs.get("com", 99)
		com2 = self.dBuffer[iUid][4].get("com", 99)
		if com1 != com2:
			return False

		comTime1 = dRoleArgs.get("comTime", 0)
		comTime2 = self.dBuffer[iUid][4].get("comTime", 0)
		if comTime1 != comTime2:
			return False

		firstET1 = dRoleArgs.get("firstET", 0)
		firstET2 = self.dBuffer[iUid][4].get("firstET", 0)
		if firstET1 != firstET2:
			return False
			
		return rank.object.cRanking._checkRankValueComparer(self, iUid)

	def title4(self, iUid):
		if iUid not in self.dIdNameValue:
			return "未上榜"
		args = self.dIdNameValue[iUid][4]
		com = args.get("com", 99)
		if com == 1:
			comTime = args.get("comTime", 9999) 
			return formatTime(comTime)
		elif com == 2:
			return '未答完'
		else:
			return '未参加'

	def getMyRankInfo(self, who):
		'''我的名次信息
		'''
		tMyInfo = []
		tMyInfo.append(self.getRank(who.id))
		tMyInfo.append(who.name)
		tMyInfo.append(role.defines.schoolList.get(who.school, ""))
		tMyInfo.append(self.title4(who.id))
		return tMyInfo

from common import *
import role.defines
