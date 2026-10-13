import os
import psycopg
import random

L_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random light readings
G_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random gas readings
T_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random temperature readings
H_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random humidity readings


def add_list_readings_to_db(cur, data_type, data_list):
    for x in data_list:
        cur.execute(
            f"INSERT INTO {data_type}_data ({data_type}_value) VALUES (%s)",
            (x,),)
        
def add_readings_to_db(cur, data_type, value):
        cur.execute(
            f"INSERT INTO {data_type}_data ({data_type}_value) VALUES (%s)",
            (value,),)
        
def live_readings(cur):
    data_type = input("Enter the data type (light, gas, temp, humid): ").strip().lower()
    if data_type not in ["light", "gas", "temp", "humid"]:
        print("Invalid data type. Please enter 'light', 'gas', 'temp', or 'humid'.")
        return
    data_value = float(input("Enter the data value: "))
    add_readings_to_db(cur, data_type, data_value)

def main():
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname=os.getenv("POSTGRES_DB", "mess_rcos"),
        user=os.getenv("POSTGRES_USER", "mess_user"),
        password=os.environ["POSTGRES_PASSWORD"],
    ) as conn:
        with conn.cursor() as cur:
            try:
                while True:
                    live_readings(cur)
                    conn.commit()
            except (KeyboardInterrupt, EOFError): # Handle Ctrl+C or Ctrl+D to stop the loop
                print("\nStopping the reading process.")

if __name__ == "__main__":
    main()