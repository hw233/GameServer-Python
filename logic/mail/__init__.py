# -*- coding: utf-8 -*-
	
def getMailBox(roleId):
	'''获取邮箱
	'''
	import factory
	return mailBoxKeeper.getObjFromDB(factory.NO_ROW_INSERT_PRIME_KEY, roleId)

def newMail(mailId, mailType, title, content, propsObjList, validTime):
	'''新建邮件
	'''
	mailObj = mail.object.Mail(mailId)
	mailObj.type = mailType
	mailObj.title = title
	mailObj.content = content
	if propsObjList:
		mailObj.propsList = propsObjList
	if validTime:
		mailObj.expiredTime = getSecond() + validTime
	return mailObj

def newAndLoadMail(mailId, mailData):
	'''根据数据新建邮件
	'''
	mailObj = mail.object.Mail(mailId)
	mailObj.load(mailData)
	return mailObj

def _addMail(roleId, mailType, title, content, propsObjList=None, validTime=0):
	'''发送邮件
	'''
	mailBoxObj = getMailBox(roleId)
	mailId = mailBoxObj.newMailId()
	mailObj = newMail(mailId, mailType, title, content, propsObjList, validTime)
	mailBoxObj.addInMail(mailObj)
	return mailObj

def sendSysMail(roleId, title, content, propsObjList=None, validTime=0):
	'''发送系统邮件
	'''
	return _addMail(roleId, MAIL_TYPE_SYS, title, content, propsObjList, validTime)

def sendGuildMail(roleId, title, content, propsObjList=None, validTime=0):
	'''发送仙盟邮件
	'''
	return _addMail(roleId, MAIL_TYPE_GUILD, title, content, propsObjList, validTime)

def sendTradeMail(roleId, title, content, propsObjList=None, validTime=0):
	'''发送交易邮件
	'''
	return _addMail(roleId, MAIL_TYPE_TRADE, title, content, propsObjList, validTime)


from common import *
from mail.defines import *
import mail.object

if 'mailBoxKeeper' not in globals():
	import factoryConcrete
	mailBoxKeeper = mail.object.MailBoxKeeper(factoryConcrete.mailBoxFtr)
