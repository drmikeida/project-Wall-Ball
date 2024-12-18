import pyxel
import math
import random

class App:
    def __init__(self):
        # Initialize the Pyxel window (width, height)
        pyxel.init(160, 120)
        # Set the initial position of the square
        self.reset_game()

        # Start the game loop
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        # Reset game state variables
        self.x = 75
        self.y = 55
        self.score = 0
        self.sprite_x = 80
        self.sprite_y = 60
        self.sprite_dx = 2.2
        self.sprite_dy = 2.2
        self.state = "start_menu"
        self.arrows = []

    def update(self):
        if self.state == "start_menu":
            # Check for key presses to start the game
            if pyxel.btn(pyxel.KEY_RETURN):
                self.state = "game"
        elif self.state == "game":
            # Update the square's position based on arrow keys
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
                self.y -= 2
            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
                self.y += 2
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
                self.x -= 2
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
                self.x += 2

            # Gives points when the square touches the sprite
            distance = math.sqrt((self.x - self.sprite_x)**2 + (self.y - self.sprite_y)**2)
            if distance <= 10:  
                self.score += 1

            # Check for game over condition
            if self.score <= -150:
                self.state = "game_over"
            if self.score >= 400:
                self.state = "game win"

            # Wrap the square around the screen
            self.x %= 160
            self.y %= 120

            # Update the sprite's position
            self.sprite_x += self.sprite_dx
            self.sprite_y += self.sprite_dy

            # Bounce the sprite off the edges of the screen
            if self.sprite_x <= 0 or self.sprite_x >= 160:
                self.sprite_dx *= -1
                self.sprite_x = max(0, min(self.sprite_x, 160))  # Keep within bounds
            if self.sprite_y <= 0 or self.sprite_y >= 120:
                self.sprite_dy *= -1
                self.sprite_y = max(0, min(self.sprite_y, 120))  # Keep within bounds

            # Generate arrows randomly
            if self.score >= 100:
                if random.random() < 0.1:  # Increase the chance of generating an arrow (10%)
                    self.arrows.append([random.randint(0, 160), random.randint(0, 120), random.choice([2, -2]), random.choice([2, -2])])
            else:
                if random.random() < 0.08:  # 5% chance of generating an arrow
                    self.arrows.append([random.randint(0, 160), random.randint(0, 120), random.choice([1, -1]), random.choice([1, -1])])

            # Move arrows
            for arrow in self.arrows:
                arrow[0] += arrow[2]
                arrow[1] += arrow[3]

            # Check for collisions with arrows
            for arrow in self.arrows:
                if abs(self.x - arrow[0]) < 10 and abs(self.y - arrow[1]) < 10:
                    self.arrows.remove(arrow)
                    self.score -= 10

            # Remove off-screen arrows
            self.arrows = [arrow for arrow in self.arrows if 0 <= arrow[0] <= 160 and 0 <= arrow[1] <= 120]

        elif self.state == "game_over":
            # Allow restarting the game when the key is pressed
            if pyxel.btn(pyxel.KEY_BACKSPACE):
                self.reset_game()  # Reset the game state
        elif self.state == "game win":
            if pyxel.btn(pyxel.KEY_BACKSPACE):
                self.reset_game()

    def draw(self):
        # Clear the screen with black (color 0)
        pyxel.cls(7)
        if self.state == "start_menu":
            # Draw the start menu text
            pyxel.text(50, 50, "Press Enter to Start", 8)
        elif self.state == "game":
            # Draw a square (color 9)
            pyxel.rect(self.x, self.y, 10, 10, 8)
            pyxel.tri(self.x, self.y - 5, self.x + 5, self.y - 15, self.x + 10, self.y - 5, 8) 
            pyxel.rect(self.x + 3, self.y - 15, 4, 5, 8) 
            pyxel.text(50, 110, "Merry Christmas!", 8)
            pyxel.text(110, 5, "Stage One", 8)
            pyxel.rectb(0, 0, 160, 120, 2)  # Green border
            # Draw the moving sprite (color 11)
            colors = [11, 12, 13, 14, 18, 22]
            color = random.choice(colors)
            pyxel.circ(self.sprite_x, self.sprite_y, 7, color)
            # Display the score
            pyxel.text(5, 5, f"Score: {self.score}", 0)
            # Display a message when score is high
            if self.score >= 100:
                pyxel.text(50, 50, "You’re doing great!", 8)
            # Draw arrows
            for arrow in self.arrows:
                pyxel.tri(arrow[0], arrow[1], arrow[0] + 5, arrow[1] - 5, arrow[0] + 5, arrow[1] + 5, 10)
        elif self.state == "game_over":
            # Draw the game over screen
            pyxel.cls(7)
            pyxel.text(50, 50, "Game Over!", 8)
            pyxel.text(30, 70, "Final Score: " + str(self.score), 8)
            pyxel.text(20, 90, "Press Backspace to Restart", 8)
        elif self.state == "game win":
            pyxel.cls(7)
            pyxel.text(50, 50, "You win!", 8)
            pyxel.text(30, 70, "Final Score: " + str(self.score), 8)
            pyxel.text(20, 90, "Press backspace to play again", 8)

# Run the game
App()

