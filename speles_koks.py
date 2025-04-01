from collections import deque

# Klase Virsotne – reprezentē spēles stāvokli (simbolu virkni, punktus un koka dziļumu)
#----------------------------------------------------------------------------------------
class Virsotne:
    def __init__(self, virkne, punkti_o=0, punkti_x=0, dzilums=0):
        """Inicializē virsotni ar spēles stāvokli, spēlētāju punktiem un dziļumu."""
        self.virkne = virkne               # Simbolu virkne, kas attēlo spēles stāvokli
        self.garums = len(virkne)          # Virknes garums
        self.punkti_o = punkti_o           # Spēlētāja O punkti
        self.punkti_x = punkti_x           # Spēlētāja X punkti
        self.dzilums = dzilums             # Virsotnes dziļums spēles kokā
        self.prieksteci = set()            # Iepriekšējās virsotnes, no kurām var nonākt šajā stāvoklī
        self.pecteci = []                  # Nākamās virsotnes (pēcteči)
        self.novertejums = None            # Novērtējuma vērtība (piemēram, minimax algoritmam)

    def add_priekstecis(self, virsotne):
        """Pievieno citu virsotni kā priekšteci (iepriekšējo stāvokli)."""
        self.prieksteci.add(virsotne)
    
    def add_pectecis(self, virsotne):
        """Pievieno citu virsotni kā pēcteci (turpmāko gājienu rezultātu)."""
        if virsotne not in self.pecteci:
            self.pecteci.append(virsotne)
    
    def __eq__(self, other):
        """Salīdzina divas virsotnes pēc stāvokļa un punktiem."""
        if not isinstance(other, Virsotne):
            return False
        return (self.virkne == other.virkne and 
                self.punkti_o == other.punkti_o and 
                self.punkti_x == other.punkti_x)
    
    def __hash__(self):
        """Aprēķina virsotnes hash vērtību, lai to var izmantot vārdnīcās."""
        return hash((self.virkne, self.punkti_o, self.punkti_x))
    
    def __str__(self):
        """Atgriež lasāmu virsotnes tekstuālo attēlojumu."""
        return f"[{self.virkne}] [O={self.punkti_o}, X={self.punkti_x}]"
    
    def __repr__(self):
        """Atgriež virsotnes programmatisko attēlojumu."""
        return f"Virsotne('{self.virkne}', {self.punkti_o}, {self.punkti_x}, {self.dzilums})"


