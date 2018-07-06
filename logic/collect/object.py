# -*- coding: utf-8 -*-
import template
import block
import sql
import block.singleton

'''室外收集
'''

# if 'mainService' not in SYS_ARGV:
# 	class cMainCollect(object):
# 		pass

# if 'mainService' in SYS_ARGV:
class cMainCollect(template.Template):
	def __init__(self):
		template.Template.__init__(self)
		self.timerMgr = timer.cTimerMng()
		self._name = "collect"
		
	def init(self):
		'''初始化
		'''
		pass
	
	@property
	def name(self):
		return self._name

	@property
	def logName(self):
		return "collect/"
		
	def getScriptHandler(self, script):
		for pattern, handler in gScriptHandlerList.iteritems():
			m = re.match(pattern, script)
			if not m:
				continue
			args = m.groups()
			return handler, args
		return template.Template.getScriptHandler(self, script)
			
	def testCmd(self, who, cmdIdx, *args):
		'''测试指令
		'''
		pass
	

# 脚本处理函数
gScriptHandlerList = {
}
		

import weakref
import timer
import scene
import factoryConcrete
import re
import c
import log
import u
import config
