import CellState

class GameBoard():
  board = []

  def __init__(self, otherBoard = None):
    if otherBoard is None:
      self.clear()
    elif type(otherBoard) == list:
      assert len(otherBoard) == 9
      self.board = otherBoard.copy()

      for x in self.board:
        assert x in CellState.VALID_CELLSTATES
    elif 'board' in otherBoard.__dict__:
      self.board = otherBoard.board.copy()
  
  def getRow(self, row):
    assert row >= 0 and row < 3

    start = 3 * row
    end = start + 3
    return self.board[start:end]
  
  def getColumn(self, col):
    assert col >= 0 and col < 3

    return [
      self.board[col],
      self.board[col + 3],
      self.board[col + 6]
    ]
  
  def getDiagonal(self, offAxis):
    # \
    if offAxis:
      return [
        self.board[0],
        self.board[4],
        self.board[8]
      ]
    # /
    else:
      return [
        self.board[2],
        self.board[4],
        self.board[6]
      ]
  
  def getCount(self, team, countingFn, debug=False):
    count = 0

    for i in range(3):
      row = self.getRow(i)
      col = self.getColumn(i)

      if countingFn(row, team):
        if debug:
          print(f'match row {i}')
        count = count + 1
      if countingFn(col, team):
        if debug:
          print(f'match col {i}')
        count = count + 1
    
    if countingFn(self.getDiagonal(False), team):
      if debug:
        print(f'match diag false')
      count = count + 1
    if countingFn(self.getDiagonal(True), team):
      if debug:
        print(f'match diag true')
      count = count + 1
    
    return count
  
  def setCell(self, x, y, newState):
    assert 0 <= x <= 2
    assert 0 <= y <= 2
    assert newState in CellState.VALID_CELLSTATES

    self.board[y * 3 + x] = newState
  
  def getCell(self, x, y):
    assert 0 <= x <= 2
    assert 0 <= y <= 2

    return self.board[y * 3 + x]
  
  def copy(self):
    return GameBoard(self)
  
  def clear(self):
    self.board = [
      CellState.CS_UNDEFINED,
      CellState.CS_UNDEFINED,
      CellState.CS_UNDEFINED,
      CellState.CS_UNDEFINED,
      CellState.CS_UNDEFINED,
      CellState.CS_UNDEFINED,
      CellState.CS_UNDEFINED,
      CellState.CS_UNDEFINED,
      CellState.CS_UNDEFINED
    ]
  
  def printBoard(self):
    printChars = ['_', 'X', 'O']
    for i in range(len(self.board)):
      if i % 3 == 0 and i > 0:
        print('')
      
      print(printChars[self.board[i]], end = ' ')
    
    print('')

  def getEmptyPositions(self):
    return [IndexToXY(x) for x in self.getEmptyIndices()]

  def getEmptyIndices(self):
    return [x for x in range(9) if self.board[x] == CellState.CS_UNDEFINED]
  
  def makeRandomMove(self, team):
    from random import choice

    self.board[choice(self.getEmptyIndices())] = team
  
  def swap(self):
    def invert(cell):
      if cell == CellState.CS_CIRCLE:
        return CellState.CS_CROSS
      elif cell == CellState.CS_CROSS:
        return CellState.CS_CIRCLE
      else:
        return CellState.CS_UNDEFINED
    
    return GameBoard([invert(x) for x in self.board])

  def isWon(self):
    def teamWon(cells):
      return cells[0] if (cells[0] == cells[1] == cells[2]) else CellState.CS_UNDEFINED
    
    for i in range(3):
      r = teamWon(self.getRow(i))
      c = teamWon(self.getColumn(i))

      if r != CellState.CS_UNDEFINED:
        return r
      if c != CellState.CS_UNDEFINED:
        return c
    
    d = teamWon(self.getDiagonal(False))
    if d != CellState.CS_UNDEFINED:
      return d

    d = teamWon(self.getDiagonal(True))
    if d != CellState.CS_UNDEFINED:
      return d
    
    # Neither team has won this cell yet
    return CellState.CS_UNDEFINED
  
  def isFull(self):
    return all([x != CellState.CS_UNDEFINED for x in self.board])
    
  def __repr__(self):
    return str(self)

  def __str__(self):
    printChars = ['_', 'X', 'O']
    out = ''
    for i in range(len(self.board)):
      if i % 3 == 0 and i > 0:
        out = out + '\n'
      
      out = f'{out}{printChars[self.board[i]]} '
    
    return out

def RandomBoard():
  import random
  isWon = 1
  board = GameBoard()

  while isWon > 0:
    board.clear()
    movesMade = random.randrange(1, 5)
    for move in range(movesMade):
      board.makeRandomMove(1)
      board.makeRandomMove(2)
    
    isWon = board.isWon()
  
  return board

def IndexToXY(idx):
  return (idx % 3, idx // 3)