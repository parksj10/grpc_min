from __future__ import print_function
import logging

import os, time
import grpc

import pas_pb2_grpc
import pas_pb2


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pas_pb2_grpc.PASStub(channel)
        filename = os.path.abspath('short.flb')
        request = pas_pb2.PhotonRecordsRequest(fileName=filename)
        photons_out = []
        s1 = time.time()
        for s in stub.getPhotonRecordsStream(request):
            photons_out.extend(s.photonRecords[:])
        s2 = time.time()
        photons_out_2 = stub.getPhotonRecordsUnary(request).photonRecords[:]
        s3 = time.time()
    print(
        str(s2 - s1) + 's \t' + str(sum(photons_out)) + " photons in " +
        str(len(photons_out)) + " bins")
    print(
        str(s3 - s2) + 's \t' + str(sum(photons_out_2)) + " photons in " +
        str(len(photons_out_2)) + " bins")


if __name__ == "__main__":
    logging.basicConfig()
    run()
