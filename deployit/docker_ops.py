import docker
from typing import Optional
from .utils import print_error, print_info, print_success

def ping_daemon() -> tuple[bool, Optional[str]]:
    """Check if Docker daemon is reachable and return its version."""
    try:
        client = docker.from_env()
        client.ping()
        version = client.version().get("Version", "unknown")
        return True, version
    except Exception as e:
        return False, str(e)

def login(username: str, token: str) -> bool:
    """Login to Docker Hub."""
    try:
        client = docker.from_env()
        client.login(username=username, password=token)
        print_info(f"Attempting Docker Hub login as '{username}'...")
        print_success("Docker Hub logged in")
        return True
    except Exception as e:
        print_error(f"Docker Hub login failed – {e}")
        return False

# def build_image(tag: str, path: str = ".") -> bool:
#     """Build a Docker image."""
#     try:
#         client = docker.from_env()
#         print_info(f"Building image {tag}...")
#         client.images.build(path=path, tag=tag)
#         print_success(f"Image {tag} built successfully")
#         return True
#     except Exception as e:
#         print_error(f"Failed to build image – {e}")
#         return False

# def push_image(tag: str) -> bool:
#     """Push a Docker image to Docker Hub."""
#     try:
#         client = docker.from_env()
#         print_info(f"Pushing image {tag}...")
#         client.images.push(tag)
#         print_success(f"Image {tag} pushed successfully")
#         return True
#     except Exception as e:
#         print_error(f"Failed to push image – {e}")
#         return False 