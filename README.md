# Taller 2 IA
* Yefri Stiven Barrero Solano - 2320392

# Optimización de Pokémon usando Algoritmo Genético

El código `Pokemon.py` implementa un **algoritmo genético** para optimizar las características de Pokémon, simulando un proceso evolutivo que mejora progresivamente sus atributos de combate. El sistema busca encontrar la combinación óptima de estadísticas y tipos para maximizar el poder de combate de estas criaturas virtuales.

## Fundamentos de los Algoritmos Genéticos

### Conceptos Básicos
Los algoritmos genéticos son técnicas de optimización inspiradas en la evolución natural, que aplican principios de selección, cruce y mutación para mejorar soluciones a lo largo de generaciones sucesivas.

### Aplicación al Mundo Pokémon
- **Individuos**: Pokémon con características únicas
- **Población**: Conjunto de Pokémon coexistiendo
- **Generaciones**: Iteraciones del proceso evolutivo
- **Fitness**: Poder de combate calculado

## Sistema de Características Pokémon

### Atributos Numéricos
Cada Pokémon posee cuatro atributos principales, normalizados entre 0 y 1:

- **Ataque**: Capacidad ofensiva en combate
- **Defensa**: Capacidad para resistir daño
- **Velocidad**: Orden de turno en batalla
- **Vida**: Puntos de resistencia vital

### Sistema de Tipos Elementales
- **Fuego**: Bonus ×1.1 - Ofensivo poderoso
- **Agua**: Bonus ×1.05 - Balanceado
- **Planta**: Bonus ×1.0 - Base neutral
- **Eléctrico**: Bonus ×1.08 - Veloz y efectivo

## Implementación del Algoritmo Evolutivo

### 1. Inicialización de Población
```python
def crear_pokemon():
    # Genera Pokémon con stats aleatorios y tipo elemental
```

Crea una población diversa inicial con combinaciones aleatorias de atributos y tipos.

### 2. Función de Evaluación (Fitness)
```python
def evaluar_pokemon(pokemon):
    # Calcula poder combinando stats con bonus de tipo
```

**Fórmula del poder:**
```
Poder = (Ataque×0.3 + Defensa×0.2 + Velocidad×0.25 + Vida×0.25) × Bonus_tipo
```

### 3. Selección de Padres
```python
def seleccionar_padres(poblacion):
    # Selecciona los 2 Pokémon más poderosos
```

Estrategia elitista que favorece a los individuos con mayor fitness para la reproducción.

### 4. Operador de Cruce
```python
def cruzar(padre1, padre2):
    # Combina características de ambos padres
```

- **Cruza uniforme**: Cada stat se hereda aleatoriamente de uno de los padres
- **Herencia de tipo**: El tipo elemental se elige aleatoriamente entre los padres

### 5. Operador de Mutación
```python
def mutar(pokemon):
    # Introduce variaciones aleatorias
```

- **Mutación de stats**: Modifica atributos con distribución normal
- **Cambio de tipo**: Alterna el tipo elemental con probabilidad definida
- **Preservación de límites**: Stats se mantienen entre 0 y 1

## Parámetros del Sistema Evolutivo

### Configuración Principal
- **Tamaño de población**: 10 Pokémon
- **Generaciones**: 5 ciclos evolutivos
- **Tasa de mutación**: 20% de probabilidad
- **Presión selectiva**: Los 2 mejores se reproducen

### Pesos de Evaluación
- **Ataque**: 30% - Énfasis en capacidad ofensiva
- **Defensa**: 20% - Importancia defensiva moderada
- **Velocidad**: 25% - Valor táctico significativo
- **Vida**: 25% - Resistencia vital importante

## Sistema de Visualización y Análisis

### Métricas Seguidas
- **Poder máximo**: Mejor individuo por generación
- **Poder promedio**: Calidad general de la población
- **Evolución de stats**: Progreso de atributos individuales
- **Distribución de tipos**: Variación elemental en la población

### Gráficos Generados
1. **Evolución del Poder**
   - Tendencia del mejor poder
   - Evolución del poder promedio
   - Brecha entre élite y población general

2. **Evolución de Stats Promedio**
   - Progreso individual de cada atributo
   - Balance entre características ofensivas y defensivas
   - Identificación de stats dominantes

## Análisis del Proceso Evolutivo

