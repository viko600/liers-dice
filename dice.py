from random import randint

class Dice:
  """
  Each dice in the player's hand is represented by a class
  with a couple of helper functions
  """
  def __init__(self) -> None:
    self.face = 0
  
  def get_dice_row(self) -> int:
    return self.face
  
  def row_dice(self) -> None:
    self.face = randint(1, 6)



if __name__ == "__main__":
  print("This isn't the main function.")
  print("To start the game, you need to run the main.py file.")