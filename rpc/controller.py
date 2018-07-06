#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import google.protobuf.service

class cController(google.protobuf.service.RpcController):
	def Reset(self):
		pass

	def Failed(self):
		pass

	def ErrorText(self):
		pass

	def StartCancel(self):
		pass

	def SetFailed(self,reason):
		pass

	def IsCancelled(self):
		pass

	def NotifyOnCancel(self,callback):
		pass