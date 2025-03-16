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
    tlg_id = str(message.from_user.id)
    if await db.is_user_exists(tlg_id, "banned"):
        await message.answer("❌ You have been banned ❌")
        return
    if not  await db.is_user_exists(tlg_id, "warrior"):
        await message.answer("REGISTRATION needed.")
        await state.set_state(Register.nic)
        await message.answer("Send me your call sign (in english):", reply_markup=None)
    else:
        user =  await db.select_user_by_tlg_id(tlg_id)
        await message.answer(f"Hi, {user[1]} what we do?\n"
                             f"(chose the option down below)",
                             reply_markup=await kb.main_menu())


@router.message(Register.nic)
async def register(message: Message, state: FSMContext):
    tlg_id = str(message.from_user.id)
    nic = message.text
    await state.clear()
    if not await db.is_user_exists(tlg_id, "candidate"):
        await db.insert_new_user("candidate", (tlg_id, nic,))
        await message.answer("Wait for approve.")
        await message.bot.send_message(
            chat_id=EXPERT,
            text=f"We have a new warrior:\nCall sign: {nic}\nTelegram id: {tlg_id}",
            reply_markup=await kb.list_of_candidates()
        )
    else:
        await message.answer("I know about you. Just wait.", reply_markup=None)


@router.callback_query(F.data.startswith("add_usr"))
async def add_new_warrior_to_db(callback: CallbackQuery):
    user_data = tuple(callback.data.split(":")[1:])
    # add user to warrior
    await db.insert_new_user("warrior", user_data)
    # remove from candidates & banned
    await db.delete_from_db_by_tlg_id("candidate", user_data[0])
    await db.delete_from_db_by_tlg_id("banned", user_data[0])
    await callback.bot.send_message(
        chat_id=user_data[0],
        text="✅ Wellcome to the club =)",
        reply_markup=await kb.main_menu()
    )
    await callback.message.edit_reply_markup(f"Added to db. {user_data[1]}")


@router.callback_query(F.data.startswith("ban_usr"))
async def add_new_warrior_to_db(callback: CallbackQuery):
    user_data = tuple(callback.data.split(":")[1:])
    await db.insert_new_user("banned", user_data)
    await db.delete_from_db_by_tlg_id("candidate", user_data[0])
    await db.delete_from_db_by_tlg_id("warrior", user_data[0])
    await callback.bot.send_message(chat_id=user_data[0], text="❌ You have been banned ❌", reply_markup=None)
    await callback.message.edit_reply_markup(f"Banned. {user_data[1]}", reply_markup=None)


# Add check
@router.callback_query(F.data.startswith("Add check"))
async def add_check(callback: CallbackQuery, state: FSMContext):
    if await db.is_user_exists(str(callback.from_user.id), "banned"):
        await callback.message.answer("❌ You have been banned ❌", reply_markup=None)
        return
    user = await db.select_user_by_tlg_id(str(callback.from_user.id))
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await state.update_data(user_name=user[1])
    await state.set_state(CashCheck.image_url)
    await callback.message.answer(f"Give me image of your check", reply_markup=None)


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
        asset_folder=f"{CLOUDINARY_FOLDER}/{data['user_name']}",
        public_id=f"{data['user_name']}_[{formatted_time}]"
    )
    await state.update_data(image_url=uploaded_image['secure_url'])
    await state.set_state(CashCheck.amount)
    await message.answer(
        "How much did you spend?\nGive me a whole number without a penny (round it).",
        reply_markup=None
    )


@router.message(CashCheck.amount)
async def get_amount(message: Message, state: FSMContext):
    value = message.text
    if not value.isdigit():
        await message.answer("❌ Please enter a valid amount.", reply_markup=None)
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
    await db.insert_check(check_data_to_insert)
    # get balance
    current_balance = await db.select_balance_by_tlg_id(tlg_id)
    # add to balance
    new_balance = current_balance + int(data['amount'])
    # update balance
    await db.update_balance_by_tlg_id(new_balance, tlg_id)
    await message.answer(
        f"Your balance has been increased.\nCurrent balance: {new_balance}",
        reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Refund
@router.callback_query(F.data.startswith("Refund"))
async def refund(callback: CallbackQuery, state: FSMContext):
    if await db.is_user_exists(str(callback.from_user.id), "banned"):
        await callback.message.answer("❌ You have been banned ❌", reply_markup=None)
        return
    user = await db.select_user_by_tlg_id(str(callback.from_user.id))
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await state.set_state(CashBack.amount)
    await callback.message.answer(f"Hello {user[1]}\nWrite down how much money you were refunded.", reply_markup=None)


@router.message(CashBack.amount)
async def refund_amount(message: Message, state: FSMContext):
    value = message.text
    if not value.isdigit():
        await message.answer("❌ Please enter a valid amount.")
        return
    await state.update_data(amount=int(value))
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
    await db.insert_refund(refund_data_to_insert)
    # get balance
    current_balance = await db.select_balance_by_tlg_id(tlg_id)
    # reduce balance
    new_balance = current_balance - int(data['amount'])
    # update balance
    await db.update_balance_by_tlg_id(new_balance, tlg_id)
    await message.answer(
        f"Your balance has been reduced.\nCurrent balance: {new_balance}",
        reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Your expenses
@router.callback_query(F.data.startswith("Your expenses"))
async def refund(callback: CallbackQuery):
    if await db.is_user_exists(str(callback.from_user.id), "banned"):
        await callback.message.answer("❌ You have been banned ❌", reply_markup=None)
        return
    checks = await db.select_all_checks_for_current_user(str(callback.from_user.id))
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer(
        text=f"This is all your expenses for today\n"
             f"If you have already refunded the money, simply add the old entries to the archive "
             f"by clicking the corresponding button.",
        reply_markup=await kb.all_checks_with_buttons(checks))


@router.callback_query(F.data.startswith("check"))
async def current_check(callback: CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    check_id = tuple(callback.data.split(":")[1:])
    # select all data about check by its id
    check_data = await db.select_check_by_id(check_id)  # warrior_id, image_url, created_at, amount, comment
    # send as message
    formatted_number = f"{check_data[3]:,}".replace(",", chr(0x2009))  # 12 897
    formatted_date = check_data[2].strftime("%d.%m.%Y %H:%M")  # 15.03.2025 17:10

    caption = (
        f"🖼 *Check Data*\n"
        f"📅 Date: {formatted_date}\n"
        f"💰 Amount: {formatted_number} ₴\n"
        f"💬 Comment: {check_data[4]}"
    )
    await callback.bot.send_photo(
        callback.from_user.id,
        photo=check_data[1],
        caption=caption,
        parse_mode="Markdown",
        reply_markup=await kb.add_to_archive(check_id[0])
    )
    

@router.callback_query(F.data.startswith("arch_check"))
async def check_to_arch(callback: CallbackQuery):
    check_id = tuple(callback.data.split(":")[1:])
    print(f"check_to_arch - {check_id}")
    # select all data about check by it's id
    check_data = await db.select_check_by_id(check_id)  # warrior_id, image_url, created_at, amount, comment
    # insert to check_archive
    await db.insert_check_to_archive(check_data)
    # delete check from cash_check
    await db.delete_check_from_cash_check_by_id(check_id)

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    checks = await db.select_all_checks_for_current_user(str(callback.from_user.id))
    await callback.message.answer(
        text=f"This is all your expenses for today\n"
             f"If you have already refunded the money, simply add the old entries to the archive "
             f"by clicking the corresponding button.",
        reply_markup=await kb.all_checks_with_buttons(checks))

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
