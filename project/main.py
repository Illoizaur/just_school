from menu import runmenu
from game import rungame

def main():
    if runmenu():
        rungame()

if __name__ == "__main__":
    main()