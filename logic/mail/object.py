# -*- coding: utf-8 -*-
import block
import pst
import sql
import jitKeeper

class MailBoxKeeper(jitKeeper.cJITproductKeeper):
	'''邮件管理器
	'''
	pass


class MailBox(block.cCtnBlock, pst.cEasyPersist):
	'''邮箱
	'''
	
	def __init__(self, roleId):
		block.cBlock.__init__(self, '邮箱数据', roleId)
		pst.cEasyPersist.__init__(self, self.__dirtyEventHandler)
		
		self.setIsStm(sql.MAIL_INSERT)
		self.setDlStm(sql.MAIL_DELETE)
		self.setUdStm(sql.MAIL_UPDATE)
		self.setSlStm(sql.MAIL_SELECT)

		self.ownerId = roleId
		self.inBoxMailList = {} # 收件箱
		
	def __dirtyEventHandler(self):
		import factoryConcrete
		factoryConcrete.mailBoxFtr.schedule2tail4save(self.ownerId)

	def save(self):
		data = {}
		data["data"] = pst.cEasyPersist.save(self)
		
		inBox = {}
		data["inBox"] = inBox
		for mailType in self.inBoxMailList:
			inBox[mailType] = {}
			for mailId, mailObj in self.inBoxMailList[mailType].iteritems():
				inBox[mailType][mailId] = mailObj.save()
		
		return data

	def load(self, data):
		if not data:
			return

		pst.cEasyPersist.load(self, data["data"])

		for mailType in data["inBox"]:
			self.inBoxMailList[mailType] = {}
			for mailId, mailData in data["inBox"][mailType].iteritems():
				mailObj = mail.newAndLoadMail(mailId, mailData)
				if mailObj.isExpired():  # 已过期
					self.markDirty()
				else:
					self.inBoxMailList[mailType][mailObj.id] = mailObj
					self.onAddMail(mailObj)
		
	def onAddMail(self, mailObj):
		mailObj.eDirtyEvent += self.__dirtyEventHandler
		mailObj.ownerId = self.ownerId
			
	def newMailId(self):
		'''生成一个邮件id
		'''
		lastMailId = self.fetch("lastMailId", 0)
		lastMailId += 1
		self.set("lastMailId", lastMailId)
		return lastMailId
	
	def getInMailCount(self):
		'''收件箱邮件数量
		'''
		count = 0
		for mailObjList in self.inBoxMailList.itervalues():
			count += len(mailObjList)
		return count
	
	def getInMailList(self):
		'''获取收件箱所有邮件
		'''
		mailList = {}
		for mailObjList in self.inBoxMailList.itervalues():
			mailList.update(mailObjList)
		return mailList
	
	def getInMail(self, mailId):
		'''获取收件箱邮件
		'''
		for mailObjList in self.inBoxMailList.itervalues():
			if mailId in mailObjList:
				return mailObjList[mailId]
		return None
	
	def addInMail(self, mailObj):
		'''收件箱增加邮件
		'''
		self.markDirty()
		
		mailType = mailObj.type
		if mailType not in self.inBoxMailList:
			self.inBoxMailList[mailType] = {}

		self.inBoxMailList[mailType][mailObj.id] = mailObj
		self.onAddMail(mailObj)
		mail.service.mailAdd(self.ownerId, mailObj)
		self.checkCountLimit(mailType)
		
	def delInMail(self, mailId, refresh=True):
		'''收件箱删除邮件
		'''
		mailObj = self.getInMail(mailId)
		if not mailObj:
			return
		
		self.markDirty()
		mailType = mailObj.type
		del self.inBoxMailList[mailType][mailId]
		mail.service.mailDelete(self.ownerId, mailObj)
		
	def checkCountLimit(self, mailType):
		'''检查邮件数上限
		'''
		cntLimit = countLimitList.get(mailType, 0)
		if not cntLimit: # 无限制
			return
		
		mailObjList = self.inBoxMailList[mailType]
		delCount = len(mailObjList) - cntLimit
		if delCount < 1: # 没超上限
			return
		
		tmpMailList = mailObjList.values()
		tmpMailList.sort(key=self._sortKeyForLimit)
		delObjList = tmpMailList[:delCount]
		for mailObj in delObjList:
			self.delInMail(mailObj.id)
		
	def _sortKeyForLimit(self, mailObj):
		lst = []
		
		if mailObj.isExpired(): # 已过期的
			lst.append(0)
		else:
			lst.append(1)
		
		if not mailObj.isProps() and mailObj.isReaded(): # 无附件且已阅读的
			lst.append(0)
		else:
			lst.append(1)
			
		if mailObj.isProps() and mailObj.isTaken(): # 有附件且已领取的
			lst.append(0)
		else:
			lst.append(1)
			
		if not mailObj.isProps(): # 无附件且未阅读的
			lst.append(0)
		else:
			lst.append(1)
			
		if mailObj.isProps() and mailObj.isReaded(): # 有附件且已阅读的
			lst.append(0)
		else:
			lst.append(1)
			
		lst.append(mailObj.sendTime)
		return lst
	
	def checkExpiredMail(self, refresh=True):
		'''检查过期邮件
		'''
		delList = []
		for mailObjList in self.inBoxMailList.itervalues():
			for mailObj in mailObjList.itervalues():
				if mailObj.isExpired():
					delList.append(mailObj.id)

		for mailId in delList:
			self.delInMail(mailId, refresh)


