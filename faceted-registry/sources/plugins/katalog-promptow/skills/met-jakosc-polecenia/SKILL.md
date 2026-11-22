---
name: met-jakosc-polecenia
description: Techniki z katalogu KD dla jakości polecenia (MET-01..03) — popraw prompt, dopytaj do 95% pewności, najpierw plan potem robota. Użyj, gdy użytkownik pisze „popraw mój prompt”, „dopytaj mnie”, „nie zgaduj”, „najpierw rozpisz plan”, „zatrzymaj się przed wykonaniem”, podaje ID MET-01/MET-02/MET-03, albo zleca nowy typ zadania lub wieloetapową robotę z niejasnym briefem, gdzie złe założenie na starcie dużo kosztuje.
---

# MET · Jakość polecenia

Trzy techniki, które działają **przed** wykonaniem zadania. Każda ma warunek użycia i warunek „Nie”. Zanim zastosujesz technikę, sprawdź warunek „Nie”: jeśli jest spełniony, powiedz to w jednym zdaniu i zaproponuj, że po prostu wykonasz zadanie — prompt użyty w złym momencie kosztuje więcej czasu, niż oszczędza. Jeśli użytkownik mimo to chce techniki, zastosuj ją.

Wybór trybu: jeśli użytkownik podał ID — użyj go. W przeciwnym razie dobierz po sytuacji (tabela niżej). Jeśli pasuje więcej niż jedna, zacznij od tej, która działa najwcześniej (MET-01 → MET-02 → MET-03).

| ID | Kiedy | Nie |
|---|---|---|
| MET-01 | Nowy typ zadania, którego użytkownik jeszcze nie robił rutynowo | Zadanie znane i powtarzalne — tylko opóźnia |
| MET-02 | Brief niejasny, a koszt złego założenia realny | Proste zadanie — dostaniesz przesłuchanie zamiast wyniku |
| MET-03 | Zadanie wieloetapowe, gdzie zły kierunek na starcie kosztuje wszystko | Jeden krótki deliverable |

## MET-01 · Popraw mój prompt

Rdzeń techniki:
> Zanim wykonasz moje polecenie, najpierw je popraw. Wskaż niejasności, braki i założenia. Potem napisz lepszą, precyzyjną wersję promptu.

Wykonanie:
1. Wypisz osobno: **niejasności** (co da się zrozumieć na dwa sposoby), **braki** (czego brakuje, żeby zrobić to dobrze), **założenia** (co musiałbyś przyjąć sam).
2. Napisz poprawioną wersję promptu w bloku kodu, gotową do użycia.
3. Zapytaj, czy wykonać zadanie według poprawionej wersji — nie wykonuj go od razu.

Dlaczego: wartość jest w nauce. Po kilku razach użytkownik widzi własne nawykowe braki i przestaje tej techniki potrzebować — dlatego nazywaj braki konkretnie, tak by dało się z nich wyciągnąć wzorzec.

## MET-02 · Dopytaj do 95%

Rdzeń techniki:
> Nie zgaduj i nie uzupełniaj braków samodzielnie. Zadawaj mi po jednym pytaniu doprecyzowującym, aż osiągniesz co najmniej 95% pewności, że rozumiesz cel, odbiorcę, ograniczenia i oczekiwany format wyniku. Dopiero wtedy wykonaj zadanie.

Wykonanie:
- Zadawaj **jedno** pytanie na raz. Kolejność wymiarów: cel → odbiorca → ograniczenia → format.
- Przy każdym pytaniu krótko oznacz, który wymiar domyka (np. „[odbiorca]”).
- Nie pytaj o rzeczy, które da się ustalić z materiałów, rozmowy lub pamięci — sprawdź najpierw.
- Gdy wszystkie cztery wymiary są domknięte, podsumuj je w 4 linijkach i wykonaj zadanie.

Dlaczego: cztery wymiary to lista kontrolna, po której użytkownik poznaje, czy pytania idą we właściwą stronę. Pytanie spoza nich zwykle jest szumem.

## MET-03 · Najpierw plan, potem robota

Rdzeń techniki:
> Nie wykonuj jeszcze zadania. Rozpisz plan: etapy, co powstaje na każdym, gdzie potrzebujesz mojej decyzji. Zatrzymaj się i czekaj na moją akceptację planu.

Wykonanie:
1. Tabela: etap | co powstaje | decyzja użytkownika (tak/nie + jaka).
2. Pod tabelą: największe ryzyko kierunku i jak plan je ogranicza (1–2 zdania).
3. Zatrzymaj się. Nie zaczynaj etapu 1 bez akceptacji.
