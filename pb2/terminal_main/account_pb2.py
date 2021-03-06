# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: account.proto

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
  name='account.proto',
  package='account',
  serialized_pb='\n\raccount.proto\x12\x07\x61\x63\x63ount\x1a\x16universal/public.proto\x1a\x0c\x63ommon.proto\"\xdf\x01\n\x0f\x61\x63\x63ountLoginReq\x12\x10\n\x08sAccount\x18\x01 \x02(\x0c\x12\x13\n\x0bsUserSource\x18\x02 \x02(\x0c\x12\x39\n\x07iOStype\x18\x03 \x02(\x0e\x32\x1f.account.accountLoginReq.OStype:\x07\x41NDROID\x12\x13\n\x0bsLoginAppId\x18\x05 \x02(\x0c\x12\x16\n\x0esRegisterAppId\x18\x06 \x02(\x0c\x12\x0e\n\x06sToken\x18\x04 \x01(\x0c\"-\n\x06OStype\x12\r\n\tWIN_PHONE\x10\x01\x12\x0b\n\x07\x41NDROID\x10\x02\x12\x07\n\x03IOS\x10\x04\"W\n\x08roleInfo\x12\x0f\n\x07iRoleId\x18\x01 \x02(\x04\x12\x11\n\tsRoleName\x18\x02 \x01(\x0c\x12\x12\n\niRoleLevel\x18\x03 \x01(\r\x12\x13\n\x0biRoleSchool\x18\x04 \x01(\x05\",\n\x08roleList\x12 \n\x05roles\x18\x01 \x03(\x0b\x32\x11.account.roleInfo\"0\n\rcreateRoleReq\x12\x0f\n\x07iSchool\x18\x02 \x02(\x05\x12\x0e\n\x06iShape\x18\x03 \x01(\x05\"-\n\x0bsetRoleName\x12\x0f\n\x07iRoleId\x18\x01 \x02(\x03\x12\r\n\x05sName\x18\x02 \x02(\x0c\"\xc4\x01\n\x04test\x12\t\n\x01\x64\x18\x01 \x01(\x01\x12\t\n\x01\x66\x18\x02 \x01(\x02\x12\x0b\n\x03i32\x18\x03 \x01(\x05\x12\x0b\n\x03i64\x18\x04 \x01(\x03\x12\x0b\n\x03u32\x18\x05 \x01(\r\x12\x0b\n\x03u64\x18\x06 \x01(\x04\x12\x0c\n\x04si32\x18\x07 \x01(\x11\x12\x0c\n\x04si64\x18\x08 \x01(\x12\x12\x0b\n\x03\x66\x33\x32\x18\t \x01(\x07\x12\x0b\n\x03\x66\x36\x34\x18\n \x01(\x06\x12\x0c\n\x04sf32\x18\x0b \x01(\x0f\x12\x0c\n\x04sf64\x18\x0c \x01(\x10\x12\t\n\x01\x62\x18\r \x01(\x08\x12\t\n\x01s\x18\x0e \x01(\t\x12\n\n\x02\x62y\x18\x0f \x01(\x0c\"\x1f\n\x08robotMsg\x12\x13\n\x0b\x61\x63\x63ountName\x18\x01 \x02(\x0c\"9\n\x10\x61\x63\x63ountLoginResp\x12\x12\n\nbSuccessed\x18\x01 \x02(\x08\x12\x11\n\ttimeStamp\x18\x02 \x01(\x03\x32\xba\x04\n\rterminal2main\x12\x46\n\x0frpcAccountLogin\x12\x18.account.accountLoginReq\x1a\x19.account.accountLoginResp\x12\x36\n\rrpcCreateRole\x12\x16.account.createRoleReq\x1a\r.common.bool_\x12+\n\nrpcDelRole\x12\x0e.common.int64_\x1a\r.common.bool_\x12+\n\rrpcSwitchRole\x12\x0c.public.fake\x1a\x0c.public.fake\x12/\n\x0erpcSetRoleName\x12\x0e.common.bytes_\x1a\r.common.bool_\x12\x32\n\x12rpcForceRemoveRole\x12\x0c.public.fake\x1a\x0e.common.int32_\x12-\n\x0crpcReconnect\x12\x0e.common.int64_\x1a\r.common.bool_\x12.\n\x10rpcAccountLogOut\x12\x0c.public.fake\x1a\x0c.public.fake\x12,\n\x0crpcRoleLogin\x12\x0e.common.int64_\x1a\x0c.public.fake\x12+\n\rrpcRandomName\x12\x0c.public.fake\x1a\x0c.public.fake\x12\x30\n\rrpcRobotLogin\x12\x11.account.robotMsg\x1a\x0c.public.fake2\x94\x01\n\rmain2terminal\x12.\n\x0brpcRoleList\x12\x11.account.roleList\x1a\x0c.public.fake\x12+\n\x0brpcSendName\x12\x0e.common.bytes_\x1a\x0c.public.fake\x12&\n\x07rpcTest\x12\r.account.test\x1a\x0c.public.fakeB\x03\x90\x01\x01')



