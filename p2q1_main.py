# p2q1_main.py v1.0

from utility import *
from p2q1 import *
import copy

# replace these parameters with different csv file locations
flags_csv = "./data/flags_r1.csv" # <-- change!!!!
p = 500                          # <-- change!!!!
v = 1                              # <-- change!!!! 1 (non-cycle) or 2 (cycle)

flags = list_reader(flags_csv)
flags_dict = generate_flags_dict(flags)

your_route = get_route(p, v, flags)

# print results or error msg (if any)
err_msg, dist, points = get_dist_and_points_q1(your_route, flags_dict, v)

if err_msg !=None:
  print("Error : " + err_msg)
else:
  print("Points for this route :" + str(points) + ", p :" + str(p))

  if points < p:
    print("Error : points is lesser than p!")
  else:
    print("Quality score (dist) for q1 is : " + str(dist)) # smaller score is better
