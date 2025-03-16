import os
import random
import time
from typing import List, Tuple, Optional

# Constants
PLAYER_X = "X"
PLAYER_O = "O"
TIE_RESULT = "tie"
MIN_DICE_SIDES = 2
COIN_FLIP_DELAY = 0.5

# Clear the console function based on operating system
def clear_screen() -> None:
    '''Clear the terminal screen.'''
    os.system("cls" if os.name == "nt" else "clear")

# Utility functions
def get_yes_no_input(prompt: str) -> bool:
    '''Get a yes/no input from the user.'''
    while True:
        response = input(f"{prompt} (yes/no): ").lower().strip()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def validate_integer_input(prompt: str, min_value: Optional[int] = None, 
                        max_value: Optional[int] = None, 
                        error_message: Optional[str] = None) -> int:
    '''Validate integer input within optional range.'''
    while True:
        try:
            user_input = int(input(prompt))
            if min_value is not None and user_input < min_value:
                print(error_message or f"Value must be at least {min_value}.")
                continue
            if max_value is not None and user_input > max_value:
                print(error_message or f"Value must be at most {max_value}.")
                continue
            return user_input
        except ValueError:
            print("Please enter a valid number.")

def validate_float_input(prompt: str) -> float:
    '''Validate float input.'''
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

# ---------------------- TIC-TAC-TOE GAME CLASS ----------------------
class TicTacToeGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self) -> None:
        '''Reset the game board and variables.'''
        self.available_moves = list(range(1, 10))
        self.current_player = PLAYER_X
        self.board = self.create_board()

    def create_board(self) -> Tuple[List[str], ...]:
        '''Create a new game board.'''
        return (
            [str(i) for i in range(1, 4)],
            [str(i) for i in range(4, 7)],
            [str(i) for i in range(7, 10)]
        )

    def print_board(self) -> None:
        '''Print the current game board.'''
        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)

    def get_user_move(self) -> None:
        '''Get and validate user move.'''
        while True:
            try:
                print(f"Available moves: {self.available_moves}")
                user_move = int(input(f"Player {self.current_player}, enter your move: "))
                if user_move in self.available_moves:
                    row, col = divmod(user_move - 1, 3)  # More Pythonic way to get row and column
                    self.board[row][col] = self.current_player
                    self.available_moves.remove(user_move)
                    return
                else:
                    print("Move isn't available. Please select from the available moves!")
            except ValueError:
                print("Please enter a valid number from the available moves.")

    def get_ai_move(self) -> None:
        '''Generate an AI move.'''
        ai_move = random.choice(self.available_moves)
        print(f"AI's move: {ai_move}")
        row, col = divmod(ai_move - 1, 3)  # More Pythonic way to get row and column
        self.board[row][col] = self.current_player
        self.available_moves.remove(ai_move)

    def check_win(self) -> Optional[str]:
        '''Check if there's a win or tie.'''
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0]
        
        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        
        # Check for tie
        if not self.available_moves:
            return TIE_RESULT
        
        return None

    def switch_player(self) -> None:
        '''Switch to the other player.'''
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def play(self) -> None:
        '''Main game loop.'''
        clear_screen()
        print("Tic-Tac-Toe Game")
        
        ai_mode = get_yes_no_input("Do you want to play against the AI?")
        if ai_mode:
            print("AI mode enabled!")
        
        game_over = False
        
        while not game_over:
            self.print_board()
            
            # Get move (user or AI)
            self.get_user_move()
            
            # Check for win after user move
            result = self.check_win()
            if result:
                clear_screen()
                self.print_board()
                if result == TIE_RESULT:
                    print("It's a tie!")
                else:
                    print(f"Player {result} wins!")
                
                if get_yes_no_input("Would you like to play again?"):
                    self.reset_game()
                    continue
                else:
                    break
            
            # Switch player
            self.switch_player()
            
            # AI move if in AI mode
            if ai_mode and self.available_moves:
                self.get_ai_move()
                
                # Check for win after AI move
                result = self.check_win()
                if result:
                    clear_screen()
                    self.print_board()
                    if result == TIE_RESULT:
                        print("It's a tie!")
                    else:
                        print(f"Player {result} wins!")
                    
                    if get_yes_no_input("Would you like to play again?"):
                        self.reset_game()
                        continue
                    else:
                        break
                
                # Switch player back to user
                self.switch_player()

