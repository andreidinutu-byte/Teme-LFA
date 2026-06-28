# =====================================================
#
#   E L I Z A  -  P R O G R A M U L  D O C T O R
#
#   Traducere fidela dupa Joseph Weizenbaum, 1966
#   MIT - Communications of the ACM, Ianuarie 1966
#
#   Caracteristici originale pastrate:
#   - Cuvinte cheie cu prioritati (ranguri)
#   - Raspunsuri CICLATE in ordine (nu random)
#   - Memorie pentru fallback
#   - Pre-substitutii (normalizare input)
#   - Post-substitutii (transformare pronume)
#   - Output cu MAJUSCULE (ca la teletype)
#
# =====================================================

import re
import sys


# =====================================================
# PRE-SUBSTITUTII
# Normalizeaza inputul inainte de procesare
# =====================================================

PRE = [
    (r"\bnu-mi\b",   "nu imi"),
    (r"\bmi-e\b",    "imi este"),
    (r"\bmi-a\b",    "imi a"),
    (r"\bn-am\b",    "nu am"),
    (r"\bn-ai\b",    "nu ai"),
    (r"\bn-are\b",   "nu are"),
    (r"\bnu-i\b",    "nu este"),
    (r"\bti-e\b",    "iti este"),
    (r"\bm-am\b",    "m am"),
    (r"\bm-ai\b",    "m ai"),
    (r"\bm-a\b",     "m a"),
    (r"\bnicicand\b","niciodata"),
    (r"\bnicaieri\b","niciodata"),
]


# =====================================================
# POST-SUBSTITUTII
# Transforma pronumele din raspuns (eu->tu, meu->tau etc.)
# =====================================================

POST = {
    "eu":        "tu",
    "tu":        "eu",
    "ma":        "te",
    "te":        "ma",
    "mie":       "tie",
    "tie":       "mie",
    "meu":       "tau",
    "tau":       "meu",
    "mea":       "ta",
    "ta":        "mea",
    "mei":       "tai",
    "tai":       "mei",
    "mele":      "tale",
    "tale":      "mele",
    "imi":       "iti",
    "iti":       "imi",
    "sunt":      "esti",
    "esti":      "sunt",
    "am":        "ai",
    "ai":        "am",
    "stiu":      "stii",
    "stii":      "stiu",
    "simt":      "simti",
    "simti":     "simt",
    "vreau":     "vrei",
    "vrei":      "vreau",
    "pot":       "poti",
    "poti":      "pot",
    "fac":       "faci",
    "faci":      "fac",
    "gandesc":   "gandesti",
    "gandesti":  "gandesc",
    "iubesc":    "iubesti",
    "iubesti":   "iubesc",
}


def post_transforma(text):
    """Transforma pronumele dintr-o bucata de text capturata."""
    cuvinte = text.split()
    rezultat = []
    for cuv in cuvinte:
        punct = ""
        if cuv and cuv[-1] in ".,!?":
            punct = cuv[-1]
            cuv = cuv[:-1]
        rezultat.append(POST.get(cuv.lower(), cuv) + punct)
    return " ".join(rezultat)


def normalizeaza(text):
    """
    Sterge diacriticele pentru matching uniform.
    Originalul lucra cu ASCII pur (teletype nu avea diacritice).
    """
    tabel = {
        'a': 'a', 'a': 'a', 'i': 'i', 's': 's', 't': 't',
        'A': 'A', 'A': 'A', 'I': 'I', 'S': 'S', 'T': 'T',
        'a': 'a', 'a': 'a', 'i': 'i', 's': 's', 't': 't',
        '\u0103': 'a', '\u00e2': 'a', '\u00ee': 'i',
        '\u0219': 's', '\u021b': 't', '\u015f': 's', '\u0163': 't',
        '\u0102': 'A', '\u00c2': 'A', '\u00ce': 'I',
        '\u0218': 'S', '\u021a': 'T', '\u015e': 'S', '\u0162': 'T',
    }
    rezultat = []
    for ch in text:
        rezultat.append(tabel.get(ch, ch))
    return "".join(rezultat)


def pre_transforma(text):
    """Aplica pre-substitutiile asupra inputului."""
    for pattern, inlocuire in PRE:
        text = re.sub(pattern, inlocuire, text, flags=re.IGNORECASE)
    return text


# =====================================================
# SCRIPTUL DOCTOR - 66 CUVINTE CHEIE
#
# Format:
#   (cuvant_cheie, prioritate, [(pattern, [raspuns1, raspuns2, ...])])
#
# Prioritatile sunt ca in original:
#   50 = calculator/masina (maxim)
#   15 = nume
#   10 = familie, asemanare
#    8 = membri familie extinsa
#    5 = amintiri, sentimente, ganduri
#    4 = vise, munca
#    3 = conditionale, probleme
#    2 = generalizari (toti, nimeni)
#    1 = adverbe absolute (mereu, niciodata)
#    0 = tot restul
#
# Raspunsurile sunt CICLATE (pointer avanseaza),
# exact ca in implementarea originala MAD-SLIP.
# =====================================================

