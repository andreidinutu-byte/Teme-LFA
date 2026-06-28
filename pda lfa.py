"""
PDA Simulator pentru limbajul A = {0^n 1^k | n >= 0, k >= 1}

Automat:
  Stari:    q0 (initiala), q1, q2 (finala)
  Stiva:    simbolul de baza Z0, simbol de lucru A
  Alfabet:  {0, 1}

Tranzitii:
  delta(q0, 0, Z0) = (q0, AZ0)   -- impinge A, pastreaza Z0
  delta(q0, 0, A)  = (q0, AA)    -- impinge inca un A
  delta(q0, 1, Z0) = (q1, Z0)    -- prima cifra 1 (n=0), nu modifica stiva
  delta(q0, 1, A)  = (q1, A)     -- prima cifra 1 (n>0), nu modifica stiva
  delta(q1, 1, Z0) = (q1, Z0)    -- mai multe cifre 1, pastreaza stiva
  delta(q1, 1, A)  = (q1, A)     -- mai multe cifre 1, pastreaza stiva
  delta(q1, e, Z0) = (q2, Z0)    -- epsilon-tranzitie la starea finala

Acceptare prin stare finala: q2
"""


def run_pda(w: str, verbose: bool = True) -> bool:
    """
    Ruleaza PDA-ul pe sirul w.
    Returneaza True daca sirul e acceptat, False altfel.
    """
    state = "q0"
    stack = ["Z0"]  # varful stivei e la sfarsitul listei
    pos = 0

    def log(msg):
        if verbose:
            top = stack[-1] if stack else "gol"
            print(f"  Pas {pos:>2} | stare={state} | citit='{w[pos] if pos < len(w) else 'ε'}' "
                  f"| varf_stiva={top} | {msg}")

    if verbose:
        print(f"\nSir: '{w}' {'(epsilon)' if w == '' else ''}")
        print(f"  {'Pas':>4} | stare  | citit | varf   | actiune")
        print("  " + "-" * 55)

    while pos < len(w):
        ch = w[pos]
        top = stack[-1] if stack else None

        if state == "q0":
            if ch == "0":
                if top == "Z0":
                    stack.pop()
                    stack.append("A")
                    stack.append("Z0")
                    log("delta(q0, 0, Z0) -> (q0, AZ0) | impinge A")
                elif top == "A":
                    stack.append("A")
                    log("delta(q0, 0, A)  -> (q0, AA)  | impinge A")
                else:
                    log("EROARE: stiva goala")
                    return False
                pos += 1

            elif ch == "1":
                if top in ("Z0", "A"):
                    log(f"delta(q0, 1, {top}) -> (q1, {top}) | prima cifra 1, tranzitie la q1")
                    state = "q1"
                    pos += 1
                else:
                    log("EROARE: stiva goala")
                    return False
            else:
                log(f"EROARE: caracter invalid '{ch}'")
                return False

        elif state == "q1":
            if ch == "1":
                log(f"delta(q1, 1, {top}) -> (q1, {top}) | ramane in q1")
                pos += 1
            elif ch == "0":
                log("EROARE: cifra '0' dupa '1' – nu e permis")
                return False
            else:
                log(f"EROARE: caracter invalid '{ch}'")
                return False
        else:
            log("EROARE: stare neasteptata")
            return False

    # Am consumat tot sirul – epsilon-tranzitie
    if state == "q1":
        if verbose:
            print(f"  {'ε':>4} | q1     |  ε    | {stack[-1]}    | "
                  f"delta(q1, e, Z0) -> (q2, Z0) | acceptare!")
        state = "q2"
    elif state == "q0":
        if verbose:
            print(f"  {'ε':>4} | q0     |  ε    |       | "
                  f"sirul s-a terminat in q0 – nicio cifra '1' – RESPINS")

    accepted = state == "q2"
    if verbose:
        verdict = "ACCEPTAT ✓" if accepted else "RESPINS ✗"
        print(f"\n  Rezultat: {verdict}\n")
    return accepted


def main():
    # --- Teste automate ---
    teste = [
        ("1",       True,  "un singur 1"),
        ("11",      True,  "mai multi 1"),
        ("01",      True,  "un 0, un 1"),
        ("001",     True,  "doi 0, un 1"),
        ("000111",  True,  "trei 0, trei 1"),
        ("11111",   True,  "numai 1"),
        ("",        False, "sir gol (k<1)"),
        ("0",       False, "numai 0 (k<1)"),
        ("000",     False, "numai 0 (k<1)"),
        ("10",      False, "1 urmat de 0"),
        ("101",     False, "1, 0, 1"),
    ]

    print("=" * 60)
    print("  PDA Simulator — A = {0^n 1^k | n >= 0, k >= 1}")
    print("=" * 60)

    print("\n--- Rulare detaliata pe cateva exemple ---")
    for sir, _, _ in teste[:4]:
        run_pda(sir, verbose=True)

    print("\n--- Tabel rezumat pentru toate testele ---")
    print(f"  {'Sir':<12} {'Asteptat':<12} {'Obtinut':<12} {'Descriere'}")
    print("  " + "-" * 55)
    all_ok = True
    for sir, asteptat, desc in teste:
        obtinut = run_pda(sir, verbose=False)
        ok = obtinut == asteptat
        all_ok = all_ok and ok
        status = "OK  ✓" if ok else "FAIL ✗"
        afis_sir = f"'{sir}'" if sir else "'ε'"
        print(f"  {afis_sir:<12} {str(asteptat):<12} {str(obtinut):<12} {desc}  [{status}]")

    print(f"\n  {'Toate testele au trecut! ✓' if all_ok else 'Unele teste au esuat! ✗'}")
    print()

    # --- Mod interactiv ---
    print("--- Mod interactiv (scrie 'exit' pentru a iesi) ---")
    while True:
        sir = input("  Introdu un sir: ").strip()
        if sir.lower() == "exit":
            break
        run_pda(sir, verbose=True)


if __name__ == "__main__":
    main()