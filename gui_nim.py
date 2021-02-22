import tkinter as tk
from PIL import Image, ImageTk
import nim
from time import sleep


class OptionsWindow(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title('Options')
        def protocol_close():
            self.parent.button_option.configure(state='normal')
            self.destroy()

        self.protocol('WM_DELETE_WINDOW', protocol_close)
        self.resizable(width=False, height=False)

        opt_pildi_gana = tk.BooleanVar()
        label_opt_pildigana = tk.Label(self, text="Misère Game?")
        radio_yes = tk.Radiobutton(self, text='Yes', variable=opt_pildi_gana, value=True)
        radio_no = tk.Radiobutton(self, text='No', variable=opt_pildi_gana, value=False)
        label_opt_pildigana.grid(column=0, row=0, sticky="w", pady=3)
        radio_yes.grid(column=1, row=0, columnspan=2, sticky="w")
        radio_no.grid(column=3, row=0, columnspan=2, sticky="w")

        opt_ai = tk.BooleanVar()
        label_opt_ai = tk.Label(self, text="Game Mode:")
        radio_ai_false = tk.Radiobutton(self, text="2 Players", variable=opt_ai, value=False)
        radio_ai_true = tk.Radiobutton(self, text='AI', variable=opt_ai, value=True)
        label_opt_ai.grid(column=0, row=1, sticky="w", pady=3)
        radio_ai_false.grid(column=1, row=1, columnspan=2, sticky="w")
        radio_ai_true.grid(column=3, row=1, columnspan=2, sticky="w")

        opt_human_player = tk.IntVar()
        label_opt_human = tk.Label(self, text="AI Plays As:")
        radio_ai_player1 = tk.Radiobutton(self, text="Player 1", variable=opt_human_player, value=2)
        radio_ai_player2 = tk.Radiobutton(self, text="Player 2", variable=opt_human_player, value=1)
        label_opt_human.grid(column=0, row=2, sticky="w", pady=3)
        radio_ai_player1.grid(column=1, row=2, sticky="w", columnspan=2)
        radio_ai_player2.grid(column=3, row=2, sticky="w", columnspan=2)

        opt_gamesize = tk.IntVar()
        label_gamesize = tk.Label(self, text="Game Size:")
        label_gamesize.grid(column=0, row=3, sticky="w")
        radio_sizes = {}
        for n in range(3, 7):
            radio_sizes[n] = tk.Radiobutton(self, text=f"{n}", value=n, variable=opt_gamesize)
            radio_sizes[n].grid(column=n - 2, row=3, sticky="w")

        # For incompatible radios
        def command_radio_able(enable_radio_list=(), disable_radio_list=()):
            def command():
                for r in enable_radio_list:
                    r.configure(state='normal')
                for r in disable_radio_list:
                    r.configure(state='disabled')
            return command

        radio_ai_player1.configure(state='normal' if self.parent.parent.ai else 'disabled')
        radio_ai_player2.configure(state='normal' if self.parent.parent.ai else 'disabled')
        radio_sizes[6].configure(state='normal' if not self.parent.parent.ai else 'disabled')
        radio_ai_true.configure(state='normal' if not self.parent.parent.gamesize == 6 else 'disabled')

        ai_enable_these = [radio_ai_player1, radio_ai_player2]
        ai_disable_these = [radio_sizes[6]]
        radio_ai_true.configure(command=command_radio_able(ai_enable_these, ai_disable_these))
        radio_ai_false.configure(command=command_radio_able(ai_disable_these, ai_enable_these))

        for radio in radio_sizes.values():
            radio.configure(command=command_radio_able([radio_ai_true]))
        radio_sizes[6].configure(command=command_radio_able(disable_radio_list=[radio_ai_true]))

        def command_save():
            self.parent.parent.ai = opt_ai.get()
            self.parent.parent.pildi_gana = opt_pildi_gana.get()
            self.parent.parent.gamesize = opt_gamesize.get()
            self.parent.parent.human_player = opt_human_player.get()
            for button in self.parent.parent.board.gameboard.values():
                button.destroy()
            self.parent.parent.board.show_board()
            self.parent.button_option.configure(state='normal')
            self.parent.restart_board()
            self.destroy()

        button_options_save = tk.Button(self, text='SAVE', command=command_save)
        button_options_save.grid(column=0, row=4, columnspan=5, sticky="NSEW")
        opt_ai.set(self.parent.parent.ai)
        opt_gamesize.set(self.parent.parent.gamesize)
        opt_human_player.set(self.parent.parent.human_player)
        opt_pildi_gana.set(self.parent.parent.pildi_gana)


class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.image_gear = Image.open('images/gear.png').resize((20, 20), Image.ANTIALIAS)
        self.image_gear = ImageTk.PhotoImage(self.image_gear)
        self.image_qmark = Image.open('images/qmark.png').resize((20, 20), Image.ANTIALIAS)
        self.image_qmark = ImageTk.PhotoImage(self.image_qmark)
        self.image_restart = Image.open('images/restart.png').resize((20, 20), Image.ANTIALIAS)
        self.image_restart = ImageTk.PhotoImage(self.image_restart)

        self.button_option = tk.Button(self, image=self.image_gear)
        self.button_qmark = tk.Button(self, image=self.image_qmark)
        self.button_restart = tk.Button(self, image=self.image_restart)

        self.button_option.configure(command=self.show_options)
        self.button_restart.configure(command=self.restart_board)
        self.button_qmark.configure(command=self.show_instructions)

    def show_options(self):
        self.button_option.configure(state='disabled')
        toplevel_options = OptionsWindow(self)
        toplevel_options.mainloop()

    def restart_board(self):
        parent = self.parent
        board = parent.board
        for name, button in board.gameboard.items():
            button.configure(state='normal', image=board.image_stick)
            bind_these = ['<Enter>', '<Leave>', '<Button-1>']
            with_these = [board.enter_handler_wrapper, board.leave_handler_wrapper, board.click_handler_wrapper]
            for event, handler in zip(bind_these, with_these):
                button.bind(event, handler(name))
        parent.game = nim.Game(parent.gamesize, parent.ai, parent.human_player, parent.pildi_gana)
        parent.after(100, parent.text.init_labels)

    @staticmethod
    def show_instructions():
        toplevel = tk.Toplevel(bg='#e0e038')
        toplevel.title('Instructions')
        instructions_text = ("Instructions:\n" +
                             "There is 1 or more stacks of sticks.\n" +
                             "2 Players take turns breaking any ammount of sticks in a single stack.\n" +
                             "The game ends when the last stick is broken.\n" +
                             "In a normal game, the last player to move wins the game\n" +
                             "In a misère game, the last player to move loses the game.")
        instruction_font = ('', 12, 'bold')
        instructions_label = tk.Label(toplevel, font=instruction_font, bg='#e0e038', justify='left',
                                      text=instructions_text)
        instructions_label.pack()
        toplevel.mainloop()


class Gameboard(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.gameboard = dict()
        self.stick_height = 180 * 3 // 4
        self.stick_width = 112 // 2
        self.image_stick = Image.open('images/stick.png').resize((self.stick_width, self.stick_height), Image.ANTIALIAS)
        self.image_stick = ImageTk.PhotoImage(self.image_stick)
        self.image_sb1 = Image.open('images/stickbreak1.png').resize((self.stick_width, self.stick_height), Image.ANTIALIAS)
        self.image_stickbreak1 = ImageTk.PhotoImage(self.image_sb1)
        self.image_sb2 = Image.open('images/stickbreak2.png').resize((self.stick_width, self.stick_height), Image.ANTIALIAS)
        self.image_stickbreak2 = ImageTk.PhotoImage(self.image_sb2)
        self.show_board()

    def ai_play(self):
        toolbar = self.parent.toolbar
        temp_dsbld_btns = []
        unbind_these = ["<Button-1>", "<Enter>", "Leave"]
        for name, btn in self.gameboard.items():
            if btn.config('state')[-1] == 'normal':
                temp_dsbld_btns.append((name, btn))
                for evnt in unbind_these:
                    btn.unbind(evnt)
        disable_these = [toolbar.button_qmark, toolbar.button_option, toolbar.button_restart]
        if toolbar.button_option.config('state')[-1] == 'disabled':
            disable_these.remove(toolbar.button_option)
        for btn in disable_these:
            btn.configure(state='disabled')
        self.parent.text.print2label(f"AI's Turn...")
        self.parent.update_idletasks()
        sleep(0.5)
        evaluated_options = self.parent.game.options()
        move = self.parent.game.best_move(evaluated_options)
        self.parent.update()
        for name, btn in temp_dsbld_btns:
            btn.bind('<Enter>', self.enter_handler_wrapper(name))
            btn.bind('<Leave>', self.leave_handler_wrapper(name))
            btn.bind('<Button-1>', self.click_handler_wrapper(name))
        for btn in disable_these:
            btn.configure(state='normal')
        self.parent.update_idletasks()
        move_btn = self.gameboard[f"{move[0]}{move[1] + self.parent.game.board[move[0]]}"]
        move_btn.event_generate('<Button-1>', when='tail')

    def enter_handler_wrapper(self, btn_name):
        def enter_handler(event):
            image_stickbreak = self.image_stickbreak1 if self.parent.game.player == 1 else self.image_stickbreak2
            self.gameboard[btn_name].configure(image=image_stickbreak)
            if not btn_name[1:] == '1':
                self.gameboard[str(int(btn_name) - 1)].event_generate('<Enter>', when='tail')
        return enter_handler

    def leave_handler_wrapper(self, btn_name):
        def leave_handler(event):
            self.gameboard[btn_name].configure(image=self.image_stick)
            if not btn_name[1:] == '1':
                self.gameboard[str(int(btn_name) - 1)].event_generate('<Leave>', when='head')

        return leave_handler

    def click_handler_wrapper(self, btn_name):
        ini_stack = int(btn_name[:1])
        ini_ammount = int(btn_name[1:])

        def click_handler(event):
            def loop(name):
                image_stickbreak = self.image_stickbreak1 if self.parent.game.player == 1 else self.image_stickbreak2
                self.gameboard[name].configure(image=image_stickbreak, state='disabled')
                unbind_these = ["<Leave>", "<Enter>", "<Button-1>"]
                for evnt in unbind_these:
                    self.gameboard[name].unbind(evnt)

                self.parent.game.x_a_stack(ini_stack, 1)

            for i in range(ini_ammount, self.parent.game.board[ini_stack], -1):
                loop(f"{ini_stack}{i}")
            if self.parent.game.win():
                if not self.parent.ai:
                    win_message = f"PLAYER {1 if self.parent.game.player == 2 else 2} WINS!" \
                        if self.parent.pildi_gana else f"PLAYER {self.parent.game.player} WINS!"
                else:
                    win_message = f"AI WINS!" \
                        if self.parent.pildi_gana == (self.parent.game.player == self.parent.human_player) \
                        else f"PLAYER {self.parent.human_player} WINS!"
                self.parent.text.print2label(win_message)
            elif self.parent.ai and self.parent.game.player == self.parent.human_player:
                self.parent.game.player = 1 if self.parent.game.player == 2 else 2
                self.ai_play()
            else:
                self.parent.game.player = 1 if self.parent.game.player == 2 else 2
                self.parent.text.print2label(f"Player {self.parent.game.player}'s Turn!")
        return click_handler

    def show_board(self):
        self.gameboard.clear()
        for i in range(self.parent.gamesize, 2, -1):
            for j in range(1, i + 1):
                self.gameboard[f'{i}{j}'] = tk.Button(self, image=self.image_stick)

        # Positions the Game Board
        margin = 40 if self.parent.gamesize == 3 else 20
        board_width = margin
        previous_stack = self.parent.gamesize
        for name, button in self.gameboard.items():
            if previous_stack == int(name[:1]):
                pass
            else:
                previous_stack = int(name[:1])
                board_width += 30
            button.place(anchor='w', rely=0.5, x=board_width, height=self.stick_height, width=self.stick_width)
            button.bind('<Enter>', self.enter_handler_wrapper(name))
            button.bind('<Leave>', self.leave_handler_wrapper(name))
            button.bind('<Button-1>', self.click_handler_wrapper(name))
            board_width += self.stick_width
        board_width += margin
        height = 350
        width = board_width
        self.parent.geometry(f'{width}x{height}')

        toolbar = self.parent.toolbar

        toolbar.button_option.place(x=width // 2 - 40, rely=0.5, anchor='center', width=height/10, height=height/10)
        toolbar.button_qmark.place(x=width // 2, rely=0.5, anchor='center', width=height/10, height=height/10)
        toolbar.button_restart.place(x=width // 2 + 40, rely=0.5, anchor='center', width=height/10, height=height/10)


class LabelFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.textvar_latest = tk.StringVar()
        self.textvar_second = tk.StringVar()
        self.textvar_third = tk.StringVar()

        font_latest = ("newspaper", 20)
        font_second = ("newspaper", 12)
        font_third = ("newspaper", 9)

        label_latest = tk.Label(self, textvariable=self.textvar_latest, font=font_latest, bg='#e0e038', fg='red')
        label_latest.pack(side='bottom')
        label_second = tk.Label(self, textvariable=self.textvar_second, font=font_second, bg='#e0e038')
        label_second.pack(side='bottom')
        label_third = tk.Label(self, textvariable=self.textvar_third, font=font_third, bg='#e0e038')
        label_third.pack(side='bottom')

    def print2label(self, message):
        self.textvar_third.set(self.textvar_second.get())
        self.textvar_second.set(self.textvar_latest.get())
        self.textvar_latest.set(message)

    def init_labels(self):
        self.textvar_latest.set('')
        self.textvar_second.set('')
        self.textvar_third.set('')
        self.parent.update_idletasks()
        if not self.parent.ai or self.parent.game.player == self.parent.human_player:
            self.textvar_latest.set("Player 1's Turn!")
        elif self.parent.ai:
            self.parent.board.ai_play()
        self.textvar_second.set('')
        self.textvar_third.set('')


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.gamesize = 5
        self.ai = True
        self.human_player = 1
        self.pildi_gana = False
        self.game = nim.Game(self.gamesize, self.ai, self.human_player, self.pildi_gana)

        self.title('Nim')
        self.resizable(False, False)
        self.configure(bg='#e0e038')

        self.toolbar = Toolbar(self, bg='#e0e038')
        self.board = Gameboard(self, bg='#e0e038')
        self.text = LabelFrame(self, bg='#e0e038')

        self.toolbar.place(rely=0.05, relwidth=1, relheight=0.1)
        self.board.place(rely=0.2, relwidth=1, relheight=0.5)
        self.text.place(rely=0.75, relwidth=1, relheight=0.2)

        self.after(100, self.text.init_labels)


nim_gui = MainApplication()
nim_gui.mainloop()
