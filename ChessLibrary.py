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

# Day 6:
# DOne: Minimax
# WORK NEEDED: Pruning

# Day 7:
# Done: Pruning and Minimax
# Works up to depth of 5 or 35000+ nodes
# Work on Open CV

bot = chess.Board()
file_path = "output.txt"
best_Score_List = []
best_Moves_List = []
cnt = [0]
increment = 0

# def BestMove(list1,list2):
#     combined = list(zip(list1,list2))
#     combined.sort(key =lambda x: x[0])
#     list1,list2 = zip(*combined)
#     list1,list2 = list(list1),list(list2)
#     return list2[-1]

# def reset():
#     cnt[0] = 0
#     best_Score_List.clear()
#     best_Moves_List.clear()

def InterpetMove(move,moveInSan):
    if move == "O-O-O":
        # Move servos to perform queenside castle
        pass
    elif move == "O-O":
        pass
        # Move servos to perform kingside cas tle
    elif "x" in moveInSan:
        pass
        # Move servos to remove piece at Point A first and then move piece to Point B
    else:
        pass
        # Move servos to pick up piece from point A and place in point B


def minimax(Possible_move,depth,BlackTurn, alpha,beta,firstcall = True): #Lets say black is chess bot
    if depth == 0 or bot.is_checkmate():
        white_num = 1
        black_num = 1
        number_of_squares = 0
        if bot.is_checkmate():
            if BlackTurn:
                black_num = 0
            else:
                white_num = 0
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
        moveList = set() # number of squares occupied by opposite team
        for move in bot.legal_moves:
            newstr = bot.san(move)
            iteration = -1
            if not newstr[-1].isdigit(): # if move is check or checkmate
                iteration = iteration-1
            square = str(newstr[iteration-1]) + str(newstr[iteration])
            moveList.add(square)
        number_of_squares += len(moveList)
        valueAtPossition = black_pieces*(depth+1) - white_pieces*(depth+1) - 0.8*number_of_squares
        return valueAtPossition
    elif BlackTurn: # make sure not in checkmate currently
        bestScore = -10000
        for move in Possible_move:
            bot.push(move)
            newScore = minimax(bot.legal_moves, depth-1,False,alpha,beta,False)
            bot.pop()
            bestScore = max(newScore,bestScore)
            if bestScore == newScore and firstcall:
                theBestMove = str(move)
                theBestMoveinsan = bot.san(move)
            alpha = max(alpha,newScore)
            if firstcall: # INTIAL MOVE
                best_Score_List.append(bestScore)
                best_Moves_List.append(move)
            if beta <= alpha:
                break
        if firstcall:
            return theBestMove,theBestMoveinsan
        return bestScore
    elif not BlackTurn:
        bestScore = 10000
        for move in Possible_move:
            bot.push(move)
            newScore = minimax(bot.legal_moves, depth-1,True,alpha,beta,False)
            bot.pop()
            bestScore = min(newScore,bestScore)
            beta = min(beta,newScore)
            if beta <= alpha:
                break
        return bestScore
    else:
        #BLACK LOST CUZ NO turns left
        return 0
    

while not bot.is_checkmate():
    print(bot)
    print("Play your Move\nPRESS: SPACE to confirm")
    x = input()
    # bot.push_san(str(x))
    if bot.is_checkmate():
        break
    # Open CV views object
    # CV translates this by sending it to 2x2 matrix which then updates the board
    # MAYBE: Add GUI
    # Perform Minimax
    #interepet move
    bestMove,bestmoveinsan = minimax(bot.legal_moves,3,True,-100000,100000,True)
    InterpetMove(bestMove,bestmoveinsan)
print("Game Over!")

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