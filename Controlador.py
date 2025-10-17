import numpy as np
from typing import Dict, List

# ALGORITMO GENÉTICO - Evolución de parámetros base
class GeneticoControlador:
    def __init__(self):
        self.poblacion = self._inicializar_poblacion()
        
    def _inicializar_poblacion(self) -> List[Dict]:
        return [{
            'agresividad': np.random.uniform(0.5, 1.0),
            'conservador': np.random.uniform(0.1, 0.5),
            'adelantamiento': np.random.uniform(0.6, 1.0)
        } for _ in range(50)]
    
    def evolucionar(self, evaluaciones: Dict[int, float]):
        # Ordenar por desempeño (tiempos más bajos = mejor)
        mejores = sorted(evaluaciones.items(), key=lambda x: x[1])[:10]
        
        nueva_poblacion = []
        # Conservar mejores individuos (elitismo)
        for idx, _ in mejores:
            nueva_poblacion.append(self.poblacion[idx])
        
        # Cruzar y mutar
        while len(nueva_poblacion) < len(self.poblacion):
            padre = self.poblacion[np.random.choice([idx for idx, _ in mejores])]
            madre = self.poblacion[np.random.choice([idx for idx, _ in mejores])]
            
            hijo = {}
            for gen in padre.keys():
                if np.random.random() > 0.5:
                    hijo[gen] = padre[gen]
                else:
                    hijo[gen] = madre[gen]
                
                # Mutación
                if np.random.random() < 0.1:
                    hijo[gen] = np.clip(hijo[gen] + np.random.normal(0, 0.1), 0.1, 1.0)
            
            nueva_poblacion.append(hijo)
        
        self.poblacion = nueva_poblacion

# ALGORITMO DE PARTÍCULAS - Optimización de trayectoria en tiempo real
class ControladorPSO:
    def __init__(self, parametros_base: Dict):
        self.agresividad = parametros_base['agresividad']
        self.adelantamiento = parametros_base['adelantamiento']
        
        # Espacio de búsqueda: [distancia_seguridad, ángulo_ataque, momento_adelantamiento]
        self.particulas = [np.random.uniform(0, 1, 3) for _ in range(20)]
        self.velocidades = [np.random.uniform(-0.1, 0.1, 3) for _ in range(20)]
        self.mejores_posiciones = self.particulas.copy()
        
    def decidir_adelantamiento(self, oponente: Dict, pista: Dict) -> Dict:
        # Evaluar todas las partículas
        evaluaciones = []
        for particula in self.particulas:
            score = self._evaluar_estrategia(particula, oponente, pista)
            evaluaciones.append(score)
        
        # Actualizar mejores posiciones
        mejor_global_idx = np.argmax(evaluaciones)
        
        # Mover partículas
        for i in range(len(self.particulas)):
            inercia = 0.7
            cognitivo = 1.5
            social = 1.5
            
            self.velocidades[i] = (inercia * self.velocidades[i] +
                                 cognitivo * np.random.random() * (self.mejores_posiciones[i] - self.particulas[i]) +
                                 social * np.random.random() * (self.mejores_posiciones[mejor_global_idx] - self.particulas[i]))
            
            self.particulas[i] = np.clip(self.particulas[i] + self.velocidades[i], 0, 1)
        
        mejor_estrategia = self.particulas[mejor_global_idx]
        
        return {
            'distancia_seguridad': mejor_estrategia[0] * 2 + 0.5,  # 0.5 - 2.5 metros
            'angulo_ataque': mejor_estrategia[1] * 30 - 15,  # -15° a +15°
            'momento_adelantamiento': mejor_estrategia[2] > 0.7
        }
    
    def _evaluar_estrategia(self, particula: np.ndarray, oponente: Dict, pista: Dict) -> float:
        # Factores de evaluación
        seguridad = 1.0 - abs(particula[0] - 0.3)  # Preferir distancia media
        eficiencia = particula[1] * self.agresividad
        oportunidad = particula[2] * self.adelantamiento
        
        return seguridad * 0.3 + eficiencia * 0.4 + oportunidad * 0.3

# ALGORITMO DE HORMIGAS - Aprendizaje de trayectoria óptima
class HormigaRacing:
    def __init__(self, num_tramos: int):
        self.feromonas = np.ones(num_tramos) * 0.1
        self.mejor_tiempo = float('inf')
        self.mejor_trayectoria = None
        
    def reforzar_trayectoria(self, tramo: int, tiempo: float):
        # Actualizar feromonas basado en desempeño
        if tiempo < self.mejor_tiempo:
            refuerzo = 1.0 / tiempo
            self.feromonas[tramo] += refuerzo * 2.0  # Doble refuerzo para mejores tiempos
            self.mejor_tiempo = tiempo
        else:
            self.feromonas[tramo] += 0.5 / tiempo
        
        # Evaporación natural
        self.feromonas *= 0.95
    
    def obtener_mejor_linea(self, tramo_actual: int) -> int:
        # Decidir siguiente movimiento basado en feromonas
        probabilidades = self.feromonas / np.sum(self.feromonas)
        return np.random.choice(len(self.feromonas), p=probabilidades)

# SISTEMA PRINCIPAL INTEGRADO
class ControladorRobotCarreras:
    def __init__(self, num_tramos_pista: int):
        self.genetico = GeneticoControlador()
        self.hormiga = HormigaRacing(num_tramos_pista)
        self.controlador_actual = None
        self.generacion = 0
        
    def inicializar_carrera(self):
        # Seleccionar mejor individuo de la población genética
        mejor_idx = np.random.randint(0, len(self.genetico.poblacion))  # En práctica, usar evaluaciones previas
        self.controlador_actual = ControladorPSO(self.genetico.poblacion[mejor_idx])
    
    def decidir_adelantamiento(self, oponente: Dict, pista: Dict) -> Dict:
        return self.controlador_actual.decidir_adelantamiento(oponente, pista)
    
    def actualizar_trayectoria(self, tramo: int, tiempo: float):
        self.hormiga.reforzar_trayectoria(tramo, tiempo)
    
    def evolucionar_controlador(self, resultados_carrera: Dict[int, float]):
        self.genetico.evolucionar(resultados_carrera)
        self.generacion += 1

# EJEMPLO DE USO
if __name__ == "__main__":
    # Configuración inicial
    controlador_robot = ControladorRobotCarreras(num_tramos_pista=20)
    
    # Simulación de ciclo de carrera
    for carrera in range(10):
        print(f"=== Generación {carrera + 1} ===")
        
        controlador_robot.inicializar_carrera()
        
        # Simular vuelta
        for tramo in range(20):
            tiempo_tramo = np.random.uniform(0.8, 1.5)
            controlador_robot.actualizar_trayectoria(tramo, tiempo_tramo)
            
            # Simular decisión de adelantamiento
            oponente = {'posicion': np.random.uniform(0, 10), 'velocidad': np.random.uniform(5, 15)}
            pista = {'ancho': 8, 'curvatura': np.random.uniform(-0.5, 0.5)}
            
            decision = controlador_robot.decidir_adelantamiento(oponente, pista)
            if decision['momento_adelantamiento']:
                print(f"Adelantamiento en tramo {tramo}: {decision}")
        
        # Evolucionar después de cada carrera
        resultados_simulados = {i: np.random.uniform(60, 120) for i in range(50)}
        controlador_robot.evolucionar_controlador(resultados_simulados)