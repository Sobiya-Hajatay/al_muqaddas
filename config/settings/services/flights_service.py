import requests
from django.conf import settings


def search_flights(from_city, to_city, depart_date):
    """
    LIVE FLIGHT SEARCH (API READY)
    Replace endpoint as per provider
    """

    if not (from_city and to_city and depart_date):
        return []

    try:
        # 🔥 SAMPLE STRUCTURE (replace with your provider)
        url = "https://api.example.com/flights/search"

        headers = {
            "X-API-KEY": settings.FLIGHT_API_KEY,
            "X-API-SECRET": settings.FLIGHT_API_SECRET,
        }

        payload = {
            "from": from_city,
            "to": to_city,
            "date": depart_date,
        }

        # ====== TEMP MOCK (until real API) ======
        # comment below when real API ready
        return [
            {
                "airline": "Saudi Airlines",
                "departure": "10:30",
                "arrival": "14:45",
                "price": 28500,
            },
            {
                "airline": "Air India",
                "departure": "06:15",
                "arrival": "10:25",
                "price": 26200,
            },
        ]

    except Exception as e:
        print("Flight API Error:", e)
        return []