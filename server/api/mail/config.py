from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

file_path = Path(__file__).resolve().parent
class Config(BaseSettings):
    """Project configuration class for environmental attributes inheriting pydantic's BaseSettings.

    Args:
        BaseSettings (_class_): Base class for settings, allowing values to be overridden by environment variables.
    """

    smtp_login : str
    api_key : str

    bulk_mail_smtp_url : str
    individual_mail_smtp_url : str
    default_smtp_port : int

    model_config = SettingsConfigDict(env_file=f'{Path(file_path).joinpath('.env')}')
