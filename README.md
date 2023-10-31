# Ai-Powered-Connect-Four
Connect-4 AI
This Python script allows you to play the classic game Connect-4, but with an AI opponent!

Game Design
The game is designed using a 2D NumPy array to represent the game board, with piece placements marked within the array.

Players indicate their moves by choosing a column to drop their piece. Constraints such as maximum column capacity and value ranges are validated.

The AI uses a sophisticated MiniMax algorithm with Alpha-Beta pruning to determine its move. The algorithm evaluates potential moves based on various factors like board state, possibilities of winning, and blocking the human player's victory.

Game Outcome
The game will continue until a winning condition is met - four consecutive pieces from the same player in any direction. Alternatively, the game ends if the board fills up without any winning condition met.
