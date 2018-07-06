#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#
import terminal_main_pb2
import endPoint
from common import getRole

#指令服务
class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	def rpcInstruction(self,ep,ctrlr,reqMsg):return rpcInstruction(self,ep,ctrlr,reqMsg)
		
def rpcInstruction(self,ep,ctrlr,reqMsg):
	realInstruction(ep,reqMsg.sValue.strip())#去除两边的空白

def realInstruction(ep,sInstruct):
	#print 'realInstruction==',sInstruct
	try:
		lSection=_splitInstruction(sInstruct)#再以空白分开
		if not lSection:
			return
		sCmd=lSection.pop(0)
		for mod,iExtraArg in gdModPath.iteritems():			
			func=getattr(mod,sCmd,None)
			if func and type(func)==types.FunctionType:#
				break
			func=getFuncByShortName(mod,sCmd)#长指令名找不到,用短指令名找一找
			if func:
				sCmd=func.func_name
				break
		else:
			if config.IS_INNER_SERVER:
				ep.rpcTips('没有{}指令'.format(sCmd))
			return		

# 		if config.IS_INNER_SERVER:
# 			iNeedGroup=ANY #内服任何人可以执行任何指令
# 		else:
# 			iNeedGroup=getattr(func,'iNeedGroup',ADMIN)
# 			if iNeedGroup and not iNeedGroup&ADMIN:
# 				iNeedGroup|=ADMIN #虽然是生产环境,至少admin可以执行
# 
# 		if iNeedGroup and not ep.group()&iNeedGroup:
# 			if not config.IS_INNER_SERVER:
# 				ep.rpcTips('你所在用户组没有权限执行{}'.format(sCmd))
# 			return
			
		iTotalArgc=func.func_code.co_argcount #总参数个数
		iDefaultArgc=len(func.func_defaults) if func.func_defaults else 0 #默认参数个数
		iProvide=1 #不需用户提供但是指令中又肯定要有的endpoint对象
		iArgc=len(lSection) #实际提供的参数个数
# 		if iArgc<iTotalArgc-iDefaultArgc-iProvide:
# 			#if not config.IS_INNER_SERVER:
# 			ep.rpcTips('参数个数不够')
# 			return
# 		if iArgc>iTotalArgc-iProvide:
# 			#if not config.IS_INNER_SERVER:
# 			ep.rpcTips('参数个数过多')
# 			return
		if iExtraArg==GET_ROLE:#for role
			bRet,unknown=_getRole(ep,func,iArgc,iTotalArgc,iProvide,lSection)
			if not bRet:
				#if not config.IS_INNER_SERVER:
				ep.rpcTips(unknown)
				return			
			l=_parseArgs(lSection)
			func(ep,*l,target=unknown)
		elif iExtraArg==GET_ACCOUNT:#for account
			pass
		elif iExtraArg == DAOBIAO:
			instruction.forAny.update(ep)
			func(ep,*_parseArgs(lSection))
			instruction.forAny.commit(ep)
		elif iExtraArg==NOTHING:#for any
			func(ep,*_parseArgs(lSection))
		else:
			iRoleId=getattr(ep,'iRoleId',0)
			who=getRole(iRoleId)
			l=_parseArgs(lSection)
			func(who,*l)
	except Exception:#指令异常就不要写到log中去		
		etype,value=sys.exc_type,sys.exc_value
		sMessage=str(value.message) if value.message else str(value)
		sText='{}:{}'.format(etype.__name__,sMessage)
		if config.IS_INNER_SERVER:#内服才进log
			u.reRaise('执行指令出错,请确保指令是正确的')
		else:
			ep.rpcModalDialog(sText,'执行指令异常')	
			
	finally:#无论如何,都要把打过的指令记录下来
		log.log('instruction','{}:{}'.format(ep.selfDescription(),sInstruct))
		
def _splitInstruction(sInstruct):
	import re
	lst = []
	for idx,arg in enumerate(sInstruct.split()):
		if idx:
			try:
				eArg = eval(arg)
				if type(eArg) == types.ModuleType:
					arg = "'%s'" % arg
			except:
				#if idx and not re.match("^-?\d+(\.\d+)?$", arg):
				arg = "'%s'" % arg
		lst.append(arg)
	return lst

def _parseArgs(lArgs):#解析指令的参数
	for uArg in lArgs:
		try:
			yield eval(uArg)
		except Exception:
			raise Exception,'参数出错了,如果参数是字符串,请用在参数的两边加上单引号'

def _getRole(ep,func,iArgc,iTotalArgc,iProvide,lSection):
	if iArgc<iTotalArgc-iProvide:#参数没有全部给全的,取当前打指令的玩家对象
		iRoleId=getattr(ep,'iRoleId',0)
		if iRoleId==0:			
			return False,'请提供角色id参数' #如果是玩家打指令可以免id
	else:#参数全部都给全了		
		sRoleId=lSection.pop(-1)
		if not sRoleId.isdigit():
			return False,'角色id必须是数值型'
		iRoleId=int(sRoleId)
	
	iRoleFrom=getattr(func,'iRoleFrom',ONLINE)#默认情况要求在线的玩家作为参数
	if iRoleFrom==ONLINE:#在线的玩家
		who=role.gKeeper.getObj(iRoleId)
		if not who:
			return False,'id为{}的角色不在线'.format(iRoleId)									
	elif iRoleFrom==MEMORY:#在内存的玩家
		who=factoryConcrete.roleFtr.getProductFromMemory(iRoleId)
		if not who:
			return False,'id为{}的角色不在内存中'.format(iRoleId)
									
	else:# DATABASE 从db加载玩家
		who=factoryConcrete.roleFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE,iRoleId)
		if not who:			
			return False,'id为{}的角色在数据库中不存在'.format(iRoleId)
	return True,who	
		
		
