# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connection.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='connection.proto',
  package='connection',
  serialized_pb='\n\x10\x63onnection.proto\x12\nconnection\"m\n\x0e\x63onnectionInfo\x12\x16\n\x0eiGateServiceId\x18\x01 \x02(\x05\x12\x0f\n\x07iConnId\x18\x02 \x02(\x05\x12\x0b\n\x03sIP\x18\x03 \x02(\x0c\x12\r\n\x05iPort\x18\x04 \x02(\x05\x12\x16\n\x08iTimeout\x18\x05 \x01(\r:\x04\x31\x30\x30\x30\x42\x03\x90\x01\x01')




_CONNECTIONINFO = _descriptor.Descriptor(
  name='connectionInfo',
  full_name='connection.connectionInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iGateServiceId', full_name='connection.connectionInfo.iGateServiceId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iConnId', full_name='connection.connectionInfo.iConnId', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sIP', full_name='connection.connectionInfo.sIP', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iPort', full_name='connection.connectionInfo.iPort', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iTimeout', full_name='connection.connectionInfo.iTimeout', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=1000,
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
  serialized_start=32,
  serialized_end=141,
)

DESCRIPTOR.message_types_by_name['connectionInfo'] = _CONNECTIONINFO

class connectionInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CONNECTIONINFO

  # @@protoc_insertion_point(class_scope:connection.connectionInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\220\001\001')
# @@protoc_insertion_point(module_scope)