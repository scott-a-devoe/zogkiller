from django.apps import AppConfig
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CustomCommandsConfig(AppConfig):
    name = 'customCommands'
    path = os.path.join(BASE_DIR, 'customCommands')