# Klase SpelesKoks – pārvalda spēles koka ģenerēšanu un struktūru
#----------------------------------------------------------------------------------------
class SpelesKoks:
    def __init__(self, sakmes_virkne, max_dzilums=5):
        """Inicializē spēles koku ar sākuma virkni un maksimālo dziļumu, lai ierobežotu koka augšanu."""
        self.sakmes_virkne = sakmes_virkne
        self.max_dzilums = max_dzilums       # Maksimālais dziļums, līdz kuram tiks ģenerēts koks
        self.speles_koks = {}               # Vārdnīca, kas sasaista virsotnes ar to pēctečiem
        self.virsotnu_saraksts = {}          # Saglabā visas unikālās virsotnes

    def generet_saknes_koku(self):
        """Ģenerē sākuma koku no saknes virknes un sāk ģenerēšanu ar spēlētāju 'O'."""
        saknes_virsotne = Virsotne(self.sakmes_virkne)
        self.virsotnu_saraksts[saknes_virsotne] = saknes_virsotne
        self.speles_koks[saknes_virsotne] = []
        self._generet_apakskoku(saknes_virsotne, "O", 0)
        return saknes_virsotne
    
    def _generet_apakskoku(self, virsotne, speletajs, dzilums):
        """Rekursīvi ģenerē apakškoku, kamēr nav sasniegts maksimālais dziļums vai spēle beidzas."""
        if dzilums >= self.max_dzilums or len(virsotne.virkne) <= 1:
            return
        
        # Nākamais spēlētājs X vai O
        pretinieks = "X" if speletajs == "O" else "O"
        # Aprēķina iespējamos nākamos stāvokļus (gājienus)
        pecteci = self._aprekinat_iespejas(virsotne, speletajs)
        
         # Katru iespējamo jauno stāvokli apstrādā atsevišķi
        for pectecis in pecteci:
            pectecis.dzilums = dzilums + 1
            
             # Ja stāvoklis jau eksistē, savieno to ar pašreizējo virsotni
            if pectecis in self.virsotnu_saraksts:
                pectecis = self.virsotnu_saraksts[pectecis]
                if virsotne not in pectecis.prieksteci:
                    pectecis.add_priekstecis(virsotne)
                    virsotne.add_pectecis(pectecis)
            # Ja stāvoklis ir jauns, pievieno kokam un turpina ģenerēt tālāk dziļumā
            else:
                self.virsotnu_saraksts[pectecis] = pectecis
                self.speles_koks[pectecis] = []
                pectecis.add_priekstecis(virsotne)
                virsotne.add_pectecis(pectecis)
                # Rekursīvi ģenerē nākamo dziļumu
                self._generet_apakskoku(pectecis, pretinieks, dzilums + 1)
        
         # Saglabājā pašreizējās virsotnes pēctečus spēles kokā
        self.speles_koks[virsotne] = virsotne.pecteci
    
    def _aprekinat_iespejas(self, virsotne, speletajs):
        """Aprēķina visus iespējamos gājienus no dotās virsotnes, ievērojot spēles noteikumus."""
        virkne = virsotne.virkne
        pecteci = []
        
        if len(virkne) <= 1:
            return pecteci
        
        for i in range(len(virkne) - 1):
            jauna_virkne = None
            punkti = 0
            
            if speletajs == "O":  # Spēlētājs ar aplīšiem
                # Ja atrasts pāris "XX", aizvieto ar 'O' un piešķir 2 punktus
                if i < len(virkne) - 1 and virkne[i:i+2] == "XX":
                    jauna_virkne = virkne[:i] + "O" + virkne[i+2:]
                    punkti = 2
                # Ja atrasts pāris "XO", aizvieto ar 'O' un piešķir 1 punktu
                elif i < len(virkne) - 1 and virkne[i:i+2] == "XO":
                    jauna_virkne = virkne[:i] + "O" + virkne[i+2:]
                    punkti = 1
            else:  # Spēlētājs ar krustiņiem (X)
                # Ja atrasts pāris "OO", aizvieto ar 'X' un piešķir 2 punktus
                if i < len(virkne) - 1 and virkne[i:i+2] == "OO":
                    jauna_virkne = virkne[:i] + "X" + virkne[i+2:]
                    punkti = 2
                # Ja atrasts pāris "OX", aizvieto ar 'X' un piešķir 1 punktu
                elif i < len(virkne) - 1 and virkne[i:i+2] == "OX":
                    jauna_virkne = virkne[:i] + "X" + virkne[i+2:]
                    punkti = 1
            
            if jauna_virkne:
                # Izveido jaunu virsotni ar atjaunotajiem punktiem
                jauni_punkti_o = virsotne.punkti_o + (punkti if speletajs == "O" else 0)
                jauni_punkti_x = virsotne.punkti_x + (punkti if speletajs == "X" else 0)
                pecteci.append(Virsotne(jauna_virkne, jauni_punkti_o, jauni_punkti_x))
        
        return pecteci
    
    def generet_nakamo_dzilumu(self, virsotne, speletajs):
        """Ģenerē nākamo dziļuma līmeni spēles kokā no dotās virsotnes."""
        jaunas_virsotnes = []
        virsotnu_skaits = 0
        
        if not virsotne.pecteci or len(virsotne.virkne) <= 1:
            pecteci = self._aprekinat_iespejas(virsotne, speletajs)
            pretinieks = "X" if speletajs == "O" else "O"
            
            for pectecis in pecteci:
                virsotnu_skaits += 1
                pectecis.dzilums = virsotne.dzilums + 1
                
                if pectecis in self.virsotnu_saraksts:
                    pectecis = self.virsotnu_saraksts[pectecis]
                    if virsotne not in pectecis.prieksteci:
                        pectecis.add_priekstecis(virsotne)
                        virsotne.add_pectecis(pectecis)
                else:
                    self.virsotnu_saraksts[pectecis] = pectecis
                    self.speles_koks[pectecis] = []
                    pectecis.add_priekstecis(virsotne)
                    virsotne.add_pectecis(pectecis)
                    jaunas_virsotnes.append(pectecis)
                    # Dziļāku līmeņu ģenerēšana tiek izlaista, lai izvairītos no pārlielas augšanas.
            
            self.speles_koks[virsotne] = virsotne.pecteci
        
        print(f"Ģenerēts {virsotnu_skaits} jaunas virsotnes no {virsotne}")
        return jaunas_virsotnes
    
    def koka_karte(self):
        """Izvada visu spēles koka pārejas ceļu, lai parādītu virsotņu savstarpējo saikni."""
        for virsotne, pecteci in self.speles_koks.items():
            if pecteci:
                for pec in pecteci:
                    print(f"{virsotne} --> {pec}")
            else:
                print(f"{virsotne} --> Nav pēcteču")



# Testa kods
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    sakuma_virkne = "OXXX"  # Testa sākuma simbolu virkne
    koks = SpelesKoks(sakuma_virkne)
    koks.generet_saknes_koku()  # Ģenerē sākuma koku
    koks.koka_karte()          # Izvada koka pārejas ceļu
