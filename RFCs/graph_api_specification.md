API Specification

General:

* all the members in a class should be provided getter and setters

`Comparable` Abstract Class:

* It should have an initializer that takes in an identity, which should be comparable, meaning it should support `__eq__`, `__neq__` and possibly `__hash__` functions. 
* It should support `__eq__`, `__neq__` and `__hash__` function. The hash function should be cached. 

`HasProperty` Abstract Class:

* It should have an initializer that takes in an dictionary or an `Iterable` of 2-tuples to initialize the property dictionary.

* It should have an initializer that allows users to specify the initial properties. It can be either a dictionary or a `Iterable` of 2-tuples. 

  ```python
  def __init__(self, init_properties: Union[Mapping, Iterable[Tuple]] = ()):
    self.properties = {}
    if isinstance(init_properties, Mapping):
      self.properties.update(init_properties)
    elif isinstance(init_properties, Iterable) and all(validator(element) element in init_properties):
      self.properties.update(init_properties)
    else:
      raise Exception
  ```

* It should support `setitem` and `getitem` operations so that users can use `instance[property_name]` to access the property. 

* It should support `contains` operation so that the one can check if a property exists in the instance It should support `get_properties` that returns either the dictionary or an iterator of tuples of key-value pair It should support `property_size` that returns the size of the current property dictionary 

`Stylable` Abstract class:

* It should have two class instance that contains the default styles and the default class name respectively so that the descendants of the class can override the default behavior.
* It should have two default validator that checks the validity of the input styles and the input classes 
* It should have an initializer that supports adding default styles and default classes. There should also be four keyword arguments that specify if the instance is going to use the default styles and classes and the style/class validators 

`Node` Object:

* Node object is **immutable** and the only identification is the `identity` field. 

* Node objects should implement all three abstract classes. 

* Node object should have an initializer that takes the `identity` of the node as positional argument and keyword arguments to add styles/classes and indicate if it’s going to use the default styles and classes. 

* It should supports `__str__` and `__repr__` function that gives proper string representation of the node. 

* The current proposal is `Node(id: ‘identifier’)`. 

* It should support recording neighbors and connected edges and getting the neighbors and connected edges. 

  - It should have a member variable named `neighbors` that records the reachable node of the node instance. The field is currently proposed to be a dictionary whose keys are node instances and values are sets of edges linking the two nodes together. That is 

    ```python
    self.neighbors = {
    	'node_1': {'edge_1', 'edge_2'},
    	'node_2': {'edge_3', 'edge_5'}
    }
    ```

  - It should have a member variable named `connected_edges` that records the reachable edges of the node instance. The field is currently proposed to be a set of edge instances.

    ```python
    self.connected_edges = {'edge_1', 'edge_2', 'edge_3', 'edge_5'}
    ```
  
* It should have a function named `add_neighbor` that takes in a node instance that’s going to be recorded in the `neighbors` field. `delete_neighbor` should be used to do the opposite, which is deleting a neighbor. 

  * `add_neighbor`

  ```python
  # ver_1 (should be obseleted)
  def add_neighbor(self, connected_edge: Edge, ):
  	node = next(iter(connected_edge))
    if node is not self:
    	node = next(iter(connected_edge))
    if node is not self:
    	raise Exception('Invalid Edge Specified')
    
    edge_set: Set[Edge] = self.neighbors.get(node, None)
    if edge_set is None:
    	edge_set = set()
    	self.neighbors[node] = edge_set
    
    if connected_edge not in edge_set:
    	edge_set.add(connected_edge)
    	self.add_connected_edge(connected_edge)
  ```

  ```python
  # ver_2: this func should only be called by `add_connected_edge`
  def add_neighbor(self, connected_edge: Edge):
    connected_node = connected_edge.get_next_node(self)
    if connected_node is None:
      return 
    	# or raise exception? 
    edge_set: Set[Edge] = self.neighbors.get(connected_node, None)
    if edge_set is None:
      edge_set = set()
      self.neighbors[node] = edge_set
    edge_set.add(connected_edge)
  ```

  * `delete_neighbor`

  ```python
  # ver_1
  def delete_neighbor(self, connected_edge: Edge):
    connected_node = connected_edge.get_next_node(self)
    if connected_node is None:
      return 
    	# or raise? 
  	edge_set: Set[Edge] = self.neighbors.get(connected_node, None)
    if edge_set is None or connected_edge not in edge_set:
    	raise Exception
    edge_set.remove(connected_edge)
    if len(edge_set) == 0:
      self.neighbors[connected_node] = None
  ```

  ```python
  # ver_2
  def delete_neighbor(self, connected_edge: Edge):
    if self not in connected_edge:
      return 
    connected_node = connected_edge.get_next(self)
    if connected_node is None:
      return 
    edge_set: Set[Edge] = self.neighbors.get(connected_node, None)
    if edge_set is None or connected_edge not in edge_set:
      return 
    edge_set.remove(connected_edge)
    if len(edge_set) == 0:
    	self.neighbors[connected_node] = None
  ```

