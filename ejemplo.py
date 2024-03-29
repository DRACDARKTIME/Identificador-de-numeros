import mnist_loader
import network
import pickle

training_data, validation_data , test_data = mnist_loader.load_data_wrapper()

training_data = list(training_data)
test_data = list(test_data)

net=network.Network([784,30,10])

net.Adam( training_data, epochs=30, mini_batch_size=10, eta=0.5, test_data=test_data)

archivo = open("red_prueba1.pkl",'wb')
pickle.dump(net,archivo)
archivo.close()
exit()
#leer el archivo

archivo_lectura = open("red_prueba.pkl",'rb')
net = pickle.load(archivo_lectura)
archivo_lectura.close()

net.SGD( training_data, epochs=10, mini_batch_size=50, eta=0.5, test_data=test_data)

archivo = open("red_prueba.pkl",'wb')
pickle.dump(net,archivo)
archivo.close()
exit()

#esquema de como usar la red :
imagen = leer_imagen("disco.jpg")
print(net.feedforward(imagen))
