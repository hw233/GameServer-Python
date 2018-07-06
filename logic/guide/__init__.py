# -*- coding: utf-8 -*-
#新手引导相关


def onLogin(who, bReLogin):
	guide.service.sendGuideRecord(who)


from common import *
import message
import guide.service

