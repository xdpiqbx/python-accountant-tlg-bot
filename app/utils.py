from datetime import datetime
from aiogram.types import CallbackQuery

def reformat_datetime_from_db(dt):
    # Original datetime string
    # dt = "2025-03-14 13:09:59.498756"
    # Parse the string into a datetime object
    dt_obj = datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S.%f")
    # Format the datetime object into the desired format
    # return dt_obj.strftime("%d.%m.%Y %H:%M")
    return dt_obj.strftime("%d.%m.%Y")

def hryvna_format(amount):
    return f"{int(amount):,}{chr(0x2009)}{chr(0x20B4)}".replace(',', chr(0x2009))

async def remove_prev_inline_keyboard(callback: CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
