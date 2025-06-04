# traduction_utf8.py
import codecs

input_file = "tweets_csv_2.csv"
output_file = "tweets_csv_utf8_corrige.csv"

with open(input_file, "r", encoding="latin1", errors="replace") as f_in:
    lines = f_in.readlines()

with open(output_file, "w", encoding="utf-8") as f_out:
    for line in lines:
        try:
            corrected = line.encode("latin1").decode("utf-8")
        except UnicodeDecodeError:
            corrected = codecs.decode(line.encode("latin1"), "utf-8", errors="replace")
        f_out.write(corrected)

print(f"✅ Fichier corrigé enregistré sous : {output_file}")
