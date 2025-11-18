'''
1. Instancias

Tipos de Nodo :
FuentesNodos no-fuente

Tuberias (aristas):
Peso asociados, simbolizado la capacidad de la tuberia.

-Numero de nodos y aristas
-[NODES]: Listado de nodos. Cada uno contiene un id de nodo, sus coordenadas en x,
y y un numero booleano que indica si el nodo es una fuente o no.
-[EDGES]: Listado de aristas. Cada una esta formada por los ids de dos nodos 
y un tercer numero que representa su capacidad (diámetro).
-[OFFICE]: El id de un nodo donde se encuentra la oficina base. 
-[NEW]:  Una lista de nuevos nodos para ser agregados a la red. 
Por cada uno se indican sus coordenadas x,y, y el diámetro de la tubería que se usaría para conectarlo. Ninguno de los nodos nuevos es una fuente. 
'''





'''
2. Longitud de las tuberias

Utiliza las coordenadas x,y de cada nodo para calcular la distancia entre ellos.

Salidas: un listado de aristas, agregando la longitud a sus atributos preexistentes. 


'''



'''
3. Sectorizacion

En la division de la red en sectores asociados a cada fuente.

Los nodos deben ser suministrados por la fuente mas cercana, con respecto a la red. 
La separación entre sectores se consigue cerrando algunas tuberías. Determina cuales.
Debes reportar cuales nodos pertenecen al mismo sector, 
cuales tuberías quedan cerradas, y mostrarlo visualmente (grafico de colores, marcando las 
tuberías cerradas, estilo libre)

Salidas: lista cuales nodos pertenecen al mismo sector y cuales tuberías quedan cerradas. 
'''



'''
4. Frescura de agua

Una métrica de la calidad del agua es el tiempo que tarda en llegar de la fuente a un nodo. 
Esto es proporcional a la distancia de la fuente al nodo.

Salidas: Por cada sector, su fuente, nodo mas lejano y la longitud de esa distancia. 
'''


'''
5. Flujo maximo de cada sector
Utiliza la capacidad de las diferentes tuberías para determinar el flujo máximo de cada sector
Considera como
Origen: la fuente
Destino: el nodo mas alejado de la fuente

Salidas:  Por cada sector, sus nodos origen, destino, y flujo máximo. 
Además, por cada tubería (arista) del sector, cuanta de su capacidad se utiliza. Ej. 50 de 200.
'''


'''
6. Mustra de calidad de agua

Para analizar la calidad del agua, se deben tomar muestras de cada nodo.
Determina una ruta de distancia mínima para que una persona, ubicada 
en el nodo marcado como "office" visite toda la red tomando muestras y regrese.
Supón que puede hacerlo en un solo día, y que los patrones de las calles coinciden con las tuberías

Salidas: La secuencia de visita de los nodos, con la distancia de cada arista en el recorrido y el total de su suma. 
'''


'''
7. Expansion de la red
Suponiendo que se crea un nuevo nodo en
coordenadas especificas
¿Cómo se conectaría a la red? Enlaza el nuevo nodo al nodo mas cercano que no sea una fuente.
Después, actualiza la red apropiadamente

Se repiten los pasos 2, 3, 4, 5 y 6 para la nueva red.

Salidas: Las aristas nuevas del nodo, y su longitud. Para mostrar la actualización, crea dos archivos con el antes y el después. 
'''



'''
Coloca las salidas en dos archivos de texto (antes y después de agregar los nodos nuevos). Dale a estos archivos nombres que coincidan con el nombre las instancias de prueba.
Guarda las salidas de los puntos anteriores en un formato legible y ordenado, especificando a que punto corresponden y que datos se están mostrando.

Genera graficas donde se aprecien visualmente las salidas:

a) Los nodos, sus conexiones, longitudes, capacidades.
b) Cuales nodos son fuentes, nodos mas lejanos, cuales pertenecen al mismo sector. 
c) Cual es el recorrido del punto 6, la longitud de las aristas involucradas, y longitud total. 
e) La red actualizada con los nodos nuevos. 

Guarda las imágenes en archivos jpg o png. 


'''