from menu import runmenu
from game import rungame

def main():
    while True:
        if not runmenu():
            break
        
        game_result = rungame()
        
        if game_result == "menu":
            continue
        else:
            break

if __name__ == "__main__":
    main()