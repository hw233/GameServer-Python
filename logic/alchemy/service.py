#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import alchemy_pb2
import endPoint
import misc

class cService(alchemy_pb2.terminal2main):

	@endPoint.result
	def rpcAlchemyOpen(self, ep, who, reqMsg): return rpcAlchemyOpen(who, reqMsg)

	@endPoint.result
	def rpcAlchemyClick(self, ep, who, reqMsg): return rpcAlchemyClick(who, reqMsg)

	@endPoint.result
	def rpcAlchemyGet(self, ep, who, reqMsg): return rpcAlchemyGet(who, reqMsg)

	@endPoint.result
	def rpcAlchemyOneKey(self, ep, who, reqMsg): return rpcAlchemyOneKey(who, reqMsg)

	@endPoint.result
	def rpcArtificeOpen(self, ep, who, reqMsg): return rpcArtificeOpen(who, reqMsg)

	@endPoint.result
	def rpcArtificeProps(self, ep, who, reqMsg): return rpcArtificeProps(who, reqMsg)


def rpcAlchemyOpen(who, reqMsg):
	'''打开炼丹界面
	'''
	sendAlchemy(who)

def rpcAlchemyClick(who, reqMsg):
	'''点击物品
	'''
	propsNo = reqMsg.propsNo
	if propsNo not in (221402,202024,202025,230012):
		return
	obj = who.alchemyCtn.getAlchemy(propsNo)
	getCnt = getGainCnt(who,obj)
	if getCnt:
		getProps(who,propsNo,obj,getCnt)  #领取
	else:
		alchemyProps(who,propsNo,obj)  #炼化

def rpcAlchemyGet(who, reqMsg):
	'''一键领取
	'''
	for propsNo,obj in who.alchemyCtn.getAllAlchemy():
		getCnt = getGainCnt(who,obj)
		if not getCnt:
			continue
		if not getProps(who,propsNo,obj,getCnt,False):
			return
	sendAlchemy(who)

def rpcAlchemyOneKey(who, reqMsg):
	'''一键炼丹
	'''
	bFull = True
	for propsNo in (221402,202024,202025,230012):
		alchemy = who.alchemyCtn.getAlchemy(propsNo)
		if alchemy:
			continue
		if who.alchemyCtn.getAnima()<ALCHEMY_ANIMA:
			message.tips(who,"你的灵气不足，请先炼化足够的灵气")
			sendAlchemy(who)
			return
		who.alchemyCtn.addAnima(-ALCHEMY_ANIMA)
		obj = who.alchemyCtn.addAlchemy(propsNo)
		obj.set("time",getSecond())
		obj.set("cnt",1)

	for propsNo,obj in who.alchemyCtn.getAllAlchemy():
		if obj.fetch("cnt")>=2:
			continue
		if who.alchemyCtn.getAnima()<ALCHEMY_ANIMA:
			message.tips(who,"你的灵气不足，请先炼化足够的灵气")
			sendAlchemy(who)
			return
		who.alchemyCtn.addAnima(-ALCHEMY_ANIMA)
		obj.set("cnt",2)
		bFull = False

	if not bFull:
		sendAlchemy(who)
	else:
		message.tips(who,"每种道具最多进行#C042个#n炼丹")

def rpcArtificeOpen(who, reqMsg):
	'''打开炼化界面
	'''
	who.endPoint.rpcArtificeInfo(who.getAnima())

def rpcArtificeProps(who, reqMsg):
	'''炼化物品
	'''
	allAnima = 0
	for msg in reqMsg.propsList:
		propsId = msg.propsId
		stack = msg.stack
		propsObj = who.propsCtn.getItem(propsId)
		if not propsObj or propsObj.stack() < stack:
			continue
		allAnima += artificeProps(who,propsObj,stack)
	if allAnima:
		anima = who.alchemyCtn.addAnima(allAnima)
		who.endPoint.rpcAnimaMod(anima)

def alchemyProps(who,propsNo,obj):
	'''炼丹
	'''
	if obj:
		if obj.fetch("cnt") == 2:
			message.tips(who,"每种道具最多进行#C042个#n炼丹")
			return
		cnt = 2
	else:
		cnt = 1

	if who.alchemyCtn.getAnima() < ALCHEMY_ANIMA:
		message.tips(who,"你的灵气不足，请先炼化足够的灵气")
		return

	anima = who.alchemyCtn.addAnima(-ALCHEMY_ANIMA)
	if not obj:
		obj = who.alchemyCtn.addAlchemy(propsNo)
		obj.set("time",getSecond())
	obj.set("cnt",cnt)
	who.endPoint.rpcAlchemyMod(packAlchemy(propsNo,obj))
	who.endPoint.rpcAnimaMod(anima)

def getProps(who,propsNo,obj,getCnt,bRPC=True):
	'''领取
	'''
	if not who.propsCtn.leftCapacity():
		message.tips(who,"背包已满")
		return False
	launch.launchBySpecify(who,propsNo,getCnt,True,"炼丹",None)

	cnt = obj.fetch("cnt")
	time = obj.fetch("time")
	if getCnt == cnt:
		who.alchemyCtn.removeAlchemy(propsNo)
		if bRPC:
			who.endPoint.rpcAlchemyDel(propsNo)
	else:
		obj.set("cnt",cnt-getCnt)
		obj.set("time",time+ALCHEMY_TIME*getCnt)
		if bRPC:
			who.endPoint.rpcAlchemyMod(packAlchemy(propsNo,obj))
	return True

def artificeProps(who,propsObj,stack):
	'''炼化
	'''
	anima = propsObj.getAnima()
	if not anima:
		return anima
	who.propsCtn.addStack(propsObj,-stack)
	return stack*anima

def sendAlchemy(who):
	'''发送炼丹信息
	'''
	msg = {}
	msg["anima"] = who.alchemyCtn.getAnima()
	msg["propsList"] = [packAlchemy(propsNo,obj) for propsNo,obj in who.alchemyCtn.getAllAlchemy()]

	who.endPoint.rpcAlchemyInfo(**msg)

def getGainCnt(who,obj):
	'''可领取数量
	'''
	if not obj:
		return 0
	cnt = obj.fetch("cnt")
	time = obj.fetch("time")
	getCnt = min(cnt,(getSecond()-time)/ALCHEMY_TIME)
	return getCnt

def packAlchemy(propsNo,obj):
	'''打包炼丹物品
	'''
	crossTime = getSecond() - obj.fetch("time")
	getCnt = crossTime/ALCHEMY_TIME
	cnt = obj.fetch("cnt")
	msgObj = alchemy_pb2.alchemyProps()
	msgObj.propsNo = propsNo
	msgObj.time = 0 if getCnt>0 else ALCHEMY_TIME-crossTime
	msgObj.getCnt = min(getCnt,cnt)
	msgObj.maxCnt = cnt
	
	return msgObj

from common import *
import message
import launch


ALCHEMY_TIME=60*60*4
ALCHEMY_ANIMA=100