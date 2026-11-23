"""Tanda 12 (ePub de Elejandría): limpia la promoción del ePub y rehace los capítulos con los encabezados reales.

python textos/fichas/fix_epub12.py   (después de epub.py; se ejecuta desde la raíz del repositorio)
Cada libro: qué líneas son grupo (parte, volumen, cántica) y cuáles capítulo. Lo que hay antes del primer capítulo
(portada, autor, «Libro descargado en…») se descarta; lo que hay después de «¡Gracias por leer…», también.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

TEXTS = Path("textos")
PROMO = re.compile(r"(?i)elejandr[ií]a|gracias por leer este libro|descubre nuestra colecci[oó]n|^\s*fin\.?\s*$")
ROMAN = r"[IVXLC]+"
ORD = {"primera": "Primera", "segunda": "Segunda", "tercera": "Tercera", "cuarta": "Cuarta", "quinta": "Quinta",
       "sexta": "Sexta"}


def cap(text):
    """«EN LA MADRIGUERA DEL CONEJO.» → «En la madriguera del conejo»."""
    text = text.strip().rstrip(".")
    if text.isupper():
        text = text.lower()
        text = text[:1].upper() + text[1:]
    return text


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:60].strip("-")


def reflow(blocks):
    """Texto de OCR con un renglón por línea: une los renglones de cada párrafo y quita números de página."""
    out = []
    for kind, text in blocks:
        if kind != "P":
            out.append((kind, text))
            continue
        if re.fullmatch(r"\d{1,4}", text.strip()):
            continue
        if out and out[-1][0] == "P" and not re.search(r"[.!?:»”)\]—]$", out[-1][1]):
            prev = out[-1][1]
            prev = prev[:-1] + text if prev.endswith("-") else prev + " " + text
            out[-1] = ("P", prev)
        else:
            out.append(("P", text))
    return out


def rebuild(slug, detect, start=None, stop=PROMO, reflow_text=False):
    """detect(kind, text, state) → None, ("group", nombre) o ("chapter", título)."""
    path = TEXTS / f"{slug}.txt"
    lines = path.read_text(encoding="utf-8").split("\n")
    blocks = [(x[0], x[2:]) for x in lines if x[1:2] == "|"]
    blocks = [(k, t) for k, t in blocks if not (k == "H" and re.fullmatch(r"Parte \d+|Inicio", t))]
    if reflow_text:
        blocks = reflow(blocks)
    body, chapters, state = [], [], {"group": ""}
    started = False
    for kind, text in blocks:
        if PROMO.search(text):
            if started and re.search(r"(?i)gracias por leer|^\s*fin\.?\s*$", text):
                break  # fin del libro: lo que sigue es promoción
            continue
        hit = detect(kind, text, state)
        if hit and hit[0] == "group":
            state["group"] = hit[1]
            continue
        if hit and hit[0] == "chapter":
            started = True
            if chapters:
                chapters[-1]["end"] = len(body) - 1
            chapters.append({"slug": "", "title": hit[1], "summary": "", "start": len(body), "end": len(body)})
            body.append("H|" + hit[1])
            continue
        if not started:
            continue
        if kind == "H":
            body.append("S|" + text)  # subtítulo dentro del capítulo
        else:
            body.append(f"{kind}|{text}")
    chapters[-1]["end"] = len(body) - 1
    used = set()
    for c in chapters:
        s = slugify(c["title"]) or "parte"
        while s in used:
            s += "-2"
        used.add(s)
        c["slug"] = s
    meta = json.loads((TEXTS / f"{slug}.json").read_text(encoding="utf-8"))
    meta["chapters"] = chapters
    meta.pop("inner_titles", None)
    path.write_text("\n".join(body), encoding="utf-8")
    (TEXTS / f"{slug}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    words = sum(len(b.split()) for b in body if b[:2] in ("P|", "V|"))
    print(f"{slug}: {len(chapters)} capítulos, {words:,} palabras · {chapters[0]['title']} … {chapters[-1]['title']}")


def h(rx, fmt=lambda m, st: m.group(0)):
    def detect(kind, text, state):
        if kind != "H":
            return None
        m = re.fullmatch(rx, text.strip(), re.I)
        return ("chapter", fmt(m, state)) if m else None
    return detect


def crimen(kind, text, state):
    t = text.strip()
    m = re.fullmatch(r"(Primera|Segunda|Tercera|Cuarta|Quinta|Sexta) parte", t, re.I)
    if kind == "H" and m:
        return ("group", ORD[m.group(1).lower()] + " parte")
    if kind == "H" and re.fullmatch(r"Ep[ií]logo", t, re.I):
        state["group"] = "Epílogo"
        return ("chapter", "Epílogo")
    if kind == "H" and re.fullmatch(ROMAN, t) and state["group"]:
        return ("chapter", f'{state["group"]}, capítulo {t}')
    return None


def divina(kind, text, state):
    t = text.strip().rstrip(".")
    m = re.match(r"(INFIERNO|PURGATORIO|PARA[IÍ]SO)", t)
    if kind == "H" and m:
        state["group"] = {"INFIERNO": "Infierno", "PURGATORIO": "Purgatorio"}.get(m.group(1), "Paraíso")
    m = re.fullmatch(r"CANTO\s+(\w+)", t, re.I)
    if kind == "H" and m:
        return ("chapter", f'{state["group"] or "Infierno"}, canto {m.group(1).lower()}')
    if kind == "H" and re.fullmatch(r"NOTAS:?", t):
        return ("chapter", "Notas")
    return None


def frankenstein(kind, text, state):
    t = text.strip().rstrip(".")
    m = re.fullmatch(r"VOLUMEN\s+(" + ROMAN + ")", t)
    if kind == "H" and m:
        return ("group", "Volumen " + m.group(1))
    m = re.fullmatch(r"(CARTA|CAP[IÍ]TULO)\s+(\w+)", t)
    if kind == "H" and m:
        word = "Carta" if m.group(1) == "CARTA" else "capítulo"
        return ("chapter", f"Carta {m.group(2)}" if word == "Carta" else f'{state["group"]}, capítulo {m.group(2)}')
    return None


def zaratustra(kind, text, state):
    t = text.strip()
    if t in ("Prólogo de Zaratustra",):
        return ("chapter", "Prólogo de Zaratustra")
    m = re.fullmatch(r"(\d{1,2})\.\s+(.{3,60})", t)
    if m and (kind == "H" or (kind == "P" and len(t) < 60 and not t.endswith((".", ",", ";")))):
        return ("chapter", f"{m.group(1)}. {cap(m.group(2))}")
    return None


def meditaciones(kind, text, state):
    m = re.fullmatch(r"LIBRO\s+(" + ROMAN + ")", text.strip())
    return ("chapter", "Libro " + m.group(1)) if m else None


def republica(kind, text, state):
    t = text.strip()
    if kind == "H" and re.fullmatch(ROMAN + r"|\d{1,2}", t):
        n = state.get("n", 0) + 1
        state["n"] = n
        return ("chapter", f"Libro {['I','II','III','IV','V','VI','VII','VIII','IX','X'][n - 1]}")
    return None


BOOKS = {
    "noches-blancas-dostoyevski": dict(detect=h(r"(PRIMERA|SEGUNDA|TERCERA|CUARTA) NOCHE|LA HISTORIA DE NASTENKA|MAÑANA",
                                                lambda m, s: cap(m.group(0)))),
    "el-principito-saint-exupery": dict(detect=h(r"DEDICATORIA|CAP[IÍ]TULO\s+" + ROMAN,
                                                 lambda m, s: "Dedicatoria" if m.group(0).startswith("DED") else "Capítulo " + m.group(0).split()[-1])),
    "don-quijote-de-la-mancha-cervantes": dict(detect=None),
    "el-arte-de-la-guerra-sun-tzu": dict(detect=h(r"(?:Sun Tzu\.\s*)?(Cap[ií]tulo\s+\d+)\s*(.*)",
                                                  lambda m, s: f"{m.group(1)}. {m.group(2)}" if m.group(2) else m.group(1))),
    "crimen-y-castigo-dostoyevski": dict(detect=crimen),
    "meditaciones-marco-aurelio": dict(detect=meditaciones),
    "la-divina-comedia-dante": dict(detect=divina),
    "la-metamorfosis-kafka": dict(detect=h(r"Cap[ií]tulo\s+\d+")),
    "memorias-del-subsuelo-dostoyevski": dict(detect=None),
    "de-la-brevedad-de-la-vida-seneca": dict(detect=h(r"(?:.*\.\s*)?(Cap[ií]tulo\s+" + ROMAN + ")", lambda m, s: m.group(1))),
    "asi-hablo-zaratustra-nietzsche": dict(detect=zaratustra),
    "la-republica-platon": dict(detect=republica, reflow_text=True),
    "frankenstein-mary-shelley": dict(detect=frankenstein),
    "dracula-bram-stoker": dict(detect=h(r"(?:Bram Stoker\.\s*)?(Cap[ií]tulo\s+\d+)\s*(.*)",
                                         lambda m, s: f"{m.group(1)}. {cap(m.group(2))}" if m.group(2) else m.group(1))),
    "alicia-en-el-pais-de-las-maravillas-lewis-carroll": dict(detect=None),
}


ALICIA = ["EN LA MADRIGUERA DEL CONEJO", "EL CHARCO DE LÁGRIMAS", "UNA CARRERA DE CAUCUS Y UNA LARGA HISTORIA",
          "EL CONEJO ENVÍA UNA PEQUEÑA FACTURA", "CONSEJOS DE UNA ORUGA", "CERDO Y PIMIENTA", "UNA LOCA FIESTA DE TÉ",
          "EL CAMPO DE CROQUET DE LA REINA", "LA HISTORIA DE LA TORTUGA FALSA", "LA CUADRILLA DE LANGOSTAS",
          "¿QUIÉN ROBÓ LAS TARTAS?", "LAS PRUEBAS DE ALICIA"]


def alicia(kind, text, state):
    if kind == "H" and text.strip().rstrip(".") in ALICIA:
        state["n"] = state.get("n", 0) + 1
        return ("chapter", f"Capítulo {['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII'][state['n'] - 1]}. {cap(text)}")
    return None


BOOKS["alicia-en-el-pais-de-las-maravillas-lewis-carroll"]["detect"] = alicia


def memorias(kind, text, state):
    t = text.strip()
    m = re.fullmatch(r"Parte (\d+): (.+)", t)
    if kind == "H" and m:
        state["group"] = f"Parte {m.group(1)}"
        state["sub"] = m.group(2)
        return None
    if re.fullmatch(ROMAN, t) and state["group"]:
        return ("chapter", f'{state["group"]} ({state["sub"]}), {t}')
    return None


def quijote(kind, text, state):
    if kind != "H":
        return None
    t = text.strip()
    m = re.match(r"(Primera|Segunda) parte\. (Cap[ií]tulo.*)", t)
    if m:
        state["group"] = m.group(1) + " parte"
        return ("chapter", f'{state["group"]}, {m.group(2)[0].lower()}{m.group(2)[1:]}')
    if re.match(r"Cap[ií]tulo\s+" + ROMAN, t) and state["group"]:
        return ("chapter", f'{state["group"]}, c{t[1:]}')
    if re.match(r"(Pr[oó]logo|Dedicatoria|Tasa|Al lector|Fe de erratas|El rey|Aprobaci[oó]n|Privilegio)", t):
        return ("chapter", t.replace("Prologo", "Prólogo") + (f' ({state["group"].lower()})' if state["group"] else ""))
    return None


BOOKS["memorias-del-subsuelo-dostoyevski"]["detect"] = memorias
BOOKS["don-quijote-de-la-mancha-cervantes"]["detect"] = quijote
NAMES = ["Jonathan", "Harker", "Mina", "Murray", "Lucy", "Westenra", "Seward", "Van Helsing", "Helsing", "Arthur",
         "Holmwood", "Quincey", "Morris", "Drácula", "Whitby", "Londres", "Transilvania", "Renfield", "Dailygraph", "Pall Mall"]


def fix_names(slug):
    p = TEXTS / f"{slug}.json"
    meta = json.loads(p.read_text(encoding="utf-8"))
    lines = (TEXTS / f"{slug}.txt").read_text(encoding="utf-8").split("\n")
    for c in meta["chapters"]:
        t = c["title"]
        for n in NAMES:
            t = re.sub(r"\b" + n.lower() + r"\b", n, t)
        c["title"] = t
        lines[c["start"]] = "H|" + t
    p.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (TEXTS / f"{slug}.txt").write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    only = sys.argv[1:]
    for slug, conf in BOOKS.items():
        if not only or slug in only:
            rebuild(slug, **conf)
            if slug == "dracula-bram-stoker":
                fix_names(slug)
