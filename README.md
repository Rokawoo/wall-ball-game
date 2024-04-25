

<div align="center">
  <h1>Wall Ball</h1>
  <p>By Rokawoo</p>
  ![Vintage Labels](https://static.vecteezy.com/system/resources/thumbnails/018/887/506/small/shapes-vintage-labels-png.png)
</div>

**Game Overview**
Wall & Ball is a classic arcade-style game where players control a paddle to bounce a ball around a room while protecting their boundaries. The goal is to achieve 20 bounces to win and aim for as many additional bounces as possible before losing all health. Built with Python's Pygame library, Wall & Ball is fast-paced, challenging, and fun for players of all skill levels.

**Gameplay**
- Start the game by pressing the **SPACE** key.
- Move the paddle horizontally using the **mouse**.
- The game pauses when the ball hits your boundary or when you reach the win condition (20 bounces). Resume the game at any time by pressing **SPACE** again.
- When the ball hits the paddle, 1 point is added, and the ball's speed increases by 5%.
- If the ball hits your boundary, you lose 5 points, and your speed is recalculated based on your current score. You also lose 1 health point, which pauses the game for a moment to give you a break. You lose when health points reach zero.

**Game Features**
- **Scoreboard**: Displays the player's current score.
- **Speedboard**: Shows the current speed of the ball.
- **Healthboard**: Indicates the player's remaining health points.
- **Sound Effects**: Enjoy sounds that correlate with game events, like hitting the paddle or boundaries.
- **Trail and Rainbow Effects**: The ball leaves a trail after a certain number of bounces, with a rainbow effect when 12 hits are reached.
- **Pause Functionality**: The game pauses when the ball hits the boundary or if you win, allowing you to take a breather. Resume by pressing **SPACE**.
- **Win/Lose Conditions**: Win by reaching 20 bounces. Lose if all health points are lost.
- **Dynamic Difficulty**: The ball's speed increases exponentially, keeping the challenge engaging and fun.
- **Afterplay**: Continue playing after winning if you still have health points remaining.

**Game Structure**
- `Ball.py`: Defines the `Ball` class, responsible for the ball's movement and properties.
- `Paddle.py`: Contains the `Paddle` class, responsible for the paddle's movement and properties.
- `Text.py`: Handles the `Text` class, displaying the score, speed, and health.
- `Boundary.py`: Defines the `Boundary` class, which creates the game boundaries.
- `Drawable.py`: A parent class for managing the location and collision detection of other classes.
- `main.py`: The main script to start the game, update the game state, and render graphics.

**Controls**
- **SPACE**: Start or resume the game.
- **Mouse Left/Right**: Move the paddle left or right.

**Credits**
Wall & Ball was developed by Augustus Sroka using the Pygame library. It draws inspiration from classic arcade games like Pong and traditional wallball games played by children. 

**How to Play**
To play Wall & Ball, run the `main.py` script with Python. Have fun, and enjoy the game!
