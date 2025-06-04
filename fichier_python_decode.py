"""
La base de données était illisible en l'état, car certains textes étaient doublement corrompus: UTF-8 → ISO-8859-1 → UTF-8
On renvoie donc un csv correctement encodé en utf8
"""

import codecs

input_file = "tweets_csv_2.csv"
output_file = "tweets_csv_utf8_corrige_final.csv"

def double_decode(text):
    current = text
    for _ in range(2):
        try:
            # réinterprête comme s'il y avait eu mauvaise lecture ISO-8859-1
            current = current.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
        except Exception:
            break
    return current

with open(input_file, "r", encoding="latin1", errors="replace") as f_in:
    lines = f_in.readlines()

with open(output_file, "w", encoding="utf-8") as f_out:
    for line in lines:
        cleaned = double_decode(line)
        f_out.write(cleaned)

print(f"Fichier corrigé enregistré sous : {output_file}")
