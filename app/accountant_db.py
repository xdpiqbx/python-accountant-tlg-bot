from env_variables import db_params
import psycopg2

import app.sql_queries as sql_query

from env_variables import expert_data_to_insert


def is_connected():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                print("Connected to the database successfully!")
                return True
    except Exception as e:
        print("Error:", e)
        return False


def create_tables():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.create_table_warrior())
                cursor.execute(sql_query.create_table_cash_check())
                cursor.execute(sql_query.create_table_cash_back())
                cursor.execute(sql_query.create_table_candidate())
                cursor.execute(sql_query.create_table_banned())
                conn.commit()
                print("Tables created successfully!")
    except Exception as e:
        print("Error while creating tables:", e)


def insert_expert():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.insert_new_user_to_db("warrior"), expert_data_to_insert)
                conn.commit()
                print("Data inserted successfully!")
    except Exception as e:
        print("Error inserting data:", e)

def insert_new_user(table_name, data):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.insert_new_user_to_db(table_name), data)
                conn.commit()
                print("Data inserted successfully!")
    except Exception as e:
        print("Error inserting data:", e)

def delete_from_db_by_tlg_id(table_name, data):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.delete_by_tlg_id(table_name), (data,))
                conn.commit()
    except Exception as e:
        print("Error inserting data:", e)


async def is_user_exists(tlg_id, table_name):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_by_tlg_id(table_name), (tlg_id,))
                result = cursor.fetchone()
                return result is not None
    except Exception as e:
        print("Error inserting data:", e)

async def select_all_users(table_name):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_all_users(table_name))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Error inserting data:", e)


if is_connected():
    # create_tables()
    # insert_expert()
    print("Connected.")
else:
    print("Not connected to the database.")
