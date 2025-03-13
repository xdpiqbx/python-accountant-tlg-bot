from datetime import datetime

from aiogram import Router, html, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.accountant_db as db

from env_variables import EXPERT, TOKEN, cloudinary_config, CLOUDINARY_FOLDER

# Cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ---------------------------------------------------------------------------


router = Router()


class Register(StatesGroup):
    nic = State()


class CashCheck(StatesGroup):
    user_name = State()
    image_url = State()
    amount = State()
    comment = State()

class CashBack(StatesGroup):
    user_name = State()
    amount = State()
    comment = State()


# /start
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if await db.is_user_exists(str(message.from_user.id), "banned"):
        await message.answer("❌ You have been banned ❌")
        return
    if not await db.is_user_exists(str(message.from_user.id), "warrior"):
        await message.answer("REGISTRATION needed.")
        await state.set_state(Register.nic)
        await message.answer("Send me your call sign (in english):")
    else:
        await message.answer("Hello")


@router.message(Register.nic)
async def register(message: Message, state: FSMContext):
    tlg_id = str(message.from_user.id)
    nic = message.text
    await state.clear()
    if not await db.is_user_exists(tlg_id, "candidate"):
        db.insert_new_user("candidate", (tlg_id, nic,))
        await message.answer("Wait for approve.")
        await message.bot.send_message(
            chat_id=EXPERT,
            text=f"We have a new warrior:\nCall sign: {nic}\nTelegram id: {tlg_id}",
            reply_markup=await kb.list_of_candidates()
        )
    else:
        await message.answer("I know about you. Just wait.")


@router.callback_query(F.data.startswith("add_usr"))
async def add_new_warrior_to_db(callback: CallbackQuery):
    user_data = tuple(callback.data.split(":")[1:])
    # add user to warrior
    db.insert_new_user("warrior", user_data)
    # remove from candidates & banned
    db.delete_from_db_by_tlg_id("candidate", user_data[0])
    db.delete_from_db_by_tlg_id("banned", user_data[0])
    await callback.bot.send_message(chat_id=user_data[0], text="✅ Wellcome to the club =)")
    await callback.message.edit_reply_markup(f"Added to db. {user_data[1]}")


@router.callback_query(F.data.startswith("ban_usr"))
async def add_new_warrior_to_db(callback: CallbackQuery):
    user_data = tuple(callback.data.split(":")[1:])
    db.insert_new_user("banned", user_data)
    db.delete_from_db_by_tlg_id("candidate", user_data[0])
    db.delete_from_db_by_tlg_id("warrior", user_data[0])
    await callback.bot.send_message(chat_id=user_data[0], text="❌ You have been banned ❌")
    await callback.message.edit_reply_markup(f"Banned. {user_data[1]}")


# /add_check
@router.message(Command('add_check'))
async def add_check(message: Message, state: FSMContext):
    if await db.is_user_exists(str(message.from_user.id), "banned"):
        await message.answer("❌ You have been banned ❌")
        return
    user = await db.select_user_by_tlg_id(str(message.from_user.id))
    await message.answer(f"Hello {user[1]}\nGive me image of your check")
    await state.update_data(user_name=user[1])
    await state.set_state(CashCheck.image_url)

