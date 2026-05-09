import chess

best_Score_List = []
best_Moves_List = []

def reset():
    global best_Score_List, best_Moves_List
    best_Score_List = []
    best_Moves_List = []

def minimax(bot, Possible_move, depth, WhiteTurn, alpha, beta, firstcall = True): # White is chess bot
    if depth == 0 or bot.is_checkmate():
        white_num = 1
        black_num = 1
        number_of_squares = 0
        if bot.is_checkmate():
            if WhiteTurn:
                white_num = 0
            else:
                black_num = 0
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
        valueAtPossition = white_pieces*(depth+1) - black_pieces*(depth+1) - 0.8*number_of_squares
        return valueAtPossition
    elif WhiteTurn: # make sure not in checkmate currently
        bestScore = -10000
        for move in list(Possible_move):
            bot.push(move)
            newScore = minimax(bot, bot.legal_moves, depth-1,False,alpha,beta,False)
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
    elif not WhiteTurn:
        bestScore = 10000
        for move in list(Possible_move):
            bot.push(move)
            newScore = minimax(bot, bot.legal_moves, depth-1,True,alpha,beta,False)
            bot.pop()
            bestScore = min(newScore,bestScore)
            beta = min(beta,newScore)
            if beta <= alpha:
                break
        return bestScore
    else:
        # White LOST; No turns left
        return 0