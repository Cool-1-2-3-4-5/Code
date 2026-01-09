import chess

# DAY 1:
# fix the static counter

# DAY 3:
# FIXED: the static counter
# WORK NEEDED: add ability to identify check, and checkmate

# Day 4:
# Worked on adding checkmate, worked for 1 case but not for 3rd and then recoded and flipped
# ADDED: sort for best move
# WORK NEEDED: checkmate finder

bot = chess.Board()
file_path = "output.txt"
best_Score_List = []
best_Moves_List = []
cnt = [0]
increment = 0

def BestMove(list1,list2):
    combined = list(zip(list1,list2))
    combined.sort(key =lambda x: x[0])
    list1,list2 = zip(*combined)
    list1,list2 = list(list1),list(list2)
    return list2[-1]

def reset():
    cnt[0] = 0
    best_Score_List.clear()
    best_Moves_List.clear()


def minimax(Possible_move,depth,BlackTurn, firstcall = True): #Lets say black is chess bot
    if depth == 0:
        white_pieces = sum([
            len(bot.pieces(chess.PAWN, chess.WHITE)),
            3*len(bot.pieces(chess.KNIGHT, chess.WHITE)),
            3*len(bot.pieces(chess.BISHOP, chess.WHITE)),
            7*len(bot.pieces(chess.ROOK, chess.WHITE)),
            9*len(bot.pieces(chess.QUEEN, chess.WHITE)),
            len(bot.pieces(chess.KING, chess.WHITE))
        ])
        black_pieces = sum([
            len(bot.pieces(chess.PAWN, chess.BLACK)),
            3*len(bot.pieces(chess.KNIGHT, chess.BLACK)),
            3*len(bot.pieces(chess.BISHOP, chess.BLACK)),
            7*len(bot.pieces(chess.ROOK, chess.BLACK)),
            9*len(bot.pieces(chess.QUEEN, chess.BLACK)),
            len(bot.pieces(chess.KING, chess.BLACK))
        ])
        moveList = set() # number of squares occupied
        for move in bot.legal_moves:
            newstr = bot.san(move)
            iteration = -1
            if not newstr[-1].isdigit():
                iteration = iteration-1
            square = str(newstr[iteration-1]) + str(newstr[iteration])
            moveList.add(square)
        number_of_squares = len(moveList)
        valueAtPossition = black_pieces - white_pieces + number_of_squares
        return valueAtPossition
    elif BlackTurn: # make sure not in checkmate currently
        bestScore = -10000
        # print("now")
        # print(bot.legal_moves)
        # print(cnt[0])
        for move in Possible_move:
            # print("MOVE")
            # print(move)
            bot.push(move)
            if (len(list(bot.legal_moves))) == 0: # if check
                bestScore = 1000000
                bot.pop()
                print("Move: " + str(move) + " is Checkmate")
                print(bot)
                break
            # print(bot)
            else:
                newScore = minimax(bot.legal_moves, depth-1,False,False)
                if newScore == -1000000: #Saw checkmate in depth
                    newScore = -newScore
                bestScore = max(newScore,bestScore)
            bot.pop()
            # print("done" + str(bestScore))
            # print(bot)
            if firstcall: # INTIAL MOVE
                bestScore = -10000
                best_Score_List.append(bestScore)
                best_Moves_List.append(move)
        return bestScore
    elif not BlackTurn:
        bestScore = 10000
        for move in Possible_move:
            # print("MOVENotBlack")
            # print(move)
            bot.push(move)
            if (len(list(bot.legal_moves))) == 0: # if checkmate
                bestScore = -1000000
                bot.pop()
                print("Move2: " + str(move) + " is Checkmate")
                break
            # print(bot)
            # bot.push(move)
            else:
                newScore = minimax(bot.legal_moves, depth-1,True,False)
                if newScore == 1000000: #Saw checkmate in depth
                    newScore = -newScore
                bestScore = min(newScore,bestScore)
            # print("doneNotBlack" + str(bestScore))
            # print(bot)
            bot.pop()
            if firstcall: # INTIAL MOVE
                best_Score_List.append(move)
                best_Moves_List.append(bestScore)
        return bestScore
    else:
        #BLACK LOST CUZ NO turns left
        return 0

# print(bot.legal_moves)
# bot.push_san("Nf3")
# print(moveList)
# minimax(bot.legal_moves,3,True)
# print(best_Score_List)
# print(best_Moves_List)
# [Move.from_uci('a8b8'), Move.from_uci('a8a7'), Move.from_uci('a8a6'), Move.from_uci('a8a5'), Move.from_uci('a8a4'), Move.from_uci('a8a3'), Move.from_uci('a8a2'), Move.from_uci('d7e8'), Move.from_uci('d7d8'), Move.from_uci('d7e6'), Move.from_uci('d7d6'), Move.from_uci('d7c6'), Move.from_uci('f6g8'), Move.from_uci('f6e8'), Move.from_uci('f6h5'), Move.from_uci('f6d5'), Move.from_uci('f6g4'), Move.from_uci('f6e4'), Move.from_uci('h7h6'), Move.from_uci('g7g6'), Move.from_uci('e7e6'), Move.from_uci('c7c6'), Move.from_uci('b7b6'), Move.from_uci('h7h5'), Move.from_uci('g7g5'), Move.from_uci('e7e5'), Move.from_uci('c7c5'), Move.from_uci('b7b5')]
# [-19, -19, -19, -19, -19, -19, -18, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19]
bot.push_san("f3")      # White
bot.push_san("e5")      # Black
bot.push_san("g4")      # White
# bot.push_san("Qh4#")    # Black - CHECKMATE!
# <LegalMoveGenerator at 0x1b9c0f02dd0 (Ne7, Nh6, Nf6, Be7, Bd6, Bc5, Bb4, Ba3, Ke7, Qe7, Qf6, Qg5, Qh4#, Nc6, Na6, h6, g6, f6, d6, c6, b6, a6, e4, h5, g5, f5, d5, c5, b5, a5)>
print(bot)
minimax(bot.legal_moves,1,True,True)
print(bot.legal_moves)
print(best_Score_List)
print(best_Moves_List)

# while not bot.is_checkmate():
#     print(bot)
#     myMove = input("ENTER Move: ")
#     bot.push_san(str(myMove))
#     print(bot)
#     print(bot.legal_moves)
#     minimax(bot.legal_moves,1,True,True)
#     print(best_Score_List)
#     print(best_Moves_List)
#     print("BestMove")
#     NextMove = BestMove(best_Score_List,best_Moves_List)
#     print(NextMove)
#     bot.push_uci(str(NextMove))
#     reset()

print("GAME Over")
# print(f"White in check: {bot.is_check()}")
# print(f"Checkmate: {bot.is_checkmate()}")

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