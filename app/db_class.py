import os
import asyncpg
from dotenv import load_dotenv
import app.sql_queries as sql_query

load_dotenv()

DB_PARAMS = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(**DB_PARAMS)
        print("Database pool created successfully!")

    async def disconnect(self):
        await self.pool.close()
        print("Database pool closed.")

    async def execute(self, query, *args, fetch=False, fetchval=False, fetchrow=False):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                if fetch:
                    return await conn.fetch(query, *args)
                elif fetchval:
                    return await conn.fetchval(query, *args)
                elif fetchrow:
                    return await conn.fetchrow(query, *args)
                else:
                    return await conn.execute(query, *args)

    async def is_connected(self):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("SELECT 1")
                print("Connected to the database successfully!")
                return True
        except Exception as e:
            print("Error:", e)
            return False

    async def create_tables(self):
        queries = [
            sql_query.create_table_warrior(),
            sql_query.create_table_cash_check(),
            sql_query.create_table_cash_back(),
            sql_query.create_table_candidate(),
            sql_query.create_table_banned(),
            sql_query.create_table_check_archive(),
        ]
        for query in queries:
            await self.execute(query)
        print("Tables created successfully!")

    async def insert_new_user(self, table_name, data):
        await self.execute(sql_query.insert_new_user_to_db(table_name), *data)
        print("New user inserted successfully!")

    async def insert_check(self, data):
        await self.execute(sql_query.insert_check_to_db(), *data)
        print("Check inserted successfully!")

    async def insert_check_to_archive(self, data):
        await self.execute(sql_query.insert_check_to_archive(), *data)
        print("Check added to archive!")

    async def insert_refund(self, data):
        await self.execute(sql_query.insert_refund_to_db(), *data)
        print("Refund added!")

    async def delete_from_db_by_tlg_id(self, table_name, data):  # 1 maybe same with delete_check_from_cash_check_by_id
        await self.execute(sql_query.delete_by_tlg_id(table_name), *data)
        print("Deleted from DB!")

    async def delete_check_from_cash_check_by_id(self, data):  # 1 maybe same with delete_from_db_by_tlg_id
        await self.execute(sql_query.delete_check_from_cash_check_by_id(), *data)
        print("Deleted from DB!")

    async def select_user_by_tlg_id(self, data):
        return await self.execute(sql_query.select_by_tlg_id("warrior"), *data, fetchrow=True)

    async def is_user_exists(self, data, table_name):
        return await self.execute(sql_query.select_by_tlg_id(table_name), *data, fetchrow=True)

    async def select_all_warriors_with_balance(self):
        return await self.execute(sql_query.select_all_warriors_with_balance(), fetch=True)

    async def select_all_warriors(self):
        return await self.execute(sql_query.select_all_warriors(), fetch=True)

    async def select_warriors_who_have_checks_in_archive(self):
        return await self.execute(sql_query.select_warriors_who_have_checks_in_archive(), fetch=True)

    async def select_all_candidates(self):
        return await self.execute(sql_query.select_all_candidates(), fetch=True)

    async def count_candidates(self):
        return await self.execute(sql_query.count_candidates(), fetchval=True)

    async def select_balance_by_tlg_id(self, data):
        return await self.execute(sql_query.select_balance_by_tlg_id(), *data,  fetchval=True)

    async def select_all_checks_for_current_user(self, data, table_name):
        return await self.execute(sql_query.select_all_checks_for_current_user(table_name), *data, fetch=True)

    async def select_check_by_id(self, data):
        return await self.execute(sql_query.select_check_by_id(), *data, fetchrow=True)

    async def select_arch_check_by_id(self, data):
        return await self.execute(sql_query.select_arch_check_by_id(), *data, fetchrow=True)

    async def update_balance_by_tlg_id(self, data):
        await self.execute(sql_query.update_balance_by_tlg_id(), *data)  # data = (balance, tlg_id,)
        print("Balance updated successfully!")

    async def select_sum_balance(self):
        return await self.execute(sql_query.select_sum_balance(), fetchval=True) or 0

    async def select_total_sum_refund(self):
        return await self.execute(sql_query.select_total_refund(), fetchval=True) or 0

    async def start_db(self):
        await self.connect()
        if await self.is_connected():
            await self.create_tables()
            print("Connected and initialized database.")
        else:
            print("Failed to connect to the database.")
