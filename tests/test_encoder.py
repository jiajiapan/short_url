from app.encoder import Encoder
from unittest.mock import Mock


def test_get_bits():
    db_accessor_mock = Mock()
    db_accessor_mock.return_value = True

    encoder = Encoder(db_accessor_mock)
    encoder.get_bits = Mock(return_value="b0df12f")
    result = encoder.get_bits("www5")
    assert result == "b0df12f"
    encoder.get_bits.assert_called_once_with("www5")

def test_check_collision():
    db_accessor_mock = Mock()
    db_accessor_mock.longurl_exists.return_value = False
    db_accessor_mock.shorturl_exists.return_value = False

    encoder = Encoder(db_accessor_mock)
    encoder.check_collision = Mock(return_value=False)
    result = encoder.check_collision("www5","b0df12f")
    assert result == False
    encoder.check_collision.assert_called_once_with("www5","b0df12f")

def test_get_encoding():
    db_accessor_mock = Mock()
    db_accessor_mock.return_value = True

    encoder = Encoder(db_accessor_mock)
    encoder.get_encoding = Mock(return_value="b0df12f")
    result = encoder.get_encoding("www5")
    assert result == "b0df12f"
    encoder.get_encoding.assert_called_once_with("www5")
