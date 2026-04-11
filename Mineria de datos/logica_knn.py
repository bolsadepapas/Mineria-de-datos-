def obtener_k_vecinos(dataset, usuario_objetivo, metrica_func, k=5, es_distancia=True):
    resultados = []
    data_objetivo = dataset.get(usuario_objetivo)
    
    if not data_objetivo:
        return [] # Retorna lista vacía si no existe

    for otro_usuario, data_otro in dataset.items():
        if otro_usuario != usuario_objetivo:
            valor = metrica_func(data_objetivo, data_otro)
            
            # Filtramos si la distancia es infinita
            if valor != float('inf'):
                resultados.append((otro_usuario, valor))

    # Ordenamiento: Distancias (Ascendente), Similitudes (Descendente)
    resultados.sort(key=lambda x: x[1], reverse=not es_distancia)

    return resultados[:k]