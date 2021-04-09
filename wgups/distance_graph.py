#!/usr/bin/env python -u
# encoding: utf-8


class DistanceGraph:
    """This creates an adjacency matrix 
    
    """

    def __init__(self, distance_data):
        self.distance_data = distance_data
        self.graph = self.create_graph()
        self.nodes = len(self.graph)

    def __repr__(self):
        return str(self.graph)
    
    def create_graph(self):
        """"Create the adjacency matrix from the imported distance data
        Time complexity: O(n^2)
        Space complexity: O(n) 
        
        """
        distance_graph = []

        for x in self.distance_data:
            distance_graph.append(x)

        for i in range(0, len(distance_graph)):
            for j in range(0, len(distance_graph[i])):
                #The distance data was only half filled in, complete the full graph
                if distance_graph[i][j] == "":
                    distance_graph[i][j] = distance_graph[j][i]
            
        return distance_graph
        

    def shortest_path(self, start):
        """Dijkstra's Shortest Path Algorithm
        Time complexity: O(n log n)
        Space complexity: O(n) 
        """
        
        
        
        #create a list of nodes and set the value of all to 'inf'
        distance = [float('inf')] * self.nodes
        #create another list of visited nodes and set the values to False
        visited = [False] * self.nodes

        #Set the source node to 0
        distance[start] = 0
        
        #Find the node with the shortest distance to the source node
        def _minimum_distance(nodes, distance, visited):

            # Initialize minimum distance for next node
            min = float('inf')

            
            for node in range(nodes):
                if distance[node] < min and visited[node] is False:
                    min = distance[node]
                    min_index = node

            return min_index

        for _ in range(self.nodes):
            u = _minimum_distance(self.nodes, distance, visited)
            visited[u] = True


            # Update distance[n] if: 
            # 1. It is not in visited, 
            # 2. There is an path from u to n
            # 3. the distance from the source node to n through u is smaller than distance[n]   
            for n in range(self.nodes):
                if visited[n] is False and float(self.graph[u][n]) > 0  and distance[u] + float(self.graph[u][n]) < distance[n]:
                    distance[n] = round(distance[u] + float(self.graph[u][n]), 1)

        return distance

    #Update the adjacency matrix using Shortest Path Algorithm
    #to get the shortest distance between all nodes
    def shortest_adj_matrix(self):
        """Adjacency matrix with Shortest Path Algorithm giving smallest distance between locations
        Time complexity: O(n^2 log n)
        Space complexity: O(n) 
        """
        adj_matrix = []
        for i in range(0, self.nodes):
            distance = self.shortest_path(i)
            adj_matrix.append(distance)
        return adj_matrix

