"""Async worker that consumes ingestion tasks from a queue."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from .pipeline import DocumentIngestionPipeline


@dataclass
class IngestionTask:
    source_uri: str
    knowledge_codes: list[str]


class InMemoryQueue:
    def __init__(self) -> None:
        self._queue: asyncio.Queue[IngestionTask] = asyncio.Queue()

    async def put(self, task: IngestionTask) -> None:
        await self._queue.put(task)

    async def get(self) -> IngestionTask:
        task = await self._queue.get()
        self._queue.task_done()
        return task


class Worker:
    def __init__(self, pipeline: DocumentIngestionPipeline | None = None) -> None:
        self.pipeline = pipeline or DocumentIngestionPipeline()
        self.queue = InMemoryQueue()

    async def start(self) -> None:
        while True:
            task = await self.queue.get()
            self.pipeline.run(task.source_uri, task.knowledge_codes)

    async def enqueue(self, source_uri: str, knowledge_codes: list[str]) -> None:
        await self.queue.put(IngestionTask(source_uri, knowledge_codes))


async def main() -> None:
    worker = Worker()
    await worker.enqueue("sample.txt", ["ALG-001"])
    await asyncio.wait_for(worker.start(), timeout=0.1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.TimeoutError:
        print("Worker processed initial task and shut down (timeout)")
