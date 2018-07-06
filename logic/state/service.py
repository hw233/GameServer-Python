# -*- coding: utf-8 -*-

import endPoint
import state_pb2

class cService(state_pb2.terminal2main):
	@endPoint.result
	def rpcStateRepairAll(self, ep, who, reqMsg): return rpcStateRepairAll(who, reqMsg)

	@endPoint.result
	def rpcStateClick(self, ep, who, reqMsg): return rpcStateClick(who, reqMsg)


# 一键修理身上的装备
def rpcStateRepairAll(who, reqMsg):
	iCostCash = 0
	equips = []
	for equip in who.equipCtn.getAllWearEquip():
		iCostCash += equip.lifeRepairPrice()
		equips.append(equip)
	if iCostCash <= 0:
		message.tips(who, "装备不需要修理")
		return
	content = "花费#IS#n#C07{}#n修理全身装备？\nQ取消\nQ修理".format(iCostCash)
	message.confirmBoxNew(who, responseRepairAll, content)
		
def responseRepairAll(who, yes):
	if not yes:
		return
	
	iCostCash = 0
	equips = []
	for equip in who.equipCtn.getAllWearEquip():
		iCostCash += equip.lifeRepairPrice()
		equips.append(equip)
	if iCostCash <= 0:
		message.tips(who, "装备不需要修理")
		return
	if not money.checkCash(who, iCostCash):
		return
	who.addCash(-iCostCash, "一键修理身上的装备")
	for equip in equips:
		equip.recoverLife()
	message.tips(who, "修理成功")

def rpcStateClick(who, reqMsg):
	taskObj = task.hasTask(who, 30601)
	if taskObj and taskObj.timerMgr.hasTimerId("timeOut"):
		scene.walkGuard(who, 2010)


import message
import money
import task
import scene
