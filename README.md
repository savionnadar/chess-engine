# Chess Engine & Pygame GUI

An academic chess engine implementation featuring a recursive Minimax search algorithm, material evaluation, and a fully interactive graphical user interface built with Python and Pygame.

## Overview
This project bridges low-level game-tree search theory with a modern graphical interface. It utilizes `python-chess` for rigorous rule validation and move generation, while `pygame` renders an intuitive 8x8 board with dynamic piece selection, legal move validation, and game-state management.

## Technical Stack
* **Language:** Python
* **Game Logic:** `python-chess`
* **GUI Framework:** `Pygame`

## Algorithmic Architecture
### 1. Board Evaluation (`evaluate_board`)
Assigns a static numerical score to the current board state by weighing piece values (Pawns: 1, Knights/Bishops: 3, Rooks: 5, Queen: 9, King: 10,000) and checking terminal states such as checkmate or stalemate.

### 2. Move Generation (`python-chess` integration)
Extracts and validates all legal moves dynamically from the board state, filtering out illegal positions and handling special cases like pawn promotion.

### 3. Recursive Minimax (`minimax`)
Systematically traverses the game tree up to a configurable search depth (`MINIMAX_DEPTH = 3`), alternating between maximizing (White) and minimizing (Black) evaluations to determine optimal moves looking multiple turns ahead.

## Areas of Improvement: Board Evaluation Function
While the current material-weighted evaluation function provides a solid foundational baseline, it contains several strategic blind spots:
* **Piece-Square Tables (PSTs):** Currently, a piece is valued identically regardless of its position. Implementing PSTs would reward positional advantages, encouraging the engine to control the center, develop knights early, and activate kings during the endgame.
* **Pawn Structure Analysis:** The function lacks awareness of structural weaknesses such as doubled, isolated, or backward pawns, as well as passed pawn progression.
* **King Safety:** Aside from detecting checkmate, the evaluation does not penalize an exposed king or reward castled positions, occasionally leading to poor defensive decisions.

## Performance Bottleneck & Future Work
* **The Challenge:** The exponential growth of the game tree causes computation time to spike dramatically when increasing the search depth beyond 3.
* **Proposed Solution:** Implementation of **Alpha-Beta pruning** to efficiently prune branches that do not influence the final minimax decision.

