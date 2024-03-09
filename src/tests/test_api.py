import pytest


@pytest.mark.created_at("2024-03-01 12:00:00")
@pytest.mark.parametrize(
    "qs_from, qs_to, expected_count", (
        (100, 1704099500, 0),
        (1704099601, 1704099602, 0),
        (1709283599, 1709283601, 3),
        (100, 1709283601, 3),
    )
)
def test_get_visited_domains(links, api_client, qs_from, qs_to, expected_count):
    response = api_client.get(f"/visited_domains?from_={qs_from}&to={qs_to}")
    assert len(response.json()["domains"]) == expected_count
