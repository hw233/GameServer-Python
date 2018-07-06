# -*- coding: utf-8 -*-
#作者:马昭@曹县闫店楼镇
def launchBySpecify(who,iPropsNo,iAmount,bIsBind,sLogReason='',sTips='',*tPropsArgs,**dPropsArgs):#sTips传None就不会提示
	iRoleId=who.id
	iTmp=iAmount
	while iAmount>0:
		oProps=props.new(iPropsNo,*tPropsArgs,**dPropsArgs)
		if oProps.isVirtual():
			oProps.setValue(iAmount)
			iRealStack = iAmount
		else:
			iMaxStack=oProps.maxStack()
			if iAmount>iMaxStack:
				iRealStack=iMaxStack
			else:
				iRealStack=iAmount
			oProps.setStack(iRealStack)
		iAmount-=iRealStack
		if bIsBind and not oProps.isBind():
			oProps.bind()
		launchProps(who,oProps,sLogReason,sTips)
	iAmount=iTmp
	return iPropsNo,iAmount

#这段代码被弃用了，请用这条self.launchProps(who, int(propsNo), amount, binded)
# def launchForTask(who,iPropsNo,iAmount,bIsBind,sLogReason='',sTips='',*tPropsArgs,**dPropsArgs):
# 	launchBySpecify(who,iPropsNo,iAmount,bIsBind,sLogReason,sTips,*tPropsArgs,**dPropsArgs)
# 	oProps = props.getCacheProps(iPropsNo)
# 	message.message(who,"获得{}个{}".format(iAmount,oProps.name))

def launchProps(who,propsObj,sLogReason,sTips=""):
	iRoleId=who.id
	if propsObj.isVirtual():
		_launchVirtualProps(who,propsObj)
		return
	if not who.propsCtn.leftCapacity() and propsObj.isVisible():  #背包满了放进临时背包
		message.tips(who,"你的背包已满，请及时整理以免丢失物品")
		if who.tempCtn.itemCount()>=15:
			log.log('props','{}获得{},原因={},但背包和临时背包已满所以被丢弃'.format(iRoleId,propsObj.toLogStr(),sLogReason))
			return
		who.addProps(who.tempCtn, propsObj, sLogReason)
	else:
		who.endPoint.rpcAddPropsFlash(propsObj.getMsg4Package(None,*propsObj.MSG_FIRST))
		propsIdList = who.addProps(who.propsCtn, propsObj, sLogReason)
		who.endPoint.rpcGetNewProps(iPropsIds=propsIdList)

# #投放道具,bTryMail为True表示包裹放不下就存系统邮箱
# def launchProps(who,oProps,sLogReason,sTips='',bTryMail=True):#sTips为None时表示不显示提示		
# 	#if oProps.isTaskProps():
# 	#	raise Exception,'是任务道具,不要放到普通包裹来'
# 	iRoleId=who.id
# 	ep=who.endPoint
# 	if oProps.isVirtual():
# 		_launchVirtualProps(who,oProps,sLogReason,sTips)
# 		return

# 	iOri=oProps.stack()
# 	iReal,bExclusive=_tryAddProps(who,oProps,sLogReason)#bExclusive是否独占一个格子
# 	if iReal<=0 and not bTryMail:#一个也放不下,又不愿放邮件
# 		return 0
# 	if iReal>0 and sTips!=None:
# 		name = oProps.name
# 		if iReal > 1:
# 			name = "%s×%d" % (name, iReal)
# 		if not sTips:
# 			sTips='获得了$prop'
# 		sTips = sTips.replace("$prop", name)
# 		ep.rpcTips(sTips)
	
# 	if bExclusive:
# 		log.log('props','{}获得{},原因={},独占一个包裹格子.'.format(iRoleId,oProps.toLogStr(),sLogReason))	
# 		return iOri
# 	elif iReal==iOri:
# 		log.log('props','{}获得{},原因={},全部叠加到了已有的物品上'.format(iRoleId,oProps.toLogStr(),sLogReason))
# 		return iOri
		
# 	if iReal>0:
# 		if bTryMail:
# 			log.log('props','{}获得{},原因={},已经叠加到了已有的物品上,其他将进邮箱'.format(iRoleId,oProps.toLogStr(),sLogReason))
# 		else:
# 			log.log('props','{}获得{},原因={},已经叠加到了已有的物品上,放不下的丢弃'.format(iRoleId,oProps.toLogStr(),sLogReason))
# 			return iReal
# 	else:
# 		log.log('props','{}获得{},原因={},全部将进入邮箱'.format(iRoleId,oProps.toLogStr(),sLogReason))
	
# 	if iReal>0:#部分进入了包裹,oProps可以继续使用
# 		oProps.setStack(iOri-iReal)
# 	mail.sendSysMail(iRoleId,'奖励物品','奖励物品请提取',None,oProps)#给个邮件有效期吧??	
# 	ep.rpcTips('包裹已满,请到邮箱领取{}'.format(oProps.name))
# 	return iOri	

# def _tryAddProps(who,oProps,sLogReason):#会改变oProps对象里面的数据	
# 	iStack=oProps.stack()
# 	propsCtn=who.propsCtn
# 	if not oProps.canAutoCombine():#有存盘属性的,不可自动叠加
# 		return (iStack,True) if propsCtn.addItem(oProps) else (0,False)
# 	iMaxStack=oProps.maxStack()		
# 	#if iStack>=iMaxStack and propsCtn.addItem(oProps):	#如果达到数量上限的,尝试直接放入包裹空格子上	
# 	#	return iStack,True #想了一下,不合理,说不定拆开分别叠到已有的物品,可以叠完,就不用浪费一个格子了
		
# 	#尝试叠到已有物品的格子上
# 	iNo=oProps.no()
# 	iLeft=iStack
# 	l=[]		
# 	for obj in propsCtn.getAllValues():
# 		if obj.no()!=iNo:#编号不相同,是绝对不能叠在一起的
# 			continue
# 		if obj.stack()>=iMaxStack:
# 			continue
# 		if not obj.canAutoCombine():
# 			continue
# 		#走到这里说明可以进行叠加了
# 		iSpace=iMaxStack-obj.stack()
# 		if iSpace>=iLeft:#可以全部叠进去
# 			l.append((obj,iLeft))
# 			iLeft=0
# 			break
# 		else:#只能叠一些进去
# 			l.append((obj,iSpace))
# 			iLeft-=iSpace				
# 	else:#全部可以叠加的空间加起来都不够放.
# 		#尝试找一个空格放进去,因为你叠了后不够放最后还是要占一个新格子的,干脆直接全部放在一个格子里.
# 		if propsCtn.addItem(oProps):
# 			return iStack,True
# 	#开始真正的叠(可能是因为没有空格子了才叠,也可能是有空格子,但是已有物品够叠)
# 	for obj,iAdd in l:
# 		propsCtn.addStack(obj,iAdd)		
# 	return iStack-iLeft,False


#处理虚拟道具
def _launchVirtualProps(who,oProps):
	oProps.use(who)

import u
import misc
import log
import mail
import props
import block.numenBag
import message