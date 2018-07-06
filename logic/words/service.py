# -*- coding: utf-8 -*-
# 闲话服务
import endPoint
import words_pb2

class cService(words_pb2.terminal2main):

	@endPoint.result
	def rpcWordsGet(self, ep, who, reqMsg): return rpcWordsGet(who, reqMsg)

	@endPoint.result
	def rpcWordsSet(self, ep, who, reqMsg): return rpcWordsSet(who, reqMsg)

	@endPoint.result
	def rpcWordsReset(self, ep, who, reqMsg): return rpcWordsReset(who, reqMsg)
	
def rpcWordsGet(who, reqMsg):
	'''获取闲话
	'''
	entityType = reqMsg.type
	entityNo = reqMsg.entity
	if not 1 <= entityType <= 2:
		return
	msg = packetMsg(who,entityType, entityNo)
	who.endPoint.rpcWordsList(msg)

def rpcWordsSet(who, reqMsg):
	'''设置闲话
	'''
	entityType = reqMsg.type
	entityNo = reqMsg.entity
	wordsEvent = reqMsg.msg.event
	wordsMsg = reqMsg.msg.content
	if not 1 <= entityType <= 2:
		return
	if not 1<=wordsEvent<=8:
		return
	if calLenForWord(wordsMsg) > 20:
		return
	if "*" in trie.fliter(wordsMsg):
		message.tips(who, "输入内容中有不合法的词汇，请重新输入")
		return
	who.words.setWords(entityType,entityNo,wordsEvent,wordsMsg)
	who.endPoint.rpcWordsMod(reqMsg)

def rpcWordsReset(who, reqMsg):
	'''重置闲话
	'''
	entityType = reqMsg.type
	entityNo = reqMsg.entity
	if not 1 <= entityType <= 2:
		return
	who.words.delWords(entityType,entityNo)
	msg = packetMsg(who,entityType, entityNo)
	who.endPoint.rpcWordsList(msg)


def packetMsg(who, entityType, entityNo):
	'''打包消息
	'''
	msg = words_pb2.wordsList()
	msg.type = entityType
	msg.entity = entityNo

	for event in eventByEntityType[entityType]:
		content = msg.msgList.add()
		content.event = event
		content.content = who.words.getWords(entityType,entityNo,event)

	return msg

from common import *
import trie
import message

eventByEntityType = {
	1:[1,2,3,4,6,7,8],
	2:[1,2,3,5,8],
}