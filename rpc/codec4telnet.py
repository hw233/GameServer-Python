#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

SEPARATOR='\r\n'

#编码器
class cEncoder(object):
	def encode(self,sPacket):
		return sPacket+SEPARATOR

#解码器
class cDecoder(object):
	def __init__(self):
		self.sBuffer=''

	def decode(self,sData):
		self.sBuffer+=sData
		while True:
			iIdx=self.sBuffer.find(SEPARATOR)
			if iIdx==-1:
				return #跳出,需要再读多一点数据
			sPacket,self.sBuffer=self.sBuffer[:iIdx],self.sBuffer[iIdx+len(SEPARATOR):]
			print 'a msg =',sPacket
			yield sPacket

import struct
import p

