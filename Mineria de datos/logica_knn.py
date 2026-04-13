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

# Fíjate que añadí 'es_distancia=False' al final de los parámetros
def generar_recomendaciones(dataset, usuario_objetivo, vecinos_cercanos, umbral=3.0, tope=5, min_vecinos=3, es_distancia=False):
    items_vistos_usuario = dataset.get(usuario_objetivo, {})
    if not items_vistos_usuario: return []
        
    promedio_objetivo = sum(items_vistos_usuario.values()) / len(items_vistos_usuario)
    candidatos = {} 

    for vecino_info in vecinos_cercanos:
        id_vecino = vecino_info['usuario']
        valor_metrica = vecino_info['valor'] 
        
        # --- EL FIX MAESTRO ---
        # Si calculaste con Euclidiana/Manhattan, lo convertimos a Similitud (1 / 1 + d)
        if es_distancia:
            similitud = 1 / (1 + valor_metrica)
        else:
            similitud = valor_metrica # Si fue Pearson/Coseno, se queda igual
            
        items_vecino = dataset.get(id_vecino, {})
        if not items_vecino: continue
            
        promedio_vecino = sum(items_vecino.values()) / len(items_vecino)

        for item, nota in items_vecino.items():
            if item not in items_vistos_usuario: 
                if item not in candidatos:
                    candidatos[item] = {'numerador': 0.0, 'denominador': 0.0, 'confianza': 0}
                
                # Usamos la 'similitud' corregida
                candidatos[item]['numerador'] += similitud * (nota - promedio_vecino)
                candidatos[item]['denominador'] += abs(similitud)
                candidatos[item]['confianza'] += 1
                
    recomendaciones_finales = []
    for item, datos in candidatos.items():
        if datos['denominador'] > 0 and datos['confianza'] >= min_vecinos:
            prediccion = promedio_objetivo + (datos['numerador'] / datos['denominador'])
            prediccion = max(1.0, min(5.0, prediccion))
            
            if prediccion >= umbral:
                recomendaciones_finales.append({
                    'item': item, 'prediccion': prediccion, 'confianza': datos['confianza']
                })
        
    recomendaciones_finales.sort(key=lambda x: (x['prediccion'], x['confianza']), reverse=True)
    return recomendaciones_finales[:tope]