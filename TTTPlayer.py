import BoardEvaluator
import GameBoard
import CellState
import random

def MakeMove(board, team, weights, returnOtherOptions = False):
  possibleMoves = []

  for movePosition in board.getEmptyPositions():
    potentialBoard = board.copy()
    potentialBoard.setCell(movePosition[0], movePosition[1], team)

    possibleMoves.append((
      potentialBoard, 
      BoardEvaluator.EvaluateBoard(potentialBoard, team, weights)
    ))
  
  # Sort by lowest score first
  possibleMoves.sort(key=lambda m: m[1])
  bestMove = possibleMoves[0]

  if returnOtherOptions:
    return bestMove[0], possibleMoves
  else:
    return bestMove[0]

def PlayGameAgainstRandom(weights):
  board = GameBoard.GameBoard()
  boardHistory = [(board, BoardEvaluator.EvaluateBoard(board, CellState.CS_AI, weights))]
  isWon = False
  isFull = False
  teamToMove = random.choice([CellState.CS_AI, CellState.CS_OPPONENT])

  while not isWon and not isFull:
    if teamToMove == CellState.CS_AI:
      nextBoard, otherMoves = MakeMove(board, teamToMove, weights, returnOtherOptions=True)
    else:
      emptySpots = board.getEmptyPositions()
      nextBoard = board.copy()
      nextBoard.makeRandomMove(CellState.CS_OPPONENT)
      otherMoves = []

    nextBoardScore = BoardEvaluator.EvaluateBoard(nextBoard, CellState.CS_AI, weights)
    board = nextBoard
    boardHistory.append((board, nextBoardScore, otherMoves))
    teamToMove = CellState.CS_OPPONENT if teamToMove == CellState.CS_AI else CellState.CS_AI
    isWon = board.isWon()
    isFull = board.isFull()
  
  return board, boardHistory

def PlayGameAgainstSelf(weights):
  board = GameBoard.GameBoard()
  boardHistory = [(board, BoardEvaluator.EvaluateBoard(board, CellState.CS_AI, weights))]
  isWon = False
  isFull = False
  teamToMove = random.choice([CellState.CS_AI, CellState.CS_OPPONENT])

  while not isWon and not isFull:
    nextBoard, otherMoves = MakeMove(board, teamToMove, weights, returnOtherOptions=True)
    nextBoardScore = BoardEvaluator.EvaluateBoard(nextBoard, CellState.CS_AI, weights)

    if teamToMove == CellState.CS_OPPONENT:
      # Need to change the otherMoves scores. They're scores for the CS_OPPONENT team.
      # Training assumes that these scores are for the CS_AI team.
      for i in range(len(otherMoves)):
        otherMoves[i] = (otherMoves[i][0], BoardEvaluator.EvaluateBoard(otherMoves[i][0], CellState.CS_AI, weights))

    board = nextBoard
    boardHistory.append((board, nextBoardScore, otherMoves))
    teamToMove = CellState.CS_OPPONENT if teamToMove == CellState.CS_AI else CellState.CS_AI
    isWon = board.isWon()
    isFull = board.isFull()
  
  return board, boardHistory


human_game_history = []
human_board = GameBoard.GameBoard()

def StartNewGameAgainstHuman(weights, ai_starts = False):
  global human_board
  global human_game_history
  human_board = GameBoard.GameBoard()
  human_game_history = [(human_board, BoardEvaluator.EvaluateBoard(human_board, CellState.CS_AI, weights))]

  if ai_starts:
    nextBoard, otherMoves = MakeMove(human_board, CellState.CS_AI, weights, returnOtherOptions=True)
    nextBoardScore = BoardEvaluator.EvaluateBoard(nextBoard, CellState.CS_AI, weights)

    human_board = nextBoard
    human_game_history.append((human_board, nextBoardScore, otherMoves))

  return human_board

def PlayHumanTurn(weights, x, y):
  global human_board
  global human_game_history
  assert human_board.getCell(x, y) == CellState.CS_UNOWNED

  # Set opponent turn
  human_board = human_board.copy()
  human_board.setCell(x, y, CellState.CS_OPPONENT)
  nextBoardValue = BoardEvaluator.EvaluateBoard(human_board, CellState.CS_AI, weights)

  human_game_history.append((human_board, nextBoardValue))
  #print(human_game_history[-1])

  # Play AI turn
  if not human_board.isWon() and not human_board.isFull():
    nextBoard, otherMoves = MakeMove(human_board, CellState.CS_AI, weights, returnOtherOptions=True)
    nextBoardScore = BoardEvaluator.EvaluateBoard(nextBoard, CellState.CS_AI, weights)

    human_board = nextBoard
    human_game_history.append((human_board, nextBoardScore, otherMoves))
    #print(human_game_history[-1][0:2])
  
  print(human_game_history[-1][1])
  print('')
  return human_board

def GetHumanGame():
  global human_board
  global human_game_history
  
  return (human_board, human_game_history)