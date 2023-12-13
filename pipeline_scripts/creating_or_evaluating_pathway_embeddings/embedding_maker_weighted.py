import os
import numpy as np
import networkx as nx
import gensim
from tqdm import tqdm
from scipy.sparse import load_npz
from collections import defaultdict

class WeightedNode2Vec:
    def __init__(self, graph, dimensions, walk_length, num_walks, p=1, q=1, workers=1):
        self.graph = graph
        self.dimensions = dimensions
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.p = p
        self.q = q
        self.workers = workers

    def generate_walk(self, start_node):
        walk = [start_node]
        prev_node = None
        for _ in range(self.walk_length - 1):            
            current_node = walk[-1]
            neighbors = list(self.graph.neighbors(current_node))
            if not neighbors:
                break  # end the walk if the current node has no neighbors
            probabilities = [self.graph[current_node][neighbor]['weight'] for neighbor in neighbors]
            probabilities = np.array(probabilities)

            # Adjust probabilities based on previous node
            if prev_node is not None:
                for i, neighbor in enumerate(neighbors):
                    if neighbor == prev_node:
                        probabilities[i] /= self.p  # less likely to return to the previous node
                    elif self.graph.has_edge(prev_node, neighbor):
                        probabilities[i] /= self.q  # less likely to move away from the previous node
            probabilities /= np.sum(probabilities)

            next_node = np.random.choice(neighbors, p=probabilities)
            walk.append(next_node)
            prev_node = current_node
        return walk

    def fit(self):
        walks = []
        for _ in tqdm(range(self.num_walks), desc="Generating walks"):
            nodes = list(self.graph.nodes)
            np.random.shuffle(nodes)
            for node in tqdm(nodes, desc="Processing nodes"):
                walk = self.generate_walk(node)
                walks.append([str(node) for node in walk])

        model = gensim.models.Word2Vec(
                    walks,
                    vector_size=self.dimensions,
                    window=10,
                    min_count=1,
                    workers=self.workers,
                    sg=1,
                    epochs=1
                )

        # Extract embeddings and save them to a .npy file
        embeddings = np.array([model.wv[str(node)] for node in self.graph.nodes])
        return embeddings, model

# List of file paths
file_paths = [
    #"/0_weighted_adj_matrix.npz",
   # "/1_weighted_adj_matrix.npz",
   # "/2_weighted_adj_matrix.npz",
    "/3_weighted_adj_matrix.npz", 
]


# Process each file
for file_path in tqdm(file_paths):
    adjacency_matrix = load_npz(file_path)
    graph = nx.Graph(adjacency_matrix)
    node2vec = WeightedNode2Vec(graph, dimensions=64, walk_length=80, num_walks=10, workers=4, p=1, q=1)
    embeddings, model = node2vec.fit()

    # Save the embeddings to a .npy file in the same directory as the input file
    input_file_name = os.path.basename(file_path).split('.')[0]
    output_file_name = f"{input_file_name}_embeddings.npy"
    output_path = os.path.join(os.path.dirname(file_path), output_file_name)
    np.save(output_path, embeddings)
