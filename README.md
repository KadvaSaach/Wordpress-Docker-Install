# WordPress Site Management CLI

This command-line tool allows you to manage WordPress sites using Docker and docker-compose.

## Installation

1. Clone the repository.

   ```shell
   git clone https://github.com/KadvaSaach/Wordpress-Docker-Install.git

   ```

2. Change into the project directory:

   ```shell
   cd Wordpress-Docker-Install
   ```

3. Run the CLI as the superuser (root) using the following command:

   ```shell
   sudo su
   ```

   This will prompt you to enter your password. After successful authentication, you will have root privileges.

4. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

5. Run the CLI:

   ```shell
   python main.py [command]
   ```

## Usage

### Install Docker

Install Docker on your system:

```shell
python main.py install_docker
```

### Install docker-compose

Install docker-compose on your system:

```shell
python main.py install_docker_compose
```

### Create a WordPress site

Create a new WordPress site with the specified name:

```shell
python main.py create_site [site_name]
```

### Delete a site

Delete the specified WordPress site::

```shell
python main.py delete_site [site_name]
```

### Enable or disable a site

Manage the state of the specified WordPress site. Use the `--enable` flag to enable the site or the `--no-enable` flag to disable the site:

```shell
python main.py manage_site [site_name] --enable
```

```shell
python main.py manage_site [site_name] --no-enable
```

### Check site health

Check the status and health of a WordPress site:

```shell
python main.py prompt_open_browser [site_name]
```

### To list all commands

```shell
python main.py --help
```
