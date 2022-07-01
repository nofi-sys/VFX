# MI PROPIO OBJETO MIDI, TRANSFORMADO Y SIMPLIFICADO PARA PODER
# ACCEDER FÁCILMENTE A ALGUNOS DATOS. MI OBJETIVO (AL MENOS INICIAL)
# ES EXTRAER EL RITMO EXPLÍCITO E IMPLÍCITO Y LAS ACENTUACIONES
# PRINCIPALES Y SECUNDARIAS O HASTA TERCIARIAS (CAPAS RÍTMICAS)
import mido
import sys
import numpy as np
import math
import collections


sys.path.insert(0, 'F:\DESARROLLO\VFX\TIMECODE')
sys.path.insert(0, 'F:\DESARROLLO\VFX\PRESETS')
sys.path.insert(0, 'F:\DESARROLLO\VFX\TIEMPO')
sys.path.insert(0, 'F:\DESARROLLO\VFX\RITMO')
sys.path.insert(0, r'F:\DESARROLLO\VFX\NLE_OUTPUT')

import TIEMPO.UTILIDADES_TIEMPO as ut
from PRESETS.PRESETS_BEATS import *
from NLE_OUTPUT.XML_EXPORT import *

PLANO_1 = True
PLANO_2 = not PLANO_1

class Ritmo:

    def __init__(self, tempo=120, numerador = 4, denominador = 4, inicio=0):
        self.tempo = tempo
        self.clocks_per_click = 24
        self.n32n_per_beat = 8
        #self.duracion_negra = self.clocks_per_click * self.n32n_per_beat
        self.cargar_valor_figuras(self.clocks_per_click * self.n32n_per_beat)
        self.pulsos = numerador #cantidad de pulsos
        self.base = denominador #base rítmica
        self.inicio = inicio
        self.compases = 1 # cantidad de compases (PARA SOBRECARGAR)
        self.duracion_bloque = 0 #(PARA SOBRECARGAR)
        #print(self.tempo_a_microsegundo(tempo))

    def duracion_compas(self):
        d = self.base/4 # LA BASE NORMALIZADA A 1 = NEGRA
        return (self.valor_figuras["NEGRA"] * self.pulsos)/d

    def agregar_cantidad_compases(self, compases):
        self.compases = math.ceil(compases)
        self.duracion_bloque = self.compases * self.duracion_compas()

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


