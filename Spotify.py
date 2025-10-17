import random
import numpy as np
from collections import defaultdict

# Base de datos expandida de canciones
canciones = {
    'song1': {'rock': 0.8, 'energia': 0.9, 'pop': 0.2, 'jazz': 0.1, 'baile': 0.3},
    'song2': {'pop': 0.9, 'energia': 0.6, 'rock': 0.3, 'jazz': 0.2, 'baile': 0.8},
    'song3': {'jazz': 0.7, 'energia': 0.4, 'rock': 0.1, 'pop': 0.3, 'baile': 0.2},
    'song4': {'rock': 0.6, 'energia': 0.8, 'pop': 0.4, 'jazz': 0.2, 'baile': 0.5},
    'song5': {'pop': 0.7, 'energia': 0.7, 'rock': 0.2, 'jazz': 0.3, 'baile': 0.6},
    'song6': {'jazz': 0.9, 'energia': 0.5, 'rock': 0.1, 'pop': 0.2, 'baile': 0.3},
    'song7': {'rock': 0.9, 'energia': 0.8, 'pop': 0.1, 'jazz': 0.1, 'baile': 0.4},
    'song8': {'pop': 0.8, 'energia': 0.5, 'rock': 0.4, 'jazz': 0.3, 'baile': 0.7},
    'song9': {'rock': 0.7, 'energia': 0.9, 'pop': 0.3, 'jazz': 0.2, 'baile': 0.6},
    'song10': {'pop': 0.6, 'energia': 0.8, 'rock': 0.5, 'jazz': 0.4, 'baile': 0.5}
}

# Matriz de feromonas inicial con valores más bajos para promover exploración
feromonas = defaultdict(lambda: defaultdict(lambda: 0.1))

def calcular_similitud(cancion1, cancion2):
    """Calcula similitud entre dos canciones usando similitud coseno"""
    caracteristicas = list(canciones[cancion1].keys())
    
    dot_product = sum(canciones[cancion1][car] * canciones[cancion2][car] for car in caracteristicas)
    norm1 = np.sqrt(sum(canciones[cancion1][car] ** 2 for car in caracteristicas))
    norm2 = np.sqrt(sum(canciones[cancion2][car] ** 2 for car in caracteristicas))
    
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

def calcular_afinidad(cancion, preferencias):
    """Calcula qué tan afín es una canción a las preferencias del usuario"""
    afinidad_total = 0
    total_peso = 0
    
    for caracteristica, peso_usuario in preferencias.items():
        if caracteristica in canciones[cancion]:
            afinidad_total += canciones[cancion][caracteristica] * peso_usuario
            total_peso += peso_usuario
    
    return afinidad_total / total_peso if total_peso > 0 else 0

class UsuarioHormiga:
    def __init__(self, preferencias, alpha=1.0, beta=2.0):
        self.playlist = []
        self.preferencias = preferencias
        self.alpha = alpha  # Peso de las feromonas
        self.beta = beta    # Peso de la heurística
        
    def evaluar_transicion(self, cancion_actual, siguiente_cancion):
        """Evalúa la probabilidad de transición entre canciones"""
        if cancion_actual == siguiente_cancion:
            return 0
            
        similitud = calcular_similitud(cancion_actual, siguiente_cancion)
        afinidad_usuario = calcular_afinidad(siguiente_cancion, self.preferencias)
        
        heuristica = similitud * afinidad_usuario
        
        # Fórmula con parámetros alpha y beta
        feromona_val = feromonas[cancion_actual][siguiente_cancion]
        return (feromona_val ** self.alpha) * (heuristica ** self.beta)
    
    def construir_playlist(self, longitud=5):
        """Construye una playlist usando reglas de transición"""
        canciones_disponibles = list(canciones.keys())
        
        # Primera canción: selección basada en afinidad con algo de aleatoriedad
        afinidades = [calcular_afinidad(c, self.preferencias) for c in canciones_disponibles]
        # Suavizar probabilidades para permitir exploración
        afinidades = [a + 0.1 for a in afinidades]  # Evitar ceros
        total_afinidad = sum(afinidades)
        probabilidades = [a/total_afinidad for a in afinidades]
        
        primera_cancion = np.random.choice(canciones_disponibles, p=probabilidades)
        self.playlist.append(primera_cancion)
        canciones_disponibles.remove(primera_cancion)
        
        # Construir el resto de la playlist
        for _ in range(longitud - 1):
            cancion_actual = self.playlist[-1]
            
            # Calcular probabilidades para cada canción disponible
            probabilidades = []
            for siguiente in canciones_disponibles:
                probabilidad = self.evaluar_transicion(cancion_actual, siguiente)
                probabilidades.append(max(probabilidad, 0.001))  # Mínimo para evitar ceros
            
            # Selección probabilística con ruido para exploración
            total = sum(probabilidades)
            if total > 0:
                probabilidades = [p/total for p in probabilidades]
                siguiente_cancion = np.random.choice(canciones_disponibles, p=probabilidades)
            else:
                siguiente_cancion = random.choice(canciones_disponibles)
            
            self.playlist.append(siguiente_cancion)
            canciones_disponibles.remove(siguiente_cancion)
        
        return self.playlist
    
    def evaluar_playlist(self):
        """Evalúa la calidad de la playlist construida - MEJORADA"""
        calidad_total = 0
        
        # Evaluar afinidad promedio (peso 60%)
        afinidad_promedio = sum(calcular_afinidad(c, self.preferencias) for c in self.playlist) / len(self.playlist)
        calidad_total += afinidad_promedio * 0.6
        
        # Evaluar transiciones suaves (peso 30%)
        similitud_transiciones = 0
        for i in range(len(self.playlist) - 1):
            similitud_transiciones += calcular_similitud(self.playlist[i], self.playlist[i + 1])
        similitud_promedio = similitud_transiciones / (len(self.playlist) - 1) if len(self.playlist) > 1 else 0
        calidad_total += similitud_promedio * 0.3
        
        # Bonus por diversidad de géneros (peso 10%)
        generos_unicos = set()
        for cancion in self.playlist:
            genero_principal = max(canciones[cancion].items(), key=lambda x: x[1] if x[0] != 'energia' else 0)[0]
            if genero_principal != 'energia':
                generos_unicos.add(genero_principal)
        diversidad = len(generos_unicos) / len(self.playlist)
        calidad_total += diversidad * 0.1
        
        return calidad_total

