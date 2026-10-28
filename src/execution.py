import asyncio
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str
    action: str
    timeout_ms: int


@dataclass(frozen=True)
class AuditEvent:
    request_id: str
    action: str
    success: bool
    error_code: str | None


class AuditSink(Protocol):
    def emit(self, event: AuditEvent) -> str:
        """Accept an event and return its stable evidence reference."""
        ...


class ActionExecutor(Protocol):
    async def execute(self, action: str) -> None:
        """Run an action asynchronously; cancellation must be cooperative."""
        ...


@dataclass(frozen=True)
class ExecutionResult:
    request_id: str
    success: bool
    error_code: str | None = None
    evidence_reference: str | None = None


CANCELLATION_GRACE_MS = 50


async def _run_with_deadline(
    executor: ActionExecutor, action: str, timeout_ms: int
) -> str | None:
    task = asyncio.create_task(executor.execute(action))
    done, _ = await asyncio.wait({task}, timeout=timeout_ms / 1000)
    if task in done:
        await task
        return None

    task.cancel()
    done, _ = await asyncio.wait(
        {task}, timeout=CANCELLATION_GRACE_MS / 1000
    )
    if task in done and task.cancelled():
        return "EXECUTION_TIMEOUT"

    # The executor either suppressed cancellation or did not settle promptly.
    # Do not claim the action stopped or that its side effects did not occur.
    return "EXECUTION_STATE_UNKNOWN"


async def execute(
    request: ExecutionRequest,
    audit_sink: AuditSink,
    action_executor: ActionExecutor,
) -> ExecutionResult:
    if not request.request_id:
        result = ExecutionResult(request.request_id, False, "INVALID_REQUEST")
    elif not request.action:
        result = ExecutionResult(request.request_id, False, "INVALID_ACTION")
    elif request.timeout_ms <= 0:
        result = ExecutionResult(request.request_id, False, "INVALID_TIMEOUT")
    else:
        try:
            error_code = await _run_with_deadline(
                action_executor, request.action, request.timeout_ms
            )
            result = ExecutionResult(
                request.request_id, error_code is None, error_code
            )
        except Exception:
            result = ExecutionResult(
                request.request_id, False, "EXECUTION_FAILURE"
            )

    event = AuditEvent(
        request_id=request.request_id,
        action=request.action,
        success=result.success,
        error_code=result.error_code,
    )
    try:
        reference = audit_sink.emit(event)
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError("AuditSink must return a non-empty evidence reference")
    except Exception:
        return ExecutionResult(
            request.request_id, False, "AUDIT_SINK_FAILURE", None
        )

    return ExecutionResult(
        request_id=result.request_id,
        success=result.success,
        error_code=result.error_code,
        evidence_reference=reference,
    )
