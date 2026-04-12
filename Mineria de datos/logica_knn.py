def obtener_k_vecinos(dataset, usuario_objetivo, metrica_func, k=3, es_distancia=True, min_coincidencias=2):
    resultados = []
    data_objetivo = dataset[usuario_objetivo]

    for usuario, data_otro in dataset.items():
        if usuario == usuario_objetivo:
            continue

        # Ahora la métrica devuelve (valor, coincidencias)
        valor, n_comunes = metrica_func(data_objetivo, data_otro)

        # --- FILTRO DE CREDIBILIDAD ---
        if n_comunes < min_coincidencias:
            continue # Ignoramos usuarios con poca base de datos común

        resultados.append({
            'usuario': usuario,
            'valor': valor,
            'n_comunes': n_comunes
        })

    # --- ORDENAMIENTO ROBUSTO ---
    # Si hay empate en distancia/similitud, priorizamos al que tiene más ítems en común
    if es_distancia:
        # Menor distancia primero, si empatan, mayor n_comunes primero
        resultados.sort(key=lambda x: (x['valor'], -x['n_comunes']))
    else:
        # Mayor similitud primero, si empatan, mayor n_comunes primero
        resultados.sort(key=lambda x: (-x['valor'], -x['n_comunes']))

    return resultados[:k]