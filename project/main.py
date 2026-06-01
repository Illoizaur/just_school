import game
import world

state = "menu"

while True:
    if state == "menu":
        state = menu.menu()
    elif state == "game":    
        state = game.game()
    elif state == "quit":
        pygame.exit...()