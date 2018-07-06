#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def channelBuilt(iReportBackEnd,iComeFrom):#某后端与某后端之间打通了通道
	if 'mainService' in SYS_ARGV:
		if iReportBackEnd==backEnd_pb2.MAIN_SERVICE:
			raise Exception,'自己向{}报到.,又通知自己,神经'.format('路由' if 1 else '网关')
		elif iReportBackEnd==backEnd_pb2.SCENE_SERVICE:
			_sceneReport4ms(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.FIGHT_SERVICE:
			_fightReport4ms(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.CHAT_SERVICE:
			_chatReport4ms(iComeFrom)

	if 'sceneService' in SYS_ARGV:
		if iReportBackEnd==backEnd_pb2.MAIN_SERVICE:
			_mainReport4ss(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.SCENE_SERVICE:
			raise Exception,'自己向{}报到.,又通知自己,神经'.format('路由' if 1 else '网关')
		elif iReportBackEnd==backEnd_pb2.FIGHT_SERVICE:
			_fightReport4ss(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.CHAT_SERVICE:
			_chatReport4ss(iComeFrom)

	if 'fightService' in SYS_ARGV:
		if iReportBackEnd==backEnd_pb2.MAIN_SERVICE:
			_mainReport4fs(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.SCENE_SERVICE:
			_sceneReport4fs(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.CHAT_SERVICE:
			_chatReport4fs(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.FIGHT_SERVICE:
			raise Exception,'自己向{}报到.,又通知自己,神经'.format('路由' if 1 else '网关')

	if 'chatService' in SYS_ARGV:
		if iReportBackEnd==backEnd_pb2.MAIN_SERVICE:
			_mainReport4cs(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.SCENE_SERVICE:
			_sceneReport4cs(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.FIGHT_SERVICE:
			_fightReport4cs(iComeFrom)
		elif iReportBackEnd==backEnd_pb2.CHAT_SERVICE:
			raise Exception,'自己向{}报到.,又通知自己,神经'.format('路由' if 1 else '网关')

if 'mainService' in SYS_ARGV:
	def _sceneReport4ms(iComeFrom):#场景服务与主服务通道打通了(有可能是断开重连的哦)
		if iComeFrom==1:
			print '"场景服务"向路由报到.'
			backEnd.ssReport2routeEv4ms.set()
		else:
			print '"场景服务"向网关报到.'
			backEnd.ssReport2gateEv4ms.set()
		
	def _fightReport4ms(iComeFrom):
		if iComeFrom==1:
			print '"战斗服务"向路由报到.'
			backEnd.fsReport2routeEv4ms.set()
		else:
			print '"战斗服务"向网关报到.'
			backEnd.fsReport2gateEv4ms.set()

	def _chatReport4ms(iComeFrom):
		if iComeFrom==1:
			print '"聊天服务"向路由报到.'
			backEnd.csReport2routeEv4ms.set()
		else:
			print '"聊天服务"向网关报到.'
			backEnd.csReport2gateEv4ms.set()


if 'sceneService' in SYS_ARGV:
	def _mainReport4ss(iComeFrom):
		if iComeFrom==1:
			print '"主服务"向路由报到.'
			backEnd.msReport2routeEv4ss.set()
		else:
			print '"主服务"向网关报到.'
			backEnd.msReport2gateEv4ss.set()

	def _fightReport4ss(iComeFrom):
		if iComeFrom==1:
			print '"战斗服务"向路由报到.'
			backEnd.fsReport2routeEv4ss.set()
		else:
			print '"战斗服务"向网关报到.'
			backEnd.fsReport2gateEv4ss.set()

	def _chatReport4ss(iComeFrom):
		if iComeFrom==1:
			print '"聊天服务"向路由报到.'
			backEnd.csReport2routeEv4ss.set()
		else:
			print '"聊天服务"向网关报到.'
			backEnd.csReport2gateEv4ss.set()


if 'fightService' in SYS_ARGV:
	def _sceneReport4fs(iComeFrom):
		if iComeFrom==1:
			print '"场景服务"向路由报到.'
			backEnd.ssReport2routeEv4fs.set()
		else:
			print '"场景服务"向网关报到.'
			backEnd.ssReport2gateEv4fs.set()

	def _mainReport4fs(iComeFrom):
		if iComeFrom==1:
			print '"主服务"向路由报到.'
			backEnd.msReport2routeEv4fs.set()
		else:
			print '"主服务"向网关报到.'
			backEnd.msReport2gateEv4fs.set()

	def _chatReport4fs(iComeFrom):
		if iComeFrom==1:
			print '"聊天服务"向路由报到.'
			backEnd.csReport2routeEv4fs.set()
		else:
			print '"聊天服务"向网关报到.'
			backEnd.csReport2gateEv4fs.set()


if 'chatService' in SYS_ARGV:
	def _mainReport4cs(iComeFrom):
		if iComeFrom==1:
			print '"主服务"向路由报到.'
			backEnd.msReport2routeEv4cs.set()
		else:
			print '"主服务"向网关报到.'
			backEnd.msReport2gateEv4cs.set()

	def _sceneReport4cs(iComeFrom):
		if iComeFrom==1:
			print '"场景服务"向路由报到.'
			backEnd.ssReport2routeEv4cs.set()
		else:
			print '"场景服务"向网关报到.'
			backEnd.ssReport2gateEv4cs.set()

	def _fightReport4cs(iComeFrom):
		if iComeFrom==1:
			print '"战斗服务"向路由报到.'
			backEnd.fsReport2routeEv4cs.set()
		else:
			print '"战斗服务"向网关报到.'
			backEnd.fsReport2gateEv4cs.set()


import backEnd
import backEnd_pb2