"""OpenRouter API client."""
import asyncio
from typing import Optional

import aiohttp
from tqdm import tqdm

from core.constants import (
    API_TIMEOUT,
    DEFAULT_SYSTEM_PROMPT,
    MAX_RETRIES,
    OPENROUTER_API_URL,
    RETRY_DELAY,
)
from core.exceptions import APIConnectionError, APIResponseError


class OpenRouterClient:
    """OpenRouter API client (async, with retry support)."""

    def __init__(self, api_key: str, model: str, site_url: str = "https://example.com"):
        self.api_key = api_key
        self.model = model
        self.site_url = site_url
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "OpenRouterClient":
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._session:
            await self._session.close()

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-Title": "Content Generator"
        }

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        pbar: Optional[tqdm] = None
    ) -> str:
        """Generate content for a single prompt (with retry)."""
        if not self._session:
            raise RuntimeError("Client must be used with context manager")

        if system_prompt is None:
            system_prompt = DEFAULT_SYSTEM_PROMPT

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }

        last_error: Optional[Exception] = None
        for attempt in range(MAX_RETRIES):
            try:
                async with self._session.post(
                    OPENROUTER_API_URL,
                    headers=self._headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    if pbar:
                        pbar.update(1)
                    return result["choices"][0]["message"]["content"]
            except aiohttp.ClientError as e:
                last_error = APIConnectionError(f"Connection error: {e}")
            except KeyError as e:
                last_error = APIResponseError(f"Unexpected API response: {e}")
            except Exception as e:
                last_error = e

            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))

        raise APIConnectionError(
            f"API call failed after {MAX_RETRIES} attempts: {last_error}"
        )

    async def generate_batch(
        self,
        tasks: list[tuple[str, str]],
        pbar: Optional[tqdm] = None
    ) -> dict[str, str]:
        """Process multiple prompts in parallel."""
        async def _task(name: str, prompt: str) -> tuple[str, str]:
            result = await self.generate(prompt, pbar=pbar)
            return name, result

        results = await asyncio.gather(
            *[_task(name, prompt) for name, prompt in tasks],
            return_exceptions=True
        )

        output = {}
        for item in results:
            if isinstance(item, Exception):
                raise item
            name, content = item
            output[name] = content

        return output
