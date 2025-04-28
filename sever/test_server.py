import pytest
from sever.server import PhonebookServicer, generate_signature, PHONEBOOK
import phonebook_pb2 as pb

servicer = PhonebookServicer()

@pytest.mark.parametrize("query,expected_number,expected_found", [
    ("Leonid Merkulov", PHONEBOOK.get("Leonid Merkulov"), True),
    ("Merkulov Leonid",  PHONEBOOK.get("Leonid Merkulov"), True),
    ("Unknown Person",   "", False),
])
def test_get_number_by_name(query, expected_number, expected_found):
    req = pb.NameRequest(name=query)
    resp = servicer.GetNumberByName(req, None)
    assert resp.number == expected_number
    assert resp.found  == expected_found
    sig = generate_signature(query, resp.number, resp.found)
    assert resp.signature == sig