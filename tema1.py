# Autor: Surdu Bob Alexandru
# Grupa 352 , an 2022
# Exemplu de apelare: python tema1.py fisiere_input fisiere_output 20

import copy
import sys
from os import listdir
# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        global fisier_output
        l = self.obtineDrum()
        for nod in l:
            fisier_output.write(str(nod))
        if afisCost:
            fisier_output.write("\nCost: " + self.g.__str__())
        if afisLung:
            fisier_output.write("\nLungime: " + str(len(l)) + '\n')
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    def __str__(self):
        sir = "\n"
        sir += str(len(self.obtineDrum())) + ')\n'
        maxInalt = max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva) < inalt:
                    sir += "   ".center(5)
                else:
                    sir += ('|' + str(stiva[inalt - 1]) + "| ").center(4)
            sir += "\n"
        sir += "=" * (4 * len(self.info) + 2)
        return sir


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        global fisier_output

        def obtineStive(sir):
            stiveSiruri = sir.strip().split('\n')
            listaStive = [sirStiva.strip().split('/') if sirStiva.strip() != "|" else [] for sirStiva in stiveSiruri]
            for st in listaStive:
                st[:] = [int(elem) for elem in st]
            return listaStive

        f = open(nume_fisier, 'r')

        continutFisier = f.read()  # citesc tot continutul fisierului
        self.start = obtineStive(continutFisier)
        if not self.testeaza_configuratie_valida(self.start):
            self.start = []
            return
        fisier_output.write("Stare Initiala:" + self.start.__str__())

    def testeaza_configuratie_valida(self, infonod):
        stive = infonod
        i = 0
        for st in stive:
            if len(st) > 0:
                last = st[0]
                j = 0
                for elem in st:
                    if elem > last or (i != 0 and len(stive[i-1]) > j and stive[i-1][j] > stive[i][j]):
                        return False
                    last = elem
                    j += 1
            i += 1
        return True

    def testeaza_scop(self, nodCurent):
        stive = nodCurent.info

        last = len(stive[0])
        for st in stive[1:]:
            if len(st) > last:
                return False
            last = len(st)

        return True

    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        stive_c = nodCurent.info  # stivele din nodul curent
        nr_stive = len(stive_c)
        for idx in range(nr_stive):  # idx= indicele stivei de pe care iau bloc

            if len(stive_c[idx]) == 0:
                continue
            copie_interm = copy.deepcopy(stive_c)
            bloc = copie_interm[idx].pop()  # iau varful stivei
            for j in range(nr_stive):  # j = indicele stivei pe care pun blocul
                if idx == j:  # nu punem blocul de unde l-am luat
                    continue
                stive_n = copy.deepcopy(copie_interm)  # lista noua de stive
                stive_n[j].append(bloc)  # pun blocul
                if not self.testeaza_configuratie_valida(stive_n):
                    continue
                costMutareBloc = idx
                if not nodCurent.contineInDrum(stive_n):
                    nod_nou = NodParcurgere(stive_n, nodCurent, cost=nodCurent.g + costMutareBloc,
                                            h=self.calculeaza_h(stive_n, tip_euristica))
                    listaSuccesori.append(nod_nou)

        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if self.testeaza_configuratie_valida(infoNod):
                return 1  # se pune costul minim pe o mutare
            return 0
        elif tip_euristica == "euristica admisibila 1": # calculeaza cate stive nu au inaltimea necesara pentru
            euristici = [0]                             # a se indeplini conditia de scop
            last = len(infoNod[0])
            for i in range(1, len(infoNod)):
                if last < len(infoNod[i]):
                    euristici[0] += 1

            return min(euristici)
        elif tip_euristica == "euristica admisibila 2": # calculeaza costul mutarii blocurilor pentru a ajunge in stare scop
            euristici = [0]

            last = len(infoNod[0])
            for i in range(1, len(infoNod)):
                if last < len(infoNod[i]):
                    euristici[0] += (len(infoNod[i]) - last) * i  # i este costul unei mutari de pe stiva cu nr i

            return min(euristici)
        else:  # tip_euristica=="euristica neadmisibila"
            euristici = [0]

            inaltimi_stive = [len(st) for st in infoNod]

            euristici[0] = (max(inaltimi_stive) - min(inaltimi_stive)) * len(infoNod)

            return max(euristici)

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def breadth_first(gr, nrSolutiiCautate):
    global fisier_output
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None)]

    while len(c) > 0:
        # fisier_output.write("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            # fisier_output.write("\nSolutie calculata cu BF:")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            fisier_output.write("\n========================================\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, "euristica admisibila 1")
        c.extend(lSuccesori)


def a_star(gr, nrSolutiiCautate, tip_euristica):
    global fisier_output
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            fisier_output.write("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            fisier_output.write("\n========================================\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def ucs(gr, nrSolutiiCautate, tip_euristica):
    global fisier_output
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            fisier_output.write("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            fisier_output.write("\n========================================\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].g >= s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


input_dir = sys.argv[1]
output_dir = sys.argv[2]
nsol = int(sys.argv[3])
timeout = int(sys.argv[4])

fisiere_input = listdir(input_dir)
fisier_output = None

for f in fisiere_input:
    cale_fisier_output = output_dir + '/' + f
    fisier_output = open(cale_fisier_output, 'w')
    gr = Graph(input_dir + '/' + f)

    if not gr.start:
        fisier_output.write("Starea initiala este invalida")
        continue

    fisier_output.write("\nSolutie calculata cu BF:\n")
    breadth_first(gr, nrSolutiiCautate=nsol)

    fisier_output.write("\nSolutie calculata cu A*:\n")
    a_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica admisibila 1")

    fisier_output.write("\nSolutie calculata cu UCS:\n")
    ucs(gr, nsol, tip_euristica="euristica admisibila 2")
