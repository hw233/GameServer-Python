# -*- coding: utf-8 -*-


#打开客户端界面
#iLinkId:界面连接id(dtViewLink中的id)
#sPbName:protod消息定义结构（例如：common_pb.reloginMsg)
#sSerialized:信息序列化后的字节流	
def rpcOpenUIPanel(who, iLinkId, sPbName="", argsMsg=None):
	# if iLinkId not in ViewLinkData.gdData:
	# 	raise Exception, "打开客户端界面连接{}不存在".format(iLinkId)
		# return
	
	msg = makeUiPanelMsg(iLinkId, sPbName, argsMsg)
	who.endPoint.rpcOpenUIPanel(msg)

def makeUiPanelMsg(iLinkId, sPbName="", argsMsg=None):
	msg = common_pb2.uiPanelMsg()
	msg.iLinkId = iLinkId
	msg.sPbName = sPbName
	if argsMsg:
		msg.sSerialized = argsMsg.SerializeToString()
	return msg

def makeUiPanelPacket(rpcName, iLinkId, sPbName="", argsMsg=None):
	msg = makeUiPanelMsg(iLinkId, sPbName, argsMsg)
	return endPoint.makePacket(rpcName, msg)

#================================
def commonInt32Msg(iValue):
	msg = common_pb2.int32_()
	msg.iValue = iValue
	return msg

def commonInt64Msg(iValue):
	msg = common_pb2.int64_()
	msg.iValue = iValue
	return msg

def commonUInt32Msg(iValue):
	msg = common_pb2.uin32_()
	msg.iValue = iValue
	return msg

def commonBytesMsg(sValue):
	msg = common_pb2.bytes_()
	msg.sValue = sValue
	return msg

def commonBoolMsg(bValue):
	msg = common_pb2.bool_()
	msg.bValue = bValue
	return msg

def commonFloatMsg(fValue):
	msg = common_pb2.float_()
	msg.fValue = fValue
	return msg

def commonDoubleMsg(fValue):
	msg = common_pb2.double_()
	msg.fValue = fValue
	return msg
#================================


def openPetRewardUi(who, petId):
	'''打开获得宠物界面
	'''
	rpcOpenUIPanel(who, 12, "common_pb.int64_", commonInt64Msg(petId))

def openAnswerProblem(who):
	'''打开每日界面
	'''
	rpcOpenUIPanel(who, 13)

def answerQuickProblemPacket(rpcName, sPbName, msg):
	'''抢答题目
	'''
	return makeUiPanelPacket(rpcName, 13, sPbName, msg)

def openRankUi(who, iRankNo):
	import rank_pb2
	msg = rank_pb2.lookInfo()
	msg.iRankNo = iRankNo
	msg.iUid = 0
	rpcOpenUIPanel(who, 8, "rank_pb.lookInfo", msg)

def openTSSellUI(who, iStallId):
	'''珍品阁出售界面
	'''
	msg = treasureShop.service.packGoodsInfo(who,iStallId,False)
	rpcOpenUIPanel(who, 15, "treasureShop_pb.goodsInfo", msg)	

def openTSBuyUI(who, iStallId):
	'''珍品阁购买界面
	'''
	msg = treasureShop.service.packGoodsInfo(who,iStallId,False)
	rpcOpenUIPanel(who, 16, "treasureShop_pb.goodsInfo", msg)


def openCommonTips(who, iTipsId):
	'''打开通用tips界面
	'''
	rpcOpenUIPanel(who, 55, "common_pb.int32_", commonInt32Msg(iTipsId))


from common import *
import common_pb2
import ViewLinkData
import endPoint
import treasureShop.service
