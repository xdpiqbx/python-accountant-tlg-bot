from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import app.accountant_db as db

# Inline buttons
# candidate_to_warrior = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Add Warrior", callback_data="add_usr")],
#     [InlineKeyboardButton(text="Cancel", callback_data="cancel_new_warrior")]
# ])

async def list_of_candidates():
    candidates = await db.select_all_users("candidate")
    keyboard = InlineKeyboardBuilder()
    for candidate in candidates:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{candidate[1]} ❌",
                callback_data=f"ban_usr:{candidate[0]}:{candidate[1]}"
            )
        )
        keyboard.add(
            InlineKeyboardButton(
                text=f"{candidate[1]} ✅",
                callback_data=f"add_usr:{candidate[0]}:{candidate[1]}"
            )
        )
    return keyboard.adjust(2).as_markup()
# async def inline_cities():
#     cities = ["Kyiv", "Brisbane", "Portland"]
#     keyboard = InlineKeyboardBuilder()
#     for city in cities:
#         keyboard.add(InlineKeyboardButton(text=city, url="https://youtube.com"))
#     return keyboard.adjust(2).as_markup()

# ============================================================================

# # Reply big buttons
# main = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text="Catalog")],
#     [KeyboardButton(text="Cart"), KeyboardButton(text="Contacts")]
# ], resize_keyboard=True, input_field_placeholder="Choose menu bottom...")
#
# # Inline buttons
# mainInline = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Catalog", callback_data="catalog")],
#     [
#         InlineKeyboardButton(text="Cart", callback_data="cart"),
#         InlineKeyboardButton(text="Contacts", callback_data="contacts")
#     ]
# ])
#
# settings = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="YouTube", url="https://youtube.com")],
#     [InlineKeyboardButton(text="Google", url="http://google.com")],
# ])
#
# get_contact = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text="Send your contact", request_contact=True)]
# ], resize_keyboard=True)
#
# async def reply_cars():
#     cars = ["Tesla", "Mercedes", "Mitsubishi"]
#     keyboard = ReplyKeyboardBuilder()
#     for car in cars:
#         keyboard.add(KeyboardButton(text=car))
#     return keyboard.adjust(2).as_markup()
#
#
# async def inline_cities():
#     cities = ["Kyiv", "Brisbane", "Portland"]
#     keyboard = InlineKeyboardBuilder()
#     for city in cities:
#         keyboard.add(InlineKeyboardButton(text=city, url="https://youtube.com"))
#     return keyboard.adjust(2).as_markup()