SCRIPT = [

    # --------------------------------------------------
    # SALUTURI
    # --------------------------------------------------
    ("salut", 0, [
        (r".*", [
            "Buna ziua. Va rog sa-mi spuneti problema dumneavoastra.",
        ])
    ]),
    ("buna", 0, [
        (r".*", [
            "Buna ziua. Va rog sa-mi spuneti ce va preocupa.",
        ])
    ]),
    ("hei", 0, [
        (r".*", [
            "Buna ziua. Cu ce va pot ajuta?",
        ])
    ]),

    # --------------------------------------------------
    # CALCULATOR / MASINA  (prioritate 50 - maxima)
    # Weizenbaum a ales aceasta prioritate intentionat:
    # pacientii care mentionau calculatorul erau redirectionati
    # --------------------------------------------------
    ("calculator", 50, [
        (r".*", [
            "Credeti ca oamenii seamana cu calculatoarele?",
            "De ce va ganditi la calculatoare?",
            "Calculatoarele va preocupa?",
            "Ce inseamna pentru dumneavoastra un calculator?",
            "Va simtiti amenintat de calculatoare?",
        ])
    ]),
    ("masina", 50, [
        (r".*", [
            "De ce va ganditi la masini?",
            "Masinile va preocupa?",
            "Va simtiti amenintat de masini?",
        ])
    ]),
    ("robot", 50, [
        (r".*", [
            "De ce va ganditi la roboti?",
            "Robotii va preocupa?",
            "Va simtiti amenintat de roboti?",
        ])
    ]),
    ("computer", 50, [
        (r".*", [
            "Credeti ca oamenii seamana cu computerele?",
            "De ce va ganditi la computere?",
            "Computerele va preocupa?",
        ])
    ]),

    # --------------------------------------------------
    # NUME  (prioritate 15)
    # Originalul refuza sa discute despre identitate
    # --------------------------------------------------
    ("nume", 15, [
        (r".*", [
            "Nu ma intereseaza numele. Va rog sa continuati.",
            "Nu am nevoie de numele dumneavoastra. Ce va preocupa?",
        ])
    ]),

    # --------------------------------------------------
    # SCUZE
    # --------------------------------------------------
    ("scuze", 0, [
        (r".*", [
            "Va rog sa nu va scuzati.",
            "Scuzele nu sunt necesare.",
            "Ce inseamna ca va cereti scuze?",
        ])
    ]),
    ("imi pare rau", 0, [
        (r".*", [
            "Va rog sa nu va scuzati.",
            "Scuzele nu sunt necesare.",
            "Ce sentimente va fac sa va cereti scuze?",
        ])
    ]),

    # --------------------------------------------------
    # NU POT
    # --------------------------------------------------
    ("nu pot", 0, [
        (r"nu pot (.*)", [
            "Cum de nu puteti sa {}?",
            "Ati incercat vreodata sa {}?",
            "De ce credeti ca nu puteti sa {}?",
            "Poate ca acum puteti sa {}.",
            "Ce v-ar ajuta sa {}?",
        ])
    ]),

    # --------------------------------------------------
    # NU VREAU
    # --------------------------------------------------
    ("nu vreau", 0, [
        (r"nu vreau (.*)", [
            "De ce nu vreti sa {}?",
            "Ati vrea cu adevarat sa {}?",
            "Cum s-ar schimba lucrurile daca ati vrea sa {}?",
        ])
    ]),

    # --------------------------------------------------
    # NU STIU
    # --------------------------------------------------
    ("nu stiu", 0, [
        (r".*", [
            "De ce nu stiti?",
            "Ce v-ar ajuta sa stiti?",
            "Cum va simtiti ca nu stiti?",
        ])
    ]),

    # --------------------------------------------------
    # IFI AMINTESC  (prioritate 5)
    # --------------------------------------------------
    ("imi amintesc", 5, [
        (r"imi amintesc (.*)", [
            "De ce va amintiti de {} acum?",
            "Va mai ganditi des la {}?",
            "Ce altceva va aduce aminte de {}?",
            "Ce inseamna pentru dumneavoastra amintirea despre {}?",
            "De ce a venit aceasta amintire acum?",
        ]),
        (r"nu imi amintesc (.*)", [
            "Cum va simtiti cand nu va amintiti de {}?",
            "De ce credeti ca nu va amintiti de {}?",
            "Va amintiti de altceva in loc de {}?",
        ]),
        (r".*", [
            "Ce alte amintiri va vin in minte?",
            "Povestiti-mi mai mult.",
        ])
    ]),

    # --------------------------------------------------
    # DACA  (prioritate 3)
    # --------------------------------------------------
    ("daca", 3, [
        (r"daca (.*)", [
            "Credeti ca e posibil ca {}?",
            "V-ati gandit ce s-ar intampla daca {}?",
            "Dar daca {}?",
            "Cat de probabil credeti ca este ca {}?",
        ])
    ]),

    # --------------------------------------------------
    # AM VISAT  (prioritate 4)
    # --------------------------------------------------
    ("am visat", 4, [
        (r"am visat (.*)", [
            "De ce credeti ca ati visat {}?",
            "Ati mai visat despre {} inainte?",
            "Ce sentimente v-a trezit visul despre {}?",
            "Cine apare in visele despre {}?",
            "Ce credeti ca inseamna sa visezi {}?",
        ]),
        (r".*", [
            "Ce credeti ca inseamna visele dumneavoastra?",
            "Ati mai visat asa ceva inainte?",
        ])
    ]),
    ("visez", 4, [
        (r"visez (.*)", [
            "De ce credeti ca visati {}?",
            "Ce semnificatie credeti ca are faptul ca visati {}?",
            "Ati mai visat despre {} inainte?",
            "Cine altcineva apare in visele despre {}?",
        ])
    ]),
    ("vis", 3, [
        (r".*", [
            "Ce inseamna pentru dumneavoastra visele?",
            "Ati mai visat ceva asemanator?",
            "Ce sentimente va trezesc visele?",
            "Va ganditi des la vise?",
        ])
    ]),

    # --------------------------------------------------
    # POATE / PROBABIL
    # --------------------------------------------------
    ("poate", 0, [
        (r"poate (.*)", [
            "Sunteti sigur ca {}?",
            "De ce nu sunteti sigur ca {}?",
            "Nu puteti sti cu certitudine daca {}?",
        ]),
        (r".*", [
            "Sunteti sigur?",
            "De ce ezitati?",
        ])
    ]),
    ("probabil", 0, [
        (r"probabil (.*)", [
            "De ce nu sunteti sigur ca {}?",
            "Cat de probabil credeti ca e {}?",
        ])
    ]),

    # --------------------------------------------------
    # MEREU / INTOTDEAUNA / NICIODATA  (prioritate 1)
    # --------------------------------------------------
    ("mereu", 1, [
        (r"(.*) mereu (.*)", [
            "Puteti da un exemplu concret?",
            "Cand s-a intamplat asta prima oara?",
            "De ce credeti ca e mereu asa?",
            "Chiar mereu?",
        ]),
        (r".*", [
            "Puteti da un exemplu concret?",
            "Chiar mereu?",
        ])
    ]),
    ("intotdeauna", 1, [
        (r"(.*)", [
            "Puteti da un exemplu concret?",
            "Chiar intotdeauna?",
            "De ce credeti ca e intotdeauna asa?",
        ])
    ]),
    ("niciodata", 1, [
        (r"(.*)", [
            "De ce niciodata?",
            "Sigur niciodata?",
            "Puteti da un exemplu cand s-a intamplat totusi?",
            "Nu chiar niciodata?",
        ])
    ]),

    # --------------------------------------------------
    # LA FEL / ASEMANATOR  (prioritate 10)
    # --------------------------------------------------
    ("la fel", 10, [
        (r"(.*)", [
            "In ce fel?",
            "Ce asemanare vedeti?",
            "Ce va face sa credeti ca sunt la fel?",
        ])
    ]),
    ("asemanator", 10, [
        (r"(.*)", [
            "In ce fel?",
            "Ce asemanare vedeti?",
        ])
    ]),
    ("identic", 10, [
        (r"(.*)", [
            "In ce fel?",
            "Ce asemanare vedeti exact?",
        ])
    ]),

    # --------------------------------------------------
    # DIFERIT
    # --------------------------------------------------
    ("diferit", 0, [
        (r"(.*)", [
            "Cum este diferit?",
            "Ce diferenta vedeti?",
            "De ce e important pentru dumneavoastra ca e diferit?",
        ])
    ]),

    # --------------------------------------------------
    # SUNT (eu sunt...)
    # --------------------------------------------------
    ("sunt", 0, [
        (r"sunt (.*)", [
            "De cat timp esti {}?",
            "De ce crezi ca esti {}?",
            "Ce inseamna pentru tine sa fii {}?",
            "Cum te simti ca esti {}?",
            "Iti place sa fii {}?",
        ]),
        (r".*", [
            "Va rog sa continuati.",
        ])
    ]),

    # --------------------------------------------------
    # ESTI (tu esti... / esti tu...)
    # --------------------------------------------------
    ("esti", 0, [
        (r"esti (.*)", [
            "De ce crezi ca eu sunt {}?",
            "Iti place sa crezi ca eu sunt {}?",
            "Ti-ar placea ca eu sa fiu {}?",
            "Ce ti-ar schimba daca as fi {}?",
        ]),
        (r".*", [
            "De ce credeti asta despre mine?",
        ])
    ]),

    # --------------------------------------------------
    # AL MEU / A MEA
    # --------------------------------------------------
    ("al meu", 0, [
        (r"(.*) al meu (.*)", [
            "Povestiti-mi mai mult despre {} al dumneavoastra.",
            "De ce imi spuneti despre {} al dumneavoastra?",
        ]),
        (r".*", [
            "Povestiti-mi mai mult.",
        ])
    ]),
    ("a mea", 0, [
        (r"(.*) a mea (.*)", [
            "Povestiti-mi mai mult despre {} a dumneavoastra.",
            "De ce imi spuneti despre {} a dumneavoastra?",
        ])
    ]),

    # --------------------------------------------------
    # EU
    # --------------------------------------------------
    ("eu", 0, [
        (r"eu (.*)", [
            "De ce spuneti ca dumneavoastra {}?",
            "Va indoiti ca dumneavoastra {}?",
            "Dar daca n-ati {}?",
            "De cat timp {}?",
            "Ce simtiti ca spuneti ca {}?",
        ]),
        (r".*", [
            "Va rog sa continuati.",
        ])
    ]),

    # --------------------------------------------------
    # TU
    # --------------------------------------------------
    ("tu", 0, [
        (r"tu (.*)", [
            "De ce credeti ca eu {}?",
            "Va imaginati ca eu {}?",
            "Ce v-a facut sa credeti ca eu {}?",
            "Va ganditi des ca eu {}?",
        ]),
        (r".*", [
            "Va ganditi des la mine?",
            "De ce ma mentionati?",
        ])
    ]),

    # --------------------------------------------------
    # DA
    # --------------------------------------------------
    ("da", 0, [
        (r".*", [
            "Sunteti sigur?",
            "Ah, inteleg.",
            "Puteti dezvolta?",
            "Va rog sa continuati.",
            "Inteleg. Si?",
        ])
    ]),

    # --------------------------------------------------
    # NU (singur ca raspuns)
    # --------------------------------------------------
    ("nu", 0, [
        (r"^nu[.!]?$", [
            "Nu sunteti convins?",
            "De ce nu?",
            "De ce raspundeti negativ?",
        ]),
        (r"nu (.*)", [
            "De ce nu {}?",
            "Sunteti sigur ca nu {}?",
        ])
    ]),

    # --------------------------------------------------
    # POT
    # --------------------------------------------------
    ("pot", 0, [
        (r"pot (.*)", [
            "Credeti ca puteti cu adevarat sa {}?",
            "Daca ati putea sa {}, ce s-ar schimba?",
            "De ce vreti sa {}?",
        ])
    ]),

    # --------------------------------------------------
    # SIMT  (prioritate 5)
    # --------------------------------------------------
    ("simt", 5, [
        (r"ma simt (.*)", [
            "De cand va simtiti {}?",
            "Ce va face sa va simtiti {}?",
            "Va mai simtiti adesea {}?",
            "Ce ati simtit inainte sa va simtiti {}?",
        ]),
        (r"simt (.*)", [
            "De ce va simtiti {}?",
            "De cand va simtiti {}?",
            "Ce va face sa va simtiti {}?",
        ]),
        (r".*", [
            "Povestiti-mi mai mult despre sentimentele dumneavoastra.",
        ])
    ]),

    # --------------------------------------------------
    # GANDESC / CRED  (prioritate 5)
    # --------------------------------------------------
    ("gandesc", 5, [
        (r"ma gandesc (.*)", [
            "De ce va ganditi la {}?",
            "Ati mai avut acest gand inainte?",
            "Ce altceva va vine in minte cand va ganditi la {}?",
        ]),
        (r"cred ca (.*)", [
            "Aveti dovezi ca {}?",
            "Ce v-a convins ca {}?",
            "Dar daca ar fi altfel?",
        ]),
        (r".*", [
            "Povestiti-mi mai mult.",
        ])
    ]),
    ("cred", 5, [
        (r"cred ca (.*)", [
            "Aveti dovezi ca {}?",
            "Ce v-a convins ca {}?",
            "De ce credeti ca {}?",
            "Dar daca nu ar fi {}?",
        ]),
        (r"nu cred (.*)", [
            "De ce nu credeti?",
            "Ce v-ar convinge?",
        ]),
        (r".*", [
            "De ce spuneti asta?",
            "Va rog sa dezvoltati.",
        ])
    ]),

    # --------------------------------------------------
    # MUNCA / LUCRU  (prioritate 4)
    # --------------------------------------------------
    ("munca", 4, [
        (r"(.*)", [
            "Va place munca dumneavoastra?",
            "Cum va face sa va simtiti munca?",
            "Ce altceva legat de munca vreti sa-mi spuneti?",
            "Povestiti-mi mai mult despre munca.",
        ])
    ]),
    ("lucru", 4, [
        (r"lucrez (.*)", [
            "Ce va face sa lucrezi {}?",
            "De cat timp lucrezi {}?",
        ]),
        (r"(.*)", [
            "Ce fel de lucru faceti?",
            "Va place ce faceti?",
        ])
    ]),
    ("serviciu", 4, [
        (r"(.*)", [
            "Va place serviciul dumneavoastra?",
            "Cum va simtiti la serviciu?",
            "Povestiti-mi mai mult despre serviciu.",
        ])
    ]),

    # --------------------------------------------------
    # FAMILIA  (prioritati 8-10)
    # --------------------------------------------------
    ("mama", 10, [
        (r"(.*) mama (.*)", [
            "Povestiti-mi mai mult despre mama dumneavoastra.",
            "Cum va intelegeati cu mama?",
            "Ce va amintiti despre mama din copilarie?",
            "Cum va simtiti fata de mama?",
            "Cine altcineva din familie va vine in minte?",
        ]),
        (r"(.*)", [
            "Povestiti-mi mai mult despre mama dumneavoastra.",
            "Cum va simtiti fata de mama?",
            "Ce va amintiti despre mama?",
        ])
    ]),
    ("tata", 10, [
        (r"(.*) tata (.*)", [
            "Povestiti-mi mai mult despre tatal dumneavoastra.",
            "Cum va intelegeati cu tatal?",
            "Ce va amintiti despre tatal din copilarie?",
            "Cum va simtiti fata de tatal?",
            "Cine altcineva din familie va vine in minte?",
        ]),
        (r"(.*)", [
            "Povestiti-mi mai mult despre tatal dumneavoastra.",
            "Cum va simtiti fata de tatal?",
        ])
    ]),
    ("parinti", 10, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre parintii dumneavoastra.",
            "Cum va intelegeati cu parintii?",
            "Ce va amintiti despre parinti din copilarie?",
            "Cine altcineva din familie va vine in minte?",
        ])
    ]),
    ("sora", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre sora dumneavoastra.",
            "Cum va intelegeati cu sora?",
            "Cine altcineva din familie va vine in minte?",
        ])
    ]),
    ("frate", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre fratele dumneavoastra.",
            "Cum va intelegeati cu fratele?",
            "Cine altcineva din familie va vine in minte?",
        ])
    ]),
    ("sotia", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre sotia dumneavoastra.",
            "Cum va intelegeati cu sotia?",
            "Ce va face sa va ganditi la sotia?",
        ])
    ]),
    ("sotul", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre sotul dumneavoastra.",
            "Cum va intelegeati cu sotul?",
        ])
    ]),
    ("copii", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre copiii dumneavoastra.",
            "Cum va simtiti fata de copii?",
            "Ce va aduce aminte de copii acum?",
        ])
    ]),
    ("copilul", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre copilul dumneavoastra.",
            "Cum va simtiti fata de copil?",
        ])
    ]),
    ("familia", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre familia dumneavoastra.",
            "Cine altcineva din familie va vine in minte?",
            "Cum va simtiti fata de familia dumneavoastra?",
            "Ce rol joaca familia in viata dumneavoastra?",
        ])
    ]),
    ("bunica", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre bunica dumneavoastra.",
            "Ce va amintiti despre bunica?",
        ])
    ]),
    ("bunicul", 8, [
        (r"(.*)", [
            "Povestiti-mi mai mult despre bunicul dumneavoastra.",
            "Ce va amintiti despre bunicul?",
        ])
    ]),

    # --------------------------------------------------
    # TOATA LUMEA / TOTI / NIMENI  (prioritate 2)
    # --------------------------------------------------
    ("toata lumea", 2, [
        (r"(.*)", [
            "Chiar toata lumea?",
            "Puteti da un exemplu concret?",
            "La cine exact va ganditi?",
        ])
    ]),
    ("toti", 2, [
        (r"(.*)", [
            "Chiar toti?",
            "Puteti da un exemplu concret?",
            "La cine va ganditi exact?",
        ])
    ]),
    ("nimeni", 2, [
        (r"(.*)", [
            "Sigur nimeni?",
            "Nimeni niciodata?",
            "La cine va ganditi exact?",
            "Chiar nimeni?",
        ])
    ]),
    ("nimic", 2, [
        (r"(.*)", [
            "Sigur nimic?",
            "Ce va face sa credeti ca e nimic?",
        ])
    ]),

    # --------------------------------------------------
    # DE CE
    # --------------------------------------------------
    ("de ce", 0, [
        (r"de ce (.*)", [
            "De ce credeti ca {}?",
            "Ce v-a facut sa intrebati asta?",
            "Aveti dumneavoastra un raspuns la asta?",
            "De ce e important pentru dumneavoastra sa stiti {}?",
        ])
    ]),

    # --------------------------------------------------
    # CUM
    # --------------------------------------------------
    ("cum", 0, [
        (r"cum (.*)", [
            "De ce va intrebati cum {}?",
            "Ce va face sa va ganditi la cum {}?",
            "Puteti descrie mai bine?",
        ])
    ]),

    # --------------------------------------------------
    # CAND
    # --------------------------------------------------
    ("cand", 0, [
        (r"cand (.*)", [
            "De ce va intereseaza cand {}?",
            "Ce va face sa va ganditi la momentul cand {}?",
        ])
    ]),

    # --------------------------------------------------
    # UNDE
    # --------------------------------------------------
    ("unde", 0, [
        (r"unde (.*)", [
            "De ce va intereseaza unde {}?",
            "Ce va face sa va ganditi la asta?",
        ])
    ]),

    # --------------------------------------------------
    # STARI EMOTIONALE
    # --------------------------------------------------
    ("fericit", 0, [
        (r"(.*) fericit (.*)", [
            "Ce va face fericit?",
            "De cand va simtiti fericit?",
            "De ce va simtiti fericit?",
        ]),
        (r"(.*)", [
            "Ce va face fericit?",
            "Va simtiti cu adevarat fericit?",
            "De cand va simtiti fericit?",
        ])
    ]),
    ("bucuros", 0, [
        (r"(.*)", [
            "Ce va face bucuros?",
            "De cand va simtiti bucuros?",
            "Ce v-a adus aceasta bucurie?",
        ])
    ]),
    ("trist", 0, [
        (r"(.*) trist (.*)", [
            "De ce va simtiti trist?",
            "De cand va simtiti trist?",
            "Imi pare rau sa aud ca esti trist.",
            "Ce v-a facut sa va simtiti trist?",
        ]),
        (r"(.*)", [
            "De ce va simtiti trist?",
            "De cand va simtiti trist?",
            "Imi pare rau sa aud asta.",
        ])
    ]),
    ("deprimat", 0, [
        (r"(.*)", [
            "De cand va simtiti deprimat?",
            "Imi pare rau sa aud ca esti deprimat.",
            "Ce v-a facut sa va simtiti deprimat?",
            "Ati vorbit cu cineva despre asta?",
        ])
    ]),
    ("nefericit", 0, [
        (r"(.*)", [
            "De ce va simtiti nefericit?",
            "De cat timp va simtiti nefericit?",
            "Ce v-ar face sa va simtiti mai bine?",
            "Credeti ca venirea aici va ajuta sa nu mai fiti nefericit?",
        ])
    ]),
    ("ingrijorat", 0, [
        (r"(.*)", [
            "De ce sunteti ingrijorat?",
            "De cat timp sunteti ingrijorat?",
            "Ce v-a facut sa va ingrijorati?",
        ])
    ]),
    ("anxios", 0, [
        (r"(.*)", [
            "De ce sunteti anxios?",
            "De cat timp va simtiti anxios?",
            "Ce va face sa va simtiti anxios?",
        ])
    ]),
    ("speriat", 0, [
        (r"(.*)", [
            "De ce va este frica?",
            "De ce sunteti speriat?",
            "Ce va sperie?",
            "De cand va este frica?",
        ])
    ]),
    ("furios", 0, [
        (r"(.*)", [
            "De ce sunteti furios?",
            "Ce v-a facut sa fiti furios?",
            "Cum va manifestati furia?",
        ])
    ]),
    ("suparat", 0, [
        (r"(.*)", [
            "De ce sunteti suparat?",
            "Ce v-a suparat?",
            "De cand sunteti suparat?",
        ])
    ]),
    ("singuratic", 0, [
        (r"(.*)", [
            "De ce va simtiti singuratic?",
            "De cat timp va simtiti singuratic?",
            "Aveti pe cineva cu care sa vorbiti?",
        ])
    ]),

    # --------------------------------------------------
    # SINGUR
    # --------------------------------------------------
    ("singur", 5, [
        (r"(.*)", [
            "De ce va simtiti singur?",
            "De cat timp va simtiti singur?",
            "Ce v-ar ajuta sa nu va mai simtiti singur?",
            "Aveti pe cineva cu care sa vorbiti?",
        ])
    ]),

    # --------------------------------------------------
    # IUBIRE / URA
    # --------------------------------------------------
    ("iubesc", 0, [
        (r"iubesc (.*)", [
            "Ce va face sa iubiti {}?",
            "De cat timp iubiti {}?",
            "Ce inseamna pentru dumneavoastra sa iubiti {}?",
        ]),
        (r"(.*)", [
            "Ce va face sa simtiti iubire?",
            "Povestiti-mi mai mult.",
        ])
    ]),
    ("iubire", 0, [
        (r"(.*)", [
            "Ce inseamna iubirea pentru dumneavoastra?",
            "Povestiti-mi mai mult despre iubire.",
        ])
    ]),
    ("urasc", 0, [
        (r"urasc (.*)", [
            "De ce urati {}?",
            "De cat timp urati {}?",
            "Ce v-a facut sa urati {}?",
        ]),
        (r"(.*)", [
            "De ce simtiti ura?",
            "Ce v-a facut sa simtiti ura?",
        ])
    ]),

    # --------------------------------------------------
    # PENTRU CA
    # --------------------------------------------------
    ("pentru ca", 0, [
        (r"(.*) pentru ca (.*)", [
            "Aceasta este adevarata cauza?",
            "Ce alte motive ar mai fi?",
            "De ce credeti ca acesta e motivul?",
        ])
    ]),

    # --------------------------------------------------
    # PRIETENI
    # --------------------------------------------------
    ("prieten", 5, [
        (r"prietenul meu (.*)", [
            "Povestiti-mi mai mult despre prietenul dumneavoastra.",
            "Cum va intelegeati cu prietenul?",
        ]),
        (r"(.*) prieten (.*)", [
            "Povestiti-mi mai mult despre prietenul dumneavoastra.",
            "Ce inseamna pentru dumneavoastra prietenia?",
        ]),
        (r"(.*)", [
            "Povestiti-mi mai mult despre prietenii dumneavoastra.",
            "Ce inseamna pentru dumneavoastra prietenia?",
        ])
    ]),

    # --------------------------------------------------
    # SANATATE
    # --------------------------------------------------
    ("bolnav", 5, [
        (r"(.*)", [
            "De cat timp va simtiti bolnav?",
            "Ati consultat un medic?",
            "Ce simptome aveti?",
        ])
    ]),
    ("doare", 5, [
        (r"ma doare (.*)", [
            "De cat timp va doare {}?",
            "Ati consultat un medic pentru {}?",
        ]),
        (r"(.*)", [
            "De ce va doare?",
            "De cat timp aveti aceasta durere?",
        ])
    ]),

    # --------------------------------------------------
    # PROBLEME  (prioritate 3)
    # --------------------------------------------------
    ("problema", 3, [
        (r"(.*) problema (.*)", [
            "Ce fel de problema?",
            "De cat timp aveti aceasta problema?",
            "Ce credeti ca a cauzat aceasta problema?",
            "Povestiti-mi mai mult despre aceasta problema.",
        ]),
        (r"(.*)", [
            "Povestiti-mi mai mult despre problema.",
            "De cat timp aveti aceasta problema?",
            "Ce credeti ca a cauzat problema?",
        ])
    ]),

    # --------------------------------------------------
    # AJUTOR
    # --------------------------------------------------
    ("ajutor", 3, [
        (r"am nevoie de ajutor (.*)", [
            "Ce fel de ajutor doriti?",
            "Ce v-ar ajuta cel mai mult?",
            "De ce aveti nevoie de ajutor {}?",
        ]),
        (r"(.*)", [
            "Ce fel de ajutor doriti?",
            "Ce v-ar ajuta cel mai mult?",
            "Ce inseamna pentru dumneavoastra sa primiti ajutor?",
        ])
    ]),

    # --------------------------------------------------
    # MOARTE / SFARSIT
    # --------------------------------------------------
    ("moarte", 5, [
        (r"(.*)", [
            "De ce va ganditi la moarte?",
            "Va ganditi des la moarte?",
            "Ce va aduce aminte de moarte?",
        ])
    ]),
    ("mor", 5, [
        (r"vreau sa mor", [
            "Imi pare rau sa aud asta. Va rugati sa-mi spuneti mai mult.",
            "De ce va simtiti asa?",
            "De cat timp va simtiti asa?",
        ]),
        (r"(.*)", [
            "De ce va ganditi la moarte?",
            "Ce v-a facut sa mentionati asta?",
        ])
    ]),

    # --------------------------------------------------
    # SPERANCE / DORINTE
    # --------------------------------------------------
    ("sper", 0, [
        (r"sper (.*)", [
            "De ce sperati ca {}?",
            "Ce s-ar intampla daca {}?",
            "Cat de mult conteaza pentru dumneavoastra ca {}?",
        ])
    ]),
    ("doresc", 0, [
        (r"doresc (.*)", [
            "De ce doriti {}?",
            "Ce v-a facut sa doriti {}?",
            "Daca ati obtine {}, ce s-ar schimba?",
        ])
    ]),
    ("vreau", 0, [
        (r"vreau (.*)", [
            "De ce vreti {}?",
            "Ce v-a facut sa vreti {}?",
            "Daca ati obtine {}, ce s-ar schimba?",
            "Ce inseamna pentru dumneavoastra sa vreti {}?",
        ])
    ]),

    # --------------------------------------------------
    # TRECUT
    # --------------------------------------------------
    ("copilarie", 5, [
        (r"(.*)", [
            "Ce va amintiti din copilarie?",
            "Ce sentimente va trezeste copilaria?",
            "Cine era important pentru dumneavoastra in copilarie?",
        ])
    ]),
    ("trecut", 5, [
        (r"(.*)", [
            "Ce va amintiti din trecut?",
            "De ce va ganditi la trecut?",
            "Ce sentimente va trezeste trecutul?",
        ])
    ]),

    # --------------------------------------------------
    # LIMBI STRAINE (ca in original - redirect)
    # --------------------------------------------------
    ("english", 0, [
        (r".*", [
            "Va rog sa continuati in romana.",
        ])
    ]),
    ("franceza", 0, [
        (r".*", [
            "Va rog sa continuati in romana.",
        ])
    ]),
]