class NofiMid(mido.MidiFile):

    columnas_tiempo=[]

    def __init__(self, archivo=r"F:\DESARROLLO\VFX\MUSICA\01.mid", midi_type=1, tracks=1):
        mido.MidiFile.__init__(self, archivo)
        mid = self
        self.PRESETS_BEATS = PRESETS_BEATS
        self.track_base = mid.tracks[0]
        for msg in self.track_base:
            if msg.type == 'set_tempo':
                self.tempo = ut.mseg_a_tempo(msg.tempo)

        if midi_type == 0:
            self.track_principal = self.track_base
        else:
            self.track_principal = mid.tracks[-1]
        self.beats = []
        self.extraer_beats_track_principal(self.track_principal)

        self.estructura_ritmica = []
        self.crear_estructura_ritmica(self.track_base)
        self.lista_notas = []
        self.crear_lista_notas()

        self.rango_tonal = (self.rango_notas())

        # ESQUEMA MIDI
        self.crear_esquema_midi()  #FUSA por default

        # LISTA DE CORTES
        self.lista_de_cortes = []
        self.crear_lista_de_cortes()

    def tempo_a_microsegundo(self, tempo=120):
        return int(1000000 / (tempo / 60))
    def crear_estructura_ritmica(self, track):
        inicio_compas = True
        for mensaje in track:
            if mensaje.type == "set_tempo":
                tempo = self.tempo_a_microsegundo(mensaje.tempo)

            if mensaje.type == "time_signature":
                print("mensaje" *10)
                print(mensaje)

                compas = Ritmo(tempo, mensaje.numerator, mensaje.denominator, mensaje.time)

                if inicio_compas:
                    self.estructura_ritmica.append(compas)
                    duracion_compas = compas.duracion_compas()
                    inicio_compas = False
                else:
                    compases = mensaje.time / duracion_compas
                    self.estructura_ritmica[-1].agregar_cantidad_compases(compases)
                    #compas.inicio = inicio_compas
                    self.estructura_ritmica.append(compas)
                    duracion_compas = compas.duracion_compas()
        #TODO: AGREGAR DURACIÓN DE ÚLTIMO BLOQUE
        #compases = ?
        #self.estructura_ritmica[-1].agregar_cantidad_compases(compases)
                #self.estructura_ritmica.append(compas)
    def extraer_beats_track_principal(self, track):
        duracion = 0
        for mensaje in track:
            if mensaje.type == "note_on":
                duracion += mensaje.time
                if mensaje.velocity > 0:
                    self.beats.append(duracion)
                #print(duracion)
        self.duracion_total = duracion
        self.duracion_total_negras = duracion / 192
        print("DURACION TOTAL: ", self.duracion_total)
        print("DURACION TOTAL BEATS: ", self.duracion_total_negras)
        self.beats = list(dict.fromkeys(self.beats))
        #print(self.beats)
    def crear_lista_notas(self, grano=PRESETS_BEATS["FUSA"]):
        tiempo = 0
        for nota in self.track_principal:
            if nota.type == "note_on":
                tono = nota.note
                vol = nota.velocity
                if vol > 0:
                    estado = True
                else:
                    estado = False
                tiempo += math.ceil(nota.time / grano)
                self.lista_notas.append((tono, estado, vol, tiempo))
        #print(self.lista_notas)
    def rango_notas(self):
        mn = 127
        mx = 0
        #RECORRER TRACK Y DETERMINAR MIN Y MAX
        for x in self.lista_notas:
            if x[0] < mn:
                mn = x[0]
            if x[0] > mx:
                mx = x[0]

        return mn, mx
    def crear_esquema_midi(self, grano=PRESETS_BEATS["FUSA"]):
        assert self.track_principal
        self.cantidad_columnas = math.ceil(self.duracion_total / grano)
        self.columnas_tiempo = [[False for _ in range(0, 127)] for _ in range(0, self.cantidad_columnas)]

        for n, (nota, estado, volumen, tiempo) in enumerate(self.lista_notas):
            print(n, nota, tiempo)

            if volumen > 0:
                try:
                    self.columnas_tiempo[tiempo][nota] = True
                   #print(self.columnas_tiempo[tiempo])
                except:
                    break
            elif volumen == 0:
                # col[nota] = False
                # print("nota apagada", tiempo, nota)
                try:
                    self.columnas_tiempo[tiempo][nota] = True
                except:
                    break

        for n, col in enumerate(self.columnas_tiempo):

            for nota, estado in enumerate(col):
                if estado == True:
                    try:
                        self.columnas_tiempo[n+1][nota] = not self.columnas_tiempo[n+1][nota]
                    except:
                        pass



    def crear_lista_de_cortes(self):

        # print("estructura ritmica " * 10)
        # print(self.estructura_ritmica)

        #OPCIÓN 1: EN BASE A PRESETS DE RITMO
        for bloque_ritmo in self.estructura_ritmica:
            #print(bloque_ritmo.__dict__)
            pass

        #OPCIÓN 2: RITMO CUSTOM (EN BASE A LISTA DE NOTAS)
        #ESTA OPC ES PREFERIBLE CUANDO CONTAMOS CON
        #MIDI EXCLUSIVAMENTE RÍTMICO (HECHO "A MEDIDA")

        img = PLANO_1

        for nota in self.lista_notas:

            if nota[1] is True:
                tiempo = nota[3]
                clip = (tiempo, img)
                self.lista_de_cortes.append(clip)
                img = not img
        print(self.lista_de_cortes)





    def exportar_xml(self, nombre="NOFI_MID", lista_de_cortes= []):
        archivo = nombre + ".xml"
        self.xml = NOFI_XML(nombre=archivo, lista_de_cortes=self.lista_de_cortes)
        self.xml.exportar_xml(archivo)


    def _test_columnas(secuencia):
        for columna in secuencia.columnas_tiempo:
            for nota in enumerate(columna):
                if nota[1] is True:
                    print(nota)
        print(secuencia.columnas_tiempo[0])


if __name__ == "__main__":
    archivo = r"F:\DESARROLLO\VFX\MUSICA\KALIBANG_RITMO.mid"
    #archivo = "F:\DESARROLLO\VFX\MUSICA\RITMO4468v3.mid"
    secuencia = NofiMid(archivo)
    secuencia.exportar_xml(nombre="KALIBANG")
