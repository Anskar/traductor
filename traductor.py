#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from gi.repository import Gtk, GObject, GLib , Gdk
import wikipedia, codecs, re, catlib
import sys, os
from threading import Thread
import string
import subprocess

path = os.path.dirname(sys.argv[0])
print path

GObject.threads_init()

print u'Importats tots els mòduls necessaris'



class Feines(Thread):

    def __init__(self, ginys, boolean):

        Thread.__init(self)
        pass

    def run(self):
        pass

    def paremThreads(self, boolean):
        pass

class Inici:
    def peticions(self):
        print self.widgets
        pass


class Finestra(Inici):

    def dibuixFinestra(self):

        self.marca_inici = True
        self.volem_sortir = True

        const = Gtk.Builder()
        const.add_from_file(path+'/vistes/finestres.glade')
        self.fin = const.get_object('finestra-inici')
        self.fin.connect('destroy', self.destroy)
        self.fin_prog = const.get_object('finestra-programa')
        self.fin_prog.connect('destroy',self.destroy)
        self.fin_plant = const.get_object('finestra-plantilles')

        finestres = self.fin_plant

        # BARRA D'EINES
        boto_edita = const.get_object('toolbutton1')
        boto_edita.connect('clicked',self.edita)
        boto_dicc = const.get_object('toolbutton2')
        boto_dicc.connect('clicked',self.desaDicc)
        boto_plant = const.get_object('toolbutton3')
        boto_plant.connect('clicked',self.mostraPlantilla)
        imatge_enllacos = const.get_object('enllacos')
        boto_sortida = const.get_object('toolbutton4')
        boto_sortida.connect('clicked', self.destroy)
        # ESPAI DE PETICIÓ
        titol = const.get_object('titol')
        actual = const.get_object('actual')
        usuari = const.get_object('usuari')
        regex = const.get_object('regex')
        enllacos = const.get_object('enllacos')
        capitol = const.get_object('capitol')
        peticio = (titol, actual, usuari, regex, enllacos, capitol)
        # TEXT
        label_idioma = const.get_object('label1')
        vista_text_ori = const.get_object('text-original')
        buffer_text_ori = vista_text_ori.get_buffer()
        vista_text_ca = const.get_object('text-catala')
        buffer_text_ca = vista_text_ca.get_buffer()
        text = (buffer_text_ori,buffer_text_ca,label_idioma)
        # PARAULES NO TRADUIDES
        no_trad = const.get_object('mot-no-trad')
        mot_trad = const.get_object('entry1')
        mots = no_trad
        boto_ok_mot = const.get_object('button1')
        boto_ok_mot.connect('clicked',self.motTrad)
        boto_altre_mot = const.get_object('button2')
        boto_altre_mot.connect('clicked',self.altreMot)
        # PLANTILLES
        plant_ori = const.get_object('plantilla-original')
        plant_ca = const.get_object('plantilla-catala')
        self.tupla_ori = []
        self.tupla_ca = []
        self.llista_ori = const.get_object('plant-ori')
        self.llista_ca = const.get_object('plant-ca')
        self.llista_final = const.get_object('plant-final')
        plantilles = (self.llista_ori,self.llista_ca,self.llista_final,self.tupla_ori, self.tupla_ca,plant_ori,plant_ca)
        marca_ori = const.get_object('cellrenderertoggle1')
        marca_ori.connect('toggled',self.marcaOri)
        marca_ca = const.get_object('cellrenderertoggle2')
        marca_ca.connect('toggled',self.marcaCa)
        marca_final = const.get_object('cellrenderertoggle3')
        marca_final.connect('toggled',self.marcaFinal)
        boto_cancella = const.get_object('button3')
        boto_cancella.connect('clicked', self.cancella)
        boto_desfes = const.get_object('button4')
        boto_desfes.connect('clicked',self.desfes)
        boto_afegir = const.get_object('button5')
        boto_afegir.connect('clicked',self.afegir)
        boto_desa = const.get_object('button6')
        boto_desa.connect('clicked',self.desaPlantilla)
        # ENLLAÇOS
        enllac_ori = const.get_object('enllac-original')
        enllac_ca = const.get_object('enllac-catala')
        enllacos = (enllac_ori,enllac_ca)
        # BARRES DE PROGRÉS I D'ESTAT
        progres_capitol = const.get_object('progressbar1')
        progres_prog = const.get_object('progressbar2')
        progres = (progres_capitol,progres_prog)

