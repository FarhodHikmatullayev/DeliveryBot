from datetime import datetime
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from config.settings import DEVELOPMENT_MODE
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        if DEVELOPMENT_MODE:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        else:
            self.pool = await asyncpg.create_pool(
                dsn=config.DATABASE_URL
            )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # for users
    async def create_user(self, phone, username, full_name, telegram_id):
        sql = "INSERT INTO Users (phone, username, full_name, telegram_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, phone, username, full_name, telegram_id, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_user(self, user_id, **kwargs):
        sql = "UPDATE Users SET "
        parameters = {}
        for i, (key, value) in enumerate(kwargs.items(), start=1):
            sql += f"{key} = ${i}, "
            parameters[key] = value
        sql = sql[:-2] + " WHERE id = ${}".format(len(parameters) + 1)
        parameters["id"] = user_id
        return await self.execute(sql, *parameters.values(), execute=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM Users WHERE id = $1"
        return await self.execute(sql, user_id, execute=True)

        # CRUD operations for Order model

    async def create_order(self, user_id, products, payment, created_at=datetime.now()):
        sql = "INSERT INTO Orders (user_id, products, payment, created_at) VALUES($1, $2, $3, $4) RETURNING *"
        return await self.execute(sql, user_id, products, payment, created_at, fetchrow=True)

    async def select_order(self, **kwargs):
        sql = "SELECT * FROM Orders WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_orders(self):
        sql = "SELECT * FROM Orders"
        return await self.execute(sql, fetch=True)

    async def update_order(self, order_id, **kwargs):
        sql = "UPDATE Orders SET "
        parameters = {}
        for i, (key, value) in enumerate(kwargs.items(), start=1):
            sql += f"{key} = ${i}, "
            parameters[key] = value
        sql = sql[:-2] + " WHERE id = ${}".format(len(parameters) + 1)
        parameters["id"] = order_id
        return await self.execute(sql, *parameters.values(), execute=True)

    async def delete_order(self, order_id):
        sql = "DELETE FROM Orders WHERE id = $1"
        return await self.execute(sql, order_id, execute=True)

    # CRUD operations for Stock model
    async def create_stock(self, product_name, products_url, created_at=datetime.now()):
        sql = "INSERT INTO Stock (product_name, products_url, created_at) VALUES($1, $2, $3) RETURNING *"
        return await self.execute(sql, product_name, products_url, created_at, fetchrow=True)

    async def select_stock(self, **kwargs):
        sql = "SELECT * FROM Stock WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_stocks(self):
        sql = "SELECT * FROM Stock"
        return await self.execute(sql, fetch=True)

    async def update_stock(self, stock_id, **kwargs):
        sql = "UPDATE Stock SET "
        parameters = {}
        for i, (key, value) in enumerate(kwargs.items(), start=1):
            sql += f"{key} = ${i}, "
            parameters[key] = value
        sql = sql[:-2] + " WHERE id = ${}".format(len(parameters) + 1)
        parameters["id"] = stock_id
        return await self.execute(sql, *parameters.values(), execute=True)

    async def delete_stock(self, stock_id):
        sql = "DELETE FROM Stock WHERE id = $1"
        return await self.execute(sql, stock_id, execute=True)
