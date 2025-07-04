import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

# --- КОНФІГУРАЦІЯ ---
TOKEN = os.getenv("TOKEN", "7546219321:AAEyiWUNii7cl-vxvCSh7pSj0fGhSzXoyQ4")  # Для локального запуску

# --- ІНІЦІАЛІЗАЦІЯ ---
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# --- КЛАВІАТУРИ ---
main_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="🗺️ З чого почати? Покроковий план", callback_data="step_by_step_plan")],
    [types.InlineKeyboardButton(text="🏗️ Структура курсової роботи", callback_data="structure")],
    [types.InlineKeyboardButton(text="✍️ Правила оформлення (ДСТУ)", callback_data="formatting_rules")],
    [types.InlineKeyboardButton(text="📚 Де шукати джерела?", callback_data="sources")],
    [types.InlineKeyboardButton(text="🔥 Отримати особисту консультацію", callback_data="personal_consultation")],
])
back_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="◀️ Назад до головного меню", callback_data="back_to_main_menu")]
])

# --- ХЕНДЛЕРИ ---

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    welcome_message = (
        f"Привіт, {hbold(message.from_user.full_name)}!\n\n"
        "Я ваш особистий помічник у написанні курсових робіт. 🧭\n\n"
        "Чим я можу вам допомогти? Оберіть один з пунктів нижче:"
    )
    await message.answer(welcome_message, reply_markup=main_menu_keyboard)

@dp.callback_query(F.data == "back_to_main_menu")
async def process_back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Чим ще я можу вам допомогти? Оберіть один з пунктів нижче:",
        reply_markup=main_menu_keyboard
    )
    await callback.answer()

@dp.callback_query(F.data == "step_by_step_plan")
async def process_step_by_step_plan(callback: CallbackQuery):
    text = (
        f"{hbold('🗺️ Покроковий план написання курсової:')}\n\n"
        "1. Вибір теми.\n2. План.\n3. Джерела.\n4. Теорія.\n5. Практика.\n6. Вступ і висновки.\n7. Оформлення.\n8. Плагіат.\n9. Здача."
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard)
    await callback.answer()

@dp.callback_query(F.data == "structure")
async def process_structure(callback: CallbackQuery):
    text = (
        f"{hbold('🏗️ Типова структура курсової роботи:')}\n\n"
        f"🔹 {hbold('Титульна сторінка')}\n🔹 {hbold('Зміст')}\n🔹 {hbold('Вступ')}\n🔹 {hbold('Розділ 1')}\n"
        f"🔹 {hbold('Розділ 2')}\n🔹 {hbold('Висновки')}\n🔹 {hbold('Список джерел')}\n🔹 {hbold('Додатки')}"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard)
    await callback.answer()

@dp.callback_query(F.data == "formatting_rules")
async def process_formatting(callback: CallbackQuery):
    text = (
        f"{hbold('✍️ Основні правила оформлення (ДСТУ):')}\n\n"
        f"▪️ {hbold('Шрифт:')} Times New Roman, 14\n"
        f"▪️ {hbold('Інтервал:')} 1.5\n"
        f"▪️ {hbold('Поля:')} ліве – 30 мм, праве – 10 мм\n"
        f"▪️ {hbold('Нумерація:')} у верхньому куті\n"
        f"▪️ {hbold('Заголовки:')} великі літери по центру"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard)
    await callback.answer()

@dp.callback_query(F.data == "sources")
async def process_sources(callback: CallbackQuery):
    text = (
        f"{hbold('📚 Де шукати джерела:')}\n\n"
        f"🔗 {hbold('Google Scholar')} — scholar.google.com\n"
        f"🔗 {hbold('Academia.edu')} — наукові роботи\n"
        f"🔗 {hbold('НБУ ім. Вернадського')} — nbuv.gov.ua\n"
        f"🔗 {hbold('Університетські бібліотеки')} — бази даних"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard, disable_web_page_preview=True)
    await callback.answer()

@dp.callback_query(F.data == "personal_consultation")
async def process_personal_consultation(callback: CallbackQuery):
    YOUR_USERNAME = "@yurij2000"
    text = (
        f"{hbold('🔥 Потрібна особиста допомога?')}\n\n"
        "Якщо автоматичних порад недостатньо, напишіть мені напряму:\n\n"
        f"📞 {hbold('Мій контакт:')} {YOUR_USERNAME}\n\n"
        "Обговоримо деталі у приваті."
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard)
    await callback.answer(text="Переходьте до особистих повідомлень!", show_alert=True)

# --- ЗАПУСК ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинено.")
