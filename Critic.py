import CellState
import GameBoard

def extractEntireGameMoveset(moveList):
  # moveList is a list of board states and their corresponding values
  # each element is a move made by a player.
  # Optionally, other potential moves might be available
  # [
  #    (Board, 4.0, otherMoves),
  #    (Board, 2.9, otherMoves),
  #    (Board, -10),
  #    (Board, 5, otherMoves)
  # ]
  # otherMoves is itself an array of (Board, Score)

  # First, collect the definite games with scores into a set
  entireMoveset = [move[0:2] for move in moveList]

  # Then append in the other explored moves with their scores
  for moveInfo in moveList:
    if len(moveInfo) > 2:
      otherMoves = moveInfo[2]

      entireMoveset = entireMoveset + otherMoves

  return entireMoveset

def generateTrainingExamplesFromGame(moveList):
  entireMoveset = extractEntireGameMoveset(moveList)
  trainingExamples = []

  for i in range(len(entireMoveset)):
    board = entireMoveset[i][0]
    actualScore = entireMoveset[i][1]

    if i < len(moveList) - 2:
      # Main game training, train using what happened afterward
      expected_score = moveList[i+2][1]
    elif i < len(moveList):
      # We should train towards what actually happened at the end of the game
      gameWonBy = moveList[-1][0].isWon()
      if gameWonBy == CellState.CS_UNDEFINED:
        expected_score = 0.
      elif gameWonBy == CellState.CS_AI:
        expected_score = -100.
      elif gameWonBy == CellState.CS_OPPONENT:
        expected_score = 100.
      else:
        raise "Won by unknown team?"
    else:
      # By default use the actual calculated score
      expected_score = actualScore

    # If the board has been won, we know what the score should be
    winningTeam = board.isWon()
    if winningTeam != CellState.CS_UNDEFINED:
      expected_score = -100 if winningTeam == CellState.CS_AI else 100
    
    # If the board HASN'T been won, but the score is over or under 100, the score should be lower
    #elif (actualScore > 100 or actualScore < -100):
    #  expected_score = 0
    
    # We've applied all our knowledge. Check to see if the actual score
    # has deviated from the expected score.
    if abs(expected_score - actualScore) > 1.0:
      trainingExamples.append([board, expected_score])
  
  return trainingExamples
