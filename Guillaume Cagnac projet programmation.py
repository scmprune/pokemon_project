import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from math import cos, sin, sqrt
from time import sleep
from functools import partial

def erreur(error):
    # pour afficher les erreurs sur l'interface graphique et pas dans la console
    messagebox.showerror('Erreur', error)



#Sert à savoir si il y a une statistique qui est le total des autres
def totaldansfichier(listestats):
    total = False
    for nom in listestats:
        for j in range(4):
            i = pokemons.iloc[j]
            somme = 0
            for nom2 in listestats:
                if nom != nom2:
                    print(i[nom2])
                    somme += int(i[nom2])
            if somme == i[nom]:
                total = True
                return (total, nom)
    return (total, None)



#Pour traiter les colonnes différement et pour savoir sur lesquelles on va faire une analyse statistique
def traitementfichier():    
    listepetit = []
    listegrand = []
    for i in pokemons:
        if len(set(pokemons[i])) > 20:
            listegrand.append(i)
        else:
            listepetit.append(i)
    return (listepetit, listegrand)


##########
#Calcul la distance entre deux points dans un espace à deux dimensions
def distance(point1, point2):
    return sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

#Sert à voir si le signe est positif ou pas
def signe(x):
    if round(x, 3) >= 0:
        return True
    elif round(x, 3) < 0:
        return False

#Sert à projeter un point sur le segment qui passe par les points (x0,y0) et (xf,yf)
def projete(point, x0, y0, xf, yf):
    X = ((xf - x0) * (point[0] - xf) + (yf - y0) * (point[1] - yf)) / distance((x0, y0), (xf, yf)) ** 2
    projetex = xf + (xf - x0) * X
    projetey = yf + (yf - y0) * X
    return ((round(projetex), round(projetey)))





#Classe qui définit la zone d'affichage pour les pokemons
class zonneaffichagepokemon():
    def __init__(self, frame, largeur, hauteur, pokemon):
        self.frame = frame
        self.hauteur = hauteur
        self.largeur = largeur
        self.pokemon = pokemon
        self.image = None
        self.affichenom = None
        self.affichestat = None
        self.radar = None

#Organise la zone d'affichage
    def miseenplace(self):

        self.affichenom = tk.Label(self.frame, relief="raised", bg='gold2',
                                   text=f'{self.pokemon["#"].values[0]}  {self.pokemon["Name"].values[0]}',
                                   font=("Arial", 12))
        self.affichenom.place(relx=0.05, rely=0.1, width=self.largeur * 0.4, height=30)
        image = Image.open(f'/Users/killianguillaume/Desktop/python/pokemon/Images pokemons/{int(self.pokemon["#"])}.png')
        img = ImageTk.PhotoImage(image.resize((round(self.largeur * 0.4), round(self.hauteur * 0.4))))
        self.zoneimage = tk.Canvas(self.frame, width=img.width(), height=img.height())
        self.zoneimage.place(relx=0.05, rely=0.2)
        self.zoneimage.create_image(0, 0, anchor=tk.NW, image=img)
        self.zoneimage.image = img
        dicpok = {}
        stats = listegrand[2:]
        for nomstat in stats:
            if pokemons[nomstat].dtypes != 'int64':
                stats.remove(nomstat)
        verif, nomtotal = totaldansfichier(stats)
        if verif:
            stats.remove(nomtotal)
        self.affichestat = ttk.Treeview(self.frame, columns=["Nom", "Valeur"], show='headings', height=len(stats))
        self.affichestat.column("Nom", width=round(self.hauteur * 0.225), anchor="center")
        self.affichestat.column("Valeur", width=round(self.hauteur * 0.225), anchor="center")
        self.affichestat.heading("Nom", text="Statistique")
        self.affichestat.heading("Valeur", text="Valeur")
        self.affichestat.place(relx=0.5, rely=0.1)
        for nomstat in stats:
            dicpok[nomstat] = int(self.pokemon[nomstat])
            self.affichestat.insert('', index=tk.END, values=[nomstat, int(self.pokemon[nomstat])])
        self.radar = graph(self.frame, True, dicpok, self.hauteur * 0.45)
        self.radar.configuration()
        self.radar.place(relx=0.5, rely=0.5)





