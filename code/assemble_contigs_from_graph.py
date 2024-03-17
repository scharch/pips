#!/usr/bin/env python3.6

import sys
from Bio.Seq import Seq

class Contig():
    def __init__(self, header_line):
        self.num, self.length, self.cov = header_line[1:].strip().split(" ")
        self.children = []
    def set_seq(self, seq_line):
        self.seq = Seq(seq_line.strip())
    def pos(self):
        return str(self.seq)
    def neg(self):
        return str(self.seq.reverse_complement())
    def __str__(self):
        return self.pos()
    def __repr__(self):
        return str(self)

class ContigNode():
    def __init__(self, contig, forward, other):
        self.contig = contig
        self.forward = forward
        self.seq = contig.pos() if forward else contig.neg()
        self.children = {}
        self.other = other
    def get_cov(self):
        return int(self.other.split(" ")[1][2:-1])
    def add_child(self, other, dist):
        self.children[other] = dist
    def name(self):
        return str(self.contig.num) + ("+" if self.forward else "-")
    def get_sequence_paths(self):
        out = []
        if not self.children:
            return [[(self, 0)]]
        for child, dist in self.children.items():
            paths = child.get_sequence_paths()
            for path in paths:
                out.append([(self, dist)] + path)

        return out
    def __repr__(self):
        child_str = [child.name() for child in self.children]
        return self.name() + " {" + ",".join(child_str) + "}"

class ContigGraph():
    def __init__(self):
        self.nodes = {}
    def add_node(self, node):
        self.nodes[node.name()] = node
    def add_edge(self, parent, child, dist):
        self.nodes[parent].add_child(self.nodes[child], dist)
    def get_roots(self):
        out = []
        for name, node in self.nodes.items():
            if not node.children:
                opposite = node.contig.num + ("+" if not node.forward else "-")
                out.append(self.nodes[opposite])
        return out
    def get_fasta(self):
        root = self.get_roots()[1]
        paths = root.get_sequence_paths()
        out = ""

        for path in paths:
            cov = 0
            seq = ""
            for node, dist in path:
                if dist < 0:
                    seq += node.seq[:dist]
                    cov += node.get_cov()
                else:
                    seq += "_"*dist + node.seq
                    cov += node.get_cov()
            out += ">" + GENE + " - " + str(cov / len(seq)) + " - " + str(hash(seq)) + "\n"
            out += seq + "\n"

        return out
    def __repr__(self):
        return str(self.nodes)

if __name__ == "__main__":
    GENE = sys.argv[1]
    sequence_path = sys.argv[2]
    graph_path = sys.argv[3]
    GLOBAL_D = 0
    local_d = None

    contigs = []

    with open(sequence_path, "r") as sequence_file:
        for line in sequence_file:
            contigs.append(Contig(line))
            contigs[-1].set_seq(next(sequence_file))

    graph = ContigGraph()

    with open(graph_path, "r") as graph_file:
        for i in range(3):
            line = next(graph_file).strip()
            if "[d=" in line:
                GLOBAL_D = int(line.split("[d=")[-1][:-1])
        for line in graph_file:
            if " -> " in line: #edge
                if " [d=" in line:
                    local_d = int(line.strip().split(" [d=")[1][:-1])

                names = line.strip().split(" [")[0]
                first, second = [e[1:-1] for e in names.split(" -> ")]

                if local_d is not None:
                    graph.add_edge(first, second, local_d)
                    local_d = None
                else:
                    graph.add_edge(first, second, GLOBAL_D)

            elif line.strip() != "}": #node
                raw_name, other = line.strip().rsplit(" [")
                num, forward = int(raw_name[1:-2]), raw_name[-2:-1]=="+"
                to_add = ContigNode(contigs[num], forward, other)
                graph.add_node(to_add)

    print(graph.get_fasta(), end="")
