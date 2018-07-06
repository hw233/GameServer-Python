# -*- coding: utf-8 -*-
'''活动相关指令
'''
import instruction

@instruction.properties(sn='act')
def testActivity(who, activityName, cmdIdx, *args):
	'''测试活动
	'''
	activityObj = activity.getActivity(activityName)
	if not activityObj:
		message.tips(who, "活动#C02%s#n不存在" % activityName)
		return
	activityObj.testCmd(who, cmdIdx, *args)
	# message.tips(who, "OK")
		
import activity
import message