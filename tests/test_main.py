from app.main import shortern_url_processor, redirect_url_processor
from app.schemas import LongUrl, ShortUrl
from unittest.mock import Mock


def test_get_short_url():
    Long_Url = LongUrl(long_url="www5")
    Short_Url = ShortUrl(short_url="b0df12f")

    db_accessor_mock = Mock()
    db_accessor_mock.longurl_exists.return_value = False
    db_accessor_mock.insert_url_data.return_value = True

    url_encoder_mock = Mock()
    url_encoder_mock.get_encoding.return_value = "b0df12f"

    shortern_url_processor = Mock(return_value=Short_Url)

    result = shortern_url_processor(Long_Url, db_accessor_mock, url_encoder_mock)
    assert result == Short_Url
    shortern_url_processor.assert_called_once_with(
        Long_Url, db_accessor_mock, url_encoder_mock
    )


def test_get_long_url():
    Long_Url = LongUrl(long_url="www5")
    Short_Url = ShortUrl(short_url="b0df12f")

    db_accessor_mock = Mock()
    db_accessor_mock.shorturl_exists.return_value = True
    db_accessor_mock.get_longurl.return_value = "www5"

    redirect_url_processor = Mock(return_value=Long_Url)

    result = redirect_url_processor(Short_Url, db_accessor_mock)
    assert result == Long_Url
    redirect_url_processor.assert_called_once_with(Short_Url, db_accessor_mock)


# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)


# def test_root():
#     res = client.get("/")
#     assert res.json().get("message") == "this is short url website."
#     assert res.status_code == 200


# def test_shorten_url():
#     res = client.post("/api/v1/shorturl", json={"long_url": "www5"})
#     assert res.json().get("short_url") == "b0df12f"
#     assert res.status_code == 201


# def test_redirect_url_exists():
#     res = client.post("/api/v1/longurl", json={"short_url": "b0df12f"})
#     assert res.json().get("long_url") == "www5"
#     assert res.status_code == 200


# def test_redirect_url_does_not_exist():
#     res = client.post("/api/v1/longurl", json={"short_url": "1234567"})
#     assert res.status_code == 404
