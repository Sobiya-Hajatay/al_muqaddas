import requests
from django.conf import settings


def search_hotels(city, checkin, checkout):
    """
    LIVE HOTEL SEARCH
    Replace endpoint with provider
    """

    if not city:
        return []

    try:
        # 🔥 SAMPLE STRUCTURE
        url = "https://api.example.com/hotels/search"

        headers = {
            "X-API-KEY": settings.HOTEL_API_KEY,
            "X-API-SECRET": settings.HOTEL_API_SECRET,
        }

        payload = {
            "city": city,
            "checkin": checkin,
            "checkout": checkout,
        }

        # ===== TEMP MOCK DATA =====
        return [
            {
                "name": "Ibis Styles Makkah",
                "address": "Makkah, Saudi Arabia",
                "rating": 4.1,
                "price": 4200,
                "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1200",
            },
            {
                "name": "Rose Al Faidy Madinah",
                "address": "Madinah, Saudi Arabia",
                "rating": 4.3,
                "price": 3800,
                "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?q=80&w=1200",
            },
        ]

    except Exception as e:
        print("Hotel API Error:", e)
        return []