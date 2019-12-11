import numpy as np
from sklearn.datasets import make_blobs

class Node:
  def __init__(self, inputs = []):
      self.inputs = inputs

  def eval(self):
    return 1

  def run(self):
    return self.eval()

class Operation(Node):
  def __init__(self, inputs = []):
    super().__init__(inputs)

  def compute(self):
    return 1

  def calc_inputs(self):
    return list(map(lambda i: i.eval(), self.inputs))

  def eval(self):
    return self.compute()

class Add(Operation):
  def __init__(self, inputs= []):
    super().__init__(inputs)

  def compute(self):
    return np.sum(self.calc_inputs())


class Multiply(Operation):
  def __init__(self, inputs= []):
    super().__init__(inputs)

  def compute(self):
    return np.product(self.calc_inputs())

class MatrixMultiply(Operation):
  def __init__(self, inputs= []):
    super().__init__(inputs)

  def compute(self):
    values = self.calc_inputs()
    return np.array(values[0]).dot(np.array(values[1]))

class Variable(Node):
  def __init__(self, value, inputs = []):
    self.value = value
    super().__init__(inputs)

  def eval(self):
    return self.value


class Placeholder(Node):
  def __init__(self, inputs = []):
    super().__init__(inputs)

  def eval(self):
    return Placeholder.items[self]

class Sigmoid(Operation):
  def __init__(self, inputs =[]):
    super().__init__(inputs)
  
  def compute(self):
    print(self.calc_inputs())
    val = self.calc_inputs()[0]
    return 1 / (1 + np.exp(-val))
      
x = Placeholder()
z = Add([Multiply([Variable(10), x]), Variable(1)])

Placeholder.items = { x: 10}
print(z.run())

m1 = Variable([[1,2], [3, 4]])
m2 = Variable([[5,6], [7, 8]])

print(MatrixMultiply([m1, m2]).run())

data = make_blobs(n_samples=50, n_features=2, centers=2, random_state=75)


x = Placeholder()
w = Variable([1, 1])
b = Variable(-5)
z = Add([MatrixMultiply([w, x]), b])
a = Sigmoid([z])

Placeholder.items= {x: [8, 10]}
print(a.run())
