import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "db" / "ecommerce.db"


def load_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    df = pd.read_csv(path)
    print(f"Cargado {filename}: {len(df)} filas")
    return df


def main():
    conn = sqlite3.connect(DB_PATH)

    # Activa foreign keys en SQLite
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        load_order = [
            ("countries", "countries.csv"),
            ("categories", "categories.csv"),
            ("users", "users.csv"),
            ("products", "products.csv"),
            ("product_details", "product_details.csv"),
            ("orders", "orders.csv"),
            ("order_items", "order_items.csv"),
            ("shipping_regions", "shipping_regions.csv"),
        ]

        for table_name, csv_file in load_order:
            df = load_csv(csv_file)
            df.to_sql(table_name, conn, if_exists="append", index=False)
            print(f"Insertado en {table_name}\n")

        # Cargar currency_rates solo si tiene filas
        currency_file = DATA_DIR / "currency_rates_template.csv"
        if currency_file.exists():
            df_currency = pd.read_csv(currency_file)
            if not df_currency.empty:
                df_currency.to_sql("currency_rates", conn, if_exists="append", index=False)
                print("Insertado en currency_rates\n")
            else:
                print("currency_rates_template.csv está vacío, se omite.\n")

        conn.commit()
        print("Carga completada correctamente.")

    except Exception as e:
        conn.rollback()
        print(f"Error durante la carga: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()