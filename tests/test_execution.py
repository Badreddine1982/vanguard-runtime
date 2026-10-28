import asyncio

from src.execution import AuditEvent, ExecutionRequest, execute


class InMemoryAuditSink:
    def __init__(self):
        self.events = []

    def emit(self, event: AuditEvent) -> str:
        self.events.append(event)
        return f"audit://{event.request_id or 'invalid-request'}/{len(self.events)}"


class NoopExecutor:
    async def execute(self, action: str) -> None:
        assert action == "noop"


def run(request, sink, executor=None):
    return asyncio.run(execute(request, sink, executor or NoopExecutor()))


def test_valid_request_succeeds_and_emits_audit_event():
    sink = InMemoryAuditSink()
    result = run(ExecutionRequest("req-1", "noop", 1000), sink)

    assert result.success is True
    assert result.request_id == "req-1"
    assert result.error_code is None
    assert result.evidence_reference
    assert sink.events == [AuditEvent("req-1", "noop", True, None)]


def test_missing_action_is_deterministic_error_and_audited():
    sink = InMemoryAuditSink()
    result = run(ExecutionRequest("req-2", "", 1000), sink)

    assert result.success is False
    assert result.error_code == "INVALID_ACTION"
    assert sink.events == [AuditEvent("req-2", "", False, "INVALID_ACTION")]


def test_invalid_timeout_is_deterministic_error_and_audited():
    sink = InMemoryAuditSink()
    result = run(ExecutionRequest("req-3", "noop", 0), sink)

    assert result.success is False
    assert result.error_code == "INVALID_TIMEOUT"
    assert sink.events == [AuditEvent("req-3", "noop", False, "INVALID_TIMEOUT")]


def test_missing_request_id_is_audited():
    sink = InMemoryAuditSink()
    result = run(ExecutionRequest("", "noop", 1000), sink)

    assert result.success is False
    assert result.error_code == "INVALID_REQUEST"
    assert len(sink.events) == 1
    assert sink.events[0].request_id == ""


def test_long_running_action_is_cancelled_at_deadline():
    class SlowExecutor:
        async def execute(self, action):
            await asyncio.sleep(1)

    sink = InMemoryAuditSink()
    result = run(ExecutionRequest("req-timeout", "slow", 10), sink, SlowExecutor())

    assert result.success is False
    assert result.error_code == "EXECUTION_TIMEOUT"
    assert sink.events == [
        AuditEvent("req-timeout", "slow", False, "EXECUTION_TIMEOUT")
    ]


def test_uncertain_cancellation_does_not_claim_clean_timeout():
    class CancellationSuppressingExecutor:
        async def execute(self, action):
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                return

    sink = InMemoryAuditSink()
    result = run(
        ExecutionRequest("req-unknown", "slow", 10),
        sink,
        CancellationSuppressingExecutor(),
    )

    assert result.success is False
    assert result.error_code == "EXECUTION_STATE_UNKNOWN"
    assert sink.events == [
        AuditEvent("req-unknown", "slow", False, "EXECUTION_STATE_UNKNOWN")
    ]


def test_audit_sink_failure_fails_closed():
    class BrokenSink:
        def emit(self, event):
            raise OSError("sink unavailable")

    result = run(ExecutionRequest("req-4", "noop", 1000), BrokenSink())

    assert result.success is False
    assert result.error_code == "AUDIT_SINK_FAILURE"
    assert result.evidence_reference is None
