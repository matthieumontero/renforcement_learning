# classe pour spécifier un joueur humain
class HumanPlayer:
    def __init__(self, name='humain', symbol=1):
        self.name = name
        self.symbol = symbol

    def chooseNextBestAction(self, index_position):
        action = None
        while action is None:
            index = input("Enter row i and column j such i,j : ")
            act = (int(index[0])-1, int(index[2])-1)
            if act in index_position:
                action= act
            else:
              print('Position unavailable. choose another case : \n\n')
        return action


