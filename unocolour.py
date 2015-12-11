from tkinter import Tk, Button, Frame, messagebox
import tkinter
import random
import logix

CARDW = 30
CARDH = 30
PAD = 10

triangle = lambda i: i*(i+1)//2

##style = ttk.Style()
##style.configure("Card.R", foreground="blue", background="#F00", relief="flat")
##style.map("Card.R", background=[("disabled", "#900"), ("pressed","#C00"),("active","F33")])

cardcolour = {"red":"#F00", "blue":"#00F", "green":"#0F0", "yellow":"#FF0", "black":"#000", "empty":"#FDD"}
textcolour = {"red":"#022", "blue":"#DD0", "green":"#020", "yellow":"#002", "black":"#DDD", "empty":"#FDD"}
acticolour = {"red":"#C00", "blue":"#00C", "green":"#0C0", "yellow":"#CC0", "black":"#333", "empty":"#FDD"}
discolour = {"red":"#966", "blue":"#669", "green":"#696", "yellow":"#996", "black":"#666", "empty":"#FDD"}
selcolour = {"red":"#F66", "blue":"#66F", "green":"#6F6", "yellow":"#FF6", "black":"#666", "empty":"#FDD"}

def romanik(n):
    if n <= 1: return ""
    ret = n//10 * "X"
    n %= 10
    ret += n//5 * "V"
    n %= 5
    ret = n//2 * "I" + ret + (n+1)//2 * "I"
    return ret

class card(Button):
    def __init__(self, master=None, x=0, y=0, colour=None):
        Button.__init__(self, master, relief="flat", fg = "#444", font = ("Ariel", 10),
                        bd=0, command=self.command)
        self.x, self.y = x, y
        self.select=False
        
        if colour: self.pile = [colour]
        else: self.pile = []
        self.colourize()
        self.pile_size_display()

        
    def colour(self):
        if self.pile: return self.pile[-1]
        else: return "empty"
    def colourize(self):
        colour = self.colour()
        self.place(x=PAD+(PAD+CARDW)*self.x, y=PAD+(PAD+CARDH)*self.y, height=CARDH, width=CARDW)
        self["fg"] = textcolour[colour]
        if self["state"]!="disabled":
            self["bg"]=cardcolour[colour]
            self["activebackground"]=acticolour[colour]
        else:
            if self.select:
                self["bg"]=selcolour[colour]
                self.place(x=PAD+(PAD+CARDW)*self.x-5, y=PAD+(PAD+CARDH)*self.y-5, height=CARDH+10, width=CARDW+10)
            else:
                self["bg"]=discolour[colour]

    def disable_card(self):
        self.select_card()

    def select_card(self, colour=False):
        self.select = colour
        self["state"] = "disabled"
        self.colourize()
        self.pile_size_display()

    def enable_card(self):
        if self.select: self.pile.append(self.select)
        self.select = False
        if self.pile: self["state"] = "normal"
        self.colourize()

    def command(self):
        self.master.click(self.x, self.y)

    def discard(self, level):
        for i in range(level):
            if self.pile:
                yield self.pile.pop()
        self.colourize()
        self.pile_size_display()

    def pile_size_display(self):
        n = len(self.pile)
        if self.select: n += 1
        self["text"] = romanik(n)
        if n > 22: self["font"] = ("Ariel", 6)
        