# ---------------------- ROCK-PAPER-SCISSORS GAME CLASS ----------------------
class RockPaperScissorsGame:
    # Game choices
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"
    
    def __init__(self):
        self.reset_settings()
        self.scores = {"Player 1": 0, "Player 2": 0}
        self.valid_choices = {
            "1": self.ROCK, "rock": self.ROCK, "r": self.ROCK,
            "2": self.PAPER, "paper": self.PAPER, "p": self.PAPER,
            "3": self.SCISSORS, "scissors": self.SCISSORS, "s": self.SCISSORS
        }
        self.menu_choices = ["menu", "main menu"]

    def reset_settings(self) -> None:
        '''Reset game settings to default.'''
        self.require_names = True
        self.two_player_mode = False
        self.has_names = False
        self.player1_name = "Player 1"
        self.player2_name = "The Bot"

    def main_menu(self) -> None:
        '''Display the main menu for Rock-Paper-Scissors.'''
        clear_screen()
        print("""
Rock, Paper, Scissors!
The game where Rock beats Scissors, Scissors beats Paper, and Paper beats Rock!
Pro tip 1: You can use the numbers to choose.
Pro tip 2: Type "menu" to return to the menu at any time.

Please choose an option:
1. New Game
2. Settings
3. Back to Main Menu
""")
        choice = input("Enter your choice: ").lower().strip()
        
        if choice in ["1", "new game", "n"]:
            self.pre_game()
        elif choice in ["2", "settings", "s"]:
            self.settings_menu()
        elif choice in ["3", "back to main menu", "b"] + self.menu_choices:
            return
        else:
            print("Invalid option. Please try again.")
            self.main_menu()

    def get_player_names(self) -> bool:
        '''Get player names based on settings.'''
        clear_screen()
        self.player1_name = input("Player 1, enter your name: ").strip()
        if self.player1_name.lower() in self.menu_choices:
            self.main_menu()
            return False
        
        if self.two_player_mode:
            self.player2_name = input("Player 2, enter your name: ").strip()
            if self.player2_name.lower() in self.menu_choices:
                self.main_menu()
                return False
            print(f"Hello {self.player1_name} and {self.player2_name}!")
        else:
            print(f"Hello {self.player1_name}. You'll be playing against {self.player2_name}.")
        
        input("Press Enter to continue...")
        self.has_names = True
        return True

    def pre_game(self) -> None:
        '''Prepare for the game.'''
        clear_screen()
        if self.require_names and not self.has_names:
            if not self.get_player_names():
                return
        
        self.play_round()

    def get_player_choice(self, player_name: str) -> Optional[str]:
        '''Get a player's choice.'''
        while True:
            choice = input(f"""{player_name}, please choose:
1. Rock
2. Paper
3. Scissors
""").lower().strip()
            
            if choice in self.valid_choices:
                return self.valid_choices[choice]
            elif choice in self.menu_choices:
                self.main_menu()
                return None
            else:
                print("Invalid choice. Please try again.")

    def play_round(self) -> None:
        '''Play a single round of the game.'''
        clear_screen()
        
        # Get player 1's choice
        player1_choice = self.get_player_choice(self.player1_name)
        if player1_choice is None:
            return
        clear_screen()
        
        # Get player 2's choice
        if self.two_player_mode:
            player2_choice = self.get_player_choice(self.player2_name)
            if player2_choice is None:
                return
        else:
            player2_choice = random.choice([self.ROCK, self.PAPER, self.SCISSORS])
        clear_screen()
        
        # Show choices and determine winner
        print(f"{self.player1_name} chose {player1_choice}")
        print(f"{self.player2_name} chose {player2_choice}")
        
        # Determine winner - more Pythonic way using tuples
        if player1_choice == player2_choice:
            print("It's a tie!")
        elif (player1_choice, player2_choice) in [(self.ROCK, self.SCISSORS), 
                                                (self.SCISSORS, self.PAPER), 
                                                (self.PAPER, self.ROCK)]:
            print(f"{self.player1_name} wins!")
            self.scores["Player 1"] += 1
        else:
            print(f"{self.player2_name} wins!")
            self.scores["Player 2"] += 1
        
        self.print_scores()
        input("Press Enter to continue...")
        self.after_game_menu()

    def print_scores(self) -> None:
        '''Print the current scores.'''
        print(f"\n{self.player1_name}'s score: {self.scores['Player 1']}")
        print(f"{self.player2_name}'s score: {self.scores['Player 2']}")

    def after_game_menu(self) -> None:
        '''Display menu after a game.'''
        clear_screen()
        self.print_scores()
        
        print("""\nWhat would you like to do?
1. Play Again
2. Rock-Paper-Scissors Menu
3. Back to Main Menu
""")
        
        choice = input("Enter your choice: ").lower().strip()
        
        if choice in ["1", "play again", "p"]:
            self.play_round()
        elif choice in ["2", "rock-paper-scissors menu", "r"]:
            self.main_menu()
        elif choice in ["3", "back to main menu", "b"] + self.menu_choices:
            return
        else:
            print("Invalid option. Please try again.")
            self.after_game_menu()

    def settings_menu(self) -> None:
        '''Display and handle settings.'''
        clear_screen()
        
        print(f"""Settings:
1. Require Names: {self.require_names}
2. Two Player Mode: {self.two_player_mode}
3. Reset to Default Settings
4. Back to Rock-Paper-Scissors Menu
""")
        
        choice = input("Enter your choice: ").lower().strip()
        
        if choice in ["1", "require names", "n"]:
            self.require_names = not self.require_names
            self.has_names = False
            self.settings_menu()
        elif choice in ["2", "two player mode", "t"]:
            self.two_player_mode = not self.two_player_mode
            self.player2_name = "Player 2" if self.two_player_mode and not self.require_names else "The Bot"
            self.settings_menu()
        elif choice in ["3", "reset to default settings", "d"]:
            self.reset_settings()
            self.settings_menu()
        elif choice in ["4", "back to rock-paper-scissors menu", "b"]:
            self.main_menu()
        else:
            print("Invalid option. Please try again.")
            self.settings_menu()

    def play(self) -> None:
        '''Main function to start the Rock-Paper-Scissors game.'''
        self.main_menu()

