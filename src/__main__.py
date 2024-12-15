from uvicorn import run as server_run

from cars_backend.create_app import create_app

if __name__ == "__main__":
    app = create_app()

    server_run(app, host="0.0.0.0")
