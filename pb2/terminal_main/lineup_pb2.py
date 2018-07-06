# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lineup.proto

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
  name='lineup.proto',
  package='lineup',
  serialized_pb='\n\x0clineup.proto\x12\x06lineup\x1a\x16universal/public.proto\x1a\x0c\x63ommon.proto\"#\n\x0cskillListMsg\x12\x13\n\x0bskillIdList\x18\x01 \x03(\x05\"\xa1\x01\n\x06\x65yeMsg\x12\r\n\x05\x65yeId\x18\x01 \x01(\x03\x12\r\n\x05\x65yeNo\x18\x02 \x01(\x05\x12\x10\n\x08speRatio\x18\x03 \x01(\x05\x12\'\n\tskillList\x18\x04 \x01(\x0b\x32\x14.lineup.skillListMsg\x12\x0e\n\x06isStar\x18\x05 \x01(\x08\x12\r\n\x05isUse\x18\x06 \x01(\x08\x12\x0e\n\x06roleLv\x18\x07 \x01(\x05\x12\x0f\n\x07stallCD\x18\x08 \x01(\x05\"H\n\tlineupMsg\x12\x10\n\x08lineupId\x18\x01 \x02(\x05\x12\r\n\x05level\x18\x02 \x01(\x05\x12\x0b\n\x03\x65xp\x18\x03 \x01(\x05\x12\r\n\x05\x65yeId\x18\x04 \x01(\x03\"&\n\x08propsMsg\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x0e\n\x06\x61mount\x18\x02 \x02(\x05\"C\n\nupgradeMsg\x12\x10\n\x08lineupId\x18\x01 \x02(\x05\x12#\n\tpropsList\x18\x02 \x03(\x0b\x32\x10.lineup.propsMsg\"l\n\rlineupListMsg\x12\x13\n\x0b\x63urLineupId\x18\x01 \x01(\x05\x12%\n\nlineupList\x18\x02 \x03(\x0b\x32\x11.lineup.lineupMsg\x12\x1f\n\x07\x65yeList\x18\x03 \x03(\x0b\x32\x0e.lineup.eyeMsg2\xce\x01\n\rterminal2main\x12.\n\x0erpcLineupLearn\x12\x0e.common.int32_\x1a\x0c.public.fake\x12\x34\n\x10rpcLineupUpgrade\x12\x12.lineup.upgradeMsg\x1a\x0c.public.fake\x12)\n\trpcEyeUse\x12\x0e.lineup.eyeMsg\x1a\x0c.public.fake\x12,\n\x0crpcEyeChange\x12\x0e.lineup.eyeMsg\x1a\x0c.public.fake2\xdc\x02\n\rmain2terminal\x12\x34\n\rrpcLineupList\x12\x15.lineup.lineupListMsg\x1a\x0c.public.fake\x12/\n\x0crpcLineupAdd\x12\x11.lineup.lineupMsg\x1a\x0c.public.fake\x12/\n\x0frpcLineupDelete\x12\x0e.common.int32_\x1a\x0c.public.fake\x12/\n\x0crpcLineupMod\x12\x11.lineup.lineupMsg\x1a\x0c.public.fake\x12)\n\trpcEyeAdd\x12\x0e.lineup.eyeMsg\x1a\x0c.public.fake\x12,\n\x0crpcEyeDelete\x12\x0e.lineup.eyeMsg\x1a\x0c.public.fake\x12)\n\trpcEyeMod\x12\x0e.lineup.eyeMsg\x1a\x0c.public.fakeB\x03\x90\x01\x01')




_SKILLLISTMSG = _descriptor.Descriptor(
  name='skillListMsg',
  full_name='lineup.skillListMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='skillIdList', full_name='lineup.skillListMsg.skillIdList', index=0,
      number=1, type=5, cpp_type=1, label=3,
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
  serialized_start=62,
  serialized_end=97,
)


_EYEMSG = _descriptor.Descriptor(
  name='eyeMsg',
  full_name='lineup.eyeMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='eyeId', full_name='lineup.eyeMsg.eyeId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='eyeNo', full_name='lineup.eyeMsg.eyeNo', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speRatio', full_name='lineup.eyeMsg.speRatio', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='skillList', full_name='lineup.eyeMsg.skillList', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isStar', full_name='lineup.eyeMsg.isStar', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isUse', full_name='lineup.eyeMsg.isUse', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='roleLv', full_name='lineup.eyeMsg.roleLv', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stallCD', full_name='lineup.eyeMsg.stallCD', index=7,
      number=8, type=5, cpp_type=1, label=1,
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
  serialized_start=100,
  serialized_end=261,
)


_LINEUPMSG = _descriptor.Descriptor(
  name='lineupMsg',
  full_name='lineup.lineupMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lineupId', full_name='lineup.lineupMsg.lineupId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='level', full_name='lineup.lineupMsg.level', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exp', full_name='lineup.lineupMsg.exp', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='eyeId', full_name='lineup.lineupMsg.eyeId', index=3,
      number=4, type=3, cpp_type=2, label=1,
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
  serialized_start=263,
  serialized_end=335,
)


