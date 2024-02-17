'''Settings module'''

import os
from dotenv import load_dotenv

load_dotenv()

FM_URL = os.getenv('FM_URL')
