# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='base.proto',
  package='base',
  serialized_pb='\n\nbase.proto\x12\x04\x62\x61se\"\x18\n\x06int32_\x12\x0e\n\x06iValue\x18\x01 \x02(\x05\"\x18\n\x06int64_\x12\x0e\n\x06iValue\x18\x01 \x02(\x03\"\x18\n\x06uin32_\x12\x0e\n\x06iValue\x18\x01 \x02(\r\"\x19\n\x07sint32_\x12\x0e\n\x06iValue\x18\x01 \x02(\x11\"\x19\n\x07sint64_\x12\x0e\n\x06iValue\x18\x01 \x02(\x12\"\x1a\n\x08\x66ixed32_\x12\x0e\n\x06iValue\x18\x01 \x02(\x07\"\x1a\n\x08\x66ixed64_\x12\x0e\n\x06iValue\x18\x01 \x02(\x06\"\x1b\n\tsfixed32_\x12\x0e\n\x06iValue\x18\x01 \x02(\x0f\"\x1b\n\tsfixed64_\x12\x0e\n\x06iValue\x18\x01 \x02(\x10\"\x18\n\x06\x62ytes_\x12\x0e\n\x06sValue\x18\x01 \x02(\x0c\"\x17\n\x05\x62ool_\x12\x0e\n\x06\x62Value\x18\x01 \x02(\x08\"\x18\n\x06\x66loat_\x12\x0e\n\x06\x66Value\x18\x01 \x02(\x02\"\x19\n\x07\x64ouble_\x12\x0e\n\x06\x66Value\x18\x01 \x02(\x01\"-\n\tint32Pair\x12\x0f\n\x07iValue1\x18\x01 \x02(\x05\x12\x0f\n\x07iValue2\x18\x02 \x02(\x05\"-\n\tint64Pair\x12\x0f\n\x07iValue1\x18\x01 \x02(\x03\x12\x0f\n\x07iValue2\x18\x02 \x02(\x03\"-\n\tbytesPair\x12\x0f\n\x07sValue1\x18\x01 \x02(\x0c\x12\x0f\n\x07sValue2\x18\x02 \x02(\x0c\"0\n\nint32int64\x12\x10\n\x08iValue32\x18\x01 \x02(\x05\x12\x10\n\x08iValue64\x18\x02 \x02(\x03\"4\n\x0cuint32uint64\x12\x11\n\tiValueU32\x18\x01 \x02(\r\x12\x11\n\tiValueU64\x18\x02 \x02(\x04')




_INT32_ = _descriptor.Descriptor(
  name='int32_',
  full_name='base.int32_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.int32_.iValue', index=0,
      number=1, type=5, cpp_type=1, label=2,
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
  serialized_start=20,
  serialized_end=44,
)


_INT64_ = _descriptor.Descriptor(
  name='int64_',
  full_name='base.int64_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.int64_.iValue', index=0,
      number=1, type=3, cpp_type=2, label=2,
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
  serialized_start=46,
  serialized_end=70,
)


_UIN32_ = _descriptor.Descriptor(
  name='uin32_',
  full_name='base.uin32_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.uin32_.iValue', index=0,
      number=1, type=13, cpp_type=3, label=2,
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
  serialized_start=72,
  serialized_end=96,
)


_SINT32_ = _descriptor.Descriptor(
  name='sint32_',
  full_name='base.sint32_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.sint32_.iValue', index=0,
      number=1, type=17, cpp_type=1, label=2,
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
  serialized_start=98,
  serialized_end=123,
)


_SINT64_ = _descriptor.Descriptor(
  name='sint64_',
  full_name='base.sint64_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.sint64_.iValue', index=0,
      number=1, type=18, cpp_type=2, label=2,
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
  serialized_start=125,
  serialized_end=150,
)


_FIXED32_ = _descriptor.Descriptor(
  name='fixed32_',
  full_name='base.fixed32_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.fixed32_.iValue', index=0,
      number=1, type=7, cpp_type=3, label=2,
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
  serialized_start=152,
  serialized_end=178,
)


_FIXED64_ = _descriptor.Descriptor(
  name='fixed64_',
  full_name='base.fixed64_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.fixed64_.iValue', index=0,
      number=1, type=6, cpp_type=4, label=2,
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
  serialized_start=180,
  serialized_end=206,
)


_SFIXED32_ = _descriptor.Descriptor(
  name='sfixed32_',
  full_name='base.sfixed32_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.sfixed32_.iValue', index=0,
      number=1, type=15, cpp_type=1, label=2,
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
  serialized_start=208,
  serialized_end=235,
)


_SFIXED64_ = _descriptor.Descriptor(
  name='sfixed64_',
  full_name='base.sfixed64_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue', full_name='base.sfixed64_.iValue', index=0,
      number=1, type=16, cpp_type=2, label=2,
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
  serialized_start=237,
  serialized_end=264,
)


_BYTES_ = _descriptor.Descriptor(
  name='bytes_',
  full_name='base.bytes_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sValue', full_name='base.bytes_.sValue', index=0,
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
  serialized_start=266,
  serialized_end=290,
)


_BOOL_ = _descriptor.Descriptor(
  name='bool_',
  full_name='base.bool_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bValue', full_name='base.bool_.bValue', index=0,
      number=1, type=8, cpp_type=7, label=2,
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
  serialized_start=292,
  serialized_end=315,
)


