# replace the content of this function with your own algorithm
# inputs:
#   p: min target no. of points player must collect. p>0
#   v: 1 (non-cycle) or 2 (cycle)
#   flags: 2D list [[flagID, value, x, y], [flagID, value, x, y]....]
# returns:
#   1D list of flagIDs to represent a route. e.g. [F002, F005, F003, F009]

#creating helper functions
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

#used to calculate entire route distance, will dynamically calculate distance matrix and store for future use
def route_dist(route, dist_matrix,main):
	total_dist = 0
	previous = 'F0'
	for point in route:
		if point not in dist_matrix[previous].keys():
			dist_matrix[previous][point] = math.sqrt((abs(main[previous][2]-main[point][2])**2+abs(main[previous][3]-main[point][3])**2))
		total_dist += dist_matrix[previous][point]
		previous = point
	return total_dist

#two-opt code adpated from online source
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

#main code body
def get_route(p, v, flags):
	main = {flag[0]: [flag[0], int(flag[1]), float(flag[2]), float(flag[3])] for flag in flags} #creating master dictionary
	route = []
	start = ['F0',0,0,0]
	current_node = start #initialize starting location
	points = 0
	#greedy
	while points < p:
		local_optimal_roi = 0 #measures how much you have to travel to get the node
		for flag,potential_node in main.items():
			if flag not in route:
				#checks is node's ROI is higher than the current highests ROI found
				if (potential_node[1]/(abs((current_node[2]-potential_node[2]))**2+abs((current_node[3]-potential_node[3]))**2)) > local_optimal_roi:
					local_optimal_option = flag
					local_optimal_roi = (potential_node[1]/(abs((current_node[2]-potential_node[2])**2)+abs((current_node[3]-potential_node[3])**2)))
		#completed iteration, add selected node to suggested route list
		route.append(local_optimal_option)
		current_node = main[local_optimal_option]
		points += main[local_optimal_option][1]

	#creating basis of distance matrix, code will generate values when needed
	dist_matrix = {flag : {} for flag in route}
	dist_matrix['F0'] = {}

	#check the version of the game and perform two-opt code
	main['F0'] = ['F0',0,0,0]
	if v == 1:
		route = ['F0'] + list(route)
		result = two_opt(route, dist_matrix,main)
		result.remove('F0')
		route = result

	else:
		route = ['F0'] + list(route) + ['F0']
		result = two_opt(route, dist_matrix,main)
		result.remove('F0')
		result.remove('F0')
		route = result

	#remove the excess points exceeding the target amount
	if points > p:
		exceed_factor = points - p
		checksum = True
		to_check = Queue()
		for flag in route:
			if main[flag][1] <= exceed_factor: #put those flags that can poentially be removed into priority queue
				to_check.enqueue([main[flag][1],flag])
		while exceed_factor > 0 and checksum: #code compares to see which is the ideal node to remove based on final distance
			best_flag_removal = list()
			best_distance = 'run'
			removed = []
			while to_check.notempty():
				sample_route = route [:]
				candidate_node = to_check.dequeue()
				sample_route.remove(candidate_node[1])
				if best_distance == 'run':
					best_distance = route_dist(sample_route, dist_matrix,main)
					best_flag_removal = candidate_node
				elif route_dist(sample_route, dist_matrix,main) < best_distance:
					removed.append(best_flag_removal)
					best_distance = route_dist(sample_route, dist_matrix,main)
					best_flag_removal = candidate_node
				else:
					removed.append(candidate_node)
			if len(best_flag_removal) > 0: #remove selected node from route
				route.remove(best_flag_removal[1])
				exceed_factor -= best_flag_removal[0]
				best_flag_removal = list()
				if exceed_factor > 0 and len(removed) > 0: #if there's still more score left to deduct and flags left to potentially remove
					for flag in removed:
						if len(flag) == 0:
							pass
						elif flag[0] <= exceed_factor and len(flag) > 0:
							to_check.enqueue(flag)
					if not to_check.notempty(): #no more flags that can possibly be removed
						checksum = False
			else:
				checksum = False
	return route
