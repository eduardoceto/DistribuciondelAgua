'''
1. Instancias

Tipos de Nodo :
FuentesNodos no-fuente

Tuberias (aristas):
Peso asociados, simbolizado la capacidad de la tuberia.

'''


'''
2. Longitud de las tuberias

Utiliza las coordenadas x,y de cada nodo para calcular la distancia entre ellos.
'''



'''
3. Sectorizacion

En la division de la red en sectores asociados a cada fuente.

Los nodos deben ser suministrados por la fuente mas cercana, con respecto a la red. 
La separación entre sectores se consigue cerrando algunas tuberías. Determina cuales.
Debes reportar cuales nodos pertenecen al mismo sector, 
cuales tuberías quedan cerradas, y mostrarlo visualmente (grafico de colores, marcando las 
tuberías cerradas, estilo libre)
'''



'''
4. Frescura de agua

Una métrica de la calidad del agua es el tiempo que tarda en llegar de la fuente a un nodo. 
Esto es proporcional a la distancia de la fuente al nodo.
'''


'''
5. Flujo maximo de cada sector
Utiliza la capacidad de las diferentes tuberías para determinar el flujo máximo de cada sector
Considera como
Origen: la fuente
Destino: el nodo mas alejado de la fuente
'''


'''
6. Mustra de calidad de agua

Para analizar la calidad del agua, se deben tomar muestras de cada nodo.
Determina una ruta de distancia mínima para que una persona, ubicada 
en el nodo marcado como "office" visite toda la red tomando muestras y regrese.
Supón que puede hacerlo en un solo día, y que los patrones de las calles coinciden con las tuberías
'''


'''
7. Expansion de la red
Suponiendo que se crea un nuevo nodo en
coordenadas especificas
¿Cómo se conectaría a la red? Enlaza el nuevo nodo al nodo mas cercano que no sea una fuente.
Después, actualiza la red apropiadamente
'''