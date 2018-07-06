#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

class cBuffer(object):
	def __init__(self,iInitLen=1024):
		if iInitLen<=0:
			raise Exception,'滚,长度至少为1'
		self.mBuffer=memoryview(bytearray(iInitLen))
		self.iReadIdx,self.iWriteIdx=0,0 #[前闭,后开)

	def readableBytes(self):
		return self.iWriteIdx-self.iReadIdx
		
	def makeSpace(self,iNeedSize):#挪动或扩充,得到一个连续的iNeedSize可写空间.(只会扩充得比需要的多,不会少)
		iReadAble = self.iWriteIdx-self.iReadIdx
		iLen=len(self.mBuffer)

		while iLen-iReadAble<iNeedSize or iLen-iReadAble < iLen/3.0:#可写空间不够needSize或不足1/3,要搞大他
			iLen*=2

		if iLen!=len(self.mBuffer):
			mNewBuffer=memoryview(bytearray(iLen))#扩充空间只能另搞一个对象,因为bytearray被memoryview包装过后无法扩大容量
			mNewBuffer[0:iReadAble]=self.mBuffer[self.iReadIdx:self.iReadIdx+iReadAble]
			self.mBuffer=mNewBuffer
		else:
			self.mBuffer[0:iReadAble]=self.mBuffer[self.iReadIdx:self.iReadIdx+iReadAble]
		self.iReadIdx,self.iWriteIdx=0,iReadAble

	def hasWritten(self,iLen):
		if iLen>len(self.mBuffer)-self.iWriteIdx:
			raise Exception,'都没有这么多字节数'
		self.iWriteIdx += iLen

	def retrieve(self,iLen):
		if iLen > self.iWriteIdx-self.iReadIdx:
			raise Exception,'没有这么多字节数'
		if iLen < self.iWriteIdx-self.iReadIdx:	
			self.iReadIdx += iLen
		else:
			self.iReadIdx=self.iWriteIdx=0
	
	def peekWrite(self,iSize=0):#0表示拿全部
		if iSize==0:
			if self.iWriteIdx==len(self.mBuffer):
				self.makeSpace(1024)
			return self.mBuffer[self.iWriteIdx:]
		else:#
			if self.iWriteIdx+iSize>len(self.mBuffer):
				self.makeSpace(iSize)
			return self.mBuffer[self.iWriteIdx:self.iWriteIdx+iSize]

	def peekRead(self,iSize):
		return self.mBuffer[self.iReadIdx:self.iReadIdx+iSize]

	# def append(self,sData):#这个函数差不多要作废了,socket.recv返回是str,但是要改用socket.recv_into了
	# 	iDataLen=len(sData)
	# 	if len(self.mBuffer)-self.iWriteIdx<iDataLen:#后面的空间不够用了
	# 		self.makeSpace(iDataLen)#挪腾数据,扩大空间

	# 	self.mBuffer[self.iWriteIdx:self.iWriteIdx+iDataLen]=sData
	# 	self.iWriteIdx+=iDataLen

#import struct
#import p
#import u
