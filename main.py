from environnement import gameEnvironnement
from humanPlayer import HumanPlayer
from agentPlayer import AgentPlayer

if __name__=='__main__':
    # jeu avec un joueur jouant aléatoirement
    computer = AgentPlayer("computer",epsilon=0.3, gamma=0.9, symbol=1) 
    computer.loadPolicy("policy_agent")

    opponent = HumanPlayer(name='humain', symbol=-1)

    game = gameEnvironnement(opponent, computer)
    game.playWithAnother()