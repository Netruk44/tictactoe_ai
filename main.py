import BoardEvaluator
import Critic
import TTTPlayer
import WeightTrainer


weights = [-1.] * BoardEvaluator.NUM_WEIGHTS
entireGame = TTTPlayer.PlayGameAgainstSelf(weights)
learningExamples = Critic.generateTrainingExamplesFromGame(entireGame[1])
for i in learningExamples:
  weights = WeightTrainer.iterateWeights(weights, i)

print(weights)