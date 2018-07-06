#coding:utf-8
'''
角色系统设置相关
'''
def getLockStatus(who):
	'''获取安全锁的状态
	'''
	if not isLockSet(who):
		return 0#未设置锁
	elif who.fetch("lockForceUnlock"):
		return 3#时间强行解锁
	elif who.fetch("lockLock"):
		if getattr(who, "lockUnlock", False):
			return 2
		return 1#上锁
	else:
		return 2#未上锁

def clearLock(who):
	'''清除角色安全锁
	'''
	who.delete("lockLock")
	who.delete("lockPwd")
	who.delete("lockForceUnlock")

def getForceUnlockTime(who):
	'''获取强行解锁的时间
	'''
	iApplyTime = who.fetch("lockForceUnlock")
	if not iApplyTime:
		return (0, 0)
	iEndTime = iApplyTime + 3600 * 24 * 5
	return (iApplyTime, iEndTime)

def checkForceUnlockTime(who):
	'''检测时间强行解锁到期与否
	'''
	iApplyTime, iEndTime = getForceUnlockTime(who)
	if not iApplyTime:
		return
	if timeU.getStamp() > iEndTime:
		# 检查这五内天的活跃度
		for i in xrange(0, -5, -1):
			if who.day.fetch("actPoint", iWhichCyc=i) < 120:
				who.delete("lockForceUnlock")
				message.tips(who, "不符合时间审核的要求，解除安全锁失败")
				return
		clearLock(who)
		message.tips(who, "时间审核期已结束，成功解除安全锁")

def isLockSet(who):
	'''是否设置了安全锁
	'''
	if who.fetch("lockPwd"):
		return True
	return False

def isLock(who):
	'''是否在安全锁的保护中
	'''
	# 没有设置安全锁肯定不在保护中
	if not isLockSet(who):
		return False
	# 设置安全锁后还要上锁才在保护中
	if who.fetch("lockLock"):
		# 上锁解锁过
		if getattr(who, "lockUnlock", False):
			return False
		else:
			return True
	return False

def lockSet(who, oMsg):
	'''设置安全锁
	'''
	if isLockSet(who):
		message.tips(who, "你已经设置过安全锁了")
		return False
	# 要不要转成MD5保存？
	sPwd = oMsg.sPassword
	iLen = calLen(sPwd)
	if not sPwd or not (4 <= iLen <= 12) or not sPwd.isalnum():
		message.tips(who, "密码应为#C044~12#n位的#C04数字或字母#n组成，请检查输入是否正确")
		return False
	who.set("lockPwd", sPwd)
	message.tips(who, "密码设置成功，请记牢新密码")
	return True

def lockModify(who, oMsg):
	'''修改密码
	'''
	if not isLockSet(who):
		message.tips(who, "请先设置安全锁")
		return False
	if who.fetch("lockForceUnlock"):
		message.tips(who, "时间解锁审核期间无法进行修改密码操作")
		return False
	sPwd = oMsg.sPassword
	sOldPwd = oMsg.sOldPwd
	iLen = calLen(sPwd)
	if not sPwd or not (4 <= iLen <= 12) or not sPwd.isalnum():
		message.tips(who, "密码应为#C044~12#n位的#C04数字或字母#n组成，请检查输入是否正确")
		return False
	if sOldPwd != who.fetch("lockPwd"):
		message.tips(who, "原密码错误")
		return False
	who.set("lockPwd", sPwd)
	message.tips(who, "密码修改成功，请记牢新密码")
	return True

def lockLock(who, oMsg):
	'''上锁
	'''
	if not isLockSet(who):
		message.tips(who, "请先设置安全锁")
		return False
	if who.fetch("lockLock") == 1:
		if getattr(who, "lockUnlock", False):
			setattr(who, "lockUnlock", False)
		else:
			message.tips(who, "已经上锁过了")
			return False
	else:
		who.set("lockLock", 1)
	message.tips(who, "安全锁上锁成功")
	return True

def lockUnlock(who, oMsg):
	'''解锁
	'''
	if not isLockSet(who):
		message.tips(who, "请先设置安全锁")
		return False
	if who.fetch("lockForceUnlock"):
		message.tips(who, "时间解锁审核期间无法进行修改密码操作")
		return False
	if who.fetch("lockLock") != 1:
		message.tips(who, "你还未上过锁")
		return False
	sPwd = oMsg.sPassword
	if sPwd != who.fetch("lockPwd"):
		message.tips(who, "密码错误")
		return False
	# who.set("lockLock", 0)
	setattr(who, "lockUnlock", True) # 这个不存盘，用来判断是否解过锁
	# 人物下线是否需要再上锁？
	message.tips(who, "安全锁解除成功")
	return True

def lockTimeForceUnlock(who, oMsg):
	'''时间强行解锁
	'''
	if not isLockSet(who):
		message.tips(who, "请先设置安全锁")
		return False
	if who.fetch("lockLock") != 1:
		message.tips(who, "你还未上过锁")
		return False
	if who.fetch("lockForceUnlock"):
		message.tips(who, "你已经申请过时间解锁了")
		return False
	who.set("lockForceUnlock", int(timeU.getStamp()))
	return True

def lockCancelUnlock(who, oMsg):
	'''取消强行解锁
	'''
	if not isLockSet(who):
		message.tips(who, "请先设置安全锁")
		return False
	who.delete("lockForceUnlock")
	return True

def handleSecurityLock(who, iOpType, oMsg):
	'''安全锁相关操作
	'''
	handleFunc = dLockHandler.get(iOpType)
	if not handleFunc:
		return False
	return handleFunc(who, oMsg)


# 1设置，2修改，3上锁，4解锁，5时间强行解锁，6取消时间强行解锁
dLockHandler = {
1:lockSet,
2:lockModify,
3:lockLock,
4:lockUnlock,
5:lockTimeForceUnlock,
6:lockCancelUnlock,
}


import message
from common import *
import timeU
