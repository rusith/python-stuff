import numpy as np

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

class Scaler(Node):
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


# z = Ax + b where A = 20, b = 2

x = Placeholder()
z = Add([Multiply([Scaler(10), x]), Scaler(1)])

Placeholder.items = { x: 10}
print(z.run())
