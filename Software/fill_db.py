import os
import psycopg
import random

L_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random light readings
G_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random gas readings
T_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random temperature readings
H_reading = [random.uniform(0, 100) for _ in range(10)]  # Generate 10 random humidity readings


def add_readings_to_db(cur, data_type, data_list):
    for x in data_list:
        cur.execute(
            f"INSERT INTO {data_type}_data ({data_type}_value) VALUES (%s)",
            (x,),)

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname=os.getenv("POSTGRES_DB", "mess_rcos"),
    user=os.getenv("POSTGRES_USER", "mess_user"),
    password=os.environ["POSTGRES_PASSWORD"],
) as conn:
    with conn.cursor() as cur:
        if L_reading is not None:
            add_readings_to_db(cur, "light", L_reading)
        if G_reading is not None:
            add_readings_to_db(cur, "gas", G_reading)
        if T_reading is not None:
            add_readings_to_db(cur, "temp", T_reading)
        if H_reading is not None:
            add_readings_to_db(cur, "humid", H_reading)
