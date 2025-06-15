#!/usr/bin/env python3
import os
import typer
from dotenv import load_dotenv
from . import __version__
from .config import load_config
from .docker_ops import ping_daemon, login
from .utils import print_error, print_info, print_success

load_dotenv()

app = typer.Typer(help="DeployIt – petit outil de déploiement Docker one-click")

CONFIG_PATH_DEFAULT = os.path.expanduser(os.getenv("CONFIG_PATH", "~/.deployit/config.toml"))

@app.callback()
def main(ctx: typer.Context,
         config: str = typer.Option(CONFIG_PATH_DEFAULT, "--config", "-c",
                                    help="Chemin du fichier de config TOML")):
    ctx.obj = {"config_path": config}

@app.command()
def check(ctx: typer.Context, full: bool = typer.Option(False, "--full", "-f", 
                                                       help="Vérifie aussi l'auth Docker Hub")):
    """Vérifie Docker + config Docker Hub."""
    is_reachable, version = ping_daemon()
    if not is_reachable:
        print_error(f"Docker unreachable – {version}")
        raise typer.Exit(1)
    
    print_success(f"Docker daemon reachable (v{version})")
    
    username, token = load_config(ctx.obj["config_path"])
    print_success("Docker Hub credentials loaded")

    if full and not login(username, token):
        raise typer.Exit(1)

@app.command()
def auth(ctx: typer.Context):
    """Authentifie avec Docker Hub."""
    username, token = load_config(ctx.obj["config_path"])
    if not login(username, token):
        raise typer.Exit(1)

# @app.command()
# def build(ctx: typer.Context, 
#           tag: str = typer.Argument(..., help="Tag de l'image (ex: user/image:tag)"),
#           path: str = typer.Option(".", "--path", "-p", help="Chemin du Dockerfile")):
#     """Construit une image Docker."""
#     if not build_image(tag, path):
#         raise typer.Exit(1)

# @app.command()
# def push(ctx: typer.Context,
#          tag: str = typer.Argument(..., help="Tag de l'image à pousser")):
#     """Pousse une image Docker vers Docker Hub."""
#     if not push_image(tag):
#         raise typer.Exit(1)

def run():
    """Point d'entrée principal pour l'application."""
    app()