* It should have a function named `add_connected_edge` that adds a new connected edge. And also `delete_connected_edge` to delete a connected edge 

  * `add_connected_edge`

    ```python
    # with ver_1 `add_neighbor` (should be obseleted)
    def add_connected_edge(self, connected_edge: Edge):
      self.connected_edges.add(connected_edge)
    ```

    ```python
    # with ver_2 `add_neighbor` 
    def add_connected_edge(self, connected_edge: Edge):
      if connected_edge in self.connected_edges:
        return 
      if self not in connnected_edge:
        raise Exception 
      self.add_neighbor(connected_edge)
      self.connected_edges.add(connected_edge)
    ```

  * `delete_connected_edge`

    ```python 
    # with ver_2 `delete_neighbor`
    def delete_connected_edge(self, connected_edge: Edge):
      if connected_edge not in self.connected_edges:
        return 
      self.connected_edges.remove(connected_edge)
      self.delete_neighbor(connected_edge)
    ```

`Edge` Object: 

* `Edge` object should __immutable__ and it should be identified by `identity` and the `directed` field. 

* `Edge` objects should implement all three abstract classes. 

* `Edge` objects should have `directed` field, which indicate if the edge is directed. 

* It should have an initializer that allows users to specify `identity`, `node_pair`, `directed` and styles/classes to initialize the abstract classes. 

  ```python
      def __init__(self, identity, node_pair: NodeTuple, name=None, directed=False,
                   styles: Union[str, Iterable[Mapping]] = (), classes: Iterable[str] = (),
                   add_default_styles=False, add_default_classes=False):
          """
          create an edge with an identity and a pair of nodes
          @param identity:
          @param node_pair:
          @param name:
          @param styles: the styles used on this edge
          @param classes: the class used on this edge
          @param directed: whether this edge is directed
          @raise KeyError: if there is some problem with the node pair
          """
          Comparable.__init__(self, identity, name)
          HasProperty.__init__(self)
          Stylable.__init__(
              self, [*styles, *(self.default_directed_styles if directed else ())], classes,
              add_default_styles=add_default_styles, add_default_classes=add_default_classes
          )
  
          if isinstance(node_pair, Tuple) and all(isinstance(node, Node) for node in node_pair):
              self.node_pair: NodeTuple = node_pair
          else:
              raise KeyError('%s is not a tuple or contains non-node element' % str(node_pair))
          self.directed: bool = directed
  ```

  

* `Edge` object should overload `__contains__` procedure such that it supports `node` membership query and property query. 

  ```python
  def __contains__(self, other: Union[Node, str]):
  	if isinstance(other, Node):
  		return other in self.node_pair
  	elif isinstance(other, str):
  		return other in self.properties 
  	else:
  		return False
  ```

* It should provide method to get the `n1` and `n2`. (Expect better naming)

  ```python
  def get_n1(self):
  	return self.node_pair[0]
  ```

  ```python
  def get_n2(self):
  	return self.node_pair[1]
  ```

* It should have a method that supports querying which node you can get from a given node. (Better naming for the function is expected)

  ```python
  def get_next(self, node: Node):
    if node not in self.node_pair:
      return None
    if node is self.node_pair[0]:
      return self.node_pair[1]
    else:
      if self.is_directed:
        return None
      else:
        return self.node_pair[1]
  ```

* The class should override the default style class so that corresponding edges can have directed-edge style, since it looks like the only way to make an edge look directed in Cytoscape is to have right styles. 

* It may support reverse for directed edges, but I think the use case is limited. 

`Graph` Object: 

* It is a mutable object. Although it can have immutable invariant. But the use case is limited. 

