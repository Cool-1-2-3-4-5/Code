import chess
bot = chess.Board()
bot.push_san(list(bot.legal_moves)[0].uci())
