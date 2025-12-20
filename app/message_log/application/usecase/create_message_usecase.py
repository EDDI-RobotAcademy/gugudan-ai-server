from app.message_log.domain.entity import ChatMessage, MessageRole, ContentType
from app.message_log.infrastructure.repository.chat_message_repository_impl import ChatMessageRepositoryImpl
from app.config.security.message_crypto import AESEncryption


class CreateMessageUseCase:
    """메시지 생성 UseCase"""

    def __init__(self):
        self.message_repo = ChatMessageRepositoryImpl()
        self.encryption = AESEncryption()

    def execute(
            self,
            room_id: str,
            account_id: int,
            content: str,
            role: MessageRole,
            content_type: ContentType,
            img_url: str | None = None
    ) -> ChatMessage:
        """
        메시지 생성 및 저장

        Args:
            room_id: 채팅방 ID
            account_id: 사용자 ID
            content: 원본 메시지 내용
            role: 메시지 역할
            content_type: 컨텐츠 타입
            img_url: 이미지 URL (선택)

        Returns:
            생성된 ChatMessage
        """
        # 유효성 검증
        if not room_id:
            raise ValueError("room_id는 필수입니다")

        if not content or len(content.strip()) == 0:
            raise ValueError("content는 비어있을 수 없습니다")

        if len(content) > 10000:
            raise ValueError("content는 10000자를 초과할 수 없습니다")

        # 메시지 암호화
        encrypted_content, iv = self.encryption.encrypt(content)

        # Domain Entity 생성
        message = ChatMessage(
            id=0,  # DB에서 자동 생성
            chat_room_id=room_id,
            account_id=account_id,
            role=role,
            content_enc=encrypted_content,
            iv=iv,
            enc_version=self.encryption.get_version(),
            contents_type=content_type,
            img_url=img_url
        )

        # 저장
        saved_message = self.message_repo.save(message)

        return saved_message
    
    def decrypt_message(self, message: ChatMessage) -> str:
        """
        메시지 복호화 (필요 시에만 사용)
        
        Args:
            message: 암호화된 메시지
            
        Returns:
            str: 복호화된 원본 내용
        """
        return self.encryption.decrypt(message.content_enc)
    
    @staticmethod
    def _validate_input(chat_room_id: str, content: str) -> None:
        """입력값 검증"""
        if not chat_room_id:
            raise ValueError("chat_room_id는 필수입니다.")
        
        if not content or not content.strip():
            raise ValueError("content는 비어있을 수 없습니다.")
        
        if len(content) > 10000:
            raise ValueError("content는 10000자를 초과할 수 없습니다.")
