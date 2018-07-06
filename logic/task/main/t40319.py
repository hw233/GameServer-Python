# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·明修罗'''
	intro = '''六大门派全面围攻慈云寺，$target就在大殿，我们突击'''
	detail = '''六大门派全面围攻慈云寺，$target就在大殿，我们突击'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1531,NI1532,NI1533,NI1534,NI1535,NI1536,NI1537,NI1538,NI1539,NI1540,NI1541,NI1542,NI1543,NI1546,NI1547,NI1548,E(1531,1550),E(1532,1551),E(1533,1552),E(1534,1555),E(1535,1556),E(1536,1557),E(1537,1557),E(1538,1558),E(1539,1559),E(1540,1560),E(1541,1561),E(1542,1562),E(1543,1558),E(1546,1557),E(1547,1564),E(1548,1565)'''
#导表结束