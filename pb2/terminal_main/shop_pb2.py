# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: shop.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import universal.public_pb2
import common_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='shop.proto',
  package='shop',
  serialized_pb='\n\nshop.proto\x12\x04shop\x1a\x16universal/public.proto\x1a\x0c\x63ommon.proto\",\n\x07\x62uyInfo\x12\x10\n\x08iPropsNo\x18\x01 \x02(\x05\x12\x0f\n\x07iAmount\x18\x02 \x02(\x05\"O\n\x08openInfo\x12\x11\n\tiShopType\x18\x01 \x02(\x05\x12\x0f\n\x07iTaskId\x18\x02 \x01(\x05\x12\x10\n\x08iPropsNo\x18\x03 \x01(\x05\x12\r\n\x05\x62Shut\x18\x04 \x01(\x08\"?\n\x0bpropsExInfo\x12\x10\n\x08iPointID\x18\x01 \x02(\x05\x12\x1e\n\x07\x62uyInfo\x18\x02 \x01(\x0b\x32\r.shop.buyInfo\"C\n\x0bmoneyExInfo\x12\x12\n\niMoneyType\x18\x01 \x02(\x05\x12\x0f\n\x07iSource\x18\x02 \x01(\x05\x12\x0f\n\x07iAmount\x18\x03 \x01(\x05\"@\n\x0c\x65xchangeInfo\x12\x10\n\x08iPointID\x18\x01 \x02(\x05\x12\x1e\n\x07\x62uyInfo\x18\x02 \x03(\x0b\x32\r.shop.buyInfo\"\x7f\n\tmallProps\x12\x10\n\x08iPropsNo\x18\x01 \x02(\x05\x12\x0f\n\x07iAmount\x18\x02 \x01(\x05\x12\x0e\n\x06iPrice\x18\x03 \x01(\x05\x12\x11\n\tiOriginal\x18\x04 \x01(\x05\x12\x0c\n\x04iIdx\x18\x05 \x01(\x05\x12\x0f\n\x07iWeight\x18\x06 \x01(\x05\x12\r\n\x05iTime\x18\x07 \x01(\x05\"A\n\x08mallInfo\x12\x11\n\tiMallType\x18\x01 \x02(\x05\x12\"\n\tmallProps\x18\x02 \x03(\x0b\x32\x0f.shop.mallProps2\xb9\x02\n\rterminal2main\x12*\n\x0brpcBuyGoods\x12\r.shop.buyInfo\x1a\x0c.public.fake\x12\x33\n\x10rpcPropsExchange\x12\x11.shop.propsExInfo\x1a\x0c.public.fake\x12\x33\n\x10rpcMoneyExchange\x12\x11.shop.moneyExInfo\x1a\x0c.public.fake\x12\x36\n\x12rpcExchangeInfoReq\x12\x12.shop.exchangeInfo\x1a\x0c.public.fake\x12.\n\x0erpcMallInfoReq\x12\x0e.shop.mallInfo\x1a\x0c.public.fake\x12*\n\nrpcMallBuy\x12\x0e.shop.mallInfo\x1a\x0c.public.fake2\xe2\x01\n\rmain2terminal\x12+\n\x0brpcOpenShop\x12\x0e.shop.openInfo\x1a\x0c.public.fake\x12:\n\x16rpcExchangeInfoRespone\x12\x12.shop.exchangeInfo\x1a\x0c.public.fake\x12\x32\n\x12rpcMallInfoRespone\x12\x0e.shop.mallInfo\x1a\x0c.public.fake\x12\x34\n\x14rpcOpenPropsExchange\x12\x0e.common.int32_\x1a\x0c.public.fakeB\x03\x90\x01\x01')




_BUYINFO = _descriptor.Descriptor(
  name='buyInfo',
  full_name='shop.buyInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPropsNo', full_name='shop.buyInfo.iPropsNo', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iAmount', full_name='shop.buyInfo.iAmount', index=1,
      number=2, type=5, cpp_type=1, label=2,
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
  serialized_start=58,
  serialized_end=102,
)


_OPENINFO = _descriptor.Descriptor(
  name='openInfo',
  full_name='shop.openInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iShopType', full_name='shop.openInfo.iShopType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iTaskId', full_name='shop.openInfo.iTaskId', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iPropsNo', full_name='shop.openInfo.iPropsNo', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bShut', full_name='shop.openInfo.bShut', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=104,
  serialized_end=183,
)


_PROPSEXINFO = _descriptor.Descriptor(
  name='propsExInfo',
  full_name='shop.propsExInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPointID', full_name='shop.propsExInfo.iPointID', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyInfo', full_name='shop.propsExInfo.buyInfo', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=185,
  serialized_end=248,
)


_MONEYEXINFO = _descriptor.Descriptor(
  name='moneyExInfo',
  full_name='shop.moneyExInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iMoneyType', full_name='shop.moneyExInfo.iMoneyType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iSource', full_name='shop.moneyExInfo.iSource', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iAmount', full_name='shop.moneyExInfo.iAmount', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  serialized_start=250,
  serialized_end=317,
)


