import sys
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty
from collections import deque
sys.path.insert(0, 'F:\DESARROLLO\VFX\MIDI')
from MIDI.NOFI_MIDI import NofiMid
sys.path.insert(0, '/PRESETS')
from PRESETS.PRESETS_BEATS import *
sys.path.insert(0, 'F:\DESARROLLO\VFX\MIDI')
#import MIDI.MIDI_A_TENSOR as mt
sys.path.insert(0, 'F:\DESARROLLO\VFX\TIEMPO')
import TIEMPO.UTILIDADES_TIEMPO
FIGURAS_REPRODUCTOR = {"PLAY": "F:\DESARROLLO\VFX\IMG\PLAY.png",
                       "PLAY_ON":"F:\DESARROLLO\VFX\IMG\PLAY_ON.png",
                       "REW":"F:\DESARROLLO\VFX\IMG\REW.png",
                       "REW_ON":"F:\DESARROLLO\VFX\IMG\REW_OFF.png",
                       "FF":"F:\DESARROLLO\VFX\IMG\FF.png",
                       "FF_ON":"F:\DESARROLLO\VFX\IMG\FF_OFF.png"
                       }
PLAY = ("PLAY", "PLAY_ON", 2)
REW = ("REW", "REW_ON", 1)
FF = ("FF", "FF_ON", 0)

BOTONES = {"PLAY": PLAY[2],"REW":REW[2],"FF":FF[2]}

class BotonReproductor(Button):
    indice = NumericProperty()

class ReproductorMidi(BoxLayout):
    estado = False
    velocidad_reproduccion = NumericProperty()
    velocidad_actual = NumericProperty(0)
    posicion_actual = BoundedNumericProperty(0, min=0, max=1000)
    posicion_actual_en_beats = NumericProperty(0)
    tempo = NumericProperty(120)
    monitor = ListProperty()
    monitor_in = NumericProperty(0)
    monitor_out = NumericProperty(16)
    #columnas_reproduccion = ListProperty()
    def __init__(self, tempo = 120):
        self.PLAY = PLAY
        self.FF = FF
        self.REW = REW
        self.FIGURAS_REPRODUCTOR = FIGURAS_REPRODUCTOR
        self.BOTONES = BOTONES
        self.beat_minimo = PRESETS_BEATS["FUSA"]

        #self.columnas_reproduccion = deque()
        self.columna_actual = int
        self.duracion_total = 0
        super().__init__()
        self.cargar_midi(archivo=r"F:\DESARROLLO\VFX\MUSICA\01_48.mid")
        #exit()
    def boton_apretado(self, boton=PLAY[2]):

        if boton == PLAY[2]:

            #SI ESTÁ APAGADO, EMPEZAR A REPRODUCIR
            if self.velocidad_actual == 0:
                print("POSICION: ", self.posicion_actual)
                self.estado = True
                self.velocidad_actual += self.velocidad_reproduccion
                #print("VELOCIDAD AUMENTADA A: ", self.velocidad_actual)
                self.event = Clock.schedule_interval(self.reproducir, self.velocidad_reproduccion)
                #self.event()
            #SI ESTÁ REPRODUCIENDO, FRENAR
            else:
                self.velocidad_actual = 0
                self.estado = False
                self.event.cancel()
                #Clock.schedule_interval(self.reproducir, 0)
                print("STOP")

        elif boton == FF[2]:
           #self.event.cancel()
            self.reproducir(self.velocidad_reproduccion)
            print("FF")

        elif boton == REW[2]:
            #self.event.cancel()
            self.velocidad_reproduccion= -abs(self.velocidad_reproduccion)
            self.reproducir(self.velocidad_reproduccion)
            self.velocidad_reproduccion = abs(self.velocidad_reproduccion)
            #Clock.schedule_once(my_callback, reversa)

    def reproducir(self, dt=0):

        #GENERAR CADENA DE EVENTOS
        if self.posicion_actual >= self.duracion_total-1:
            self.posicion_actual = dt
            print("STOP")
            return False
        print("posicion actual ", self.posicion_actual)
        self.posicion_actual += dt
        if self.posicion_actual < 0:
            self.posicion_actual = 0

        print(self.posicion_actual)
        return True

    def cargar_midi(self, archivo=r"F:\DESARROLLO\VFX\MUSICA\01_48.mid"):
        self.midi = NofiMid(archivo)
        #self.posicion_actual = BoundedNumericProperty(0, min=0, max=self.midi.duracion_total)
        self.tempo = self.midi.tempo
        print("x" * 100)
        print("POSICION")
        print(self.posicion_actual)
        #self.property('posicion_actual').set_max(self, self.duracion_total/192)
        print(self.midi.duracion_total/192)
        print("x" * 100)
        # print("tempo ",self.midi.tempo)
        # print("beat minimo ",self.beat_minimo)
        self.velocidad_reproduccion = self.beat_a_segs(self.beat_minimo, tempo=self.midi.tempo)
        print(self.velocidad_reproduccion)
        self.monitor = self.midi.columnas_tiempo[self.monitor_in:self.monitor_out]
        # if True in self.monitor[15]:
        #     print("True en monitor" * 30)
        #     exit()
        self.duracion_total = self.midi.duracion_total
        return

    def segs_a_beat(self, segundos, tempo=60, grano=192):
        negras_por_seg = tempo / 60
        duracion_beat = 1 / (negras_por_seg * grano)

        return int(segundos / duracion_beat)

    def on_posicion_actual(self, instance, info):
        #print("POSICION ACTUAL: ")
        #print(self.posicion_actual)
        self.posicion_actual_en_beats = self.segs_a_beat(self.posicion_actual, self.midi.tempo)
        self.columna_actual = int(self.posicion_actual_en_beats / self.beat_minimo)
        if self.columna_actual < self.midi.cantidad_columnas - 16:
            self.monitor[0].pop()
            # Agregar nueva columna
            self.monitor.append(self.midi.columnas_tiempo[self.columna_actual+16])
            self.actualizar_monitor()
        else:
            self.velocidad_actual = 0
            self.estado = False
            self.event.cancel()
        # if True in self.monitor:
        #     print("True en monitor" * 30)


        #print(len(self.monitor))
        #print(self.monitor[0][80:92])
        #print(self.midi.columnas_tiempo[self.columna_actual][81])

        # if self.midi.columnas_tiempo[self.columna_actual][81] == False:
        #     print("FALSE")
    def actualizar_monitor(self):
        print("test actualizar monitor desde reproductor" *10)
        if True in self.monitor[16]:
            print("true en monitor 16")
            for n, x in enumerate(self.monitor[16]):
                if x is True:
                    print(n)

            print("True en monitor" * 30)

        for layouts in self.children:
            #print(layouts)
            for monitor in layouts.children:

                if "MidiMonitor" in str(monitor):
                    print("ACTUALIZANDO MONITOR")
                    monitor.actualizar(self.monitor)

            # for bloque in columna.children:
            #      print(bloque.estado)

