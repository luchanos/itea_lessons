"""
table for shops
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""CREATE TABLE IF NOT EXISTS shops (
shop_id SERIAL NOT NULL,
shop_name TEXT NOT NULL,
address TEXT NOT NULL,
created_dt DATE NOT NULL,
updated_dt DATE)""",

         """
         DROP TABLE IF EXISTS shops
         """)
]
