import sys
from tkinter import Button, Label
import random
from turtle import width
from webbrowser import get
import settings
import ctypes

class Cell:
    all = []
    cell_count_label = None
    cell_count = settings.CELL_COUNT
    def __init__(self,x,y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        #Append object to cell.all list
        Cell.all.append(self)

    def create_btn_object(self,location):
        btn = Button(location, width = 12, height = 4)
        btn.bind('<Button-1>', self.left_click_action) #left click
        btn.bind('<Button-3>', self.right_click_action) #right click
        self.cell_btn_object = btn
    
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(location, text = f"Cells Left: {Cell.cell_count}",width = 12, height = 4, 
        bg = "Black",
        fg = "white", font = ("", 30))
        
        Cell.cell_count_label = lbl

    def left_click_action(self,event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()

            #change color back to white if left clicked
            self.cell_btn_object.configure(bg = 'SystemButtonFace')
            self.is_mine_candidate = False

            #cancel left and right click events if cell is already opened
            self.cell_btn_object.unbind('<Button-1>')
            self.cell_btn_object.unbind('<Button-3>')

            #if cell count = 9 player wins
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'You win!', 'Congratulation!',0)
    
    def show_mine(self):
        # A logic to interrupt the game and Game over
        self.cell_btn_object.configure(bg = 'red')
        ctypes.windll.user32.MessageBoxW(0, 'You lose', 'Game Over', 0)
        sys.exit()
    
    def get_cell_by_axis(self, x,y):
        #return a cell object based on the value of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
    @property
    def surrounded_cells(self):
         cells = [
         self.get_cell_by_axis(self.x - 1, self.y - 1),
         self.get_cell_by_axis(self.x - 1, self.y),
         self.get_cell_by_axis(self.x - 1, self.y + 1),
         self.get_cell_by_axis(self.x, self.y - 1),
         self.get_cell_by_axis(self.x + 1, self.y - 1),
         self.get_cell_by_axis(self.x + 1, self.y),
         self.get_cell_by_axis(self.x + 1, self.y + 1),
         self.get_cell_by_axis(self.x, self.y + 1)
         ]
         cells = [cell for cell in cells if cell is not None]
         return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text = self.surrounded_cells_mines_length)
            #update text
            if Cell.cell_count_label:
                Cell.cell_count_label.configure(
                    text = f"Cells Left: {Cell.cell_count}"
                )
        #Maked cell as opened 
        self.is_opened = True

    def right_click_action(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg = 'orange')
            self.is_mine_candidate = True
        else: 
            self.cell_btn_object.configure(bg = 'SystemButtonFace')
            self.is_mine_candidate = False
        
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for picked_cells in picked_cells:
            picked_cells.is_mine = True
        
    def __repr__(self):
        return f"Cell({self.x},{self.y})"