_FLOAT_ = _descriptor.Descriptor(
  name='float_',
  full_name='base.float_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fValue', full_name='base.float_.fValue', index=0,
      number=1, type=2, cpp_type=6, label=2,
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
  serialized_start=317,
  serialized_end=341,
)


_DOUBLE_ = _descriptor.Descriptor(
  name='double_',
  full_name='base.double_',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fValue', full_name='base.double_.fValue', index=0,
      number=1, type=1, cpp_type=5, label=2,
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
  serialized_start=343,
  serialized_end=368,
)


_INT32PAIR = _descriptor.Descriptor(
  name='int32Pair',
  full_name='base.int32Pair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue1', full_name='base.int32Pair.iValue1', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iValue2', full_name='base.int32Pair.iValue2', index=1,
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
  serialized_start=370,
  serialized_end=415,
)


_INT64PAIR = _descriptor.Descriptor(
  name='int64Pair',
  full_name='base.int64Pair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue1', full_name='base.int64Pair.iValue1', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iValue2', full_name='base.int64Pair.iValue2', index=1,
      number=2, type=3, cpp_type=2, label=2,
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
  serialized_start=417,
  serialized_end=462,
)


_BYTESPAIR = _descriptor.Descriptor(
  name='bytesPair',
  full_name='base.bytesPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sValue1', full_name='base.bytesPair.sValue1', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sValue2', full_name='base.bytesPair.sValue2', index=1,
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
  serialized_start=464,
  serialized_end=509,
)


_INT32INT64 = _descriptor.Descriptor(
  name='int32int64',
  full_name='base.int32int64',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValue32', full_name='base.int32int64.iValue32', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iValue64', full_name='base.int32int64.iValue64', index=1,
      number=2, type=3, cpp_type=2, label=2,
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
  serialized_start=511,
  serialized_end=559,
)


_UINT32UINT64 = _descriptor.Descriptor(
  name='uint32uint64',
  full_name='base.uint32uint64',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iValueU32', full_name='base.uint32uint64.iValueU32', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iValueU64', full_name='base.uint32uint64.iValueU64', index=1,
      number=2, type=4, cpp_type=4, label=2,
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
  serialized_start=561,
  serialized_end=613,
)

DESCRIPTOR.message_types_by_name['int32_'] = _INT32_
DESCRIPTOR.message_types_by_name['int64_'] = _INT64_
DESCRIPTOR.message_types_by_name['uin32_'] = _UIN32_
DESCRIPTOR.message_types_by_name['sint32_'] = _SINT32_
DESCRIPTOR.message_types_by_name['sint64_'] = _SINT64_
DESCRIPTOR.message_types_by_name['fixed32_'] = _FIXED32_
DESCRIPTOR.message_types_by_name['fixed64_'] = _FIXED64_
DESCRIPTOR.message_types_by_name['sfixed32_'] = _SFIXED32_
DESCRIPTOR.message_types_by_name['sfixed64_'] = _SFIXED64_
DESCRIPTOR.message_types_by_name['bytes_'] = _BYTES_
DESCRIPTOR.message_types_by_name['bool_'] = _BOOL_
DESCRIPTOR.message_types_by_name['float_'] = _FLOAT_
DESCRIPTOR.message_types_by_name['double_'] = _DOUBLE_
DESCRIPTOR.message_types_by_name['int32Pair'] = _INT32PAIR
DESCRIPTOR.message_types_by_name['int64Pair'] = _INT64PAIR
DESCRIPTOR.message_types_by_name['bytesPair'] = _BYTESPAIR
DESCRIPTOR.message_types_by_name['int32int64'] = _INT32INT64
DESCRIPTOR.message_types_by_name['uint32uint64'] = _UINT32UINT64

class int32_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INT32_

  # @@protoc_insertion_point(class_scope:base.int32_)

class int64_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INT64_

  # @@protoc_insertion_point(class_scope:base.int64_)

class uin32_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UIN32_

  # @@protoc_insertion_point(class_scope:base.uin32_)

class sint32_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SINT32_

  # @@protoc_insertion_point(class_scope:base.sint32_)

class sint64_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SINT64_

  # @@protoc_insertion_point(class_scope:base.sint64_)

class fixed32_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FIXED32_

  # @@protoc_insertion_point(class_scope:base.fixed32_)

class fixed64_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FIXED64_

  # @@protoc_insertion_point(class_scope:base.fixed64_)

class sfixed32_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SFIXED32_

  # @@protoc_insertion_point(class_scope:base.sfixed32_)

class sfixed64_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SFIXED64_

  # @@protoc_insertion_point(class_scope:base.sfixed64_)

class bytes_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BYTES_

  # @@protoc_insertion_point(class_scope:base.bytes_)

class bool_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BOOL_

  # @@protoc_insertion_point(class_scope:base.bool_)

class float_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FLOAT_

  # @@protoc_insertion_point(class_scope:base.float_)

class double_(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DOUBLE_

  # @@protoc_insertion_point(class_scope:base.double_)

class int32Pair(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INT32PAIR

  # @@protoc_insertion_point(class_scope:base.int32Pair)

class int64Pair(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INT64PAIR

  # @@protoc_insertion_point(class_scope:base.int64Pair)

class bytesPair(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BYTESPAIR

  # @@protoc_insertion_point(class_scope:base.bytesPair)

class int32int64(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INT32INT64

  # @@protoc_insertion_point(class_scope:base.int32int64)

class uint32uint64(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UINT32UINT64

  # @@protoc_insertion_point(class_scope:base.uint32uint64)


# @@protoc_insertion_point(module_scope)
