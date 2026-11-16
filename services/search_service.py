import requests
from config import SERPER_API_KEY

def search_web(query: str, num_results: int = 8) -> list[dict]:
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query.strip(), "num": num_results}
    try:
        response = requests.post(url, headers = headers, json = payload, timeout = 20)
        response.raise_for_status()
        data = response.json()
        return data.get("organic", [])
    except requests.exceptions.Timeout:
        raise RuntimeError("Serper request timed out")
    except requests.exceptions.HTTPError as error:
        raise RuntimeError(f"Serper API returned an HTTP error: {error}")
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Search request failed: {error}")
    except ValueError:
        raise RuntimeError("Invalid JSON response from Serper")
