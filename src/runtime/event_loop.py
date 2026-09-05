"""Educational micro-coroutine event loop scheduler implementing cooperative multitasking."""

from __future__ import annotations

import heapq
import time
from collections import deque
from collections.abc import Callable, Generator
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


@dataclass(order=True)
class ScheduledTimer:
    deadline: float
    callback: Callable[[], Any] = field(compare=False)
    cancelled: bool = field(default=False, compare=False)


class Task:
    """Represents a schedulable coroutine unit of execution."""

    def __init__(self, task_id: str, coroutine: Generator[Any, Any, Any]) -> None:
        self.task_id = task_id
        self.coroutine = coroutine
        self.state = TaskState.PENDING
        self.result: Any = None
        self.error: Exception | None = None

    def step(self) -> bool:
        """Advances the coroutine by one step. Returns True if task is still active."""
        if self.state in (TaskState.DONE, TaskState.CANCELLED):
            return False

        self.state = TaskState.RUNNING
        try:
            # Yield control back to scheduler
            next(self.coroutine)
            self.state = TaskState.PENDING
            return True
        except StopIteration as stop:
            self.state = TaskState.DONE
            self.result = stop.value
            return False
        except Exception as exc:
            self.state = TaskState.DONE
            self.error = exc
            return False

    def cancel(self) -> None:
        self.state = TaskState.CANCELLED


class MicroEventLoop:
    """A minimal, deterministic event loop demonstrating task scheduling and timers."""

    def __init__(self) -> None:
        self.ready_queue: deque[Task] = deque()
        self.timer_heap: list[ScheduledTimer] = []
        self.task_counter = 0
        self.iterations = 0
        self.history: list[dict[str, Any]] = []

    def create_task(self, coroutine: Generator[Any, Any, Any], name: str | None = None) -> Task:
        self.task_counter += 1
        tname = name or f"task-{self.task_counter}"
        task = Task(tname, coroutine)
        self.ready_queue.append(task)
        self.history.append({"event": "task_enqueued", "task_id": tname, "tick": self.iterations})
        return task

    def call_later(self, delay_seconds: float, callback: Callable[[], Any]) -> ScheduledTimer:
        deadline = time.perf_counter() + delay_seconds
        timer = ScheduledTimer(deadline, callback)
        heapq.heappush(self.timer_heap, timer)
        return timer

    def run_until_complete(self, max_ticks: int = 1000) -> dict[str, Any]:
        """Runs the loop until ready queue and timers are exhausted or max ticks reached."""
        while (self.ready_queue or self.timer_heap) and self.iterations < max_ticks:
            self.iterations += 1

            # 1. Process expired timers
            now = time.perf_counter()
            while self.timer_heap and self.timer_heap[0].deadline <= now:
                timer = heapq.heappop(self.timer_heap)
                if not timer.cancelled:
                    timer.callback()
                    self.history.append({"event": "timer_fired", "tick": self.iterations})

            # 2. Process ready queue tasks for this tick
            if self.ready_queue:
                task = self.ready_queue.popleft()
                is_active = task.step()
                self.history.append({
                    "event": "task_stepped",
                    "task_id": task.task_id,
                    "state": task.state.value,
                    "tick": self.iterations,
                })
                if is_active:
                    self.ready_queue.append(task)

            # Small cooperative sleep if waiting on timers only
            if not self.ready_queue and self.timer_heap:
                time.sleep(0.005)

        return {
            "total_ticks": self.iterations,
            "tasks_scheduled": self.task_counter,
            "events_recorded": len(self.history),
            "history": self.history[-25:],  # Return latest 25 events
        }
