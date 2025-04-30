import grpc
from concurrent import futures
import json
import hmac
import hashlib
import phonebook_pb2
import phonebook_pb2_grpc

SECRET_KEY = b'supersecretkey'
PHONEBOOK: dict = {}
norm_map: dict = {}

def load_phonebook(path: str):
    global PHONEBOOK, norm_map
    with open(path, "r", encoding="utf-8") as f:
        PHONEBOOK = json.load(f)

    norm_map = {}
    for fullname, number in PHONEBOOK.items():
        parts = fullname.strip().lower().split()
        key = " ".join(parts)           
        norm_map[key] = number
        if len(parts) == 2:
            swapped = " ".join(reversed(parts)) 
            norm_map[swapped] = number

def create_server(max_workers: int = 10) -> grpc.Server:
    return grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

def lookup(name: str) -> str:
    parts = name.strip().lower().split()
    key = " ".join(parts)
    return norm_map.get(key, "")

def generate_signature(name: str, number: str, found: bool) -> str:
    msg = f"{name}:{number}:{found}".encode()
    return hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()

class PhonebookServicer(phonebook_pb2_grpc.PhonebookServiceServicer):
    def GetNumberByName(self, request, context):
        raw = request.name
        number = lookup(raw)
        found = bool(number)
        signature = generate_signature(raw, number, found)
        return phonebook_pb2.NumberResponse(
            name=raw,
            number=number,
            found=found,
            signature=signature
        )

def serve():
    print("Loading phonebook...")
    load_phonebook("data.json")

    print("Starting server...")
    server = create_server(max_workers=10)
    phonebook_pb2_grpc.add_PhonebookServiceServicer_to_server(
        PhonebookServicer(), server
    )
    port = server.add_insecure_port("0.0.0.0:50051")
    print(f"Bound to port: {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()