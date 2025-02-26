from aiogram import Router, html, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb

router = Router()


# /start
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=kb.mainInline
    )


# /help
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(
        f"HELP \n{message.from_user.id} \n{message.from_user.first_name}",
        reply_markup=kb.settings
    )


# /cars
@router.message(Command('cars'))
async def get_help(message: Message):
    await message.answer(
        f"cars \n{message.from_user.id} \n{message.from_user.first_name}",
        reply_markup=await kb.reply_cars()
    )


# /city
@router.message(Command('city'))
async def get_help(message: Message):
    await message.answer(
        f"cities \n{message.from_user.id} \n{message.from_user.first_name}",
        reply_markup=await kb.inline_cities()
    )


# /who_am_i
@router.message(Command('who_am_i'))
async def get_help(message: Message):
    print(message.from_user)
    await message.reply(f"{message.from_user.id} "
                        f"\n{message.from_user.first_name}")


# How are you?
@router.message(F.text == "How are you?")
async def how_are_you(message: Message):
    await message.answer("I am ok =)")


# Photo
@router.message(F.photo)
async def how_are_you(message: Message):
    await message.answer(f"ID photo: {message.photo[-1].file_id}")


# Send photo by id or link
@router.message(Command("get_photo"))
async def get_photo(message: Message):
    # photo_id = "AgACAgIAAxkBAAMTZ6izif6ExZ6Af1K_DNilJdl5rOIAAjDoMRtYp0hJQI26-e9jJ4cBAAMCAANtAAM2BA"
    photo_id = "https://media.istockphoto.com/id/844000052/uk/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D1%96-%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F/%D0%BF%D0%BE%D0%BA%D0%B0%D0%B6%D1%87%D0%B8%D0%BA-%D0%BC%D1%96%D1%81%D1%86%D1%8F-%D0%B7%D0%B0%D0%BF%D0%BE%D0%B2%D0%BD%D0%B5%D0%BD%D0%BD%D1%8F-%D0%B7%D0%B0-%D0%B7%D0%B0%D0%BC%D0%BE%D0%B2%D1%87%D1%83%D0%B2%D0%B0%D0%BD%D0%BD%D1%8F%D0%BC-%D1%87%D0%BE%D0%BB%D0%BE%D0%B2%D1%96%D0%BA-%D1%96-%D0%B6%D1%96%D0%BD%D0%BA%D0%B0.jpg?s=612x612&w=0&k=20&c=talHWUK32xc3PoTKuaUKW4r-CrofXvSnoFw0jOlsZGQ="
    await message.answer_photo(photo=photo_id, caption='default user avatar')


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.answer("You have choose catalog")
    # await callback.answer("You have chosen catalog", show_alert=True)
    # await callback.message.answer("callback Catalog")
    # await callback.message.answer("callback Catalog")
    await callback.message.edit_text("callback Catalog", reply_markup=await kb.inline_cities())
# @router.callback_query(F.data == "cart")
# @router.callback_query(F.data == "contacts")