#Classe qui définit une zone de recherche pour le nom des pokemons
#C'est un héritage d'un Entry et le but est qu'il propose les noms existants commençant par ce que l'on tape
class entryrecherchenom(tk.Entry):
    def __init__(self, frame, textvar):
        super().__init__(frame, textvariable=textvar)
        self.bind('<Key>', self.afficherrecherchenom)
        self.frame = frame
        self.textvar = textvar
        self.carac = ''
        self.tableaunom = None

#Créé le tableau qui contient les noms commençant par ce que contient le entry
#On construit le caractère petit à petit 
    def afficherrecherchenom(self, event):
        if self.textvar.get() == "":
            self.carac = ""
        if event.keysym == 'BackSpace':
            self.carac = self.carac[:-1]
        else:
            self.carac += event.char
        if self.tableaunom == None:
            self.tableaunom = ttk.Treeview(self.frame, columns=["Name"], show='headings')
            self.tableaunom.heading("Name", text="Name")
            self.tableaunom.column("Name", anchor="center")
            self.tableaunom.grid(column=1, row=3)
            self.tableaunom.bind("<Button-1>", self.clicbarrerecherche)
        else:
            self.tableaunom.delete(*self.tableaunom.get_children())
        names = pokemons[pokemons["Name"].str.startswith(self.carac)]["Name"]
        for i in names:
            self.tableaunom.insert("", index=tk.END, values=[i])
            
            
#Sert à ce qu'on puisse choisir un nom dans le tableau créé au dessus
#Quand on clique le entry prend ce nom en valeur,le tableau se détruit et le caractère se réinitialise
    def clicbarrerecherche(self, event):
        item = self.tableaunom.focus()
        if item:
            self.textvar.set(self.tableaunom.set(item, column="Name"))
            self.tableaunom.destroy()
            self.tableaunom = None
            self.carac = ""




#La classe des graphiques radar. Deux possibilités True, le radar est voué à afficher les stats d'un pokemon
#False le radar nous sert à faire une recherche
class graph(tk.Canvas):
    def __init__(self, fenetre, choix, stats, taille):
        super().__init__(fenetre, height=taille, width=taille, bg="black", confine=True)
        self.taille = taille
        self.fenetre = fenetre
        self.stats = stats
        self.choix = choix
        if not self.choix:
            self.listeligne = []
            self.lastclic = None
            self.bind("<Button-1>", self.evenementClicG)

#Dessine l'interface du radar et dessine le polygone si True et stock les points qui sont au bout des lignes si False
#Cela servira à projeter les points qu'on dessinera sur les segments entre ces points et le centre
    def configuration(self):
        nombrestat = len(self.stats)
        points = []
        for rayon in [0.4 * round(self.taille) * i / 5 for i in range(1, 6)]:
            self.create_oval(round(self.taille / 2) - rayon, round(self.taille / 2) - rayon,
                             round(self.taille / 2) + rayon, round(self.taille / 2) + rayon, outline='green')
        i = 0
        for nomstat in self.stats:
            angle = 3 * np.pi / 2 + (np.pi * 2 * i / nombrestat)
            xf = int(self.taille / 2 + 0.4 * round(self.taille) * cos(angle))
            yf = int(self.taille / 2 + 0.4 * round(self.taille) * sin(angle))
            self.create_line(self.taille / 2, self.taille / 2, xf, yf, fill='green')
            i += 1
            message = tk.Label(self, text=nomstat, bg='black', fg='white', font=("Courrier", round(self.taille / 33)))

            if signe(cos(angle)) :
                if signe(sin(angle)) :
                    message.place(x=xf + 2, y=yf + 2)
                else:
                    message.place(x=xf, y=yf - self.taille / 16)

            else:
                if not signe(sin(angle)):
                    message.place(x=xf - self.taille / 7, y=yf - self.taille / 16)
                else:
                    message.place(x=xf - self.taille / 7, y=yf)
            if not self.choix:
                self.listeligne.append((xf, yf))
        if self.choix:
            self.transformationspoints()


