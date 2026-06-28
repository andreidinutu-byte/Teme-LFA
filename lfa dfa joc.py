import json
import os

class InterpretDFA:
    def __init__(self, fisier_config):
        with open(fisier_config, 'r', encoding='utf-8') as f:
            self.date = json.load(f)
        self.stare_curenta = self.date["stare_initiala"]
        self.finale = self.date["stari_finale"]
        self.harta = self.date["dfa"]

    def ruleaza(self):
        print("--- MOTOR DFA PORNIȚI ---")

        while True:
            camera_actuala = self.harta[self.stare_curenta]
            print(f"\n---------------------------------")
            print(f"LOCAȚIE: {self.stare_curenta}")
            print(camera_actuala["descriere"])
            if self.stare_curenta in self.finale:
                break
            optiuni = list(camera_actuala["tranzitii"].keys())
            print(f"Comenzi posibile: {optiuni}")
            comanda = input("> ").lower().strip()
            if comanda in camera_actuala["tranzitii"]:
                self.stare_curenta = camera_actuala["tranzitii"][comanda]
            else:
                print(f"\n[!] Simbolul '{comanda}' nu face parte din alfabetul acestei stări!")
        print("\n--- EXIT AUTOMATON ---")
if __name__ == "__main__":
    if os.path.exists('aventura3.json'):
        joc = InterpretDFA('aventura3.json')
        joc.ruleaza()
    else:
        print("Eroare: Fișierul 'aventura3.json' nu a fost găsit!")