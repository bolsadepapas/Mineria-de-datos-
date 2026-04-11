import csv

# Logica de transformación de datos, a un estandar mas universal 
def cargar_dataset_inteligente(ruta_csv):
    dataset = {}
    
    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            encabezados = lector.fieldnames
            
            if not encabezados:
                return {}

            # Establecemos formatos a travez de los datos que encuentre en este caso establecemos el formato MovieLens (userId, movieId, rating)
            if 'userId' in encabezados and 'movieId' in encabezados and 'rating' in encabezados:
                for fila in lector:
                    usuario = fila['userId']
                    item = fila['movieId']
                    try:
                        nota = float(fila['rating'])
                        if usuario not in dataset:
                            dataset[usuario] = {}
                        dataset[usuario][item] = nota
                    except ValueError:
                        continue # Ignorar si la nota no es un número

            # Formato Música (Usuario, Item1)
            elif 'Usuario' in encabezados or 'usuario' in encabezados:
                col_usuario = 'Usuario' if 'Usuario' in encabezados else 'usuario'
                for fila in lector:
                    usuario = fila[col_usuario]
                    if usuario not in dataset:
                        dataset[usuario] = {}
                        
                    for item, valor in fila.items():
                        # Si la columna no es el nombre del usuario y tiene una nota
                        if item != col_usuario and valor.strip(): 
                            try:
                                dataset[usuario][item] = float(valor)
                            except ValueError:
                                pass # Ignoramos si alguien puso texto en vez de número
            else:
                print(f"Error: No se reconoce el formato de las columnas en {ruta_csv}")
                
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_csv}")
        
    return dataset