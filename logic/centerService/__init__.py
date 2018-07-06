# -*- coding: utf-8 -*-

def attrChange(changeList):
	oCenterEP = client4center.getCenterEndPoint()
	oCenterEP.rpcUpdateResume(**changeList)

def getCenterEp(iZoneNo):
	return centerService.cs4backEnd.gBackEndProxy.getProxy((iZoneNo, backEnd_pb2.MAIN_SERVICE))

import client4center
import centerService.cs4backEnd
import backEnd_pb2