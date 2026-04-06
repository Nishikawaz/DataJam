import sqlite3
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "ecommerce.db"

API_URL = "https://api.first.org/data/v1/countries"


def fetch_all_countries():
    all_countries = {}
    limit = 249
    offset = 0

    while True:
        response = requests.get(API_URL, params={"limit": limit, "offset": offset}, timeout=30)
        response.raise_for_status()
        payload = response.json()

        data = payload.get("data", {})
        total = payload.get("total", 0)
        current_offset = payload.get("offset", 0)
        current_limit = payload.get("limit", limit)

        all_countries.update(data)

        offset = current_offset + current_limit
        if offset >= total:
            break

    return all_countries


def assign_shipping(region: str):
    """
    Reglas lógicas propias para zona logística y días estimados.
    Puedes ajustarlas si su profe les pide otra lógica, pero esta ya es defendible.
    """
    if region in ("South America", "Central America", "North America", "Americas"):
        return "AMER", "3-7 days"
    elif region == "Europe":
        return "EMEA", "5-10 days"
    elif region == "Africa":
        return "EMEA", "7-14 days"
    elif region in ("Asia", "Oceania"):
        return "APAC", "7-15 days"
    elif region == "Antarctic":
        return "OTHER", "15-30 days"
    else:
        return "OTHER", "10-20 days"


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    try:
        print("Consultando API FIRST...")
        api_countries = fetch_all_countries()
        print(f"Países obtenidos desde API: {len(api_countries)}")

        cursor.execute("SELECT country_code FROM shipping_regions")
        shipping_codes = [row[0] for row in cursor.fetchall()]
        print(f"Códigos a enriquecer en shipping_regions: {len(shipping_codes)}")

        updated = 0
        missing = []

        for code in shipping_codes:
            info = api_countries.get(code)

            if not info:
                missing.append(code)
                continue

            region = info.get("region")

            if not region:
                missing.append(code)
                continue

            shipping_zone, estimated_days = assign_shipping(region)

            cursor.execute(
                """
                UPDATE shipping_regions
                SET region = ?, shipping_zone = ?, estimated_days = ?
                WHERE country_code = ?
                """,
                (region, shipping_zone, estimated_days, code)
            )
            updated += 1

        conn.commit()

        print(f"Filas actualizadas: {updated}")
        if missing:
            print("Códigos sin match en API:", ", ".join(missing))
        else:
            print("Todos los country_code fueron enriquecidos correctamente.")

    except Exception as e:
        conn.rollback()
        print(f"Error durante el enriquecimiento: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()