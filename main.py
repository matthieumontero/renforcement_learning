from environnement import gameEnvironnement
from humanPlayer import HumanPlayer
from agentPlayer import AgentPlayer

if __name__=='__main__':
    # play with random
    computer = AgentPlayer("computer",epsilon=0.3, gamma=0.9, symbol=1) 
    computer.loadPolicy("policy_agent")

    random = RandomPlayer(name='humain', symbol=1)

    game = gameEnvironnement(computer, random)
    game.playWithAnother()