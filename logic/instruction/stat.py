# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
# 统计,状态查询,只读不修改的指令

import instruction


# 服务器时间
def serverinfo(ep):
	txtList = []
	
	t = time.localtime()[:6]
	txtList.append("当前时间:{}年{}月{}日{}时{}分{}秒".format(*t))
	
	t = time.localtime(getSecond())[:6]
	txtList.append("测试时间:{}年{}月{}日{}时{}分{}秒".format(*t))

	txtList.append("天序号:{} 周序号:{} 月序号:{}".format(getHourNo(), getDayNo(), getWeekNo(), getMonthNo()))
	txtList.append("服务器id:{}".format(config.ZONE_ID))	
	txtList.append("服务器区号:{}".format(config.ZONE_NO))	
	txtList.append("全服共有玩家{}个".format(role.gKeeper.amount()))
	ep.rpcModalDialog("\n".join(txtList))


from common import *
import config
import role