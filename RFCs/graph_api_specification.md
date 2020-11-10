API Specification

`Comparable` Abstract Class:

* It should have an initializer that takes in an identity, which should be comparable, meaning it should support `__eq__`, `__neq__` and possibly `__hash__` functions. 
* It should support `__eq__`, `__neq__` and `__hash__` function. The hash functio should be cached. 

`HasProperty` Abstract Class:

* It should have an initializer that takes in an dictionary or an iterable of 2-tuples to initialize the property dictionary.
* It should support `setitem` and `getitem` operations so that users can use `instance[property_name]` to access the property. 
* It should support `contains` operation so that the one can check if a property exists in the instance It should support `get_properties` that returns either the dictionary or an iterator of tuples of key-value pair It should support `property_size` that returns the size of the current property dictionary 

`Stylable` Abstract class:

* It should have two class instance that contains the default styles and the default class name respectively so that the descendants of the class can override the default behavior.
* It should have two default validator that checks the validity of the input styles and the input classes 
* It should have an initializer that supports adding default styles and default classes. There should also be four keyword arguments that specify if the instance is going to use the default styles and classes and the style/class validators 

`Node` Object:

* Node object is **immutable** and the only identification is the `identity` field. 

* It should support all the properties in the `Comparable` abstract class. Two node objects with the same `identity` are regarded as the same node. 

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
  def delete_neighbor(self, connected_node: Node):
  	edge_set: Set[Edge] = self.neighbors.get(connected_node, None)
    if edge_set is None:
    	return 
    	# or riase exception? 
    if len(edge_set) != 0:
      raise Exception('Unsafe removal')
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
    # 
    ```

`Graph` Object: 

* Support for adding nodes by specifying node 
