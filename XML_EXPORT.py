import copy

import lxml.etree as etree
import uuid

class NOFI_XML():

    # INSERTAR DATA PRESETEADA SECUENCIA
    def __init__(self, base_xml=r"F:\DESARROLLO\VFX\NLE_OUTPUT\XML_TEMPLATES\XML.xml",
                       base_seq=r"F:\DESARROLLO\VFX\NLE_OUTPUT\XML_TEMPLATES\SEQ.xml",
                       nombre="NOFI_MID_EXPERIMENTAL",
                       lista_de_cortes=None
                 ):

        # CARGAR XML BASE
        self.xml = etree.parse(base_xml)
        self.uuid = uuid.uuid4()
        self.nombre = nombre
        self.carpeta_exports = "EXPORTS/"
        self.archivo = self.carpeta_exports + self.nombre + ".xml"


        # CARGAR TEMPLATE CLIP ITEMs
        clip_item_template_1 = r"F:\DESARROLLO\VFX\NLE_OUTPUT\XML_TEMPLATES\CLIP_ITEM_1.xml"
        clip_item_template_1 = etree.parse(clip_item_template_1)
        clip_item_template_2 = r"F:\DESARROLLO\VFX\NLE_OUTPUT\XML_TEMPLATES\CLIP_ITEM_2.xml"
        clip_item_template_2 = etree.parse(clip_item_template_2)
        self.clip_item_templates = [clip_item_template_1, clip_item_template_2]
        self.crear_lista_clips(lista_de_cortes=lista_de_cortes)
        # CREAR SEQ
        self.seq = etree.parse(base_seq)
        self.crear_secuencia(self.seq.getroot())

    def crear_lista_clips(self, lista_de_cortes=None):
        self.clip_items = []

        if lista_de_cortes==None:
            lista_de_cortes = []
            tiempo = 0
            img = True
            for x in range(0, 10):
#               lista_de_cortes=[(tiempo, img)]
                lista_de_cortes.append((tiempo, img))
                tiempo += 25
                img = not img

        for n, item in enumerate(lista_de_cortes):

            tiempo = item[0]
            start = str(tiempo)
            img = int(item[1])
            # print("img")
            # print(img)

            # print(lista_de_corte[n + 1])
            try:
                end = str(lista_de_cortes[n+1][0])
            except:
                end = str(int(tiempo) + 25)
            #print(start,end)
            item = self.crear_clip_item(self.clip_item_templates[img], n+1, start, end)
            # etree.dump(item)
            self.clip_items.append(item)

        return

    def obtener_duracion(self):
        pass

    def crear_secuencia(self, seq):

        #LLENAR UUID
        seq.find('uuid').text = str(self.uuid)

        # NOMBRE DE SEQ
        seq.find('name').text = str(self.nombre)

        # CLIP ITEMS
        media = seq.find('media')
        video = media.find('video')
        track = video.find('track')

        for n, item in enumerate(self.clip_items):
            track.insert(n, item)

        # INSERTAR SECUENCIA EN XML
        xml = self.xml.getroot()
        xml.insert(0, seq)

        #self.seq = etree.parse(seq)
        # etree.dump(video)



            #INSERTAR CLIP_ITEM EN SEQ




        # DURACIÓN

    # CLIP ITEMS (Y LISTA DE CORTES VIDEO + AUDIO)
    def crear_clip_item(self, clip_item_template, id=1, start=0, end=400):
        #print(id, start, end)
        nuevo_item = copy.deepcopy(clip_item_template.getroot())
        #TODO: id="clipitem-x", <masterclipid>, <name>
        item_id = 'masterclip-' + str(id)
        nuevo_item.set('id', item_id)
        #append <start> y <end>
        nuevo_item.find('start').text = str(start)
        nuevo_item.find('end').text = str(end)
        #etree.dump(nuevo_item)

        # nombre = nuevo_item.xpath('in/text()')
        # print(nombre)

        return nuevo_item

        pass

    # EXPORTAR ARCHIVO .xml
    def exportar_xml(self, archivo = ''):

        with open(archivo, 'wb') as arch:
            self.xml.write(arch)


    def _test(self):
        test = self.xml.getroot()
        nombre = test.xpath('sequence/name/text()')
        #nombre = test.find('sequence/name')
        # print(nombre)
        #self.crear_clip_item(self.clip_item_templates[0])
#        etree.dump(nombre)

if __name__ == "__main__":

    nofi_xml = NOFI_XML()
    #nofi_xml._test()
    nofi_xml.exportar_xml()
