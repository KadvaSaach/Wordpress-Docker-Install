

import subprocess
import sys
import os
import time
from typing import Optional
import typer
from rich.console import Console
import requests

console = Console()
app = typer.Typer()

# DOCKER_COMPOSE_INSTALL_COMMAND = "pip install docker-compose"

@app.command(short_help="Create a WordPress site")
def create_site(site_name: str):
    typer.secho(f"Creating WordPress site: {site_name}", fg=typer.colors.GREEN)

    # Check if Docker is installed
    if not is_docker_installed():
        install_docker()

    # Check if docker-compose is installed
    if not is_docker_compose_installed():
        install_docker_compose()

    # Create docker-compose.yml file
    create_docker_compose_file(site_name)

    # Start containers
    start_containers()

    # Add /etc/hosts entry
    add_hosts_entry(site_name)

    prompt_open_browser(site_name)



# Delete the site by removing the containers and local files.
@app.command(short_help="Delete the site.")
def delete_site(site_name: str):
    typer.secho(f"Deleting site: {site_name}", fg=typer.colors.GREEN)

    # Check if docker-compose is installed
    if not is_docker_compose_installed():
        typer.secho("docker-compose is not installed.", fg=typer.colors.RED)
        return

    # Stop and remove containers
    stop_containers()
    remove_containers()

    # Remove local files
    remove_local_files()

# to eneble site use --enble flag, to disable use --no-enable flag 
@app.command(short_help="Enable or disable the site")
def manage_site(site_name: str, enable: bool = True):
    typer.secho(f"Managing site: {site_name}", fg=typer.colors.GREEN)

    # Check if docker-compose is installed
    if not is_docker_compose_installed():
        typer.secho("docker-compose is not installed.", fg=typer.colors.RED)
        return

    # Stop or start the containers
    if enable:
        start_containers()
    else:
        stop_containers()


@app.command(short_help="Install Docker.")
def install_docker():
    typer.secho("Docker is not installed. Installing Docker...", fg=typer.colors.GREEN)
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "docker", "-y"], check=True)
        typer.secho("Docker installed successfully!", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("Failed to install Docker.", fg=typer.colors.RED)
        sys.exit(1)

@app.command(short_help="Install docker-compose.")
def install_docker_compose():
    typer.secho("docker-compose is not installed. Installing docker-compose...", fg=typer.colors.GREEN)
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "docker-compose"], check=True)
        typer.secho("docker-compose installed successfully!", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("Failed to install docker-compose.", fg=typer.colors.RED)
        sys.exit(1)

@app.command(short_help="Check if Docker is installed.")
def is_docker_installed() -> bool:
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        typer.secho("docker is installed.", fg=typer.colors.GREEN)
        return True
    except subprocess.CalledProcessError:
        # typer.secho("docker is not installed." + subprocess.CalledProcessError, fg=typer.colors.RED)
        typer.secho("docker is not installed.", fg=typer.colors.RED)
        return False


@app.command(short_help="Check if docker-compose is installed.")
def is_docker_compose_installed() -> bool:
    try:
        subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        typer.secho("docker-compose is installed.", fg=typer.colors.GREEN)
        return True
    except subprocess.CalledProcessError:
        # typer.secho("docker-compose is not installed." + subprocess.CalledProcessError, fg=typer.colors.RED)
        typer.secho("docker-compose is not installed.", fg=typer.colors.RED)
        return False




@app.command(short_help="Create the docker-compose.yml file")
def create_docker_compose_file(site_name: str):
    compose_content = f"""
    version: '3'
    services:
      db:
        image: mysql:latest
        environment:
          MYSQL_DATABASE: wordpress
          MYSQL_USER: wordpress
          MYSQL_PASSWORD: wordpress
          MYSQL_RANDOM_ROOT_PASSWORD: '1'
        volumes:
          - db_data:/var/lib/mysql
        networks:
          - wordpress_network
      wordpress:
        depends_on:
          - db
        image: wordpress:latest
        ports:
          - '80:80'
        environment:
          WORDPRESS_DB_HOST: db:3306
          WORDPRESS_DB_USER: wordpress
          WORDPRESS_DB_PASSWORD: wordpress
          WORDPRESS_DB_NAME: wordpress
        volumes:
          - ./wordpress:/var/www/html
        networks:
          - wordpress_network
    volumes:
      db_data: {{}}
    networks:
      wordpress_network: {{}}
    """

    with open("docker-compose.yml", "w") as compose_file:
        compose_file.write(compose_content)

@app.command(short_help="Start the container")
def start_containers():
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        typer.secho("Containers are running......", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("Failed to start containers.", fg=typer.colors.RED)
        sys.exit(1)

@app.command(short_help="Stop the containers")
def stop_containers():
    try:
        subprocess.run(["docker-compose", "stop"], check=True)
        typer.secho("Containers stopped successfully......", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        # typer.secho("Failed to stop containers. "+ subprocess.CalledProcessError, fg=typer.colors.RED)
        typer.secho("Failed to stop containers. ", fg=typer.colors.RED)
        sys.exit(1)

@app.command(short_help="Add an entry to /etc/hosts")
def add_hosts_entry(site_name: str):
    try:
        with open("/etc/hosts", "a") as hosts_file:
            hosts_file.write(f"127.0.0.1 {site_name}\n")
    except PermissionError:
        typer.secho("Permission denied. Please run with sudo or as an administrator.", fg=typer.colors.RED)
        sys.exit(1)


def show_loading_animation():
    animation = "|/-\\"
    for _ in range(15):
        for char in animation:
            typer.secho(char, nl=False, fg=typer.colors.GREEN)
            time.sleep(0.1)
            typer.echo("\b", nl=False)


@app.command(short_help="To check site health")
def prompt_open_browser(site_name: str):

    def is_site_up_and_healthy(site_name: str) -> bool:
        try:
            site = "http://" + site_name
            response = requests.get(site)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
    
    typer.echo(f"Cheking the site status......")
    show_loading_animation()
    # time.sleep(10)     
    if is_site_up_and_healthy(site_name):
        typer.echo(f"Site '{site_name}' is up and healthy! Open http://{site_name} in a browser to view it.")
        # typer.input("Press Enter to continue...")
    else:
        typer.echo(f"Site '{site_name}' is not up or healthy.")
    

@app.command(short_help="Remove the container")
def remove_containers():
    try:
        # typer.secho("debugg - 1.", fg=typer.colors.RED)
        subprocess.run(["docker-compose", "rm", "-v"], input="y\n", text=True, check=True)
        # typer.secho("debugg - 2.", fg=typer.colors.RED)
    except subprocess.CalledProcessError:
        typer.secho("Failed to remove containers.", fg=typer.colors.RED)
        sys.exit(1)

@app.command(short_help="Remove local files.")
def remove_local_files():
    try:
        subprocess.run(["sudo", "rm", "-rf", f"./wordpress"], check=True)
    except subprocess.CalledProcessError:
        typer.secho("Failed to remove local files.", fg=typer.colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    app()