#UTILIDADES
    def beat_a_segs(self, cantidad_beats, tempo=60, grano=192):
        negras_por_seg = self.midi.tempo / 60
        print("x" * 200)
        print(negras_por_seg)
        duracion_beat = 1 / (negras_por_seg * grano)
        return duracion_beat * cantidad_beats

class ReproductorMidiApp(App):
    def build(self):
        return ReproductorMidi()

# COLUMNA QUE REPRESENTA TODAS LAS NOTAS POSIBLES

class BloqueBeat(Image):
    nota = NumericProperty()
    estado = BooleanProperty(False)
    def __init__(self, id = 0):
        self.nota = id
        self.silencio = 0.4
        self.start = True


        Image.__init__(self, source="F:\DESARROLLO\VFX\IMG\BORDE MAGENTA.png", color=[1, 1, 1, 0.4], size_hint_x=1,
                         keep_ratio=False, allow_stretch=True )

    def invertir_estado(self):
        self.estado = not self.estado

    def actualizar(self, estado):
        #self.invertir_estado()
        #self.estado = estado
        self.on_estado(self, estado)
        if self.start == True:
            #print("PRIMERA ACTUALIZACION")
            self.on_estado(self, estado)
            self.start = False
        else:
            pass
        #print("ACTUALIZAR BLOQUE BEAT")




    def on_estado(self, instance, estado):
        pass
        #
        # if self.estado == True:
        #     Image.__init__(self, source="F:\DESARROLLO\VFX\IMG\MAGENTA_MINI.png", color=[1, 1, 1, 1],
        #                    size_hint_x=1,
        #                    keep_ratio=False, allow_stretch=True)
        # else:
        #     Image.__init__(self, source="F:\DESARROLLO\VFX\IMG\BORDE MAGENTA.png", color=[1, 1, 1, 0.4], size_hint_x=1,
        #                    keep_ratio=False, allow_stretch=True)

        #print("DEBERÍA CAMBIAR EL COLOR")

class ColumnaBeat(BoxLayout):
    id = NumericProperty
    columna_monitor = ListProperty()
    def __init__(self, id = 0, **kwargs):
        BoxLayout.__init__(self, orientation="vertical", **kwargs)
        self.id = id
        self.mn, self.mx = (0, 127)
        # if self.mn > 48:
        #     self.mn = 48
        # if self.mx < 96:
        #     self.mx = 96

        for x in range(self.mn, self.mx):
            b = BloqueBeat(x)
            self.columna_monitor.append(b.estado)
            self.add_widget(b)

    def actualizar(self, columna=0):

        self.columna_monitor = columna
        #print("COLUMNA ACTUALIZADA")

    def on_columna_monitor(self, instance, value):
        #print("instance ", instance)
        #print("value ", value)
        for n, bloques in enumerate(self.children):
            #bloques.actualizar(self.columna_monitor[n])
            bloques.actualizar(self.columna_monitor[n])
            # if x == True:
            #     print(n, "es True")
            #
# PANTALLA CENTRAL: REPRESENTACIÓN GRÁFICA DEL MIDI
class MidiMonitor(BoxLayout):
    columnas_reproduccion = ListProperty(deque())

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, orientation="horizontal", **kwargs)
        for x in range(0,16):
            col = ColumnaBeat(x)
            #col.columna_monitor
            #col.bind()
            # self.monitor.append()
            self.add_widget(col)
        self.start = True
        #self.activar_test()

    def on_columnas_reproduccion(self, instance, value):
        #print("COLUMNAS CAMBIADAS")
        for n, columna in enumerate(self.children):
            pass
            #print(n, columna)
            #print(self.columnas_reproduccion)
#            columna.actualizar(self.columnas_reproduccion[n])


    # def actualizar_columna(self, columna = ColumnaBeat()):
    #     for nota in columna:
    #         if nota == True:
    #             print("ACTIVAR NOTA", nota.n)
    def actualizar(self, columnas=[]):
       #print("actualizar monitor")
       self.columnas_reproduccion = columnas
       if self.start == False:
           pass
           #print("ARRANQUE")
           #self.on_columnas_reproduccion()
       else:
           self.start = False

    def activar_test(self):

        for col, columna in enumerate(self.children):
            #print("COLUMNA ",col)
            for bloque in columna.children:
                pass
                 #print(bloque.estado)
        #print("TEST DE NOTA 81")
        #print(self.children[1].children[1][81].estado)

if __name__ == '__main__':
    ReproductorMidiApp().run()