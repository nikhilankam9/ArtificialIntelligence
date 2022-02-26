import random
import numpy as np
import mnist_loader

class Network(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            test_data=None):

        training_data = list(training_data)
        n = len(training_data)

        if test_data:
            test_data = list(test_data)
            n_test = len(test_data)

        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k+mini_batch_size] for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch_matrix(mini_batch, eta, mini_batch_size)
                # break
            if test_data:
                print("Epoch {} : {} / {}".format(j,self.evaluate(test_data),n_test))
            else:
                print("Epoch {} complete".format(j))

    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]

    def update_mini_batch_matrix(self, mini_batch, eta, mini_batch_size):
        nabla_B = []
        Biases = []
        for b in self.biases:
            temp = np.array(np.zeros(b.shape))
            for itr in range(mini_batch_size - 1):
                temp = np.append(temp, np.zeros(b.shape), axis=1)
            nabla_B.append(temp)

            temp1 = np.array(b)
            for itr in range(mini_batch_size - 1):
                temp1 = np.append(temp1, b, axis=1)
            Biases.append(temp1)

        nabla_W = [np.zeros(w.shape) for w in self.weights]

        X = None
        Y = None
        for x, y in mini_batch:
            if X is None and Y is None:
                X = np.array(x)
                Y = np.array(y)
            else:
                X = np.append(X, x, axis=1)
                Y = np.append(Y, y, axis=1)

        # feedforward
        activation = X
        activations = [X]
        zs = [] 
        for B, w in zip(Biases, self.weights):
            Z = np.dot(w, activation) + B
            zs.append(Z)
            activation = sigmoid(Z)
            activations.append(activation)

        # back propagate
        delta = self.cost_derivative(activations[-1], Y) * sigmoid_prime(zs[-1])
        nabla_B[-1] = delta
        nabla_W[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            Z = zs[-l]
            sp = sigmoid_prime(Z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_B[-l] = delta
            nabla_W[-l] = np.dot(delta, activations[-l-1].transpose())

        #Updating weights and biases
        self.weights = [w - (eta / mini_batch_size) * nw for w, nw in zip(self.weights, nabla_W)]

        nabla_b_sum = [np.zeros(b.shape) for b in self.biases]
        nabla_b_sum = [snb + dnb 
                        for nb in nabla_B 
                            for delta_nabla_b in nb 
                                for snb, dnb in zip(nabla_b_sum, delta_nabla_b)]
        self.biases = [b - (eta / mini_batch_size) * nb for b, nb in zip(self.biases, nabla_b_sum)]

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x] 
        zs = [] 
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        return (output_activations-y)

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

if __name__ == "__main__":
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

    net = Network([784, 30, 10])
    net.SGD(training_data, 1, 10, 1.0, test_data=test_data)
    