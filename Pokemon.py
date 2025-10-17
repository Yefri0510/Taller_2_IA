import matplotlib.pyplot as plt
import random

# Configuración inicial
TIPOS = ['fuego', 'agua', 'planta', 'eléctrico']
PROB_MUTACION = 0.2
TAM_POBLACION = 10
GENERACIONES = 5

def crear_pokemon():
    return {
        'ataque': random.random(),
        'defensa': random.random(),
        'velocidad': random.random(),
        'vida': random.random(),
        'tipo': random.choice(TIPOS)
    }

def evaluar_pokemon(pokemon):
    bonus_tipo = {
        'fuego': 1.1,
        'agua': 1.05,
        'planta': 1.0,
        'eléctrico': 1.08
    }
    
    poder = (pokemon['ataque'] * 0.3 +
             pokemon['defensa'] * 0.2 +
             pokemon['velocidad'] * 0.25 +
             pokemon['vida'] * 0.25)
    
    return poder * bonus_tipo[pokemon['tipo']]

def seleccionar_padres(poblacion):
    poblacion_ordenada = sorted(poblacion, key=evaluar_pokemon, reverse=True)
    return poblacion_ordenada[:2]

def cruzar(padre1, padre2):
    hijo = {}
    # Cruza uniforme para stats
    for stat in ['ataque', 'defensa', 'velocidad', 'vida']:
        hijo[stat] = random.choice([padre1[stat], padre2[stat]])
    
    # Cruza para el tipo
    hijo['tipo'] = random.choice([padre1['tipo'], padre2['tipo']])
    
    return hijo

def mutar(pokemon):
    if random.random() < PROB_MUTACION:
        stat = random.choice(['ataque', 'defensa', 'velocidad', 'vida'])
        pokemon[stat] = max(0, min(1, pokemon[stat] + random.gauss(0, 0.1)))
    
    if random.random() < PROB_MUTACION:
        pokemon['tipo'] = random.choice(TIPOS)
    
    return pokemon

def graficar_evolucion(historial):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gráfico 1: Evolución del poder
    generaciones = range(1, len(historial) + 1)
    mejores_poderes = [h['mejor_poder'] for h in historial]
    promedios_poderes = [h['promedio_poder'] for h in historial]
    
    ax1.plot(generaciones, mejores_poderes, 'o-', label='Mejor Poder', linewidth=2)
    ax1.plot(generaciones, promedios_poderes, 's-', label='Promedio Poder', linewidth=2)
    ax1.set_xlabel('Generación')
    ax1.set_ylabel('Poder')
    ax1.set_title('Evolución del Poder por Generación')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2: Evolución de stats promedio
    stats = ['ataque', 'defensa', 'velocidad', 'vida']
    for stat in stats:
        valores = [h['stats_promedio'][stat] for h in historial]
        ax2.plot(generaciones, valores, 'o-', label=stat.capitalize(), linewidth=2)
    
    ax2.set_xlabel('Generación')
    ax2.set_ylabel('Valor del Stat')
    ax2.set_title('Evolución de Stats Promedio')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

historial = []    
# Evolución
poblacion = [crear_pokemon() for _ in range(TAM_POBLACION)]

for generacion in range(GENERACIONES):
    print(f"\n*** Generación {generacion + 1} ***")
    
    # Evaluar y mostrar población
    for i, pokemon in enumerate(poblacion):
        print(f"Pokémon {i+1}: {pokemon} -> Poder: {evaluar_pokemon(pokemon):.2f}")
    
    # Calcular estadísticas para el historial
    poderes = [evaluar_pokemon(p) for p in poblacion]
    mejor_pokemon = max(poblacion, key=evaluar_pokemon)

    stats_promedio = {
        'ataque': sum(p['ataque'] for p in poblacion) / len(poblacion),
        'defensa': sum(p['defensa'] for p in poblacion) / len(poblacion),
        'velocidad': sum(p['velocidad'] for p in poblacion) / len(poblacion),
        'vida': sum(p['vida'] for p in poblacion) / len(poblacion)
        }

    historial.append({
        'mejor_poder': evaluar_pokemon(mejor_pokemon),
        'promedio_poder': sum(poderes) / len(poderes),
        'stats_promedio': stats_promedio
        })

    # Crear nueva generación
    nueva_poblacion = []
    while len(nueva_poblacion) < TAM_POBLACION:
        padre1, padre2 = seleccionar_padres(poblacion)
        hijo = cruzar(padre1, padre2)
        hijo = mutar(hijo)
        nueva_poblacion.append(hijo)
    
    poblacion = nueva_poblacion

# Mostrar resultado final
graficar_evolucion(historial)
mejor_pokemon = max(poblacion, key=evaluar_pokemon)
print("\n*** Mejor Pokémon Final ***")
print(f"Stats: {mejor_pokemon}")
print(f"Poder: {evaluar_pokemon(mejor_pokemon):.2f}")