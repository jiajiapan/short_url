import app.main
import app.schemas
from unittest.mock import Mock


def test_root_url():
    app.main.root = Mock(return_value = {"message": "this is short url website."})
    result = app.main.root()
    assert result == {"message": "this is short url website."}
    app.main.root.assert_called_once_with()

def test_get_short_url():
    Long_Url = app.schemas.LongUrl(long_url="www5")
    Short_Url = app.schemas.ShortUrl(short_url="b0df12f")

    db_accessor_mock = Mock()
    db_accessor_mock.longurl_exists.return_value = False
    db_accessor_mock.insert_url_data.return_value = True

    url_encoder_mock = Mock()
    url_encoder_mock.get_encoding.return_value = "b0df12f"

    app.main.shortern_url_processor = Mock(return_value=Short_Url)

    result = app.main.shortern_url_processor(Long_Url,db_accessor_mock, url_encoder_mock)
    assert result == Short_Url
    app.main.shortern_url_processor.assert_called_once_with(Long_Url,db_accessor_mock, url_encoder_mock)

def test_get_long_url():
    Long_Url = app.schemas.LongUrl(long_url="www5")
    Short_Url = app.schemas.ShortUrl(short_url="b0df12f")

    db_accessor_mock = Mock()
    db_accessor_mock.shorturl_exists.return_value = True
    db_accessor_mock.get_longurl.return_value = "www5"

    app.main.redirect_url_processor = Mock(return_value=Long_Url)

    result = app.main.redirect_url_processor(Short_Url,db_accessor_mock)
    assert result == Long_Url
    app.main.redirect_url_processor.assert_called_once_with(Short_Url,db_accessor_mock)
