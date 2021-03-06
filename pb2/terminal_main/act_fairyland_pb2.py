# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: act_fairyland.proto

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


DESCRIPTOR = _descriptor.FileDescriptor(
  name='act_fairyland.proto',
  package='act_fairyland',
  serialized_pb='\n\x13\x61\x63t_fairyland.proto\x12\ract_fairyland\x1a\x16universal/public.proto\x1a\x0c\x63ommon.proto\x1a\x0bprops.proto\"4\n\x07infoMsg\x12\x12\n\niPassStage\x18\x01 \x01(\x05\x12\x15\n\riSurplusCount\x18\x02 \x01(\x05\"w\n\x08stageMsg\x12\x10\n\x08iStageNo\x18\x01 \x02(\x05\x12\x11\n\tiFastTime\x18\x02 \x01(\x05\x12\x11\n\tsFastName\x18\x03 \x01(\x0c\x12\x0f\n\x07iMyTime\x18\x04 \x01(\x05\x12\x10\n\x08\x62\x43\x61nSkip\x18\x05 \x01(\x08\x12\x10\n\x08iTimeOut\x18\x06 \x01(\x05\"\x9d\x01\n\x06npcMsg\x12\x0b\n\x03iId\x18\x01 \x02(\x03\x12\r\n\x05sName\x18\x02 \x01(\x0c\x12\x0e\n\x06iShape\x18\x03 \x01(\x05\x12\n\n\x02iX\x18\x04 \x01(\x05\x12\n\n\x02iY\x18\x05 \x01(\x05\x12\n\n\x02iD\x18\x06 \x01(\x05\x12\x12\n\nshapeParts\x18\x07 \x03(\x05\x12\x0e\n\x06sTitle\x18\x08 \x01(\x0c\x12\x0e\n\x06\x63olors\x18\t \x03(\x05\x12\x0f\n\x07iAction\x18\n \x01(\x05\"1\n\x0c\x62oxRewardMsg\x12\x10\n\x08iPropsNo\x18\x01 \x01(\x05\x12\x0f\n\x07iAmount\x18\x02 \x01(\x05\"P\n\x0f\x62oxRewardResult\x12\x0c\n\x04iPos\x18\x01 \x02(\x05\x12/\n\nrewardList\x18\x02 \x03(\x0b\x32\x1b.act_fairyland.boxRewardMsg2\xb2\x03\n\rterminal2main\x12/\n\x11rpcFairylandEnter\x12\x0c.public.fake\x1a\x0c.public.fake\x12.\n\x10rpcFairylandQuit\x12\x0c.public.fake\x1a\x0c.public.fake\x12=\n\x14rpcFairylandStageGet\x12\x17.act_fairyland.stageMsg\x1a\x0c.public.fake\x12?\n\x16rpcFairylandStageFight\x12\x17.act_fairyland.stageMsg\x1a\x0c.public.fake\x12\x39\n\x10rpcFairylandPass\x12\x17.act_fairyland.stageMsg\x1a\x0c.public.fake\x12>\n\x15rpcFairylandTaskQuest\x12\x17.act_fairyland.stageMsg\x1a\x0c.public.fake\x12\x45\n\x15rpcFairylandBoxChoose\x12\x1e.act_fairyland.boxRewardResult\x1a\x0c.public.fake2\xb7\x03\n\rmain2terminal\x12\x39\n\x11rpcFairylandBegin\x12\x16.act_fairyland.infoMsg\x1a\x0c.public.fake\x12:\n\x12rpcFairylandChange\x12\x16.act_fairyland.infoMsg\x1a\x0c.public.fake\x12-\n\x0frpcFairylandEnd\x12\x0c.public.fake\x1a\x0c.public.fake\x12\x38\n\x10rpcFairylandInfo\x12\x16.act_fairyland.infoMsg\x1a\x0c.public.fake\x12>\n\x15rpcFairylandStageSend\x12\x17.act_fairyland.stageMsg\x1a\x0c.public.fake\x12\x39\n\x19rpcFairylandBoxRewardOpen\x12\x0e.common.int32_\x1a\x0c.public.fake\x12K\n\x1brpcFairylandBoxRewardResult\x12\x1e.act_fairyland.boxRewardResult\x1a\x0c.public.fakeB\x03\x90\x01\x01')




_INFOMSG = _descriptor.Descriptor(
  name='infoMsg',
  full_name='act_fairyland.infoMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPassStage', full_name='act_fairyland.infoMsg.iPassStage', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iSurplusCount', full_name='act_fairyland.infoMsg.iSurplusCount', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=89,
  serialized_end=141,
)


_STAGEMSG = _descriptor.Descriptor(
  name='stageMsg',
  full_name='act_fairyland.stageMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iStageNo', full_name='act_fairyland.stageMsg.iStageNo', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iFastTime', full_name='act_fairyland.stageMsg.iFastTime', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sFastName', full_name='act_fairyland.stageMsg.sFastName', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iMyTime', full_name='act_fairyland.stageMsg.iMyTime', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bCanSkip', full_name='act_fairyland.stageMsg.bCanSkip', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iTimeOut', full_name='act_fairyland.stageMsg.iTimeOut', index=5,
      number=6, type=5, cpp_type=1, label=1,
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
  serialized_start=143,
  serialized_end=262,
)


