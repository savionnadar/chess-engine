import chess
import pygame

pygame.init()

WIDTH, HEIGHT = 640, 640
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

LIGHT_COLOR = pygame.Color("#f0d9b5")
DARK_COLOR = pygame.Color("#b58863")
HIGHLIGHT_COLOR = pygame.Color(255, 255, 0, 100)

UNICODE_PIECES = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}

# --- YOUR CHESS BOT LOGIC ---
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 10000,
}

MINIMAX_DEPTH = 3

def evaluate_board(board):
  if board.is_checkmate():
    return -99999 if board.turn == chess.WHITE else 99999
  if board.is_stalemate() or board.is_insufficient_material():
    return 0

  total_score = 0
  for square in chess.SQUARES:
    piece = board.piece_at(square)
    if piece:
      value = PIECE_VALUES[piece.piece_type]
      total_score += value if piece.color == chess.WHITE else -value
  return total_score


def minimax(board, depth, is_white):
  if depth == 0 or board.is_game_over():
    return evaluate_board(board)

  if is_white:
    max_eval = -float("inf")
    for move in board.legal_moves:
      board.push(move)
      eval_score = minimax(board, depth - 1, not is_white)
      board.pop()
      max_eval = max(max_eval, eval_score)
    return max_eval
  else:
    min_eval = float("inf")
    for move in board.legal_moves:
      board.push(move)
      eval_score = minimax(board, depth - 1, not is_white)
      board.pop()
      min_eval = min(min_eval, eval_score)
    return min_eval


def best_move(board, depth):
  is_white = board.turn == chess.WHITE
  best_eval = -float("inf") if is_white else float("inf")
  best_move_found = None

  for move in board.legal_moves:
    board.push(move)
    eval_score = minimax(board, depth - 1, not is_white)
    board.pop()

    if is_white:
      if eval_score > best_eval:
        best_eval = eval_score
        best_move_found = move
    else:
      if eval_score < best_eval:
        best_eval = eval_score
        best_move_found = move

  return best_move_found

# GUI
def draw_board(screen):
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      color = LIGHT_COLOR if (r + c) % 2 == 0 else DARK_COLOR
      pygame.draw.rect(
          screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
      )


def draw_pieces(screen, board):
  font_name = None
  available_fonts = pygame.font.get_fonts()
  for candidate in [
      "segoeuisymbol",
      "dejavusans",
      "arial",
      "freesans",
      "helvetica",
  ]:
    if candidate in available_fonts:
      font_name = candidate
      break

  font = pygame.font.SysFont(font_name, 45)

  for square in chess.SQUARES:
    piece = board.piece_at(square)
    if piece:
      row = 7 - (square // 8)
      col = square % 8

      piece_symbol = UNICODE_PIECES[piece.symbol()]
      

      text_color = (255, 255, 255) if piece.color == chess.WHITE else (20, 20, 20)
      
      if piece.color == chess.WHITE:
        shadow_surface = font.render(piece_symbol, True, (0, 0, 0))
        screen.blit(
            shadow_surface,
            shadow_surface.get_rect(
                center=(col * SQ_SIZE + SQ_SIZE // 2 + 2, row * SQ_SIZE + SQ_SIZE // 2 + 2)
            ),
        )

      text_surface = font.render(piece_symbol, True, text_color)
      screen.blit(
          text_surface,
          text_surface.get_rect(
              center=(col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)
          ),
      )

def main():
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Python Chess Bot (Minimax)")
  clock = pygame.time.Clock()

  board = chess.Board()
  selected_square = None
  player_is_white = True  # You play as White, Bot plays as Black
  
  # NEW: Track whether we've already printed the game over message
  game_over_printed = False

  running = True
  while running:
    # Handle Bot's Turn if it's Black's turn and game isn't over
    if not board.is_game_over() and board.turn != player_is_white:
      pygame.display.flip()
      pygame.time.wait(300)  # Brief pause so the bot feels natural
      ai_move = best_move(board, depth=MINIMAX_DEPTH)
      if ai_move:
        board.push(ai_move)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      # Mouse click handling for human player (only if game isn't over!)
      elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == player_is_white and not board.is_game_over():
        location = pygame.mouse.get_pos()  
        col = location[0] // SQ_SIZE
        row = location[1] // SQ_SIZE
        clicked_square = chess.square(col, 7 - row)

        if selected_square is None:
          piece = board.piece_at(clicked_square)
          if piece and piece.color == player_is_white:
            selected_square = clicked_square
        else:
          move = chess.Move(selected_square, clicked_square)
          
          if board.piece_at(selected_square).piece_type == chess.PAWN and (
              chess.square_rank(clicked_square) == 7
              or chess.square_rank(clicked_square) == 0
          ):
            move = chess.Move(selected_square, clicked_square, promotion=chess.QUEEN)

          if move in board.legal_moves:
            board.push(move)
            selected_square = None
          else:
            piece = board.piece_at(clicked_square)
            if piece and piece.color == player_is_white:
              selected_square = clicked_square
            else:
              selected_square = None

    # Drawing the screen
    screen.fill((255, 255, 255))
    draw_board(screen)
    
    if selected_square is not None:
      r = 7 - (selected_square // 8)
      c = selected_square % 8
      s = pygame.Surface((SQ_SIZE, SQ_SIZE))
      s.set_alpha(100)
      s.fill((0, 255, 0))
      screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

    draw_pieces(screen, board)

    # Print game over result exactly ONCE
    if board.is_game_over() and not game_over_printed:
      print("Game Over! Result:", board.result())
      print("Termination reason:", board.outcome())
      game_over_printed = True

    pygame.display.flip()
    clock.tick(MAX_FPS)

  pygame.quit()

if __name__ == "__main__":
  main()
