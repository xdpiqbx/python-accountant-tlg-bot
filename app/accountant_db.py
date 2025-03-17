from env_variables import db_params
import psycopg2

import app.sql_queries as sql_query

from env_variables import expert_data_to_insert


async def is_connected():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                print("Connected to the database successfully!")
                return True
    except Exception as e:
        print("Error:", e)
        return False


async def create_tables():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.create_table_warrior())
                cursor.execute(sql_query.create_table_cash_check())
                cursor.execute(sql_query.create_table_cash_back())
                cursor.execute(sql_query.create_table_candidate())
                cursor.execute(sql_query.create_table_banned())
                cursor.execute(sql_query.create_table_check_archive())
                conn.commit()
                print("Tables created successfully!")
    except Exception as e:
        print("Error while creating tables:", e)


async def insert_expert():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.insert_new_user_to_db("warrior"), expert_data_to_insert)
                conn.commit()
                print("Expert inserted successfully!")
    except Exception as e:
        print("Error inserting data:", e)


async def insert_new_user(table_name, data):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.insert_new_user_to_db(table_name), data)
                conn.commit()
                print("New user inserted successfully!")
    except Exception as e:
        print("Error inserting data:", e)


async def insert_check(data):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.insert_check_to_db(), data)
                conn.commit()
                print("Check inserted successfully!")
    except Exception as e:
        print("Error inserting data:", e)


async def insert_check_to_archive(data):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.insert_check_to_archive(), data)
                conn.commit()
                print("Check was archived.")
    except Exception as e:
        print("Error inserting data:", e)


async def insert_refund(data):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.insert_refund_to_db(), data)
                conn.commit()
                print("Refund added!")
    except Exception as e:
        print("Error inserting data:", e)


async def delete_from_db_by_tlg_id(table_name, data):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.delete_by_tlg_id(table_name), (data,))
                conn.commit()
    except Exception as e:
        print("Error inserting data:", e)


async def delete_check_from_cash_check_by_id(check_id):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.delete_check_from_cash_check_by_id(), check_id)
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


async def select_user_by_tlg_id(tlg_id):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_by_tlg_id("warrior"), (tlg_id,))
                result = cursor.fetchone()
                return result
    except Exception as e:
        print("Error inserting data:", e)


async def select_all_warriors():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_all_warriors())
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Error inserting data:", e)


async def select_warriors_who_have_checks_in_archive():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_warriors_who_have_checks_in_archive())
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Error inserting data:", e)


async def select_all_candidates():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_all_candidates())
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Error inserting data:", e)


async def select_balance_by_tlg_id(tlg_id):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_balance_by_tlg_id(), (tlg_id,))
                result = cursor.fetchone()
                return int(result[0])
    except Exception as e:
        print("Error inserting data:", e)


async def select_all_checks_for_current_user(tlg_id, table_name):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_all_checks_for_current_user(table_name), (tlg_id,))
                result = cursor.fetchall()
                return result
    except Exception as e:
        print("Error inserting data:", e)


async def select_check_by_id(check_id):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_check_by_id(), (check_id,))
                result = cursor.fetchone()
                return result
    except Exception as e:
        print("Error inserting data:", e)


async def select_arch_check_by_id(check_id):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_arch_check_by_id(), (check_id,))
                result = cursor.fetchone()
                return result
    except Exception as e:
        print("Error inserting data:", e)


async def update_balance_by_tlg_id(balance, tlg_id):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.update_balance_by_tlg_id(), (balance, tlg_id,))
                conn.commit()
                print("Balance updated successfully!")
    except Exception as e:
        print("Error inserting data:", e)


async def select_sum_balance():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query.select_sum_balance())
                result = cursor.fetchone()
                return result[0] if result and result[0] is not None else 0
    except Exception as e:
        print("Error inserting data:", e)


async def start_db():
    if await is_connected():
        await create_tables()
        # await insert_expert()
        print("Connected.")
    else:
        print("Not connected to the database.")