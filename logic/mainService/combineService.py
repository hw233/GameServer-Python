#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#拼装各种服务

import instruction
import friend.svcFriend
import title.svcTitle
import svcHyperLink

import miscService

import block.propsExchange
import block.diamondExchange
# import guild.svcGuild


class cService1(
	#这里面的class实现每一个成员方法时,都调用另一个全局方法,
	#因为成员方法都加了装饰器,加了装饰器形成闭包后会热更新失败,
	#全局方法因为没有装饰器,所以可以热更新

	
	# chatRoom.cService,
	instruction.cService,
	#mail.svcMail.cService,
	#friend.svcFriend.cService,
	#task.svcTask.cService,
	#title.svcTitle.cService,
	svcHyperLink.cService,

	#block.propsExchange.cService,
	#block.diamondExchange.cService,
	#guild.svcGuild.cService,
	
	#杂项
	miscService.cService,
	):
	pass


import svcMisc
class cService2(
	#这里面的class实现每一个成员方法时,都调用另一个全局方法,
	#因为成员方法都加了装饰器,加了装饰器形成闭包后会热更新失败,
	#全局方法因为没有装饰器,所以可以热更新
	svcMisc.cService,
	

	):
	pass