_NPCMSG = _descriptor.Descriptor(
  name='npcMsg',
  full_name='act_fairyland.npcMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iId', full_name='act_fairyland.npcMsg.iId', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sName', full_name='act_fairyland.npcMsg.sName', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iShape', full_name='act_fairyland.npcMsg.iShape', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iX', full_name='act_fairyland.npcMsg.iX', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iY', full_name='act_fairyland.npcMsg.iY', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iD', full_name='act_fairyland.npcMsg.iD', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shapeParts', full_name='act_fairyland.npcMsg.shapeParts', index=6,
      number=7, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sTitle', full_name='act_fairyland.npcMsg.sTitle', index=7,
      number=8, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='colors', full_name='act_fairyland.npcMsg.colors', index=8,
      number=9, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iAction', full_name='act_fairyland.npcMsg.iAction', index=9,
      number=10, type=5, cpp_type=1, label=1,
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
  serialized_start=265,
  serialized_end=422,
)


_BOXREWARDMSG = _descriptor.Descriptor(
  name='boxRewardMsg',
  full_name='act_fairyland.boxRewardMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPropsNo', full_name='act_fairyland.boxRewardMsg.iPropsNo', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iAmount', full_name='act_fairyland.boxRewardMsg.iAmount', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=424,
  serialized_end=473,
)


_BOXREWARDRESULT = _descriptor.Descriptor(
  name='boxRewardResult',
  full_name='act_fairyland.boxRewardResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iPos', full_name='act_fairyland.boxRewardResult.iPos', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rewardList', full_name='act_fairyland.boxRewardResult.rewardList', index=1,
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
  serialized_start=475,
  serialized_end=555,
)

_BOXREWARDRESULT.fields_by_name['rewardList'].message_type = _BOXREWARDMSG
DESCRIPTOR.message_types_by_name['infoMsg'] = _INFOMSG
DESCRIPTOR.message_types_by_name['stageMsg'] = _STAGEMSG
DESCRIPTOR.message_types_by_name['npcMsg'] = _NPCMSG
DESCRIPTOR.message_types_by_name['boxRewardMsg'] = _BOXREWARDMSG
DESCRIPTOR.message_types_by_name['boxRewardResult'] = _BOXREWARDRESULT

class infoMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INFOMSG

  # @@protoc_insertion_point(class_scope:act_fairyland.infoMsg)

class stageMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STAGEMSG

  # @@protoc_insertion_point(class_scope:act_fairyland.stageMsg)

class npcMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _NPCMSG

  # @@protoc_insertion_point(class_scope:act_fairyland.npcMsg)

class boxRewardMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BOXREWARDMSG

  # @@protoc_insertion_point(class_scope:act_fairyland.boxRewardMsg)

class boxRewardResult(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BOXREWARDRESULT

  # @@protoc_insertion_point(class_scope:act_fairyland.boxRewardResult)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\220\001\001')

_TERMINAL2MAIN = _descriptor.ServiceDescriptor(
  name='terminal2main',
  full_name='act_fairyland.terminal2main',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=558,
  serialized_end=992,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcFairylandEnter',
    full_name='act_fairyland.terminal2main.rpcFairylandEnter',
    index=0,
    containing_service=None,
    input_type=universal.public_pb2._FAKE,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandQuit',
    full_name='act_fairyland.terminal2main.rpcFairylandQuit',
    index=1,
    containing_service=None,
    input_type=universal.public_pb2._FAKE,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandStageGet',
    full_name='act_fairyland.terminal2main.rpcFairylandStageGet',
    index=2,
    containing_service=None,
    input_type=_STAGEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandStageFight',
    full_name='act_fairyland.terminal2main.rpcFairylandStageFight',
    index=3,
    containing_service=None,
    input_type=_STAGEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandPass',
    full_name='act_fairyland.terminal2main.rpcFairylandPass',
    index=4,
    containing_service=None,
    input_type=_STAGEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandTaskQuest',
    full_name='act_fairyland.terminal2main.rpcFairylandTaskQuest',
    index=5,
    containing_service=None,
    input_type=_STAGEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandBoxChoose',
    full_name='act_fairyland.terminal2main.rpcFairylandBoxChoose',
    index=6,
    containing_service=None,
    input_type=_BOXREWARDRESULT,
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
  full_name='act_fairyland.main2terminal',
  file=DESCRIPTOR,
  index=1,
  options=None,
  serialized_start=995,
  serialized_end=1434,
  methods=[
  _descriptor.MethodDescriptor(
    name='rpcFairylandBegin',
    full_name='act_fairyland.main2terminal.rpcFairylandBegin',
    index=0,
    containing_service=None,
    input_type=_INFOMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandChange',
    full_name='act_fairyland.main2terminal.rpcFairylandChange',
    index=1,
    containing_service=None,
    input_type=_INFOMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandEnd',
    full_name='act_fairyland.main2terminal.rpcFairylandEnd',
    index=2,
    containing_service=None,
    input_type=universal.public_pb2._FAKE,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandInfo',
    full_name='act_fairyland.main2terminal.rpcFairylandInfo',
    index=3,
    containing_service=None,
    input_type=_INFOMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandStageSend',
    full_name='act_fairyland.main2terminal.rpcFairylandStageSend',
    index=4,
    containing_service=None,
    input_type=_STAGEMSG,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandBoxRewardOpen',
    full_name='act_fairyland.main2terminal.rpcFairylandBoxRewardOpen',
    index=5,
    containing_service=None,
    input_type=common_pb2._INT32_,
    output_type=universal.public_pb2._FAKE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='rpcFairylandBoxRewardResult',
    full_name='act_fairyland.main2terminal.rpcFairylandBoxRewardResult',
    index=6,
    containing_service=None,
    input_type=_BOXREWARDRESULT,
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
