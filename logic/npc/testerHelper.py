#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import npc.object
#交易中间人
class cNpc(npc.object.cNpc):
	
	def __init__(self):
		npc.object.cNpc.__init__(self)
		self.name = "测试Npc"

	def doLook(self, who):
		ep = who.endPoint
		sQuestion='''can i help you?
Q我要元宝
Q我要钻石
Q我要道具
Q我要经验
Q我要体力
Q我要一套装备
Q我要一封系统邮件
Q我要在系统频道发言
Q我要清除次数限制
Q我要清空背包
Q我要接指定任务
Q我要返回至初始状态
Q我要解锁全部副本
Q我要升到指定等级
Q我要解锁全部主城
'''.format(who.name)
		bFail,uMsg=ep.rpcSelectBox(sQuestion)
		if bFail:
			return
		iSelect=uMsg.iValue		
		if iSelect==0:
			bFail,uMsg=ep.rpcInputBox('你要多少元宝?尽管说')
			if bFail:return
			sInput=uMsg.sValue
			if len(sInput)>19:
				ep.rpcTips('数值过大,请重试')
				return
			try:
				iAdd=int(sInput)
				who.addTradeCash(iAdd,'测试助手添加')
			except Exception:
				ep.rpcTips('只能输入数字')

		elif iSelect==1:
			bFail,uMsg=ep.rpcInputBox('你要多少钻石?尽管说')
			if bFail:return
			if len(uMsg.sValue)>10:
				ep.rpcTips('数值过大,请重试')
				return
			sInput=uMsg.sValue
			try:
				iAddDia=int(sInput)
				who.addDiamond(iAddDia,'测试助手添加')
			except Exception:
				ep.rpcTips('只能输入数字')

		elif iSelect==2:
			bFail,uMsg=ep.rpcInputBox('你要什么道具?请输入道具编号')
			if bFail:return
			oProps=props.new(int(uMsg.sValue))
			who.propsCtn.launchProps(oProps,'从测试npc处获取',False)

		elif iSelect==3:
			bFail,uMsg=ep.rpcInputBox('你要多少经验?尽管说')
			if bFail:return
			who.addExp(int(uMsg.sValue),'测试助手添加')
		elif iSelect==4:
			who.addRest(role.REST_MAX,'测试NPC')
			ep.rpcTips('体力补满了.')
		elif iSelect==5:
			sQuestion='''你要多少级的装备
Q一级装备一套
Q十级装备一套
Q二十级装备一套
Q三十级装备一套
Q四十级装备一套
Q五十级装备一套
Q六十级装备一套
Q七十级装备一套
Q八十级装备一套
Q九十级装备一套'''
			bFail,uMsg=ep.rpcSelectBox(sQuestion)
			if bFail:
				return
			iSelect=uMsg.iValue
			if iSelect==0:
				self.sendEquipByLv(who,1)
			elif iSelect==1:
				self.sendEquipByLv(who,10)
			elif iSelect==2:
				self.sendEquipByLv(who,20)
			elif iSelect==3:
				self.sendEquipByLv(who,30)
			elif iSelect==4:
				self.sendEquipByLv(who,40)
			elif iSelect==5:
				sQuestion='''你要什么品质的装备
Q五十级紫装
Q五十级橙装'''
				bFail,uMsg=ep.rpcSelectBox(sQuestion)
				if bFail:
					return
				if uMsg.iValue==0:
					self.sendEquipByLv(who,50,3)
				if uMsg.iValue==1:
					self.sendEquipByLv(who,50,4)
			elif iSelect==6:
				self.sendEquipByLv(who,60)
			elif iSelect==7:
				self.sendEquipByLv(who,70)
			elif iSelect==8:
				sQuestion='''你要什么品质的装备
Q八十级橙装
Q八十级红装'''
				bFail,uMsg=ep.rpcSelectBox(sQuestion)
				if bFail:
					return
				if uMsg.iValue==0:
					self.sendEquipByLv(who,80,4)
				if uMsg.iValue==1:
					self.sendEquipByLv(who,80,5)
			elif iSelect==9:
				self.sendEquipByLv(who,90)
		elif iSelect==6:
			bFail,uMsg=ep.rpcInputBox('请输入角色ID，0代表发给自己')
			if bFail:
				return 
			iRoleId=int(uMsg.sValue) if int(uMsg.sValue)!=0 else who.id#s输入0发给发给自己
			bFail,uMsg=ep.rpcInputBox('请输入邮件标题')
			if bFail:
				return 
			
			sTitle=uMsg.sValue
			bFail,uMsg=ep.rpcInputBox('请输入文本内容')
			if bFail:
				return
			sContent=uMsg.sValue
			bFail,uMsg=ep.rpcInputBox('请输入附件内容,0带表无附件.\n附件格式为“道具编号，数量|\n道具编号，数量|。。。')
			if bFail:
			 	return 
			lItems=[]#附件
			sAttachment=uMsg.sValue.split('|')
			for sTemp in  sAttachment:
			 	if int(sTemp[0])==0:
			 			lItems=[]
			 			break
			 	sTemp2=sTemp.split(',')
			 	if len(sTemp2)<2:
					ep.rpcTips('请输入正确的附件:\n附件格式为“道具编号，数量|\n道具编号，数量|。。。')
					return				
			 	iNo=int(sTemp2[0])
			 	iAmount=int(sTemp2[1])
			 	if iNo not in c.VIR_ITEM:#不是虚拟物品的情况
			 		oProp=props.new(iNo)
					iMaxStack=oProp.maxStack()
					iCounter=int(math.ceil(iAmount/float(iMaxStack)))
					for i in xrange(iCounter):
						oProp=props.new(iNo)
						iStack=iMaxStack if i<iCounter-1 else iAmount-iMaxStack*i
						oProp.setStack(iStack)
						lItems.append(oProp)
				 	continue
			 	# sTemp3=[]#是虚拟物品的情况
			 	# for  sNo in  sTemp2:
			 	# 	sTemp3.append(int(sNo))
			 	# sTemp3=tuple(sTemp3)
			 	lItems.append((iNo,iAmount))
			if iRoleId:
				mail.sendSysMail(iRoleId,sTitle,sContent,None,*tuple(lItems))
				ep.rpcTips('邮件发送成功')
		elif iSelect==7:
			pass
			# bFail,uMsg=ep.rpcInputBox('请输入聊天信息：')
			# if bFail:
			# 	return
			# oChatSysDown=chatRoom_pb2.chatSysDown()
			# oChatSysDown.iEndPoint=2
			# oChatSysDown.sContent=uMsg.sValue
			# for ep2 in mainService.gRoleIdMapEndPoint.getAll().itervalues():
			# 	ep2.rpcAnnounce(oChatSysDown)
			ep.rpcTips('已费用')
		elif iSelect==8:
			 who.day.clear()
		elif iSelect==9:
			bDelSucc=False
			for oProp in list(who.propsCtn.getAllValues(False)):
				 who.propsCtn.removeItem(oProp)
			ep.rpcTips('背包已清空')
		#接指定任务
		elif iSelect==10:
			bFail,uMsg=ep.rpcInputBox('请输入任务编号')
			if bFail:
				return
			iTaskNo=int(uMsg.sValue)  #要领取的任务编号
			if iTaskNo not in  taskData.gdData.iterkeys():
				ep.rpcTips('任务编号不存在')
				return	

			who.taskCtn.lFinishTask=[]   #已完成任务列表,提交之后的任务会记录在这里,存盘
			who.taskCtn.dNPCAcceptedTaskList={}  #NPC可接任务列表,上线或者条件发生变化时候更新.{npc编号:{任务类型:[任务编号1,任务编号2...]}}
			who.taskCtn.dNPCFinishedTaskList={}  #NPC可完成列表,任务达到完成状态的时候更新
			who.taskCtn.dDialog={}
			for obj in who.taskCtn.getAllValues():
				if obj.getConfig('tasktype')==block.blockTask.TASK_MAIN:
					who.taskCtn.removeItem(obj)

			for i,dData in taskData.gdData.iteritems():
				otask=who.taskCtn.getItem(i)
				if otask:
					otask.setFinish()	
					who.taskCtn.submitTask(otask.key)
					continue
				if 	i>=	iTaskNo	:
					continue
				if taskData.getConfig(i,"event")=="TASK":
					for j in taskData.getConfig(i,"condition").keys():
						who.taskCtn.acceptTask(j)
						otask=who.taskCtn.getItem(j)
						otask.setFinish()
						who.taskCtn.submitTask(otask.key)
				who.taskCtn.acceptTask(i)
				otask=who.taskCtn.getItem(i)
				otask.setFinish()	
				who.taskCtn.submitTask(otask.key)


			who.taskCtn.acceptTask(iTaskNo)		
			oScene=scene.gSceneProxy.getProxy(who.active.getSceneId())
			who.taskCtn.sendNPCStatusTheScene(oScene)
			ep.rpcTips('任务接收成功')
		elif iSelect==11:
			who.set("level", 1)
			who.exp = 0
			who.tradeCash = 0
			who.accountObj.accountMf.iDiamond=0
			who.reCalcAttr()
			bFail=ep.rpcAvatarAttrChange(**role.roleHelper.makeAttrInitMsg(who))
			for oEquip in who.propsCtn.getWearEquipGroup():
				who.propsCtn.removeItem(oEquip)
			ep.rpcTips('成功返回至初始状态')
		elif iSelect==12:
			for iNo in barrierData.gdData:
				who.barrier.setLockBarrier(iNo,1)
			ep.rpcTips('解锁成功')		
		elif iSelect==13:#升到指定等级
			bFail,uMsg=ep.rpcInputBox('请问你要改到多少级？？')
			if bFail:
				return
			iLv=int(uMsg.sValue)
			iNeedExp=0
			if iLv>=who.level:
				for i in xrange(iLv-who.level):
					iNeedExp+=roleAttrData.getConfig(who.level+i,'exp')
				iNeedExp-=who.exp
				who.addExp(iNeedExp,'测试助手添加')
			else:
				who.set("level", 1)
				who.exp = 0
				if iLv==1:
					who.reCalcAttr()
					bFail=ep.rpcAvatarAttrChange(**role.roleHelper.makeAttrInitMsg(who))
					return
				for i in xrange(iLv):
					iNeedExp+=roleAttrData.getConfig(i+1,'exp')
				iNeedExp-=roleAttrData.getConfig(iLv,'exp')
				who.addExp(iNeedExp,'测试助手更改')
			ep.rpcTips('恭喜，等级更改成功')
		elif iSelect==14:#解锁全部主城
			lAnpa=list(mapData.gdData.keys())
			who.active.set('anpa', lAnpa)	
			ep.rpcTips('解锁全部主城成功')

	def sendEquipByLv(self,who,level,iColor=0):
		lEquip=[]
		for iKey,dValue in equipData.gdData.iteritems():
			if dValue.get('等级')!=level:
				continue
			if iColor!=0:
				if  dValue.get('color')!=iColor:
					continue
			if dValue.get('school')==0 or dValue.get('school')==who.school:
				lEquip.append(iKey)
		for  iNo in  lEquip:
			 oProp=props.new(iNo)
			 who.propsCtn.launchProps(oProp,'测试助手添加装备')

	def menuName(self):
		return '测试NPC'


import math
import u
import misc
import c
import log
import role
import props
import equipData
import instruction.forAny
import mail
import taskData
import block.blockTask
import role.roleHelper
import instruction.switch
import task

import scene
import roleAttrData
