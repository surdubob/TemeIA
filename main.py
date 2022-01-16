"""
Dati enter dupa fiecare solutie afisata.

Presupunem ca avem costul de mutare al unui bloc egal cu indicele in alfabet,
cu indicii incepănd de la 1 (care se calculează prin 1+ diferenta dintre valoarea codului
ascii al literei blocului de mutat si codul ascii al literei "a" ) .
Astfel A* are trebui sa prefere drumurile in care se muta intai
blocurile cu infomatie mai mica lexicografic pentru a ajunge la una dintre starile scop

"""

import copy


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
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Lungime: ", len(l))
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

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        sir = ""
        maxInalt = max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva) < inalt:
                    sir += "  ".center(6)
                else:
                    sir += str(stiva[inalt - 1]).center(4) + " ".center(2)
            sir += "\n"
        sir += "-" * (2 * len(self.info) - 1)
        return sir

    """
    def __str__(self):
        sir=""
        for stiva in self.info:
            sir+=(str(stiva))+"\n"
        sir+="--------------\n"
        return sir
    """


class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        def obtineStive(sir):
            stiveSiruri = sir.strip().split('\n')
            listaStive = [sirStiva.strip().split('/') if sirStiva.strip() != "|" else [] for sirStiva in stiveSiruri]
            for st in listaStive:
                st[:] = [int(elem) for elem in st]
            return listaStive

        f = open(nume_fisier, 'r')

        continutFisier = f.read()  # citesc tot continutul fisierului
        self.start = obtineStive(continutFisier)
        print("Stare Initiala:", self.start)

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
        valid = self.testeaza_configuratie_valida(nodCurent.info)
        stive = nodCurent.info

        last = len(stive[0])
        i = 0
        for st in stive:
            if i != 0 and len(st) > last:
                return False

        return valid

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
        elif tip_euristica == "euristica admisibila 1":
            euristici = [0]
            last = len(infoNod[0])
            for i in range(1, len(infoNod)):
                if last < len(infoNod[i]):
                    euristici[0] += len(infoNod[i]) - last

            return min(euristici)
        elif tip_euristica == "euristica admisibila 2":
            euristici = []

            return min(euristici)
        else:  # tip_euristica=="euristica neadmisibila"
            euristici = []

            return max(euristici)

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def breadth_first(gr, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None)]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie:")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, "euristica admisibila 1")
        c.extend(lSuccesori)


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            input()
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
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


gr = Graph("input.txt")

# Rezolvat cu breadth first

# print("Solutii obtinute cu breadth first:")
# breadth_first(gr, nrSolutiiCautate=3)


print("\n\n##################\nSolutii obtinute cu A*:")
print("\nObservatie: stivele sunt afisate pe orizontala, cu baza la stanga si varful la dreapta.")
nrSolutiiCautate = 3
a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica admisibila 1")
