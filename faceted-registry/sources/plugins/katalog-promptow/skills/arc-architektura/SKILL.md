---
name: arc-architektura
description: Techniki z katalogu KD dla architektury (ARC-01..03) — szkic ADR z warunkiem rewizji, porównanie opcji z kosztem zmiany i „kiedy to zły wybór”, analiza wpływu zmiany (co się zepsuje — zależności twarde/miękkie/wzmianki). Użyj, gdy użytkownik chce „zapisać decyzję”, „zrobić ADR”, „porównać opcje”, „trade-offy”, „którą drogę wybrać”, „co się zepsuje, jak zmienię X”, „impact analysis”, albo podaje ID ARC-01..03.
---

# ARC · Architektura

Trzy techniki dla decyzji architektonicznych. Najpierw rozpoznaj stan decyzji: otwarta → ARC-02; zapadła → ARC-01; dotyczy zmiany istniejącego komponentu → ARC-03.

| ID | Kiedy | Nie |
|---|---|---|
| ARC-01 | Decyzja zapadła i trzeba ją utrwalić | Decyzja jeszcze otwarta — najpierw ARC-02 |
| ARC-02 | Rozwiązanie ma więcej niż jedną drogę | Droga jest jedna, a użytkownik szuka potwierdzenia — powiedz to wprost |
| ARC-03 | Zmiana w komponencie, na którym coś stoi | Brak zapisanych zależności — nie będzie z czego czytać; zaproponuj ich spisanie |

Gdy warunek „Nie” jest spełniony, powiedz to w zdaniu i przekieruj na właściwą technikę.

## ARC-01 · Szkic ADR

> Zamień poniższe ustalenia w ADR:
> Kontekst — co wymusiło decyzję
> Rozważane opcje — tabela: opcja | za | przeciw | koszt
> Decyzja — jedno zdanie, w trybie oznajmującym
> Uzasadnienie — dlaczego ta, a nie sąsiednia
> Konsekwencje — co teraz staje się trudniejsze
> Kiedy to przemyśleć ponownie — konkretny warunek
> Nie wygładzaj. Jeśli decyzja była kompromisem, napisz to.

Dla vaulta Obsidian dodaj frontmatter (type: adr, status, domain, created, confidence). Warunek rewizji ma być mierzalny lub zdarzeniowy („gdy wolumen zamówień > X/dzień”, „gdy Salesforce wycofa Y”), nie „w razie potrzeby”. ADR bez warunku rewizji staje się dogmatem. Nie dopisuj opcji ani argumentów, których nie ma w ustaleniach — braki wypisz jako pytania.

## ARC-02 · Porównanie opcji

> Rozpisz opcje w tabeli: opcja | co zyskujemy | co tracimy | koszt zmiany później | kiedy to zły wybór.
> Potem odpowiedz na dwa pytania:
> – która opcja jest najtrudniejsza do wycofania?
> – co musiałoby być prawdą, żeby wybrać tę, którą dziś odrzucasz?

Odpowiedz na oba pytania osobnymi akapitami. Drugie pytanie wymaga konkretnych warunków, nie ogólników — to ono odsłania ukryte założenia.

## ARC-03 · Co się zepsuje

> Zmieniam [komponent / wzorzec]. Przejdź po notatkach i wypisz wszystko, co się na tym opiera. Podziel na: zależność twarda (przestanie działać) | miękka (do przejrzenia) | wzmianka (bez wpływu). Jeśli nie masz pewności, do której grupy coś należy, wpisz je do twardych.

Źródłem są notatki/vault użytkownika (lub repozytorium, jeśli podał) — przeszukaj je narzędziami (grep po nazwie, aliasach, linkach). Przy każdej pozycji podaj plik i dlaczego trafiła do grupy. Niepewne → twarde: koszt fałszywego alarmu jest niższy niż koszt przeoczonej awarii.
