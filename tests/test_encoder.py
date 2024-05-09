from app.encoder import Encoder
import app.schemas
from unittest.mock import Mock


# def test_get_bits():
#     encoder = Encoder()
#     encoder.get_bits = Mock(return_value = {"message": "this is short url website."})
#     result = app.main.root()
#     assert result == {"message": "this is short url website."}
#     app.main.root.assert_called_once_with()

# def test_check_collision():
#     app.main.root = Mock(return_value = {"message": "this is short url website."})
#     result = app.main.root()
#     assert result == {"message": "this is short url website."}
#     app.main.root.assert_called_once_with()

# def test_get_encoding():
#     app.main.root = Mock(return_value = {"message": "this is short url website."})
#     result = app.main.root()
#     assert result == {"message": "this is short url website."}
#     app.main.root.assert_called_once_with()
