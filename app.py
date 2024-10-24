import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from random import choice


BOT_TOKEN = '7766810555:AAF4amktj49A0HDSVDUMVPd-1vxFpOjnb_g'
GAME_CHOICES = {'Камень 👊', 'Ножницы ✌️', 'Бумага ✋'}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


keyboard_answer: list[list[KeyboardButton]] = [KeyboardButton(text='Давай!'), KeyboardButton(text='Нихачу(')]

keyboard_game: list[list[KeyboardButton]] =[KeyboardButton(text='Камень 👊'), KeyboardButton(text='Ножницы ✌️'), KeyboardButton(text='Бумага ✋')]


builder1 = ReplyKeyboardBuilder()

builder1.row(*keyboard_answer, width=3)

builder2 = ReplyKeyboardBuilder()
builder2.row(*keyboard_game, width=3)


def game_logic(choice_bot, choice_player):
    if choice_bot == choice_player:
        return None
    elif choice_bot == 'Бумага ✋':
        if choice_player == 'Камень 👊':
            return False
        elif choice_player == 'Ножницы ✌️':
            return True
    elif choice_bot == 'Ножницы ✌️':
        if choice_player == 'Камень 👊':
            return True
        elif choice_player == 'Бумага ✋':
            return False


@dp.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(
        'Привет, хочешь сыграть в игру камень-ножницы бумага?',
        reply_markup=builder1.as_markup(resize_keyboard=True))


@dp.message(Command(commands=['help']))
async def process_command_help(message: Message):
    await message.answer(
        text='Победитель определяется по следующим правилам: '
                'Бумага побеждает камень («бумага обёртывает камень»). '
                'Камень побеждает ножницы («камень затупляет ножницы»). '
                'Ножницы побеждают бумагу («ножницы разрезают бумагу»).\n'
                'Хочешь сыграть со мной в игру?',
        reply_markup=builder1.as_markup(resize_keyboart=True),
    )


@dp.message(F.text == 'Давай!')
async def process_command_game(message: Message):
    await message.answer(
        text='Выбирай!',
        reply_markup=builder2.as_markup(resize_keyboard=True)
    )


@dp.message(F.text.in_(GAME_CHOICES))
async def process_command_choice(message: Message):
    choice_bot = choice(list(GAME_CHOICES))
    check_result = game_logic(choice_bot, message.text)
    if check_result is None:
        await message.answer(
            text='Ура! У нас получилась ничья! '
            'Давай попробуем ещё раз!',
            reply_markup=builder2.as_markup(resize_keyboard=True))
    if check_result:
        await message.answer(
            text='Вау! Ты выиграл! '
            'Ну ничего! У меня получится в другой раз '
            'Хочешь сыграть ещё раз?',
            reply_markup=builder1.as_markup(resize_keyboard=True))
    else:
        await message.answer(
            text=f'Похоже, ты проиграл :( '
            f'Я выбрал {choice_bot}\n'
            f'Давай сыграем ещё разок?',
            reply_markup=builder1.as_markup(resize_keyboard=True))


@dp.message(F.text == 'Нихачу(')
async def process_command_diss(message: Message):
    await message.answer(
        text='Ладно :(\nМожет захочешь попозже',
        reply_markup=builder1.as_markup(resize_keyboard=True)
    )


@dp.message()
async def process_command_diss(message: Message):
    await message.answer(
        text='К сожалению я тебя не понял ( '
        'Давай сыграем?',
        reply_markup=builder1.as_markup(resize_keyboard=True)
    )


if __name__ == '__main__':
    dp.run_polling(bot)