# Get Started

## Graph Objects

There are several main building blocks for a graph: `Node`, `NodeSet`, `Edge`, `EdgeSet`, `Graph`. In this section, we will go over these concepts.

### `Node`
Every `Node` object has a unique id and a name. When the name of a node is not specified specifically, it is filled with it's id and a prefix. For `Node`, the default prefix is `n`. So the name of a node with id `1` is `n1`. Two `Node` instances are equal if and only if their ids are equal. Every `Node` instance has a `properties` field that collects all the properties this node has. The properties will be displayed once your mouse curser is hovered on the node.

Some magic methods are overriden so that you can use the basic operators llike `==` and `!=`. The equality follows the rules above. 

```python
# assume n1 and n2 are Node instances
n1 == n2	# if the id of n1 is equal to that of n2
n1 != n2 	# the negation of equality above
n1 > n2   	# if the id of n1 is bigger than n2
n1 < n2 	# if the id of n1 is smaller than n2
n1 >= n2
n1 <= n2
```

The representation string of a Node object is `Node(id: the_node_id)`.

### `NodeSet`
`NodeSet` describes a set of nodes. The elements in the set are unique. It is also not editable (for now). You can also use python native operators to get the relationships between `Node` and `NodeSet`. 

```python
# assume n1, n2, and n3 are Node instances; node_set is a NodeSet instance
# the ids of the three nodes are 1, 2, 3 respectively
# also, n1 and n3 are in node_set while n2 is not
len(node_set) == 2	# evaluated True
node_set[1] == n1	# evaluated True
n3 in node_set		# evaluated True
n2 not in node_set	# evaluated True
for node in node_set:
	print(node) 	# this will print Node(id: 1) and Node(id: 3)
					# on separated lines
print(node_set)		# print out [Node(id: 1), Node(id: 3)
```

### `Edge` 
`Edge` is like `Node` since every instance of `Edge` has a `id` and `name`. The same rules described above are also applied to `Edge`. The `properties` field is also present in `Edge`. It can be accessed using the same method. 

Naturally, instances of `Edge` also support native pyton operators. But there are more in `Edge`.

```python
# assuming n1, n2 and n3 are Node instances
# e1 is an Edge instance which is from n1 to n2
n1 in e1			# evaluated True
n3 in e1			# evaluated False
for node in edge:
	print(node) 	# this will print Node(id: 1) and Node(id: 2)
len(e1)				# is equal to 2 and does not make sense at all
```

The representation string of a Edge object is `Edge(id: the_edge_id)`

### `EdgeSet`

The `EdgeSet` is similiar to `NodeSet`. All the operators are supported. 

### `Graph`

The a `Graph` instance has a node set and an edge set which are represented by `NodeSet` and `EdgeSet`. You can access the node set by calling `graph.nodes` or `graph.V` assuming `graph` is a `Graph` instance. Similiarly, the edge set can be accessed by `graph.edges` or `graph.E`. 

```python
# assuming n1, n2, n3, and n4 are nodes in a graph named g1
# e1, e2, e3 are edges 
n1 in g1			# evaluated True
e1 in g1			# evaluated True
g1.empty()			# evaluated False since the graph is not empty
```


