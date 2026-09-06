from knowledge_base import verify_entity


def test_verify_known_company():
    result = verify_entity("Googl", "company")  
    assert result["verified"] is True
    assert result["matched_to"] == "Google"


def test_verify_unknown_company():
    result = verify_entity("Totally Made Up Corp Inc", "company")
    assert result["verified"] is False
