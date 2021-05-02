# replace the content of this function with your own algorithm
# inputs:
#   p: min target no. of points player must collect. p>0
#   v: 1 (non-cycle) or 2 (cycle)
#   flags: 2D list [[flagID, value, x, y], [flagID, value, x, y]....]
# returns:
#   1D list of flagIDs to represent a route. e.g. [F002, F005, F003, F009]
import math

class Queue:
	def __init__(self):
		self.array = []
	def enqueue(self, item):
		self.array.append(item)
	def dequeue(self):
		if len(self.array) > 0:
			first = self.array[0]
			self.array = self.array[1:]
			return first
		else:
			return False
	def notempty(self):
		if len(self.array) != 0:
			return True
		else:
			return False
	def peek(self):
		if len(self.array) == 0:
			return False
		else:
			return self.array[0]
	def display(self):
		print("head => " + str(self.array))

def route_dist(route, dist_matrix,main):
	total_dist = 0
	previous = 'F0'
	for point in route:
		if point not in dist_matrix[previous].keys():
			dist_matrix[previous][point] = math.sqrt((abs(main[previous][2]-main[point][2])**2+abs(main[previous][3]-main[point][3])**2))
		total_dist += dist_matrix[previous][point]
		previous = point
	return total_dist

def two_opt(route,dist_matrix,main):
	best = route
	improved = True
	best_dist = route_dist(route, dist_matrix,main)
	while improved:
		improved = False
		for i in range(1, len(route)-2):
			for j in range(i+1, len(route)):
				if j-i == 1: continue
				new_route = route[:]
				new_route[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
				new_dist = route_dist(new_route, dist_matrix,main)
				if new_dist < best_dist:
					best = new_route
					improved = True
					best_dist = new_dist
			route = best
	return best

def get_routes(p, v, flags, n):
	main = {flag[0]: [flag[0], int(flag[1]), float(flag[2]), float(flag[3])] for flag in flags}
	# if the points needed are a comparatively small amount or when person = 1, run qn1 code
	path = [[] for i in range(n)]
	all_visited = set()
	start = ['F0',0,0,0]
	current_node = ['F0',0,0,0]
	points = 0
	selected_route_nodes = []
	#running greedy to get all points needed
	while points < p:
		local_optimal_roi = 'run' #measures how much you have to travel to get the node
		local_optimal_player = 0
		local_optimal_flag = ""
		for i in range(len(path)):
			if len(path[i]) > 0:
				player_current_node = main[path[i][-1]]
			else:
				player_current_node = start
			for flag,potential_node in main.items():
				if flag not in all_visited:
					current_distance = (abs(player_current_node[2]-potential_node[2])**2+abs(player_current_node[3]-potential_node[3])**2)
					if local_optimal_roi == 'run' or (current_distance/potential_node[1]) < local_optimal_roi:
						local_optimal_flag = flag
						local_optimal_roi = current_distance/potential_node[1]
						local_optimal_player = i
		all_visited.add(local_optimal_flag)
		path[local_optimal_player].append(local_optimal_flag)
		points += main[local_optimal_flag][1]

	#generating dictionary for distance matrix
	all_visited.add('F0')
	main['F0'] = ['F0',0,0,0]
	dist_matrix = {flag : {} for flag in list(all_visited)}

	#based the game version, add in points where needed and run two-opt
	post_two_opt = []
	for x in range(len(path)):
		path[x].insert(0,'F0')
		route = path[x]
		if v == 1:
			result = two_opt(route, dist_matrix,main)
			result.remove('F0')
			post_two_opt.append(result)
		else:
			route = list(route) + ['F0']
			result = two_opt(route, dist_matrix,main)
			result.remove('F0')
			result.remove('F0')
			post_two_opt.append(result)

	#check if the amount of points is more than what is required
	if points > p:
		exceed_factor = points - p
		checksum = True
		to_check = Queue()
		all_visited.remove('F0')
		for route_id in range(len(post_two_opt)):
			curr_route = post_two_opt[route_id]
			for flag in curr_route:
				if main[flag][1] <= exceed_factor: #put all candidates for removal into a queue
					to_check.enqueue([main[flag][1],math.sqrt(abs(main[flag][2]-0)**2+abs(main[flag][3]-0)**2),flag,route_id])
		best_dist_arr = {route_id : route_dist(post_two_opt[route_id], dist_matrix,main) for route_id in range(len(post_two_opt))}
		while exceed_factor > 0 and checksum:
			best_flag_removal = list()
			best_improvment = 0
			removed = []
			while to_check.notempty(): #dequeue each node 1 by 1 and check how much improvment it will make if it was removed
				candidate_node = to_check.dequeue()
				sample_route = post_two_opt[candidate_node[3]][:]
				sample_route.remove(candidate_node[2])
				if (best_dist_arr[candidate_node[3]] - route_dist(sample_route, dist_matrix,main)) > best_improvment:
					removed.append(best_flag_removal)
					best_improvment = (best_dist_arr[candidate_node[3]] - route_dist(sample_route, dist_matrix,main))
					best_flag_removal = candidate_node
				else:
					removed.append(candidate_node)
			if len(best_flag_removal) > 0: #process choosen node and update excess score
				post_two_opt[best_flag_removal[3]].remove(best_flag_removal[2])
				exceed_factor -= best_flag_removal[0]
				best_dist_arr[best_flag_removal[3]] = route_dist(post_two_opt[best_flag_removal[3]], dist_matrix,main)
				best_flag_removal = list()
				best_improvment = 0
				if exceed_factor > 0 and len(removed) > 0: #still room for improvment, queue all nodes for another iteration
					for flag in removed:
						if len(flag) == 0:
							pass
						elif flag[0] <= exceed_factor:
							to_check.enqueue(flag)
					if not to_check.notempty():
						checksum = False
			else:
				checksum = False	
	return post_two_opt