_PROPSMSG = _descriptor.Descriptor(
  name='propsMsg',
  full_name='lineup.propsMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lineup.propsMsg.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='lineup.propsMsg.amount', index=1,
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
  serialized_start=337,
  serialized_end=375,
)


_UPGRADEMSG = _descriptor.Descriptor(
  name='upgradeMsg',
  full_name='lineup.upgradeMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lineupId', full_name='lineup.upgradeMsg.lineupId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='propsList', full_name='lineup.upgradeMsg.propsList', index=1,
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
  serialized_start=377,
  serialized_end=444,
)


_LINEUPLISTMSG = _descriptor.Descriptor(
  name='lineupListMsg',
  full_name='lineup.lineupListMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='curLineupId', full_name='lineup.lineupListMsg.curLineupId', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lineupList', full_name='lineup.lineupListMsg.lineupList', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='eyeList', full_name='lineup.lineupListMsg.eyeList', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=446,
  serialized_end=554,
)

_EYEMSG.fields_by_name['skillList'].message_type = _SKILLLISTMSG
_UPGRADEMSG.fields_by_name['propsList'].message_type = _PROPSMSG
_LINEUPLISTMSG.fields_by_name['lineupList'].message_type = _LINEUPMSG
_LINEUPLISTMSG.fields_by_name['eyeList'].message_type = _EYEMSG
DESCRIPTOR.message_types_by_name['skillListMsg'] = _SKILLLISTMSG
DESCRIPTOR.message_types_by_name['eyeMsg'] = _EYEMSG
DESCRIPTOR.message_types_by_name['lineupMsg'] = _LINEUPMSG
DESCRIPTOR.message_types_by_name['propsMsg'] = _PROPSMSG
DESCRIPTOR.message_types_by_name['upgradeMsg'] = _UPGRADEMSG
DESCRIPTOR.message_types_by_name['lineupListMsg'] = _LINEUPLISTMSG

class skillListMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SKILLLISTMSG

  # @@protoc_insertion_point(class_scope:lineup.skillListMsg)

class eyeMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EYEMSG

  # @@protoc_insertion_point(class_scope:lineup.eyeMsg)

class lineupMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LINEUPMSG

  # @@protoc_insertion_point(class_scope:lineup.lineupMsg)

class propsMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PROPSMSG

  # @@protoc_insertion_point(class_scope:lineup.propsMsg)

class upgradeMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UPGRADEMSG

  # @@protoc_insertion_point(class_scope:lineup.upgradeMsg)

class lineupListMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LINEUPLISTMSG

  # @@protoc_insertion_point(class_scope:lineup.lineupListMsg)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\220\001\001')

_TERMINAL2MAIN = _descriptor.ServiceDescriptor(
  name='terminal2main',
  full_name='lineup.terminal2main',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=557,
  serialized_end=763,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcLineupLearn',
    full_name='lineup.terminal2main.rpcLineupLearn',
    index=0,
    containing_service=None,
    input_type=common_pb2._INT32_,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcLineupUpgrade',
    full_name='lineup.terminal2main.rpcLineupUpgrade',
    index=1,
    containing_service=None,
    input_type=_UPGRADEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcEyeUse',
    full_name='lineup.terminal2main.rpcEyeUse',
    index=2,
    containing_service=None,
    input_type=_EYEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcEyeChange',
    full_name='lineup.terminal2main.rpcEyeChange',
    index=3,
    containing_service=None,
    input_type=_EYEMSG,
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
  full_name='lineup.main2terminal',
  file=DESCRIPTOR,
  index=1,
  options=None,
  serialized_start=766,
  serialized_end=1114,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcLineupList',
    full_name='lineup.main2terminal.rpcLineupList',
    index=0,
    containing_service=None,
    input_type=_LINEUPLISTMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcLineupAdd',
    full_name='lineup.main2terminal.rpcLineupAdd',
    index=1,
    containing_service=None,
    input_type=_LINEUPMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcLineupDelete',
    full_name='lineup.main2terminal.rpcLineupDelete',
    index=2,
    containing_service=None,
    input_type=common_pb2._INT32_,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcLineupMod',
    full_name='lineup.main2terminal.rpcLineupMod',
    index=3,
    containing_service=None,
    input_type=_LINEUPMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcEyeAdd',
    full_name='lineup.main2terminal.rpcEyeAdd',
    index=4,
    containing_service=None,
    input_type=_EYEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcEyeDelete',
    full_name='lineup.main2terminal.rpcEyeDelete',
    index=5,
    containing_service=None,
    input_type=_EYEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcEyeMod',
    full_name='lineup.main2terminal.rpcEyeMod',
    index=6,
    containing_service=None,
    input_type=_EYEMSG,
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
