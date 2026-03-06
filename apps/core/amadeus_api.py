import requests
from django.conf import settings
from django.core.cache import cache

AMADEUS_BASE = "https://test.api.amadeus.com"


# ================= TOKEN =================
def get_token():
    cached_token = cache.get("amadeus_token")
    if cached_token:
        return cached_token

    url = f"{AMADEUS_BASE}/v1/security/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": settings.AMADEUS_API_KEY,
        "client_secret": settings.AMADEUS_API_SECRET,
    }

    r = requests.post(url, data=data, timeout=20)
    r.raise_for_status()

    token = r.json()["access_token"]

    # ✅ cache token for 25 minutes
    cache.set("amadeus_token", token, 60 * 25)

    return token


# ================= FLIGHTS =================
def search_flights(origin, destination, depart_date):
    cache_key = f"flights_{origin}_{destination}_{depart_date}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    token = get_token()

    url = f"{AMADEUS_BASE}/v2/shopping/flight-offers"

    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": depart_date,
        "adults": 1,
        "max": 10,
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        data = r.json().get("data", [])
    except Exception as e:
        print("Flight API Error:", e)
        return []

    results = []

    for item in data:
        try:
            segment = item["itineraries"][0]["segments"][0]

            results.append({
                "airline": segment["carrierCode"],
                "from": segment["departure"]["iataCode"],
                "to": segment["arrival"]["iataCode"],
                "departure": segment["departure"]["at"],
                "arrival": segment["arrival"]["at"],
                "price": item["price"]["total"],
            })
        except Exception:
            continue

    # ✅ cache results for 10 minutes
    cache.set(cache_key, results, 60 * 10)

    return results


# ================= HOTELS =================
def search_hotels(city_code, checkin=None, checkout=None):
    cache_key = f"hotels_{city_code}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    token = get_token()

    url = f"{AMADEUS_BASE}/v1/reference-data/locations/hotels/by-city"

    headers = {"Authorization": f"Bearer {token}"}
    params = {"cityCode": city_code}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        data = r.json().get("data", [])[:10]
    except Exception as e:
        print("Hotel API Error:", e)
        return []

    hotels = []

    for h in data:
        hotels.append({
            "name": h.get("name"),
            "hotel_id": h.get("hotelId"),
            "city": city_code,
            "rating": "4.2",
            "price": "—",
            "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
        })

    # ✅ cache hotels
    cache.set(cache_key, hotels, 60 * 10)

    return hotels
import requests
from django.conf import settings


# ================= TOKEN =================
def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": settings.AMADEUS_API_KEY,
        "client_secret": settings.AMADEUS_API_SECRET,
    }

    r = requests.post(url, data=data, timeout=20)
    return r.json().get("access_token")


# ================= FLIGHTS =================
def search_flights(origin, destination, depart_date):
    try:
        token = get_amadeus_token()

        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": depart_date,
            "adults": 1,
            "max": 10,
        }

        r = requests.get(url, headers=headers, params=params, timeout=20)
        data = r.json()

        flights = []

        for item in data.get("data", []):
            flights.append({
                "airline": item["validatingAirlineCodes"][0],
                "price": item["price"]["total"],
                "currency": item["price"]["currency"],
            })

        return flights
    

    except Exception as e:
        print("Flight API error:", e)
        return []
    # ================= HOTELS =================
def search_hotels(city_code):
    try:
        token = get_amadeus_token()

        url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "cityCode": city_code
        }

        r = requests.get(url, headers=headers, params=params, timeout=20)
        data = r.json()

        hotels = []

        for h in data.get("data", [])[:10]:
            hotels.append({
                "name": h.get("name"),
                "city": city_code,
            })

        return hotels

    except Exception as e:
        print("Hotel API error:", e)
        return []
    
    
    