# =====================================================
# RASPUNSURI IMPLICITE (NONE)
# Folosite cand nu se gaseste niciun cuvant cheie.
# Ciclate in ordine, ca in original.
# =====================================================

NONE = [
    "Va rog sa continuati.",
    "Inteleg.",
    "Puteti dezvolta?",
    "Ce inseamna asta pentru dumneavoastra?",
    "Puteti fi mai specific?",
    "Va rog sa nu va opriti.",
    "Continuati, va ascult.",
    "Ce altceva va vine in minte?",
    "Sunt sigur ca nu este placut sa discutati despre asta.",
    "Nu inteleg pe deplin. Va rog sa continuati.",
    "Interesant. Povestiti-mi mai mult.",
    "Ce va face sa spuneti asta?",
]


# =====================================================
# TEMPLATE-URI MEMORIE
# Folosite cand memoria contine fraze anterioare
# si nu se gaseste niciun keyword curent.
# =====================================================

MEMORY_TEMPLATES = [
    "Hai sa revenim la ce ati mentionat mai devreme: {}. Povestiti-mi mai mult.",
    "Mai devreme ati vorbit despre {}. Ce vreti sa spuneti prin asta?",
    "Am observat ca ati mentionat {}. Ce va vine in minte acum?",
    "Sa revenim la {} - ce inseamna asta pentru dumneavoastra?",
]

