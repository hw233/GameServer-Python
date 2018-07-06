# -*- coding: utf-8 -*-

def getData(channelId):
	return gdData.get(channelId)
	
#导表开始
gdData={
	1:{"内容长度":60,"时间间隔":"20-(lv/10)*1","活力":"50-(lv/6)*3"},
	2:{"内容长度":60,"时间间隔":"5","活力":"0"},
	3:{"内容长度":60,"时间间隔":"1","活力":"0"},
	4:{"内容长度":60,"时间间隔":"1","活力":"0"},
	5:{"内容长度":60,"时间间隔":"5","活力":"0"},
	6:{"内容长度":60,"时间间隔":"1","活力":"0"},
	7:{"内容长度":60,"时间间隔":"5","活力":"0"},
	8:{"内容长度":60,"时间间隔":"1","活力":"0"},
}
#导表结束

def afterHotUpdate():
	if "mainService" in SYS_ARGV:
		mainService.getChatEP().rpcHotUpdate("channelData")
	
import mainService