"""
network.py
~~~~~~~~~
A module to implement the stochastic gradient descent learning
algorithm for a feedforward neural network.  Gradients are calculated
using backpropagation.  Note that I have focused on making the code
simple, easily readable, and easily modifiable.  It is not optimized,
and omits many desirable features.
"""

#-------- Libraries --------#

import random
    # Standard library

import numpy as np
    # Third-party libraries

#-------- Definición de la Red Neuronal  --------#

class Network(object):

    def __init__(self, sizes):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.
        Note that the first layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        self.num_layers = len(sizes) #Numero de capas
        self.sizes = sizes #Creamos un atributo 'sizes' a self 
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]] 
            #Creamos un atributo 'biases' a self, donde asignamos una lista
            #Esta lista tiene como elementos a arrays,
                #cada array pertenece a una capa de la red, sin contar la capa de input
            #Cada array tiene una 'b' random para cada neurona de cada capa  
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
            #Ahora asignamos un peso w aleatorio --entre cada par-- de neuronas 
            #Se crea un primer array con los pesos que unen a cada neurona entre la capa uno y dos
                #En este array hay otros array con n valores, esos valores corresponden a los w's
                #Que tiene cada nuerona de la segunda capa a la primer capa.
            #Se crea un segundo array con los pesos que unen a cada neurona entre la capa dos y tres
            #El ciclo se repite   
            #         .
            #         .
            #         .
            #Hasta que se alcanza a la última capa.
        
            #------Ejemplo para sizes =[2,3,1]-------
        
            #self.weights = [array_0([ [w^{1}_{11}, w^{1}_{12}],
            #                          [w^{1}_{21}, w^{1}_{22}],
            #                          [w^{1}_{31}, w^{1}_{32}]  ]),     "Estas son las w's que unen la capa 
            #                                                                      input y la intermedia"
        
            #               array_1([ [w^{2}_{11},w^{2}_{12},w^{2}_{13}]  ]) ]  "Estas son las w's que unen
            #                                                                   la capa intermedia y output"            

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input.""" #La entrada 'a' debe ser un vector columna, de la misma
                                                                    #longitud que el primer valor de size.
        for b, w in zip(self.biases, self.weights): #Tomamos un valor de self.biases y self.weights (son arrays)
            a = sigmoid(np.dot(w, a)+b) #a^{l}_{j} = \sigma( w^{l}_{jk} * a^{l-1}_{k} + b^{l}_{j}  ) suma implicita en k
                                        #Hace el producto matricial entre las entradas de la capa input a^{0} y w^{1}, despues
                                            #lo evalua en la sigmoide creando una nueva a, a^{1} (es un array)
                                            #después se vuelve a calcular lo mismo pero para la siguiente a^{2}
                                        #El ciclo se repite hasta tener la activación final
        return a                        #Regresa la activación final de la red.
#-----------------------No se modifica lo de arriba (en Adam)---------------------

    def Adam(self, training_data, epochs, mini_batch_size, eta,
            test_data=None, beta_1=0.9, beta_2=0.95):  #-------Stochastic Gradient Descent-------
                              #self            --- Llamamos a nuestra clase 'self'
                              #training_data   --- Una lista de tuplas (x,y) donde ('espectativa','realidad') xd  
                              #epochs          --- Ciclos a repetir
                              #mini_batch_size --- Es el paso que hay en la selección de los datos "step"
                              #eta             --- Ritmo de aprendizaje
                              #test_data       --- Información de prueba  
        epsilon = 1e-8
        t=0
        g=0
        m_b=np.zeros_like(self.biases)
        v_b=np.zeros_like(self.biases)
        m_w=np.zeros_like(self.weights)
        v_w=np.zeros_like(self.weights)
        delta_nabla_b, delta_nabla_w = self.backprop(x, y)

        #Para b's
        for j in range(1000):
            m_b = beta_1*m_b + (1-beta_1)*delta_nabla_b
            v_b = beta_2*v_b + (1-beta_2)*delta_nabla_b**2
            m_b_hat = m_b/(1-beta_1**t)
            v_b_hat = v_b/(1-beta_2**t)
            theta_b = theta_b - eta*m_b_hat/(np.sqrt(v_b_hat)+epsilon) 
        #Para w's    
        for j in range(1000):
            m_w = beta_1*m_w + (1-beta_1)*delta_nabla_w
            v_w = beta_2*v_w + (1-beta_2)*delta_nabla_w**2
            m_w_hat = m_w/(1-beta_1**t)
            v_w_hat = v_b/(1-beta_2**t)
            theta_w = theta_w - eta*m_w_hat/(np.sqrt(v_w_hat)+epsilon) 

        if test_data:
            test_data = list(test_data) #La convertimos en lista
            n_test = len(test_data)     #Obtenemos su longitud

        training_data = list(training_data) #La convertimos en lista
        n = len(training_data)              #Obtenemos su longitud
        for j in range(epochs):
            random.shuffle(training_data)   #Revolvemos el orden de los datos en training_data

            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)] #Se crean los subconjuntos de training_data
                                                       #De tamaño = n/mini_batch_size
                                                       #mini_batch_size es el step de 0 a n

            for mini_batch in mini_batches:             #mini_batch es un elemento de mini_batches
                self.update_mini_batch(mini_batch, eta) #Llamamos a la función update_mini_batch (definida abajo)
                                                        #La cual nos mueve un poco los pesos y los biases
            if test_data:
                print("Epoch {0}: {1} / {2}".format(
                    j, self.evaluate(test_data), n_test)) #Imprimimos el número de época en que estamos,
                                                          #el valor de evaluate(función definida abajo) y
                                                          #la longitud de test_data
            else:
                print("Epoch {0} complete".format(j))     #Solo se imprime la epoca en que se está

    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``eta``
        is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]     #Crea una lista igual a self.biases pero con puros ceros
        nabla_w = [np.zeros(w.shape) for w in self.weights]    #Crea una lista igual a self.weights pero con puros ceros
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)            #Regresa el gradiente de la función de costo respecto de b y de a
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)] #Ahora nabla_b está llena de la suma de los valores
                                                                          #nabla_b + delta_nabla_b
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)] #Ahora nabla_w está llena de la suma de los valores
                                                                          #nabla_w + delta_nabla_w
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]          #Actualizamos los pesos, moviendo un poco los w's
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]            #Actualizamos los biases, moviendo un poco los b's

#-------------------------De aquí para abajo no se modifica----------------------------
    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]       #Crea una lista igual a self.biases pero con puros ceros
        nabla_w = [np.zeros(w.shape) for w in self.weights]      #Crea una lista igual a self.weights pero con puros ceros
        #-----feedforward------
        activation = x    #Input
        activations = [x] #list to store all the activations, layer by layer  Valores de sigma
        zs = []           #list to store all the z vectors, layer by layer              
        for b, w in zip(self.biases, self.weights):     
            z = np.dot(w, activation)+b                   
            zs.append(z)                      #Añadimos elementos a zs
            activation = sigmoid(z)
            activations.append(activation)    #Añadimos elementos a activations
            #zs es una lista donde guardamos todas las z's de nuestra red
            #activations es una lista donde guardamos todas las a's de nuestra red

        #-----backward pass-----
        delta = self.cost_derivative(activations[-1], y)                #Calculamos la ultima delta usando Cross-entropy
                                                                        #  $\delta^{L} = a^{L} - y$                                                                               
        nabla_b[-1] = delta                                             #El último dato de nabla_b 
                                                                        #lo cambiamos por delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())        #Cambiamos el último dato de w,
                                                                        #usando la nueva b

        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        
        #Es lo mismo que arriba pero ya para todos los valores
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp   
        #       \delta^{l-1} = [ (w^{l})^{T} * \delta^{l} ]*\sigma^{'}(z^{l-1})
            nabla_b[-l] = delta
        #       \frac{\partial C}{\partial b^{l}_{j}} = \delta^{l}_{j}
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        #       \frac{\partial C}{\partial w^{l}_{jk}} = a^{l-1}_{k}*\delta^{l}_{j}
        return (nabla_b, nabla_w)    #Hemos actualizado todos los valores de nabla_b y nabla_w

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]           #Es una lista de tuplas (f,y) donde f es 
                                                           #el indice de x de la primer activación más grande.
                                                           #y es el indice correcto.
        
        return sum(int(x == y) for (x, y) in test_results) #Nos da la cantidad de datos que coincidieron, 
                                                           #Simplemento compara los indices y cuenta los que sí coinciden.

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)  #Esta es la ultima delta usando Cross-Entropy

#------------ Miscellaneous functions ------------#

def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))
