
import pytest


@pytest.fixture(name='once_conflict_mock')
def fixture_once_conflict_mock(mocker):
    def _once_conflict_mock(conflict_positions):
        _conflict_positions = conflict_positions

        def _mock_is_conflict(color, grid, x, y):
            nonlocal _conflict_positions

            if (x, y) in _conflict_positions:
                _conflict_positions.remove((x, y))
                return True

            return False

        mock = mocker.MagicMock()
        mock.side_effect = _mock_is_conflict

        return mock

    return _once_conflict_mock
