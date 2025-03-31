import os
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import app.utils as util
import app.buttons as btn
from dotenv import load_dotenv

load_dotenv()

EXPERT_TLG_ID = os.getenv("EXPERT_TLG_ID")


async def list_of_candidates(candidates):
    keyboard = InlineKeyboardBuilder()
    for [tlg_id, nic] in candidates:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{nic} ❌",
                callback_data=f"ban_usr:{tlg_id}:{nic}"
            )
        )
        keyboard.add(
            InlineKeyboardButton(
                text=f"{nic} ✅",
                callback_data=f"add_usr:{tlg_id}:{nic}"
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
            text=btn.BACK,
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
            text=btn.BACK,
            callback_data=f"back_to_main"
        )
    )
    return keyboard.adjust(1).as_markup()


async def main_menu(user_id):
    buttons = [
        btn.ADD_CHECK,
        btn.REFUND,
        btn.YOUR_EXPENSES,
        btn.SQUAD_EXPENSES,
        btn.ARCHIVE,
        # btn.REFUND_HISTORY, # TODO
        btn.STATISTICS
    ]
    if EXPERT_TLG_ID == user_id:
        buttons.append(btn.ALL_WARRIORS)
        buttons.append(btn.CANDIDATES)
        # buttons.append(btn.BANNED)  # TODO
    inline_keyboard = [[InlineKeyboardButton(text=button, callback_data=button)] for button in buttons]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def back_to_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn.BACK_TO_MAIN, callback_data=f"back_to_main")]
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
            text=btn.BACK, callback_data="back_to_main"
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
            text=btn.BACK, callback_data=btn.SQUAD_EXPENSES
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
            text=btn.BACK, callback_data=btn.ARCHIVE
        )
    )
    return keyboard.adjust(1).as_markup()


async def add_to_archive(check_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Send to archive", callback_data=f"arch_check:{check_id}")],
        [InlineKeyboardButton(text=btn.BACK, callback_data=btn.YOUR_EXPENSES)]
    ])


async def squad_exp_user_checks(check_id, tlg_id, name, to_show_arch_button):
    if to_show_arch_button:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Send to archive", callback_data=f"arch_check:{check_id}")],
            [InlineKeyboardButton(text=btn.BACK, callback_data=f"user_expenses:{tlg_id}:{name}")]
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn.BACK, callback_data=f"user_expenses:{tlg_id}:{name}")]
    ])


async def call_squad_expenses():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn.BACK, callback_data=btn.SQUAD_EXPENSES)]
    ])


async def call_your_expenses():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn.BACK, callback_data=btn.YOUR_EXPENSES)]
    ])


async def back_to_user_archive(callback_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn.BACK, callback_data=callback_data)]
    ])


no_comment = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="No comment")]
], resize_keyboard=True)