#Sert à tracer le polygone représentant les stats
#Hors de configuration pour permettre de dessiner un autre radar sur le même graphique
    def transformationspoints(self, color='red'):
        points = []
        i = 0
        for nomstat in self.stats:
            angle = 3 * np.pi / 2 + (np.pi * 2 * i / len(self.stats))
            i += 1
            points.append((self.taille / 2 + cos(angle) * (int(self.stats[nomstat]) / 230 * 0.4 * round(self.taille)),
                           self.taille / 2 + sin(angle) * (int(self.stats[nomstat]) / 230 * 0.4 * round(self.taille))))
        self.create_polygon([points[i] for i in range(len(points))], fill="", outline=color,
                            width=3, activefill=color, activestipple='gray25')

#Partie pour récupérer la position de notre clic
    def evenementClicG(self, event):
        self.lastclic = event

    def recupererClic(self):
        self.fenetre.focus()
        self.update()
        clic = self.lastclic
        self.lastclic = None
        return clic

    def attendreClic(self):
        clic = None
        while clic == None:
            sleep(0.1)
            clic = self.recupererClic()
        return clic

#Fonction qui permet de dessiner notre propre polygône. Elle renvoie la liste des points que l'on a dessiné.
    def dessin(self, color):
        points = []
        i = 0
        while i < len(self.listeligne):
            clic = self.attendreClic()
            if min(self.listeligne[i][0] - 3, self.taille / 2 - 3) <= clic.x <= max(self.listeligne[i][0] + 3,
                                                                                    self.taille / 2 + 3) and min(
                    self.listeligne[i][1] - 3, self.taille / 2 - 3) <= clic.y <= max(self.listeligne[i][1] + 3,
                                                                                     self.taille / 2 + 3):
                projete_clic = projete((clic.x, clic.y), round(self.taille / 2), round(self.taille / 2),
                                       self.listeligne[i][0], self.listeligne[i][1])
                self.create_oval(projete_clic[0] - 3, projete_clic[1] - 3, projete_clic[0] + 3, projete_clic[1] + 3,
                                 outline='red', fill='red')
                points.append(projete_clic)
                if i != 0:
                    self.create_line(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1], fill=color,
                                     width=3)
                i += 1
        self.create_line(points[i - 1][0], points[i - 1][1], points[0][0], points[0][1], fill=color, width=3)
        return (points)

########
#interface graphique + analyse statistique
class Pokedex():
    def __init__(self):
        self.fenetre = tk.Tk()
        self.liste_element = []
        for element in pokemons:
            self.liste_element.append(element)
        self.dic = {}
        self.diccomparer = {}
        self.dicostat = {}
        self.item = None
        self.radar2 = None

#La grosse fonction de recherche
#L'idée est de récupérer chaque condition, mettre les noms des pokemons vérifiant cette condition dans un set
#Puis de faire l'intersection de tous les sets pour ne garder que ceux qui vérifient toutes les conditions
    def rechercher1(self):
        if self.radar2:
            self.radar2.destroy()
            self.bouton_effacer.destroy()
            self.radar2 = None
        for item in self.table.get_children():
            self.table.delete(item)
        listeset = []
        #on récupère les conditions données par l'utilisateur et on les appliques suivant les types
        for nom_colonne in self.dic:
            condition = self.dic[nom_colonne].get()
            if condition != "" and condition != "Par Défault":
                if pokemons[nom_colonne].dtypes == 'int64':
                    if condition.isdigit() == False:
                        raise ValueError(erreur('Il faut rentrer un nombre entier pour les statistiques'))
                    if nom_colonne == "#":
                        listenom = pokemons[pokemons[nom_colonne] == int(condition)]["Name"]
                    else:
                        objcomparateur = self.diccomparer[nom_colonne].get()
                        if objcomparateur == ">=":
                            if int(condition) > pokemons[nom_colonne].max():
                                raise ValueError(erreur(
                                    'Le nombre rentré est supérieur au maximum possible\nconsulter la page "Information" qui se trouve en bas à droite.'))
                            listenom = pokemons[pokemons[nom_colonne] >= int(condition)]["Name"]
                        elif objcomparateur == "<=":
                            listenom = pokemons[pokemons[nom_colonne] <= int(condition)]["Name"]
                            if int(condition) < pokemons[nom_colonne].min():
                                raise ValueError(erreur(
                                    'Le nombre rentré est inférieur au minimum possible\nconsulter la page "Information" qui se trouve en bas à droite.'))
                        else:
                            if pokemons[pokemons[nom_colonne] == int(condition)].empty:
                                raise ValueError(erreur(
                                    'Aucun Pokemon ne correspond à votre demande\nconsulter la page "Information" qui se trouve en bas à droite.'))
                            listenom = pokemons[pokemons[nom_colonne] == int(condition)]["Name"]

                elif pokemons[nom_colonne].dtypes == 'bool':
                    if condition == "False":
                        condition = False
                    else:
                        condition = True
                    listenom = pokemons[pokemons[nom_colonne] == condition]["Name"]
                elif pokemons[nom_colonne].dtypes == 'object':
                    if condition.isdigit() == True:
                        raise ValueError(erreur('Il faut rentrer une chaine de caractère.'))
                    listenom = pokemons[pokemons[nom_colonne] == str(condition)]["Name"]
                setcond = set(i for i in listenom)
                listeset.append(setcond)
            #s'il n'y a pas de condition particulière, on rajoute toute la colonne
            if condition == "Par Défault" or condition == "":
                listenom = pokemons["Name"]
                setcond = set(i for i in listenom)
                listeset.append(setcond)
        names = listeset[0]
        for i in range(len(listeset)):
            names = names & listeset[i]
        resultat = pokemons[pokemons.Name.isin(names)]
        for i in range(len(resultat)):
            ligne = resultat.iloc[i]
            self.table.insert('', index=tk.END, values=[ligne[element] for element in self.liste_element])
        self.entry_nom.carac = ""
        self.entry_nom.textvar.set('')



