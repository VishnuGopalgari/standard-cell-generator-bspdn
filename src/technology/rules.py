"""GT3 design rules. All values in nm."""

# (rule, layer) -> value
RULES = {
    # FEOL / MOL
    ("width",   "GATE"):  15,
    ("pitch",   "GATE"):  42,     # CPP
    ("width",   "GCUT"):  10,
    ("spacing", "OD"):    30,     # NMOS to PMOS
    ("spacing", "GATE-SDCON"): 6,
    ("tiptip",  "SDCON"): 20,
    ("width",   "BPR"):   32,
    ("width",   "VBPR"):  15,
    ("width",   "VSD"):   13,
    ("width",   "VG"):    15,

    # M0  (M2 uses the same numbers)
    ("width",   "M0"):    12,
    ("spacing", "M0"):    12,
    ("tiptip",  "M0"):    17,
    ("corner",  "M0"):    15,
    ("encl",    "M0"):    4,      # M0 over VSD / VG

    # M1 and M3
    ("width",   "M1"):    14,
    ("spacing", "M1"):    14,
    ("tiptip",  "M1"):    20,
    ("corner",  "M1"):    16,
    ("encl",    "M1"):    4,

    # M4 and M5
    ("width",   "M4"):    21,
    ("spacing", "M4"):    21,
    ("tiptip",  "M4"):    30,
    ("corner",  "M4"):    24,
    ("encl",    "M4"):    5,
}

# layers that copy another layer's rules
SAME_AS = {"M2": "M0", "M3": "M1", "M5": "M4"}


def get(rule, layer):
    """Rule value, or None. Follows SAME_AS."""
    layer = SAME_AS.get(layer, layer)
    return RULES.get((rule, layer))


def check(rule, layer, actual):
    """Return an error string if actual breaks the rule, else None."""
    limit = get(rule, layer)
    if limit is None or actual >= limit:
        return None
    return f"{layer} {rule}: {actual} nm < {limit} nm needed"


def show(layer=None):
    """Print the rules, optionally one layer only."""
    for (rule, name), value in RULES.items():
        if layer and name != SAME_AS.get(layer, layer):
            continue
        print(f"  {name:<12}{rule:<9}{value:>4} nm")
    for alias, target in SAME_AS.items():
        if layer in (None, alias):
            print(f"  {alias:<12}same rules as {target}")
