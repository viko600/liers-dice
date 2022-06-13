from game import Game

"""
The main file for the game.
Once started, a game instance will be called and the main loop will be started
"""

if __name__ == "__main__":

  print("Welcome to the liar's dice CLI")
  players = 0
  while True:
    try:
      players = int(input("Whit how many bots you want to play [number between 1 and 10]: "))
      if players < 1 or players > 10:
        print("Enter a valid number of players.")
        continue
      break
    except:
      print("You need to enter a number")

  game = Game(players + 1)
  game.main_loop()
