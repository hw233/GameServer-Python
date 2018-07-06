#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import npc.object

class cNpc(npc.object.cNpc):
	
	def __init__(self):
		npc.object.cNpc.__init__(self)
		self.name = "导表Npc"

	def doLook(self,who):#override 被触碰了
		pid = who.id
		lTable=[]
		lFunc=[]
		for func in makeData.getAllMethod():
			if not func.func_doc:#没有设置函数的doc
				continue
			sName='{} {}'.format(func.func_doc,func.func_name)
			lTable.append(sName)
			lFunc.append(func)
		iRes=message.selectBox(who,'你要导什么表呢??\nQ'+'\nQ'.join(lTable), self)
		if not iRes:
			return
		who=getRole(pid)
		if not who:
			return

		ep = who.endPoint
		instruction.forAny.update(ep)#从svn服务器拿最新的数据
		try:
			lFunc[iRes-1](ep)#执行某个导表
		except BaseException,e:
			u.reRaise('{}数据异常'.format(lTable[iRes-1]))
		else:
			instruction.forAny.commit(ep)#生成后数据提交到svn服务器


	def menuName(self):
		return '导表'

from common import *
import u
import misc
import c
import log
import makeData
import instruction
import instruction.forAny
import message