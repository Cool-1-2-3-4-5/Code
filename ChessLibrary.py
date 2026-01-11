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

# Day 5:
# Worked: Made a branch for depth, now code works for check in 1, check in 3, and chck in 3 from also having 1 more move in check
# WORK NEEDED: If there is multiple checks which one is better, rn the function gives all possilbe checks, not all forced checks

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
    if depth == 0 or bot.is_checkmate():
        white_num = 0
        black_num = 0
        number_of_squares = 0
        if bot.is_checkmate():
            if BlackTurn:
                print("No Won")
                white_num = 1
                number_of_squares -=200
            else:
                print("WIN " + str(depth))
                black_num = 1
                number_of_squares +=200
        white_pieces = sum([
            len(bot.pieces(chess.PAWN, chess.WHITE)),
            3*len(bot.pieces(chess.KNIGHT, chess.WHITE)),
            3*len(bot.pieces(chess.BISHOP, chess.WHITE)),
            7*len(bot.pieces(chess.ROOK, chess.WHITE)),
            9*len(bot.pieces(chess.QUEEN, chess.WHITE)),
            90*white_num*len(bot.pieces(chess.KING, chess.WHITE))
        ])
        black_pieces = sum([
            len(bot.pieces(chess.PAWN, chess.BLACK)),
            3*len(bot.pieces(chess.KNIGHT, chess.BLACK)),
            3*len(bot.pieces(chess.BISHOP, chess.BLACK)),
            7*len(bot.pieces(chess.ROOK, chess.BLACK)),
            9*len(bot.pieces(chess.QUEEN, chess.BLACK)),
            90*black_num*len(bot.pieces(chess.KING, chess.BLACK))
        ])
        moveList = set() # number of squares occupied
        for move in bot.legal_moves:
            newstr = bot.san(move)
            iteration = -1
            if not newstr[-1].isdigit():
                iteration = iteration-1
            square = str(newstr[iteration-1]) + str(newstr[iteration])
            moveList.add(square)
        number_of_squares += len(moveList)
        valueAtPossition = black_pieces*(depth+1) - white_pieces*(depth+1) + number_of_squares
        if bot.is_checkmate():
            print("Black: " + str(black_pieces) + "White: " + str(white_pieces) + " numSquares: " + str(number_of_squares))
            print("BlackNum: " + str(black_num) + " WhiteNum: " + str(white_num))
            print("ValueAtPos" + str(valueAtPossition))
        return valueAtPossition
    elif BlackTurn: # make sure not in checkmate currently
        bestScore = -10000
        force_checkmate_cnt = 0 # Uses to iterate through number of checkmates
        for move in Possible_move:
            bot.push(move)
            newScore = minimax(bot.legal_moves, depth-1,False,False)
            if newScore > 18:
                print("NEWSCOE: " + str(newScore) + " "+ str(move))
            bestScore = max(newScore,bestScore)
            bot.pop()
            if firstcall: # INTIAL MOVE
                best_Score_List.append(bestScore)
                best_Moves_List.append(move)
                bestScore = -10000
        print("Highest = " + str(bestScore) + " " + str(depth))
        return bestScore
    elif not BlackTurn:
        bestScore = 10000
        for move in Possible_move:
            bot.push(move)
            newScore = minimax(bot.legal_moves, depth-1,True,False)
            if newScore == 1000000: #Saw checkmate in depth
                newScore = -newScore
            bestScore = min(newScore,bestScore)
            bot.pop()
            if firstcall: # INTIAL MOVE
                best_Score_List.append(move)
                best_Moves_List.append(bestScore)
                bestScore = 10000
        print("Lowest = " + str(bestScore))
        return bestScore
    else:
        #BLACK LOST CUZ NO turns left
        return 0

bot = chess.Board()
bot.push_san("f3")
# bot.push_san("e6")
# bot.push_san("g4")
print(bot)
print(bot.legal_moves)
minimax(bot.legal_moves,3,True,True)
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