#####
# FINESTRA D'INICI
#####

        boto_inici = const.get_object('button7')
        boto_inici.connect('clicked', self.comenca)
        self.bot = const.get_object('radiobutton2')
        self.bot.connect('toggled',self.botMarca)
        self.manual = const.get_object('radiobutton1')
        self.gravar_viqui = const.get_object('checkbutton1')
        self.boto_proves = const.get_object('checkbutton9')
        self.boto_proves.connect('toggled',self.proves)
        self.prova_plant = const.get_object('checkbutton2')
        self.prova_plant.connect('toggled', self.comprovaProves)
        self.prova_enllac = const.get_object('checkbutton3')
        self.prova_enllac.connect('toggled', self.comprovaProves)
        self.prova_commons = const.get_object('checkbutton4')
        self.prova_commons.connect('toggled', self.comprovaProves)
        self.prova_webs = const.get_object('checkbutton5')
        self.prova_webs.connect('toggled', self.comprovaProves)
        self.prova_altres = const.get_object('checkbutton6')
        self.prova_altres.connect('toggled', self.comprovaProves)
        self.prova_trad = const.get_object('checkbutton7')
        self.prova_trad.connect('toggled', self.comprovaProves)
        self.escollir_capitol = const.get_object('checkbutton8')
        self.escollir_capitol.connect('toggled',self.escollirCapitol)
        self.capitol_escollit = const.get_object('spinbutton1')
        self.capitol_escollit.connect('value-changed',self.numCapitol)
        self.n_cap = self.capitol_escollit.get_value()
        self.avis = const.get_object('avis')
        self.alerta = const.get_object('alerta')
        self.vista_alerta = const.get_object('box2')

        self.idioma_manual_escull = const.get_object('triar-idioma')
        self.idioma_manual_escull.connect('changed',self.idiomaNou)
        self.nou_idioma_manual = const.get_object('nou-idioma')
        self.titol_manual = const.get_object('titol-original')
        self.titol_manual_escull = const.get_object('titol-escollit')
        self.regex_manual = const.get_object('checkbutton11')
        self.regex_manual.connect('toggled',self.mostraRegex)
        self.regex_manual_escull = const.get_object('triar-regex')
        self.regex_manual_escull.connect('changed',self.regexManual)
        self.nova_regex_manual = const.get_object('nou-regex')
        self.mostra_titol = const.get_object('checkbutton10')
        self.mostra_titol.connect('toggled',self.mostraTitol)
        self.enllacos_manual = const.get_object('checkbutton12')

        # VISIBILITAT
        self.vista_total = const.get_object('programa')
        self.vista_mots = const.get_object('mots')
        self.vista_plantilles = const.get_object('plantilles')
        self.vista_enllacos = const.get_object('caixa-enllacos')
        self.vista_proves = const.get_object('proves')
        self.vista_capitols = const.get_object('capitols')
        self.vista_manual = const.get_object('manual')
        self.vista_barra_eines = const.get_object('handlebox1')

        self.comprovaProves()

        self.widgets = (peticio,text,mots,plantilles,enllacos,self.comprova_proves,self.capitol_escollit,finestres,progres,['bot'])
        print self.widgets


        self.fin.show()

        if self.segona:
            self.comenca()

#####
# INICI
####

    def comenca(self, *args):
        print self.manual.get_active()
        if self.idioma_manual_escull.get_active_text() == 'Altres':
            try:
                self.idioma_original_escollit = self.nou_idioma_manual.get_text()
            except:
                self.alerta.set_text("Cal indicar un idioma nou\nsi no s'escull cap dels idiomes predeterminats")
                self.vista_alerta.set_visible(True)
                return

        if True not in self.comprova_proves:
            self.alerta.set_text('Cal marcar almenys una prova')
            self.vista_alerta.set_visible(True)
            return
        if self.manual.get_active():
            print u'Per aqui ha de passar'
            if self.titol_manual.get_text() == '' or self.idioma_original_escollit == '':
                self.alerta.set_text('Cal indicar un idioma\ni un títol')
                self.vista_alerta.set_visible(True)
                return

        if self.marca_inici:
            self.volem_sortir = False
            self.fin.destroy()
            self.fin_prog.show()
#            self.fin_prog.maximize()
            self.avis.set_text('Qualsevol canvi en la configuració inicial\ncaldrà reiniciar el programa')
            self.marca_inici = False
            self.peticions()
        else:
            self.volem_sortir = False
            self.fin.destroy()
            self.dibuixFinestra()

    def botMarca(self,cell_toggled):
        if self.bot.get_active():
            print u'Bot'
            self.vista_manual.set_visible(False)
            self.widgets[-1][0] = 'bot'
        else:
            self.widgets[-1][0] = 'manual'
            print u'Manual'
            self.vista_manual.set_visible(True)

