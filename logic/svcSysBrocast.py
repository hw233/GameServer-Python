#-*-coding:utf-8-*-
#系统广播

if 'gdAmount' not in globals():
	gdAmount=1


def sendSysBrocast():
	global gdAmount
	if gdAmount>sysBrocastData.AMOUNT: #从第一条信息读起,读到最后一条就循环从第一条开始重新广播
		gdAmount=1
	sContent=sysBrocastData.getConfig(gdAmount,'sContent')
	oMsg=chatRoom_pb2.chatSysDown(iChannel=1,sContent=sContent,)
	sPacket=endPoint.makePacket('rpcAnnounce',oMsg)
	for iUid,ep in mainService.gRoleIdMapEndPoint.getAll().iteritems():
		ep.send(sPacket)
	gdAmount+=1

def init():
	gTimerMsg.run(sendSysBrocast,10,120)

import timer
import mainService
import sysBrocastData
import endPoint

gTimerMsg=timer.cTimerMng()
init()
