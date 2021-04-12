import BoardEvaluator
import Critic
import TTTPlayer
import WeightTrainer

class AutoTTTLearner():
  weights = []
  learning_rate = 0.
  last_game = None

  def __init__(self, learning_rate = 5e-3):
    self.ResetWeights()
    self.learning_rate = learning_rate

  def ResetWeights(self):
    self.weights = [-1.] * BoardEvaluator.NUM_WEIGHTS

  def LearnFromSelf(self, iterations = 5):
    for _ in range(iterations):
      finalBoard, moveList = TTTPlayer.PlayGameAgainstSelf(self.weights)
      print(finalBoard, len(moveList))

      learningExamples = Critic.generateTrainingExamplesFromGame(moveList)
      print(f'Learning from {len(learningExamples)} examples last game.')
      for i in learningExamples:
        self.weights = WeightTrainer.iterateWeights(self.weights, i, learning_rate=self.learning_rate)
      
      print(self.weights)
  
  def LearnFromRandom(self, iterations = 5):
    for _ in range(iterations):
      finalBoard, moveList = TTTPlayer.PlayGameAgainstRandom(self.weights)
      print(finalBoard, len(moveList))

      learningExamples = Critic.generateTrainingExamplesFromGame(moveList)
      print(f'Learning from {len(learningExamples)} examples last game.')
      for i in learningExamples:
        self.weights = WeightTrainer.iterateWeights(self.weights, i, learning_rate=self.learning_rate)
      
      print(self.weights)

  def LearnFromGame(self, game):
    finalBoard, moveList = game
    learningExamples = Critic.generateTrainingExamplesFromGame(moveList)
    print(f'Learning from {len(learningExamples)} examples last game.')
    old_weights = self.weights
    for i in learningExamples:
      self.weights = WeightTrainer.iterateWeights(self.weights, i, learning_rate=self.learning_rate)
    print(f'Change: {[new - old for new, old in zip(self.weights, old_weights)]}')