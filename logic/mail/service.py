# -*- coding: utf-8 -*-
'''邮件服务
'''
import endPoint
import mail_pb2

class cService(mail_pb2.terminal2main):
	
	@endPoint.result
	def rpcMailReadDetail(self, ep, who, reqMsg): return rpcMailReadDetail(who, reqMsg)

	@endPoint.result
	def rpcMailDelete(self, ep, who, reqMsg): return rpcMailDelete(who, reqMsg)
	
	@endPoint.result
	def rpcMailDeleteOneKey(self, ep, who, reqMsg): return rpcMailDeleteOneKey(who, reqMsg)
	
	@endPoint.result
	def rpcMailTakeProps(self, ep, who, reqMsg): return rpcMailTakeProps(who, reqMsg)

def rpcMailReadDetail(who, reqMsg):
	'''读取邮件详情
	'''
	mailId = reqMsg.mailId
	mailBoxObj = mail.getMailBox(who.id)
	mailObj = mailBoxObj.getInMail(mailId)
	if not mailObj:
		return
	if mailObj.isExpired():
		mailBoxObj.delInMail(mailId)
		message.tips(who, "该邮件已过期")
		return
	
	if not mailObj.isReaded():
		mailObj.setReaded()
	mailDetail(who, mailObj)
	
def rpcMailDelete(who, reqMsg):
	'''删除邮件
	'''
	mailId = reqMsg.mailId
	mailBoxObj = mail.getMailBox(who.id)
	mailObj = mailBoxObj.getInMail(mailId)
	if not mailObj:
		return
	if mailObj.type != MAIL_TYPE_SYS: # 只有系统删除才能删除
		return
	mailBoxObj.delInMail(mailId)

def rpcMailDeleteOneKey(who, reqMsg):
	'''一键删除邮件
	'''
	mailBoxObj = mail.getMailBox(who.id)
	mailList = mailBoxObj.getInMailList()
	
	delList = []
	for mailId, mailObj in mailList.iteritems():
		if mailObj.isNeedDelete():
			delList.append(mailId)
	
	for mailId in delList:
		mailBoxObj.delInMail(mailId)

def rpcMailTakeProps(who, reqMsg):
	'''收取邮件附件物品
	'''
	mailId = reqMsg.mailId
	mailBoxObj = mail.getMailBox(who.id)
	mailObj = mailBoxObj.getInMail(mailId)
	if not mailObj:
		return
	if not mailObj.isProps(): # 没有附件物品
		return
	if mailObj.isExpired():
		mailBoxObj.delInMail(mailId)
		message.tips(who, "该邮件已过期")
		return
	if mailObj.isTaken(): # 不可重复收取
		return
	if not who.propsCtn.validCapacityByObj(mailObj.propsList):
		message.tips(who, "包裹已满，请清理包裹才能收取附件物品")
		return
	
	mailObj.setTaken()
	for propsObj in mailObj.propsList:
		launch.launchProps(who, propsObj, "邮件", None)
	


#===============================================================================
# 服务端发往客户端
#===============================================================================
def packetMailDetail(mailObj):
	'''邮件详情
	'''
	msgObj = mail_pb2.mailMsg()
	msgObj.mailId = mailObj.id
	msgObj.content = mailObj.content
	msgObj.senderName = mailObj.getSenderName()
	
	if mailObj.propsList:
		propsList = []
		for propsObj in mailObj.propsList:
			propsMsg = propsObj.getMsg4Package(None, *propsObj.MSG_ALL)
			propsList.append(propsMsg)
		msgObj.propsList.extend(propsList)
		
	return msgObj

def packetMailSummary(mailObj):
	'''邮件摘要
	'''
	msgObj = mail_pb2.mailMsg()
	msgObj.mailId = mailObj.id
	msgObj.type = mailObj.type
	msgObj.title = mailObj.title
	msgObj.sendTime = mailObj.sendTime
	msgObj.expiredTime = mailObj.expiredTime
	msgObj.isReaded = mailObj.isReaded()
	msgObj.isTaken = mailObj.isTaken()
	msgObj.isProps = mailObj.isProps()
		
	return msgObj

def mailListAll(who):
	'''所有邮件信息
	'''
	mailBoxObj = mail.getMailBox(who.id)
	mailBoxObj.checkExpiredMail(False)

	mailList = []
	for mailObj in mailBoxObj.getInMailList().itervalues():
		mailList.append(packetMailSummary(mailObj))

	msgObj = mail_pb2.mailAllMsg()
	msgObj.mailList.extend(mailList)
	who.endPoint.rpcMailListAll(msgObj)
	
def mailDetail(who, mailObj):
	'''邮件详情
	'''
	msgObj = packetMailDetail(mailObj)
	who.endPoint.rpcMailDetail(msgObj)

def mailAdd(roleId, mailObj):
	'''增加邮件
	'''
	who = getRole(roleId)
	if not who:
		return

	msgObj = packetMailSummary(mailObj)
	who.endPoint.rpcMailAdd(msgObj)
	
def mailDelete(roleId, mailObj):
	'''删除邮件
	'''
	who = getRole(roleId)
	if not who:
		return

	who.endPoint.rpcMailDelete(mailObj.id)
	
def mailChange(roleId, mailObj, *attrNameList):
	'''修改邮件
	'''
	who = getRole(roleId)
	if not who:
		return
	
	msg = {
		"mailId": mailObj.id,
	}

	for attrName in attrNameList:
		msg[attrName] = mailObj.getValByName(attrName)

	who.endPoint.rpcMailChange(**msg)


from common import *
from mail.defines import *
import mail
import launch
import message
