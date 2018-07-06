#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
def getConfig(iNo,sKey,uDefault=0):
	if iNo not in gdData:
		raise PlannerError,'没有编号为{}的系统广播'.format(iNo)
	return gdData[iNo].get(sKey,uDefault)


#导表开始
gdData={
	1:{"sContent":"《龙之谷：破晓》精英测试现正进行中。"},
	2:{"sContent":"你提我改，留下您的意见和建议帮助我们完善版本。"},
	3:{"sContent":"通过官网首页（dnd.sdo.com）新闻入口参与你提我改"},
	4:{"sContent":"关注有礼，抢先关注官方微信赢海量金币、畅玩体力。"},
	5:{"sContent":"关注官方微信号：poxiaoqibing_LZG，丰富活动等你来。"},
	6:{"sContent":"战力风云，角色战力排行前三名赢京东购物卡。"},
	7:{"sContent":"任性签到，每日登录都可领取道具奖励。"},
	8:{"sContent":"角色每升5级就可领取成长礼包，开启获得超级好礼。"},
	9:{"sContent":"如游戏发生卡死或无响应请后台关闭游戏并重新启动。"},
	10:{"sContent":"提示：包裹可拓展、药剂可同时增加体力与法力。"},
	11:{"sContent":"提示：目前尚未开放钻石充值，但可以体验钻石部分功能。"},
}
#导表结束

AMOUNT=len(gdData)