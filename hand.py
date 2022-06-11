from dice import Dice

class Hand:
  """
  Class representing each player's hand.
  The player will lose if they are left without dices in the hand.
  """

  def __init__(self) -> None:
    self.hand = [Dice() for i in range(5)]

  def row_dice(self) -> None:

    for i in self.hand:
      i.row_dice()

  def get_hand(self) -> None:

    print("Your row is:")
    for i in self.hand:
      print(i.get_dice_row(), end=" ")
    
    print("\n")

  def get_num_of_dices(self) -> int:
    return len(self.hand)

  def get_num_of_specific_dice(self, dice_number) -> int:
    count = 0
    for i in self.hand:
      if i.get_dice_row() == dice_number:
        count += 1
    
    return count

  def lose_dice(self):
    self.hand.pop()

  # Returns the most common number in hand and return it with the half it's appearance
  def get_most_common_number(self) -> tuple:
    counter = 0
    number = 0
    dice_values = []
    for i in self.hand:
      dice_values.append(i.get_dice_row())
    
    for j in dice_values:
      current_val = dice_values.count(j)
      if current_val > counter:
        counter = current_val
        number = j

    return (int((counter+1)/2), number)


if __name__ == "__main__":
  print("This isn't the main function.")
  print("To start the game, you need to run the main.py file.")