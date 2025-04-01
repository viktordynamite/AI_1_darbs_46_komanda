import random

class Minimax:
    def __init__(self, maks_dzilums=5, alpha_beta = False):
        """Inicializē minimax un alpha_beta algoritmu."""
        self.maks_dzilums = maks_dzilums # Maksimālais dziļums, līdz kuram meklēt gājienus (noklusējuma vērtība: 5)
        self.alpha_beta = alpha_beta # Ja vērtība ir True, izmanto alpha_beta algoritmu

    def _aprekinat_novertejumus(self, virsotne, dzilums, maksimize, speletajs, alpha = float('-inf'), beta = float('inf')):
        """Minimax algoritma rekursīvā implementācija ar opcionāliem alpha-beta nogriešanas parametriem."""
        # Ja virsotne jau ir novērtēta, atgriež to pašu vērtību
        if virsotne.novertejums is not None:
            return virsotne.novertejums
            
        # Ja sasniegts maksimālais dziļums vai virsotne ir strupceļa virsotne
        if dzilums >= self.maks_dzilums or not virsotne.pecteci:
            # Aprēķina punktu starpību atkarībā no tā, kurš ir dators
            if speletajs == "O":
                # Ja O ir dators
                punktu_starpiba = virsotne.punkti_o - virsotne.punkti_x
            else:
                # Ja X ir dators
                punktu_starpiba = virsotne.punkti_x - virsotne.punkti_o
                
            
            # Normalizē starpību, saglabājot punktu starpības lielumu
            if punktu_starpiba > 0:
                novertejums = 1 * punktu_starpiba  # Pozitīvs = labs datoram
            elif punktu_starpiba < 0:
                novertejums = -1 * abs(punktu_starpiba)  # Negatīvs = slikts datoram
            else:
                novertejums = 0  # Neizšķirts
                
            virsotne.novertejums = novertejums
            return novertejums
            
        # Rekursīvi aprēķina novērtējumus pēctečiem
        if maksimize:
            # MAX līmenis - meklē maksimālo novērtējumu
            max_novertejums = float('-inf')
            for pectecis in virsotne.pecteci:
                novertejums = self._aprekinat_novertejumus(pectecis, dzilums + 1, False, speletajs, alpha, beta)
                if novertejums > max_novertejums:
                    max_novertejums = novertejums
                if self.alpha_beta:
                    alpha = max(alpha, novertejums)
                    if beta <= alpha:
                        break  # Beta nogriešana
            virsotne.novertejums = max_novertejums
            return max_novertejums
        else:
            # MIN līmenis - meklē minimālo novērtējumu
            min_novertejums = float('inf')
            for pectecis in virsotne.pecteci:
                novertejums = self._aprekinat_novertejumus(pectecis, dzilums + 1, True, speletajs, alpha, beta)
                if novertejums < min_novertejums:
                    min_novertejums = novertejums
                if self.alpha_beta:
                    beta = min(beta, novertejums)
                    if beta <= alpha:
                        break  # Alpha nogriešana
            virsotne.novertejums = min_novertejums
            return min_novertejums

    def notirit_novertejumus(self, virsotne):
        """Notīra visus novērtējumus no koka."""
        virsotne.novertejums = None
        for pectecis in virsotne.pecteci:
            self.notirit_novertejumus(pectecis)

    def izveleties_gajienu(self, virsotne, speletajs, is_computer=True):
        """Izvēlas labāko gājienu, balstoties uz minimax algoritmu."""
        if not virsotne.pecteci:
            return None
        
        # Aprēķina novērtējumus no datora puses (dators vienmēr maksimizē savu rezultātu)
        self._aprekinat_novertejumus(virsotne, 0, True, speletajs)
        
        # Izvēlas labāko gājienu ar maksimālo novērtējumu
        labaka_verte = max([p.novertejums for p in virsotne.pecteci])
        labakie_pecteci = [p for p in virsotne.pecteci if p.novertejums == labaka_verte]
        izveleta_virsotne = random.choice(labakie_pecteci)
        self.notirit_novertejumus(virsotne)
        return izveleta_virsotne