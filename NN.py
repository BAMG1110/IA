import numpy as np
import nnfs
from nnfs.datasets import spiral_data

# cada neurona recibe n entradas, devuelve 1 salida
# capa de n neuronas
class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        # matriz de tamaño n_inputs x n_neurons
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

# hace 0 los numeros negativos
class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

# toma los valores de salida y los traduce a valores entre el 0 y 1
class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        norm_values = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = norm_values

class Loss:
    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses)
        return data_loss

class Loss_catCrossEntropy(Loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7)

        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[range(samples), y_true]
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(y_pred_clipped*y_true, axis=1)

        negative_log = -np.log(correct_confidences)
        return negative_log

nnfs.init()
# set de datos con 10 sets de 2 valores (x, y) para 3 clases de datos
X, y = spiral_data(samples=10, classes=3)

capa_1 = Layer_Dense(2, 3)
capa_2 = Layer_Dense(3, 3)

act_1 = Activation_ReLU()
act_2 = Activation_Softmax()

loss_calc = Loss_catCrossEntropy()

# secuencia
capa_1.forward(X)
act_1.forward(capa_1.output)
capa_2.forward(act_1.output)
act_2.forward(capa_2.output)

loss = loss_calc.calculate(act_2.output, y)

print("X\n", X)
print("y\n", y)
print("capa_1\n", capa_1.output)
print("act_1\n", act_1.output)
print("capa_2\n", capa_2.output)
print("act_2\n", act_2.output)
print("loss\n", loss)