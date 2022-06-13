from hand import Hand
from random import uniform, randint

class Game:
  """
  The game class is where the core of the game takes place.
  The class takes the number of players as an input and has no output.
  In the class there are 2 loops, one is the main game loop, which
  goes through all players and rolls the dice in their hands,
  and the other is for the bet machine, that will go through each player
  and will ask them if they want to raise or call the previous player a lia
  r.
  """
  def __init__(self, num_players) -> None:
    self.round = 0
    self.current_bet = [0, 0]
    self.players = {}
    self._init_players(num_players)
    self.current_player_pointer = 'player1'
    self.previous_player_pointer = 'player0'
    self.bet_stopper = False

  def _init_players(self, player_count):
    for i in range(1, player_count + 1):
      self.players[f'player{i}'] = Hand()
  
  def _number_of_players(self) -> int:
    return len(self.players)

  def main_loop(self) -> None:

    while True:
      # Check for winning conditions
      if self._check_for_end():
        break
      
      # Row dices of player and bots
      for i in self.players.values():
        i.row_dice()
      
      self._display_player_row()

      # Start the betting
      self._bet_machine()

      # Raising the round counte with 1
      self.round += 1

    if 'player1' in self.players:
      print(f"Congratulations you won at rount {self.round}!!!")

    else:
      print(f"You lost on round {self.round}. Better luck next time!")

  def _check_for_end(self) -> bool:
    return (self._number_of_players() < 2 or 'player1' not in self.players)

  def _display_player_row(self):
    self.players['player1'].get_hand()

  def _bet_machine(self):

    # the first player makes a bet
    # But the first player can be a bot too
    self._raise()

    while not self.bet_stopper:
      print(f"Current player is {self.current_player_pointer}")
      # every other player is given a choise to raise or call a lie
      self._player_bet()

    # Bet goes back to 0 and the bet marker is returned to False
    self.current_bet = [0, 0]
    self.bet_stopper = False

  def _player_bet(self):

    # If the human player is on turn, show a menu with options
    if self.current_player_pointer == 'player1':

      bet = ''
      print(f"Current bet is {self.current_bet[0]} of {self.current_bet[1]}")
      while bet != 'c' and bet != 'r':
        bet = input("Do you want to raise [r] or call lie [c]: ")
      
      if bet == 'c':
        self._call_lie()

      elif bet == 'r':
        self._raise()
    
    # Else play a bot turn
    else:
      self._bot_turn()

  # Player or bot raise
  def _raise(self):

    bet_raise = 0
    what_number = 1
    if self.current_player_pointer == 'player1':
      while True:
        if self.current_bet[1] == 0:
          try:
            what_number = int(input("What value are you announcing: "))
          except:
            print("The dice has values from 1 to 6")
            continue
        try:
          bet_raise = int(input("How much you need to raise: "))
        except:
          print(f"You should enter a number grater then {self.current_bet[0]}")
          continue


        if bet_raise <= self.current_bet[0]:
          print(f"You should enter a number grater then {self.current_bet[0]}")
          continue
      
        elif what_number < 0 or what_number > 6:
          print("The dice has values from 1 to 6")
          continue
          
        else:
          break
    else:
      bet_raise, what_number = self.players[self.current_player_pointer].get_most_common_number()
      print(f"{self.current_player_pointer.capitalize()} has called {bet_raise} of {what_number}")
    
    
    # Raise the bet only if it's valid
    self.current_bet[0] = bet_raise
    self.current_bet[1] = what_number if self.current_bet[1] == 0 else self.current_bet[1]
    self._switch_playrs('normal')

  def _call_lie(self):
    # Stop the betting in the bet machine loop and see if the previos player was lying
    self.bet_stopper = True
    all_dice_count = 0
    bet_loser = 'player0'
    print(f"{self.current_player_pointer.capitalize()} calls a lie on {self.previous_player_pointer.capitalize()}.....")
    print(f"The last bet from {self.previous_player_pointer.capitalize()} was {self.current_bet[0]} of {self.current_bet[1]}...")

    for player_hand in self.players.values():
      all_dice_count += player_hand.get_num_of_specific_dice(self.current_bet[1])

    print("===============================================")

    if self.current_bet[0] > all_dice_count:
      print(f"{self.current_player_pointer.capitalize()} wins!!!!")
      print(f"There were {all_dice_count} dices in total\n")
      bet_loser = self.previous_player_pointer
      # the loser must become the next player
      self._switch_playrs('lose')

    else:
      print(f"{self.current_player_pointer.capitalize()} loses.")
      print(f"There were {all_dice_count} dices in total\n")
      bet_loser = self.current_player_pointer
      
    print("===============================================")

    self._lose_dice(bet_loser)


  def _bot_turn(self):
    # if the number of called dice is divided by the number of currents 
    # players multiplied by a wildcard is bigger than 1 call a lie
    if int((self.current_bet[0] / self._number_of_players()) * uniform(0, 1)) >= 1:
      print("Bot calls a lie")
      self._call_lie()

    else:
      # both raises the bet
      self.current_bet[0] += randint(1, int(self._number_of_players()/self.current_bet[0])+1)
      print(f"The both has raised the beth to {self.current_bet[0]}")
      self._switch_playrs('normal')

  def _switch_playrs(self, condition):

    if condition == 'normal':
      # Go to next player and keep track on the previos player
      self.previous_player_pointer = self.current_player_pointer

      if self.current_player_pointer == list(self.players.keys())[-1]:
        self.current_player_pointer = list(self.players.keys())[0]

      else:
        player_index = list(self.players.keys()).index(self.current_player_pointer)
        self.current_player_pointer = list(self.players.keys())[player_index + 1]

    if condition == 'lose':
      if not (self.players[self.previous_player_pointer].get_num_of_dices() < 2):
        self.current_player_pointer = self.previous_player_pointer
      
      
  def _lose_dice(self, player: str):

    self.players[player].lose_dice()

    if (self.players[player].get_num_of_dices()) < 1:
      print(f"{player.capitalize()} was eliminated")
      self.players.pop(player)

    else:
      print(f"{player.capitalize()} lost a dice and now has {self.players[player].get_num_of_dices()} dices left.")


if __name__ == "__main__":
  print("This isn't the main function.")
  print("To start the game, you need to run the main.py file.")
