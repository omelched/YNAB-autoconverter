from src.app import Application
from utils import config

if config.PRODUCT:
    application = Application()