# ---------------------- NUMBER GUESSING GAME CLASS ----------------------
class NumberGuessingGame:
    def __init__(self):
        self.min_num = 1
        self.max_num = 100
        self.attempts = 5
        self.target_number = None
        self.guesses = []

    def setup_game(self) -> None:
        '''Set up the game parameters.'''
        # Get number of attempts
        self.attempts = validate_integer_input(
            "Enter the number of attempts you would like to have: ",
            min_value=1,
            error_message="You must have at least 1 attempt."
        )
        
        # Get number range
        self.max_num = validate_integer_input("Enter the highest number for the range: ")
        self.min_num = validate_integer_input(
            "Enter the lowest number for the range: ",
            max_value=self.max_num,
            error_message=f"The lowest number must be less than or equal to {self.max_num}."
        )
        
        # Generate random number
        self.target_number = random.randint(self.min_num, self.max_num)
        self.guesses = []

    def get_guess(self, attempt: int) -> int:
        '''Get the user's guess.'''
        return validate_integer_input(
            f"\nAttempt {attempt}: ",
            min_value=self.min_num,
            max_value=self.max_num,
            error_message=f"Please enter a number between {self.min_num} and {self.max_num}."
        )

    def check_guess(self, guess: int, attempt: int) -> bool:
        '''Check if the guess is correct.'''
        if guess == self.target_number:
            print(f"Correct! You guessed the number in {attempt} attempts.")
            return True
        
        print("Too low!" if guess < self.target_number else "Too high!")
        return False

    def print_summary(self, attempt: int, win: bool) -> None:
        '''Print a summary of the game.'''
        odd_guesses = [g for g in self.guesses if g % 2 != 0]
        even_guesses = [g for g in self.guesses if g % 2 == 0]
        
        print("\nGame Summary")
        print(f"- Result: {'You guessed correctly!' if win else 'You did not guess correctly!'}")
        print(f"- Target number: {self.target_number}")
        print(f"- Number of attempts used: {attempt}")
        print(f"- Your guesses: {self.guesses}")
        print(f"- Even guesses: {even_guesses}")
        print(f"- Odd guesses: {odd_guesses}")

    def play(self) -> None:
        '''Main game function.'''
        clear_screen()
        print("Number Guessing Game")
        
        while True:
            self.setup_game()
            
            print(f"\nI'm thinking of a number between {self.min_num} and {self.max_num}.")
            print(f"You have {self.attempts} attempts to guess it.")
            
            win = False
            for attempt_num in range(1, self.attempts + 1):
                guess = self.get_guess(attempt_num)
                self.guesses.append(guess)
                
                if self.check_guess(guess, attempt_num):
                    win = True
                    break
                
                if attempt_num == self.attempts:
                    print("\nYou've run out of attempts!")
                    print(f"The number was {self.target_number}.")
            
            self.print_summary(attempt_num, win)
            
            if not get_yes_no_input("\nDo you want to play again?"):
                break

# ---------------------- COIN FLIP CLASS ----------------------
class CoinFlip:
    HEADS = "Heads"
    TAILS = "Tails"
    
    def play(self) -> None:
        '''Run the coin flip game.'''
        clear_screen()
        print("Coin Flip")
        
        while True:
            input("\nPress Enter to flip a coin...")
            clear_screen()
            print("Flipping coin...")
            time.sleep(COIN_FLIP_DELAY)  # Using constant for delay
            
            # Perform the coin flip
            result = self.HEADS if random.randint(1, 2) == 1 else self.TAILS
            print(f"The coin landed on: {result}!")
            
            if not get_yes_no_input("\nDo you want to flip again?"):
                break

