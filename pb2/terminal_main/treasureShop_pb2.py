# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: treasureShop.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import universal.public_pb2
import common_pb2
import props_pb2
import lineup_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='treasureShop.proto',
  package='treasureShop',
  serialized_pb='\n\x12treasureShop.proto\x12\x0ctreasureShop\x1a\x16universal/public.proto\x1a\x0c\x63ommon.proto\x1a\x0bprops.proto\x1a\x0clineup.proto\"\xfd\x01\n\tgoodsInfo\x12\x10\n\x08iStallId\x18\x01 \x02(\x03\x12\x0e\n\x06iPrice\x18\x02 \x01(\x03\x12\x12\n\niAttention\x18\x03 \x01(\x05\x12\x12\n\nbAttention\x18\x04 \x01(\x08\x12\x10\n\x08iGoodsId\x18\x05 \x01(\x05\x12\x0f\n\x07iReport\x18\x06 \x01(\x05\x12\x0f\n\x07\x62Report\x18\x07 \x01(\x08\x12$\n\x05props\x18\x08 \x01(\x0b\x32\x15.props.packageItemMsg\x12\x1b\n\x03\x65ye\x18\t \x01(\x0b\x32\x0e.lineup.eyeMsg\x12\r\n\x05iType\x18\n \x01(\x05\x12\r\n\x05iTime\x18\x0b \x01(\x05\x12\x11\n\tiSellerId\x18\x0c \x01(\x03\"\x8d\x01\n\rgoodsListInfo\x12\x10\n\x08iGoodsId\x18\x01 \x02(\x05\x12\x0e\n\x06iOrder\x18\x02 \x01(\x05\x12\r\n\x05iPage\x18\x03 \x01(\x05\x12\r\n\x05iType\x18\x04 \x01(\x05\x12\x10\n\x08iPageMax\x18\x05 \x01(\x05\x12*\n\tgoodsList\x18\x06 \x03(\x0b\x32\x17.treasureShop.goodsInfo\",\n\x08sellInfo\x12\x10\n\x08iPropsId\x18\x01 \x02(\x03\x12\x0e\n\x06iPrice\x18\x02 \x01(\x03\"g\n\x08itemInfo\x12\x0f\n\x07iItemId\x18\x01 \x02(\x05\x12\x0f\n\x07iStatus\x18\x02 \x01(\x05\x12*\n\tgoodsInfo\x18\x03 \x01(\x0b\x32\x17.treasureShop.goodsInfo\x12\r\n\x05iTime\x18\x04 \x01(\x05\"K\n\x0citemListInfo\x12\x11\n\tiPriceAll\x18\x01 \x01(\x03\x12(\n\x08itemList\x18\x02 \x03(\x0b\x32\x16.treasureShop.itemInfo2\xd9\x04\n\rterminal2main\x12>\n\x11rpcTSGoodsListReq\x12\x1b.treasureShop.goodsListInfo\x1a\x0c.public.fake\x12:\n\x11rpcTSGoodsInfoReq\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake\x12\x36\n\rrpcTSGoodsBuy\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake\x12\x36\n\x0erpcTSGoodsSell\x12\x16.treasureShop.sellInfo\x1a\x0c.public.fake\x12<\n\x13rpcTSGoodsSellAgain\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake\x12:\n\x11rpcTSGoodsGetBack\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake\x12?\n\x16rpcTSGoodsAttentionSet\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake\x12-\n\x0frpcTSItemLisReq\x12\x0c.public.fake\x1a\x0c.public.fake\x12\x37\n\x0erpcTSProfitGet\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake\x12\x39\n\x10rpcTSGoodsReport\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake2\xe4\x03\n\rmain2terminal\x12?\n\x12rpcTSGoodsListSend\x12\x1b.treasureShop.goodsListInfo\x1a\x0c.public.fake\x12;\n\x12rpcTSGoodsInfoSend\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake\x12:\n\x11rpcTSGoodsInfoMod\x12\x17.treasureShop.goodsInfo\x1a\x0c.public.fake\x12=\n\x11rpcTSItemListSend\x12\x1a.treasureShop.itemListInfo\x1a\x0c.public.fake\x12<\n\x10rpcTSItemListMod\x12\x1a.treasureShop.itemListInfo\x1a\x0c.public.fake\x12\x34\n\x0crpcTSItemMod\x12\x16.treasureShop.itemInfo\x1a\x0c.public.fake\x12\x34\n\x0crpcTSItemDel\x12\x16.treasureShop.itemInfo\x1a\x0c.public.fake\x12\x30\n\x10rpcTSSellSuccess\x12\x0e.common.int32_\x1a\x0c.public.fakeB\x03\x90\x01\x01')




