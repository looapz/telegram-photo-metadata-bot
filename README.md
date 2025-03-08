# Telegram Бот для Анализа Метаданных Фотографий

Этот бот анализирует метаданные фотографий, отправленных пользователем в Telegram. Он извлекает информацию о формате, размере, режиме и EXIF данных (если они доступны).

## Возможности

- Анализ метаданных фотографий (размер, формат, режим)
- Извлечение EXIF данных (если доступны)
- Поддержка сжатых и несжатых фотографий
- Поддержка пересылаемых сообщений с фотографиями

## Требования

- Python 3.7+
- Библиотеки из файла requirements.txt
- Токен Telegram бота (получается через @BotFather)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/looapz/telegram-photo-metadata-bot.git
cd telegram-photo-metadata-bot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте бота в Telegram через [@BotFather](https://t.me/BotFather) и получите токен

4. Настройте переменную окружения с токеном бота:

**Linux/macOS:**
```bash
export TELEGRAM_BOT_TOKEN="ваш_токен_бота"
```

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN="ваш_токен_бота"
```

**Windows (CMD):**
```cmd
set TELEGRAM_BOT_TOKEN=ваш_токен_бота
```

## Запуск

```bash
python bot.py
```

## Использование

1. Запустите бота командой `/start`
2. Отправьте боту фотографию
3. Бот ответит сообщением с метаданными фотографии

## Постоянный запуск на сервере

Для запуска бота на сервере в фоновом режиме можно использовать различные методы:

### Использование systemd (Linux)

1. Создайте файл службы `/etc/systemd/system/telegram-photo-bot.service`:

```ini
[Unit]
Description=Telegram Photo Metadata Bot
After=network.target

[Service]
User=ваш_пользователь
WorkingDirectory=/путь/к/боту
Environment="TELEGRAM_BOT_TOKEN=ваш_токен_бота"
ExecStart=/путь/к/python /путь/к/боту/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Включите и запустите службу:

```bash
sudo systemctl enable telegram-photo-bot
sudo systemctl start telegram-photo-bot
```

### Использование Docker

1. Создайте Dockerfile в корне проекта:

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

2. Соберите и запустите Docker-контейнер:

```bash
docker build -t telegram-photo-bot .
docker run -d --name photo-bot -e TELEGRAM_BOT_TOKEN=ваш_токен_бота telegram-photo-bot
```

## Лицензия

MIT