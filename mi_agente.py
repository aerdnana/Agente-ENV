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
    
