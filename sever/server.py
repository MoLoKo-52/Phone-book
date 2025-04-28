import grpc
from concurrent import futures
import json
import hmac
import hashlib
import phonebook_pb2
import phonebook_pb2_grpc

def load_phonebook(path: str):
    global PHONEBOOK
    with open(path, "r", encoding="utf-8") as f:
        PHONEBOOK = json.load(f)

def create_server(max_workers: int = 10) -> grpc.Server:
    return grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

SECRET_KEY = b'supersecretkey'

with open("data.json") as f:
    PHONEBOOK = json.load(f)

def generate_signature(name, number, found):
    message = f"{name}:{number}:{found}".encode()
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

class PhonebookServicer(phonebook_pb2_grpc.PhonebookServiceServicer):
    def GetNumberByName(self, request, context):
        raw = request.name.strip()

        number = PHONEBOOK.get(raw)

        if number is None:
            parts = raw.split()
            if len(parts) == 2:
                swapped = f"{parts[1]} {parts[0]}"
                number = PHONEBOOK.get(swapped)

        found = number is not None
        if not found:
            number = ""

        signature = generate_signature(raw, number, found)

        return phonebook_pb2.NumberResponse(
            name=raw,
            number=number,
            found=found,
            signature=signature
        )

def serve():
    print("Loading phonebook...")
    with open("data.json") as f:
        PHONEBOOK = json.load(f)

    print("Setting up server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=500))
    phonebook_pb2_grpc.add_PhonebookServiceServicer_to_server(PhonebookServicer(), server)
    port = server.add_insecure_port('0.0.0.0:50051')
    print(f"Bound to port: {port}")
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()