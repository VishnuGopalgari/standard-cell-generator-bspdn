"""GT3 cell architecture and sizing.

Values from Shim et al., GT3, IEEE TED 72(4), 2025. Sizes in nm.
"""

from technology import layers
from technology import rules

# --- cell architecture (Section III) ---
HEIGHT       = 144    # cell height
HEIGHT_2X    = 288    # for complex cells
CPP          = 42     # contacted poly pitch = width of one column
GATE_LENGTH  = 15
PN_SPACING   = 30     # NMOS to PMOS
DIFF_HEIGHT  = 72     # N/P diffusion region
TRACKS       = 6      # M0 track positions
SIGNAL_TRACKS = 5     # usable; the y=0 track is shared with the cell below

# --- device (Section III-A) ---
NANOSHEETS   = 3      # sheets stacked per transistor
NS_THICKNESS = 5
NS_SPACING   = 10
NS_WIDTH     = 21

# --- devices, Table I: (work function eV, Vt mV, SS mV/dec, Ion uA) ---
DEVICES = {
    "nmos_rvt": (4.45,  229, 65.1, 128),
    "pmos_rvt": (4.84, -232, 65.6, 63.4),
    "nmos_lvt": (4.38,  159, 65.9, 167),
    "pmos_lvt": (4.92, -152, 66.9, 78.5),
}

# --- interconnect, Table III: (bulk resistivity uOhm-cm, size-effect nm) ---
MATERIALS = {"Cu": (1.72, 5.7), "Ru": (6.06, 3.28)}


def cell_width(columns):
    """Cell width in nm for a given number of poly columns."""
    return columns * CPP


def cell_area(columns, double_height=False):
    return cell_width(columns) * (HEIGHT_2X if double_height else HEIGHT)


def track_positions():
    """Y position of each M0 track, bottom-up."""
    return [i * layers.pitch("M0") for i in range(TRACKS)]


def usable_tracks():
    """Tracks free for signal. The y=0 track is dropped: it is shared with
    the cell below, and once cells abut, shapes from the two neighbours can
    land diagonally adjacent and break the M0 corner rule."""
    return track_positions()[1:]


def fins(transistor):
    """Finger count. GT3 puts drive strength in M, so M=12 is 12 columns."""
    return max(1, transistor.multiplicity or 1)


def transistor_width(transistor):
    """Total effective width = sheets x sheet width x fingers."""
    w = (transistor.wgaa * 1000) if transistor.wgaa else NS_WIDTH
    return w * NANOSHEETS * fins(transistor)


def columns_needed(cell):
    """Lower bound on poly columns: the wider of the two rows."""
    p = sum(fins(t) for t in cell.transistors.values() if t.type == "PMOS")
    n = sum(fins(t) for t in cell.transistors.values() if t.type == "NMOS")
    return max(p, n), p, n


def show():
    """Print the architecture summary."""
    print(f"  GT3 6-track, 3 nm GAAFET, buried power rail")
    print(f"  cell height    {HEIGHT} nm  ({HEIGHT_2X} nm for complex cells)")
    print(f"  CPP            {CPP} nm")
    print(f"  gate length    {GATE_LENGTH} nm")
    print(f"  P/N spacing    {PN_SPACING} nm")
    print(f"  device         {NANOSHEETS} nanosheets, {NS_THICKNESS} nm "
          f"thick, {NS_WIDTH} nm wide")
    print(f"  M0 tracks      {TRACKS} total, {SIGNAL_TRACKS} for signal")
    print(f"  track y        {track_positions()}")
    print(f"  in-cell layers {', '.join(layers.INCELL_LAYERS)}")


def show_cell(cell):
    """Print the physical size of a parsed cell."""
    columns, p, n = columns_needed(cell)
    print(f"  PMOS fingers   {p}")
    print(f"  NMOS fingers   {n}")
    print(f"  poly columns   {columns}   (lower bound, no dummy poly yet)")
    print(f"  cell width     {cell_width(columns)} nm")
    print(f"  cell height    {HEIGHT} nm")
    print(f"  cell area      {cell_area(columns)} nm2")
