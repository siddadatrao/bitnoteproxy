import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Setup retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

url = "https://bitnote-a97b19c0e48d.herokuapp.com/response_router"
params = {
    "role": "You are a helpful assistant",
    "prompt": "What is 2+2?"
}

try:
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()  # Raise an error for bad status codes
    print("JSON Response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {str(e)}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        print(f"Response text: {e.response.text}") 



    