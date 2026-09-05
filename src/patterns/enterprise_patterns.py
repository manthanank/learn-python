"""Production-ready Enterprise Design Patterns implemented in modern Python."""

from __future__ import annotations

import inspect
from collections import defaultdict
from collections.abc import Callable, Generator, Iterable
from typing import Any, TypeVar

T = TypeVar("T")


class DIContainer:
    """Lightweight Inversion of Control / Dependency Injection Container."""

    def __init__(self) -> None:
        self._services: dict[type, Any] = {}
        self._factories: dict[type, Callable[..., Any]] = {}

    def register_singleton(self, service_type: type[T], instance: T) -> None:
        self._services[service_type] = instance

    def register_transient(self, service_type: type[T], factory: Callable[..., T]) -> None:
        self._factories[service_type] = factory

    def resolve(self, service_type: type[T]) -> T:
        if service_type in self._services:
            return self._services[service_type]

        if service_type in self._factories:
            factory = self._factories[service_type]
            sig = inspect.signature(factory)
            kwargs = {}
            for param in sig.parameters.values():
                if param.annotation != inspect.Parameter.empty and param.annotation in self._services:
                    kwargs[param.name] = self.resolve(param.annotation)
            return factory(**kwargs)

        # Attempt automatic constructor injection
        if inspect.isclass(service_type):
            init_sig = inspect.signature(service_type.__init__)
            kwargs = {}
            for name, param in init_sig.parameters.items():
                if name == "self":
                    continue
                if param.annotation in self._services or param.annotation in self._factories:
                    kwargs[name] = self.resolve(param.annotation)
            instance = service_type(**kwargs)
            return instance

        raise KeyError(f"Service {service_type} has not been registered in container")


class EventBus:
    """Decoupled Publisher/Subscriber event notification bus."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Any], Any]]] = defaultdict(list)
        self.published_events_count = 0

    def subscribe(self, topic: str, handler: Callable[[Any], Any]) -> None:
        self._subscribers[topic].append(handler)

    def publish(self, topic: str, payload: Any) -> list[Any]:
        self.published_events_count += 1
        results = []
        for handler in self._subscribers.get(topic, []):
            results.append(handler(payload))
        return results


class StreamPipeline:
    """Lazy streaming data transformation pipeline using Python generators."""

    @staticmethod
    def filter_stream(iterable: Iterable[T], predicate: Callable[[T], bool]) -> Generator[T, None, None]:
        for item in iterable:
            if predicate(item):
                yield item

    @staticmethod
    def map_stream(iterable: Iterable[Any], transform: Callable[[Any], Any]) -> Generator[Any, None, None]:
        for item in iterable:
            yield transform(item)

    @staticmethod
    def batch_stream(iterable: Iterable[T], batch_size: int) -> Generator[list[T], None, None]:
        batch: list[T] = []
        for item in iterable:
            batch.append(item)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