### Dinámica Poblacional
- **Convergencia**: Tendencia hacia soluciones óptimas
- **Diversidad genética**: Mantenida mediante mutación
- **Presión selectiva**: Fuerza que dirige la evolución

### Estrategias Emergentes
- **Especialización**: Pokémon que optimizan stats específicos
- **Balance**: Distribución equitativa de características
- **Adaptación**: Preferencia por tipos con mejores bonus

## Mecánicas de Combate Simuladas

### Sistema de Bonus por Tipo
Los tipos elementales introducen variación estratégica:
- **Fuego**: Alto riesgo/recompensa
- **Eléctrico**: Balance ofensivo
- **Agua**: Versatilidad confiable
- **Planta**: Enfoque equilibrado

### Meta-Estrategias
- **Optimización local**: Mejora progresiva dentro del espacio de búsqueda
- **Exploración vs Explotación**: Balance entre variedad y refinamiento
- **Resistencia a estancamiento**: Mutaciones evitan óptimos locales

# Sistema de Recomendación de Playlists usando Colonia de Hormigas

El código `Spotify.py` implementa un **sistema de recomendación inteligente** para generar playlists musicales personalizadas utilizando el algoritmo de **Optimización por Colonia de Hormigas (ACO)**. El sistema simula el comportamiento colectivo de hormigas virtuales que exploran el espacio de canciones para encontrar secuencias óptimas basadas en las preferencias del usuario.

## Fundamentos del Algoritmo de Colonia de Hormigas

### Inspiración Biológica
El algoritmo se basa en el comportamiento real de las hormigas, que depositan feromonas para marcar caminos hacia fuentes de alimento. Las hormigas siguen preferentemente rutas con mayor concentración de feromonas, creando un sistema de inteligencia colectiva.

### Aplicación a Recomendaciones Musicales
- **Hormigas**: Usuarios virtuales que exploran combinaciones de canciones
- **Feromonas**: Rastros que indican transiciones exitosas entre canciones
- **Alimento**: Playlists de alta calidad que satisfacen preferencias

## Modelo de Datos Musicales

### Caracterización de Canciones
Cada canción se representa mediante un vector de características normalizadas:

```python
'song1': {'rock': 0.8, 'energia': 0.9, 'pop': 0.2, 'jazz': 0.1, 'baile': 0.3}
```

### Sistema de Preferencias del Usuario
Las preferencias se modelan como pesos para diferentes características:
```python
preferencias_usuario = {'rock': 0.9, 'energia': 0.8, 'pop': 0.3}
```

## Componentes del Algoritmo

### 1. Cálculo de Similitud entre Canciones
```python
def calcular_similitud(cancion1, cancion2):
    # Usa similitud coseno para medir proximidad musical
```

**Fórmula**: Similitud Coseno entre vectores de características

### 2. Cálculo de Afinidad con el Usuario
```python
def calcular_afinidad(cancion, preferencias):
    # Calcula compatibilidad con preferencias del usuario
```

Combina características de la canción con pesos de preferencia

### 3. Clase UsuarioHormiga
Simula el comportamiento de un usuario explorando canciones:

#### Construcción de Playlist
```python
def construir_playlist(self, longitud=5):
    # Construye secuencias usando reglas probabilísticas
```

#### Evaluación de Transiciones
```python
def evaluar_transicion(self, cancion_actual, siguiente_cancion):
    # Combina feromonas y heurística para decisiones
```

**Fórmula de Transición**:
```
Probabilidad = (Feromonas^α) × (Heurística^β)
```

### 4. Sistema de Feromonas
```python
def actualizar_feromonas(hormigas, evaporacion=0.3, Q=2.0):
    # Actualiza rastros basado en calidad de playlists
```

**Mecanismos**:
- **Evaporación**: Reduce feromonas antiguas (30% por iteración)
- **Refuerzo**: Añade feromonas en caminos exitosos
- **Límites**: Mínimo de 0.01 para mantener exploración

## Métricas de Calidad de Playlist

### Función de Evaluación Mejorada
```python
def evaluar_playlist(self):
    # Evalúa múltiples dimensiones de calidad
```

#### Componentes de Evaluación:
1. **Afinidad con Usuario** (60%): Alineamiento con preferencias
2. **Suavidad de Transiciones** (30%): Coherencia musical entre canciones consecutivas
3. **Diversidad de Géneros** (10%): Variedad en la playlist

