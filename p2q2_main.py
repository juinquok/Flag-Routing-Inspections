# p2q2_main.py v1.0

from utility import *
from p2q2 import *
import copy

# replace these parameters with different csv file locations
flags_csv = "./data/flags_m3.csv" # <-- change!!!!
p = 100                        # <-- change!!!!
v = 1                           # <-- change!!!! 1 (non-cycle) or 2 (cycle)
n = 5                            # <-- change!!!!

flags = list_reader(flags_csv)
flags_dict = generate_flags_dict(flags)

your_routes = get_routes(p, v, flags, n)

# print results or error msg (if any)
err_msg, dist, points = get_dist_and_points_q2(your_routes, flags_dict, v, n)

if err_msg !=None:
  print("Error : " + err_msg)
else:
  print("Points for all routes :" + str(points) + ", p :" + str(p))

  if points < p:
    print("Error : points is lesser than p!")
  else:
    print("Quality score (dist for all routes) for q2 is : " + str(dist)) # smaller score is better
