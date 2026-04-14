import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile

BOT_TOKEN = "8544927235:AAFS6EKwdDF2hBn-ayxzq3-3j_MVBqFkGak"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище: user_id -> путь к файлу
user_files = {}

@dp.message(F.document)
async def get_file(message: Message):
    file = message.document
    file_id = file.file_id
    
    # Скачиваем файл
    file_info = await bot.get_file(file_id)
    file_path = f"downloads/{file_id}_{file.file_name}"
    
    os.makedirs("downloads", exist_ok=True)
    await bot.download_file(file_info.file_path, file_path)
    
    user_files[message.from_user.id] = file_path
    await message.answer("✅ Файл получен! Теперь напиши новое название с расширением.\n\nПример: document.pdf")

@dp.message(F.text)
async def rename_file(message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_files:
        await message.answer("⚠️ Сначала отправь файл!")
        return
    
    new_name = message.text.strip()
    old_path = user_files[user_id]
    new_path = f"downloads/{new_name}"
    
    # Переименовываем
    os.rename(old_path, new_path)
    
    # Отправляем обратно
    file = FSInputFile(new_path, filename=new_name)
    await message.answer_document(file, caption=f"✅ Файл переименован: {new_name}")
    
    # Удаляем локально
    os.remove(new_path)
    del user_files[user_id]

async def main():
    await dp.start_polling(bot)

asyncio.run(main())