_ACCOUNTLOGINREQ_OSTYPE = _descriptor.EnumDescriptor(
  name='OStype',
  full_name='account.accountLoginReq.OStype',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WIN_PHONE', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANDROID', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IOS', index=2, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=243,
  serialized_end=288,
)


_ACCOUNTLOGINREQ = _descriptor.Descriptor(
  name='accountLoginReq',
  full_name='account.accountLoginReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sAccount', full_name='account.accountLoginReq.sAccount', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sUserSource', full_name='account.accountLoginReq.sUserSource', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iOStype', full_name='account.accountLoginReq.iOStype', index=2,
      number=3, type=14, cpp_type=8, label=2,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sLoginAppId', full_name='account.accountLoginReq.sLoginAppId', index=3,
      number=5, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sRegisterAppId', full_name='account.accountLoginReq.sRegisterAppId', index=4,
      number=6, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sToken', full_name='account.accountLoginReq.sToken', index=5,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ACCOUNTLOGINREQ_OSTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=65,
  serialized_end=288,
)


_ROLEINFO = _descriptor.Descriptor(
  name='roleInfo',
  full_name='account.roleInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iRoleId', full_name='account.roleInfo.iRoleId', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sRoleName', full_name='account.roleInfo.sRoleName', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iRoleLevel', full_name='account.roleInfo.iRoleLevel', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iRoleSchool', full_name='account.roleInfo.iRoleSchool', index=3,
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
  serialized_start=290,
  serialized_end=377,
)


_ROLELIST = _descriptor.Descriptor(
  name='roleList',
  full_name='account.roleList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='roles', full_name='account.roleList.roles', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=379,
  serialized_end=423,
)


_CREATEROLEREQ = _descriptor.Descriptor(
  name='createRoleReq',
  full_name='account.createRoleReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iSchool', full_name='account.createRoleReq.iSchool', index=0,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iShape', full_name='account.createRoleReq.iShape', index=1,
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
  serialized_start=425,
  serialized_end=473,
)


_SETROLENAME = _descriptor.Descriptor(
  name='setRoleName',
  full_name='account.setRoleName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iRoleId', full_name='account.setRoleName.iRoleId', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sName', full_name='account.setRoleName.sName', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  serialized_start=475,
  serialized_end=520,
)


_TEST = _descriptor.Descriptor(
  name='test',
  full_name='account.test',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='d', full_name='account.test.d', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='f', full_name='account.test.f', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='i32', full_name='account.test.i32', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='i64', full_name='account.test.i64', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='u32', full_name='account.test.u32', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='u64', full_name='account.test.u64', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='si32', full_name='account.test.si32', index=6,
      number=7, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='si64', full_name='account.test.si64', index=7,
      number=8, type=18, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='f32', full_name='account.test.f32', index=8,
      number=9, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='f64', full_name='account.test.f64', index=9,
      number=10, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sf32', full_name='account.test.sf32', index=10,
      number=11, type=15, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sf64', full_name='account.test.sf64', index=11,
      number=12, type=16, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='b', full_name='account.test.b', index=12,
      number=13, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='s', full_name='account.test.s', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='by', full_name='account.test.by', index=14,
      number=15, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
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
  serialized_start=523,
  serialized_end=719,
)


_ROBOTMSG = _descriptor.Descriptor(
  name='robotMsg',
  full_name='account.robotMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='accountName', full_name='account.robotMsg.accountName', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  serialized_start=721,
  serialized_end=752,
)


_ACCOUNTLOGINRESP = _descriptor.Descriptor(
  name='accountLoginResp',
  full_name='account.accountLoginResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bSuccessed', full_name='account.accountLoginResp.bSuccessed', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timeStamp', full_name='account.accountLoginResp.timeStamp', index=1,
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
  serialized_start=754,
  serialized_end=811,
)

