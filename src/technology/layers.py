"""GT3 physical layers. All sizes in nm."""

# name: (tier, purpose, width, pitch, direction, material)
LAYERS = {
    # FEOL - the devices
    "NS":    ("FEOL",  "diffusion", 21,  None, "horizontal", "Si"),
    "OD":    ("FEOL",  "diffusion", 72,  None, "horizontal", "Si"),
    "GATE":  ("FEOL",  "gate",      15,  42,   "vertical",   "metal"),
    "GCUT":  ("FEOL",  "cut",       10,  None, None,         None),

    # MOL - contacts up to metal
    "SDCON": ("MOL",   "contact",   None, None, "vertical",  "W"),
    "VSD":   ("MOL",   "via",       13,  None, None,         "W"),
    "VG":    ("MOL",   "via",       15,  None, None,         "W"),

    # BSPDN - buried power
    "BPR":   ("BSPDN", "power",     32,  None, "horizontal", "Ru"),
    "VBPR":  ("BSPDN", "via",       15,  None, None,         "Ru"),

    # BEOL - routing (M0-M3 ruthenium, M4 up copper)
    "M0":    ("BEOL",  "routing",   12,  24,   "horizontal", "Ru"),
    "V0":    ("BEOL",  "via",       12,  24,   None,         "Ru"),
    "M1":    ("BEOL",  "routing",   14,  28,   "vertical",   "Ru"),
    "V1":    ("BEOL",  "via",       14,  28,   None,         "Ru"),
    "M2":    ("BEOL",  "routing",   12,  24,   "horizontal", "Ru"),
    "V2":    ("BEOL",  "via",       12,  24,   None,         "Ru"),
    "M3":    ("BEOL",  "routing",   14,  28,   "vertical",   "Ru"),
    "M4":    ("BEOL",  "routing",   21,  42,   "horizontal", "Cu"),
    "M5":    ("BEOL",  "routing",   21,  42,   "vertical",   "Cu"),
    "M6":    ("BEOL",  "routing",   38,  76,   "horizontal", "Cu"),
}

# ohms per micrometre for metal, ohms per cut for vias
RESISTANCE = {
    "M0": 622, "V0": 55, "M1": 438, "V1": 46,
    "M2": 622, "V2": 55, "M3": 438,
    "M4": 166, "M5": 166, "M6": 26,
}

# layers a cell generator may route on
INCELL_LAYERS = ["M0", "M1", "M2"]


def get(name):
    return LAYERS[name]


def width(name):
    return LAYERS[name][2]


def pitch(name):
    return LAYERS[name][3]


def direction(name):
    return LAYERS[name][4]


def by_tier(tier):
    return [n for n in LAYERS if LAYERS[n][0] == tier]


def show(tier=None):
    """Print the layers, optionally one tier only."""
    for name, (t, purpose, w, p, d, mat) in LAYERS.items():
        if tier and t != tier:
            continue
        line = f"  {name:<7}{t:<7}{purpose:<11}"
        if w:
            line += f"w={w:<5}"
        if p:
            line += f"pitch={p:<5}"
        if d:
            line += f"{d:<11}"
        if mat:
            line += mat
        if name in RESISTANCE:
            line += f"  R={RESISTANCE[name]}"
        print(line)
