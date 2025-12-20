from abc import ABC, abstractmethod
from typing import Tuple


class EncryptionPort(ABC):
    """암호화 서비스 인터페이스"""
    
    @abstractmethod
    def encrypt(self, plaintext: str) -> bytes:
        """
        평문을 암호화
        
        Args:
            plaintext: 암호화할 문자열
            
        Returns:
            bytes: 암호화된 바이트 데이터
        """
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> str:
        """
        암호문을 복호화
        
        Args:
            ciphertext: 암호화된 바이트 데이터
            
        Returns:
            str: 복호화된 평문
        """
        pass
    
    @abstractmethod
    def get_iv(self) -> bytes:
        """
        현재 IV(Initialization Vector) 가져오기
        
        Returns:
            bytes: IV
        """
        pass
    
    @abstractmethod
    def get_version(self) -> int:
        """
        암호화 버전 가져오기
        
        Returns:
            int: 암호화 버전
        """
        pass
