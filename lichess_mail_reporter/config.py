from typing import List, Type, Tuple
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

class Settings(BaseSettings):
    username: str = Field(...)
    sender_name: str = Field(...)
    sender_mail: str = Field(...)
    recipients: List[str] = Field(...)
    template_uid: str = Field(...)
    mail_token: str = Field(...)
    model_config = SettingsConfigDict(toml_file='settings.toml')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)
