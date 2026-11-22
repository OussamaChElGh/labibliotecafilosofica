"""Retoques de las obras de teatro de la tanda 10, después de teatro_verso.py (se ejecuta desde repo/)."""
import json
import re

PLAYS = ["la-vida-es-sueno-calderon", "el-burlador-de-sevilla-tirso-de-molina", "don-juan-tenorio-zorrilla",
         "la-casa-de-bernarda-alba-lorca", "fuenteovejuna-lope-de-vega", "bodas-de-sangre-lorca"]
RENAME = {"el-burlador-de-sevilla-tirso-de-molina": {"Tenorio": "Don Diego Tenorio"},
          "don-juan-tenorio-zorrilla": {"Torn": "Tornera", "Gast": "Gastón", "ALGUACIL 1º": "Alguacil 1.º",
                                        "ALGUACIL 2º": "Alguacil 2.º", "Inés": "Doña Inés", "Ana": "Doña Ana"}}
TENORIO = ["Parte primera, acto I", "Parte primera, acto II", "Parte primera, acto III", "Parte primera, acto IV",
           "Parte segunda, acto I", "Parte segunda, acto II", "Parte segunda, acto III"]
TENORIO_SUB = ["Libertinaje y escándalo", "Destreza", "Profanación", "El diablo a las puertas del cielo",
               "La sombra de doña Inés", "La estatua de don Gonzalo", "Misericordia de Dios y apoteosis del amor"]


def caps_ratio(text):
    letters = [c for c in text if c.isalpha()]
    return sum(c.isupper() for c in letters) / max(1, len(letters))


for slug in PLAYS:
    meta = json.load(open(f"textos/{slug}.json", encoding="utf-8"))
    blocks = open(f"textos/{slug}.txt", encoding="utf-8").read().split("\n")
    speakers = {int(k): v for k, v in meta["speakers"].items()}
    starts = {c["start"] for c in meta["chapters"]}
    drop = set()
    if slug == "don-juan-tenorio-zorrilla":
        first = next(i for i, b in enumerate(blocks) if b == "S|Escena primera")
        cast = next(i for i in range(first) if blocks[i].startswith("S|Don JUAN"))
        for i in range(1, first):
            if i not in (cast, first - 1):
                drop.add(i)
        blocks[cast] = "S|Personajes: " + blocks[cast][2:]
        speakers.pop(first - 1, None)
    for i, b in enumerate(blocks):
        kind, text = b[:2], b[2:]
        if i in starts or i in drop:
            continue
        if text in ("Índice",) or re.fullmatch(r"(JORNADA|ACTO)\s+\w+\.?", text):
            drop.add(i)
            continue
        if re.fullmatch(r"ESCENA\s+[\wÁÉÍÓÚ]+\.?", text):
            blocks[i] = "S|Escena " + text.split(None, 1)[1].lower().rstrip(".")
            continue
        text = re.sub(r"\s*\(\s*$", "", text).replace("Clarin", "Clarín") if kind == "S|" else text
        if kind in ("P|", "V|") and i not in speakers:
            whole = re.fullmatch(r"\(([^()]*)\)\s*\.?", text)
            if whole:
                blocks[i] = "S|(" + whole.group(1).strip() + ")"
                continue
            if len(text) < 160 and caps_ratio(text) > 0.6 and text.rstrip()[-1:] in ",.;":
                blocks[i] = "S|" + text  # quienes están en escena: «DON LUIS MEJÍA,»
                continue
            if slug == "la-casa-de-bernarda-alba-lorca" and kind == "V|" and len(text) > 80:
                blocks[i] = "S|(" + text + ")"
                continue
        blocks[i] = blocks[i][:2] + text if blocks[i][:2] == kind else blocks[i]
    # Rehacer índices sin los bloques eliminados.
    new_index, out = {}, []
    for i, b in enumerate(blocks):
        if i in drop:
            continue
        new_index[i] = len(out)
        out.append(b)
    for c in meta["chapters"]:
        c["start"] = new_index[c["start"]]
        end = c["end"]
        while end not in new_index:
            end -= 1
        c["end"] = new_index[end]
    ren = RENAME.get(slug, {})
    meta["speakers"] = {str(new_index[k]): ren.get(v, v) for k, v in sorted(speakers.items()) if k in new_index}
    if slug == "don-juan-tenorio-zorrilla":
        for n, c in enumerate(meta["chapters"]):
            c["title"] = f"{TENORIO[n]}: {TENORIO_SUB[n]}"
            c["slug"] = ("primera" if n < 4 else "segunda") + f"-parte-acto-{(n if n < 4 else n - 4) + 1}"
            out[c["start"]] = "H|" + c["title"]
    open(f"textos/{slug}.txt", "w", encoding="utf-8").write("\n".join(out))
    open(f"textos/{slug}.json", "w", encoding="utf-8").write(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    print(slug, len(out), [c["title"] for c in meta["chapters"]])
