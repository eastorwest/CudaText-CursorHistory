# -*- coding: utf-8 -*-

# Отслеживание истории перемещения курсора (каретки).
# Последующее восстановление позиции каретки
# Простой путь - независимо от вкладки и времени (общий список)

from cudatext import *
import datetime

def dprint(a_str):
  print(a_str)
  pass

class Command:
  #caret_history = [] # все позиции строк в текущем документе [ (PosX, PosY), ... ]
  caret_history = [(None,None, 0,0)] # все позиции строк в текущем документе [ (id_tab, datetime, PosX, PosY), ... ]
  cur_pos = 0     # текущий индекс позиции строки
  skip_rec = False

  def __init__(self):
    pass

  def run(self):
    n = ed.get_line_count()
    s = "Lines count: " + str(n)
    msg_box(s, MB_OK)

  def on_caret(self, ed_self):
    if not self.skip_rec:
      cur_line = ed_self.get_carets()[0][1]
      cur_col  = ed_self.get_carets()[0][0]
      if (cur_line < 0) or (cur_line >= ed_self.get_line_count()):
        return
      #d_t = datetime.datetime.now()
      d_t = None # debug fastest
      #tab_id = ed_self.get_prop(PROP_TAB_ID) # уникальный ID вкладки
      tab_id = None # debug fastest
      # Запомнить текущую строку для последующего перехода
      # (не каждую строку, а достаточно удаленную, хотя бы на 10 строк от последней)
      if abs(self.caret_history[self.cur_pos][3] - cur_line) >= 10:
        self.cur_pos = self.cur_pos + 1
        if len(self.caret_history)-1 >= self.cur_pos:
          del self.caret_history[self.cur_pos:]
        #self.caret_history.append( (cur_col, cur_line) )
        self.caret_history.append( (tab_id, d_t, cur_col, cur_line) )
        #dprint(self.caret_history)
    else:
      self.skip_rec = False

  def move_caret(self):
    #ed.set_caret(posx, posy)
    #ed.set_caret(self.caret_history[self.cur_pos][0], self.caret_history[self.cur_pos][1])
    ed.set_caret(self.caret_history[self.cur_pos][2], self.caret_history[self.cur_pos][3])
    #ed.set_caret(*self.caret_history[self.cur_pos]) # сокращённая форма

  def move_backward(self):
    self.skip_rec = True
    if self.cur_pos:
      self.cur_pos = self.cur_pos - 1
    self.move_caret()

  def move_forward(self):
    self.skip_rec = True
    if len(self.caret_history)-1 > self.cur_pos:
      self.cur_pos = self.cur_pos + 1
    self.move_caret()