_EXCHANGEINFO = _descriptor.Descriptor(
  name='exchangeInfo',
  full_name='shop.exchangeInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPointID', full_name='shop.exchangeInfo.iPointID', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyInfo', full_name='shop.exchangeInfo.buyInfo', index=1,
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
  serialized_start=319,
  serialized_end=383,
)


_MALLPROPS = _descriptor.Descriptor(
  name='mallProps',
  full_name='shop.mallProps',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPropsNo', full_name='shop.mallProps.iPropsNo', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iAmount', full_name='shop.mallProps.iAmount', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iPrice', full_name='shop.mallProps.iPrice', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iOriginal', full_name='shop.mallProps.iOriginal', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iIdx', full_name='shop.mallProps.iIdx', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iWeight', full_name='shop.mallProps.iWeight', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iTime', full_name='shop.mallProps.iTime', index=6,
      number=7, type=5, cpp_type=1, label=1,
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
  serialized_start=385,
  serialized_end=512,
)


_MALLINFO = _descriptor.Descriptor(
  name='mallInfo',
  full_name='shop.mallInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iMallType', full_name='shop.mallInfo.iMallType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mallProps', full_name='shop.mallInfo.mallProps', index=1,
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
  serialized_start=514,
  serialized_end=579,
)

_PROPSEXINFO.fields_by_name['buyInfo'].message_type = _BUYINFO
_EXCHANGEINFO.fields_by_name['buyInfo'].message_type = _BUYINFO
_MALLINFO.fields_by_name['mallProps'].message_type = _MALLPROPS
DESCRIPTOR.message_types_by_name['buyInfo'] = _BUYINFO
DESCRIPTOR.message_types_by_name['openInfo'] = _OPENINFO
DESCRIPTOR.message_types_by_name['propsExInfo'] = _PROPSEXINFO
DESCRIPTOR.message_types_by_name['moneyExInfo'] = _MONEYEXINFO
DESCRIPTOR.message_types_by_name['exchangeInfo'] = _EXCHANGEINFO
DESCRIPTOR.message_types_by_name['mallProps'] = _MALLPROPS
DESCRIPTOR.message_types_by_name['mallInfo'] = _MALLINFO

class buyInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BUYINFO

  # @@protoc_insertion_point(class_scope:shop.buyInfo)

class openInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _OPENINFO

  # @@protoc_insertion_point(class_scope:shop.openInfo)

class propsExInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PROPSEXINFO

  # @@protoc_insertion_point(class_scope:shop.propsExInfo)

class moneyExInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MONEYEXINFO

  # @@protoc_insertion_point(class_scope:shop.moneyExInfo)

class exchangeInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EXCHANGEINFO

  # @@protoc_insertion_point(class_scope:shop.exchangeInfo)

class mallProps(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MALLPROPS

  # @@protoc_insertion_point(class_scope:shop.mallProps)

class mallInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MALLINFO

  # @@protoc_insertion_point(class_scope:shop.mallInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\220\001\001')

_TERMINAL2MAIN = _descriptor.ServiceDescriptor(
  name='terminal2main',
  full_name='shop.terminal2main',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=582,
  serialized_end=895,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcBuyGoods',
    full_name='shop.terminal2main.rpcBuyGoods',
    index=0,
    containing_service=None,
    input_type=_BUYINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcPropsExchange',
    full_name='shop.terminal2main.rpcPropsExchange',
    index=1,
    containing_service=None,
    input_type=_PROPSEXINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcMoneyExchange',
    full_name='shop.terminal2main.rpcMoneyExchange',
    index=2,
    containing_service=None,
    input_type=_MONEYEXINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcExchangeInfoReq',
    full_name='shop.terminal2main.rpcExchangeInfoReq',
    index=3,
    containing_service=None,
    input_type=_EXCHANGEINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcMallInfoReq',
    full_name='shop.terminal2main.rpcMallInfoReq',
    index=4,
    containing_service=None,
    input_type=_MALLINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcMallBuy',
    full_name='shop.terminal2main.rpcMallBuy',
    index=5,
    containing_service=None,
    input_type=_MALLINFO,
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
  full_name='shop.main2terminal',
  file=DESCRIPTOR,
  index=1,
  options=None,
  serialized_start=898,
  serialized_end=1124,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcOpenShop',
    full_name='shop.main2terminal.rpcOpenShop',
    index=0,
    containing_service=None,
    input_type=_OPENINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcExchangeInfoRespone',
    full_name='shop.main2terminal.rpcExchangeInfoRespone',
    index=1,
    containing_service=None,
    input_type=_EXCHANGEINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcMallInfoRespone',
    full_name='shop.main2terminal.rpcMallInfoRespone',
    index=2,
    containing_service=None,
    input_type=_MALLINFO,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcOpenPropsExchange',
    full_name='shop.main2terminal.rpcOpenPropsExchange',
    index=3,
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
