from src.main import health


def test_health_endpoint_logic():
    assert health() == {"status": "ok"}
