from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import app.accountant_db as db
import app.utils as util


async def list_of_candidates():
    candidates = await db.select_all_candidates()
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


async def list_of_warriors(users):
    keyboard = InlineKeyboardBuilder()
    for user in users:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{user[1]} - {util.hryvna_format(user[2])}",
                callback_data=f"user_expenses:{user[0]}:{user[1]}"
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text=f"Back",
            callback_data=f"back_to_main"
        )
    )
    return keyboard.adjust(1).as_markup()


async def list_of_warriors_archived_checks(users):
    keyboard = InlineKeyboardBuilder()
    for user in users:
        keyboard.add(
            InlineKeyboardButton(
                text=user[1],
                callback_data=f"user_archive:{user[0]}:{user[1]}"
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text=f"Back",
            callback_data=f"back_to_main"
        )
    )
    return keyboard.adjust(1).as_markup()


async def main_menu():
    buttons = ["Add check", "Refund", "Your expenses", "Squad expenses", "Archive", "Statistics"]
    inline_keyboard = [[InlineKeyboardButton(text=button, callback_data=button)] for button in buttons]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def back_to_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back to Menu", callback_data=f"back_to_main")]
    ])


async def all_checks_with_buttons(checks):
    keyboard = InlineKeyboardBuilder()
    for check in checks:
        dt = util.reformat_datetime_from_db(check[1])
        keyboard.add(
            InlineKeyboardButton(
                text=f"{util.hryvna_format(check[2])} - {dt}",
                callback_data=f"check_data_for_my_exp:{check[0]}"
            )
        )
        keyboard.add(
            InlineKeyboardButton(
                text=f"Send to archive", callback_data=f"arch_check:{check[0]}"
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text=f"Back", callback_data="back_to_main"
        )
    )
    return keyboard.adjust(2).as_markup()


async def all_checks_with_buttons_for_current_from_sqad_exp(checks, tlg_id, name, to_show_arch_button):
    keyboard = InlineKeyboardBuilder()
    for check in checks:
        dt = util.reformat_datetime_from_db(check[1])
        keyboard.add(
            InlineKeyboardButton(
                text=f"{util.hryvna_format(check[2])} - {dt}",
                callback_data=f"check_data_for_current:{check[0]}:{tlg_id}:{name}"
            )
        )
        if to_show_arch_button:
            keyboard.add(
                InlineKeyboardButton(
                    text=f"Send to archive", callback_data=f"arch_check:{check[0]}"
                )
            )
    keyboard.add(
        InlineKeyboardButton(
            text=f"Back", callback_data="Squad expenses"
        )
    )
    return keyboard.adjust(2 if to_show_arch_button else 1).as_markup()


async def all_archived_checks(checks, name):
    keyboard = InlineKeyboardBuilder()
    for check in checks:
        dt = util.reformat_datetime_from_db(check[1])
        keyboard.add(
            InlineKeyboardButton(
                text=f"{util.hryvna_format(check[2])} - {dt}",
                callback_data=f"check_from_archive:{check[0]}:{name}"
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text=f"Back", callback_data="Archive"
        )
    )
    return keyboard.adjust(1).as_markup()


async def add_to_archive(check_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Send to archive", callback_data=f"arch_check:{check_id}")],
        [InlineKeyboardButton(text="Back", callback_data=f"Your expenses")]
    ])


async def squad_exp_user_checks(check_id, tlg_id, name, to_show_arch_button):
    if to_show_arch_button:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Send to archive", callback_data=f"arch_check:{check_id}")],
            [InlineKeyboardButton(text="Back", callback_data=f"user_expenses:{tlg_id}:{name}")]
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data=f"user_expenses:{tlg_id}:{name}")]
    ])


async def call_squad_expenses():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data=f"Squad expenses")]
    ])


async def call_your_expenses():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data=f"Your expenses")]
    ])


async def back_to_user_archive(callback_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data=callback_data)]
    ])


no_comment = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="No comment")]
], resize_keyboard=True)

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
