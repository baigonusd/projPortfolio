from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(dotenv_path=find_dotenv())


class Settings:
    TITLE = "My portfolio application"
    DESCRIPTION = """
    ## Shop application created in FASTAPI
    Special for portfolio
    """
    CONTACT = {
        "name": "Baigonus Dinmukhamed",
        "email": "d.baigonus@gmail.com"
    }
    TAGS = [
        {
            "name": "Users",
            "description": "Users routes"
        },
        {
            "name": "Items",
            "description": "Items routes"
        }
    ]

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    SECRET_KEY : str = os.getenv("SECRET_KEY")
    ALGORITHM : str = os.getenv("ALGORITHM")
    TEST_USER : str = os.getenv("TEST_USER")
    TEST_PASSWORD : str = os.getenv("TEST_PASSWORD")
settings = Settings()
