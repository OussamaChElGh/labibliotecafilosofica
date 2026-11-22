"""Teatro de es.wikisource.org con personajes, en verso o en prosa, al formato de textos/ (un acto o jornada por capítulo).

Uso:  python teatro_verso.py "Fuenteovejuna" fuenteovejuna-lope-de-vega --titulo Fuenteovejuna --autor "Lope de Vega" \
          --ficha /fuenteovejuna-lope-de-vega/ [--partes "Obra/Acto I|Obra/Acto II|…"] [--edicion …]

Reconoce las formas en que Wikisource marca el diálogo:
  - tabla de dos columnas: personaje | versos (Fuenteovejuna, El burlador de Sevilla, Don Juan Tenorio);
  - «PERSONAJE: verso» o «ROS. verso» al principio de la línea, dentro de un poema o un <pre> (La vida es sueño);
  - «<b>Personaje</b>: texto» en prosa (Lorca).
Cada intervención empieza en su primer verso o párrafo, con el personaje en «speakers». Las acotaciones (entre
paréntesis, en cursiva o centradas: «Salen…», «Vase») van como S|. Las abreviaturas («ROS.», «BUTT.») se
desarrollan con el nombre completo que aparece en la obra o en el reparto cuando solo hay uno que empiece así.
"""
import argparse
import html as htmllib
import json
import re
import urllib.parse

from lxml import html

from wikisource import TEXTS, api, chapter_slug, subpages

CAPS = "A-ZÁÉÍÓÚÑÜ"
SPEAKER_ONLY = re.compile(rf"^([{CAPS}][{CAPS}a-záéíóúñü\.\s]{{0,30}}?)\s*[:.]?\s*$")
SPEAKER_LINE = re.compile(rf"^([{CAPS}][{CAPS}]+(?:\s+[{CAPS}][{CAPS}]+){{0,3}}\.?)\s*(?:[:.]\s*[—–-]|[:.—–])\s*(.+)$")
STAGE_START = re.compile(r"^(Sale|Salen|Vase|Vanse|Vánse|Éntrase|Éntranse|Entra|Entran|Cantan|Dentro|Tocan|Suena|Cúbrese|Descúbrese|Aparece)\b")
ACT = re.compile(r"^(ACTO|JORNADA|PARTE)\b", re.I)


def clean(text):
    return re.sub(r"\s+", " ", htmllib.unescape(text).replace("\xa0", " ")).strip()


def is_caps_name(text):
    letters = re.sub(r"[^A-Za-zÁÉÍÓÚÑÜáéíóúñü]", "", text)
    return bool(letters) and letters.isupper() and len(text) <= 32 and not ACT.match(text) and not text.startswith("ESCENA")


def lines_of_cell(node):
    """Texto de un nodo partido en líneas por <br>, <p> y saltos de línea; las cursivas quedan marcadas con «⟨…⟩»."""
    raw = html.tostring(node, encoding="unicode")
    raw = re.sub(r"<(i|em)\b[^>]*>(.*?)</\1>", lambda m: "⟨" + re.sub(r"<[^>]+>", "", m.group(2)) + "⟩", raw, flags=re.S)
    raw = re.sub(r"<br\s*/?>|</p>|</div>|</dd>|</li>", "\n", raw)
    raw = re.sub(r"<[^>]+>", "", raw)
    return [clean(line) for line in htmllib.unescape(raw).split("\n") if clean(line)]


class Builder:
    def __init__(self):
        self.blocks, self.speakers, self.pending = [], {}, None

    def stage(self, text):
        text = text.replace("⟨", "").replace("⟩", "").strip()
        if text:
            self.blocks.append("S|" + text)

    def say(self, kind, text, speaker=None):
        if speaker:
            self.pending = speaker
        # Acotación en cursiva al principio o al final de la línea: aparte, como S|.
        lead = re.match(r"^⟨([^⟩]*)⟩\s*(.*)$", text)
        if lead and lead.group(2):
            if self.pending is None and not self.blocks:
                pass
            text = lead.group(2)
            stage_first = lead.group(1)
        else:
            stage_first = None
        tail = re.match(r"^(.*?)\s*⟨([^⟩]*)⟩$", text)
        stage_last = None
        if tail and tail.group(1):
            text, stage_last = tail.group(1), tail.group(2)
        text = text.replace("⟨", "(").replace("⟩", ")") if kind == "P|" else text.replace("⟨", "").replace("⟩", "")
        if stage_first and kind == "P|":
            text = f"({stage_first.strip(' ()')}) {text}"
        elif stage_first:
            self.stage(stage_first)
        if self.pending:
            self.speakers[len(self.blocks)] = self.pending
            self.pending = None
        self.blocks.append(kind + text.strip())
        if stage_last:
            self.stage(stage_last if stage_last.startswith("(") else f"({stage_last.strip(' ()')})")


