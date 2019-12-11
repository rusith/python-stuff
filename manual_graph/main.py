import numpy as np

class Operation():
  def __init__(self, input_nodes=[]):
    self.input_nodes = input_nodes
    self.output_nodes = []

    for node in input_nodes:
      node.output_nodes.append(self)

    _default_graph.operations.append(self)

  def compute(self):
    pass

  def toSt(self, name):
    # inn = self.input_nodes
    return name

    # s = ', '.join(list(map(lambda a: str(a) + '', inn)))
    # return f'{name} {s}'

    
class Add(Operation):
  def __init__(self, x, y):
    super().__init__([x, y])
  
  def compute(self, x_var, y_var):
    self.inputs = [x_var, y_var]
    return x_var + y_var

  def __repr__(self):
    return self.toSt('Add')

class Multiply(Operation):
  def __init__(self, x, y):
    super().__init__([x, y])

  def compute(self, x_var, y_var):
    self.inputs = [x_var, y_var]
    return x_var * y_var

  def __repr__(self):
    return self.toSt('Multiply')

class MatMultiply(Operation):
  def __init__(self, x, y):
    super().__init__([x, y])

  def compute(self, x_var, y_var):
    self.inputs = [x_var, y_var]
    return x_var.dot(y_var)

  def __repr__(self):
    return self.toSt('MatMultiply')

class Graph():
  def __init__(self):
    self.operations = []
    self.placeholders = []
    self.variables = []
  
  def set_as_default(self):
    global _default_graph
    _default_graph = self

class Variable():
  def __init__(self, initial_value=None):
    self.value = initial_value
    self.output_nodes = []
    _default_graph.variables.append(self)

  def __repr__(self):
    return "Variable"

class Placeholder():
  def __init__(self):
    self.output_nodes = []
    _default_graph.placeholders.append(self)

  def __repr__(self):
    return "Placeholder"

def traverse_postorder(op):
  node_postorder = []
  def go(node):
    if isinstance(node, Operation):
      for input_node in node.input_nodes:
        go(input_node)
    node_postorder.append(node)
  
  go(op)
  return node_postorder

class Session():
  def run(self, operation, feed_dic= {}):
    nodes_postorder = traverse_postorder(operation)

    for node in nodes_postorder:
      if type(node) == Placeholder:
        node.output = feed_dic[node]
      elif type(node) == Variable:
        node.output = node.value
      else:
        node.inputs = [inn for inn in node.input_nodes]
        node.output = node.compute(*node.inputs)

      if type(node.output) == list:
        node.output = np.array(node.output)
    return operation.output

def main():
  g = Graph()
  g.set_as_default()
  A = Variable(10)
  b = Variable(1)
  x = Placeholder()

  y = Multiply(A, x)
  z = Add(y, b)

  l = traverse_postorder(z)
  print(l)

  s = Session()
  res = s.run(operation = z, feed_dic={x: 10})
  print(res)
if __name__ == '__main__':
  main()