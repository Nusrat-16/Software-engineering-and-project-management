import os

def clear_screen():
    """Clears the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')