import numpy as np

# classe pour spécifier un random player (joueur jouant aléatoirement)
class RandomPlayer:
  def __init__(self,player_name='Random', gamma=0.9, alpha=0.2, symbol=-1):
    self.name = player_name
    self.states = [] 
    self.gamma = gamma
    self.alpha = alpha
    self.q_value = {} 
    self.symbol = symbol

  # crée une clé pour la configuration du tableau
  def getHash(self, board):
    boardHash = str(board.reshape(3*3))
    return boardHash

  def chooseNextBestAction(self, index_position):
    idx = np.random.choice(len(index_position))
    action = index_position[idx]
    return action

  # ajoute un état hash
  def addState(self, state):
    self.states.append(state)

  # met à jour la qvalue de l'état
  def update_qvalue(self, reward):
    for state in reversed(self.states):
      if self.q_value.get(state) is None:
        self.q_value[state] = 0
      self.q_value[state] += self.alpha * (self.gamma * reward - self.q_value[state])
      reward = self.q_value[state]

  def reset(self):
      self.states = []