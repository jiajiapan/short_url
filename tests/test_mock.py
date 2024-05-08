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
    app.main.shorten_url = Mock(return_value=Short_Url)
    result = app.main.shorten_url(Long_Url)
    assert result == Short_Url
    app.main.shorten_url.assert_called_once_with(Long_Url)

def test_get_long_url():
    Long_Url = app.schemas.LongUrl(long_url="www5")
    Short_Url = app.schemas.ShortUrl(short_url="b0df12f")
    app.main.redirect_url = Mock(return_value=Long_Url)
    result = app.main.redirect_url(Short_Url)
    assert result == Long_Url
    app.main.redirect_url.assert_called_once_with(Short_Url)