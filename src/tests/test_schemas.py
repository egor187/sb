import pytest

from core.schemas import QSDateFilterSchema


@pytest.mark.parametrize(
    "from_, to, raises", (
        (1, 2, False),
        (2, 1, True),
        (2, 9999999999999999999999, True),
        (123123123, 231231231, False),
        (-1, -2, True),
    )
)
def test_date_filter_schema(from_, to, raises):
    if raises:
        with pytest.raises(ValueError):
            QSDateFilterSchema(from_=from_, to=to)
    else:
        QSDateFilterSchema(from_=from_, to=to)

