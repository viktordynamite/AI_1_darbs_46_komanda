from speles_koks import SpelesKoks
from algoritmi import Minimax
import time
import random

def generet_nejauso_virkni(garums):
    # Ģenerē nejaušu O un X virkni ar norādīto garumu."
    simboli = ["O", "X"]
    return ''.join(random.choice(simboli) for _ in range(garums))

class Spele:
    def __init__(self, sakuma_virkne=None, speletajs="O", algoritms="minimax", max_dzilums=5, gui_mode=False):
        # Uzsāk spēli ar sākuma parametriem.
        # Ja nav norādīta sākuma virkne, izmanto noklusējuma virkni
        if sakuma_virkne is None:
            sakuma_virkne = "XOXOXOOXXOXOXOOX"
            
        self.sakuma_virkne = sakuma_virkne
        self.max_dzilums = max_dzilums
        self.pirmais_speletajs = "O"            # Pirmais spēlētājs pēc noklusējuma
        self.otrais_speletajs = "X"             # Otrais spēlētājs pēc noklusējuma
        self.speletajs = speletajs              # Cilvēka izvēlētais simbols
        self.algoritms = algoritms.lower()      # Izvēlētais algoritms
        self.gui_mode = gui_mode                # Norāda, vai spēle darbojas GUI režīmā
        self.move_history = []                  # Gājienu vēsture - pārnests no GUI
        
        # Inicializē spēli
        self.reset()
    
    def reset(self):
        # atiestata spēli sākotnējā stāvoklī.
        # Inicializē spēles koku un algoritmus
        self.speles_koks = SpelesKoks(self.sakuma_virkne, self.max_dzilums)
        self.minimax = Minimax(self.max_dzilums)
        self.alpha_beta = Minimax(self.max_dzilums, True)
        
        self.saknes_virsotne = self.speles_koks.generet_saknes_koku()
        self.pasreizeja_virsotne = self.saknes_virsotne
        self.pasreizejais_speletajs = self.pirmais_speletajs
        self.spele_beigusies = False
        self.move_history = []  # Notīra vēsturi
        
        # Statistika
        self.gajienu_skaits = 0
        self.apskatito_virsotnu_skaits = 0
    
    def cilveka_gajiens(self, izveles_indekss):
        """
        Veic cilvēka gājienu, izvēloties no iespējamo gājienu saraksta.
        
        Parametri:
            izveles_indekss: Gājiena indekss no saraksta (1-based)
            
        Atgriež:
            True, ja gājiens veiksmīgs, False pretējā gadījumā
        """
        if self.spele_beigusies:
            return False
        
        # Pārbauda, vai indekss ir derīgs
        if not self.pasreizeja_virsotne.pecteci:
            self.spele_beigusies = True
            return False
        
        try:
            index = int(izveles_indekss) - 1  # Konvertē uz 0-based indeksu
            if 0 <= index < len(self.pasreizeja_virsotne.pecteci):
                # Saglabā veco stāvokli
                veca_virkne = self.pasreizeja_virsotne.virkne
                speletajs_kurs_gaja = self.pasreizejais_speletajs
                
                # Veic gājienu
                nakama_virsotne = self.pasreizeja_virsotne.pecteci[index]
                self._veikt_gajienu(nakama_virsotne)
                
                # Pievieno gājienu vēsturei
                jauna_virkne = nakama_virsotne.virkne
                aizstajamie, pozicija = self.atrast_aizstajamos_simbolus_ar_poziciju(veca_virkne, jauna_virkne) 
                
                # Saglabā vēsturi
                history_entry = f"Spēlētājs ({speletajs_kurs_gaja}): {aizstajamie}→{speletajs_kurs_gaja} poz.{pozicija} => {jauna_virkne}"
                self.move_history.append(history_entry)
                
                return True
            else:
                return False
        except ValueError:
            return False
    
    def datora_gajiens(self):
        # veic datora gājienu, izmantojot izvēlēto algoritmu.
        if self.spele_beigusies:
            return False
        
        # Pārbauda, vai ir iespējami gājieni
        if not self.pasreizeja_virsotne.pecteci:
            self.spele_beigusies = True
            return False
        
        # Saglabā veco stāvokli
        veca_virkne = self.pasreizeja_virsotne.virkne
        datora_simbols = self.pasreizejais_speletajs
        
        # Izvēlas algoritmu
        if self.algoritms == "minimax":
            algoritms = self.minimax
        elif self.algoritms == "alpha_beta":
            algoritms = self.alpha_beta
        else:
            return False
        
        # Nosaka datora simbolu (pretējs cilvēka simbolam)
        datora_simbols_algo = "X" if self.speletajs == "O" else "O"
        
        # Izmanto algoritmu, lai atrastu labāko gājienu
        nakama_virsotne = algoritms.izveleties_gajienu(
            self.pasreizeja_virsotne, 
            datora_simbols_algo,  # Datora simbols būs tas, kuru algoritms maksimizēs
            is_computer=True
        )
        
        if nakama_virsotne:
            self._veikt_gajienu(nakama_virsotne)
            
            # Pievieno gājienu vēsturei
            jauna_virkne = nakama_virsotne.virkne
            aizstajamie, pozicija = self.atrast_aizstajamos_simbolus_ar_poziciju(veca_virkne, jauna_virkne)
            
            # Saglabā vēsturi
            history_entry = f"PC ({datora_simbols}): {aizstajamie}→{datora_simbols} poz.{pozicija} => {jauna_virkne}"
            self.move_history.append(history_entry)
            
            return True
        else:
            self.spele_beigusies = True
            return False
    
    def _veikt_gajienu(self, nakama_virsotne):
        # veic gājienu uz nākamo virsotni.
        # Atjauno pašreizējo virsotni
        self.pasreizeja_virsotne = nakama_virsotne
        self.gajienu_skaits += 1
        
        # Maina spēlētāju
        self.pasreizejais_speletajs = self.otrais_speletajs if self.pasreizejais_speletajs == self.pirmais_speletajs else self.pirmais_speletajs

        # Pārbauda spēles beigas
        if len(nakama_virsotne.virkne) <= 1 or not nakama_virsotne.pecteci:
            # Pārbauda vai vēl ir iespējami gājieni
            if len(nakama_virsotne.virkne) <= 1 or not self.ir_iespejami_gajieni(nakama_virsotne.virkne):
                self.spele_beigusies = True
        
        # ģenerē nākamo dziļumu kokam
        if not self.spele_beigusies:
            # notīra novērtējumus
            if hasattr(self.minimax, 'notirit_novertejumus'):
                self.minimax.notirit_novertejumus(self.saknes_virsotne)
            
            # paplašina koku no pašreizējās virsotnes
            self.speles_koks.generet_nakamo_dzilumu(nakama_virsotne, self.pasreizejais_speletajs)

    def ir_iespejami_gajieni(self, virkne):
        # pārbauda vai ir vēl iespējami gājieni.
        if (self.pasreizejais_speletajs == "O" and ("XX" in virkne or "XO" in virkne)):
            return True
        elif (self.pasreizejais_speletajs == "X" and ("OO" in virkne or "OX" in virkne)):
            return True
        else:
            return False
            
    def parbaudit_speles_beigas(self):
        # pārbauda vai spēle ir beigusies.
        virsotne = self.pasreizeja_virsotne
        if len(virsotne.virkne) <= 1 or not self.ir_iespejami_gajieni(virsotne.virkne):
            self.spele_beigusies = True
            return True
        return False

    def speles_rezultats(self):
        """
        Izvada spēles rezultātu.
        
        Atgriež:
            Ziņojumu par spēles rezultātu
        """
        if not self.spele_beigusies and len(self.pasreizeja_virsotne.virkne) > 1:
            return "Spēle vēl nav beigusies."
        
        virsotne = self.pasreizeja_virsotne
        o_punkti = virsotne.punkti_o
        x_punkti = virsotne.punkti_x
        
        if o_punkti > x_punkti:
            return f"Uzvarēja spēlētājs O ar {o_punkti} punktiem! (X: {x_punkti} punkti)"
        elif x_punkti > o_punkti:
            return f"Uzvarēja spēlētājs X ar {x_punkti} punktiem! (O: {o_punkti} punkti)"
        else:
            return f"Neizšķirts! Abi spēlētāji ieguva {o_punkti} punktus."
            
    # --- Pārnestās un jaunās metodes UI atbalstam ---
    
    def atrast_aizstajamos_simbolus_ar_poziciju(self, veca_virkne, jauna_virkne):
        """
        Atrod simbolu pāri un pozīciju, kas tika mainīta starp divām virknēm.
        
        Parametri:
           - veca_virkne: Sākotnējā virkne
           - jauna_virkne: Jaunā virkne pēc gājiena
            
        Atgriež:
            (aizstajama_virknes_dala, pozicija): Tuplī ar aizstāto apakšvirkni un pozīciju
        """
        if not veca_virkne or not jauna_virkne:
            return "??", "?"

        # atrod pirmo atšķirīgo pozīciju
        pozicija = -1
        len_min = min(len(veca_virkne), len(jauna_virkne))
        for i in range(len_min):
            if veca_virkne[i] != jauna_virkne[i]:
                pozicija = i
                break
                
        # ja garumi atšķiras, bet visas kopīgās pozīcijas vienādas
        if pozicija == -1 and len(veca_virkne) != len(jauna_virkne):
            pozicija = len_min

        if pozicija == -1:
            return "??", "?"

        # iegūst aizvietoto simbolu pāri (2 simboli, ko nomainīja ar vienu)
        aizstajama_virknes_dala = veca_virkne[pozicija:pozicija + 2]
        
        # pārbauda vai aizvietotā virknes daļa ir derīga (2 simboli)
        if len(aizstajama_virknes_dala) == 2:
            return aizstajama_virknes_dala, str(pozicija + 1)
        else:
            return "??", str(pozicija + 1)
            
    def get_iespejamo_gajienu_info(self):
        """
        Iegūst informāciju par visiem iespējamiem gājieniem pašreizējā stāvoklī.
        Šī metode paredzēta GUI vajadzībām.
        
        Atgriež:
           - Sarakstu ar gājienu informāciju katram iespējamam gājienam.
            - Katrs elements satur: (indekss, teksts pogai, pēcteča virsotne)
        """
        if self.spele_beigusies or not self.pasreizeja_virsotne.pecteci:
            return []
            
        virsotne = self.pasreizeja_virsotne
        gajienu_info = []
        
        for i, pectecis in enumerate(virsotne.pecteci):
            try:
                aizstajamie, pozicija = self.atrast_aizstajamos_simbolus_ar_poziciju(virsotne.virkne, pectecis.virkne)
                if aizstajamie == "??":
                    continue
                    
                punktu_starpiba = 0
                speletajs_kurs_izdara_gajienu = self.pasreizejais_speletajs
                if speletajs_kurs_izdara_gajienu == "O":
                    punktu_starpiba = pectecis.punkti_o - virsotne.punkti_o
                else:
                    punktu_starpiba = pectecis.punkti_x - virsotne.punkti_x
                    
                jauna_virkne_rezultata = pectecis.virkne
                button_text = f"Poz.{pozicija}: {aizstajamie}→{speletajs_kurs_izdara_gajienu} (+{punktu_starpiba}) => {jauna_virkne_rezultata}"
                
                gajienu_info.append((i+1, button_text, pectecis))
            except Exception as e:
                print(f"Kļūda veidojot gājiena info {i+1}: {e}")
                
        return gajienu_info
        
    def get_current_string(self):
        # atgriež pašreizējo virkni.
        if self.pasreizeja_virsotne:
            return self.pasreizeja_virsotne.virkne
        return ""
        
    def get_points_o(self):
        # atgriež O spēlētāja punktus.
        if self.pasreizeja_virsotne:
            return self.pasreizeja_virsotne.punkti_o
        return 0
        
    def get_points_x(self):
        # atgriež X spēlētāja punktus.
        if self.pasreizeja_virsotne:
            return self.pasreizeja_virsotne.punkti_x
        return 0
        
    def get_current_player(self):
        # pārbauda pašreizējo spēlētāju.
        return self.pasreizejais_speletajs
        
    def is_game_over(self):
        # pārbauda vai spēle ir beigusies.
        return self.spele_beigusies
        
    def is_player_turn(self):
        # pārbauda vai ir spēlētāja gājiens. 
        return self.pasreizejais_speletajs == self.speletajs
        
    def get_last_move_history_entry(self):
        # atgriež pēdējo gājienu vēstures ierakstu.
        if self.move_history:
            return self.move_history[-1]
        return None 