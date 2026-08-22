from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from library.services.spotify.client import SpotifyClient


@pytest.mark.asyncio
async def test_get():
    http_client = MagicMock()

    response = MagicMock()
    response.json.return_value = {"id": "123"}
    response.raise_for_status.return_value = None

    http_client.get = AsyncMock(return_value=response)

    client = SpotifyClient(http_client)

    result = await client.get(
        "/me",
        "access-token",
    )

    http_client.get.assert_awaited_once_with(
        "https://api.spotify.com/v1/me",
        headers={
            "Authorization": "Bearer access-token",
        },
        params=None,
    )

    response.raise_for_status.assert_called_once_with()

    assert result == {"id": "123"}


@pytest.mark.asyncio
async def test_get_403():
    http_client = MagicMock()

    response = MagicMock()

    request = httpx.Request(
        "GET",
        "https://api.spotify.com/v1/me",
    )

    http_response = httpx.Response(
        403,
        request=request,
    )

    response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "403 Forbidden",
        request=request,
        response=http_response,
    )

    http_client.get = AsyncMock(return_value=response)

    client = SpotifyClient(http_client)

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await client.get(
            "/me",
            "access-token",
        )

    assert exc_info.value.response.status_code == 403