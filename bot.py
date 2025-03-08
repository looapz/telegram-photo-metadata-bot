import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from PIL import Image, ExifTags
import io
import logging

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_photo_metadata(photo: types.PhotoSize, file_id: str) -> str:
    """Получение метаданных фотографии"""
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    # Скачиваем файл
    downloaded_file = await bot.download_file(file_path)
    image = Image.open(io.BytesIO(downloaded_file.read()))
    
    # Собираем метаданные
    metadata = {
        "Формат": image.format,
        "Размер": f"{image.width}x{image.height}",
        "Режим": image.mode,
        "File ID": file_id,
        "Размер файла": f"{file.file_size} байт"
    }
    
    # Получаем EXIF данные, если они есть
    exif = image.getexif()
    if exif:
        # Добавляем основные EXIF данные
        exif_data = {}
        for tag_id in exif:
            tag = exif.get(tag_id)
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            exif_data[tag_name] = tag
        metadata["EXIF"] = exif_data

    # Формируем текст ответа
    result = "📸 Метаданные фотографии:\n\n"
    for key, value in metadata.items():
        if key != "EXIF":
            result += f"• {key}: {value}\n"
    
    if "EXIF" in metadata:
        result += "\n📑 EXIF данные:\n"
        for key, value in metadata["EXIF"].items():
            result += f"• {key}: {value}\n"
    
    return result

@dp.message(F.photo)
async def handle_photo(message: Message):
    """Обработчик для фотографий"""
    # Получаем самую большую версию фото
    photo = message.photo[-1]
    try:
        metadata = await get_photo_metadata(photo, photo.file_id)
        await message.reply(metadata)
    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке фото: {str(e)}")

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer("👋 Привет! Отправь мне фотографию, и я покажу её метаданные.")

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())