class board(Frame):
    def __init__(self, master=None, game = None):
        Frame.__init__(self, master, width=logix.WIDTH*(CARDW+PAD)+PAD, height=logix.HEIGHT*(CARDH+PAD)+PAD)
        self.game = game
        self["bg"]="#FDD"
        self.deck = ["red", "blue", "yellow", "green"]*25+["black"]*8
        self.decksize = len(self.deck)
        random.shuffle(self.deck)
        self.cards = [[card(self, i, j, self.deck.pop()) for j in range(5)] for i in range(10)]
        self.sel = []
        self.round = 1
        self.score = 0
        self.scoresheet = []
        game.update_counter(len(self.deck))

    def end_check(self):
        """ Check if the current round is further playable. Then do end round things"""
        if len(self.deck) >= 4:
            for piece in logix.blocks:
                cols = [self.cards[i][j].colour() for i, j in piece]
                if logix.colourmatch(cols):
                    return
        self.scoresheet.append(logix.defaultlist())
        prescore = self.score
        for row in self.cards:
            for tile in row:
                self.deck.extend(tile.discard(self.round))
                self.score += self.round*triangle(len(tile.pile))
                self.scoresheet[-1][len(tile.pile)] += 1
        random.shuffle(self.deck)
        self.display_scores(prescore)
        self.game.update_counter(len(self.deck))
        if self.decksize == len(self.deck):
            self.game_over()
        else:
            self.round += 1
            self.game.update_level(self.round)
            self.end_check()
        
    def display_scores(self, prescore):
        title = "Round {} is over".format(self.round)
        detail = "Pilesize: Count: Score\n"
        detail += "\n".join("{:2d}: {:2d}: {:4d}".format(i, j, triangle(i)*j*self.round) for i, j in enumerate(self.scoresheet[-1]))
        detail += "\nThis round: {}".format(self.score-prescore)
        detail += "\nTotal: {}".format(self.score)
        messagebox.showinfo(title, detail)

    def game_over(self):
        messagebox.showerror("Game Over","You scored {}\nYou reached till level {}".format(self.score, self.round))
        self.game.endgame()
        
                
    def click(self, x, y):
        """ The action to be done if the button at (x, y) is pressed"""
        if self.sel == []:
            possibs = logix.prune(logix.blocks, (x, y))
        else:
            possibs = logix.prune(self.prune, (x, y))

        prune = []
        for piece in possibs:
            cols = [self.cards[i][j].colour() for i, j in piece]
            if logix.colourmatch(cols):
                prune.append(piece)
        if not prune: return
        
        if len(self.sel) == 3:
            self.cards[x][y].select_card(self.deck.pop())
            self.game.update_counter(len(self.deck))
            self.sel = []
            for row in self.cards:
                for tile in row:
                    tile.enable_card()
            self.end_check()
        else:
            clickables = set.union(*(set(piece) for piece in prune))
            self.cards[x][y].select_card(self.deck.pop())
            self.game.update_counter(len(self.deck))
            self.sel.append((x, y))
            self.prune = prune
            for i in range(logix.WIDTH):
                for j in range(logix.HEIGHT):
                    if (i, j) not in clickables and (i, j) not in self.sel:
                        self.cards[i][j].disable_card()

class game(object):
    def __init__(self):
        self.root = Tk()
        self.root["width"]=logix.WIDTH*(CARDW+PAD)+3*PAD
        self.root["height"]=logix.HEIGHT*(CARDH+PAD)+3*PAD + 50
        self.root.title("Unocolour")
        self.mainscreen()
        self.root.mainloop()
        
    def mainscreen(self):
        self.gamename = tkinter.Label(self.root, text = "UNOCOLOUR", font = ("Ariel", 24))
        self.gamename.place(x=(logix.WIDTH*(CARDW+PAD)+3*PAD-400)//2, y=10, width = 400, height = 25)
        self.startbutton = Button(text = "Start", command=self.startgame)
        self.startbutton.place(x=(logix.WIDTH*(CARDW+PAD)+3*PAD-100)//2, y=60, width = 100, height = 25)

    def startgame(self):
        self.cardcounter = tkinter.Label(text = "Cards: 108")
        self.cardcounter.place(x=10, y=25)
        self.lvltitle = tkinter.Label(text = "Level I")
        self.lvltitle.place(x=10, y=10)
        self.b=board(self.root, self)
        self.b.place(x=10,y=50)
        self.startbutton.destroy()
        del self.startbutton
        
    def endgame(self):
        self.b.destroy()
        self.cardcounter.destroy()
        self.lvltitle.destroy()
        del self.b, self.cardcounter, self.lvltitle
        self.mainscreen()

    def update_counter(self, n):
        self.cardcounter["text"] = "Cards: {}".format(n)
    def update_level(self, n):
        self.lvltitle["text"] = "Level {}".format(romanik(n))

game()
