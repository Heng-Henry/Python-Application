from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CommandHandler, CallbackQueryHandler
from password import token
from random import choice

black = '⚫️'
white = '⚪️'
BOARD_SIZE = 8


board = create_board()
turn = black
game_over = False


def get_flipped(row, col, color):
    global board, black, white
    flip = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    if color == black:
        other_color = white
    else:
        other_color = black
    for dx, dy in directions:
        flipped = []
        x, y = row + dx, col + dy

        # 在該方向上找到對手的棋子
        while is_valid_position(x, y) and board[x][y] == other_color:
            flipped.append((x, y))
            x += dx
            y += dy

            # 如果找到自己的棋子，則將之前找到的對手棋子加入要翻轉的列表中
            if is_valid_position(x, y) and board[x][y] == color:
                flip.extend(flipped)
                break

    return flip

def is_valid_move(row, column, color):
    global board, black, white
    tile_flip = []
    # 檢查該位置是否在棋盤範圍內且為空位置
    if not is_valid_position(row, column) or (board[row][column] == black or board[row][column] == white):
        return False

    ###
    if color == black:
        other_color = white
    else:
        other_color = black


    # 檢查該位置周圍是否有相鄰的對手棋子
    for dx, dy in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x = row
            y = column
            x += dx
            y += dy
            if is_valid_position(x, y) and (board[x][y] == other_color):
                x += dx
                y += dy
                if not is_valid_position(x, y):
                    continue
                while board[x][y] == other_color:
                    x += dx
                    y += dy
                    if not is_valid_position(x,y):
                        break
                if not is_valid_position(x, y):
                    continue
                if board[x][y] == color:
                    while True:
                        x -= dx
                        y -= dy
                        if x == row and y == column:
                            break
                        tile_flip.append([x, y])
    board[row][column] = " "
    return tile_flip


def is_valid_position(row, column):
    global board
    num_rows = len(board)
    num_columns = len(board[0])
    return 0 <= row < num_rows and 0 <= column < num_columns

def get_valid_moves(color):
    global board
    valid_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(row, col, color) :
                valid_moves.append((row, col))
    if len(valid_moves) > 0:
        return valid_moves
    else :
        return None

def count_flips(row, column, color):
    global board

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    flips = 0

    for direction in directions:
        r, c = row, column
        r += direction[0]
        c += direction[1]

        if not is_valid_move(r, c, color):
            continue

        while board[r][c] != color:
            flips += 1
            r += direction[0]
            c += direction[1]

            if not is_valid_move(r, c, color):
                break

    return flips


def get_computer_move():
    color = white
    global board
    valid_moves = get_valid_moves(color)
    if not valid_moves:
        return None
    best_move = None
    max_flips = -1

    for move in valid_moves:
        flips = count_flips(move[0], move[1], color)
        if flips > max_flips:
            max_flips = flips
            best_move = move

    return best_move[0], best_move[1]
def create_board():

    board = [[f'{row},{col}'for col in range(BOARD_SIZE)]for row in range(BOARD_SIZE)]

    return board



def enc(board):
    # board is a dictionary mapping (row, col) to grid
    # grid = [[board.get((row, col), '') for col in range(8)] for row in range(8)]
    number = 0
    base = 3
    for row in range(8):
        for col in range(8):
            number *= base
            # if grid[row][col] == black:
            if board[row][col] == black:
                number += 2
            # elif grid[row][col] == white:
            elif board[row][col] == white:
                number += 1
    return str(number)


def dec(number):
    global board
    base = 3
    for row in [7, 6, 5, 4, 3, 2, 1, 0]:
        for col in [7, 6, 5, 4, 3, 2, 1, 0]:
            if number % 3 == 2:
                board[row][col] = black
            elif number % 3 == 1:
                board[row][col] = white
            number //= base
    return board


def board_markup(board):
    # board will be encoded and embedded to callback_data
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(board[row][col], callback_data=f'{row}{col}') for col in range(8)]
        for row in range(8)])


# Define a few command handlers. These usually take the two arguments update and
# context.
async def func(update, context):
    global turn, board, game_over
    if game_over or turn == white:
        return



    data = update.callback_query.data
    # user clicked the button on row int(data[0]) and col int(data[1])
    row = int(data[0])
    col = int(data[1])
    #await context.bot.answer_callback_query(update.callback_query.id, f'你按的 row {row} col {col}')
    # TODO: check if the button is clickable. if not, report it is not clickable and return
    game_end = 0

    turn = white
     # 我方無法有效落子 直接換電腦下
    if get_valid_moves(black) == None:
        await context.bot.answer_callback_query(update.callback_query.id, f'沒辦法有效落子，換對方下')
        game_end += 1

        # 沒辦法下 換電腦
        pass
    # 下的地方不合法 重下
    elif is_valid_move(row, col, black):
        #tile_flip = is_valid_move(row, col, black)
        ## 下棋
        board[row][col] = black
        ## 找應該要被翻轉的棋並且將其翻轉
        flip = get_flipped(row, col, black)
        for x, y in flip:
            board[x][y] = black
    else:
        await context.bot.answer_callback_query(update.callback_query.id, f'這邊不能下 請重新下棋')
        turn = black
        return


    # the board is encoded and stored as data[2:]
    #board = dec(int(data[2:]))


    # computer

    await context.bot.edit_message_text('等待對方下棋',
                                        reply_markup=board_markup(board),
                                        chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id)
    #rand_row, rand_col = choice([(r, c) for r in range(8) for c in range(8) if board[r][c] not in (black, white)])
    #board[rand_row][rand_col] = white
    if get_computer_move() != None and turn == white:
        r, c = get_computer_move()
        #
        board[r][c] = white
        ##
        flip = get_flipped(r, c, white)
        for x, y in flip:
            board[x][y] = white
        # 電腦不能下棋 直接換玩家下
    elif get_computer_move() == None:
        game_end += 1

    ##
    if game_end == 2:
        game_over = True
        #print("遊戲結束")
        await context.bot.answer_callback_query(update.callback_query.id, f'遊戲結束')
        player_count = 0
        ai_count = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == black:
                    player_count += 1
                elif board[x][y] == white:
                    ai_count += 1
        ###

        if player_count > ai_count:
            await context.bot.answer_callback_query(update.callback_query.id, f'玩家獲勝')
            end = '玩家獲勝'
        elif player_count < ai_count:
            await context.bot.answer_callback_query(update.callback_query.id, f'對手獲勝')
            end = '對手獲勝'
        else:
            await context.bot.answer_callback_query(update.callback_query.id, f'平局')
            end = '平局'
    else:
        end = '目前盤面'



    await context.bot.edit_message_text( end,
                                        reply_markup=board_markup(board),
                                        chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id)
    turn = black
async def start(update, context):
    global board, turn, game_over, black, white
    board = create_board()
    turn = black
    game_over = False

    #
    board[3][3] = black
    board[3][4] = white
    board[4][3] = white
    board[4][4] = black
    # reply_markup = board_markup(board)
    await update.message.reply_text('目前盤面', reply_markup=board_markup(board))



def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("game_start", start))
    application.add_handler(CommandHandler("restart", start))
    application.add_handler(CallbackQueryHandler(func))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()