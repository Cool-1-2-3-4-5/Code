import chess
# from nicegui import ui


# DAY 1:
# fix the static counter

bot = chess.Board()
file_path = "output.txt"
best_Score_List = []
best_Moves_List = []
cnt = [0]
def minimax(Possible_move,depth,BlackTurn): #Lets say black is chess bot
    cnt[0] +=1
    if depth == 0:
        white_pieces = sum([
            len(bot.pieces(chess.PAWN, chess.WHITE)),
            len(bot.pieces(chess.KNIGHT, chess.WHITE)),
            len(bot.pieces(chess.BISHOP, chess.WHITE)),
            len(bot.pieces(chess.ROOK, chess.WHITE)),
            len(bot.pieces(chess.QUEEN, chess.WHITE)),
            len(bot.pieces(chess.KING, chess.WHITE))
        ])

        black_pieces = sum([
            len(bot.pieces(chess.PAWN, chess.BLACK)),
            len(bot.pieces(chess.KNIGHT, chess.BLACK)),
            len(bot.pieces(chess.BISHOP, chess.BLACK)),
            len(bot.pieces(chess.ROOK, chess.BLACK)),
            len(bot.pieces(chess.QUEEN, chess.BLACK)),
            len(bot.pieces(chess.KING, chess.BLACK))
        ])
        valueAtPossition = black_pieces - white_pieces
        return valueAtPossition
    if BlackTurn:
        intial = -10000
        print("now")
        print(bot.legal_moves)
        print(cnt[0])
        for move in Possible_move:
            print("right")
            print(move)
            bot.push(move)
            newScore = minimax(bot.legal_moves, depth-1,False)
            bestScore = max(newScore,intial)
            bot.pop()
            print("Happening")
            print(cnt[0])
            if cnt[0] == 1: # INTIAL MOVE
                best_Score_List.append(move)
                best_Moves_List.append(bestScore)
        return bestScore
    if not BlackTurn:
        intial = 10000
        for move in Possible_move:
            bot.push(move)
            newScore = minimax(bot.legal_moves, depth-1,True)
            bestScore = max(newScore,intial)
            bot.pop()
        return bestScore
    else:
        #BLACK LOST CUZ NO turns left
        return 0

print(bot.legal_moves)
bot.push_san("Nf3")
print(bot)
minimax(bot.legal_moves,1,True)
print(best_Score_List)
print(best_Moves_List)
# File write happens after every move:
# with open(file_path, 'w') as file:
#     file.write(str(bot))
# hashmap = {
#     "r":"♜",
#     "n":"♞",
#     "b":"♝",
#     "q":"♛",
#     "k":"♚",
#     "p":"♟",
#     "R":"♖",
#     "N":"♘",
#     "B":"♗",
#     "Q":"♕",
#     "K":"♔",
#     "P":"♙",
#     ".":""
# }
# print(bot)
# status = []
# with open(file_path,'r') as file:
#     for line in file:
#         print(line.strip())
#         status.append(line.strip())
# print(status)
# for row in status:
#     row = row.split(" ")
#     with ui.row():
#         for col in row:
#             print(hashmap[col])
#             ui.label(hashmap[col])
#     print(row)
# ui.run()