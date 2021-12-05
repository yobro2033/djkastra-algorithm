"""
I imagine this is nowhere near the best implementation of the algorithm
-For one working_nodes, finalised_nodes, and newest_finalised node are scoped to Graph not to the Dijkstras method which
 would be ideal
-I also imagine that other aspects could be better opimised
-Only currently works with bi-directional connections, though I believe to fix this it would only really require
 tinkering with which nodes get the connection object appended to their list of connections
"""


class Graph:
    def __init__(self, *nodes):
        self.nodes = nodes
        self.working_nodes = []  # list of nodes with working values
        self.finalised_nodes = []  # list of nodes with final values
        self.newest_finalised_node = None

    def find_node_by_name(self, name: str):  # loops through each node in the graph until it finds one with the name
        for node in self.nodes:
            if node.name == name:
                return node

    def add_connections(self, *connections: (str, str, int)):
        for conn in connections:
            node_a = self.find_node_by_name(conn[0])  # getting the node object from the string name
            node_b = self.find_node_by_name(conn[1])  # see above
            conn_object = Connection(node_a, node_b, conn[2])
            node_a.connections.append(conn_object)  # the connection object needs to be added to both nodes
            node_b.connections.append(conn_object)

    def __evaluate_next_finalised_node(self):
        lowest_value = 999999
        lowest_node = None
        for node in self.working_nodes:
            if lowest_value > node.working_value:  # finding the lowest working weight in the working nodes
                lowest_value = node.working_value
                lowest_node = node

        # remove from working nodes and add to finalised nodes, set to the newest finalised node, and give a final value
        self.working_nodes.remove(lowest_node)
        self.finalised_nodes.append(lowest_node)
        self.newest_finalised_node = lowest_node
        lowest_node.final_value = lowest_node.working_value

    def dijkstras(self, start: str, end: str):

        """
        Dijkstras Instructions:
        (start node is called S and end node called E, N is the newest node to receive a final value)
        1. set S.final_value = 0, N = S
        2. set working value at every node connected to N to N.final_value + that_connection.weight
        3. finalise the value of the node with the lowest current working value which hasn't been finalised (new N)
        4. If N == E the algorithm is complete, GOTO 6
        5. GOTO 2
        6. To find the shortest path traceback from E
        """

        start_node = self.find_node_by_name(start)
        end_node = self.find_node_by_name(end)
        start_node.final_value = 0
        self.newest_finalised_node = start_node
        while True:
            if self.newest_finalised_node == end_node:
                break

            for connection in self.newest_finalised_node.connections:
                node, weight = connection.get_contents(self.newest_finalised_node)
                if node not in self.finalised_nodes:
                    node.evaluate_working_value(weight, self.newest_finalised_node)  # decide if the working value of that should change
                    if node not in self.working_nodes:  # only add it to the working nodes if it's not already there
                        self.working_nodes.append(node)

            self.__evaluate_next_finalised_node()  # decide the next node to be finalised
            print(f"finalised Nodes : {[node.name for node in self.finalised_nodes]}")
            print(f"working Nodes: {[node.name for node in self.working_nodes]}")
            print("--------------------------------------------------------------------------------------------------")

        path = []
        cursor = end_node
        while True:
            path.append(cursor.name)
            cursor = cursor.cheapest_node_to
            if cursor == start_node:
                path.append(cursor.name)
                break
        path.reverse()
        print(f"path: {path}")
        print(f"weight: {end_node.final_value}")



class GraphNode:
    def __init__(self, name: str):
        self.name = name
        self.connections = []
        self.working_value = 99999
        self.cheapest_node_to = None

    def evaluate_working_value(self, weight: int, node_from):
        if self.working_value > weight + node_from.final_value:
            self.working_value = weight + node_from.final_value
            self.cheapest_node_to = node_from


class Connection:
    def __init__(self, node_a: GraphNode, node_b: GraphNode, weight: int):
        self.graphNodes = (node_a, node_b)
        self.weight = weight

    def get_contents(self, node_checked_from: GraphNode) -> (GraphNode, int):
        return [i for i in self.graphNodes if i != node_checked_from][0], self.weight


# should be if __name__ == "__main__" but pycharm wasn't liking that so using the classic fix of just get rid of it.
if True:
    names = ["S", "A", "D", "T", "B", "C"]
    n = [GraphNode(name) for name in names]
    graph = Graph(*n)
    graph.add_connections(("S", "A", 5),
                          ("S", "B", 6),
                          ("S", "C", 2),
                          ("A", "D", 4),
                          ("B", "D", 4),
                          ("B", "T", 8),
                          ("B", "C", 2),
                          ("C", "T", 12),
                          ("D", "T", 3))
    graph.dijkstras("S", "T")