* It should inherit all three abstract classes. 

* It should have an initializer that takes in two positional arguments with default value `tuple()` for initial nodes and edges respectively. The two arguments should be `Iterable` of nodes and edges respectively. It can also takes two keyword arguments to specify the container type for nodes and edges. The containers should be the subclass of `ElementSet`. It can also takes in two keyword arguments to specify the initial styles and classes as well as two more to specify if the graph is going to use the default style set and class set. 

* It should override the default style list so that all graphs have a unified looks. The default style list should also contain a style sheet for directed edges, which should only works on the edges with directed style class specified. 

* It should support membership query for edges, nodes, and properties. It should also have individual procedures to query the membership of nodes and edges with either the instances of the corresponding classes or the identity. 

  ```python
  def __contains__(self, other: Union[str, Node, Edge]) -> bool:
    if isinstance(other, str):
      return other in self.properties
    elif isinstance(other, Node):
      return self.has_node(other)
    elif isinstance(other, Edge):
      return self.has_edge(other)
    else:
      return False
  ```

  ```python
  def has_node(self, node: Union[Node, str]) -> bool:
  	return node in self.node_set
  ```

  ```python
  def has_edge(self, edge: Union[Edge, str]) -> bool:
    return edge in self.edge_set
  ```

* It should have procedures that supports adding new nodes as well as deleting existing nodes. 

  ```python
  def add_node(self, identity: Union[Node, comparable], 
               default_styles=(), use_default_styles=False, 
               default_classes=(), use_default_classes=False, 
               init_properties=None):
    if identity in self.node_set:
      continue
      
    if isinstance(element, Node):
      node = element
    else:
      node = Node(element, default_styles, use_default_styles, default_classes, use_default_classes, init_properties)
  	self.node_set.add(node)
  ```
  
  ```python
  def delete_node(self, node_info: Union[Node, comparable]):
  	self.node_set.remove(element)
  ```

* It should also support adding new edges and deleting existing edges. There should be a keyword argument, `nodes_exist`, specifying whether the two nodes in the new edge have already existed in the graph. If it's set to `True` and one or both of the nodes do not exist, it should raise an error. If it's set to `False`, and the nonexistent node(s) will be automatically added to the graph (with every attribute set to default).
  
  ```python
  def add_edge(self, info: Union[Edge, Iterable[Union[comparable, Node]]], identity: str = None,
               nodes_exist: bool = True,
               default_styles=(), use_default_styles=False, 
               default_classes=(), use_default_classes=False, 
               init_properties=None):
    if identity in self.edge_set:
    	raise SomeException
    
    if isinstance(info, Edge):
      edge = info
      node_pair = edge.get_node_pair()
    else:
    	node_pair = self.edge_info_to_node_pair(info, not nodes_exist)
    	if any(node not in self.node_set for node in node_pair):
      	raise Exception
      
    	if identity is None:
        identity = self.identity_generator()
    
  	  edge = Edge(identity, node_pair, 
                  default_styles, use_default_styles, 
                  default_classes, use_default_classes, 
                  init_properties)
      
    self.connect_nodes_by_edge(edge)
    self.edge_set.add(edge)
  ```
  
  ```python
  def delete_edge(self, info: Union[Sequence[Union[str, Node]], Edge] = None, identity: str = None):
    if info is not None and (isinstance(info, Edge) or isinstance(info, Sequence)):
      edge = self.edge_set.get_edge(info)
    elif identity is not None:
      edge = self.edge_set.get_edge(info)
    else:
      raise  # or simply return 
    self.edge_set.remove(edge)
    self.disconnect_nodes_by_edge(edge)
  ```
  
* It should have procedures that support batch adding/deleting nodes and edges. 

  ```python
  def add_nodes_from(self, identities: Iterable[Node, Sequence[comparable, Mapping]]):
    if not validate(identities):
      # validator will be specified later
      return 
    
    for element in identites:
      if isinstance(element, Node):
  			self.add_node(element)
      else isinstance(element, Sequence):
        if len(element) == 2:
          self.add_node(element[0], **element[1])
        elif len(element) == 1:
          self.add_node(element[0])
        else:
          pass
  ```
  
  ```python
  def delete_nodes_from(self, inputs: Iterable[Node, comparable]):
    if not validate(inputs):
      return
    
    for element in inputs:
      self.delete_node(element)
  ```
