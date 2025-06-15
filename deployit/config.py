import os
import tomllib
import typer
from typing import Tuple
from .utils import print_error, print_info, print_success

def ensure_config_dir(path: str) -> None:
    """Ensure the config directory exists."""
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
        print_info(f"Config directory created at {os.path.dirname(path)}")

def create_config(path: str) -> Tuple[str, str]:
    """Create a new config file with user input."""
    ensure_config_dir(path)
    
    username = typer.prompt("Enter your Docker Hub username")
    token = typer.prompt("Enter your Docker Hub token", hide_input=True)

    with open(path, "w") as f:
        f.write(f"[dockerhub]\nusername = \"{username}\"\ntoken = \"{token}\"")
    
    print_success(f"Config file created at {path}")
    return username, token

def load_config(path: str) -> Tuple[str, str]:
    """Load or create Docker Hub configuration."""
    if not os.path.exists(path):
        print_error(f"Config file not found at {path}")
        if typer.confirm("Would you like to create it?"):
            return create_config(path)
        else:
            print_error("Config file is required to proceed")
            raise typer.Exit(1)
    
    with open(path, "rb") as f:
        config = tomllib.load(f)
    
    try:
        username = config["dockerhub"]["username"]
        token = config["dockerhub"]["token"]
    except KeyError:
        print_error("Docker Hub username or token not found in config")
        raise typer.Exit(1)
    
    return username, token 