# ---------------------- TEMPERATURE CONVERTER CLASS ----------------------
class TemperatureConverter:
    def celsius_to_fahrenheit(self, celsius: float) -> float:
        '''Convert Celsius to Fahrenheit.'''
        return (celsius * 9/5) + 32
    
    def fahrenheit_to_celsius(self, fahrenheit: float) -> float:
        '''Convert Fahrenheit to Celsius.'''
        return (fahrenheit - 32) * 5/9
    
    def play(self) -> None:
        '''Run the temperature converter.'''
        clear_screen()
        print("Temperature Converter")
        
        while True:
            try:
                # Get temperature and conversion direction
                temperature = validate_float_input("Enter temperature: ")
                
                while True:
                    unit = input("Convert to (C/F): ").upper().strip()
                    if unit in ["C", "F"]:
                        break
                    print("Please enter either 'C' for Celsius or 'F' for Fahrenheit.")
                
                # Perform conversion
                if unit == "C":
                    converted = self.fahrenheit_to_celsius(temperature)
                    print(f"{temperature}°F is {converted:.2f}°C")
                else:  # unit == "F"
                    converted = self.celsius_to_fahrenheit(temperature)
                    print(f"{temperature}°C is {converted:.2f}°F")
                
                if not get_yes_no_input("\nDo you want to convert another temperature?"):
                    break
                    
            except ValueError as e:
                print(f"Error: {e}")
                print("Please try again.")

# ---------------------- SIMPLE CALCULATOR CLASS ----------------------
class SimpleCalculator:
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def play(self) -> None:
        '''Run the calculator.'''
        clear_screen()
        print("Simple Calculator")
        
        operations = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide
        }
        
        while True:
            try:
                # Get inputs
                num1 = validate_float_input("Enter first number: ")
                
                while True:
                    op = input("Enter operation (+, -, *, /): ").strip()
                    if op in operations:
                        break
                    print("Please enter a valid operation: +, -, *, or /")
                
                num2 = validate_float_input("Enter second number: ")
                
                # Perform calculation - more Pythonic using a dictionary of functions
                try:
                    result = operations[op](num1, num2)
                    print(f"Result: {result}")
                except ValueError as e:
                    print(f"Error: {e}")
                    if not get_yes_no_input("Do you want to try again?"):
                        break
                    continue
                
                if not get_yes_no_input("\nDo you want to perform another calculation?"):
                    break
                    
            except ValueError as e:
                print(f"Error: {e}")
                if not get_yes_no_input("Do you want to try again?"):
                    break

# ---------------------- DICE ROLLER CLASS ----------------------
class DiceRoller:
    def play(self) -> None:
        '''Run the dice roller.'''
        clear_screen()
        print("Dice Roller")
        
        while True:
            try:
                # Get number of sides
                sides = validate_integer_input(
                    "Enter number of sides on the dice: ",
                    min_value=MIN_DICE_SIDES,
                    error_message=f"A dice must have at least {MIN_DICE_SIDES} sides."
                )
                
                # Roll the dice
                roll = random.randint(1, sides)
                print(f"You rolled a {roll}!")
                
                if not get_yes_no_input("\nDo you want to roll again?"):
                    break
                    
            except ValueError as e:
                print(f"Error: {e}")
                print("Please try again.")

# ---------------------- MAIN MENU CLASS ----------------------
class GameSuite:
    def __init__(self):
        self.games = {
            "1": ("Tic-Tac-Toe", TicTacToeGame()),
            "2": ("Rock-Paper-Scissors", RockPaperScissorsGame()),
            "3": ("Number Guessing Game", NumberGuessingGame()),
            "4": ("Coin Flip", CoinFlip()),
            "5": ("Temperature Converter", TemperatureConverter()),
            "6": ("Simple Calculator", SimpleCalculator()),
            "7": ("Dice Roller", DiceRoller())
        }

    def show_menu(self) -> str:
        '''Show the main menu and get user choice.'''
        clear_screen()
        print("""
Welcome to the All-In-One Game Suite!
Please choose an option:""")
        
        for key, (name, _) in self.games.items():
            print(f"{key}. {name}")
        
        print("8. Quit")
        
        return input("\nEnter your choice: ").strip()

    def run(self) -> None:
        '''Run the game suite.'''
        while True:
            choice = self.show_menu()
            
            if choice in self.games:
                _, game = self.games[choice]
                game.play()
            elif choice == "8":
                clear_screen()
                print("Thank you for playing. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
                input("Press Enter to continue...")

# Start the program
if __name__ == "__main__":
    try:
        game_suite = GameSuite()
        game_suite.run()
    except KeyboardInterrupt:
        clear_screen()
        print("\nProgram interrupted. Exiting...")
    except Exception as e:
        clear_screen()
        print(f"\nAn unexpected error occurred: {e}")
        print("The program will now exit.") 