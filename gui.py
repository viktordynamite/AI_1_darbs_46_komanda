import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, font as tkfont
try:
    from spele import Spele, generet_nejauso_virkni
except ImportError:
    messagebox.showerror("Import kļūda", "Nevar importēt 'Spele' klasi no 'spele.py'.\nPārliecinieties, ka fails atrodas tajā pašā mapē.")
    exit() 

class SpeleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virknes spēle")
        self.initial_geometry = "950x800" 
        self.root.geometry(self.initial_geometry) 

        self.root.minsize(850, 650)  

        # --- krāsu shēmas ---
        self.themes = {
            "day": {
                "bg_color": "#f0f2f5",
                "frame_bg": "#ffffff",
                "text_color": "#1c1e21",
                "highlight_color": "#007bff",
                "points_color": "#007bff",
                "btn_color": "#007bff",
                "btn_text": "#ffffff",
                "reset_btn_bg": "#ffc107",
                "reset_btn_fg": "#212121",
                "entry_bg": "#ffffff",
                "listbox_bg": "#ffffff",
                "listbox_fg": "#1c1e21",
                "listbox_select_fg": "#ffffff",
                "disabled_fg": "#adb5bd",
                "scrollbar_bg": "#e9ecef",
                "scrollbar_trough": "#f8f9fa",
                "scrollbar_arrow": "#343a40",
            },
            "night": {
                "bg_color": "#212529",
                "frame_bg": "#343a40",
                "text_color": "#e9ecef",
                "highlight_color": "#0d6efd",
                "points_color": "#0d6efd",
                "btn_color": "#0d6efd",
                "btn_text": "#ffffff",
                "reset_btn_bg": "#dc3545",
                "reset_btn_fg": "#ffffff",
                "entry_bg": "#495057",
                "listbox_bg": "#495057",
                "listbox_fg": "#e9ecef",
                "listbox_select_fg": "#ffffff",
                "disabled_fg": "#6c757d",
                "scrollbar_bg": "#6c757d",
                "scrollbar_trough":"#495057",
                "scrollbar_arrow": "#e9ecef",
            }
        }
        self.current_theme = "night" 

        # --- fonts ---
        try:
             self.title_font = tkfont.Font(family="Segoe UI Variable", size=16, weight="bold") 
             self.button_font = tkfont.Font(family="Segoe UI Variable", size=11)
             self.text_font = tkfont.Font(family="Segoe UI Variable", size=11)
             self.points_font = tkfont.Font(family="Segoe UI Variable", size=11, weight="bold")
        except tk.TclError:
             print("Brīdinājums: Segoe UI Variable fonts netika atrasts, izmanto Helvetica.")
             self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
             self.button_font = tkfont.Font(family="Helvetica", size=11)
             self.text_font = tkfont.Font(family="Helvetica", size=11)
             self.points_font = tkfont.Font(family="Helvetica", size=11, weight="bold")
             
        self.history_font = tkfont.Font(family="Consolas", size=10)
        try:
             tkfont.Font(family="Consolas", size=10).actual()
        except tk.TclError:
             print("Brīdinājums: Consolas fonts netika atrasts, lieto Courier New.")
             self.history_font = tkfont.Font(family="Courier New", size=10)

        # --- mainīgie ---
        self.spele = None
        self.string_var = StringVar(value="")
        self.player_var = StringVar(value="O")
        self.algorithm_var = StringVar(value="minimax")
        self.string_length_var = StringVar(value="15")
        self.first_player_var = StringVar(value="O")
        self.game_active = False
        self.move_buttons = []
        self.game_move_history = [] 

        # --- sākotnējā konfigurācija ---
        self.apply_theme(self.current_theme) 
        self.setup_ui()

    def apply_theme(self, theme_name):
        "Iestāta krāsu mainīgos un pārkonfigurē UI atbilstoši tēmai."
        if theme_name not in self.themes:
            print(f"Kļūda: Tēma '{theme_name}' nav atrasta.")
            return

        self.current_theme = theme_name
        theme_colors = self.themes[theme_name]

        for color_key, color_value in theme_colors.items():
            setattr(self, color_key, color_value)

        self.configure_styles() 
        self.root.configure(bg=self.bg_color)

        if hasattr(self, 'history_listbox'):
             self.history_listbox.config(
                 bg=self.listbox_bg,
                 fg=self.listbox_fg, 
                 selectbackground=self.highlight_color,
                 selectforeground=self.listbox_select_fg 
             )
        
        if hasattr(self, 'theme_toggle_button'):
            next_theme_name = "Nakts" if self.current_theme == "day" else "Dienas"
            self.theme_toggle_button.config(text=f"{next_theme_name} režīms")


    def configure_styles(self):
        "Konfigurē ttk logrīku stilus, izmantojot self.*_color atribūtus."
        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except tk.TclError:
             print("Brīdinājums: 'clam' tēma nav pieejama, lieto noklusēto.")
             style.theme_use('default')

        # --- pamata stili ---
        style.configure('.',
                        background=self.bg_color,
                        foreground=self.text_color,
                        font=self.text_font,
                        fieldbackground=self.entry_bg,
                        bordercolor=self.frame_bg, 
                        lightcolor=self.frame_bg, 
                        darkcolor=self.frame_bg) 

        style.configure('TFrame', background=self.frame_bg)
        style.configure('TLabel', background=self.frame_bg, foreground=self.text_color, font=self.text_font)
        style.configure('Title.TLabel', background=self.bg_color, foreground=self.highlight_color, font=self.title_font)
        style.configure('Points.TLabel', background=self.frame_bg, foreground=self.points_color, font=self.points_font) 
        style.configure('Info.TLabel', 
                        background=self.entry_bg, 
                        foreground=self.text_color, 
                        padding=(8, 5), 
                        relief=tk.FLAT, 
                        borderwidth=1, 
                        bordercolor=self.frame_bg) 

        # --- Frame ---
        style.configure('TLabelframe', 
                        background=self.bg_color, 
                        relief=tk.SOLID,         
                        bordercolor=self.frame_bg, 
                        borderwidth=1, 
                        padding=(15, 10))        
        style.configure('TLabelframe.Label', 
                        background=self.bg_color, 
                        foreground=self.text_color, 
                        font=self.text_font,
                        padding=(0, 0, 5, 0)) 

        # --- Pogas ---
        style.configure('TButton',
                        background=self.btn_color,
                        foreground=self.btn_text,
                        font=self.button_font,
                        padding=(8, 4),
                        relief=tk.RAISED,
                        borderwidth=1,
                        focuscolor=self.highlight_color, 
                        bordercolor=self.btn_color) 
        style.map('TButton',
                  background=[('active', self.highlight_color), ('disabled', self.frame_bg)],
                  foreground=[('active', self.btn_text), ('disabled', self.disabled_fg)],
                  relief=[('pressed', tk.SUNKEN), ('!pressed', tk.RAISED)]) 

        # Reset poga
        style.configure('Reset.TButton', background=self.reset_btn_bg, foreground=self.reset_btn_fg, bordercolor=self.reset_btn_bg)
        active_reset_bg = self.highlight_color 
        style.map('Reset.TButton',
                   background=[('active', active_reset_bg), ('disabled', self.frame_bg)],
                   foreground=[('active', self.reset_btn_fg), ('disabled', self.disabled_fg)],
                   relief=[('pressed', tk.SUNKEN), ('!pressed', tk.RAISED)])
        
        # Tēmas poga
        style.configure('Theme.TButton', padding=(5, 2), font=(self.text_font.cget("family"), 9), relief=tk.FLAT) 
        style.map('Theme.TButton',
                   background=[('active', self.highlight_color)],
                   foreground=[('active', self.btn_text)])

        # --- Radio button ---
        style.configure('TRadiobutton',
                        background=self.bg_color, 
                        foreground=self.text_color,
                        font=self.text_font,
                        indicatorrelief=tk.FLAT,
                        indicatormargin=-1, 
                        padding=(5, 2))
        style.map('TRadiobutton',
                  background=[('active', self.frame_bg)], 
                  indicatorbackground=[('selected', self.highlight_color), ('!selected', self.entry_bg), ('active', self.highlight_color)],
                  foreground=[('disabled', self.disabled_fg)])

        # --- Entry ---
        style.configure('TEntry',
                        fieldbackground=self.entry_bg,
                        foreground=self.text_color,
                        relief=tk.FLAT,
                        borderwidth=1,
                        bordercolor=self.frame_bg, 
                        insertcolor=self.text_color) 
        style.map('TEntry',
                  bordercolor=[('focus', self.highlight_color)], 
                  fieldbackground=[('disabled', self.frame_bg)], 
                  foreground=[('disabled', self.disabled_fg)])

        # --- Scrollbar ---
        style.configure("Vertical.TScrollbar",
                        background=self.scrollbar_bg,
                        troughcolor=self.scrollbar_trough,
                        bordercolor=self.frame_bg,  
                        arrowcolor=self.scrollbar_arrow,
                        relief=tk.FLAT,
                        arrowrelief = tk.FLAT)
        style.map("Vertical.TScrollbar",
                   background=[('active', self.highlight_color)], 
                  )


    def toggle_theme(self):
        # oārslēdz starp dienas un nakts tēmu.
        next_theme = "night" if self.current_theme == "day" else "day"
        self.apply_theme(next_theme)


    def setup_ui(self):
        # izveido galveno lietotāja saskarni.
        main_frame = ttk.Frame(self.root, style='TFrame', padding=(15, 10)) 
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1) 

        header_frame = ttk.Frame(main_frame, style='TFrame') 
        header_frame.pack(fill=tk.X, pady=(5, 15)) 

        title_label = ttk.Label(header_frame, text="Virknes spēle", style='Title.TLabel', background=self.frame_bg)
        title_label.pack(side=tk.LEFT, anchor=tk.W, padx=(5,0)) 

        next_theme_name = "Nakts" if self.current_theme == "day" else "Dienas"
        self.theme_toggle_button = ttk.Button(
            header_frame,
            text=f"{next_theme_name} režīms",
            command=self.toggle_theme,
            style='Theme.TButton',
            width=12 
        )
        self.theme_toggle_button.pack(side=tk.RIGHT, anchor=tk.E, padx=10)

        setup_frame = ttk.LabelFrame(main_frame, text="Spēles uzstādījumi") 
        setup_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        setup_frame.columnconfigure(0, weight=1)

        game_frame = ttk.LabelFrame(main_frame, text="Spēles laukums") 
        game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        game_frame.columnconfigure(0, weight=1) 
        game_frame.rowconfigure(0, weight=0)    
        game_frame.rowconfigure(1, weight=0)    
        game_frame.rowconfigure(2, weight=1) 
        game_frame.rowconfigure(3, weight=0)    

        self.setup_game_settings(setup_frame)
        self.setup_game_board(game_frame) 


    def setup_game_settings(self, parent):
        # izveido spēles uzstādījumu sadaļu.
        # iekšējie rāmji un LabelFrame iekšpusē lieto TFrame/TLabel stilus
        
        top_settings_outer = ttk.Frame(parent, style='TFrame', padding=(5, 10)) 
        top_settings_outer.pack(fill=tk.X)
        
        ttk.Label(top_settings_outer, text="Sākuma virkne:").pack(side=tk.LEFT, padx=(0, 5))
        self.string_entry = ttk.Entry(top_settings_outer, textvariable=self.string_var, width=25, font=self.text_font)
        self.string_entry.pack(side=tk.LEFT, padx=5, ipady=2)
        ttk.Label(top_settings_outer, text="Garums:").pack(side=tk.LEFT, padx=(10, 5))
        self.length_entry = ttk.Entry(top_settings_outer, textvariable=self.string_length_var, width=4, font=self.text_font)
        self.length_entry.pack(side=tk.LEFT, padx=5, ipady=2)
        self.random_btn = ttk.Button(top_settings_outer, text="Nejauša", command=self.generate_random_string, width=8)
        self.random_btn.pack(side=tk.LEFT, padx=5)

        bottom_settings_outer = ttk.Frame(parent, style='TFrame', padding=(5,5))
        bottom_settings_outer.pack(fill=tk.X)

        left_controls = ttk.Frame(bottom_settings_outer, style='TFrame')
        left_controls.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        algo_frame = ttk.Frame(left_controls, style='TFrame')
        algo_frame.pack(side=tk.LEFT, padx=(0,15))
        ttk.Label(algo_frame, text="Algoritms:").pack(side=tk.LEFT, padx=(0, 5))
        self.algo_radio1 = ttk.Radiobutton(algo_frame, text="  Minimax", variable=self.algorithm_var, value="minimax")
        self.algo_radio1.pack(side=tk.LEFT)
        self.algo_radio2 = ttk.Radiobutton(algo_frame, text="  Alpha-Beta", variable=self.algorithm_var, value="alpha_beta")
        self.algo_radio2.pack(side=tk.LEFT, padx=5)

        player_frame = ttk.Frame(left_controls, style='TFrame')
        player_frame.pack(side=tk.LEFT)
        ttk.Label(player_frame, text="Jūsu simbols:").pack(side=tk.LEFT, padx=(0, 5))
        self.player_radio1 = ttk.Radiobutton(player_frame, text=" O", variable=self.player_var, value="O")
        self.player_radio1.pack(side=tk.LEFT)
        self.player_radio2 = ttk.Radiobutton(player_frame, text=" X", variable=self.player_var, value="X")
        self.player_radio2.pack(side=tk.LEFT, padx=5)

        button_frame = ttk.Frame(bottom_settings_outer, style='TFrame')
        button_frame.pack(side=tk.RIGHT)
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_game, state=tk.DISABLED, style='Reset.TButton', width=10)
        self.reset_button.pack(side=tk.RIGHT, padx=(5, 0))
        self.start_button = ttk.Button(button_frame, text="Sākt spēli", command=self.start_game, width=10)
        self.start_button.pack(side=tk.RIGHT)


    def setup_game_board(self, parent):
        "Izveido spēles laukuma sadaļu, izmantojot grid layout."
        
        # --- augšējās daļas info ---
        info_frame = ttk.Frame(parent, style='TFrame', padding=(0, 5))
        info_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 5)) 
        
        ttk.Label(info_frame, text="Pašreizējā virkne:").pack(side=tk.LEFT, padx=(0, 5))
        self.current_string_var = StringVar(value="")
        self.current_string_display = ttk.Label(info_frame, textvariable=self.current_string_var, style='Info.TLabel', width=40, anchor=tk.W) 
        self.current_string_display.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        points_frame = ttk.Frame(info_frame, style='TFrame')
        points_frame.pack(side=tk.RIGHT)
        self.o_points_var = StringVar(value="0")
        ttk.Label(points_frame, text="O:").pack(side=tk.LEFT, padx=(10, 1)) 
        ttk.Label(points_frame, textvariable=self.o_points_var, style='Points.TLabel', width=3).pack(side=tk.LEFT) 
        self.x_points_var = StringVar(value="0")
        ttk.Label(points_frame, text="X:").pack(side=tk.LEFT, padx=(10, 1)) 
        ttk.Label(points_frame, textvariable=self.x_points_var, style='Points.TLabel', width=3).pack(side=tk.LEFT) 

        # --- spēles info rinda ---
        self.game_info_var = StringVar(value="Spēle nav sākta")
        game_info_label = ttk.Label(parent, textvariable=self.game_info_var, style='Info.TLabel', anchor=tk.CENTER)
        game_info_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5) 

        # --- vēstures rāmis --
        history_frame = ttk.LabelFrame(parent, text="Gājienu vēsture") 
        history_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5) 
        history_frame.rowconfigure(0, weight=1)
        history_frame.columnconfigure(0, weight=1)
        
        listbox_container = ttk.Frame(history_frame, style='TFrame') 
        listbox_container.grid(row=0, column=0, sticky='nsew', padx=5, pady=5) 
        listbox_container.rowconfigure(0, weight=1)    
        listbox_container.columnconfigure(0, weight=1) 
        
        history_scrollbar = ttk.Scrollbar(listbox_container, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        history_scrollbar.grid(row=0, column=1, sticky='ns')
        
        self.history_listbox = tk.Listbox(
            listbox_container, yscrollcommand=history_scrollbar.set, font=self.history_font,
            bg=self.listbox_bg, fg=self.listbox_fg, borderwidth=0, highlightthickness=0, 
            selectbackground=self.highlight_color, selectforeground=self.listbox_select_fg,
            activestyle='none', 
        )
        self.history_listbox.grid(row=0, column=0, sticky='nsew')
        history_scrollbar.config(command=self.history_listbox.yview)

        # --- iespējamo gājienu rāmis ---
        moves_outer_frame = ttk.Frame(parent, style='TFrame', padding=(5,0)) 
        moves_outer_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=(5, 0)) 
        moves_outer_frame.columnconfigure(0, weight=1) 
        
        ttk.Label(moves_outer_frame, text="Iespējamie gājieni:", anchor=tk.W).pack(fill=tk.X) 
        self.moves_buttons_frame = ttk.Frame(moves_outer_frame, style='TFrame') 
        self.moves_buttons_frame.pack(fill=tk.X, pady=5) 


    def generate_random_string(self):
        # ģenerē nejaušu virkni.
        try:
            garums = int(self.string_length_var.get())
            if garums < 15 or garums > 25: 
                garums = 15
                self.string_length_var.set("15")
                messagebox.showwarning("Brīdinājums", "Virknes garumam jābūt no 15 līdz 25. Izmantots garums 15.", parent=self.root)
        except ValueError:
            garums = 15
            self.string_length_var.set("15")
            messagebox.showwarning("Brīdinājums", "Ievadiet derīgu skaitli. Izmantots garums 15.", parent=self.root)

        try:
            random_string = generet_nejauso_virkni(garums) 
            self.string_var.set(random_string)
        except NameError:
             messagebox.showerror("Kļūda", "Funkcija 'generet_nejauso_virkni' nav atrasta.\nPārbaudiet 'spele.py' importu.", parent=self.root)


    def start_game(self):
        # sāk jaunu spēli.
        if self.game_active:
            if not messagebox.askyesno("Apstiprināt", "Vai tiešām vēlaties sākt jaunu spēli?", parent=self.root):
                return
        
        # Notīra vēstures sarakstu
        if hasattr(self, 'history_listbox'): 
            self.history_listbox.delete(0, tk.END)

        # pārbauda un sagatavo sākuma virkni
        sakuma_virkne = self.string_var.get().upper() 
        if not sakuma_virkne or not all(c in "OX" for c in sakuma_virkne):
            messagebox.showerror("Kļūda", "Lūdzu, ievadiet derīgu virkni (tikai O un X)!", parent=self.root)
            return
        self.string_var.set(sakuma_virkne) 

        # sagatavo spēles parametrus
        speletajs = self.player_var.get()
        algoritms = self.algorithm_var.get()
        pirmais_speletajs = "O" 

        try:
            # izveido spēles objektu
            self.spele = Spele(sakuma_virkne=sakuma_virkne, speletajs=speletajs, algoritms=algoritms, max_dzilums=5, gui_mode=True)
            self.spele.pirmais_speletajs = pirmais_speletajs 
            self.spele.otrais_speletajs = "X" if pirmais_speletajs == "O" else "O"
            self.spele.reset() 
        except Exception as e:
            messagebox.showerror("Spēles inicializācijas kļūda", f"Neizdevās izveidot spēles objektu: {e}", parent=self.root)
            return

        self.game_active = True
        
        # atspējo uzstādījumus
        if hasattr(self, 'start_button'): self.start_button.config(state=tk.DISABLED)
        if hasattr(self, 'reset_button'): self.reset_button.config(state=tk.NORMAL)
        if hasattr(self, 'string_entry'): self.string_entry.config(state=tk.DISABLED)
        if hasattr(self, 'length_entry'): self.length_entry.config(state=tk.DISABLED)
        if hasattr(self, 'random_btn'): self.random_btn.config(state=tk.DISABLED)
        if hasattr(self, 'algo_radio1'): self.algo_radio1.config(state=tk.DISABLED)
        if hasattr(self, 'algo_radio2'): self.algo_radio2.config(state=tk.DISABLED)
        if hasattr(self, 'player_radio1'): self.player_radio1.config(state=tk.DISABLED)
        if hasattr(self, 'player_radio2'): self.player_radio2.config(state=tk.DISABLED)
        
        # pievieno sākuma stāvokli vēsturei
        start_history = f"Sākums: {sakuma_virkne}"
        self.spele.move_history.append(start_history)  # Izmanto speles klases vēsturi
        if hasattr(self, 'history_listbox'):
            self.history_listbox.insert(tk.END, start_history)
            self.history_listbox.yview(tk.END)

        self.update_game_info()

        # datora pirmais gājiens
        if self.spele and not self.spele.is_player_turn() and not self.spele.is_game_over():
            self.game_info_var.set(f"Dators ({self.spele.get_current_player()}) domā...")
            self.root.update_idletasks() 
            self.root.after(200, self.make_computer_move) 

    def reset_game(self):
        # reseto sākotnējā stāvoklī UN loga izmēru.
        self.game_active = False
        self.spele = None

        # iespējo uzstādījumus
        if hasattr(self, 'start_button'): self.start_button.config(state=tk.NORMAL)
        if hasattr(self, 'reset_button'): self.reset_button.config(state=tk.DISABLED)
        if hasattr(self, 'string_entry'): self.string_entry.config(state=tk.NORMAL)
        if hasattr(self, 'length_entry'): self.length_entry.config(state=tk.NORMAL)
        if hasattr(self, 'random_btn'): self.random_btn.config(state=tk.NORMAL)
        if hasattr(self, 'algo_radio1'): self.algo_radio1.config(state=tk.NORMAL)
        if hasattr(self, 'algo_radio2'): self.algo_radio2.config(state=tk.NORMAL)
        if hasattr(self, 'player_radio1'): self.player_radio1.config(state=tk.NORMAL)
        if hasattr(self, 'player_radio2'): self.player_radio2.config(state=tk.NORMAL)

        # notīra spēles laukumu un vēsturi
        for button in self.move_buttons:
            button.destroy()
        self.move_buttons = []
        
        if hasattr(self, 'history_listbox'):
            self.history_listbox.delete(0, tk.END)

        self.current_string_var.set("")
        self.o_points_var.set("0")
        self.x_points_var.set("0")
        self.game_info_var.set("Spēle nav sākta")

        # --- atjauno sākotnējo loga izmēru ---
        if hasattr(self, 'initial_geometry'):
            self.root.geometry(self.initial_geometry)


    def update_game_info(self):
        # atjauno spēles informāciju saskarnē.
        if not self.spele or not self.game_active:
            return

        try:
            # Atjauno pašreizējo virkni un punktus
            self.current_string_var.set(self.spele.get_current_string())
            self.o_points_var.set(str(self.spele.get_points_o()))
            self.x_points_var.set(str(self.spele.get_points_x()))

            # Atjauno spēles statusa informāciju
            if self.spele.is_game_over():
                rezultats = self.spele.speles_rezultats()
                self.game_info_var.set(rezultats if rezultats else "Spēle beigusies!")
            else:
                next_player = self.spele.get_current_player()
                if self.spele.is_player_turn():
                    self.game_info_var.set(f"Jūsu gājiens ({next_player})")
                else:
                    self.game_info_var.set(f"Datora gājiens ({next_player})") 
            
            # Atjauno iespējamo gājienu pogas
            self.update_moves()

        except Exception as e:
            print(f"Atjaunināšanas kļūda: {e}")


    def update_moves(self):
        # atjauno iespējamo gājienu pogas, rādot pilnu rezultāta virkni.
        # Notīrīt esošās pogas
        if hasattr(self, 'moves_buttons_frame'):
             for widget in self.moves_buttons_frame.winfo_children():
                  widget.destroy()
        self.move_buttons = []

        # Pārbauda vai spēle ir aktīva un ir spēlētāja gājiens
        if not self.spele or not self.game_active or self.spele.is_game_over():
            return
            
        if not self.spele.is_player_turn():
            return

        # Iegūst informāciju par iespējamiem gājieniem
        gajienu_info = self.spele.get_iespejamo_gajienu_info()
        
        # Ja nav iespējamo gājienu, pārbauda spēles beigas
        if not gajienu_info:
            virsotne = self.spele.pasreizeja_virsotne
            if not virsotne.pecteci and not self.spele.is_game_over():
                self.spele.parbaudit_speles_beigas() 
                self.update_game_info() 
            return

        # Izveido pogas iespējamajiem gājieniem
        max_buttons_per_row = 2
        current_row_frame = None

        for i, (index, button_text, _) in enumerate(gajienu_info):
            if i % max_buttons_per_row == 0:
                 current_row_frame = ttk.Frame(self.moves_buttons_frame, style='TFrame')
                 current_row_frame.pack(fill=tk.X, anchor=tk.W) 

            button = ttk.Button(
                current_row_frame,
                text=button_text,
                command=lambda idx=index: self.make_human_move(idx),
            )
            button.pack(side=tk.LEFT, padx=2, pady=2, anchor=tk.W) 
            self.move_buttons.append(button)


    def make_human_move(self, move_index):
        # veic cilvēka gājienu un pievieno vēsturei.
        if not self.spele or not self.game_active or self.spele.is_game_over():
            return

        try:
            # Veic gājienu ar speles objektu
            if self.spele.cilveka_gajiens(move_index):
                # Atjauno vēstures sarakstu
                last_move = self.spele.get_last_move_history_entry()
                if last_move and hasattr(self, 'history_listbox'):
                    self.history_listbox.insert(tk.END, last_move)
                    self.history_listbox.yview(tk.END) 

                # Atjauno UI
                self.update_game_info() 

                # Ja spēle turpinās, sagatavo datora gājienu
                if not self.spele.is_game_over():
                    self.game_info_var.set(f"Dators ({self.spele.get_current_player()}) domā...")
                    self.root.update_idletasks()
                    self.root.after(500, self.make_computer_move) 
            else:
                 messagebox.showwarning("Neiespējams gājiens", "Izvēlētais gājiens nebija veiksmīgs.", parent=self.root)

        except Exception as e:
            messagebox.showerror("Gājiena kļūda", f"Kļūda veicot cilvēka gājienu: {e}", parent=self.root)


    def make_computer_move(self):
        # veic datora gājienu un pievieno vēsturei.
        if not self.spele or not self.game_active or self.spele.is_game_over():
            return

        try:
            # Veic datora gājienu
            if self.spele.datora_gajiens():
                # Atjauno vēstures sarakstu
                last_move = self.spele.get_last_move_history_entry()
                if last_move and hasattr(self, 'history_listbox'):
                    self.history_listbox.insert(tk.END, last_move)
                    self.history_listbox.yview(tk.END) 
                
                # Atjauno UI
                self.update_game_info() 
            else:
                if self.spele.pasreizeja_virsotne is None:
                    print("Kļūda: pasreizeja_virsotne ir None pēc datora gājiena!")
                    self.reset_game()

        except Exception as e:
            messagebox.showerror("Datora gājiena kļūda", f"Kļūda veicot datora gājienu: {e}", parent=self.root)
            self.reset_game()

# ja izpilda šo failu tieši
if __name__ == "__main__":
    root = tk.Tk()
    app = SpeleGUI(root)
    # Automātiski ģenerē nejaušu virkni pēc programmas palaišanas
    app.generate_random_string()
    root.mainloop()