_GOODSINFO = _descriptor.Descriptor(
  name='goodsInfo',
  full_name='treasureShop.goodsInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iStallId', full_name='treasureShop.goodsInfo.iStallId', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iPrice', full_name='treasureShop.goodsInfo.iPrice', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iAttention', full_name='treasureShop.goodsInfo.iAttention', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bAttention', full_name='treasureShop.goodsInfo.bAttention', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iGoodsId', full_name='treasureShop.goodsInfo.iGoodsId', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iReport', full_name='treasureShop.goodsInfo.iReport', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bReport', full_name='treasureShop.goodsInfo.bReport', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='props', full_name='treasureShop.goodsInfo.props', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='eye', full_name='treasureShop.goodsInfo.eye', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iType', full_name='treasureShop.goodsInfo.iType', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iTime', full_name='treasureShop.goodsInfo.iTime', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iSellerId', full_name='treasureShop.goodsInfo.iSellerId', index=11,
      number=12, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=102,
  serialized_end=355,
)


_GOODSLISTINFO = _descriptor.Descriptor(
  name='goodsListInfo',
  full_name='treasureShop.goodsListInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iGoodsId', full_name='treasureShop.goodsListInfo.iGoodsId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iOrder', full_name='treasureShop.goodsListInfo.iOrder', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iPage', full_name='treasureShop.goodsListInfo.iPage', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iType', full_name='treasureShop.goodsListInfo.iType', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iPageMax', full_name='treasureShop.goodsListInfo.iPageMax', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='goodsList', full_name='treasureShop.goodsListInfo.goodsList', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=358,
  serialized_end=499,
)


_SELLINFO = _descriptor.Descriptor(
  name='sellInfo',
  full_name='treasureShop.sellInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPropsId', full_name='treasureShop.sellInfo.iPropsId', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iPrice', full_name='treasureShop.sellInfo.iPrice', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=501,
  serialized_end=545,
)


_ITEMINFO = _descriptor.Descriptor(
  name='itemInfo',
  full_name='treasureShop.itemInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iItemId', full_name='treasureShop.itemInfo.iItemId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iStatus', full_name='treasureShop.itemInfo.iStatus', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='goodsInfo', full_name='treasureShop.itemInfo.goodsInfo', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iTime', full_name='treasureShop.itemInfo.iTime', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=547,
  serialized_end=650,
)


_ITEMLISTINFO = _descriptor.Descriptor(
  name='itemListInfo',
  full_name='treasureShop.itemListInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPriceAll', full_name='treasureShop.itemListInfo.iPriceAll', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='itemList', full_name='treasureShop.itemListInfo.itemList', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=652,
  serialized_end=727,
)

_GOODSINFO.fields_by_name['props'].message_type = props_pb2._PACKAGEITEMMSG
_GOODSINFO.fields_by_name['eye'].message_type = lineup_pb2._EYEMSG
_GOODSLISTINFO.fields_by_name['goodsList'].message_type = _GOODSINFO
_ITEMINFO.fields_by_name['goodsInfo'].message_type = _GOODSINFO
_ITEMLISTINFO.fields_by_name['itemList'].message_type = _ITEMINFO
DESCRIPTOR.message_types_by_name['goodsInfo'] = _GOODSINFO
DESCRIPTOR.message_types_by_name['goodsListInfo'] = _GOODSLISTINFO
DESCRIPTOR.message_types_by_name['sellInfo'] = _SELLINFO
DESCRIPTOR.message_types_by_name['itemInfo'] = _ITEMINFO
DESCRIPTOR.message_types_by_name['itemListInfo'] = _ITEMLISTINFO

class goodsInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GOODSINFO

  # @@protoc_insertion_point(class_scope:treasureShop.goodsInfo)

class goodsListInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GOODSLISTINFO

  # @@protoc_insertion_point(class_scope:treasureShop.goodsListInfo)

class sellInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SELLINFO

  # @@protoc_insertion_point(class_scope:treasureShop.sellInfo)

class itemInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ITEMINFO

  # @@protoc_insertion_point(class_scope:treasureShop.itemInfo)

class itemListInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ITEMLISTINFO

  # @@protoc_insertion_point(class_scope:treasureShop.itemListInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\220\001\001')

_TERMINAL2MAIN = _descriptor.ServiceDescriptor(
  name='terminal2main',
  full_name='treasureShop.terminal2main',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=730,
  serialized_end=1331,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsListReq',
    full_name='treasureShop.terminal2main.rpcTSGoodsListReq',
    index=0,
    containing_service=None,
    input_type=_GOODSLISTINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsInfoReq',
    full_name='treasureShop.terminal2main.rpcTSGoodsInfoReq',
    index=1,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsBuy',
    full_name='treasureShop.terminal2main.rpcTSGoodsBuy',
    index=2,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsSell',
    full_name='treasureShop.terminal2main.rpcTSGoodsSell',
    index=3,
    containing_service=None,
    input_type=_SELLINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsSellAgain',
    full_name='treasureShop.terminal2main.rpcTSGoodsSellAgain',
    index=4,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsGetBack',
    full_name='treasureShop.terminal2main.rpcTSGoodsGetBack',
    index=5,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsAttentionSet',
    full_name='treasureShop.terminal2main.rpcTSGoodsAttentionSet',
    index=6,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSItemLisReq',
    full_name='treasureShop.terminal2main.rpcTSItemLisReq',
    index=7,
    containing_service=None,
    input_type=universal.public_pb2._FAKE,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSProfitGet',
    full_name='treasureShop.terminal2main.rpcTSProfitGet',
    index=8,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsReport',
    full_name='treasureShop.terminal2main.rpcTSGoodsReport',
    index=9,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
])

class terminal2main(_service.Service):
  __metaclass__ = service_reflection.GeneratedServiceType
  DESCRIPTOR = _TERMINAL2MAIN
class terminal2main_Stub(terminal2main):
  __metaclass__ = service_reflection.GeneratedServiceStubType
  DESCRIPTOR = _TERMINAL2MAIN


_MAIN2TERMINAL = _descriptor.ServiceDescriptor(
  name='main2terminal',
  full_name='treasureShop.main2terminal',
  file=DESCRIPTOR,
  index=1,
  options=None,
  serialized_start=1334,
  serialized_end=1818,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsListSend',
    full_name='treasureShop.main2terminal.rpcTSGoodsListSend',
    index=0,
    containing_service=None,
    input_type=_GOODSLISTINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsInfoSend',
    full_name='treasureShop.main2terminal.rpcTSGoodsInfoSend',
    index=1,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSGoodsInfoMod',
    full_name='treasureShop.main2terminal.rpcTSGoodsInfoMod',
    index=2,
    containing_service=None,
    input_type=_GOODSINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSItemListSend',
    full_name='treasureShop.main2terminal.rpcTSItemListSend',
    index=3,
    containing_service=None,
    input_type=_ITEMLISTINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSItemListMod',
    full_name='treasureShop.main2terminal.rpcTSItemListMod',
    index=4,
    containing_service=None,
    input_type=_ITEMLISTINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSItemMod',
    full_name='treasureShop.main2terminal.rpcTSItemMod',
    index=5,
    containing_service=None,
    input_type=_ITEMINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSItemDel',
    full_name='treasureShop.main2terminal.rpcTSItemDel',
    index=6,
    containing_service=None,
    input_type=_ITEMINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTSSellSuccess',
    full_name='treasureShop.main2terminal.rpcTSSellSuccess',
    index=7,
    containing_service=None,
    input_type=common_pb2._INT32_,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
])

class main2terminal(_service.Service):
  __metaclass__ = service_reflection.GeneratedServiceType
  DESCRIPTOR = _MAIN2TERMINAL
class main2terminal_Stub(main2terminal):
  __metaclass__ = service_reflection.GeneratedServiceStubType
  DESCRIPTOR = _MAIN2TERMINAL

# @@protoc_insertion_point(module_scope)
