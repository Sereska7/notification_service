"""Lifespan function."""

import asyncio
from contextlib import asynccontextmanager

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI

from app.internal.workers import Workers
from app.internal.workers.email_sender import EmailSenderWorker


@inject
@asynccontextmanager
async def lifespan(
    app: FastAPI,  # pylint: disable=unused-argument
    mail_sender_worker: EmailSenderWorker = Provide[Workers.mail_sender_worker],
):
    app.state.shutting_down = False
    mail_sender_worker_task = asyncio.create_task(mail_sender_worker.listen_sending_message())

    yield
    app.state.shutting_down = True
    mail_sender_worker_task.cancel()

    try:
        await mail_sender_worker_task
    except asyncio.CancelledError:
        pass

    await shutdown_event()


async def shutdown_event() -> None:
    pending = [
        task for task in asyncio.all_tasks() if task is not asyncio.current_task()
    ]
    for task in pending:
        task.cancel()

    await asyncio.gather(*pending, return_exceptions=True)
