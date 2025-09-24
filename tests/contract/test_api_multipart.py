import pytest
from func_bank.api_multipart import handle_multipart


class MockRequest:
    def __init__(self, files=None, form=None):
        self.files = files or {}
        self.form = form or {}


def test_handle_multipart_success():
    """Test successful parsing of multipart request with files and data."""
    # This test will fail until implementation
    request = MockRequest(files={'file1': b'content1'}, form={'data': 'value'})
    result = handle_multipart(request)
    assert isinstance(result, dict)
    assert 'files' in result
    assert 'data' in result
    assert result['files']['file1'] == b'content1'
    assert result['data']['data'] == 'value'


def test_handle_multipart_no_files():
    """Test multipart request with no files returns empty dict."""
    request = MockRequest()
    result = handle_multipart(request)
    assert result == {}


def test_handle_multipart_size_limit():
    """Test multipart request exceeding size limits raises error."""
    large_content = b'x' * 1000001  # Assume 1MB limit
    request = MockRequest(files={'large_file': large_content})
    with pytest.raises(Exception):  # Well-documented error
        handle_multipart(request)