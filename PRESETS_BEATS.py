


NG = 192
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

PRESETS_BEATS = {"NEGRA": NG, "BLANCA": BC, "BLANCA+":BCx, "REDONDA":RD,
                 "NEGRA+": NGx, "CORCHEA": CH, "CORCHEA+": CHx,
                 "SEMICORCHEA": SC, "FUSA": FS, "SEMIFUSA":SF}
#Modo de uso: PRESETS_BEATS["FUSA"]