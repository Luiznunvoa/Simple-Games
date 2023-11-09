import os
from termcolor import cprint

def Main():
   tabuleiro, x, y, rodada, contadorverd, contadorverm, joga_denovo, check = [['   ' for _ in range(8)] for _ in range(8)], 9, 9, 0, 0, 0, False, False
   cprint('\n    JOGO DE DAMAS', 'yellow')
   cprint('\n  Deseja iniciar o jogo?\n', 'white')
   Preencher_tabuleiro(tabuleiro)

   pergunta = input()
   if pergunta == 'sim':
      Trazer_tabuleiro(x, y,tabuleiro)

      while True:
         Trazer_tabuleiro(x, y,tabuleiro)
         if (rodada % 2) == 0:
            cor = ['VERDE', 'green']
            verd, verm = True, False
         else:
            cor = ['VERMELHO', 'red']
            verd, verm = False, True
         cprint(f'\n  VEZ DO {cor[0]}!', f'{cor[1]}')
         
         while True:
            try:
               x, y = map(int, input('\n\033[1;37m  selecione uma peça sua(coluna linha)(diga nao para passar o turno\sair): ').split())
            except ValueError:
               continua = False
               joga_denovo = False
               if input('') == 'sair':
                  return
               else:
                  break
            else:
               if Peca_valida(tabuleiro, verd, verm, x, y):
                  continua = True
                  Trazer_tabuleiro(x, y,tabuleiro)
                  break
         if continua:
            while True:
               try:
                  z, a = map(int, input('\n  Diga sua jogada(coluna linha)(diga nao para voltar): ').split())
               except ValueError:
                  joga_denovo = True
                  break
               else:
                  joga_denovo = False
                  tabuleiro, contadorverd, contadorverm, joga_denovo, check = Movimentacao_de_peca(tabuleiro, x, y, z , a, verd, verm, joga_denovo, contadorverd, contadorverm, check)
                  if check:
                     break

            Trazer_tabuleiro(x, y,tabuleiro)

         if contadorverd == 12 or contadorverm == 12:
            cprint(f'VITORIA DO {cor[0]}!', f'{cor[1]}')
            return

         if not joga_denovo:
            rodada += 1

def Trazer_tabuleiro(x, y,tabuleiro):
   os.system('cls')
   Criar_tabuleiro(x, y,tabuleiro)
   return

def Preencher_tabuleiro(tabuleiro):
    for i in range(8):
        for j in range(8):
            if ((i + j) % 2) == 0:
                if i <= 2:
                    tabuleiro[i][j] = ' O '
                elif i >= 5:
                    tabuleiro[i][j] = ' X '

def Criar_tabuleiro(x,y, tabuleiro):
    print()
    cprint('                   1  2  3  4  5  6  7  8  ', 'yellow')
    for i in range(8):
        if i != 0:
            print('')
        cprint(f'                {i + 1} ', 'yellow', end = "")
        for j in range(8):
            if ((i + j) % 2) == 0:
                if tabuleiro[i][j] == ' O ':
                    if i == (y - 1) and j == (x - 1):
                        cprint(tabuleiro[i][j], 'black', 'on_green', end = "")
                    else:
                        cprint(tabuleiro[i][j],'red', 'on_white', end = "")
                elif tabuleiro[i][j] == ' X ':
                    if i == (y - 1) and j == (x - 1):
                        cprint(tabuleiro[i][j], 'black', 'on_green', end = "")
                    else:
                        cprint(tabuleiro[i][j],'green', 'on_white', end = "")   
                else:
                    if i == (y - 1) and j == (x - 1):
                        cprint(tabuleiro[i][j], 'black', 'on_green', end = "")
                    else:
                        cprint(tabuleiro[i][j],'white', 'on_white', end = "")
            else:
                cprint(tabuleiro[i][j],'blue', 'on_blue', end = "")
    print()
    return

def Peca_valida(tabuleiro, verd, verm, x, y):
   if verd: aux = ' X ' 
   elif verm: aux = ' O '
   if tabuleiro[y - 1][x - 1] ==  aux:
      return True
   else:
      cprint('\n\n  você selecionou a peça do oponente', 'red')
      return False

def Movimentacao_de_peca(tabuleiro, x, y, z , a, verd, verm, joga_denovo, contadorverd, contadorverm, check):
   if (((z - 1) + (a - 1)) % 2) == 0 and abs(y - a) <= 1 and abs(x - z) <= 1:
      check, joga_denovo =  Movimento_valido(tabuleiro, x, y, z, a, verd, verm, joga_denovo)
      if check == True and joga_denovo == True:
         tabuleiro, check = Comer_peca(x, y, tabuleiro, z, a)
         if verd: contadorverd += 1
         else: contadorverm += 1
         return tabuleiro, contadorverd, contadorverm, joga_denovo, check
      elif check == True and joga_denovo == False:
         return tabuleiro, contadorverd, contadorverm, joga_denovo, True
      else:
         return tabuleiro, contadorverd, contadorverm, joga_denovo, False
   else:
      cprint('  Casa inacessível', 'red')
      return tabuleiro, contadorverd, contadorverm, joga_denovo, False       

def Movimento_valido(tabuleiro, x, y, z, a, verd, verm, joga_denovo):
   if verd: aux = ' O ' 
   elif verm: aux = ' X '
   if tabuleiro[a - 1][z - 1] == aux:
      joga_denovo = True
      return True, True
   elif not joga_denovo and tabuleiro[a - 1][z - 1] == '   ':
      tabuleiro[y - 1][x - 1], tabuleiro[a - 1][z - 1] = tabuleiro[a - 1][z - 1], tabuleiro[y - 1][x - 1]
      return True, False
   else:
      cprint('\n  Jogada impossível', 'red')
      return False, False

def Comer_peca(x, y, tabuleiro, z, a):
    puloZ = abs(((x - z) * 2) - x) 
    puloA = abs(((y - a) * 2) - y)
    if tabuleiro[puloA - 1][puloZ - 1] != '   ':
        cprint('\n  escolha outra casa, esta está inacessível', 'red')
        return tabuleiro, False
    else:
        tabuleiro[a - 1][z - 1] = '   '
        tabuleiro[y - 1][x - 1], tabuleiro[puloA - 1][puloZ - 1] = tabuleiro[puloA - 1][puloZ - 1], tabuleiro[y - 1][x - 1]
        return tabuleiro, True       
os.system('cls')   
Main()