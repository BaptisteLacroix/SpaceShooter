import pygame
from game import Game


# Main Game Loop

game = Game()

while game.running:
    game.current_menu.display_menu()
    game.game_loop()

running = True

pygame.quit()
