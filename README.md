# 🕵️ Blind SQLi Challenge – "Order Matters"

## 📜 Opis

Twoim zadaniem jest wydobycie flagi znajdującej się w bazie danych, **bez bezpośredniego podglądania jej zawartości**.  
Strona umożliwia przeglądanie postów blogowych, a niektóre z nich mogą zawierać subtelne wskazówki…

---

## ⚠️ Uwaga dotycząca pliku `dbscript`

Plik `dbscript` zawiera:
- pełny schemat bazy danych
- **flagę** ukrytą w tabeli `flags`

🔐 **Jeśli chcesz mieć pełne doświadczenie z zadania (czyli rozwiązać je jak w prawdziwym CTF), NIE czytaj pliku `dbscript` przed rozwiązaniem.**

To tak jakby podejrzeć odpowiedzi zanim zaczniesz — niby można, ale psuje całą zabawę 😉

---

## 🚀 Uruchomienie

Aby uruchomić zadanie lokalnie:

```bash
pip install flask
python app.py
