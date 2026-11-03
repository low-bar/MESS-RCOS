from time import time, sleep

import psycopg
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../web/.env"))

import json 
with open("perfect_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    
L_reading = data["light"]
G_reading = data["gas"]
H_reading = data["humid"]
T_reading = data["temp"]

sensor_id = 9
location = "default_location"


def add_list_readings_to_db(cur, data_type, data_list, sensor_id, loc):
    for x in data_list:
        cur.execute(
            f"INSERT INTO {data_type}_data ({data_type}_value, sensor_id, loc) VALUES (%s, %s, %s)",
            (x, sensor_id, loc),)
        cur.connection.commit()
        sleep(5)
        
def main():
    with psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=5432,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    ) as conn:
        with conn.cursor() as cur:
            add_list_readings_to_db(cur, "light", L_reading, sensor_id, location)
            add_list_readings_to_db(cur, "gas", G_reading, sensor_id, location)
            add_list_readings_to_db(cur, "humid", H_reading, sensor_id, location)
            add_list_readings_to_db(cur, "temp", T_reading, sensor_id, location)

if __name__ == "__main__":
    main()