"""Add gasp + smart-dropout prep (unhinted font) — same as gftools fix-nonhinting."""
import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import ttProgram
for path in sys.argv[1:]:
    f = TTFont(path)
    gasp = newTable("gasp"); gasp.version = 1; gasp.gaspRange = {0xFFFF: 0x000F}; f["gasp"] = gasp
    prep = newTable("prep"); prep.program = ttProgram.Program()
    prep.program.fromAssembly(["PUSHW[]", "511", "SCANCTRL[]", "PUSHB[]", "4", "SCANTYPE[]"]); f["prep"] = prep
    if "maxp" in f:
        m = f["maxp"]; m.maxStackElements = max(getattr(m, "maxStackElements", 0), 2)
    f.save(path)
