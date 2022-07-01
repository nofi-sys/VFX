import sys
sys.path.insert(0, 'F:\DESARROLLO\VFX\PRESETS')

from PRESETS.PRESETS_BEATS import *
GRANO = PRESETS_BEATS["SEMICORCHEA"]
#print(GRANO)

# SEGUNDOS A TIMECODE

def segs_a_frames(segs, fps = 25):
    return segs * fps


def segs_a_timecode(segs, fps=25, offset=0):

    hrs = segs / 60 / 60 + offset
    hrs = int(hrs)
    hrs_en_segs = hrs * 60 * 60
    hrs_en_mins = hrs * 60
    mins = segs / 60
    mins -= hrs_en_mins
    mins = int(mins)
    mins_en_segs = mins * 60
    resto_segs = segs - hrs_en_segs - mins_en_segs
    segs_tc = int(resto_segs)

    frames_en_seg = segs - segs_tc
    resto = frames_en_seg - int(frames_en_seg)
    print(resto)
    frames = resto * fps
    frames = int(frames)
    print(frames)
    #    frames = int(frames_en_seg * fps / 60)
    # print(segs, hrs, hrs_en_segs, mins, mins_en_segs, segs_tc, frames_en_seg, resto)
    if resto > 0.65:
        frames += 1
        resto -= 1

    timecode = [hrs, mins, segs_tc, frames, resto]

    return timecode

def microsegs_a_timecode(microsegs, fps=25, offset=0):
    segs = microsegs / 1000000
    hrs = segs / 60 / 60 + offset
    hrs = int(hrs)
    hrs_en_segs = hrs * 60 * 60
    hrs_en_mins = hrs * 60
    mins = segs / 60
    mins -= hrs_en_mins
    mins = int(mins)
    mins_en_segs = mins * 60
    resto_segs = segs - hrs_en_segs - mins_en_segs
    segs_tc = int(resto_segs)

    frames_en_seg = segs - segs_tc
    resto = frames_en_seg - int(frames_en_seg)
    print(resto)
    frames = resto * fps
    frames = int(frames)
    print(frames)
#    frames = int(frames_en_seg * fps / 60)
    #print(segs, hrs, hrs_en_segs, mins, mins_en_segs, segs_tc, frames_en_seg, resto)
    if resto > 0.65:
        frames += 1
        resto -= 1

    timecode = [hrs, mins, segs_tc, frames, resto]
    print(timecode)
    return timecode

def beat_pos_a_TC(tempo = 120, tiempo_beat = 0, grano=192):

    negra = negra_a_mseg(tempo)
    print("negra a mseg", negra)
    beat = negra / grano
    tiempo_beat_microsegs = tiempo_beat * beat
    return microsegs_a_timecode(tiempo_beat_microsegs)

def beat_a_segs(cantidad_beats, tempo = 60, grano=192):
    negras_por_seg = tempo / 60
    duracion_beat = 1 / (negras_por_seg * grano)
    return duracion_beat * cantidad_beats

def segs_a_beat(segundos, tempo=60, grano=192):
    negras_por_seg = tempo / 60
    duracion_beat = 1 / (negras_por_seg * grano)

    return segundos / duracion_beat

def negra_a_mseg(tempo):
    mseg = int(1000000 / (tempo / 60))
    return mseg

def mseg_a_tempo(mseg = 1000000): # 1.000.000 = 120
    tempo = (1000000 * 60) / mseg
    #print("tempo ")
    return tempo


#print(beat_pos_a_TC(tempo=60, tiempo_beat=pos))
# print(beat_a_segs())
#print(segs_a_beat(0.0625))
print(mseg_a_tempo(1200000))

# TODO: QUITAR O REEMPLAZAR EXTENSIÓN ej: ".wav" por ".pkl"



# TODO: FORMATOS DE AUDIO Y VDEO