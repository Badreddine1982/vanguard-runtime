from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str
    action: str
    timeout_ms: int


@dataclass(frozen=True)
class ExecutionResult:
    request_id: str
    success: bool
    error_code: str | None = None
    evidence_reference: str | None = None


def execute(request: ExecutionRequest) -> ExecutionResult:
    if not request.request_id:
        return ExecutionResult(request.request_id, False, "INVALID_REQUEST")
    if not request.action:
        return ExecutionResult(request.request_id, False, "INVALID_ACTION")
    if request.timeout_ms <= 0:
        return ExecutionResult(request.request_id, False, "INVALID_TIMEOUT")
    return ExecutionResult(request.request_id, True)
