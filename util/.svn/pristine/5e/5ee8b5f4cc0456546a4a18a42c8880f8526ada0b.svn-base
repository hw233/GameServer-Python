#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇
#packet相关操作


def _getIntFormat(iSize,bSigned):
	if iSize==1:
		return '!b' if bSigned else '!B'
	elif iSize==2:
		return '!h' if bSigned else '!H'
	elif iSize==4:
		return '!i' if bSigned else '!I'
	elif iSize==8:
		return '!q' if bSigned else '!Q'
	else:
		raise Exception,'packInt或unPackInt字节数只能传1,2,4,8'

class cPack(object):
	def __init__(self,iPreSize=0):#iPreSize只能少或刚刚好,绝对不能多
		self.bBuffer=bytearray(iPreSize)
		self.iWriteIdx=0

	def clear(self,iPreSize=0):
		self.bBuffer=bytearray(iPreSize)
		self.iWriteIdx=0

	def getBuffer(self):#取得全部打包好的buff
		return self.bBuffer

	def packInt(self,iSize,iValue,bSigned=True):
		sInt=struct.pack(_getIntFormat(iSize,bSigned),iValue)		
		self.bBuffer[self.iWriteIdx:self.iWriteIdx+iSize]=sInt #空间不够会自动扩展的
		self.iWriteIdx+=iSize
		return self #可以链式调用

	def packStr(self,sText):
		iSize=len(sText)		
		self.packInt(iSize,4)
		
		sContent=struct.pack('!{}s'.format(iSize),sText)#str也要调用pack??
		if iSize!=len(sContent):#我不敢确认
			raise Exception,'为什么会不相等呢?有空要查一下文档'

		self.bBuffer[self.iWriteIdx:self.iWriteIdx+iSize]=sContent #空间不够会自动扩展的
		self.iWriteIdx+=iSize
		return self #可以链式调用

class cUnPack(object):
	def __init__(self,sBuffer):
		self.sBuffer=sBuffer

	def getBuffer(self):#取得剩下未解完的buffer
		return self.sBuffer

	def reSetBuffer(self,sBuffer):
		self.sBuffer=sBuffer

	def unPackStr(self):
		iSize=self.unPackInt(4)#先解出字符串长度
		if not self.sBuffer:
			raise Exception,'buffer已经被解完了'
		sText,=struct.unpack('!{}s'.format(iSize), self.sBuffer[:iSize])
		self.sBuffer=self.sBuffer[iSize:]
		return sText

	def unPackInt(self,iSize,bSigned=True):
		if not self.sBuffer:
			raise Exception,'buffer已经被解完了'
		#struct.unpack第二个参数可以接受 bytearray,memoryview,buffer 三种类型
		iValue,=struct.unpack(_getIntFormat(iSize,bSigned), self.sBuffer[:iSize])
		self.sBuffer=self.sBuffer[iSize:]
		return iValue

import struct