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
        """Persist or accept an event and return its stable evidence reference."""
        ...


@dataclass(frozen=True)
class ExecutionResult:
    request_id: str
    success: bool
    error_code: str | None = None
    evidence_reference: str | None = None


def execute(request: ExecutionRequest, audit_sink: AuditSink) -> ExecutionResult:
    if not request.request_id:
        result = ExecutionResult(request.request_id, False, "INVALID_REQUEST")
    elif not request.action:
        result = ExecutionResult(request.request_id, False, "INVALID_ACTION")
    elif request.timeout_ms <= 0:
        result = ExecutionResult(request.request_id, False, "INVALID_TIMEOUT")
    else:
        result = ExecutionResult(request.request_id, True)

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
