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
OKNOGRY_WYS = 800
INSTRUKCJA_WYS = 30
OKNO_SZER = 1600
OKNO_WYS = OKNOGRY_WYS + INSTRUKCJA_WYS # 800x430
OKNOGRY_SZER = OKNO_SZER

# przygotowanie powierzchni do rysowania, czyli inicjacja okna gry
OKNOGRY = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)

# ----------------------------------------------------------------------------------------------------------------------
#Ustawienia komórka i pole gry

# rozmiar komórki
ROZ_KOM = 20

# ilość komórek w poziomie i pionie
KOM_POZIOM = int(OKNOGRY_SZER / ROZ_KOM)
KOM_PION = int(OKNOGRY_WYS / ROZ_KOM)

# wartości oznaczające komórki "martwe" i "żywe"
KOM_MARTWA = 0
KOM_ZYWA = 1

# tytuł okna gry
pygame.display.set_caption('Gra o życie')

# Ustawienia kolorów
white = (255, 255, 255) #instrukcja
black = (0, 0, 0) #tło
green = (0, 255, 0) #komórka
gray = (50, 50, 50)  #instrukcje tło
red = (255, 0, 0)

# Ustawienia czcionki dla instrukcji
instrukcja_font = pygame.font.SysFont('arial', 20)
instrukcja_tekst = instrukcja_font.render(
    'Edycja: LPM - dodaje, PPM - usuwa. Start gra: ENTER - start, ESC - pauza',
    True
    , white)

# Ustawienia czcionki dla STOP
stop_tekst = instrukcja_font.render(
    '----- ŻYCIE ZAMARŁO -----',
    True
    , red)

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
#POLE_GRY = [[KOM_MARTWA] * KOM_PION for _ in range(KOM_POZIOM)]

def stworz_pusta_plansze():
    return [[KOM_MARTWA] * KOM_PION for _ in range(KOM_POZIOM)]

# ----------------------------------------------------------------------------------------------------------------------
# przygotowanie następnej generacji komórek, czyli zaktualizowanego POLA_GRY
# Zasady przyrostu i spadku populacji – Gra w życie Conwaya:
#
# 1. Żywa komórka:
#    - umiera z powodu niedoludnienia, jeśli ma mniej niż 2 żywych sąsiadów,
#    - przeżywa, jeśli ma 2 lub 3 żywych sąsiadów,
#    - umiera z powodu przeludnienia, jeśli ma więcej niż 3 żywych sąsiadów.
#
# 2. Martwa komórka:
#    - ożywa (powstaje nowa komórka), jeśli ma dokładnie 3 żywych sąsiadów.
#
# W skrócie:
#    0–1 sąsiadów → śmierć żywej komórki (niedoludnienie)
#    2–3 sąsiadów → żywa komórka przeżywa
#    4–8 sąsiadów → śmierć żywej komórki (przeludnienie)
#    dokładnie 3 sąsiadów → powstanie nowej komórki
#
# Każda generacja jest obliczana na podstawie stanu wszystkich
# komórek z poprzedniej generacji.

def przygotuj_populacje(polegry):
    nast_gen = stworz_pusta_plansze() #wszystkie komórki są martwe :-|

    for x in range(KOM_POZIOM):
        for y in range(KOM_PION):
            populacja = 0

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                # (-1,-1)  (0,-1)  (1,-1)
                # (-1, 0)  (0, 0)  (1, 0)
                # (-1, 1)  (0, 1)  (1, 1)
                    if dx == 0 and dy == 0: #obviously not (0, 0)
                        continue

                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < KOM_POZIOM and 0 <= ny < KOM_PION: #Sprawdź sąsiada tylko wtedy, gdy jego współrzędne rzeczywiście znajdują się na planszy.
                        if polegry[nx][ny] == KOM_ZYWA:
                            populacja += 1

            if polegry[x][y] == KOM_ZYWA and (populacja < 2 or populacja > 3):
                nast_gen[x][y] = KOM_MARTWA

            elif polegry[x][y] == KOM_ZYWA and (populacja == 3 or populacja == 2):
                nast_gen[x][y] = KOM_ZYWA

            elif polegry[x][y] == KOM_MARTWA and populacja == 3:
                nast_gen[x][y] = KOM_ZYWA

    return nast_gen

def rysuj_populacje():
    """Rysowanie komórek (kwadratów) żywych"""
    for y in range(KOM_PION):
        for x in range(KOM_POZIOM):
            if POLE_GRY[x][y] == KOM_ZYWA:
                pygame.draw.rect(OKNOGRY, green, Rect(
                    (x * ROZ_KOM, y * ROZ_KOM), (ROZ_KOM, ROZ_KOM)), 1)


# zmienne sterujące wykorzystywane w pętli głównej
zycie_trwa = False
przycisk_wdol = False
przycisk_typ = 0

POLE_GRY = stworz_pusta_plansze()
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

#not pozwala sprawdzać wartość logiczną, a nie tylko konkretną wartość False
#To zadziała też dla:
#zycie_trwa =  0, ponieważ 0 jest traktowane jako wartość fałszywa False)
#zycie_trwa = "", ponieważ pusty napis jest traktowany jako False a pusty napis "" nie jest obiektem False

        if not zycie_trwa:
            pygame.display.set_caption('Gra o życie: ŻYCIE ZAMARŁO')



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

    if zycie_trwa:
        pygame.display.set_caption('Gra o życie: ŻYCIE TRWA')
        sleep(0.5)
        POLE_GRY = przygotuj_populacje(POLE_GRY)

    OKNOGRY.fill(black)  # Czyszczenie ekranu
    rysuj_populacje() # Rysowanie komórek

    # Rysowanie paska z instrukcją na dole (poniżej planszy gry)
    tekst_wys = instrukcja_tekst.get_size()[1]
    pygame.draw.rect( OKNOGRY, gray, (0, OKNOGRY_WYS, OKNOGRY.get_width(), tekst_wys + 10))
    OKNOGRY.blit(instrukcja_tekst, (10, OKNOGRY_WYS + 5))

    # Rysowanie paska stop/game over
    stop_tekst_szer, stop_tekst_wys = stop_tekst.get_size()
    x = (OKNOGRY.get_width() - stop_tekst_szer) // 2
    y = (OKNOGRY.get_height() - stop_tekst_wys) // 2
    pygame.draw.rect(OKNOGRY, gray, (0, y, OKNOGRY.get_width(), stop_tekst_wys))
    OKNOGRY.blit(stop_tekst, (x, y))


    pygame.display.update()