#! /usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep

import pygame
import sys
from pygame.locals import *  # udostępnienie nazw metod z locals

# inicjacja modułu pygame
pygame.init()

# ----------------------------------------------------------------------------------------------------------------------
# szerokość i wysokość okna gry
OKNOGRY_WYS = 400
INSTRUKCJA_WYS = 30
OKNO_SZER = 800
OKNO_WYS = OKNOGRY_WYS + INSTRUKCJA_WYS # 800x430
OKNOGRY_SZER = OKNO_SZER

# przygotowanie powierzchni do rysowania, czyli inicjacja okna gry
OKNOGRY = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)

# tytuł okna gry
pygame.display.set_caption('Gra o życie')

# Ustawienia kolorów
white = (255, 255, 255) #instrukcja
black = (0, 0, 0) #tło
green = (0, 255, 0) #komórka

# Ustawienia czcionki dla instrukcji
font = pygame.font.SysFont('arial', 20)
instrukcja_tekst = font.render('Instrukcja: LPM - ożywia, PPM - uśmierca, ENTER - start, ESC - pauza', True, (white))

# ----------------------------------------------------------------------------------------------------------------------
#Ustawienia komórka i pole gry

# rozmiar komórki
ROZ_KOM = 10

# ilość komórek w poziomie i pionie
KOM_POZIOM = int(OKNOGRY_SZER / ROZ_KOM)
KOM_PION = int(OKNOGRY_WYS / ROZ_KOM)

# wartości oznaczające komórki "martwe" i "żywe"
KOM_MARTWA = 0
KOM_ZYWA = 1

# lista opisująca stan pola gry, 0 - komórki martwe, 1 - komórki żywe
# na początku tworzymy listę zawierającą KOM_POZIOM zer
#POLE_GRY = [KOM_MARTWA] * KOM_POZIOM #[0,0,0,]
# rozszerzamy listę o listy zagnieżdżone, otrzymujemy więc listę dwuwymiarową
# polegry = [
#     [0, 0, 0, ..., 0],  # K0 0x40
#     [0, 0, 0, ..., 0],  # K1
#     [0, 0, 0, ..., 0],  # K2
#     # ... x80
# ]
#for i in range(KOM_POZIOM):
#    POLE_GRY[i] = [KOM_MARTWA] * KOM_PION
# Znak podłogi _ to w Pythonie specjalna nazwa dla zmiennej, która mówi: "
# Muszę wykonać tę pętlę konkretną liczbę razy, ale sama wartość indeksu (0, 1, 2...) mnie nie interesuje".
# Wcześniej używałeś do tego zmiennej i
POLE_GRY = [[KOM_MARTWA] * KOM_PION for _ in range(KOM_POZIOM)]


# ----------------------------------------------------------------------------------------------------------------------
# przygotowanie następnej generacji komórek, czyli zaktualizowanego POLA_GRY
def przygotuj_populacje(polegry):

    nast_gen = [[KOM_MARTWA] * KOM_PION for _ in range(KOM_POZIOM)]

    # iterujemy po wszystkich komórkach
    for y in range(KOM_PION):
        for x in range(KOM_POZIOM):
            # zlicz populację (żywych komórek) wokół komórki
            populacja = 0

            # wiersz 1
            try:
                if polegry[x - 1][y - 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x][y - 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x + 1][y - 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            # wiersz 2
            try:
                if polegry[x - 1][y] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x + 1][y] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            # wiersz 3
            try:
                if polegry[x - 1][y + 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x][y + 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x + 1][y + 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass

            # "niedoludnienie" lub przeludnienie = śmierć komórki
            if polegry[x][y] == KOM_ZYWA and (populacja < 2 or populacja > 3):
                nast_gen[x][y] = KOM_MARTWA
            # życie trwa
            elif polegry[x][y] == KOM_ZYWA \
                    and (populacja == 3 or populacja == 2):
                nast_gen[x][y] = KOM_ZYWA
            # nowe życie
            elif polegry[x][y] == KOM_MARTWA and populacja == 3:
                nast_gen[x][y] = KOM_ZYWA
    # zwróć nowe polegry z następną generacją komórek
    return nast_gen

def rysuj_populacje():
    """Rysowanie komórek (kwadratów) żywych"""
    for y in range(KOM_PION):
        for x in range(KOM_POZIOM):
            if POLE_GRY[x][y] == KOM_ZYWA:
                pygame.draw.rect(OKNOGRY, (green), Rect(
                    (x * ROZ_KOM, y * ROZ_KOM), (ROZ_KOM, ROZ_KOM)), 1)


# zmienne sterujące wykorzystywane w pętli głównej
zycie_trwa = False
przycisk_wdol = False

# pętla główna programu
while True:
     # obsługa zdarzeń generowanych przez gracza
    for event in pygame.event.get():
        # przechwyć zamknięcie okna
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            zycie_trwa = False

        if event.type == KEYDOWN and event.key == K_RETURN:
            zycie_trwa = True

        if zycie_trwa is False:
            if event.type == MOUSEBUTTONDOWN:
                przycisk_wdol = True
                przycisk_typ = event.button
            if event.type == MOUSEBUTTONUP:
                przycisk_wdol = False
            if przycisk_wdol:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x = int(mouse_x / ROZ_KOM)
                mouse_y = int(mouse_y / ROZ_KOM)
                print(mouse_x,mouse_y)
                # lewy przycisk myszy ożywia
                if mouse_y < KOM_PION:
                    if przycisk_typ == 1:
                        POLE_GRY[mouse_x][mouse_y] = KOM_ZYWA
                    if przycisk_typ == 3:
                        POLE_GRY[mouse_x][mouse_y] = KOM_MARTWA

    if zycie_trwa is True:
        sleep(0.5)
        POLE_GRY = przygotuj_populacje(POLE_GRY)
    OKNOGRY.fill((black))  # Czyszczenie ekranu
    rysuj_populacje() # Rysowanie komórek
    # Rysowanie paska z instrukcją na dole (poniżej planszy gry)
    OKNOGRY.blit(instrukcja_tekst, (10, OKNOGRY_WYS + 5))

    #print(zycie_trwa)

    pygame.display.update()