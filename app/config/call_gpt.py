"""OpenAI GPT API 호출 모듈."""

import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()

# 환경 변수 검증
MAX_TOKENS_ENV = os.getenv("MAX_TOKENS")
if not MAX_TOKENS_ENV:
    raise ValueError("MAX_TOKENS environment variable is required")

try:
    MAX_TOKENS = int(MAX_TOKENS_ENV)
except ValueError as e:
    raise ValueError(f"MAX_TOKENS must be a valid integer: {e}") from e

# OpenAI 클라이언트 초기화
_client: Optional[OpenAI] = None


def get_client() -> OpenAI:
    """OpenAI 클라이언트 싱글톤 인스턴스를 반환합니다."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def _create_chat_completion_sync(prompt: str) -> str:
    """동기 방식으로 GPT API를 호출합니다.
    
    Args:
        prompt: 사용자 프롬프트
        
    Returns:
        GPT 응답 텍스트
        
    Raises:
        ValueError: 프롬프트가 비어있는 경우
        Exception: OpenAI API 호출 실패 시
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    client = get_client()
    
    # 타입 안전성을 위해 딕셔너리를 명시적으로 구성
    message: dict[str, str] = {"role": "user", "content": prompt}
    messages: list[ChatCompletionMessageParam] = [
        message  # type: ignore[list-item]
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=0,
        )
        
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("GPT API returned empty response")
        
        return content
    except Exception as e:
        raise Exception(f"Failed to call GPT API: {str(e)}") from e


class CallGPT:
    """OpenAI GPT API를 비동기로 호출하는 클래스."""

    @staticmethod
    async def call_gpt(prompt: str) -> str:
        """비동기 방식으로 GPT API를 호출합니다.
        
        Args:
            prompt: 사용자 프롬프트
            
        Returns:
            GPT 응답 텍스트
            
        Raises:
            ValueError: 프롬프트가 비어있는 경우
            Exception: OpenAI API 호출 실패 시
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _create_chat_completion_sync, prompt)
