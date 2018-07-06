#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import terminal_main_pb2
import endPoint
import c
#各种超链接

class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	def rpcRoleHyperLink(self,ep,who,reqMsg):return rpcRoleHyperLink(self,ep,who,reqMsg)
	@endPoint.result
	def rpcPropsHyperLink(self,ep,who,reqMsg):return rpcPropsHyperLink(self,ep,who,reqMsg)
	@endPoint.result
	def rpcTaskHyperLink(self,ep,who,reqMsg):return rpcTaskHyperLink(self,ep,who,reqMsg)
	@endPoint.result
	def rpcTitleHyperLink(self,ep,who,reqMsg):return rpcTitleHyperLink(self,ep,who,reqMsg)
	@endPoint.result
	def rpcCommonPropsHyperLink(self,ep,who,reqMsg):return rpcCommonPropsHyperLink(self,ep,who,reqMsg)
	@endPoint.result
	def rpcChatProps(self,ep,who,reqMsg):return rpcChatProps(self,ep,who,reqMsg)

glChatShowPanel = []	#c.EQUIP_PANNEL, c.PROPS_PANNEL 聊天能显示的物品面板集合
def rpcChatProps(self,ep,who,reqMsg):
	oPropsList=props_pb2.propsList()
	lPos=who.propsCtn.dPosMapProps.keys()
	lPos.sort()
	for iPos in lPos:
		oEquip=who.propsCtn.dPosMapProps.get(iPos)
		iPanal = oEquip.panel()
		if iPanal not in glChatShowPanel:
			continue
		oPropsList.props.extend([oEquip.getMsg(*c.MSG_CHAT)])
	return oPropsList

def rpcRoleHyperLink(self,ep,who,reqMsg):#角色超链接
	iTarget=reqMsg.iValue
	oTargetResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iRoleId)
	if not oTargetResume :
		return
	ep.rpcFriendAttr(oTargetResume.getAttrMsg())

def rpcPropsHyperLink(self,ep,who,reqMsg):#物品超链接
	iRoleId=reqMsg.iValueU32
	iPropsId=reqMsg.iValueU64
	oTarget=role.gKeeper.getObj(iRoleId)
	oPackage=oTarget.propsCtn if oTarget else block.blockPackage.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iRoleId)	
	oProps=oPackage.getItem(iPropsId)
	if not oProps:
		ep.rpcTips('该物品信息已经失效')
		return
	propsDetail=oProps.getMsg(*c.MSG_OTHER)
	oPropsList=props_pb2.propsList()
	#发送自身对应的装备
	oOwnPropsMsg=sendSimilarEquipMsg(oProps, who,ep, False)
	lEquipMsg = [propsDetail, oOwnPropsMsg] if oOwnPropsMsg else [propsDetail]
	oPropsList.props.extend(lEquipMsg)	
	return oPropsList

def rpcTitleHyperLink(self,ep,who,reqMsg):#称号超链接
	iRoleId=reqMsg.iRoleId
	iTitleNo=reqMsg.iTitleNo

def rpcCommonPropsHyperLink(self,ep,who,reqMsg):
	iPropsNo=reqMsg.iValue
	if iPropsNo in c.VIR_ITEM:
		msg=props_pb2.propsMsg()
		msg.iPropsId=0
		msg.sDesc=c.VIR_ITEM[iPropsNo]
		msg.sPropsName=c.VIR_ITEM[iPropsNo]
		msg.iPropsIcon=c.VIR_ICON[iPropsNo]
		msg.iKind=10086  #虚拟物品 种类10086
	else:
		if iPropsNo in equipData.gdData:
			oProps=props.equip.getCacheProps(iPropsNo,bWave=False)
		else:
			oProps=props.getCacheProps(iPropsNo)
		if not oProps:
			return
		msg=oProps.getMsg(*c.MSG_OTHER)
		if props_pb2.COLLECT not in msg.buttons:
			msg.buttons.append(props_pb2.COLLECT)
		sendSimilarEquipMsg(oProps, who, ep)
	ep.rpcSendCommonPropsDetail(msg)

#发送和目标物品同类型的角色穿戴的装备信息
def sendSimilarEquipMsg(oTargetEquip, who,ep, bSend=True):#客户端所有物品都不做缓存....OMG
	oMsg = None
	if oTargetEquip.uiType()!=c.PROPS_EQUIP:	#装备
		return oMsg
	iPos=oTargetEquip.wearPos()
	oOwnEquip=who.propsCtn.getPropsByPos(iPos)	
	if oOwnEquip and oOwnEquip.key!=oTargetEquip.key:
		oMsg=oOwnEquip.getMsg(*c.MSG_OTHER)
		if bSend:ep.rpcSendPropsDetail(oMsg)
	return oMsg



import factory
import factoryConcrete
import timeU
import log
import scene
import resume
import role
import props
import block.blockPackage
import props_pb2
import equipData
import props.equip