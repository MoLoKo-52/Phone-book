# Phonebook gRPC System

## Server setup

### Install Dependencies


```bash
cd server
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### If `phonebook_pb2.py` and `phonebook_pb2_grpc.py` are missing, generate them using:

```bash
python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/phonebook.proto
```

### Run the server

```bash
python server.py
```

## Flutter Client setup

## Generate gRPC Client Code

```bash

```

## Run the Client

```bash

```