i=-1
#1,2,4,8,16,32,64,128,256......
def increase():
	global i
	i+=1
	return pow(2,i)		


NOBODY=0 #表示指令不需要任何一个用户组,即所有人都可以执行
ANY=~0 #表示只要在其中任何一个用户组就可以执行该指令		

#用户组(一个员工可以同时属于多个组)
FAKE=0 #占位用的,没有任何权限的用户组,也就是不属于任何一个用户组

ADMIN			=increase() #超级管理员组,拥有全部指令的权限的用户组(实际是每个指令都会分配权限给该组)
LEADER			=increase() #各部门的主管


TESTER_CLERK	=increase() #测试职员
TESTER_LEADER	=increase() #测试主管
TESTER			=TESTER_CLERK|TESTER_LEADER #测试部门

GM_CLERK		=increase() #客服
GM_LEADER		=increase() #客服主管
GM				=GM_CLERK|GM_LEADER #客服部门

OPERATOR_CLERK	=increase() #运营职员
OPERATOR_LEADER	=increase() #运营主管
OPERATOR		=OPERATOR_CLERK|OPERATOR_LEADER #运营部门

PLANNER_CLERK	=increase() #策划主管
PLANNER_LEADER	=increase() #策划主管
PLANNER			=PLANNER_CLERK|PLANNER_LEADER #策划部门

CODER_CLERK		=increase() #程序职员
CODER_LEADER	=increase() #程序主管
CODER			=CODER_CLERK|CODER_LEADER #程序部门

SERVER_CODER	=increase() #服务端程序员
CLIENT_CODER	=increase() #客户端程序员
CODER_LEADER	=increase() #程序主管
	
#配置指令属性	
def properties(gr=ADMIN,sn=None):
	def __(func):
		if sn:#短指令名
			func.sShortName=sn	
		func.iNeedGroup=gr		
		return func		
	return __
	

ONLINE=1
MEMORY=2
DATABASE=3

#装饰器
def roleFrom(iRoleFrom):#执行指令时从哪获取角色对象
	def __(func):
		func.iRoleFrom=iRoleFrom		
		return func
	return __

def getFuncByShortName(mod, shortName):
	for func in getAllMethodByMod(mod):
		shortName = shortName.lower()
		if hasattr(func, "sShortName") and shortName == func.sShortName.lower():
			return func
		if shortName == func.func_name.lower():
			return func
	return None
	
def init():#检查各个指令表的指令名字(函数名)是否重复,短名字是否重复
	sNameGroup=set()	
	for mod, funcList in getAllMethod():
# 		if not hasattr(mod,'getAllMethod'):
# 			raise Exception,'{}模块必须实现getAllMethod方法'.format(mod)

		for func in funcList:
			sLongName=func.func_name			
			if sLongName in sNameGroup:
				raise Exception,'{}模块中的{}指令在别的模块中已经有了,换个名字吧'.format(mod.__name__,sLongName)
			sShortName=getattr(func,'sShortName',None)
			if sShortName!=None and sShortName in sNameGroup:
				raise Exception,'{}模块的{}这个短名字已经被其他指令占用了,换个其他短名字吧'.format(mod.__name__,sShortName)
			
			sNameGroup.add(sLongName)
			sNameGroup.add(sShortName)
			
			# iNeedGroup=getattr(func,'iNeedGroup',ADMIN)
			# if iNeedGroup and not iNeedGroup&ADMIN:
			# 	iNeedGroup=iNeedGroup|ADMIN#无论任何指令,admin都可以执行
			# func.iNeedGroup=iNeedGroup

GET_ROLE=1
GET_ACCOUNT=2
NOTHING=3
DAOBIAO=4 #导表
ACTIVITY=5 # 活动
CONFIG=6 # 系统设置

import types
import instruction
import sys
import u
import hotUpdate
import role
import misc
import config
import log
import factoryConcrete

import forRole
import forAny
import forAccount
import switch
import makeData
import memory
import forPet
import common
import forActivity
import stat
import forConfig
import forBuddy

#自动获取指令参数时,获取的对象
gdModPath={
	forRole:GET_ROLE,
	forAccount:GET_ACCOUNT,
	forAny:NOTHING,
	makeData:DAOBIAO,
	switch:NOTHING,
	memory:NOTHING,
	forPet:GET_ROLE,
	forActivity:ACTIVITY,
	stat:NOTHING,
	forConfig:NOTHING,
	forBuddy:GET_ROLE,
}

def getAllMethod():
	for mod in gdModPath:
		funcList = getAllMethodByMod(mod)
		yield mod, funcList

def getAllMethodByMod(mod):
	funcList = []
	for name in dir(mod):
		if name[0] == "_": # 系统或私有属性
			continue
		if hasattr(common, name): # 公共模块的
			continue
		obj = getattr(mod, name)
		if type(obj) != types.FunctionType:
			continue
		funcList.append(obj)
	return funcList

init()

