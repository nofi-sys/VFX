class Ritmo:

    def __init__(self, tempo=120, numerador = 4, denominador = 4):
        self.tempo = tempo
        self.clocks_per_click = 24
        self.n32n_per_beat = 8
        #self.duracion_negra = self.clocks_per_click * self.n32n_per_beat
        self.cargar_valor_figuras(self.clocks_per_click * self.n32n_per_beat)
        self.pulsos = numerador #cantidad de pulsos
        self.base = denominador #base rítmica
        self.inicio = 0
        self.compases = None # cantidad de compases
        #print(self.tempo_a_microsegundo(tempo))

    def duracion_compas(self):
        d = self.base/4 # LA BASE NORMALIZADA A 1 = NEGRA
        return (self.duracion_negra * self.pulsos)/d

    def agregar_cantidad_compases(self, compases):
        self.compases = compases

    def negras_en_compas(self, duracion):
        pass

    def cargar_valor_figuras(self, negra=192, sobrecargar=True):

        NG = negra
        BC = NG * 2
        BCx = NG * 3
        RD = NG * 4

        #NGx
        CH = int(NG / 2)
        NGx = 3 * CH

        SC = int(CH / 2)
        CHx = 3 * SC

        FS = int(SC/ 2)
        SF = int(FS / 2)
        FSx = FS + SF

        #DICCIONARIO QUE TIENE TODA LA INFORMACIÓN DE ARRIBA
        VALOR_FIGURAS = {}
        VALOR_FIGURAS = {"NEGRA": NG, "BLANCA": BC, "BLANCA+":BCx, "REDONDA":RD,
                         "NEGRA+": NGx, "CORCHEA": CH, "CORCHEA+": CHx,
                         "SEMICORCHEA": SC, "FUSA": FS, "SEMIFUSA":SF}
        if sobrecargar == True:
            self.valor_figuras = VALOR_FIGURAS
        else:
            return VALOR_FIGURAS


if __name__ == "__main__":

    ritmo = Ritmo()
    print(ritmo.valor_figuras)
    ritmo.cargar_valor_figuras(negra=96)
    print(ritmo.valor_figuras)
