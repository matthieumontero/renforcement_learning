import numpy as np
from tqdm import tqdm

class gameEnvironnement:

  def __init__(self, player1, player2):
    self.board = np.zeros((3,3)) # initialisation of board
    self.player1 = player1
    self.player2 = player2
    self.isOver = False
    self.boardHash = None

    # We give the hand to the first player whose symbol is 1
    self.playerSymbol = 1

  def game_over(self):
    if any(self.board.sum(axis=1)==3) or any(self.board.sum(axis=0)==3) or any(self.board.diagonal()==3) or  any(np.fliplr(self.board).diagonal()==3):
      self.isOver = True
      return 1
    elif any(self.board.sum(axis=1)==-3) or any(self.board.sum(axis=0)==-3) or any(self.board.diagonal()==-3) or  any(np.fliplr(self.board).diagonal()==-3):
      self.isOver=True
      return -1
    else:
      if len(self.availablePositions())==0:
        self.isOver=True
        return 0
      else:
        self.isOver = False
        return None

  # Associate to each current board a unique hash
  def getHash(self):
    self.boardHash = str(self.board.reshape(3 * 3))
    return self.boardHash


  def availablePositions(self):
    return list(zip(*np.where(self.board==0)))


  # Reward value to each state
  def giveReward(self):
    result = self.game_over()
    # backpropagate reward
    if result == 1:
        self.player1.update_qvalue(1)
        self.player2.update_qvalue(0)
    elif result == -1:
        self.player1.update_qvalue(0)
        self.player2.update_qvalue(1)
    else:
        self.player1.update_qvalue(0.1)
        self.player2.update_qvalue(0.5)

  # board reset
  def reset(self):
    self.board = np.zeros((3, 3))
    self.boardHash = None
    self.isOver = False
    self.playerSymbol = 1

  def updateState(self, position, playerSymbol):
    self.board[position] = playerSymbol

  ## Train agent with agent Random
  def TrainAgent(self, rounds=100):

    list_reward_player1 = [0]*rounds
    list_reward_player2 = [0]*rounds

    for i in tqdm(range(rounds)):
      while not self.isOver:
        # Player 1 play
        positions = self.availablePositions()
        p1_nextMove = self.player1.chooseNextBestAction(positions, self.board)
        # take action and upate board state
        self.updateState(p1_nextMove, self.player1.symbol)
        board_hash = self.getHash()
        self.player1.addState(board_hash)
        # check board status if it is end

        win = self.game_over()

        if win is not None:
          self.giveReward()

          if win==self.player1.symbol:
            list_reward_player1[i] = 1

          self.player1.reset()
          self.player2.reset()
          self.reset()
          break
        else:
          # Player 2 play
          positions = self.availablePositions()
          p2_nextMove = self.player2.chooseNextBestAction(positions, self.board)
          self.updateState(p2_nextMove, self.player2.symbol)

          win = self.game_over()
          if win is not None:
            self.giveReward()
            
            if win==self.player2.symbol:
              list_reward_player2[i] = 1

            self.player1.reset()
            self.player2.reset()
            self.reset()
            break

    self.player1.savePolicy()
    print('finish')

    return {'rounds': rounds, 'reward_player1':list_reward_player1, 'reward_player2':list_reward_player2}

  def playWithAnother(self, rounds=100):
    while not self.isOver:
      # Player 1 : Human
      positions = self.availablePositions()
      p1_NextMove = self.player1.chooseNextBestAction(positions) 
      self.updateState(p1_NextMove, self.player1.symbol)
      self.showBoard()

      # check board status if it is end
      win = self.game_over()
      if win is not None:
        # win == -1
        if win == self.player1.symbol:
            print(self.player1.name, " is the winners")
        else:
            print("anyone won the match")
        self.reset()
        break
      else:
        # Player 2 :  agent pretrained
        positions = self.availablePositions()
        p2_NextMove = self.player2.chooseNextBestAction(positions, self.board)
        self.updateState(p2_NextMove, self.player2.symbol)
        self.showBoard()

        win = self.game_over()
        if win is not None:
          if win == self.player2.symbol:
              print(self.player2.name, "wins!")
          else:
              print("anyone won the match")
          self.reset()
          break

  def showBoard(self):
    # x if symbol ==1, o is symbol==-1
    for i in range(0, 3):
      print('-------------')
      out = '| '
      for j in range(0, 3):
        if self.board[i, j] == 1:
            token = 'x'
        if self.board[i, j] == -1:
            token = 'o'
        if self.board[i, j] == 0:
            token = ' '
        out += token + ' | '
      print(out)
    print('-------------')