# Cuvinte cheie care declanseaza stocarea in memorie
MEMORY_TRIGGER = [
    "mama", "tata", "familia", "sotia", "sotul",
    "copii", "copilul", "prieten", "sora", "frate",
    "parinti", "bunica", "bunicul",
]


# =====================================================
# MOTORUL ELIZA
# =====================================================

# Contoare ciclice per cheie - replica comportamentul
# pointer-ului din implementarea originala MAD-SLIP
contoare = {}


def get_ciclic(cheie, lista):
    """Returneaza elementul curent si avanseaza pointer-ul."""
    if cheie not in contoare:
        contoare[cheie] = 0
    idx = contoare[cheie] % len(lista)
    contoare[cheie] += 1
    return lista[idx]


def proceseaza(text, memorie):
    """
    Proceseaza un input si returneaza raspunsul ELIZA.
    Logica fidela originalului:
      1. Normalizeaza si pre-transforma inputul
      2. Cauta toate cuvintele cheie din input
      3. Sorteaza dupa prioritate (descrescator)
      4. Aplica prima regula care se potriveste la keyword-ul cu rang maxim
      5. Post-transforma textul capturat (pronume)
      6. Returneaza raspunsul ciclic
    """
    text_norm = normalizeaza(pre_transforma(text.lower().strip()))

    candidati = []

    for (cuv_cheie, prioritate, reguli) in SCRIPT:
        cuv_cheie_norm = normalizeaza(cuv_cheie.lower())

        if cuv_cheie_norm in text_norm:
            for i, (pattern, raspunsuri) in enumerate(reguli):
                pattern_norm = normalizeaza(pattern)
                match = re.search(pattern_norm, text_norm)
                if match:
                    candidati.append((prioritate, cuv_cheie, i, raspunsuri, match))
                    break  # prima regula potrivita per keyword

    if candidati:
        # Sorteaza dupa prioritate descrescator - keyword cu rang maxim castiga
        candidati.sort(key=lambda x: x[0], reverse=True)
        _, cuv_cheie, idx_regula, raspunsuri, match = candidati[0]

        cheie_ciclu = f"{cuv_cheie}_{idx_regula}"
        template = get_ciclic(cheie_ciclu, raspunsuri)

        # Inlocuieste {} cu textul capturat de grupul 1
        if "{}" in template and match.lastindex and match.lastindex >= 1:
            capturat = match.group(1).strip()
            capturat = post_transforma(capturat)
            raspuns = template.format(capturat)
        else:
            raspuns = template

        # Salveaza in memorie daca textul contine un keyword de memorie
        for mk in MEMORY_TRIGGER:
            if normalizeaza(mk) in text_norm:
                memorie.append(text)
                break

        return raspuns

    # Niciun keyword gasit - incearca memoria sau NONE
    if memorie:
        vechi = memorie.pop(0)
        template = get_ciclic("memory", MEMORY_TEMPLATES)
        return template.format(f'"{vechi}"')

    return get_ciclic("none", NONE)


