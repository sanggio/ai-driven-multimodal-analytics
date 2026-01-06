from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    openai_api_key: str = Field(..., description="OpenAI API Key")
    api_secret_key: str = Field(..., description="API Secret Key for authentication")
    jwt_secret_key: str = Field(..., description="JWT Secret Key for token signing")
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection URL")
    redis_enabled: bool = Field(default=True, description="Enable Redis caching")
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")
    log_level: str = Field(default="INFO", description="Logging level")
    app_host: str = Field(default="0.0.0.0", description="Application host")
    app_port: int = Field(default=8000, description="Application port")
    openai_model: str = Field(default="gpt-4o", description="Default OpenAI model")
    openai_vision_model: str = Field(default="gpt-4o", description="OpenAI Vision model")
    openai_audio_model: str = Field(default="whisper-1", description="OpenAI Audio model")
    openai_tts_model: str = Field(default="tts-1", description="OpenAI TTS model")
    openai_tts_voice: str = Field(default="alloy", description="OpenAI TTS voice")
    max_tokens: int = Field(default=1000, description="Max tokens for completion")
    temperature: float = Field(default=0.7, description="Model temperature")


settings = Settings()

