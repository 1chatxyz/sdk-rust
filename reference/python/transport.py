from __future__ import annotations


def normalize_grpc_base_url(endpoint: str) -> str:
    trimmed = endpoint.strip()
    if trimmed.startswith("http://") or trimmed.startswith("https://"):
        return trimmed

    # host:port without scheme — gateway01 is TLS (443); in-cluster listeners use plain HTTP.
    if trimmed.endswith(":443"):
        return f"https://{trimmed}"

    colon = trimmed.rfind(":")
    has_port = colon > 0 and trimmed[colon + 1 :].isdigit()
    if has_port:
        return f"http://{trimmed}"

    looks_internal = (
        ".svc." in trimmed or trimmed.startswith("127.") or trimmed == "localhost"
    )
    if looks_internal:
        return f"http://{trimmed}"

    return f"https://{trimmed}:443"


def should_use_grpc_web_transport(base_url: str) -> bool:
    """gateway01 (HTTPS / Cloudflare) speaks grpc-web; in-cluster HTTP listeners use native gRPC."""
    return base_url.startswith("https://")


def auth_metadata(tenant_id: str, token: str) -> list[tuple[str, str]]:
    return [
        ("authorization", f"Bearer {token}"),
        ("x-tenant-id", tenant_id),
    ]
