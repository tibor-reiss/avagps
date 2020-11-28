from dotenv import load_dotenv

from src.app import create_app


load_dotenv('.env')
app = create_app()
