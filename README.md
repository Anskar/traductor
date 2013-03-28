Després de fer unes quantes traduccions automàtique m'adono que cal implementar una GUI per poder gestionar les traduccions dels paràmetres de plantilles per poder gravar els resultats a la viqui i utilitzar el diccionaari de paràmetres cada cop que una plantilla s'ha de traduir.
Posats a fer una GUI només per plantilles decideixo fer una GUI complerta per fer córrer l'Anskarbot de forma gràfica. M'adono que hi ha processos molt ferragosos i processos lleugers. Per això em plantejo implementar diversos fils per anar guanyant temps en les feines lleugeres i no haver d'esperar que acabin les ferragoses.


Gui Gtk del programa Anskarbot.

1.- El·laborar les finestres
2.- Crear threads per fer córrer procesos en paral·lel
