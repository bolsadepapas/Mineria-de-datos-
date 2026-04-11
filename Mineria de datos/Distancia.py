## Los datos son los siguientes: 

usuarios = ["Angelica", "Bill", "Chan", "Dan", "Hailey", "Jordyn", "Sam", "Veronica"]

# Lista de artistas (columnas)
artistas = [
    "Blues Traveler", "Broken Bells", "Deadmau5", "Norah Jones",
    "Phoenix", "Slightly Stoopid", "The Strokes", "Vampire Weekend"
]

# Matriz de calificaciones (None representa "-")
datos = [
    [3.5, 2,   None, 4.5, 5,   1.5, 2.5, 2],   # Angelica
    [2,   3.5, 4,    None, 2,   3.5, None, 3], # Bill
    [5,   1,   1,    3,    5,   1,   None, None], # Chan
    [3,   4,   4.5,  None, 3,   4.5, 4,   2],  # Dan
    [None,4,   1,    4,    None,None,4,   1],  # Hailey
    [None,4.5, 4,    5,    5,   4.5,4,   4],  # Jordyn
    [5,   2,   None, 3,    5,   4,   5,   None], # Sam
    [3,   None,None, 5,    4,   2.5, 3,   None]  # Veronica
]


def raiz_cuadrada(valor):
    # Método de Newton (aproximación)
    x = valor
    for _ in range(20):  # iteraciones
        x = 0.5 * (x + valor / x)
    return x


def distancia_euclidiana(i, j, datos):
    suma = 0

    for k in range(len(datos[0])):
        
        if datos[i][k] is not None and datos[j][k] is not None:
            
            diferencia = datos[i][k] - datos[j][k]
            suma += diferencia * diferencia  # (x - y)^2

    return raiz_cuadrada(suma)
    
    
print("Usuarios disponibles:")
for u in usuarios:
    print("-", u)

u1 = input("Primer usuario: ")
u2 = input("Segundo usuario: ")

if u1 in usuarios and u2 in usuarios:
    i = usuarios.index(u1)
    j = usuarios.index(u2)

    d = distancia_euclidiana(i, j, datos)
    print("Distancia Euclidiana:", d)
else:
    print("Usuario no válido")