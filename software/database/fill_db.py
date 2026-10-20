import os
import psycopg
import random

L_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random light readings
G_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random gas readings
T_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random temperature readings
H_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random humidity readings

temp_sensor_id = 1
temp_loc = "Room 101"

def add_list_readings_to_db(cur, data_type, data_list, sensor_id, loc):
    for x in data_list:
        cur.execute(
            f"INSERT INTO {data_type}_data ({data_type}_value, sensor_id, loc) VALUES (%s, %s, %s)",
            (x, sensor_id, loc),)
def add_readings_to_db(cur, data_type, value, id, loc):
        cur.execute(
            f"INSERT INTO {data_type}_data ({data_type}_value, sensor_id, loc) VALUES (%s, %s, %s)",
            (value, id, loc),)

def live_readings(cur):
    data_type = input("Enter the data type (light, gas, temp, humid): ").strip().lower()
    if data_type not in ["light", "gas", "temp", "humid"]:
        print("Invalid data type. Please enter 'light', 'gas', 'temp', or 'humid'.")
        return
    data_value = float(input("Enter the data value: "))
    add_readings_to_db(cur, data_type, data_value, temp_sensor_id, temp_loc)

def output_readings(cur, data_type):
    cur.execute(f"SELECT recorded_at, {data_type}_value, sensor_id, loc FROM {data_type}_data ORDER BY recorded_at DESC LIMIT 10")
    rows = cur.fetchall()
    print(f"\nLast 10 readings for {data_type}:")
    print(f"{'Recorded at':19} {'Value':>10}")
    print("-" * 31)
    for row in rows:
        timestamp = row[0].strftime("%Y-%m-%d %H:%M:%S")
        print(f"Senor {row[2]}, Location: {row[3]}: {timestamp:19} {row[1]:10.2f}")


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
                    choice = input("Enter 'live' to input live readings, 'output' to view last 10 readings, or 'exit' to quit: ").strip().lower()
                    if choice == 'live':
                        while True:
                            live_readings(cur)
                            if input("Enter 'back' to return to the main menu: ").strip().lower() == 'back':
                                break
                            conn.commit()
                    elif choice == 'output':
                        data_type = input("Enter the data type (light, gas, temp, humid): ").strip().lower()
                        if data_type not in ["light", "gas", "temp", "humid"]:
                            print("Invalid data type. Please enter 'light', 'gas', 'temp', or 'humid'.")
                            continue
                        output_readings(cur, data_type)
                    elif choice == 'exit':
                        break
            except (KeyboardInterrupt, EOFError): # Handle Ctrl+C or Ctrl+D to stop the loop
                print("\nStopping the reading process.")

if __name__ == "__main__":
    main()