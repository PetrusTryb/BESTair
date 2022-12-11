# BESTair

Prosta aplikacja dane o jakości powietrza w Polsce, w danym czasie, dla całego kraju lub danej stacji pomiarowej.

## Uruchomienie

1. Pobierz repozytorium oraz wygenerowaną przez nas [bazę danych](https://mega.nz/file/0dUxARQZ#BOSIBJHgNK6IPXcwrukHydDVBgv6iplWgWXE-WKD3t4).
Kod źródłowy, który posłużył do jej wygenerowania znajduje się w katalogu `back-end/dbGenerator`.
2. Umieść pobraną bazę danych w katalogu `back-end` pod nazwą `data.db`.
3. Zainstaluj [Docker](https://docs.docker.com/install/).
4. Wykonaj komendę `docker-compose build && docker-compose up` w katalogu głównym repozytorium.
5. Aplikacja powinna być dostępna pod adresem `localhost:80`.

## Wykorzystane technologie i frameworki

### Front-end
- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
### Back-end
- [SQLite](https://www.sqlite.org/index.html)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
### DevOps
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Autorzy

- Piotr Trybisz
- Stanisław Nieradko
- Bartłomiej Krawisz
- Krzysztof Nasuta