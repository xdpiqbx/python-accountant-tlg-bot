from aiogram import Router, html, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
# from app.middlewares import TestMiddleware

from env_variables import EXPERT
from app.accountant_db import is_warrior_exists, insert_new_warrior

router = Router()

# router.message.middleware(TestMiddleware())
# router.message.outer_middleware(TestMiddleware())


class Register(StatesGroup):
    nic = State()
    tlg_id = State()


class CashCheck(StatesGroup):
    image_url = State()
    amount = State()

# /start
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if not await is_warrior_exists(str(message.from_user.id)):
        await message.answer("REGISTRATION needed! Wait for approve.")
        await state.set_state(Register.nic)
        await message.answer("Send me your call sign (in english):")
    else:
        await message.answer("Hello")

@router.message(Register.nic)
async def register(message: Message, state: FSMContext):
    tlg_id = message.from_user.id
    nic = message.text
    await state.update_data(tlg_id=tlg_id, nic=nic)
    await message.forward(chat_id=EXPERT)
    await message.answer(
        f"We have a new warrior:\nCall sign: {nic}\n Telegram id: {tlg_id}",
        reply_markup=kb.add_new_warrior)

@router.callback_query(F.data == "add_new_warrior_to_db")
async def add_new_warrior_to_db(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    insert_new_warrior((data["tlg_id"], data["nic"]))
    await callback.bot.send_message(
        chat_id=EXPERT,
        text=f"Name: {data['tlg_id']} Number: {data['nic']}. Registration done!")
    await callback.bot.send_message(
        chat_id=data["tlg_id"],
        text=f"{data['nic']} registration done!")
    await state.clear()


@router.callback_query(F.data == "cancel_new_warrior")
async def cancel_new(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.bot.send_message(
        chat_id=EXPERT,
        text=f"Has been canceled\n Name: {data['tlg_id']} Number: {data['nic']}.")
    await callback.bot.send_message(
        chat_id=data["tlg_id"],
        text=f"I do not know you/")
    await state.clear()


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