# =====================================================
# BUCLA PRINCIPALA
# Output cu MAJUSCULE, indentare ca la teletype -
# exact ca in sesiunile originale de pe IBM 7094
# =====================================================

def ruleaza():
    memorie = []

    print()
    print("BUNA ZIUA. VA ROG SA-MI SPUNETI PROBLEMA DUMNEAVOASTRA.")
    print()

    while True:
        try:
            text = input("        ")
        except (EOFError, KeyboardInterrupt):
            print()
            print("LA REVEDERE.")
            print()
            break

        text = text.strip()

        if not text:
            continue

        if normalizeaza(text.lower()) in [
            "la revedere", "pa", "exit", "quit",
            "sfarsit", "gata", "adio", "opreste"
        ]:
            print()
            print("LA REVEDERE. A FOST O DISCUTIE INTERESANTA.")
            print()
            break

        raspuns = proceseaza(text, memorie)
        print()
        print(raspuns.upper())
        print()


if __name__ == "__main__":
    ruleaza()


    # structura
#     1. Transformare pronume "eu" → "tu", "mă" → "te", etc.
#  2.Scriptul cu reguli cuvinte cheie + priorități + răspunsuri multiple
#  3.Funcția de descompunere despică propoziția userului în bucăți
# 4.Funcția de reasamblare construiește răspunsul din bucăți
# 5.Memoria stochează propoziții anterioare pentru fallback
# 6. Bucla principală citește input → procesează → printează răspuns