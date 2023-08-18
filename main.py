import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from config_reader import config
from aiogram.filters import CommandObject
import requests


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher() 


@dp.message(Command("start"))
async def start(message: types.Message, bot:Bot):
    await message.reply(f"👋Привет, <b>{message.from_user.first_name}</b>!\n\n⚠️Для информации используйте команду <b>/info</b>.", parse_mode=ParseMode.HTML)

@dp.message(Command("info"))
async def info(message: types.Message):
    await message.reply("📰Информация о боте\n\nОбратная связь: Недоступно.\nGithub репозиторий: https://github.com/Leqort/traininghelp er_robot\n©️Все права защищены.", parse_mode=ParseMode.HTML)

@dp.message(Command("user"))
async def user(message: types.Message, command: CommandObject):
    if command.args:
        response = requests.get(f"https://training-server.com/api/user/{command.args}")
        res_json = response.json()
        res_data = res_json["data"]
        id = res_data["id"]
        login = res_data["login"]
        moder = res_data["moder"]
        reg_date = res_data["regdate"]
        last_login = res_data["lastlogin"]
        if moder == 0:
            moder = "Нет"
        else:
            moder = "Да"
        online = res_data["online"]
        if online == 0:
            online = "Да"
        else:
            online = "Нет"        
        await message.reply(f"🐸Информация о игроке: {login}\n\n🤖ID: <i>{id}</i>\n👨‍🦲Модератор: <i>{moder}</i>\n💻Онлайн: <i>{online}</i>\n\n🎮Зарегистрировался в: <i>{reg_date}</i>\n⌨️Последний раз заходил в: <i>{last_login}</i>", parse_mode=ParseMode.HTML)
    else:
        await message.reply("❌Вы не указали ник-нейм <b>игрока</b>!")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())