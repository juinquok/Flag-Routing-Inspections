This was a school project where we were challenged to optimize the route for a specific player based on the variables given below. The context is given below:

A game is to be played in a huge open flat field where several flags are
planted. Each flag is labelled with a positive number that indicates the
number of points the flag is worth. Players touching a flag the first time will
receive these points (no points for a subsequent touch). All players start
from the same starting point (SP) (x=0.0, y=0.0). When the whistle blows,
players are free to move from flag to flag to collect as many points as
possible by touching them.

For simplicity, you can assume that all players run at the same speed (which implies that the total
distance travelled determines the time taken by each player). You can also assume that players
move from between flags directly in straight lines. This means that the distance between two flags
can be easily calculated as the Euclidian distance between these two points. In order to facilitate
planning, players are given the coordinates of every single flag, as well as the points of each flag
before the game starts.
You are given multiple flags.csv files:
• flags<x>.csv: The list of flags is shown in this file with the following attributes: flag ID,
points, x-coordinate, y-coordinate. Each line in this CSV file represents one flag. For
example, the following three lines represent three flags in the field:
F001, 3, -39.0888931396, 14.9550391799
F002, 1, -10.3413339776, -14.6545825259
F003, 4, 25.7389470222, 32.5374354386

### Part 1

You are a player in this game. The objective is to collect at least p points. (Since players run at the
same speed, this means that you want to minimize the distance taken in your route.) It does not
matter how many points you manage to accumulate; as long as you get at least p points. Plan the
route that you will take in your attempt to win the game. There are two variations of this game:
(i) In the first variation, players stop at the last flag in their route to end the game; there
is no need to move back to the SP.
(ii) in the second variation, all players must get back to the SP to end the game.
In both variations, the objective is still the same: minimize the distance the player has to travel to
collect at least p points.

The function is expressed as get_route(p,v,flags) in p2q1.py. Test it using p2q1_main.py

p → target number of points a player must collect before ending the game. p >0 and there are enough flags on the field

v → game variation, in version 1, players do not need to return to the starting point but in version 2, players need to return to the starting point. 

flags → 2D list of unique flag IDs as well as the x,y coordinates of each flag. 

Function returns a list of Flag IDs that represent the best reoute determined by the algorithm.

### Part 2

You manage a team of n players in this game (where n is a number from 1 to 8). The rules and
objective of the game is the same as for Q1 except that:
(i) Players in your team do not get points for touching the same flag more than once. If
player 1 has already touched F0009, no other player in your team should touch the
same flag.
(ii) The total number of points collected by the whole team need to be at least p to end
the game.
Plan the routes for each player in your team so as to minimize the total distance travelled by all
players in order to collect at least p points as a team.

The function is expressed as get_route(n,v,flags) in p2q2.py. Test it using p2q2_main.py

n → number of players in the team between 1 and 8 (inclusive)

v → game variation, in version 1, players do not need to return to the starting point but in version 2, players need to return to the starting point. 

flags → 2D list of unique flag IDs as well as the x,y coordinates of each flag. 

Function returns a list of Flag IDs that represent the best reoute determined by the algorithm.