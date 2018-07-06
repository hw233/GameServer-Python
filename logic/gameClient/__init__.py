#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#模拟游戏客户端,用于测试

import client
import endPointWithSocket
class cEndPointWithSocket(endPointWithSocket.cEndPointWithSocket):
	def _onDisConnected(self):
		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)
		print '游戏客户端模拟器断线了.'
		#import traceback
		#traceback.print_stack()
		gGameClient.connect(0)#断线了,要尝试重连.

def afterConnect(sock,tAddress):
	sIP,iPort=tAddress
	print 'game client:connect success to ip:{} port:{}'.format(*tAddress)
	bDebugMode=config.IS_INNER_SERVER
	ep=cEndPointWithSocket(bDebugMode,gtService)
	ep.setIP(sIP).setPort(iPort).setSocket(sock)
	ep.start()
	return ep

def start(*tArgs):
	global gGameClient
	sLocalIP='127.0.0.1'
	if tArgs:
		if len(tArgs)==1:
			sIp,iPort=sLocalIP,int(tArgs[0])
		else:
			sIp,iPort=tArgs[0],int(tArgs[1])
	else:
		if platform.system().upper()=="WINDOWS":
			sIp,iPort=sLocalIP,config.GATE_PORT_FOR_GAME_CLIENT #  内部测试服  外网测试服 
		else:
			sIp,iPort=sLocalIP,config.INSTRUCTION_PORT 
	
	gGameClient=client.cStreamClient((sIp,iPort),afterConnect)
	gGameClient.ep=None
	print ('game client:starting try to connect to ip:{} port:{}'.format(sIp,iPort))
	gGameClient.connect(0)	
	import os
	print 'pid:', os.getpid(), 'gGameClient:', id(gGameClient.ep)
	proc()



import account_pb2
import role_pb2
import terminal_main_pb2
import serviceMisc_pb2
import svcTest
import accountService
import roleService
import svcGameClientMiscService
import chatTest
import terminal_chat_pb2
import mailService
import mail_pb2

gtService={
	"service":(
		svcTest.cService,
		svcGameClientMiscService.cService,
		accountService.cService,
		roleService.cService,
		chatTest.cService,
		mailService.cService,
	),
	"stub":(
		terminal_main_pb2.terminal2main_Stub,
		serviceMisc_pb2.gameServerMiscService_Stub,
		account_pb2.terminal2main_Stub,
		role_pb2.terminal2main_Stub,
		terminal_chat_pb2.terminal2chat_Stub,
		mail_pb2.terminal2main_Stub,
	)
}





def proc():
	while True:
		try:
			sInput=raw_input(u.trans(''))
			if not sInput:			
				continue		
			if sInput=='quit':
				break
			if sInput=='reset':
				start()
				break
			if gGameClient.ep is None:
				print '连接已断开,准备重连.'
				gGameClient.connect(1)
				continue
			ep = gGameClient.ep
			
			print '-------------------------------------'
			if sInput.startswith('@'):#指令
				sInstruct=sInput[1:] #这一行与其rpc有点不同
				gGameClient.ep.rpcInstruction(sInstruct)
				continue

			l=sInput.split()#以空格分开各个参数
			sRPC,lArgs=l[0],l[1:]
			if sRPC in ('1','rpcAccountLogin','log'):
				sAccount=lArgs[0]
				bOk, msg=gGameClient.ep.rpcAccountLogin(sAccount,'1000',2,'123','adf','asdf')
				if not msg.bSuccessed:
					return
				print "accountLoginResp.bValue:", msg.bSuccessed
				print "accountLoginResp.timeSt", msg.timeStamp
				
			elif sRPC in ('2','rpcRoleLogin','lr'):
				iRoleId=int(lArgs[0])
				gGameClient.ep.rpcRoleLogin(iRoleId)
			elif sRPC in ('rpcCreateRole','cr'):
				sName,iSchool=lArgs[0],int(lArgs[1])
				gGameClient.ep.rpcCreateRole(sName,iSchool)				
				# iSchool=int(lArgs[0])
				# gGameClient.ep.rpcCreateRole(iSchool)
			elif sRPC in ('rpcDelRole','dr'):
				iRoleId=int(lArgs[0])
				gGameClient.ep.rpcDelRole(iRoleId)
#############################################################################	
			elif sRPC in ('test',):
				#iSelectNo=int(lArgs[0])
				gGameClient.ep.rpcSetRoleName(211,'CE9')
#############################################################################	
			elif sRPC in ('ss',): #测试切换加点方案
				iType=(int)(lArgs[0])
				bFail,oMsg=gGameClient.ep.rpcSwitchScheme(iType)
				print bFail,oMsg.bValue
			elif sRPC in ('rc',): #测试加点模拟器
				gGameClient.ep.rpcReqCalculator()
			elif sRPC in ('rp',): #洗点
				bFail,oMsg=gGameClient.ep.rpcResetPoint()
				print bFail,oMsg.bValue 
			elif sRPC in ('cfrp',):#确认加点
				# bFail,oMsg=gGameClient.ep.rpcConfirmResetPoint(1,1,1,1,1,1,1)
				bFail,oMsg=gGameClient.ep.rpcConfirmResetPoint(1,0,0,0,0,0,0)
				print bFail,oMsg.bValue
			elif sRPC == "reqBanChannel":
				ep.rpcBanChannelReq()
			elif sRPC == "setBanChannel":
				channelIdList = [int(s) for s in lArgs]
				msg = terminal_chat_pb2.banChannelMsg()
				msg.channelIdList.extend(channelIdList)
				ep.rpcBanChannelSet(msg)
			elif sRPC == "rpcMailTakeProps":
				mailId = int(lArgs[0])
				msg = mail_pb2.mailMsg()
				msg.mailId = mailId
				ep.rpcMailTakeProps(msg)
			elif sRPC == "time":
				localTime  = int(time.time() * 1000)
				msg = common_pb2.int64_()
				msg.iValue = localTime
				bOk, msg=ep.rpcServerTime(msg)
				print msg
			else:
				print '客户端模拟器没有实现名为{}的这个rpc.'.format(sRPC)
		except:
			traceback.print_exc()
	return


import time
import socket
import traceback
import gevent
import gevent.socket
import gevent.queue

import makeData
import misc
import u
import log
import auction_pb2
import props_pb2
import common_pb2
import account_pb2

import task_pb2
import scene_pb2
import platform
import config