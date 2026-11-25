---
name: vlt-notatki-vault
description: Techniki z katalogu KD dla notatek i vaulta Obsidian (VLT-01..04) — notatka z ustaleń z frontmatterem (type, status, client, domain, confidence, created), typowanie linków z zamkniętej listy relacji, przetworzenie 00-inbox/ partiami do zatwierdzenia, miesięczny audyt spójności properties i linków. Użyj, gdy użytkownik wkleja surowe notatki ze spotkania i chce notatkę do vaulta, pisze „otypuj linki”, „przejrzyj inbox”, „uporządkuj wrzutki”, „audyt vaulta”, „niespójne properties”, albo podaje ID VLT-01..04.
---

# VLT · Notatki i vault

Cztery techniki do pracy z vaultem. Wspólne zasady:
- **Nic nie przenoś, nie zmieniaj ani nie usuwaj bez zatwierdzenia** — proponuj, pokazuj listę, działaj partiami.
- **Nie dopisuj treści spoza materiału** — braki wypisuj jako pytania.
- `confidence` w frontmatterze używa konwencji F / I / ? (jak WER-03).
- Pisząc markdown dla Obsidiana, stosuj składnię Obsidian (wikilinki, properties); jeśli dostępny jest skill obsidian-markdown, skorzystaj z niego.

| ID | Kiedy | Nie |
|---|---|---|
| VLT-01 | Zaraz po rozmowie, póki kontekst jest świeży | Po tygodniu — to już rekonstrukcja; zaznacz w notatce niską pewność |
| VLT-02 | Notatka ma linki, ale nie wiadomo, co znaczą | Brak zamkniętej listy dozwolonych relacji — najpierw ją ustal |
| VLT-03 | Raz w tygodniu, na wrzutki z `00-inbox/` | Nigdy jako masowa operacja na całym vaulcie |
| VLT-04 | Co miesiąc, albo przed budową pierwszej bazy | Mniej niż kilkanaście notatek — nie ma czego audytować |

## VLT-01 · Notatka z ustaleń

> Zamień moje surowe notatki w notatkę do vaulta.
> Frontmatter: type, status, client, domain, confidence, created
> Treść:
> – Ustalenia (co zostało przesądzone)
> – Otwarte (co wisi, kto ma ruch)
> – Ryzyka
> – Linki do powiązanych notatek, z typem relacji
> Nie dopisuj niczego, czego nie ma w moich notatkach. Czego brakuje — wypisz jako pytania na końcu.

`created` = dzisiejsza data (YYYY-MM-DD), chyba że notatki podają inną. W „Otwarte” przy każdym punkcie: kto ma ruch. Zwróć gotowy plik `.md`.

## VLT-02 · Otypuj linki

> Przejrzyj linki w tej notatce. Dla każdego zaproponuj typ relacji z listy: [lista użytkownika — np. używa, rozszerza, zastępuje, wynika-z, patrz-też]. Wypisz jako propozycję frontmattera. Linki, których nie da się przypisać do żadnego typu, zostaw i oznacz — być może nie powinno ich tam być.

Jeśli użytkownik nie podał listy, zapytaj o nią (przykładową podaj jako punkt startu) — nie wymyślaj nowych typów. Bez zamkniętej listy w miesiąc powstają cztery nazwy tej samej relacji i mapa przestaje działać.

## VLT-03 · Przetworzenie inboxa

> Przejdź po notatkach w 00-inbox/ i dla każdej zaproponuj: docelowy katalog | frontmatter | czy to duplikat czegoś, co już mam. Nic nie przenoś ani nie zmieniaj. Pokaż mi listę do zatwierdzenia — działamy partiami.

Partia ≈ 10 notatek. Duplikaty sprawdzaj po tytule, aliasach i treści. Po zatwierdzeniu partii wykonaj tylko zatwierdzone ruchy i pokaż kolejną.

## VLT-04 · Audyt spójności

> Przejrzyj strukturę vaulta i wypisz niespójności:
> – properties użyte w różnych wariantach nazwy
> – notatki bez wymaganych properties
> – linki do nieistniejących notatek
> – typy relacji spoza mojej listy
> Sam wynik, bez poprawiania. Posortuj po tym, co najbardziej psuje filtrowanie.

Gdy masz dostęp do plików, policz to skryptem (parsowanie frontmattera, rozwiązywanie wikilinków), nie na oko. Wynik: tabela kategoria | liczba | przykłady (pliki), posortowana od tego, co najbardziej psuje filtrowanie i bazy (.base). Nie poprawiaj.
