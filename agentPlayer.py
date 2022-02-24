## Class to create agent
import numpy as np
import pickle 

class AgentPlayer:
  def __init__(self, player_name='Agent', alpha=0.2, epsilon=0.3, gamma=0.9, symbol=1):
      self.name = player_name
      self.states = []  
      self.alpha = alpha
      self.epsilon = epsilon
      self.gamma = gamma
      self.q_value = {} 
      self.symbol = symbol

  def getHash(self, board):
      boardHash = str(board.reshape(3*3))
      return boardHash

  def chooseNextBestAction(self, index_position, current_configuration):
      # policy : epsilon greedy

      # Exploration
      random = np.random.uniform(0,1)
      if random <= self.epsilon:
          idx = np.random.choice(len(index_position))
          action = index_position[idx]
      else:
          # Exploitation : choose available action which allow to obtain the max_value
          value_max = -100000
          for p in index_position:
              next_config = current_configuration.copy()
              next_config[p] = self.symbol
              next_configHash = self.getHash(next_config)
              value = 0 if self.q_value.get(next_configHash) is None else self.q_value.get(next_configHash)

              if value >= value_max:
                  value_max = value
                  action = p
      return action

  # append a hash state
  def addState(self, state):
      self.states.append(state)

  # update qvalue of state
  def update_qvalue(self, reward):
      for state in reversed(self.states):
          if self.q_value.get(state) is None:
              self.q_value[state] = 0
          self.q_value[state] += self.alpha * (self.gamma * reward - self.q_value[state])
          reward = self.q_value[state]

  def reset(self):
      self.states = []

  def savePolicy(self):
      with open('policy_'+str(self.name), 'wb') as file:
        pickle.dump(self.q_value, file)

  def loadPolicy(self, file):
    with open(file, 'rb') as file:
      self.q_value = pickle.load(file)

