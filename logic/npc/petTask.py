# -*- coding: utf-8 -*-
import npc.object

class cNpc(npc.object.cNpc):
	def hasLookPetTask(self, who):
		'''判断是否有宠物任务
		'''
		curLv = 0
		hasCurTask = False	#当前是否有可接任务
		nextTaskLv = 0	#是否有下一等级任务等级

		lvKeys,groupTask = task.pett.getPetGroupTask()
		if not lvKeys or not groupTask:
			return hasCurTask,nextTaskLv

		petComplete = who.taskCtn.fetch("petCom", {}) #{等级:[编号]}
		for i,lv in enumerate(lvKeys):
			if lv > who.level:
				nextTaskLv = lv
				break
			completeTask = petComplete.get(lv, [])
			for _i,info in enumerate(groupTask[lv]):
				tasklist = info.get("任务", [])
				#判断任务是否全部完成,没全部完成说明是当前要进行的任务
				if len(tasklist) <= len(set(completeTask) & set(tasklist)):	
					continue
				#没有完成所有任务，说明当前在做这个等级的任务
				curLv = lv
				nextTaskLv = lvKeys[i+1] if len(lvKeys) > i+1 else 0
				break
			if curLv:
				break

		#判断当前等级的系列任务
		if curLv:
			for info in groupTask[curLv]:
				tasklist = info.get("任务", [])
				flag = True
				for no in tasklist:	#这个系列任务是否正在进行
					if who.taskCtn.getItem(no):
						flag = False
						break
				if flag and len(set(completeTask) & set(tasklist)) == 0:
					hasCurTask = True
					break

		return hasCurTask,nextTaskLv

	def doLook(self, who):
		#对话
		chat = self.getChat()	
		txtList= []
		selList = []
		
		hasCurTask,nextTaskLv = self.hasLookPetTask(who)
		if chat:
			if nextTaskLv:
				txtList.append("{}\n#C09（{}级时可领取下一阶段的异兽）#n".format(chat, nextTaskLv))
			else:
				txtList.append("{}\n#C09（已没可预览的异兽，敬请期待更新）#n".format(chat, nextTaskLv))

		if hasCurTask:
			txtList.append("Q领取异兽任务")
			selList.append(100)
		
		if nextTaskLv:
			txtList.append("Q下一异兽任务")
			selList.append(101)

		content = "\n".join(txtList)
		message.selectBoxNew(who, functor(self.responseLook, selList), content, self)
		
	def responseLook(self, who, selectNo, selList):
		if selectNo < 1 or selectNo > len(selList):
			return
		
		sel = selList[selectNo-1]
		if sel == 100:	#接任务
			self.lookCurTask(who)
		elif sel == 101:#查看下一组任务
			self.lookNextTask(who)

		
	def getPetTaskList(self, who, nextTask=False):
		'''获取宠物任务列表
		'''
		curLv = 0
		nextLv = 0
		lvKeys,groupTask = task.pett.getPetGroupTask()
		if not lvKeys or not groupTask:
			return 0,{}

		petComplete = who.taskCtn.fetch("petCom", {}) #{等级:[编号]}
		# print "petComplete=",petComplete
		for i,lv in enumerate(lvKeys):
			if lv > who.level:
				nextLv = lv
				break
			completeTask = petComplete.get(lv, [])
			for info in groupTask[lv]:
				tasklist = info.get("任务", [])
				#判断任务是否全部完成
				if len(tasklist) <= len(set(completeTask) & set(tasklist)):#完成了
					continue
				curLv = lv
				nextLv = lvKeys[i+1] if len(lvKeys) > i+1 else 0
				break
			if curLv:
				break

		if nextTask:	#显示下一等级任务
			nextPetTaskMap = {}
			if nextLv:
				for info in groupTask[nextLv]:
					tasklist = info.get("任务",[])
					petNo = info.get("宠物编号", 0)
					nextPetTaskMap[petNo] = (tasklist[0], 1)
			return nextLv,nextPetTaskMap
		else:			#当前正在做的任务
			petTaskMap = {}
			completeTask = petComplete.get(curLv, [])
			for info in groupTask.get(curLv, ()):
				tasklist = info.get("任务", [])
				#判断任务是否全部完成
				# print "petTaskMap",info.get("宠物编号", 0),set(completeTask) & set(tasklist),tasklist
				petNo = info.get("宠物编号", 0)
				isDone = 0
				if len(tasklist) <= len(set(completeTask) & set(tasklist)):#完成了
					isDone = 1
				else:
					for no in tasklist:	#这个系列任务是否正在进行
						if who.taskCtn.getItem(no):
							isDone = 1
							break
				petTaskMap[petNo] = (tasklist[0], isDone)
			return curLv,petTaskMap

	def lookCurTask(self, who):
		#已经同类型有任务不能再接
		taskLv,taskPetMap = self.getPetTaskList(who)
		if not taskPetMap:
			self.say(who, "当前可接异兽任务已全部完成")
			return
		self.rpcPetTaskSelectInfo(who, 1, taskLv, taskPetMap)

	def lookNextTask(self, who):
		taskLv,taskPetMap = self.getPetTaskList(who, True)
		if not taskPetMap:
			self.say(who, "没有下一组异兽任务")
			return
		self.rpcPetTaskSelectInfo(who, 0, taskLv, taskPetMap)
		
	def givePetTask(self, who, petNo):
		'''领取宠物任务
		'''
		#已经同类型有任务不能再接
		if task.hasTask(who, task.pett.PET_TASK_PARENTID):
			message.tips(who, "你已有异兽任务")
			return
		taskLv,taskPetMap = self.getPetTaskList(who)
		taskInfo = taskPetMap.get(petNo, (0, 1))
		if taskInfo[1] == 1:
			message.tips(who, "该异兽任务已领取")
			return
		taskId = taskInfo[0]
		if not taskId:
			message.tips(who, "领取异兽任务失败")
			return

		task.newTask(who, None, taskId)
		message.tips(who, "领取异兽任务成功")
		#删除引导任务
		task.removeTask(who, task.pett.PET_TASK_LEAD_NO)

	def lookPetInfo(self, who, petNo):
		'''查看宠物信息
		'''
		petObj = pet.getCachePet(petNo)#pet.new(petNo, 0)
		if not petObj:
			return
		who.endPoint.rpcPetHyperlink(pet.service.packPetData(petObj))

	def getPetPos(self, who, taskLv, taskPetMap):
		'''宠物任务位置
			1.一共有A、B、C三个位置，当该等级段只有1只异兽的任务可接时，它的位置在B
			2.等级段只有2只异兽任务可接时，位置在A、C
			3.等级段有3只异兽任务时，填满A、B、C，若超过3只则翻页
		'''
		lvKeys,groupTask = task.pett.getPetGroupTask()
		taskInfo = groupTask.get(taskLv, ())

		petPosList = []
		for info in taskInfo:
			petPosList.append(info.get("宠物编号", 0))

		petPos = {}
		totalCnt = len(petPosList)#总个数
		if totalCnt == 1:
			petPos[petPosList[0]] = 2
		elif totalCnt == 2:
			petPos[petPosList[0]] = 1
			petPos[petPosList[1]] = 3
		elif totalCnt >= 3:
			for pos,petNo in enumerate(petPosList):
				petPos[petNo] = pos+1
		return petPos

	def packetPetTaskInfo(self, who, showType, taskLv, taskPetMap):
		petPos = self.getPetPos(who, taskLv, taskPetMap)
		msgList = []
		for petNo,info in taskPetMap.iteritems():
			msg = task_pb2.petTaskInfo()
			msg.pos = petPos.get(petNo, 0)
			msg.petNo = petNo
			petObj = pet.getCachePet(petNo)
			if petObj:
				msg.shape = petObj.shape
				msg.shapeParts.extend(petObj.shapeParts)
			msg.isDone = info[1]
			msgList.append(msg)
		return msgList

	def rpcPetTaskSelectInfo(self, who, showType, taskLv, taskPetMap):
		msg = {}
		msg["showType"] = showType
		msg["petInfo"] = self.packetPetTaskInfo(who, showType, taskLv, taskPetMap)

		who.endPoint.rpcTaskPetInfo(**msg)


from common import *
import message
import task
import task.pett
import task_pb2
import pet
import pet.service