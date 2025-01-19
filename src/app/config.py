from msx_models.config import Config as MsxModelConfig


class AppConfig(MsxModelConfig):
    # Session settings
    # session_secret_key: str = "super-secret-key"
    session_max_age: int = 60 * 60 * 24 * 365 * 5  # 5 years
    session_file_storage_path: str = '/tmp/jmsx_session'
