"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""

from entorno import Agente


class MiAgente(Agente):

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        self.visitados = set()   # Posiciones donde ya estuvimos

    def al_iniciar(self):
        self.visitados.clear()

    def decidir(self, percepcion):
        pos_actual = percepcion['posicion']
        self.visitados.add(pos_actual)

        #Directamente hacia la meta
        for d in self.ACCIONES:
            if percepcion.get(d) == 'meta':
                return d
        
        #No visitados
        direccion_meta = percepcion.get('direccion_meta', ())
        movimientos_meta = []
        
        for d in self.ACCIONES:
            if percepcion.get(d) == 'libre':
                sig = self._sig(pos_actual, d)
                # Prioriza: hacia meta + no visitado
                es_hacia_meta = d in direccion_meta
                if es_hacia_meta and sig not in self.visitados:
                    movimientos_meta.append((2, d))
                elif es_hacia_meta:
                    movimientos_meta.append((1, d))
                elif sig not in self.visitados:
                    movimientos_meta.append((0, d))
                else:
                    movimientos_meta.append((-1, d))
        
        if movimientos_meta:
            movimientos_meta.sort(reverse=True)
            return movimientos_meta[0][1]
        
        for d in self.ACCIONES:
            if percepcion.get(d) == 'libre':
                return d
        
        return self.ACCIONES[0]
            
            
    def _sig(self, pos, d):
        f, c = pos
        return {'arriba':(f-1,c),'abajo':(f+1,c),
                'izquierda':(f,c-1),'derecha':(f,c+1)}[d]
    
