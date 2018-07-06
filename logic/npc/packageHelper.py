#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import npc.object
class cNpc(npc.object.cNpc):
	
	def __init__(self):
		npc.object.cNpc.__init__(self)
		self.name = "包裹物品Npc"
		self.shape = 1111

	def doLook(self, who):
		pid = who.id
		sInput = message.inputBox(who, "请输入要查看的物品座位号,装备孔从1开始,普通物品区从20开始,装备专区从200开始")
		if not sInput:
			return
		
		who = getRole(pid)
		if not who:
			return
		
		if not sInput.isdigit():
			message.tips(who, "请输入数字")
			return
		
		iPos=int(sInput)

		itemobj=who.ItemCtn.GetItemByPos(iPos)
		if not itemobj:
			self.say(who, '{}号座位没有物品'.format(iPos))
			return
		str=""
		l=[]
		for k,v in itemobj.dData.iteritems():
			l.append("%s=%s"%(k,v,))
		if l:
			sText=("{}座位号是{},已有属性",iPos,itemobj.Name())+",".join(l)+","
		else:
			sText=("{}座位号是{},",iPos,itemobj.Name())

		uio.G2CInputBox(who.id,("{}要修改属性,请按  属性名=属性值  的格式输入,修改多个属性用;分隔",sText))


		itemobj=who.ItemCtn.GetItemByPos(iPos)
		if not itemobj:
			self.Say(who,("{}号座位没有物品",iPos))
			return
		for nameval in sInput.split(";"):
			if not nameval:
				continue
			sName,sValue=nameval.split("=")
			itemobj.Set(sName,int(sValue))
		item.net.G2CItemResume(who.id,itemobj)
		item.net.G2CItemDetail(who.id,itemobj)
		#who.ItemCtn.Sort()#不管会不会引起座位变化,都排一下序
		notify.G2CNotify(who.id,("修改物品属性成功"))


	def menuName(self):
		return '装备'

from common import *
import u
import misc
import c
import log
import makeData
import role
import message