### Sistema de Pesos Adaptativo
- **Afinidad**: Prioridad máxima para satisfacer al usuario
- **Transiciones**: Importancia alta para experiencia de escucha fluida
- **Diversidad**: Bonus por variedad musical

## Parámetros y Configuración

### Parámetros del Algoritmo
- **Iteraciones**: 15 ciclos de optimización
- **Hormigas por iteración**: 8 agentes exploradores
- **Longitud de playlist**: 5 canciones
- **α (Alpha)**: 1.0 - Influencia de feromonas
- **β (Beta)**: 2.0 - Influencia de heurística

### Mecanismos de Control
- **Evaporación agresiva**: 30% para evitar convergencia prematura
- **Reinicio adaptativo**: Reseteo de feromonas tras 3 iteraciones sin mejora
- **Exploración forzada**: Mínimos probabilísticos para evitar ceros

## Proceso de Optimización

### Fases del Algoritmo

#### 1. Inicialización
- Creación de matriz de feromonas inicial
- Configuración de parámetros de búsqueda

#### 2. Bucle Principal por Iteraciones
```python
for iteracion in range(iteraciones):
    # Construcción de playlists por hormigas
    # Evaluación y selección de mejores
    # Actualización de feromonas
```

#### 3. Estrategias de Mejora
- **Selección por ranking**: Mejores hormigas refuerzan más feromonas
- **Elitismo implícito**: Siempre se mantiene la mejor solución global
- **Balance exploración-explotación**: Parámetros calibrados para ambos

## Análisis y Visualización

### Sistema de Monitoreo
```python
def analizar_playlist(playlist, preferencias):
    # Proporciona análisis detallado de la playlist generada
```

# Sistema de Control Inteligente para Robot de Carreras con Algoritmos Bio-Inspirados

El código `Controlador.py` implementa un **sistema de control inteligente integrado** para un robot de carreras autónomo que combina tres algoritmos bio-inspirados diferentes para optimizar el rendimiento en pista. El sistema utiliza evolución genética, inteligencia de enjambre y aprendizaje por refuerzo basado en feromonas para tomar decisiones tácticas en tiempo real.

## Arquitectura del Sistema

### Sistema de Control de Tres Capas

#### 1. **Evolución Genética (Largo Plazo)**
- Optimiza parámetros base del controlador entre generaciones
- Aprende estrategias generales de conducción

#### 2. **Optimización por Enjambre de Partículas (Corto Plazo)**
- Toma decisiones tácticas en tiempo real durante la carrera
- Adapta el comportamiento según condiciones inmediatas

#### 3. **Algoritmo de Hormigas (Medio Plazo)**
- Aprende trayectorias óptimas en la pista
- Refuerza líneas de conducción efectivas

## Componentes del Sistema

### 1. Algoritmo Genético - `GeneticoControlador`

#### Propósito
Evoluciona los parámetros base de conducción a lo largo de múltiples generaciones de carreras.

#### Parámetros Evolucionados
```python
{
    'agresividad': 0.5-1.0,      # Tendencia a tomar riesgos
    'conservador': 0.1-0.5,      # Preferencia por seguridad
    'adelantamiento': 0.6-1.0     # Propensión a adelantar
}
```

#### Mecanismos de Evolución
- **Población**: 50 individuos
- **Selección**: Elitismo (conservar los 10 mejores)
- **Cruce**: Uniforme entre padres seleccionados
- **Mutación**: 10% de probabilidad con distribución normal

### 2. Optimización por Enjambre de Partículas - `ControladorPSO`

#### Propósito
Toma decisiones tácticas en tiempo real durante la carrera.

#### Espacio de Búsqueda 3D
1. **Distancia de seguridad** (0.5-2.5 metros)
2. **Ángulo de ataque** (-15° a +15°)
3. **Momento de adelantamiento** (decisión binaria)

#### Parámetros PSO
```python
inercia = 0.7      # Conservación de velocidad anterior
cognitivo = 1.5    # Influencia de mejor posición personal
social = 1.5       # Influencia de mejor posición global
```

### 3. Algoritmo de Hormigas - `HormigaRacing`

#### Propósito
Aprende y refuerza las trayectorias óptimas en diferentes tramos de la pista.

#### Mecanismo de Feromonas
- **Refuerzo positivo**: Mejores tiempos fortalecen feromonas
- **Evaporación**: 5% de reducción por actualización
- **Selección probabilística**: Decisiones basadas en concentración de feromonas

