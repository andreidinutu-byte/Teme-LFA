# ==========================================
#  Configurația Automatului (NFA)
# ==========================================
nod_start = 'q0'
noduri_finale = {'q2', 'q3'}
alfabet = {'0', '1'}

# Expresia recunoscută: 1* 00 1* 0*
tranzitii = {
    ('q0', '1'): {'q0'},
    ('q0', '0'): {'q1'},
    ('q1', '0'): {'q2'},
    ('q2', '1'): {'q2'},
    ('q2', '0'): {'q3'},
    ('q3', '0'): {'q3'}
}


# ==========================================
#  Logica de Procesare
# ==========================================
def proceseaza_cuvant(cuvant):
    stari_active = {nod_start}
    traseu = [stari_active]

    for litera in cuvant:
        if litera not in alfabet:
            return False, traseu, f"Simbolul '{litera}' nu face parte din alfabetul {alfabet}."

        stari_urmatoare = set()
        for stare in stari_active:
            if (stare, litera) in tranzitii:
                stari_urmatoare.update(tranzitii[(stare, litera)])

        stari_active = stari_urmatoare
        traseu.append(stari_active)

        if not stari_active:
            break

    acceptat = bool(stari_active.intersection(noduri_finale))
    return acceptat, traseu, None


# ==========================================
#  Interfața de Testare
# ==========================================
def ruleaza_testare():
    print("=== Verificare NFA ===")
    print("Regulă curentă: Cuvinte ce respectă tiparul 1* 00 1* 0*")
    print("(scrie 'stop' pentru a opri execuția)\n")

    while True:
        cuvant = input("Cuvânt de testat: ").strip()

        if cuvant.lower() == 'stop':
            print("Program încheiat.")
            break

        if cuvant == "":
            if nod_start in noduri_finale:
                print("  Rezultat: ACCEPTAT ✓ (Cuvânt vid)\n")
            else:
                print("  Rezultat: RESPINS ✗ (Cuvânt vid)\n")
            continue

        acceptat, traseu, eroare = proceseaza_cuvant(cuvant)

        if eroare:
            print(f"  [!] Eroare: {eroare}\n")
        else:
            pasi = ["{" + ",".join(sorted(pas)) + "}" if pas else "∅" for pas in traseu]
            print(f"  Traseu: {' ➔ '.join(pasi)}")

            if acceptat:
                print("  Rezultat: ACCEPTAT ✓\n")
            else:
                print("  Rezultat: RESPINS ✗\n")


if __name__ == "__main__":
    ruleaza_testare()