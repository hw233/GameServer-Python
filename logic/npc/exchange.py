#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import npc.object
#交易中间人
class cNpc(npc.object.cNpc):
	
	def doLook(self, who):
		content = self.getChat()
		content +='''
Q查看商品
Q路过'''
		message.selectBoxNew(who, self.responseLook, content, self)
		
	def responseLook(self, who, selectNo):
		if selectNo == 1:
			who.endPoint.rpcOpenUIPanel(6)
	
import message