def classify_line(builder, line, kind):
    """Una línea de poema o de párrafo: personaje, acotación, verso o prosa."""
    if re.fullmatch(r"⟨[^⟩]*⟩", line) or (line.startswith("(") and line.endswith(")")):
        builder.stage(line if line.startswith("(") else "(" + line.strip("⟨⟩ ()") + ")")
        return
    head = re.match(r"^\*\*(.+?)\*\*\s*[:.]?\s*(.*)$", line)  # <b>Personaje</b>: texto
    if head:
        name, rest = head.group(1).strip(" :."), head.group(2)
        if rest:
            builder.say(kind, rest, name)
        else:
            builder.pending = name
        return
    m = SPEAKER_LINE.match(line)
    if m and is_caps_name(m.group(1)):
        builder.say(kind, m.group(2), m.group(1))
        return
    if is_caps_name(line.rstrip(":. ")) and SPEAKER_ONLY.match(line) and len(line.split()) <= 4:
        builder.pending = line.rstrip(":. ")
        return
    if STAGE_START.match(line) and kind == "V|" and builder.pending is None and len(line) < 140 and line[-1:] in ".)":
        builder.stage(line)
        return
    builder.say(kind, line)


def convert_act(page):
    data = api(action="parse", page=page, prop="text|revid", redirects=1)
    text = data["parse"]["text"]
    text = re.sub(r"<style.*?</style>|<link[^>]*>|<sup[^>]*class=\"reference\".*?</sup>", "", text, flags=re.S)
    text = re.sub(r'<span[^>]*class="pagenum"[^>]*>.*?</span>', "", text, flags=re.S)
    text = re.sub(r'<span class="mw-editsection">.*?</span></span>', "", text, flags=re.S)
    text = re.sub(r"<b>(.*?)</b>", r"**\1**", text, flags=re.S)
    tree = html.fromstring(text)
    for junk in tree.xpath('//*[@id="headertemplate"]|//*[contains(@class,"ws-noexport")]|//*[contains(@class,"noprint")]'
                           '|//*[contains(@class,"interwiki-extra")]|//table[contains(@class,"headertemplate")]'):
        junk.drop_tree()
    b = Builder()
    handled = set()
    for node in tree.iter():
        if node in handled or not isinstance(node.tag, str):
            continue
        if any(a in handled for a in node.iterancestors()):
            continue
        tag, css = node.tag, node.get("class") or ""
        if tag in ("h2", "h3", "h4", "h5"):
            handled.add(node)
            title = clean(node.text_content()).strip("*")
            if not title or ACT.match(title):
                continue
            b.stage(re.sub(r"(?i)^escena\s+", "Escena ", title.capitalize() if title.isupper() else title))
        elif tag == "tr":
            handled.add(node)
            cells = node.xpath("./td")
            if len(cells) == 2:
                name = clean(cells[0].text_content()).strip("*").rstrip(":. ")
                lines = lines_of_cell(cells[1])
                if name and is_caps_name(name):
                    b.pending = name
                for line in lines:
                    classify_line(b, line, "V|")
            elif len(cells) == 1:
                for line in lines_of_cell(cells[0]):
                    if line.strip("*").isupper() and ACT.match(line.strip("*")):
                        continue
                    b.stage(line.strip("*")) if (line.startswith("**") or STAGE_START.match(line.strip("*"))) else classify_line(b, line, "V|")
        elif tag == "pre" or (tag == "div" and "poem" in css.split() and not node.xpath(".//table")):
            handled.add(node)
            for line in lines_of_cell(node) if tag == "div" else [clean(x) for x in node.text_content().split("\n") if clean(x)]:
                classify_line(b, line, "V|")
        elif tag == "p" and not node.xpath("ancestor::table|ancestor::div[contains(@class,'poem')]"):
            handled.add(node)
            lines = lines_of_cell(node)
            if not lines:
                continue
            centered = "center" in (node.get("style") or "") or node.xpath("ancestor::*[contains(@style,'center')]")
            whole = " ".join(lines)
            if ACT.match(whole.strip("*")) and len(whole) < 60:
                continue
            if centered and not whole.startswith("**") and not is_caps_name(whole.rstrip(":. ")):
                b.stage(whole)
            elif len(lines) > 1 and not whole.startswith("**"):
                for line in lines:
                    classify_line(b, line, "V|")
            else:
                if is_caps_name(whole.strip("*").rstrip(":. ")) and len(whole.split()) <= 6 and " y " in whole:
                    b.stage(whole.strip("*"))  # «BUTTARELLI y MIGUEL»: quienes están en escena
                else:
                    classify_line(b, whole, "P|")
    # Limpieza: negritas sueltas, dobles paréntesis «((Entrando).)» y bloques vacíos.
    blocks, speakers, kept = [], {}, 0
    for i, block in enumerate(b.blocks):
        text = re.sub(r"\*\*", "", block[2:])
        text = re.sub(r"\(\(([^()]*)\)\.?\)", r"(\1.)", text).replace("..)", ".)").strip()
        if not text.strip(" .:"):
            continue
        if i in b.speakers:
            speakers[len(blocks)] = b.speakers[i]
        blocks.append(block[:2] + text)
    # Reparto al principio del acto: una sola acotación «Personajes: …».
    for i, block in enumerate(blocks):
        if re.fullmatch(r"S\|(Personajes|Dramatis person\w+|Reparto|Elenco)\.?", block):
            j = i + 1
            while j < len(blocks) and blocks[j][:2] in ("V|", "P|") and j not in speakers:
                j += 1
            if j > i + 1:
                cast = "; ".join(x[2:] for x in blocks[i + 1:j])
                blocks = blocks[:i] + ["S|Personajes: " + cast] + blocks[j:]
                speakers = {(k - (j - i - 1) if k > i else k): v for k, v in speakers.items()}
            break
    return blocks, speakers, data["parse"].get("revid")


