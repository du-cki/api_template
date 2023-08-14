# API Template

This template is a "batteries included" starting point for building APIs with `aiohttp.web`.

## Features

- **Flexible Async Web-Server**: Utilizes `aiohttp.web` for creating a flexible and efficient asynchronous web server.
- **File-Based Routing**: Any file in the routes folder is automatically added to the router, simplifying the routing process.
- **Logging Preset**: Comes with a pre-configured logging setup.

## Directory Structure

`.`<br>
`├──`[`routes/`](routes): Any file in this folder is automatically added to the router.<br>
`├──`[`utils/`](utils): Contains "global" utility files.<br>
`├──`[`app.py`](./app.py): The main entry point to the application.<br>
`└──`[`config.toml`](./config.toml): A configuration file for the web application.<br>

## Getting Started

1. Clone the repository:
   ```
   $ git clone https://github.com/du-cki/api_template.git
   ```
2. [ ] Navigate to the project directory:
   ```
   $ cd api_template
   ```
3. Install the project dependencies & run the project:
   ```
   $ poetry install
   $ poetry run adev runserver . 
   ```

## Deployment

For installing the dependencies, you could run `poetry install --without dev` to install required deps. For deployment, please refer to the official aiohttp [deployment documentation](https://docs.aiohttp.org/en/stable/deployment.html).

## Contributing

Contributions are welcome. Please feel free to open an issue or submit a pull request.
