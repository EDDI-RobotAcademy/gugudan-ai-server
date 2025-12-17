from app.domain.auth.ports import OAuthUserInfo
from app.infrastructure.oauth.base import BaseOAuthProvider
from config.settings import settings


class NaverOAuthProvider(BaseOAuthProvider):

    AUTHORIZE_URL = "https://nid.naver.com/oauth2.0/authorize"
    TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
    USERINFO_URL = "https://openapi.naver.com/v1/nid/me"
    SCOPES = []

    def __init__(self):
        super().__init__(
            client_id=settings.NAVER_CLIENT_ID,
            client_secret=settings.NAVER_CLIENT_SECRET,
            redirect_uri=settings.NAVER_REDIRECT_URI,
        )

    @property
    def provider_name(self) -> str:
        return "naver"

    async def get_user_info(self, access_token: str) -> OAuthUserInfo:
        data = await self._fetch_user_info(access_token)
        user_data = data.get("response", {})

        return OAuthUserInfo(
            email=user_data.get("email", ""),
            name=user_data.get("name", user_data.get("email", "").split("@")[0]),
            picture=user_data.get("profile_image"),
            provider=self.provider_name,
        )