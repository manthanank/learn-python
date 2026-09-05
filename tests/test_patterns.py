"""Tests for enterprise design patterns in Python."""

from src.patterns.enterprise_patterns import DIContainer, EventBus, StreamPipeline


class DatabaseClient:
    def __init__(self, dsn: str = "sqlite:///:memory:") -> None:
        self.dsn = dsn


class UserService:
    def __init__(self, db: DatabaseClient) -> None:
        self.db = db


def test_di_container():
    container = DIContainer()
    db = DatabaseClient("postgres://localhost:5432")
    container.register_singleton(DatabaseClient, db)

    svc = container.resolve(UserService)
    assert svc.db is db
    assert svc.db.dsn == "postgres://localhost:5432"


def test_event_bus():
    bus = EventBus()
    events = []

    bus.subscribe("user_registered", lambda payload: events.append(payload))
    bus.publish("user_registered", {"user_id": 42})

    assert len(events) == 1
    assert events[0]["user_id"] == 42


def test_stream_pipeline():
    numbers = range(10)
    evens = StreamPipeline.filter_stream(numbers, lambda x: x % 2 == 0)
    doubled = StreamPipeline.map_stream(evens, lambda x: x * 2)
    batches = list(StreamPipeline.batch_stream(doubled, batch_size=2))

    # Evens: 0, 2, 4, 6, 8 -> Doubled: 0, 4, 8, 12, 16 -> Batches: [[0, 4], [8, 12], [16]]
    assert batches == [[0, 4], [8, 12], [16]]
