# visualizer.py
import graphviz

def generate_career_graph(path_data: str):
    """
    Generates a Graphviz chart from structured text data.
    Expects input like: "Node1" -> "Node2"
    """
    dot = graphviz.Digraph('CareerPath', comment='Career Path Visualization')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Helvetica')
    dot.attr('edge', color='grey', fontname='Helvetica')
    dot.attr(rankdir='LR', size='10,5') # Left to Right layout

    # Initial node
    dot.node("start", "Your Current Role", shape='ellipse', fillcolor='lightgreen')

    # Keep track of nodes to avoid duplicates
    nodes = {"start"}

    lines = path_data.strip().split('\n')
    for line in lines:
        if '->' in line:
            parts = line.split('->')
            source = parts[0].strip().replace('"', '')
            destination = parts[1].strip().replace('"', '')

            # If it's a top-level path, connect from the start
            if source.lower() == "career start" or source.lower() == "current role":
                source_node = "start"
            else:
                source_node = source
            
            if source_node not in nodes:
                dot.node(source_node, source)
                nodes.add(source_node)
            
            if destination not in nodes:
                dot.node(destination, destination)
                nodes.add(destination)

            dot.edge(source_node, destination)

    # If no valid edges were created, show a simple message
    if len(dot.body) <= 1:
        dot.node("A", "Could not generate a visual path.")
        dot.node("B", "Please try refining your input.")
        dot.edge("A", "B")

    return dot