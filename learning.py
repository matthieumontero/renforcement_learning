from environnement import gameEnvironnement
from humanPlayer import HumanPlayer
from agentPlayer import AgentPlayer

if __name__=='__main__':
    # training
    player1 = AgentPlayer(player_name="agent", symbol=1)
    player2 = AgentPlayer(player_name="opponent", symbol=-1)

    print("training...")
    game = gameEnvironnement(player1, player2)
    game.TrainAgent(rounds=5000)


    


