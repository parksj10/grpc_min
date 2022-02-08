from concurrent import futures
import logging

import grpc, os

import pas_pb2_grpc
import pas_pb2

import flb_tools


class PAS_GRPC(pas_pb2_grpc.PASServicer):
    def getPhotonRecordsStream(self, request: pas_pb2.PhotonRecordsRequest,
                               context):
        raw_data_bytes = flb_tools.read_data_bytes(request.fileName)
        data = flb_tools.reshape_flb_data(raw_data_bytes)

        index = 0
        chunk_size = 1024
        len_data = len(data)
        while index < len_data:
            # last chunk
            if index + chunk_size > len_data:
                yield pas_pb2.PhotonRecordsReply(photonRecords=data[index:])
            # all other chunks
            else:
                yield pas_pb2.PhotonRecordsReply(
                    photonRecords=data[index:index + chunk_size])
            index += chunk_size

    def getPhotonRecordsUnary(self, request: pas_pb2.PhotonRecordsRequest,
                              context):
        raw_data_bytes = flb_tools.read_data_bytes(request.fileName)
        data = flb_tools.reshape_flb_data(raw_data_bytes)
        return pas_pb2.PhotonRecordsReply(photonRecords=data)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pas_pb2_grpc.add_PASServicer_to_server(PAS_GRPC(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
