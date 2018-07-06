#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_pb2

CONN_ID_SIZE=4 #连接id的大小
CONN_ID_COMMAND=0 #内部通道id,不代表真正的客户端连接

import p
SERIALIZED_UNKNOWN=p.cPack().packInt(CONN_ID_SIZE,backEnd_pb2.UNKNOWN_SERVICE).getBuffer()


