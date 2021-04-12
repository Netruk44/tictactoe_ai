import BoardEvaluator
import CellState
import Critic

def iterateWeights(currentWeights, example, learning_rate = 0.1):
  # currentWeights: list
  # example: (board, training value)

  currentValue = BoardEvaluator.EvaluateBoard(example[0], CellState.CS_AI, currentWeights)
  currentMetric = BoardEvaluator.GetBoardMetrics(example[0])
  error = example[1] - currentValue

  return [w + (learning_rate * error * x) for w, x in zip(currentWeights, currentMetric)]
