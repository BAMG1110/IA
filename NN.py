import numpy as np

# cada neurona recibe n entradas, devuelve 1 salida
# capa de n neuronas
LR = 0.5

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        # matriz de tamaño n_inputs x n_neurons
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
    
    def backdrop(self, y, a1, a0):
        pd_C0 = (-2*(y - a1))[0]

        dw = a0

        db = 1
        
        da0 = []
        for i in range(len(a0)):
            # print(pd_C0, "\npd_c0\n")
            # print(self.weights[i], "\nweights\n")
            # print(self.weights[i] * pd_C0, "\nmult\n")
            da0.append(np.sum(self.weights[i] * pd_C0))

        # pesos
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                dco = (pd_C0[j] * dw[i]) * LR
                self.weights[i][j] = self.weights[i][j] - dco
        
        # biases
        for i in range(len(self.biases[0])):
            dco = pd_C0[i] * LR
            self.biases[0][i] = self.biases[0][i] - dco

        return da0

        

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