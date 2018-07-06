# -*- coding: utf-8 -*-
import npcData

#===============================================================================
# 门派导师
#===============================================================================
def getSchoolMaster(schoolId):
	npcIdx = schoolMasterIdxList[schoolId]
	return npc.getNpcByIdx(npcIdx)

def initSchoolMasterIdxList():
	idxList = {}
	for npcIdx, info in npcData.gdData.iteritems():
		if info.get("类型") != "导师":
			continue
		schoolId = info.get("职业")
		if schoolId:
			idxList[schoolId] = npcIdx
		
	return idxList

if "schoolMasterIdxList" not in globals():
	schoolMasterIdxList = initSchoolMasterIdxList()

import npc