#La fonction qui recherche les pokemons à partir du graph tracé
#Pour chaque point,on transforme linéairement les coordonnées en stats en utilisant la distance entre le point
#et le centre du graph
    def rechercherdessin(self):
        for item in self.table.get_children():
            self.table.delete(item)
        stats = listegrand[2:]
        for nomstat in stats:
            if pokemons[nomstat].dtypes != 'int64':
                stats.remove(nomstat)
        verif, nomtotal = totaldansfichier(stats)
        if verif:
            stats.remove(nomtotal)
        self.bouton_effacer = ttk.Button(self.fenetre, text='Effacer', command=self.effacer)
        self.bouton_effacer.place(relx=0.4,rely=0.65)
        taille = self.y * 0.35
        self.radar2 = graph(self.fenetre, False, stats, taille)
        self.radar2.configuration()
        self.radar2.place(relx=0.15,rely=0.58)
        points = self.radar2.dessin('red')
        listeset = []
        for i in range(len(stats)):
            valstat = round(distance(points[i], (round(taille / 2), round(taille / 2))) / (0.4 * round(taille)) * 230)
            listenom = pokemons[(valstat - 15 <= pokemons[stats[i]]) & (pokemons[stats[i]] <= valstat + 15)][
                "Name"]
            setcond = set(i for i in listenom)
            listeset.append(setcond)
        names = listeset[0]
        for i in range(len(listeset)):
            names = names & listeset[i]
        resultat = pokemons[pokemons.Name.isin(names)]
        for i in range(len(resultat.transpose())):
            ligne = resultat.iloc[i]
            self.table.insert('', index=tk.END, values=[ligne[element] for element in self.liste_element])
            
    def effacer(self):
            self.radar2.delete(all)
            self.rechercherdessin()
            
        
#Sert à créer la zone d'affichage conçue pour le pokemon choisi
    def afficherpokemon(self, event):
        self.item = self.table.focus()
        if self.item:
            pokemon = pokemons[pokemons["Name"] == self.table.set(self.item, column="Name")]
            if self.frame4 != None:
                self.frame4.destroy()
            self.frame4 = tk.Frame(self.fenetre)
            self.frame4.place(x=round(self.x *0.72), y=0, height=self.x * 0.28, width=self.x * 0.28)
            image = Image.open("/Users/killianguillaume/Desktop/python/pokemon/Images pokemons/Fond.png")
            image = image.resize((round(self.x * 0.28), round(self.x * 0.28)), Image.Resampling.BICUBIC)
            photo = ImageTk.PhotoImage(image)
            canevas = tk.Canvas(self.frame4, width=photo.width(), height=photo.height())
            canevas.place(x=0, y=0)
            canevas.create_image(0, 0, anchor=tk.NW, image=photo)
            canevas.image = photo
            self.zoneaffiche = zonneaffichagepokemon(self.frame4, self.x * 0.28, self.x * 0.28, pokemon)
            self.zoneaffiche.miseenplace()


    def bouton_menu(self, frame, recup, col, rg, choix):
        # bouton = ttk.OptionMenu(frame, recup, choix[0], *choix)
        # bouton.grid(column=col, row=rg)
        
        bouton = ttk.Combobox(frame, textvariable=recup, values=choix, state="readonly", font=('Arial', 12, 'bold'))
        bouton.grid(column=col, row=rg)
        
        # Appliquer un style au Combobox
        bouton.configure(style="TCombobox")

    
