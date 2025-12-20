from fastapi import APIRouter, HTTPException, Query, Depends

from app.message_log.adapter.input.web.request import SendMessageRequest
from app.message_log.adapter.input.web.response import MessageResponse, MessageListResponse
from app.message_log.application.usecase.create_message_usecase import CreateMessageUseCase
from app.message_log.application.usecase.get_messages_usecase import GetMessagesUseCase
from app.config.security.message_crypto import AESEncryption
from app.message_log.domain.entity import MessageRole, ContentType
# 하드코딩으로 변경
def get_current_user() -> int:
    """현재 사용자 ID (테스트용 하드코딩)"""
    return 1  # TODO: 실제 인증 로직으로 교체

# Router 생성
router = APIRouter(tags=["message_log"])


# Dependency: Encryption
def get_encryption() -> AESEncryption:
    """암호화 어댑터 의존성"""
    return AESEncryption()


@router.post(
    "/rooms/{room_id}/messages",
    response_model=MessageResponse,
    summary="메시지 전송",
    description="채팅방에 메시지를 전송합니다. 원본 메시지는 AES-256으로 암호화되어 저장됩니다."
)
def send_message(
    room_id: str,
    request: SendMessageRequest,
    user_id: int = Depends(get_current_user)  # 기존 프로젝트의 인증 방식
):
    """
    메시지 전송

    - room_id: 채팅방 ID
    - request: 메시지 내용 (암호화되어 저장됨)
    - user_id: 현재 사용자 ID (인증에서 자동 추출)
    """
    try:
        # UseCase 생성
        usecase = CreateMessageUseCase()

        # 메시지 생성
        message = usecase.execute(
            room_id=room_id,
            account_id=user_id,
            content=request.content,
            role=MessageRole[request.role],
            content_type=ContentType[request.content_type],
            img_url=request.img_url
        )

        # 응답 생성 (원본 내용은 포함하지 않음)
        return MessageResponse(
            message_id=message.id,
            chat_room_id=message.chat_room_id,
            account_id=message.account_id,
            role=message.role.value,
            content_type=message.contents_type.value,
            img_url=message.img_url,
            created_at=message.created_at
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메시지 전송 실패: {str(e)}")


@router.get(
    "/rooms/{room_id}/messages",
    response_model=MessageListResponse,
    summary="메시지 목록 조회",
    description="채팅방의 메시지 목록을 조회합니다. 보안상 원본 내용은 반환되지 않습니다."
)
def get_messages(
    room_id: str,
    limit: int = Query(default=50, ge=1, le=100, description="조회 개수"),
    offset: int = Query(default=0, ge=0, description="오프셋")
):
    """
    메시지 목록 조회

    - room_id: 채팅방 ID
    - limit: 조회 개수 (1-100)
    - offset: 오프셋

    주의: 보안상 원본 메시지 내용은 반환되지 않습니다.
    """
    try:
        # UseCase 생성
        usecase = GetMessagesUseCase()

        # 메시지 조회
        messages, total_count = usecase.get_by_room_id(room_id, limit, offset)

        # 응답 생성 (원본 내용 제외)
        message_responses = [
            MessageResponse(
                message_id=msg.id,
                chat_room_id=msg.chat_room_id,
                account_id=msg.account_id,
                role=msg.role.value,
                content_type=msg.contents_type.value,
                img_url=msg.img_url,
                created_at=msg.created_at
            )
            for msg in messages
        ]

        return MessageListResponse(
            messages=message_responses,
            total_count=total_count,
            limit=limit,
            offset=offset
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메시지 조회 실패: {str(e)}")


@router.get(
    "/test/encryption",
    summary="암호화 테스트",
    description="AES-256 암호화 테스트 엔드포인트"
)
def test_encryption(
    text: str = Query(default="테스트 메시지입니다.", description="테스트할 텍스트"),
    encryption: AESEncryption = Depends(get_encryption)
):
    """
    암호화 테스트

    주어진 텍스트를 암호화한 후 다시 복호화하여 정상 작동 여부를 확인합니다.
    """
    try:
        # 암호화
        encrypted, iv = encryption.encrypt(text)

        # 복호화
        decrypted = encryption.decrypt(encrypted, iv)

        return {
            "original": text,
            "encrypted_length": len(encrypted),
            "decrypted": decrypted,
            "match": text == decrypted,
            "encryption_version": encryption.get_version()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"암호화 테스트 실패: {str(e)}")