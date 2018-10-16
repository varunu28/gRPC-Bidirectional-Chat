# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import messenger_pb2 as messenger__pb2


class MessengerServerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.MessageStream = channel.unary_stream(
        '/messenger.MessengerServer/MessageStream',
        request_serializer=messenger__pb2.Key.SerializeToString,
        response_deserializer=messenger__pb2.Text.FromString,
        )
    self.SendMessage = channel.stream_stream(
        '/messenger.MessengerServer/SendMessage',
        request_serializer=messenger__pb2.Text.SerializeToString,
        response_deserializer=messenger__pb2.SendConfirmation.FromString,
        )
    self.ValidateUser = channel.unary_unary(
        '/messenger.MessengerServer/ValidateUser',
        request_serializer=messenger__pb2.User.SerializeToString,
        response_deserializer=messenger__pb2.SendConfirmation.FromString,
        )
    self.RegisterKey = channel.unary_unary(
        '/messenger.MessengerServer/RegisterKey',
        request_serializer=messenger__pb2.Key.SerializeToString,
        response_deserializer=messenger__pb2.Empty.FromString,
        )
    self.ReturnUsers = channel.unary_unary(
        '/messenger.MessengerServer/ReturnUsers',
        request_serializer=messenger__pb2.User.SerializeToString,
        response_deserializer=messenger__pb2.User.FromString,
        )


class MessengerServerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def MessageStream(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendMessage(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ValidateUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RegisterKey(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReturnUsers(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MessengerServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'MessageStream': grpc.unary_stream_rpc_method_handler(
          servicer.MessageStream,
          request_deserializer=messenger__pb2.Key.FromString,
          response_serializer=messenger__pb2.Text.SerializeToString,
      ),
      'SendMessage': grpc.stream_stream_rpc_method_handler(
          servicer.SendMessage,
          request_deserializer=messenger__pb2.Text.FromString,
          response_serializer=messenger__pb2.SendConfirmation.SerializeToString,
      ),
      'ValidateUser': grpc.unary_unary_rpc_method_handler(
          servicer.ValidateUser,
          request_deserializer=messenger__pb2.User.FromString,
          response_serializer=messenger__pb2.SendConfirmation.SerializeToString,
      ),
      'RegisterKey': grpc.unary_unary_rpc_method_handler(
          servicer.RegisterKey,
          request_deserializer=messenger__pb2.Key.FromString,
          response_serializer=messenger__pb2.Empty.SerializeToString,
      ),
      'ReturnUsers': grpc.unary_unary_rpc_method_handler(
          servicer.ReturnUsers,
          request_deserializer=messenger__pb2.User.FromString,
          response_serializer=messenger__pb2.User.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'messenger.MessengerServer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
