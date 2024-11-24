from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    DATABASE_URL:str
    JWT_SECRET:str = "wdPy607463F0UxstA3_VYYVUBNtt3qHpKjLIJL1nOos"
    JWT_ALGORITHM:str = "HS256"
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    
Config=Settings()

print("DATABASE_URL:", Config.DATABASE_URL)
print("JWT_SECRET:", Config.JWT_SECRET)
print("JWT_ALGORITHM:", Config.JWT_ALGORITHM)
