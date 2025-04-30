import time
import grpc
import pytest
import hmac
import hashlib
import phonebook_pb2 as pb
import phonebook_pb2_grpc as rpc
from sever.server import load_phonebook, create_server, PhonebookServicer, PHONEBOOK

@pytest.fixture(scope="module")
def grpc_server():
    load_phonebook("data.json")
    server = create_server()
    rpc.add_PhonebookServiceServicer_to_server(PhonebookServicer(), server)
    port = server.add_insecure_port("localhost:0")
    server.start()
    time.sleep(0.1)
    yield port
    server.stop(0)

def test_integration_lookup(grpc_server):
    port = grpc_server
    channel = grpc.insecure_channel(f"localhost:{port}")
    stub   = rpc.PhonebookServiceStub(channel)
    resp = stub.GetNumberByName(pb.NameRequest(name="Leonid Merkulov"))
    assert resp.found is True
    assert resp.number == PHONEBOOK["Leonid Merkulov"]
    sig = hmac.new(
        b'supersecretkey',
        f"Leonid Merkulov:{resp.number}:{resp.found}".encode(),
        hashlib.sha256
    ).hexdigest()
    assert resp.signature == sig