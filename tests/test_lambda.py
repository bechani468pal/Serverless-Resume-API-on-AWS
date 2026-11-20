from src import lambda_function


def test_personal_endpoint(monkeypatch):

    def mock_get_item(Key):
        return {
            "Item": {
                "PK": "RESUME",
                "SK": "PERSONAL",
                "data": {
                    "name": "Test User",
                    "email": "test@example.com"
                }
            }
        }

    monkeypatch.setattr(
        lambda_function.table,
        "get_item",
        mock_get_item
    )

    event = {"rawPath": "/resume/personal"}

    result = lambda_function.lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert "Test User" in result["body"]


def test_invalid_endpoint():

    event = {"rawPath": "/resume/invalid"}

    result = lambda_function.lambda_handler(event, None)

    assert result["statusCode"] == 404


def test_missing_section(monkeypatch):

    monkeypatch.setattr(
        lambda_function.table,
        "get_item",
        lambda Key: {}
    )

    event = {"rawPath": "/resume/education"}

    result = lambda_function.lambda_handler(event, None)

    assert result["statusCode"] == 404


def test_complete_resume(monkeypatch):

    def mock_query(**kwargs):
        return {
            "Items": [
                {
                    "PK": "RESUME",
                    "SK": "PERSONAL",
                    "data": {"name": "Test User"}
                },
                {
                    "PK": "RESUME",
                    "SK": "SKILLS",
                    "data": ["Python", "AWS"]
                }
            ]
        }

    monkeypatch.setattr(
        lambda_function.table,
        "query",
        mock_query
    )

    event = {"rawPath": "/resume"}

    result = lambda_function.lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert "personal" in result["body"]
    assert "skills" in result["body"]
    