## Flujo de Integración

### Inicialización del Sistema
```python
controlador_robot = ControladorRobotCarreras(num_tramos_pista=20)
```

### Ciclo de Carrera
1. **Selección de Estrategia Base**
   - Mejor individuo del algoritmo genético
   - Parámetros de agresividad y estilo de conducción

2. **Ejecución en Pista**
   - Toma de decisiones tácticas con PSO
   - Aprendizaje de trayectorias con algoritmo de hormigas
   - Actualización en tiempo real

3. **Evolución Post-Carrera**
   - Evaluación de desempeño
   - Actualización de población genética
   - Incremento de generación

## Sistema de Toma de Decisiones

### Decisión de Adelantamiento
```python
def decidir_adelantamiento(self, oponente: Dict, pista: Dict) -> Dict:
```

#### Factores Considerados
- **Posición y velocidad del oponente**
- **Ancho y curvatura de la pista**
- **Parámetros evolucionados del conductor**
- **Evaluación de múltiples estrategias via PSO**

#### Salida de la Decisión
```python
{
    'distancia_seguridad': 1.8,      # metros
    'angulo_ataque': 12.5,           # grados
    'momento_adelantamiento': True   # decisión booleana
}
```

### Función de Evaluación de Estrategias
```python
def _evaluar_estrategia(self, particula: np.ndarray, oponente: Dict, pista: Dict) -> float:
```

#### Componentes del Score
- **Seguridad** (30%): Distancia óptima al oponente
- **Eficiencia** (40%): Ángulo de ataque ponderado por agresividad
- **Oportunidad** (30%): Momento óptimo basado en tendencia a adelantar

## Aprendizaje y Adaptación

### Aprendizaje Multi-Nivel

#### 1. **Aprendizaje Evolutivo (Genes)**
- Mejora parámetros base entre generaciones
- Tiempo escala: múltiples carreras
- Enfoque: estrategias generales de conducción

#### 2. **Aprendizaje por Refuerzo (Feromonas)**
- Optimiza trayectorias específicas de la pista
- Tiempo escala: durante la carrera
- Enfoque: líneas de conducción óptimas

#### 3. **Aprendizaje por Enjambre (PSO)**
- Adaptación táctica inmediata
- Tiempo escala: segundos/milisegundos
- Enfoque: decisiones de overtaking

### Mecanismos de Actualización

#### Actualización de Feromonas
```python
def reforzar_trayectoria(self, tramo: int, tiempo: float):
    if tiempo < self.mejor_tiempo:
        refuerzo = 1.0 / tiempo  # Mayor refuerzo para mejores tiempos
    else:
        refuerzo = 0.5 / tiempo  # Refuerzo estándar
```

#### Evolución Genética
```python
def evolucionar(self, evaluaciones: Dict[int, float]):
    # Preservar élite + generar nueva población
```

## Simulación y Ejecución

### Configuración de Simulación
- **Tramos de pista**: 20 segmentos
- **Generaciones**: 10 ciclos evolutivos
- **Evaluación**: Tiempos por vuelta como métrica principal

### Ejemplo de Ejecución
```python
# Inicializar sistema
controlador_robot = ControladorRobotCarreras(num_tramos_pista=20)

# Ciclo de carreras
for carrera in range(10):
    controlador_robot.inicializar_carrera()
    
    # Simular vuelta completa
    for tramo in range(20):
        # Tomar decisiones tácticas
        decision = controlador_robot.decidir_adelantamiento(oponente, pista)
        
        # Actualizar aprendizaje
        controlador_robot.actualizar_trayectoria(tramo, tiempo_tramo)
    
    # Evolución post-carrera
    controlador_robot.evolucionar_controlador(resultados)
```

## Características Avanzadas

### Ventajas del Enfoque Híbrido

1. **Robustez**: Múltiples algoritmos compensan limitaciones individuales
2. **Adaptabilidad**: Respuesta a diferentes escalas temporales
3. **Eficiencia**: Optimización simultánea de múltiples objetivos
4. **Aprendizaje continuo**: Mejora constante con experiencia

### Manejo de Incertidumbre
- **PSO**: Explora múltiples estrategias simultáneamente
- **Genético**: Mantiene diversidad en la población
- **Hormigas**: Aprende de experiencias pasadas en la misma pista
