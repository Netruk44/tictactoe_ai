import CellState

NUM_WEIGHTS = 7

def GetBoardMetrics(board):
  # Metrics:
  # number of 3-in-a-row for X's (team 1)
  # number of 3-in-a-row for O's (team 2)
  # number of 2-in-a-row that can still be won t1
  # number of 2-in-a-row that can still be won t2
  # number of rows that can still be won for t1
  # number of rows that can still be won for t2
  # which team owns the center

  ret = [
    board.getCount(1, threeInARow),
    board.getCount(2, threeInARow), # This seems like a bad parameter, it never gets updated
    board.getCount(1, twoInARow),
    board.getCount(2, twoInARow),
    board.getCount(1, winnable),
    board.getCount(2, winnable),
    centerIsOwnedByTeam(board, 1)
  ]

  assert len(ret) == NUM_WEIGHTS
  return ret

def EvaluateBoard(board, team, weights):
  assert len(weights) >= NUM_WEIGHTS

  # AI always assumes it's team 1, so if we're evaluating
  # for team 2, swap the board.
  if team == 2:
      board = board.swap()
  
  metrics = GetBoardMetrics(board)
  return sum([x[0] * x[1] for x in zip(metrics, weights)])

def threeInARow(cells, team):
  assert len(cells) == 3
  assert team in CellState.VALID_CELLSTATES
  
  return (cells[0] == team and 
    cells[0] == cells[1] and
    cells[1] == cells[2])
  
def twoInARow(cells, team):
  assert len(cells) == 3
  assert team in CellState.VALID_CELLSTATES

  if any([c != team and c != CellState.CS_UNOWNED for c in cells]):
    return False

  return (
    (cells[0] == team and 
      (cells[0] == cells[1] or cells[0] == cells[2])) or 
    (cells[1] == team and cells[1] == cells[2])
  )
  
def winnable(cells, team):
  assert len(cells) == 3
  assert team in CellState.VALID_CELLSTATES
  return all([c == CellState.CS_UNDEFINED or c == team for c in cells])

def centerIsOwnedByTeam(board, team):
  return 1 if board.getCell(1, 1) == team else -1

# TODO: Rename from 'self' to board, don't use 1-9, etc.
def getEmptyCellsNearTeamCount(self, team):
  cellCount = 0

  for i in range(9):
    if self.board[i] == team:
      # Found a cell for the specified team, how many are blank?
      for xOff in range(-1, 2):
        for yOff in range(-1, 2):
          x = (i % 3) + xOff
          y = (i // 3) + yOff
          idx = y * 3 + x

          # Bounds check
          if x < 0 or x > 2 or y < 0 or y > 2:
            continue

          assert 0 <= idx <= 9

          if self.board[idx] == CellState.CS_UNDEFINED:
            cellCount = cellCount + 1
  
  return cellCount