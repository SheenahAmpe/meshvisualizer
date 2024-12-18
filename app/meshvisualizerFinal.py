import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self):
        self.graph = nx.Graph()

    def read_graph_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2:  # Node
                        node = parts[0]
                        self.graph.add_node(node)
                    elif len(parts) == 3:  # Edge with weight
                        node1, node2, weight = parts
                        try:
                          weight = float(weight)
                          self.graph.add_edge(node1, node2, weight=weight)
                        except ValueError:
                          print(f"Invalid weight format for edge: {node1}, {node2}, {weight}")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def update_graph(self, filename):
        self.graph.clear()  # Clear existing graph
        self.read_graph_from_file(filename)
        # Fixed Seed
        pos = nx.kamada_kawai_layout(self.graph, weight='weight')  # Using kamada_kawai_layout with weight consideration
        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.title("Mesh Network Distance in Meters")
        image_path = '/tmp/graph_visualization.png'
        plt.savefig(image_path)
        plt.close()
        return image_path


# # Update and visualize the graph
# update_graph(file_path)
