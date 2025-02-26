# Weather Query API
A small project for querying weather information by city name using [OpenWeatherMap](https://openweathermap.org/).
You can check this API at: [Weather Query API Docs](https://pashok11.tw1.su/apis/weather_query/docs)
## How to Use
### Tested Environments
- OS: Linux (Arch) and Docker Compose
- Python: 3.8, 3.9, 3.13.0, 3.13.1
- PostgreSQL: 9.2.19, 10.0, 17.4
### Troubleshooting Docker
If Docker is not working, try the following:
- For desktop: `systemctl start docker.socket`
- For server: `systemctl start docker.service`
### Setup
1. Copy the `.env.api.example` file to the main directory and rename it to `.env.api` (remove `.example` from the filename).
2. Update the `OPEN_WEATHER_API_KEY` in the `.env.api` file with your OpenWeatherMap API key. You can obtain a key [here](https://home.openweathermap.org/users/sign_up). The API will not function without a valid API key.
### Running the API
You have several options to run the API:
#### Using Docker Compose (Recommended)
1. Copy `.env.example` to `.env` and modify it if necessary (default values are already provided).
2. Start Docker Compose:
    ```sh
    docker compose up  
    ```
    - Add `-d` to run it in the background.
3. Stop Docker Compose:
    ```sh
    docker compose down  
    ```
    - Add `--rmi local` to remove locally created images (not ones pulled from Docker Hub).
    - Add `-v` to delete all related volumes (be cautious - this will erase the database and logs).
#### Using Docker (Experimental)
You can try running the API directly with Docker, but this method is not tested. Use it at your own risk.
#### Using Bash Scripts
1. _(Optional)_ Copy `.env.example` to `.env` and modify it if needed.
2. Run:
    ```sh
    ./start.sh  
    ```
    If you encounter issues running the script, try making it executable:
    ```sh
    chmod +x start.sh  
    ```
3. _(Development mode for automated restarts when code changes)_ Copy `.env.dev.example`, rename it to `.env.dev`, and modify it if needed. Then start with:
    ```sh
    ./start_dev.sh  
    ```
    **Note:** In development mode, logs are not saved to a file.
#### Running Manually
You can run the FastAPI app using common methods such as:
```sh
fastapi run main.py --host 0.0.0.0 --port 8000
```
or
```sh
uvicorn main:app --host 0.0.0.0 --port 8000  
```
However, this approach has not been thoroughly tested, so use it at your own risk.