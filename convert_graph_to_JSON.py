import sys
from backend.bundle.GraphObjects.Graph import MutableGraph
from backend.bundle.GraphObjects.Edge import Edge

def main(args):
    print(args)
    nodes = read_nodes(args[1])
    edges = read_edges(args[2])
    nodes_from_edges = set([e[0] for e in edges]).union(set([e[1] for e in edges]))
    for n in nodes_from_edges:
        if n not in nodes:
            sys.exit('Error: %s is in an edge but is not in the nodefile. Exiting.' % (n))
    print('%d nodes and %d edges' % (len(nodes),len(edges)))

    G = MutableGraph()
    for n in nodes:
        G.add_node(n)
    for e in edges:
        G.add_edge('%s-%s' % (e[0],e[1]),e)

    out = open(args[3],'w')
    out.write(G.generate_json(indent=1))
    out.close()
    print('Wrote to %s' % (args[3]))
    return


def read_nodes(infile):
    nodes = set()
    with open(infile) as fin:
        for line in fin:
            nodes.add(line.strip())
    return nodes

def read_edges(infile):
    edges = set()
    with open(infile) as fin:
        for line in fin:
            row = line.strip().split('\t')
            if len(row) != 2:
                print('Error with line "%s"' % (line))
                sys.exit('Parsed as ',row)
            edges.add((row[0],row[1]))
    return edges

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit('usage: convert_graph_to_JSON.py <nodefile> <edgefile> <out.json>\n\t<nodefile>: one-column file of nodes\n\t<edgefile>: two-column tab-delimited edges\n\t<out.json>: outfile to write to.')
    main(sys.argv)