# MANUAL

    def regexManual(self, *args):
        if self.regex_manual_escull.get_active_text() == 'Altres':
            self.nova_regex_manual.set_visible(True)
        else:
            self.nova_regex_manual.set_visible(False)
            self.regex_escollit = self.regex_manual_escull.get_active_text()

    def idiomaNou(self, *args):
        if self.idioma_manual_escull.get_active_text() == 'Altres':
            self.nou_idioma_manual.set_visible(True)
        else:
            self.nou_idioma_manual.set_visible(False)
            self.idioma_original_escollit = self.idioma_manual_escull.get_active_text()

    def mostraRegex(self, *args):
        if self.regex_manual.get_active():
            self.regex_manual_escull.set_visible(True)
        else:
            self.nova_regex_manual.set_visible(False)
            self.regex_manual_escull.set_visible(False)

    def mostraTitol(self, *args):
        if self.mostra_titol.get_active():
            self.titol_manual_escull.set_visible(True)
        else:
            self.titol_manual_escull.set_visible(False)

    def comprovaProves(self, *args):
        self.comprova_proves = (self.prova_plant.get_active(),
                                self.prova_enllac.get_active(),
                                self.prova_commons.get_active(),
                                self.prova_webs.get_active(),
                                self.prova_altres.get_active(),
                                self.prova_trad.get_active())

    def proves(self, giny):
        if giny.get_active():
            self.vista_proves.set_visible(True)
            self.gravar_viqui.set_active(False)
        else:
            self.vista_proves.set_visible(False)
            self.prova_plant.set_active(True)
            self.prova_enllac.set_active(True)
            self.prova_commons.set_active(True)
            self.prova_webs.set_active(True)
            self.prova_altres.set_active(True)
            self.prova_trad.set_active(True)

    def escollirCapitol(self, *args):
        if self.escollir_capitol.get_active():
            self.vista_capitols.set_visible(True)
        else:
            self.vista_capitols.set_visible(False)
            self.capitol_escollit.set_value(0)

    def numCapitol(self, giny):
        self.n_cap = giny.get_value()
        print self.n_cap
        return self.n_cap

###
# BARRA
####

    def edita(self, *args):
        print u'Editem text'
        self.fs(None,False).parem = True

    def desaDicc(self, *args):
        print u'Desem el diccionari de mots'

    def motTrad(self, *args):
        print u'Afegit el mot traduït'

    def altreMot(self, *args):
        print u'Mot que no cal traduir, passem al següent'

