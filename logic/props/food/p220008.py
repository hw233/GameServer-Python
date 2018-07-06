# -*- coding: utf-8 -*-
from common import *
from war.defines import *
import props.food

#玉液琼浆
class cProps(props.food.cProps):

	def useInWar(self, who, att, vic):#战斗中使用
		who.propsCtn.addStack(self, -1)
		att.war.rpcWarPerform(att, MAGIC_USE_PROPS, vic, self.no())
		sp = self.getEffect().get("愤怒1")
		vic.addSP(int(sp))
		return True