@router.message(F.photo, CashCheck.image_url)
async def get_check_image(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file = await message.bot.get_file(photo.file_id)
    file_path = f"https://api.telegram.org/file/bot{TOKEN}/{photo_file.file_path}"
    data = await state.get_data()
    formatted_time = datetime.now().strftime("%d.%m.%Y_%H:%M:%S")

    config = cloudinary.config(secure=True)
    config.cloud_name = cloudinary_config["cloud_name"]
    config.api_key = cloudinary_config["api_key"]
    config.api_secret = cloudinary_config["api_secret"]

    uploaded_image = cloudinary.uploader.upload(
        file_path,
        asset_folder=CLOUDINARY_FOLDER,
        public_id=f"{data['user_name']}_[{formatted_time}]"
    )
    await state.update_data(image_url=uploaded_image['secure_url'])
    await state.set_state(CashCheck.amount)
    await message.answer("How much did you spend?\nGive me a whole number without a penny (round it).")

@router.message(CashCheck.amount)
async def get_amount(message: Message, state: FSMContext):
    value = message.text
    if not value.isdigit():
        await message.answer("❌ Please enter a valid amount.")
        return
    await state.update_data(amount=int(value))
    await state.set_state(CashCheck.comment)
    await message.answer(
        "Send me any comment about this purchase or push big button 'No comments' down below.",
        reply_markup=kb.no_comment
    )

@router.message(CashCheck.comment)
async def get_comment_about_purchase(message: Message, state: FSMContext):
    tlg_id = str(message.from_user.id)
    await state.update_data(comment=message.text)
    await state.set_state(CashCheck.comment)
    data = await state.get_data()
    check_data_to_insert = (int(tlg_id), data['image_url'], data['amount'], data['comment'],)
    db.insert_check(check_data_to_insert)
    # get balance
    current_balance = db.select_balance_by_tlg_id(tlg_id)
    # add to balance
    new_balance = current_balance + int(data['amount'])
    # update balance
    db.update_balance_by_tlg_id(new_balance, tlg_id)
    await message.answer(f"Your balance has been increased.\nCurrent balance: {new_balance}")
    await state.clear()

# /refund
@router.message(Command('refund'))
async def refund(message: Message, state: FSMContext):
    if await db.is_user_exists(str(message.from_user.id), "banned"):
        await message.answer("❌ You have been banned ❌")
        return
    user = await db.select_user_by_tlg_id(str(message.from_user.id))
    await state.set_state(CashBack.amount)
    await message.answer(f"Hello {user[1]}\nWrite down how much money you were refunded.")

@router.message(CashBack.amount)
async def refund_amount(message: Message, state: FSMContext):
    value = message.text
    if not value.isdigit():
        await message.answer("❌ Please enter a valid amount.")
        return
    await state.update_data(amount=value)
    await state.set_state(CashBack.comment)
    await message.answer(
        "Send me any comment about this refund or push big button 'No comments' down below.",
        reply_markup=kb.no_comment
    )

@router.message(CashBack.comment)
async def get_comment_about_refund(message: Message, state: FSMContext):
    tlg_id = str(message.from_user.id)
    await state.update_data(comment=message.text)
    await state.set_state(CashBack.comment)
    data = await state.get_data()
    refund_data_to_insert = (int(tlg_id), data['amount'], data['comment'],)
    db.insert_refund(refund_data_to_insert)
    # get balance
    current_balance = db.select_balance_by_tlg_id(tlg_id)
    # reduce balance
    new_balance = current_balance - int(data['amount'])
    # update balance
    db.update_balance_by_tlg_id(new_balance, tlg_id)
    await message.answer(f"Your balance has been reduced.\nCurrent balance: {new_balance}")
    await state.clear()


# my expenses


# @router.message(Command("register"))
# async def reg_one(message: Message, state: FSMContext):
#     await state.set_state(Reg.name)
#     await message.answer("Input your name:")
#
#
# @router.message(Reg.name)
# async def reg_two(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Reg.number)
#     await message.answer("Input your number:")
#
#
# @router.message(Reg.number)
# async def two_three(message: Message, state: FSMContext):
#     await state.update_data(number=message.text)
#     data = await state.get_data()
#     await message.answer("Registration done!")
#     await message.answer(f"Name: {data["name"]} Number: {data["number"]}")
#     await state.clear()

# # /start
# @router.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await message.answer(
#         f"Hello, {html.bold(message.from_user.full_name)}!",
#         reply_markup=kb.mainInline
#     )
#
#
# # /help
# @router.message(Command('help'))
# async def get_help(message: Message):
#     await message.answer(
#         f"HELP \n{message.from_user.id} \n{message.from_user.first_name}",
#         reply_markup=kb.settings
#     )
#
#
# @router.message(Command('contact'))
# async def get_help(message: Message):
#     await message.answer(
#         f"Contact send",
#         reply_markup=kb.get_contact
#     )
#
#
# # /cars
# @router.message(Command('cars'))
# async def get_help(message: Message):
#     await message.answer(
#         f"cars \n{message.from_user.id} \n{message.from_user.first_name}",
#         reply_markup=await kb.reply_cars()
#     )
#
#
# # /city
# @router.message(Command('city'))
# async def get_help(message: Message):
#     await message.answer(
#         f"cities \n{message.from_user.id} \n{message.from_user.first_name}",
#         reply_markup=await kb.inline_cities()
#     )
#
#
# # /who_am_i
# @router.message(Command('who_am_i'))
# async def get_help(message: Message):
#     print(message.from_user)
#     await message.reply(f"{message.from_user.id} "
#                         f"\n{message.from_user.first_name}")
#
#
# # How are you?
# @router.message(F.text == "How are you?")
# async def how_are_you(message: Message):
#     await message.answer("I am ok =)")
#
#
# # Photo
# @router.message(F.photo)
# async def how_are_you(message: Message):
#     await message.answer(f"ID photo: {message.photo[-1].file_id}")
#
#
# # Send photo by id or link
# @router.message(Command("get_photo"))
# async def get_photo(message: Message):
#     # photo_id = "AgACAgIAAxkBAAMTZ6izif6ExZ6Af1K_DNilJdl5rOIAAjDoMRtYp0hJQI26-e9jJ4cBAAMCAANtAAM2BA"
#     photo_id = "https://media.istockphoto.com/id/844000052/uk/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D1%96-%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F/%D0%BF%D0%BE%D0%BA%D0%B0%D0%B6%D1%87%D0%B8%D0%BA-%D0%BC%D1%96%D1%81%D1%86%D1%8F-%D0%B7%D0%B0%D0%BF%D0%BE%D0%B2%D0%BD%D0%B5%D0%BD%D0%BD%D1%8F-%D0%B7%D0%B0-%D0%B7%D0%B0%D0%BC%D0%BE%D0%B2%D1%87%D1%83%D0%B2%D0%B0%D0%BD%D0%BD%D1%8F%D0%BC-%D1%87%D0%BE%D0%BB%D0%BE%D0%B2%D1%96%D0%BA-%D1%96-%D0%B6%D1%96%D0%BD%D0%BA%D0%B0.jpg?s=612x612&w=0&k=20&c=talHWUK32xc3PoTKuaUKW4r-CrofXvSnoFw0jOlsZGQ="
#     await message.answer_photo(photo=photo_id, caption='default user avatar')
#
#
# @router.callback_query(F.data == "catalog")
# async def catalog(callback: CallbackQuery):
#     await callback.answer("You have choose catalog")
#     # await callback.answer("You have chosen catalog", show_alert=True)
#     # await callback.message.answer("callback Catalog")
#     # await callback.message.answer("callback Catalog")
#     await callback.message.edit_text("callback Catalog", reply_markup=await kb.inline_cities())
#
#
# # @router.callback_query(F.data == "cart")
# # @router.callback_query(F.data == "contacts")
#
#
# @router.message(Command("register"))
# async def reg_one(message: Message, state: FSMContext):
#     await state.set_state(Reg.name)
#     await message.answer("Input your name:")
#
#
# @router.message(Reg.name)
# async def reg_two(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Reg.number)
#     await message.answer("Input your number:")
#
#
# @router.message(Reg.number)
# async def two_three(message: Message, state: FSMContext):
#     await state.update_data(number=message.text)
#     data = await state.get_data()
#     await message.answer("Registration done!")
#     await message.answer(f"Name: {data["name"]} Number: {data["number"]}")
#     await state.clear()
#
# # ================================================================================== echo_handler !!!
#
# # @router.message()
# # async def echo_handler(message: Message) -> None:
# #     try:
# #         # Send a copy of the received message
# #         await message.send_copy(chat_id=message.chat.id)
# #     except TypeError:
# #         # But not all the types is supported to be copied so need to handle it
# #         await message.answer("Nice try!")
