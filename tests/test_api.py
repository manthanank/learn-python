"""Tests for FastAPI endpoints using Starlette/FastAPI TestClient."""

from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_api_disassemble():
    res = client.post("/api/bytecode/disassemble", json={"code": "x = 10 + 20"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["instructions"]) > 0


def test_api_gc_endpoints():
    res = client.get("/api/memory/gc")
    assert res.status_code == 200
    data = res.json()
    assert data["is_enabled"] is True

    res_cycle = client.post("/api/memory/cyclic-garbage")
    assert res_cycle.status_code == 200
    assert "unreachable_objects_collected" in res_cycle.json()


def test_api_runtime_endpoints():
    res_mro = client.get("/api/runtime/mro")
    assert res_mro.status_code == 200
    assert len(res_mro.json()["linearization_order"]) > 0

    res_loop = client.post("/api/runtime/eventloop-demo")
    assert res_loop.status_code == 200
    assert res_loop.json()["total_ticks"] > 0


def test_api_sandbox_execution():
    res = client.post("/api/sandbox/execute", json={"code": "val = 15 * 2\nprint('Computed:', val)"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Computed: 30" in data["stdout"]
    assert data["variables"].get("val") == "30"


def test_api_sandbox_security_guard():
    res = client.post("/api/sandbox/execute", json={"code": "import os; os.system('ls')"})
    assert res.status_code == 400
    assert "prohibited" in res.json()["detail"]
