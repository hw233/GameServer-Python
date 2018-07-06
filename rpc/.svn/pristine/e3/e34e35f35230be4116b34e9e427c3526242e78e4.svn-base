#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

#编码器
class cEncoder(object):
	HEADER_SIZE=4
	def encode(self,sPacket):
		iLen=len(sPacket)
		ba = p.cPack(self.HEADER_SIZE+iLen).packInt(self.HEADER_SIZE,iLen).getBuffer()
		# if iLen+self.HEADER_SIZE!=len(ba):
		# 	raise Exception,'预分配字节数算错了iLen={},ba={}'.format(iLen,len(ba))
		ba[self.HEADER_SIZE:]=sPacket
		return ba

#解码器
class cDecoder(object):
	HEADER_SIZE=4
	def __init__(self,iMaxInputBufferSize=3*1024*1024):
		self.iPacketLen=-1
		self.iMaxInputBufferSize=iMaxInputBufferSize

	def reset(self):
		self.iPacketLen=-1

	def decode(self,oBuffer):
		readableBytes=oBuffer.readableBytes
		retrieve=oBuffer.retrieve
		peekRead=oBuffer.peekRead
		unpack=struct.unpack
		HEADER_SIZE=self.HEADER_SIZE
		iMaxInputBufferSize=self.iMaxInputBufferSize

		while True:
			if self.iPacketLen==-1:
				if readableBytes()<HEADER_SIZE:#连一个头都不够
					return #跳出,需要再读多一点数据

				mLen=peekRead(HEADER_SIZE)
				self.iPacketLen,=unpack('!i', mLen)

				retrieve(HEADER_SIZE)

				if self.iPacketLen>iMaxInputBufferSize:#防止恶意攻击,恶意的客户端
					raise Exception,'接收到一个包宣称大小是{},超过了{}'.format(self.iPacketLen,iMaxInputBufferSize)
			
			if readableBytes()<self.iPacketLen:#不够一个逻辑包
				return #跳出,需要再读多一点数据

			mPacket=peekRead(self.iPacketLen)
			retrieve(self.iPacketLen)
			self.iPacketLen=-1
	
			yield mPacket.tobytes() 
			#外部并有可能没有马上使用,这里还在修改(调整,移动),memoryview共用同一份内存,会毁坏数据
			#况且protobuf的ParseFromString函数只接受str

import struct
import p
import u

