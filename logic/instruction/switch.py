#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#各种系统开关
'''系统各种开关'''

#import instruction


def staffOnly(ep,val=True):#只有内部员工可以进行
	'只允许内部员工进入游戏.参数:[True]'		
	block.parameter.parameter.setStaffOnly(val)
	if val:
		ep.rpcTips('设置成功,普通玩家无法进入')
	else:
		ep.rpcTips('设置成功,普通玩家可以自由进入')

#物品交易所开关
def openPropsExchange(ep,bSwitch=True):#
	'打开物品交易所.参数:[True]'
	if bSwitch:
		block.propsExchange.gExchange.open()
		ep.rpcTips('打开物品交易所成功.')
	else:
		block.propsExchange.gExchange.close()
		ep.rpcTips('关闭物品交易所成功.')
#元宝交易所开关
def openDiamondExchange(ep,bSwitch=True):#
	'打开元宝交易所.参数:[True]'
	if bSwitch:
		block.diamondExchange.gExchange.open()
		ep.rpcTips('打开元宝交易所成功.')
	else:
		block.diamondExchange.gExchange.close()
		ep.rpcTips('关闭元宝交易所成功.')

#公会系统开关
def openGuild(ep,bSwitch=True):
	'打开公会.参数:[True]'
	import guild.svcGuild
	if bSwitch:
		guild.svcGuild.gbIsClosed=False
		ep.rpcTips('打开公会成功.')
	else:
		guild.svcGuild.gbIsClosed=True
		ep.rpcTips('关闭公会成功.')

#商店系统开关
def openShop(ep,bSwitch=True):
	'打开商店.参数:[True]'
	import shop.svcShop
	if bSwitch:
		shop.svcShop.gbIsClosed=False
		ep.rpcTips('打开商城成功.')
	else:
		shop.svcShop.gbIsClosed=True
		ep.rpcTips('关闭商城成功.')


#邮箱系统开关		
def openMail(ep,bSwitch=True):
	'打开邮箱系统.参数:[True]'
	if bSwitch:
		mail.svcMail.open()
		ep.rpcTips('打开邮箱系统成功.')
	else:
		mail.svcMail.close()
		ep.rpcTips('关闭邮箱系统成功.')


#强化装备开关
def openEnhaEquip(ep,bSwitch=True):
	'打开装备强化功能.参数:[True]'
	if bSwitch:
		#svcPackage.canEnchance=True
		ep.rpcTips('打开强化装备功能成功')
	else:
		#svcPackage.canEnchance=False
		ep.rpcTips('关闭强化装备功能成功')
#升星功能开关
def openUpdateStar(ep,bSwitch=True):
	'打开升星功能.参数:[True]'
	if bSwitch:
		#svcPackage.canUpStar=True
		ep.rpcTips('打开升星功能成功')
	else:
		#svcPackage.canUpStar=False
		ep.rpcTips('关闭升星功能成功')
#镶嵌功能开关
def openEquipLayIn(ep,bSwitch=True):
	'打开镶嵌功能.参数:[True]'
	if bSwitch:
		#svcPackage.canInLay=True
		ep.rpcTips('打开镶嵌功能成功')
	else:
		#svcPackage.canInLay=False
		ep.rpcTips('关闭镶嵌功能成功')
#徽章升级功能开关
def openBadgeUplevel(ep,bSwitch=True):
	'打开徽章升级功能.参数:[True]'
	pass

import types
import block.parameter
import block.diamondExchange
import block.propsExchange
#import svcPackage
