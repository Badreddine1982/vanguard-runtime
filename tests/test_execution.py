from src.execution import ExecutionRequest, execute


def test_valid_request_succeeds():
    result = execute(ExecutionRequest("req-1", "noop", 1000))
    assert result.success is True
    assert result.request_id == "req-1"
    assert result.error_code is None


def test_missing_action_is_deterministic_error():
    result = execute(ExecutionRequest("req-2", "", 1000))
    assert result.success is False
    assert result.error_code == "INVALID_ACTION"


def test_invalid_timeout_is_deterministic_error():
    result = execute(ExecutionRequest("req-3", "noop", 0))
    assert result.success is False
    assert result.error_code == "INVALID_TIMEOUT"
