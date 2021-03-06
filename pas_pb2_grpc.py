# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import pas_pb2 as pas__pb2


class PASStub(object):
    """The PAS service definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getPhotonRecordsStream = channel.unary_stream(
                '/pas.PAS/getPhotonRecordsStream',
                request_serializer=pas__pb2.PhotonRecordsRequest.SerializeToString,
                response_deserializer=pas__pb2.PhotonRecordsReply.FromString,
                )
        self.getPhotonRecordsUnary = channel.unary_unary(
                '/pas.PAS/getPhotonRecordsUnary',
                request_serializer=pas__pb2.PhotonRecordsRequest.SerializeToString,
                response_deserializer=pas__pb2.PhotonRecordsReply.FromString,
                )


class PASServicer(object):
    """The PAS service definition
    """

    def getPhotonRecordsStream(self, request, context):
        """get photon records from file (streaming)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getPhotonRecordsUnary(self, request, context):
        """get photon records from file (streaming)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PASServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getPhotonRecordsStream': grpc.unary_stream_rpc_method_handler(
                    servicer.getPhotonRecordsStream,
                    request_deserializer=pas__pb2.PhotonRecordsRequest.FromString,
                    response_serializer=pas__pb2.PhotonRecordsReply.SerializeToString,
            ),
            'getPhotonRecordsUnary': grpc.unary_unary_rpc_method_handler(
                    servicer.getPhotonRecordsUnary,
                    request_deserializer=pas__pb2.PhotonRecordsRequest.FromString,
                    response_serializer=pas__pb2.PhotonRecordsReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'pas.PAS', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PAS(object):
    """The PAS service definition
    """

    @staticmethod
    def getPhotonRecordsStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/pas.PAS/getPhotonRecordsStream',
            pas__pb2.PhotonRecordsRequest.SerializeToString,
            pas__pb2.PhotonRecordsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getPhotonRecordsUnary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pas.PAS/getPhotonRecordsUnary',
            pas__pb2.PhotonRecordsRequest.SerializeToString,
            pas__pb2.PhotonRecordsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
