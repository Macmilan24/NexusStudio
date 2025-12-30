import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- API KEYS ---
    # Pydantic will automatically look for GOOGLE_API_KEY (case-insensitive)
    google_api_key: str | None = None
    groq_api_key: str | None = None
    openrouter_api_key: str | None = None

    # We map 'hf_token' to read specifically from 'HUGGINGFACEHUB_API_TOKEN'
    hf_token: str | None = Field(
        default=None, validation_alias="HUGGINGFACEHUB_API_TOKEN"
    )

    # --- SELECTION LOGIC ---
    # We map these fields to the specific ENV variable names you created
    brain_provider: str = Field(
        default="google", validation_alias="PRIMARY_BRAIN_PROVIDER"
    )
    brain_model: str = Field(
        default="gemini-1.5-flash", validation_alias="PRIMARY_BRAIN_MODEL"
    )

    reflex_provider: str = Field(
        default="groq", validation_alias="FAST_REFLEX_PROVIDER"
    )
    reflex_model: str = Field(
        default="llama3-70b-8192", validation_alias="FAST_REFLEX_MODEL"
    )

    # Capture the project root if needed
    project_root: str | None = Field(default=None, validation_alias="PROJECT_ROOT")

    # --- CONFIG ---
    # extra="ignore" prevents the crash if you have comments or unused vars in .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