def expand_names(speakers, cast_text=""):
    """«ROS.» → «Rosaura» si en la obra o en el reparto hay un solo nombre que empiece así."""
    words = {w for w in re.findall(rf"[{CAPS}][a-záéíóúñü]+|[{CAPS}]{{3,}}", cast_text)}
    full = {n.rstrip(".") for n in speakers.values() if not n.endswith(".")} | {w for w in words}
    def nice(name):
        name = name.rstrip(".").strip()
        if name.isupper():
            name = " ".join(w if w.lower() in ("de", "del", "y", "la", "el") else w.capitalize() for w in name.lower().split())
        return name
    out = {}
    plain = lambda t: t.lower().translate(str.maketrans("áéíóúü", "aeiouu"))
    for k, name in speakers.items():
        if name.endswith("."):
            stem = name.rstrip(".").lower()
            options = {nice(f) for f in full if f.lower().startswith(stem) and f.lower() != stem}
            out[k] = options.pop() if len(options) == 1 else nice(name)
        else:
            out[k] = nice(name)
    # Variantes sin tilde («Musicos», «Ortuno»): la forma más frecuente con tilde.
    counts = {}
    for name in out.values():
        counts[name] = counts.get(name, 0) + 1
    best = {}
    for name, n in sorted(counts.items(), key=lambda x: -x[1]):
        best.setdefault(plain(name), name)
    return {k: best[plain(v)] for k, v in out.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("page")
    parser.add_argument("slug")
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--autor", required=True)
    parser.add_argument("--ficha", required=True)
    parser.add_argument("--ruta-autor", default="")
    parser.add_argument("--traductor", default="")
    parser.add_argument("--edicion", default="")
    parser.add_argument("--partes", default="", help="páginas de cada acto, separadas por «|»; si no, las subpáginas")
    parser.add_argument("--nombres", default="", help="«Ros=Rosaura|Segis=Segismundo»: nombres que no se resuelven solos (tal como salen)")
    args = parser.parse_args()
    if args.partes:
        parts = [(p, p.replace(args.page, "").strip(" /:")) for p in args.partes.split("|") if p]
        revision = None
    else:
        _, parts, revision = subpages(args.page)
    cast = ""
    body, speakers, chapters = [], {}, []
    for sub, label in parts:
        name = (label or sub.rsplit("/", 1)[-1]).strip()
        if re.search(r"(?i)personajes|elenco|reparto|dramatis", sub + " " + name):
            cast += " " + clean(html.fromstring(api(action="parse", page=sub, prop="text")["parse"]["text"]).text_content())
            continue
        blocks, own, rev = convert_act(sub)
        revision = revision or rev
        title = re.sub(r"(?i)^acto\s+", "Acto ", name)
        title = {"I": "Jornada primera", "II": "Jornada segunda", "III": "Jornada tercera"}.get(title, title)
        offset = len(body) + 1
        chapters.append({"slug": chapter_slug(name) or f"parte-{len(chapters) + 1}", "title": title, "summary": "",
                         "start": len(body), "end": len(body) + len(blocks)})
        speakers.update({k + offset: v for k, v in own.items()})
        body += ["H|" + title] + blocks
    manual = dict(x.split("=", 1) for x in args.nombres.split("|") if "=" in x)
    speakers = expand_names(speakers, cast)
    speakers = {k: manual.get(v, v) for k, v in speakers.items()}
    (TEXTS / f"{args.slug}.txt").write_text("\n".join(body), encoding="utf-8")
    config = TEXTS / f"{args.slug}.json"
    meta = json.loads(config.read_text(encoding="utf-8")) if config.exists() else {}
    meta.update({
        "slug": args.slug, "title": args.titulo, "author": args.autor, "author_route": args.ruta_autor or meta.get("author_route", ""),
        "book_route": args.ficha, "translator": args.traductor, "edition": args.edicion or meta.get("edition", ""),
        "source_url": "https://es.wikisource.org/wiki/" + urllib.parse.quote(args.page.replace(" ", "_")),
        "source_revision": revision, "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/deed.es",
        "speakers": {str(k): v for k, v in sorted(speakers.items())}, "chapters": chapters,
    })
    config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    words = sum(len(b.split()) for b in body if b[:2] in ("P|", "V|"))
    print(f"{args.slug}: {len(body)} bloques, {words:,} palabras, {len(chapters)} actos, {len(speakers)} intervenciones")


if __name__ == "__main__":
    main()
