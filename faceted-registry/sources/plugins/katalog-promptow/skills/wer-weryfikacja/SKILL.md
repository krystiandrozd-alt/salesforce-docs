---
name: wer-weryfikacja
description: Techniki z katalogu KD do weryfikacji (WER-01..04) — twarda weryfikacja w sieci z tabelą potwierdzone/obalone/nie znaleziono, audytor z premią za błędy, oznaczanie [F]/[I]/[?] (fakt vs wnioskowanie), kontrola wyrywkowa 10% danych. Użyj zawsze, gdy coś ma wyjść poza Enxoo (do klienta, w ofercie, w RFP), oraz gdy użytkownik pisze „zweryfikuj”, „sprawdź to”, „czy to prawda”, „przejrzyj jak audytor”, „co tu jest wnioskiem”, „oznacz pewność”, „sprawdź próbkę”, podaje ID WER-01..04, albo pyta o możliwości produktu, TM Forum lub licencje.
---

# WER · Weryfikacja

Cztery techniki kontroli jakości. Wspólna zasada: **brak potwierdzenia zostaje brakiem potwierdzenia** — nigdy nie awansuj „nie znaleziono” do „potwierdzone” i nie łataj luk domysłem.

| ID | Kiedy | Nie |
|---|---|---|
| WER-01 | Zawsze przed wysłaniem czegokolwiek poza Enxoo | Brak wyjątków — to jedyna pozycja, której się nie pomija |
| WER-02 | Dokument gotowy, przed ostatnim czytaniem | W trakcie pisania — zabija tempo |
| WER-03 | Odpowiedź o możliwościach produktu, TMF, licencjach | Pytania bezsporne, gdzie to tylko szum |
| WER-04 | Praca masowa na danych — arkusze, ekstrakcja, przepisywanie | Pojedynczy dokument — sprawdź w całości |

Dla WER-02..04 sprawdź warunek „Nie”; jeśli spełniony, powiedz to w zdaniu i zaproponuj właściwszą technikę. Jeśli materiał wyraźnie idzie do klienta, a użytkownik prosi o coś innego, zaproponuj na końcu WER-01.

## WER-01 · Twarda weryfikacja

> Zweryfikuj powyższe wyszukiwaniem w sieci. Rozpisz w tabeli: twierdzenie | potwierdzone / obalone / nie znaleziono | źródło. Nie uzupełniaj luk domysłem — brak potwierdzenia zostaw jako brak potwierdzenia.

Wykonanie:
1. Rozbij materiał na pojedyncze, sprawdzalne twierdzenia (liczby, nazwy, daty, możliwości produktu, cytaty).
2. Dla każdego wyszukaj osobno; preferuj źródła pierwotne (dokumentacja producenta, help.salesforce.com, tmforum.org, raporty spółek).
3. Tabela: twierdzenie | status | źródło (link) | uwaga.
4. Pod tabelą: lista twierdzeń do usunięcia lub przeformułowania.

Dlaczego trzecia kategoria: bez „nie znaleziono” każde niesprawdzone twierdzenie cicho przechodzi jako potwierdzone.

## WER-02 · Audytor z premią za błędy

> Sprawdź powyższą pracę jak audytor, który dostaje premię za każdy znaleziony błąd: zgodność liczb, spójność terminologii, braki, rzeczy zrobione na skróty, twierdzenia bez pokrycia. Wypisz wszystko, dopiero potem popraw.

Najpierw pełna lista ustaleń (kategoria | miejsce | problem | waga), bez poprawiania. Liczby sprawdzaj rachunkiem (przelicz, nie szacuj). Dopiero po liście — poprawiona wersja lub lista poprawek.

## WER-03 · Oddziel wiedzę od wnioskowania

> Przejdź przez swoją odpowiedź i oznacz każde twierdzenie:
> [F] fakt z dokumentacji — podaj gdzie
> [I] wnioskowanie — podaj, z czego wynika
> [?] nie wiem
> Jeśli czegoś nie da się przypisać do żadnej kategorii, usuń.

Konwencja [F]/[I]/[?] jest wspólna dla całego katalogu — te same etykiety stosuj w RFP-01 i jako property `confidence` w notatkach (VLT-01). Przy [F] podaj konkretne miejsce w dokumentacji; jeśli nie potrafisz, to nie jest [F].

## WER-04 · Kontrola wyrywkowa

> Wybierz losowo 10% pozycji z wyniku i pokaż mi je obok danych źródłowych, wiersz w wiersz. Nie wybieraj tych, które wyszły najlepiej.

Losuj naprawdę: gdy masz dostęp do kodu, użyj generatora losowego i pokaż ziarno lub listę wylosowanych indeksów. Minimum 5 pozycji przy małych zbiorach. Tabela: indeks | źródło | wynik | zgodne? Na końcu odsetek rozbieżności i czy uzasadnia pełne sprawdzenie. Losowość jest niezbędna — wybór „ładnych” pozycji daje próbkę reprezentatywną dla sukcesu, nie dla całości.
