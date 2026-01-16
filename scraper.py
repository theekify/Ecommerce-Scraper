import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from utils import get_random_user_agent, save_to_csv

class EcommerceScraper:
    def __init__(self):
        seld