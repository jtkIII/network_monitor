from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    api_key: str = Field(..., validation_alias="API_KEY")

    # Optional / defaults - not sure if I want to keep this or...
    debug: bool = Field(False, validation_alias="DEBUG")
    host: str = Field("127.0.0.1", validation_alias="HOST")
    port: int = Field(8000, validation_alias="PORT")
    cache_ttl_seconds: int = Field(5, validation_alias="CACHE_TTL_SECONDS")

    allowed_ips_raw: Optional[str] = Field(None, validation_alias="ALLOWED_IPS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Computed property: List[str] from comma-separated string
    @property
    def allowed_ips(self) -> List[str]:
        if not self.allowed_ips_raw:
            return []
        return [ip.strip() for ip in self.allowed_ips_raw.split(",") if ip.strip()]


# singleton instance
settings = Settings() # type: ignore
