import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '7224377423:AAEG4zgC1upN_XOmla-3k631BimfGhkmK-o'
ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
HANGMAN_GAME = 'Игра "Виселица"'
TIC_TAC_TOE_GAME = 'Игра "Крестики-нолики"'
PLAYER_STEP = 'X'
BOT_STEP = 'O'
bot = telebot.TeleBot(TOKEN)
data = {
    'game': None,
    'answer': None
}
def get_default_board():
    return {
    1: ' ', 2: ' ', 3: ' ',
    4: ' ', 5: ' ', 6: ' ',
    7: ' ', 8: ' ', 9: ' '
    }

def get_main_menu():
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    main_menu.add(KeyboardButton(HANGMAN_GAME))
    main_menu.add(KeyboardButton(TIC_TAC_TOE_GAME))
    return main_menu


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я умный бот с играми. Выбери игру из главного меню.",
                     reply_markup=get_main_menu())


@bot.message_handler(func=lambda message: message.text == HANGMAN_GAME)
def hangman_game(message):
    answer = choose_word()
    data['game'] = HANGMAN_GAME
    data['answer'] = answer.upper()
    data['guessed_letters'] = []
    data['letters'] = [letter for letter in ALPHABET]
    data['attempts'] = 6

    reply = '_ ' * len(answer)

    bot.send_message(message.chat.id, "Игра виселица началась.")
    bot.send_message(
        message.chat.id,
        text=reply,
        reply_markup=get_keyboard())


@bot.message_handler(func=lambda message: message.text in ALPHABET)
def hangman_game_realise(message):
    guess = message.text
    data['letters'].remove(guess)
    data['guessed_letters'].append(guess)
    if guess not in data['answer']:
        data['attempts'] -= 1
        bot.send_message(message.chat.id, text="Неверная буква")
        print_hangman(message)
        bot.send_message(message.chat.id, text=display_word(), reply_markup=get_keyboard())
        if data['attempts'] == 0:
            bot.send_message(message.chat.id, f"Game over. Ты не угадал слово '{data['answer']}'", reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, text=display_word(), reply_markup=get_keyboard())

        if all(letter in data['guessed_letters'] for letter in data['answer']):
            bot.send_message(message.chat.id, text=f"Поздравляю! Ты угадал слово '{data['answer']}'.",
                             reply_markup=get_main_menu())


def get_keyboard():
    keyboard = [KeyboardButton(letter) for letter in data['letters']]
    markup = ReplyKeyboardMarkup(input_field_placeholder='Выберите букву')
    markup.add(*keyboard, row_width=8)
    return markup





def choose_word():
    words = ["виселица", "телеграмм", "бот", "друг", "игра", "телепатия", "зал", "фильтр", "башня", "кордебалет", "обещание", "клавиатура", "леденец", "абзац", "комбинация", "развлечение", "фундамент", "ресница", "самовар", "кондитер", "банк"]  # и т.д.
    return random.choice(words)


def display_word():
    word = data['answer']
    answer = data['guessed_letters']
    display = ""
    for letter in word:
        if letter in answer:
            display += letter + " "
        else:
            display += "_ "
    return display


def print_hangman(message):
    data['hangman_pic'] = [
"""
------
|    |
|   O
|   /|\\
|   / \\
|   
|   
----------
""",
"""
------
|    |
|   O
|   /|\\
|   /
|   
|    
----------
""",
"""
------
|    |
|   O
|   /|\\
|   
|   
|     
----------
""",
"""
------
|    |
|   O
|   /|
|   
|   
|   
----------
""",
"""
------
|    |
|   O
|    |
| 
|   
|    
----------
""",
"""
------
|    |
|   O
|
|
|
|
----------
""",
"""
------
|    |
|
|
|
|
|
----------
"""
    ]
    bot.send_message(message.chat.id, text=data['hangman_pic'][data['attempts']], reply_markup=get_keyboard())

@bot.message_handler(func=lambda message: message.text == TIC_TAC_TOE_GAME)
def tic_tac_toe_game(message):
    data['board'] = get_default_board()
    # Реализация игры "Крестики-нолики"
    bot.send_message(message.chat.id, "Игра крестики-нолики началась.")

    bot.send_message(
        message.chat.id,
        text=display_board(),
        reply_markup=get_numboard()
    )




@bot.message_handler(func=lambda message: int(message.text) in range(1, 10))
def tic_tac_toe_game_realise(message):

    step = int(message.text)

    if data['board'][step] != ' ':
        bot.send_message(
            message.chat.id,
            text='Эта клетка уже занята.'
        )
        return

    data['board'][step] = PLAYER_STEP
    print_board_to_chat(message)
    if check_win(data['board'], PLAYER_STEP):
        bot.send_message(
            message.chat.id,
            text='Вы выиграли! Поздравляю!',
            reply_markup=get_main_menu()
        )
        return

    if ' ' not in data['board'].values():
        bot.send_message(
            message.chat.id,
            text='Ничья!',
            reply_markup=get_main_menu()
        )
        return

    data['board'][bot_move(data['board'])] = BOT_STEP
    print_board_to_chat(message)
    if check_win(data['board'], BOT_STEP):
        bot.send_message(
            message.chat.id,
            text='Бот выиграл!',
            reply_markup=get_main_menu()
        )

def print_board_to_chat(message):
    bot.send_message(
        message.chat.id,
        text=display_board()
    )


def get_numboard():
    keyboard = [KeyboardButton(num) for num in range(1, 10)]
    markup = ReplyKeyboardMarkup(input_field_placeholder='Выберите цифру')
    markup.add(*keyboard, row_width=3)
    return markup

def display_board():
    board = data['board']
    return f'''
{board[1]} | {board[2]} | {board[3]}
---------
{board[4]} | {board[5]} | {board[6]}
---------
{board[7]} | {board[8]} | {board[9]}
'''

def check_win(board, player):
    win_combinations = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],
        [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [3, 5, 7]
    ]
    for combo in win_combinations:
        if all(board[pos] == player for pos in combo):
            return True
    return False

def bot_move(board):
    available_moves = [pos for pos, value in board.items() if value == ' ']
    return random.choice(available_moves)
bot.polling()