def actualizar_feromonas(hormigas, evaporacion=0.3, Q=2.0):
    """Actualiza las feromonas - MEJORADA con evaporación más agresiva"""
    # Evaporar feromonas más agresivamente
    for c1 in canciones:
        for c2 in canciones:
            if c1 != c2:
                feromonas[c1][c2] *= (1 - evaporacion)
                # Límite mínimo para feromonas
                feromonas[c1][c2] = max(feromonas[c1][c2], 0.01)
    
    # Reforzar feromonas de las mejores playlists con depósito proporcional
    hormigas_ordenadas = sorted(hormigas, key=lambda h: h.evaluar_playlist(), reverse=True)
    
    for i, hormiga in enumerate(hormigas_ordenadas):
        calidad = hormiga.evaluar_playlist()
        refuerzo = (Q * calidad) / (i + 1)  # Menor refuerzo para peores hormigas
        
        for j in range(len(hormiga.playlist) - 1):
            c1, c2 = hormiga.playlist[j], hormiga.playlist[j + 1]
            feromonas[c1][c2] += refuerzo
            feromonas[c2][c1] += refuerzo

# Algoritmo principal mejorado
def recomendar_playlist(preferencias_usuario, iteraciones=15, num_hormigas=8, alpha=1.0, beta=2.0):
    """Algoritmo principal"""
    mejor_playlist = None
    mejor_puntaje = -1
    historial_puntajes = []
    
    for iteracion in range(iteraciones):
        hormigas = []
        
        # Cada hormiga construye su playlist
        for _ in range(num_hormigas):
            hormiga = UsuarioHormiga(preferencias_usuario, alpha=alpha, beta=beta)
            playlist = hormiga.construir_playlist(longitud=5)
            puntaje = hormiga.evaluar_playlist()
            
            hormigas.append(hormiga)
            
            # Actualizar mejor playlist global
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_playlist = playlist.copy()
        
        # Actualizar feromonas para la siguiente iteración
        actualizar_feromonas(hormigas)
        
        historial_puntajes.append(mejor_puntaje)
        print(f"Iteración {iteracion + 1}: Mejor puntaje = {mejor_puntaje:.3f}")
        
        # Reinicio parcial si no hay mejora en 3 iteraciones
        if iteracion > 3 and len(set(historial_puntajes[-3:])) == 1:
            print("  -> Reiniciando feromonas para exploración...")
            for c1 in canciones:
                for c2 in canciones:
                    if c1 != c2:
                        feromonas[c1][c2] = 0.1
    
    return mejor_playlist, mejor_puntaje, historial_puntajes

# Función para mostrar análisis detallado
def analizar_playlist(playlist, preferencias):
    print("\n" + "="*50)
    print("ANÁLISIS DETALLADO DE LA PLAYLIST")
    print("="*50)
    
    afinidad_total = 0
    similitud_total = 0
    
    print("\n Canciones en la playlist:")
    for i, cancion in enumerate(playlist, 1):
        afinidad = calcular_afinidad(cancion, preferencias)
        afinidad_total += afinidad
        print(f"{i}. {cancion} - Afinidad: {afinidad:.3f}")
        print(f"   Características: {canciones[cancion]}")
    
    print(f"\n Afinidad promedio: {afinidad_total/len(playlist):.3f}")
    
    print("\n Transiciones entre canciones:")
    for i in range(len(playlist) - 1):
        similitud = calcular_similitud(playlist[i], playlist[i + 1])
        similitud_total += similitud
        print(f"   {playlist[i]} → {playlist[i+1]}: {similitud:.3f}")
    
    print(f"\n Similitud promedio en transiciones: {similitud_total/(len(playlist)-1):.3f}")

# Ejemplo de uso mejorado
if __name__ == "__main__":
    # Preferencias de ejemplo del usuario
    preferencias_usuario = {'rock': 0.9, 'energia': 0.8, 'pop': 0.3}
    
    print("Buscando la mejor playlist (algoritmo mejorado)...")
    playlist_recomendada, puntaje, historial = recomendar_playlist(
        preferencias_usuario, 
        iteraciones=15, 
        num_hormigas=8,
        alpha=1.0, 
        beta=2.0
    )
    
    print(f"\n Playlist recomendada (puntaje: {puntaje:.3f}):")
    for i, cancion in enumerate(playlist_recomendada, 1):
        print(f"{i}. {cancion}")
    
    # Análisis detallado
    analizar_playlist(playlist_recomendada, preferencias_usuario)
    
    # Mostrar evolución del algoritmo
    print(f"\nEvolución del puntaje: {[f'{p:.3f}' for p in historial]}")