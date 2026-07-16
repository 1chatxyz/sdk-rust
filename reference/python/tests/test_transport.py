from myconversation.transport import auth_metadata, normalize_grpc_base_url, should_use_grpc_web_transport


def test_normalize_https_host():
    assert normalize_grpc_base_url("gateway01.example.com") == "https://gateway01.example.com:443"


def test_normalize_http_with_port():
    assert normalize_grpc_base_url("myconversation.svc:8080") == "http://myconversation.svc:8080"


def test_grpc_web_for_https():
    assert should_use_grpc_web_transport("https://gateway01.example.com") is True
    assert should_use_grpc_web_transport("http://localhost:8080") is False


def test_auth_metadata():
    md = auth_metadata("tenant-1", "tok123")
    assert ("authorization", "Bearer tok123") in md
    assert ("x-tenant-id", "tenant-1") in md
