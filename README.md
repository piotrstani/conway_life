
 'Instrukcja: 
 LPM - dodaje komórkę,  PPM - usuwa komórkę
 ENTER - start,  ESC - pauza'
 
Zasady przyrostu i spadku populacji – Gra w życie Conwaya:

 1. Żywa komórka:
    - umiera z powodu niedoludnienia, jeśli ma mniej niż 2 żywych sąsiadów,
    - przeżywa, jeśli ma 2 lub 3 żywych sąsiadów,
    - umiera z powodu przeludnienia, jeśli ma więcej niż 3 żywych sąsiadów.

 2. Martwa komórka:
    - ożywa (powstaje nowa komórka), jeśli ma dokładnie 3 żywych sąsiadów.

 W skrócie:
    0–1 sąsiadów → śmierć żywej komórki (niedoludnienie)
    2–3 sąsiadów → żywa komórka przeżywa
    4–8 sąsiadów → śmierć żywej komórki (przeludnienie)
    dokładnie 3 sąsiadów → powstanie nowej komórki

 Każda generacja jest obliczana na podstawie stanu wszystkich
 komórek z poprzedniej generacji.



1. INFO nad 'ŻYCIE TRWA' (na zielono) i wręcz przeciwnie (na czerwono)
2. STATYSTYKI (taki zboczku panel), komórek born,died, max, min, duartion 
3. a jakby te STATYSTYKI zrzucać do pliku i zrobić z tego panel best score (taki wyswietlany pomiędzy ESC a ENTER)
