# API Template

This template is a "batteries included" starting point for building APIs with `aiohttp.web`.

## Features

- **Flexible Async Web-Server**: Utilizes `aiohttp.web` for creating a flexible and efficient asynchronous web server.
- **File-Based Routing**: Any file in the routes folder is automatically added to the router, simplifying the routing process.
- **Logging Preset**: Comes with a pre-configured logging setup.

## Directory Structure

`.`
`├──``routes/`: Any file in this folder is automatically added to the router
`├──``utils/`: Contains "global" utility files
`├──``app.py`: The main entry point to the application
`└──``config.toml`: A configuration file for the web application

## Getting Started

1. Clone the repository:
   ```
   $ git clone https://github.com/du-cki/api_template.git
   ```
2. Navigate to the project directory:
   ```
   $ cd api_template
   ```
3. Install the project dependencies & run the project:
   ```
   $ poetry install
   $ poetry run python app.py
   ```

## Deployment

For deployment, please refer to the official aiohttp [deployment documentation](https://docs.aiohttp.org/en/stable/deployment.html).

## Contributing

Contributions are welcome. Please feel free to open an issue or submit a pull request.

---

**Note**: This project is still under development. If you encounter any problems, please report them in the issue tracker. Your feedback is greatly appreciated.
