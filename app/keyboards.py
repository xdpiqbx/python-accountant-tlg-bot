from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Reply big buttons
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Catalog")],
    [KeyboardButton(text="Cart"), KeyboardButton(text="Contacts")]
], resize_keyboard=True, input_field_placeholder="Choose menu bottom...")

# Inline buttons
mainInline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Catalog", callback_data="catalog")],
    [
        InlineKeyboardButton(text="Cart", callback_data="cart"),
        InlineKeyboardButton(text="Contacts", callback_data="contacts")
    ]
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="YouTube", url="https://youtube.com")],
    [InlineKeyboardButton(text="Google", url="http://google.com")],
])


async def reply_cars():
    cars = ["Tesla", "Mercedes", "Mitsubishi"]
    keyboard = ReplyKeyboardBuilder()
    for car in cars:
        keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(2).as_markup()


async def inline_cities():
    cities = ["Kyiv", "Brisbane", "Portland"]
    keyboard = InlineKeyboardBuilder()
    for city in cities:
        keyboard.add(InlineKeyboardButton(text=city, url="https://youtube.com"))
    return keyboard.adjust(2).as_markup()