##########
# FINESTRA DE PLANTILLES
##########

    def mostraPlantilla(self, *args):
        self.fin_plant.show()

    def vista_ori(self, path, cell_toggled):
        print "S'maga?"
        iter_amaga = self.llista_original.get_iter(cell_toggled)
        self.llista_original.set_value(iter_amaga,1,False)
        self.llista_original.set_value(iter_amaga,0,'z')

    def vista_ca(self, path, cell_toggled):
        iter_amaga = self.llista_catala.get_iter(cell_toggled)
        self.llista_catala.set_value(iter_amaga,1,False)
        self.llista_catala.set_value(iter_amaga,0,'z')

    def marca(self,path,cell_toggled):
        iter_marca = self.llista_tria.get_iter(Gtk.TreePath(cell_toggled))
        bol = self.llista_tria.get_value(iter_marca,2)
        self.llista_tria.set_value(iter_marca,2,not bol)
        marca_fill = not bol
        print self.llista_tria.iter_has_child(iter_marca)
        if self.llista_tria.iter_has_child(iter_marca) == True:
            iter_fill = self.llista_tria.iter_children(iter_marca)
            while iter_fill:
                self.llista_tria.set_value(iter_fill,2,marca_fill)
                iter_fill = self.llista_tria.iter_next(iter_fill)


        print cell_toggled
        print len(cell_toggled)

    def marcaOri(self,path, cell_toggled):
        path = Gtk.TreePath(cell_toggled)
        iter_marca = self.llista_ori.get_iter(path)
        bol = self.llista_ori.get_value(iter_marca,3)
        print self.llista_ori.get_value(iter_marca,0)
        self.llista_ori.set_value(iter_marca,2,not bol)
        if not bol == False: self.escull -= 1
        else: self.escull += 1

    def marcaCa(self,path, cell_toggled):
        path = Gtk.TreePath(cell_toggled)
        iter_marca = self.llista_ca.get_iter(path)
        bol = self.llista_ca.get_value(iter_marca,3)
        print self.llista_ca.get_value(iter_marca,0)
        self.llista_ca.set_value(iter_marca,2,not bol)

    def marcaFinal(self, path, cell_toggled):
        print u'He marcat un paràmetre final'

    def desaPlantilla(self,*args):
        text = u''
        pagina = 'Usuari:Anskarbot/'+self.idioma_original+'/Plantilles'
        pagina = wikipedia.Page('ca',pagina)
        try:
            text = pagina.get()
        except:
            pass
        text += u"\n=="+self.tupla_ca[0]+u"=="
        for x in range(len(self.llista_tria)):
            iter_pare = self.llista_tria.get_iter(x)
            parametre_ca = self.llista_tria.get_value(iter_pare,0)
            iter_fill = self.llista_tria.iter_children(iter_pare)
            while iter_fill:
                parametre_ori = self.llista_tria.get_value(iter_fill,1)
                iter_fill = self.llista_tria.iter_next(iter_fill)
                text += u'\n'+unicode(parametre_ori.decode('utf-8'))+u';'+unicode(parametre_ca.decode('utf-8'))
        pagina.put(text,u"Anskarbot traduïnt els paràmetres d'una nova plantilla")
        self.fin_plant.hide()

    def afegir(self, *args):
        self.ordre_ori.clicked()
        self.ordre_ca.clicked()
        parametre = [self.llista_catala.get_iter(Gtk.TreePath(x)) for x in range(len(self.llista_catala)) if self.llista_catala.get_value(self.llista_catala.get_iter(Gtk.TreePath(x)),3) == True][0]
        print self.tupla_ca[1][self.llista_catala.get_value(parametre,2)-1]
        del self.tupla_ca[1][self.llista_catala.get_value(parametre,2)-1]
        parametre = self.llista_catala.get_value(parametre,0)
        self.llista_tria.append(None,[parametre,None,False,True])
        parametres_ori = [self.llista_original.get_iter(Gtk.TreePath(x)) for x in range(len(self.llista_original)) if self.llista_original.get_value(self.llista_original.get_iter(Gtk.TreePath(x)),3) == True]
        for parametre in parametres_ori:
            del self.tupla_ori[1][self.llista_original.get_value(parametre,2)-1]
            parametre = self.llista_original.get_value(parametre,0)
            self.llista_tria.append(self.llista_tria.get_iter(Gtk.TreePath(len(self.llista_tria)-1)),[None,parametre, False,False])
        self.cons_ori()
        self.cons_ca()
        self.conta_par_ori.set_text(str(self.escull)+u':'+str(len(self.tupla_ori[1])))
        self.conta_par_ca.set_text(str(len(self.llista_tria))+u':'+str(len(self.tupla_ca[1])))
        self.final += 1
        self.par_ca.clicked()
        self.par_ori.clicked()

    def desfes(self, *args):
        esborra_pares = [self.llista_tria.get_iter(Gtk.TreePath(x)) for x in range(len(self.llista_tria)) if self.llista_tria.get_value(self.llista_tria.get_iter(Gtk.TreePath(x)),2) == True]
        print esborra_pares

        pass

    def cancella(self, *args):

        llista_ca = []
        llista_ori = []
        for x in range(len(self.llista_tria)):
            iter_pare = self.llista_tria.get_iter(Gtk.TreePath(x))
            llista_ca.append(self.llista_tria.get_value(iter_pare,0))
            iter_fill = self.llista_tria.iter_children(iter_pare)
            print llista_ca
            while iter_fill:
                llista_ori.append(self.llista_tria.get_value(iter_fill,1))
                iter_fill = self.llista_tria.iter_next(iter_fill)
            print llista_ori
        self.tupla_ca[1].extend(llista_ca)
        self.tupla_ori[1].extend(llista_ori)
        self.llista_tria.clear()
        self.escull = 0
        self.final = 0
        self.cons_ori()
        self.cons_ca()

####
# SORTIR
####

    def destroy(self, *args):
        Feines(None,False).paremThreads(True)
        if self.volem_sortir:
            self.sortir()

    def sortir(self, *args):
        Gtk.main_quit()


if __name__ == '__main__':
    try:
        Finestra.segona = False
        app = Finestra()
        app.dibuixFinestra()
        Gtk.main()

    finally:
        wikipedia.stopme()

