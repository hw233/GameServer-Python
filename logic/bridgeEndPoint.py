#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import endPointWithSocket
import p
import codec

CONN_ID_SIZE=4 #连接id的大小
SERIALIZED_UNKNOWN=p.cPack().packInt(CONN_ID_SIZE,0).getBuffer()

class cBridgeEndPoint(endPointWithSocket.cEndPointWithSocket):
	def __init__(self,*tArgs,**dArgs):#override
		endPointWithSocket.cEndPointWithSocket.__init__(self,*tArgs,**dArgs)
		self.oBuffer=buf.cBuffer(1024*6) #

	def send(self,uPacket,sSerializedConnId=SERIALIZED_UNKNOWN):#override
		if uPacket==StopIteration:
			endPointWithSocket.cEndPointWithSocket.send(self,uPacket)
		else:
			iPacketSize=len(uPacket)
			iNeedSize=cEncoder.HEADER_SIZE+CONN_ID_SIZE+iPacketSize
			
			mv=self.oBuffer.peekWrite(iNeedSize)
			self.oBuffer.hasWritten(iNeedSize)

			#在前面留出4个byte放长度
			#连接id
			mv[cEncoder.HEADER_SIZE:cEncoder.HEADER_SIZE+CONN_ID_SIZE]=sSerializedConnId
			#实际内容
			mv[cEncoder.HEADER_SIZE+CONN_ID_SIZE:cEncoder.HEADER_SIZE+CONN_ID_SIZE+iPacketSize]=uPacket

			endPointWithSocket.cEndPointWithSocket.send(self,mv) #sSerializedConnId+uPacket

	def _getEncoder(self):#override
		return cEncoder()
	
	def directSend(self,mvPacket):#override
		endPointWithSocket.cEndPointWithSocket.directSend(self,mvPacket)
		self.oBuffer.retrieve(len(mvPacket))

#编码器
class cEncoder(codec.cEncoder):
	def encode(self,mvPacket):#override
		#preappend
		mvPacket[0:self.HEADER_SIZE]=struct.pack('!i',len(mvPacket)-self.HEADER_SIZE)
		return mvPacket	

if 'gbOnce' not in globals():
	gbOnce=True

import struct
import buf
import backEnd_pb2