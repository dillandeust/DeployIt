#!/usr/bin/env python3
import typer
from rich import print
import docker
import os, sys, tomli
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(help="DeployIt – petit outil de déploiement Docker one-click")

CONFIG_PATH_DEFAULT = os.path.expanduser(os.getenv("CONFIG_PATH"))
@app.callback()
def main(ctx: typer.Context,
         config: str = typer.Option(CONFIG_PATH_DEFAULT, "--config", "-c",
                                    help="Chemin du fichier de config TOML")):
    ctx.obj = {"config_path": config}
    
@app.command()
def check(ctx: typer.Context, full: bool = typer.Option(False, "--full", "-f", help="Vérifie aussi l'auth Docker Hub")):
    """Vérifie Docker + config Docker Hub."""
    # 1) Ping Docker
    try:
        client = docker.from_env()
        client.ping()
        version = client.version().get("Version", "unknown")
        print(f":rocket: [green]Docker daemon reachable (v{version})[/]")

        username, token = load_config(ctx.obj["config_path"])
        print(f":white_check_mark: [green]Docker Hub credentials loaded[/]")

        if full:
            auth(ctx)

    except Exception as e:
        print(f":x: [red]Docker unreachable – {e}[/]")
        sys.exit(1)

    
import tomllib, os, typer, sys

def load_config(path: str)->dict:
    """Verifie le fichier de config ou le crée si inexistant"""
    if not os.path.exists(path):
        print(f":x: [red]Config file not found at {path}[/]")
        if typer.confirm("Would you like to create it?"):
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            print(f":rocket: [green]Config directory created at {os.path.dirname(path)}[/]")

            username = typer.prompt("Enter your Docker Hub username")
            token = typer.prompt("Enter your Docker Hub token", hide_input=True)

            with open(path, "w") as f:
                f.write(f"[dockerhub]\nusername = \"{username}\"\ntoken = \"{token}\"")
                print(f":white_check_mark: [green]Config file created at {path}[/]")
        else:
            print(":x: [red]Config file is required to proceed[/]")
            sys.exit(1)
    
    with open(path, "rb") as f:
        config = tomllib.load(f)
    
    try:
        username = config["dockerhub"]["username"]
        token = config["dockerhub"]["token"]
    except KeyError:
        print(f":x: [red]Docker Hub username or token not found in config[/]")
        sys.exit(1)
    
    return username, token

@app.command()
def auth(ctx: typer.Context):
    """Authentifie avec Docker Hub."""
    username, token = load_config(ctx.obj["config_path"])
    try:
        client = docker.from_env()
        client.login(username=username, password=token)
        print(f":key: [green]Attempting Docker Hub login as '{username}'...[/]")
        print(f":white_check_mark: [green]Docker Hub logged in[/]")
    except Exception as e:
        print(f":x: [red]Docker Hub login failed – {e}[/]")
        sys.exit(1)

if __name__ == "__main__":
    app()
