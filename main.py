import pyxel
from deplacement import deplacement_x
from quests import start_quest, launch_quest
from get_jsondata import get_quests, get_player, get_spells, get_pnj

run_sprite = [(48, 0, 38, 58), (88, 0, 29, 56), (120, 0, 32, 56),
              (152, 0, 33, 50), (192, 0, 43, 51), (0, 64, 31, 51)]
jump_sprite = [(0, 120, 28, 53), (32, 120, 36, 56), (72, 120, 31, 50),
               (104, 120, 32, 60), (136, 120, 38, 53), (176, 120, 25, 46)]
fireball_sprite = [(0, 184, 32, 56), (32, 184, 39, 56), (72, 184, 48, 53),
                   (120, 184, 50, 53)]
pal = [0x1b2954,0x8c938c,0x5a3936,0x28222c,0x4c505b,0x73522d,
       0x83604f,0x3c4c54,0xc49892,0x3c445c,0x6c6e6c,0x7c706a,
       0x6c6468,0xf3b340,0xe68d02,0xffb228,0xAF082D,0x83213C,
       0xF35C5C,0x2D2E4D,0x316595,0xffffff,0x3fb34e,0x000000]

pyxel.init(500, 250, "Ethereal Odyssey", display_scale=2)
pyxel.load("ressources.pyxres")
pyxel.colors.from_list(pal)

perso_x = 0
y = 165
scroll_x = 0
SCROLL_BORDER_X = 125
animation = "fireball"
is_jumping = False
is_descending = False
is_inside = False
launch = False
title = ""
dialog = {}
character = ""
i = 0
quest_list = get_quests()
instruction = ""
game_launched = False

def update():
  global perso_x, animation, direction, y, scroll_x, is_jumping, is_descending, is_inside, game_launched, title, launch, character, pnj_list, dialog, instruction, i

  perso_x, animation, direction = deplacement_x(perso_x, 1)
  questNumber = get_player()['questNumber']
  dimension = get_player()["dimension"]
  pnj_list = get_pnj(dimension)

  for elt in pnj_list:
    if elt["questGiver"] == True:
      is_inside = start_quest(perso_x, elt["position_x"])

  if perso_x > scroll_x + SCROLL_BORDER_X and direction == 1:
    scroll_x += 3
  elif perso_x < SCROLL_BORDER_X:
    scroll_x = 0
  elif direction == -1:
    scroll_x -= 3

  
  if(is_inside == True):
    if(i == len(get_quests()[0]["deploy"][0]["dialog"])):
      dialog = ""
      quest_list[int(questNumber)]["deploy"][int(questNumber % 1)]["showed"] = False
    else:
      launch, title, dialog, character, instruction = launch_quest(questNumber, get_quests(), launch, title, dialog, character, instruction, i)
    
      if(pyxel.btnr(pyxel.KEY_J)):
        i+=1


  if pyxel.btnr(pyxel.KEY_Z):
    animation = "fireball"

  if(game_launched == False):
    if(pyxel.btnr(pyxel.KEY_E)):
      game_launched = True

  if (pyxel.btnr(pyxel.KEY_SPACE)):
    is_jumping = True


  if (y >= 149 and is_jumping == True):
    y -= 2
  elif (is_descending == True and y <= 165):
    y += 2
  elif (y <= 149):
    is_descending = True
    is_jumping = False
  else:
    is_descending = False
    is_jumping = False


def draw():
  if game_launched == False:
    pyxel.text(100, 10, "Ethereal Odyssey", 12)
    pyxel.text(40,100,"Press [E] to play (full screen highly recommended)", 12)
  else:
    pyxel.cls(0)
    pyxel.camera(scroll_x, 0)
    pyxel.images[2].load(0, 0, "assets/assets1.png")
    pyxel.images[1].load(0, 0, "assets/background.png")
    for i in range(10):
      pyxel.blt(256*i, 0, 1, 0,0,256,177)

    for elt in pnj_list:
      pyxel.blt(elt["position_x"], elt["position_y"], elt["image_bank"], elt["location_x"], elt["location_y"], elt["size_x"], elt["size_y"], 21)

    #Démarrage de la quête
    
    for i in range(1400):
      pyxel.blt(41*i,250-21,2,1,74,41,21)
    
    pyxel.blt(200, 0, 2, 47,0,128,100,21)

    if (is_inside == True):
      pyxel.text(375, 130, "Press [E] to interact", 21)
    
    if(launch):
      pyxel.text(scroll_x + 160, 5, title, 21)
      pyxel.text(scroll_x + 150, 15, instruction, 21)

    if character != "" and dialog != {} and dialog != "":  
      pyxel.text(scroll_x + 20,135,character.split("_")[0], 21)
      pyxel.text(scroll_x + 20,150,dialog[character],21)
    #Animation
    if (animation == "run" and is_jumping == False):
      coef = pyxel.frame_count // 5 % 5
      pyxel.blt(perso_x, y, 0, run_sprite[coef][0], run_sprite[coef][1],
                run_sprite[coef][2] * direction, run_sprite[coef][3], 0)
    elif (animation == "fireball" and is_jumping == False):
      coef = pyxel.frame_count // 4 % 4
      pyxel.blt(perso_x, y, 0, fireball_sprite[coef][0], fireball_sprite[coef][1],
                fireball_sprite[coef][2], fireball_sprite[coef][3], 0)
    elif (y != 150 and is_jumping == True):
      coef = pyxel.frame_count // 6 % 6
      pyxel.blt(perso_x, y, 0, jump_sprite[coef][0], jump_sprite[coef][1],
                jump_sprite[coef][2] * direction, jump_sprite[coef][3], 0)
    else:
      pyxel.blt(perso_x, y, 0, 0, 0, 24*direction, 58, 0)


pyxel.run(update, draw)