class Mail(pst.cEasyPersist):
	'''邮件
	'''
	
	def __init__(self, mailId):
		pst.cEasyPersist.__init__(self)

		self.id = mailId  # 邮件id
		self.type = MAIL_TYPE_SYS
		self.title = ""  # 标题
		self.content = ""  # 内容
		self.senderId = 0 # 发送人id
		self.sendTime = getSecond()  # 发送时间
		self.expiredTime = 0  # 过期时间，0表示永不过期
		self.propsList = []  # 附件物品
	
	def save(self):
		data = {}
		data["data"] = pst.cEasyPersist.save(self)
		
		data["type"] = self.type
		data["title"] = self.title
		data["content"] = self.content
		data["senderId"] = self.senderId
		data["sendTime"] = self.sendTime
		if self.expiredTime:
			data["expiredTime"] = self.expiredTime

		if self.propsList:
			propsList = []
			data["propsList"] = propsList
			for propsObj in self.propsList:
				propsList.append((propsObj.no(), propsObj.save()))
			
		return data
	
	def load(self, data):
		if not data:
			return

		pst.cEasyPersist.load(self, data["data"])
		
		self.type = data["type"]
		self.title = data["title"]
		self.content = data["content"]
		self.senderId = data["senderId"]
		self.sendTime = data["sendTime"]
		
		if data.get("expiredTime"):
			self.expiredTime = data["expiredTime"]
		
		if data.get("propsList"):
			for propsNo, propsData in data["propsList"]:
				propsObj = props.createAndLoad(propsNo, propsData)
				self.propsList.append(propsObj)

	def getSenderName(self):
		'''发送人名称
		'''
		name = self.fetch("senderName")
		if name:
			return name

		name = typeNameList.get(self.type)
		if not name:
			name = "未知发送人"
		return name
	
	def setSenderName(self, name):
		'''设置发送人名称
		'''
		self.set("senderName", name)
		
	def isReaded(self):
		'''是否已读
		'''
		if self.fetch("readed"):
			return True
		return False
	
	def setReaded(self):
		'''设置为已读
		'''
		self.set("readed", 1)
		self.attrChange("isReaded")
	
	def isTaken(self):
		'''是否已领取
		'''
		if self.fetch("taken"):
			return True
		return False
	
	def setTaken(self):
		'''设置为已收取
		'''
		self.set("taken", 1)
		self.attrChange("isTaken")

	def isExpired(self):
		'''邮件是否过期
		'''
		if self.expiredTime and self.expiredTime <= getSecond():
			return True
		return False
	
	def isProps(self):
		'''是否是有附件物品的邮件
		'''
		if self.propsList:
			return True
		return False
	
	def attrChange(self, *attrNameList):
		'''属性改变
		'''
		mail.service.mailChange(self.ownerId, self, *attrNameList)
	
	def getValByName(self, attrName):
		'''根据属性名获取属性值
		'''	
		return getValByName(self, attrName)
	
	def isNeedDelete(self):
		'''是否需要删除
		'''
		if self.type != MAIL_TYPE_SYS: # 只有系统邮件才有需要被删除
			return 0
		if self.isExpired(): # 过期的
			return 1
		if self.isProps() and not self.isTaken(): # 有附件但未领取的
			return 0
		return 1


from common import *
from mail.defines import *
import mail.service
import props