#Défini les variables en mettre dans des menus déroulant 
    def traitementfichierpoke(self):
        listemenuder = listepetit
        dico = {}
        for variable in listemenuder:
            l = []
            for j in pokemons[variable].unique():
                if j != '':
                    l.append(j)
            dico[variable] = l
        return dico



    def data(self, lbl, dic):
        df = pokemons
        listeset = []
        #on traite la bdd suivant les condition donnée par l'utilisateur dans l'interface graphique
        for nom_colonne in dic:
            condition = dic[nom_colonne].get()
            if condition != 'Par Défaut':
                if pokemons[nom_colonne].dtypes == 'int64':
                    listenom = pokemons[pokemons[nom_colonne] == int(condition)]["Name"]
                elif pokemons[nom_colonne].dtypes == 'bool':
                    if condition == "False":
                        condition = False
                    else:
                        condition = True
                    listenom = pokemons[pokemons[nom_colonne] == condition]["Name"]
                else:
                    listenom = pokemons[pokemons[nom_colonne] == condition]["Name"]
            elif condition == 'Par Défaut':
                #on créer le nouveau dataframe qui nous permettra de faire toutes les stat suivant toutes les
                #conditions données par l'utilisateur
                listenom = df["Name"]
            listeset.append(set(i for i in listenom))
        names = listeset[0]
        for i in range(1, len(listeset)):
            names = names & listeset[i]
        resultat = df[df.Name.isin(names)]
        nomstats = [i for i in pokemons]
        #on veut garder uniquement les colonnes où il est pertinent de faire une analyse (hp, attaque etc..)
        for j in pokemons:
            if j == 'Name' or j == '#' or df[j].dtypes != 'int64' or (j in listepetit):
                resultat = resultat.drop(columns=[j], axis=1)
                nomstats.remove(j)
        caractere = ''    
        for nom in nomstats:
            caractere += f'\n{nom}:\n'
            caractere += f'min = {resultat[nom].min()},\n'
            caractere += f'max = {resultat[nom].max()},\n'
            caractere += f'moyenne = {round(resultat[nom].mean(), 2)},\n' 
            caractere += f'nombre = {resultat[nom].count()},\n'
        lbl.config(text=caractere)

    def stat(self):
        #meme procédé que pour l'affichage de la fenetre principale
        #fenetre d'affichage pour le bouton information
        top = tk.Toplevel()
        top.title("Fenêtre d'informations")
        top.geometry('800x800')
        image = Image.open("/Users/killianguillaume/Desktop/python/pokemon/Images pokemons/wptop.png")
        image = image.resize((800, 800), Image.Resampling.BICUBIC)
        photo = ImageTk.PhotoImage(image)
        canevas = tk.Canvas(top, width=photo.width(), height=photo.height())
        canevas.place(x=0, y=0)
        canevas.create_image(0, 0, anchor=tk.NW, image=photo)
        canevas.image = photo
        dictionnaire = self.traitementfichierpoke()
        for i in dictionnaire:
            dictionnaire[i].insert(0, "Par Défaut")
        indice = 2
        for i in dictionnaire:
            texte = ttk.Label(top, text=i, background='orangered')
            texte.grid(column=1, row=indice)
            recup = tk.StringVar(top)
            self.bouton_menu(top, recup, 2, indice, choix=dictionnaire[i])
            self.dicostat[i] = recup
            indice += 1

        comp = ttk.Button(top, text='Afficher les informations')
        labelResultat = ttk.Label(top, text="", font=("Courrier", 10), background='orangered')
        labelResultat.place(x=0,y=120)
        comp.config(command=partial(self.data, labelResultat, self.dicostat))
        comp.grid(column=2, row=indice + 1, padx=5, pady=5)


    def topcomparer(self):
        #création fenetre après activation du bouton
        #utilisation du self pour pouvoir récupérer les variables dans les autres méthodes
        self.top = tk.Toplevel()
        self.top.title('Comparer 2 Pokemons')
        self.top.geometry('600x600')
        #fond d'écran
        image = Image.open("/Users/killianguillaume/Desktop/python/pokemon/Images pokemons/Fond.png")
        image = image.resize((600, 600), Image.Resampling.BICUBIC)
        photo = ImageTk.PhotoImage(image)
        canevas = tk.Canvas(self.top, width=photo.width(), height=photo.height())
        canevas.place(x=0, y=0)
        canevas.create_image(0, 0, anchor=tk.NW, image=photo)
        canevas.image = photo
        #interface utilisateur
        btn_compare = ttk.Button(self.top, text="Comparer", command=self.comparerpokemon)
        btn_compare.grid(column=2, row=3)
        poke1 = ttk.Label(self.top, text='Pokémon 1 (rouge)', background='red')
        poke2 = ttk.Label(self.top, text='Pokémon 2 (jaune)', background='yellow')
        poke1.grid(column=1, row=1)
        poke2.grid(column=2, row=1)
        self.varpoke1 = tk.StringVar(self.top)
        entrypoke1 = entryrecherchenom(self.top, self.varpoke1)
        self.varpoke2 = tk.StringVar(self.top)
        entrypoke2 = entryrecherchenom(self.top, self.varpoke2)
        entrypoke1.grid(column=1, row=2)
        entrypoke2.grid(column=2, row=2)

    def comparerpokemon(self):
        #méthode qui compare les stat des 2 pokemons qu'on veut comparer dans la fenetre "comparer pokemons
        pokemon1 = pokemons[pokemons["Name"] == self.varpoke1.get()]
        pokemon2 = pokemons[pokemons["Name"] == self.varpoke2.get()]
        dicpok1 = {}
        dicpok2 = {}
        stats = listegrand[2:]
        for nomstat in stats:
            if pokemons[nomstat].dtypes != 'int64':
                stats.remove(nomstat)
        verif, nomtotal = totaldansfichier(stats)
        if verif:
            stats.remove(nomtotal)
        for nomstat in stats:
            dicpok1[nomstat] = int(pokemon1[nomstat])
            dicpok2[nomstat] = int(pokemon2[nomstat])
        radar = graph(self.top, True, dicpok1, 350)
        radar.place(x=125,y=125)
        radar.configuration()
        #On trace le deuxième polygône sur le même graph
        radar.stats = dicpok2
        radar.transformationspoints("yellow")

    def creationinterface(self):
        style = ttk.Style()

        # Définir un style pour le label
        style.configure("TLabel", foreground="white", background="black", font=('Arial', 12, 'bold'))
        style.configure("TButton", foreground="white", background="black", font=('Arial', 12, 'bold'), padding=10)
        style.configure("TEntry", font=('Arial', 12, 'bold'), foreground='white', background='black')
        style.configure("TOptionMenu", foreground="black", background="white")

        style.configure("TTreeview", font=('Arial', 12, 'bold'), background="black", foreground="white")
        style.configure("TTreeview.Heading", font=('Arial', 12, 'bold', 'underline'), foreground='white', background="black")


        # Création de la fenetre principale
        self.fenetre.title("Recherche de Pokémon")
        # self.fenetre.attributes('-fullscreen', True)

        self.x = self.fenetre.winfo_screenwidth()
        self.y = self.fenetre.winfo_screenheight()

        self.fenetre.geometry(f'{self.x}x{self.y}')

        dictionnaire = self.traitementfichierpoke()
        for i in dictionnaire:
            dictionnaire[i].insert(0, "Par Défault")

        image_path = "/Users/killianguillaume/Desktop/python/pokemon/Images pokemons/wallpaperpoke.png"

        image = Image.open(image_path)
        image = image.resize((self.x, self.y), Image.Resampling.BICUBIC)
        photo = ImageTk.PhotoImage(image)

        canevas = tk.Canvas(self.fenetre, width=photo.width(), height=photo.height())
        canevas.place(x=0, y=0)

        canevas.create_image(0, 0, anchor=tk.NW, image=photo)
        canevas.image = photo

        # création des frame
        frame1 = tk.Frame(self.fenetre)
        frame1.place(relx=0.05,rely=0.05)
        frame2 = tk.Frame(self.fenetre)
        frame2.place(relx=0.05,rely=0.15)
        frame3 = tk.Frame(self.fenetre)
        frame3.place(relx=0.25,rely=0.05)

        self.frame4 = None

        # frame 1
        textenum = ttk.Label(frame1, text='Recherche par numéro : ')
        textenum.grid(column=0, row=0)
        texte_num = tk.StringVar(frame1)
        entry_num = ttk.Entry(frame1, textvariable=texte_num)
        entry_num.grid(column=1, row=0)
        self.dic['#'] = texte_num

        textenom = ttk.Label(frame1, text='Recherche par Nom : ')
        textenom.grid(column=0, row=1)
        texte_nom = tk.StringVar(frame1)
        self.entry_nom = entryrecherchenom(frame1, texte_nom)
        self.entry_nom.grid(column=1, row=1)
        self.dic["Name"] = texte_nom

        textef2 = ttk.Label(frame2, text='Catégories')
        textef2.grid(column=0, row=0)

        #frame 2
        indice1 = 2
        indice2 = 1
        comparer = ["=", ">=", "<="]
        for i in dictionnaire:
            textebool = ttk.Label(frame2, text=i)
            textebool.grid(column=0, row=indice1)
            recup = tk.StringVar(frame2)
            self.bouton_menu(frame2, recup, 1, indice1, choix=dictionnaire[i])
            self.dic[i] = recup
            indice1 += 1

        #frame3
        texteintgrand = ttk.Label(frame3, text="Statistiques :")
        texteintgrand.grid(column=0, row=0)
        indice3 = indice1
        #on regroupe ici les colonnes avec beaucoup de données différentes (hp, attaque, etc...)
        for j in listegrand:
            if j != "#" and j != "Name":
                recupintgrand = tk.StringVar(frame3)
                txt = ttk.Label(frame3, text=j)
                ent = tk.StringVar(frame3)
                entrytxt = ttk.Entry(frame3, textvariable=ent)
                self.bouton_menu(frame3, recupintgrand, 1, indice3, choix=comparer)
                txt.grid(column=0, row=indice3)
                entrytxt.grid(column=2, row=indice3)
                self.dic[j] = ent
                self.diccomparer[j] = recupintgrand
                indice3 += 1

        bouton_comparer = ttk.Button(self.fenetre, text='Comparer 2 Pokemons', command=self.topcomparer)
        bouton_comparer.place(relx=0.6,rely=0.6)

        escape = ttk.Label(self.fenetre, text="Cliquer sur 'esc' pour fermer la fenetre.")
        escape.place(y=self.y - 100)
        self.fenetre.bind('<Escape>', lambda event: self.fenetre.quit())

        bouton_info = ttk.Button(self.fenetre, text='Information', command=self.stat)
        bouton_info.place(relx=0.6,rely=0.65)

        bouton_recherche = ttk.Button(self.fenetre, text='Recherche', command=self.rechercher1)
        bouton_recherche.place(relx=0.05,rely=0.3)

        bouton_dessin = ttk.Button(self.fenetre, text='Dessiner', command=self.rechercherdessin)
        bouton_dessin.place(relx=0.4,rely=0.6)

        # Créer la zone d'affichage des résultats
        self.table = ttk.Treeview(self.fenetre, columns=self.liste_element, show='headings')
        for j in self.liste_element:
            self.table.heading(j, text=j)
            self.table.column(j, width=round(self.x * 0.7 / len(self.liste_element)), anchor="center")
        self.table.bind("<Button-1>", self.afficherpokemon)
        self.table.place(relx=0.01,rely=0.35,relheight=0.2)
        self.fenetre.mainloop()


pokemons = pd.read_csv("/Users/killianguillaume/Desktop/python/pokemon/Pokemon.csv")
pokemons = pokemons.fillna('')
listepetit,listegrand=traitementfichier()
Pk = Pokedex()
Pk.creationinterface()


