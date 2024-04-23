import networkx as nx
import os
import random

class NetworkNotReadError(Exception):
    pass

class Recommender:
    
    def __init__(self):
        self.DEFAULT_DATA_FOLDER = "./networks"

    def read_pajek(self, filename, label_parser = None):

        """
        Read a Pajek format file (.net) and create a NetworkX graph.

        Parameters:
        -----------
        filename : str
            The name of the Pajek file (without extension) to be read.

        data_folder : str
            The path to the folder containing the Pajek file.

        label_parser : Callable[[str, str], Dict[str, Any]], optional
            A function used to parse node labels and values from the Pajek file.
            If not specified, a default label_parser function is used.

        Returns:
        --------
        G : nx.Graph
            A NetworkX graph representing the structure defined in the Pajek file."""
            
        filename = os.path.splitext(filename)[0]

        if label_parser is None:
            def label_parser(lab, val): return \
                {"label": lab} if val is None else {"label": lab, "value": val}

        with open(os.path.join(self.DEFAULT_DATA_FOLDER,  f"{filename}.net"), encoding="UTF-8") as file:
            file.readline()
            nodes = []

            for line in file:
                if line.startswith("*"):
                    match line.split()[0][1:]:
                        case "edges": G = nx.MultiGraph(name=filename)
                        case "arcs": G = nx.MultiDiGraph(name=filename)
                        case link_type: raise SyntaxError(f"invalid link type: {link_type}")
                    break
                else: # add node
                    match line.strip().split("\""):
                        case num, lab:
                            nodes.append((int(num) - 1, label_parser(lab, None)))
                        case num, lab, val:
                            nodes.append((int(num) - 1, label_parser(lab, val)))
                        case _:
                            raise SyntaxError("failed to parse " + line)

            G.add_nodes_from(nodes)

            for line in file:
                i, j = (int(x) - 1 for x in line.split()[:2])
                G.add_edge(i, j)

        self.G =  G
        return self
    
    def find_node(self, G: nx.Graph, label: str):
        
        """
        Find a node with a specific label in a NetworkX graph.

        Parameters:
        -----------
        G : nx.Graph
            The NetworkX graph in which to search for the node.

        label : str
            The label of the node to find.

        Returns:
        --------
        node_id : node identifier
            The identifier of the node (typically node index) that matches the given label."""
        for i, data in G.nodes(data=True):
            if data['label'] == label:
                return i
        raise ValueError(f"node '{label}' not found in {G.name}")

    def pagerank(self, G: nx.Graph, alpha=0.85, eps=1e-6, teleport: set | None = None):
        
        '''
        This function calculates page rank with power iteration.
        
        Parameters:
        -----------
        G: Networkx instance for graph objects.
        alpha: Damping factor 0.85 by default.
        eps: Convergence threshold for the power iteration algortihm.
        teleport: Nodes to teleport each time (random walks). If its set to None it will just be a normal page rank.
        
        Returns:
        -----------
        Dictionary of the for nodes and their corresponding page rank scores.
        '''
        
        P = [1 / len(G)] * len(G)
        diff = 1
        while diff > eps:
            U = [sum([P[j] * alpha / G.degree(j) for j in G[i]])
                for i in G.nodes()]
            u = sum(U)
            if teleport is not None:
                for i in teleport:
                    U[i] += (1 - u) / len(teleport)
            else:
                U = [U[i] + (1 - u) / len(G) for i in G.nodes()]
            diff = sum([abs(P[i] - U[i]) for i in G.nodes()])
            P = U
        return {i: P[i] for i in range(len(P))}

    def top_nodes(self, G: nx.Graph, C: dict[any, float], centrality: str, labels, n=10) -> list[any]:
        
        """ 
        Find and print the top 'n' nodes in a NetworkX graph based on a specified centrality measure.

        Parameters:
        -----------
        G : nx.Graph
            The NetworkX graph in which to identify the top nodes.

        C : Dict[Any, float]
            A dictionary containing centrality scores for nodes in the graph `G`.
            Keys are node identifiers, and values are centrality scores (float).

        centrality : str
            The type of centrality measure used to rank nodes (e.g., "degree centrality", "betweenness centrality").

        n : int, optional
            The number of top nodes to identify and return (default is 10).

        Returns:
        --------
        nodes : List[Any]
            A list containing the identifiers of the top 'n' nodes based on the specified centrality measure."""
            
        nodes = []
        for i, _ in sorted(C.items(), key=lambda item: (item[1], G.degree[item[0]]), reverse=True):
            if not (G.nodes[i]['label'].startswith('m-')) and not (G.nodes[i]['label'] in labels):
                nodes.append(G.nodes[i]['label'])
                n -= 1
                if n == 0:
                    break
                
        return nodes

    def get_recommendations(self, label, alpha = 0.85, eps = 1e-3, k = 10):
        """
        Get top node recommendations based on PageRank centrality scores in a NetworkX graph.

        Parameters:
        -----------
        G : nx.Graph
            The NetworkX graph from which recommendations will be generated.

        label : set
            The label of the node for which recommendations are sought.

        alpha : float, optional
            The damping factor (teleport probability) used in the PageRank algorithm (default is 0.85).

        eps : float, optional
            The convergence threshold for PageRank algorithm (default is 1e-3).

        k : int, optional
            The number of top recommendations to return (default is 10).

        Returns:
        --------
        recommendations : List[Any]
            A list of recommended nodes based on PageRank centrality scores.
            
        Raises:
        -------
        NetworkNotReadError: If no network file read before using get_recommendations method.
        """
        
        if not hasattr(self, 'G'):
            raise NetworkNotReadError("No network file read before using get_recommendations method.")
        G = self.G
        teleport_nodes = set([self.find_node(G = G, label = n) for n in label])
        pagerank = self.pagerank(G = G, alpha = alpha, eps = eps, teleport = teleport_nodes)
        recommendations = self.top_nodes(G = G, C = pagerank, centrality = 'pagerank', n = k, labels = label)
        return recommendations


    
    def get_category_list(self, G):
        """
        Get the list of categories in the graph.
        
        Parameters:
        -----------
        G : nx.Graph
            The NetworkX graph from which recommendations will be generated.
        
        Returns:
        --------
        categories : List[str]
            A list of categories in the graph."""
        categories = [n[1]['label'] for n in G.nodes(data=True)]
        return set(categories)
    
    def get_random_list(self, G, k=10):
        """
        Get the list of random nodes in the graph.
        
        Parameters:
        -----------
        G : nx.Graph
            The NetworkX graph from which recommendations will be generated.
        
        Returns:
        --------
        randoms : List[str]
            A list of random nodes in the graph."""
        node_list = [n[1]['label'] for n in G.nodes(data=True) if not n[1]['label'].startswith('m-')]
        randoms = random.sample(node_list, k)
        return randoms
    
if __name__ == '__main__':
    rec = Recommender()
    rec.read_pajek('movies_graph.net')
    recommendations = rec.get_recommendations(rec.G, 'Moana')
    print(recommendations)
