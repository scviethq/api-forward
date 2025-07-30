import yaml
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseModel


class RouteConfig(BaseModel):
    target_url: str
    timeout: int = 30


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"


class LoggingConfig(BaseModel):
    rotation: str = "1 day"
    retention: str = "30 days"
    compression: str = "zip"
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"


class Config(BaseModel):
    routes: Dict[str, RouteConfig]
    server: ServerConfig
    logging: LoggingConfig


def load_config(config_path: str = "config.yaml") -> Config:
    """Load configuration from YAML file"""
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    return Config(**config_data)


# Global config instance
config = load_config() 