_ACCOUNTLOGINREQ.fields_by_name['iOStype'].enum_type = _ACCOUNTLOGINREQ_OSTYPE
_ACCOUNTLOGINREQ_OSTYPE.containing_type = _ACCOUNTLOGINREQ;
_ROLELIST.fields_by_name['roles'].message_type = _ROLEINFO
DESCRIPTOR.message_types_by_name['accountLoginReq'] = _ACCOUNTLOGINREQ
DESCRIPTOR.message_types_by_name['roleInfo'] = _ROLEINFO
DESCRIPTOR.message_types_by_name['roleList'] = _ROLELIST
DESCRIPTOR.message_types_by_name['createRoleReq'] = _CREATEROLEREQ
DESCRIPTOR.message_types_by_name['setRoleName'] = _SETROLENAME
DESCRIPTOR.message_types_by_name['test'] = _TEST
DESCRIPTOR.message_types_by_name['robotMsg'] = _ROBOTMSG
DESCRIPTOR.message_types_by_name['accountLoginResp'] = _ACCOUNTLOGINRESP

class accountLoginReq(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ACCOUNTLOGINREQ

  # @@protoc_insertion_point(class_scope:account.accountLoginReq)

class roleInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ROLEINFO

  # @@protoc_insertion_point(class_scope:account.roleInfo)

class roleList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ROLELIST

  # @@protoc_insertion_point(class_scope:account.roleList)

class createRoleReq(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CREATEROLEREQ

  # @@protoc_insertion_point(class_scope:account.createRoleReq)

class setRoleName(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SETROLENAME

  # @@protoc_insertion_point(class_scope:account.setRoleName)

class test(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TEST

  # @@protoc_insertion_point(class_scope:account.test)

class robotMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ROBOTMSG

  # @@protoc_insertion_point(class_scope:account.robotMsg)

class accountLoginResp(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ACCOUNTLOGINRESP

  # @@protoc_insertion_point(class_scope:account.accountLoginResp)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\220\001\001')

_TERMINAL2MAIN = _descriptor.ServiceDescriptor(
  name='terminal2main',
  full_name='account.terminal2main',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=814,
  serialized_end=1384,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcAccountLogin',
    full_name='account.terminal2main.rpcAccountLogin',
    index=0,
    containing_service=None,
    input_type=_ACCOUNTLOGINREQ,
    output_type=_ACCOUNTLOGINRESP,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcCreateRole',
    full_name='account.terminal2main.rpcCreateRole',
    index=1,
    containing_service=None,
    input_type=_CREATEROLEREQ,
    output_type=common_pb2._BOOL_,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcDelRole',
    full_name='account.terminal2main.rpcDelRole',
    index=2,
    containing_service=None,
    input_type=common_pb2._INT64_,
    output_type=common_pb2._BOOL_,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcSwitchRole',
    full_name='account.terminal2main.rpcSwitchRole',
    index=3,
    containing_service=None,
    input_type=universal.public_pb2._FAKE,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcSetRoleName',
    full_name='account.terminal2main.rpcSetRoleName',
    index=4,
    containing_service=None,
    input_type=common_pb2._BYTES_,
    output_type=common_pb2._BOOL_,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcForceRemoveRole',
    full_name='account.terminal2main.rpcForceRemoveRole',
    index=5,
    containing_service=None,
    input_type=universal.public_pb2._FAKE,
    output_type=common_pb2._INT32_,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcReconnect',
    full_name='account.terminal2main.rpcReconnect',
    index=6,
    containing_service=None,
    input_type=common_pb2._INT64_,
    output_type=common_pb2._BOOL_,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcAccountLogOut',
    full_name='account.terminal2main.rpcAccountLogOut',
    index=7,
    containing_service=None,
    input_type=universal.public_pb2._FAKE,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcRoleLogin',
    full_name='account.terminal2main.rpcRoleLogin',
    index=8,
    containing_service=None,
    input_type=common_pb2._INT64_,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcRandomName',
    full_name='account.terminal2main.rpcRandomName',
    index=9,
    containing_service=None,
    input_type=universal.public_pb2._FAKE,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcRobotLogin',
    full_name='account.terminal2main.rpcRobotLogin',
    index=10,
    containing_service=None,
    input_type=_ROBOTMSG,
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
  full_name='account.main2terminal',
  file=DESCRIPTOR,
  index=1,
  options=None,
  serialized_start=1387,
  serialized_end=1535,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcRoleList',
    full_name='account.main2terminal.rpcRoleList',
    index=0,
    containing_service=None,
    input_type=_ROLELIST,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcSendName',
    full_name='account.main2terminal.rpcSendName',
    index=1,
    containing_service=None,
    input_type=common_pb2._BYTES_,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcTest',
    full_name='account.main2terminal.rpcTest',
    index=2,
    containing_service=None,
    input_type=_TEST,
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
