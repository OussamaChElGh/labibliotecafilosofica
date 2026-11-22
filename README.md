# La Biblioteca Filosófica

Versión estática de revisión. Vercel puede servir `public/` directamente con la configuración incluida.

## Vista local

```text
python -m http.server 8765 --bind 127.0.0.1 --directory public
```

Abrir http://127.0.0.1:8765/.

## Regeneración

Instala Python y lxml. Ejecuta `python migrate.py exportacion.xml uploads.zip --crawl inventario-web.csv` desde una copia limpia del proyecto. El CSV opcional añade las redirecciones verificadas durante el rastreo. El generador añade los resultados a `public/`, así que para una nueva exportación usa una carpeta de salida vacía. Guarda el WXR y el ZIP fuera del proyecto y del repositorio.

Después ejecuta `python lectura_completa.py`. Genera en `public/leer/` la lectura online, dividida en capítulos, de las obras de dominio público que hay en `textos/` (un `.txt` con el texto y un `.json` con los capítulos), y las añade al sitemap.

Después ejecuta `python pulir.py`. Quita de las páginas generadas los restos del WordPress: el bloque de donación, el widget «¿quieres conocer más libros…?», el botón de descarga repetido de Elementor, los shortcodes `[caption]`, los párrafos vacíos y los títulos sin texto. También elige las tres sugerencias de «Sigue explorando» de cada página por autor, etiquetas y palabras de la URL, y pone primero la lectura online del mismo autor si existe. Por último corrige títulos de Google repetidos y añade imagen para compartir (og:image) a las páginas que no la tienen. En las fichas de libro pone el título y el autor reales en los datos estructurados (`Book`) y, si la ficha no tiene enlace de compra, añade «Ver edición en papel» con la búsqueda del libro en Amazon y la etiqueta de afiliado (`AFFILIATE_TAG`). Se puede ejecutar varias veces sin efectos.

Por último ejecuta `node portadas.mjs`. Convierte la portada de cada obra en dos imágenes: `portada.png` (1000×1500, descargable desde el índice) y `social.png` (1200×630, la que se ve al compartir un enlace en redes o WhatsApp). El color y el número de cada portada se fijan en el campo `cover` del `.json`. Con `cover.art` (archivo en `textos/ilustraciones/`, punto de interés `focus`, `url` publicada y `credit`) la portada lleva una pintura de dominio público dentro del marco. También genera `<slug>.pdf`, la edición en PDF (A5) con portada, índice, notas y atribución, a partir de `build/impresion/` (lo escribe `lectura_completa.py`) y `impresion.css`. `vercel.json` sirve esos PDF con `X-Robots-Tag: noindex`, para que en Google posicione la ficha y no el PDF.

`revision-migracion.json` lista los recursos, enlaces y bloques pendientes. La vista de revisión deshabilita la indexación. Antes del lanzamiento deben resolverse esas incidencias, validar el contenido renderizado, revisar los enlaces a descargas e integrar y comprobar la configuración de AdSense y consentimiento. El argumento `--production` habilita el rastreo al regenerar. Conecta el dominio solo después de validar el entorno de Vercel.

Los datos privados y la configuración original se conservan en el WXR de origen. La versión estática muestra los comentarios aprobados que figuran como comentarios normales en WordPress. Los comentarios pendientes y los avisos automáticos de enlaces se conservan en el WXR. El sitio estático carece de formulario de comentarios y panel de edición.

## Vista previa en Vercel

Desde esta carpeta, inicia sesión con `npx vercel login` y ejecuta `npx vercel deploy`. Elige el equipo y el proyecto que correspondan. El despliegue de prueba usa `public/` y sirve `ads.txt` con el registro original. La configuración de revisión envía la cabecera `X-Robots-Tag: noindex`. Si el equipo ofrece protección de despliegue, actívala para limitar el acceso a la vista previa.

AdSense y la plataforma de consentimiento requieren configuración y prueba en el entorno de destino antes de conectar el dominio. El sitio incluye el archivo de autorización publicitaria. La carga de anuncios está pendiente.

## Afiliados de Amazon por país

Los enlaces de compra (`a[data-query]`, los añade `pulir.py`) apuntan a amazon.es. `public/biblioteca.js` consulta `/api/pais` (función de Vercel que lee la cabecera `x-vercel-ip-country`, sin cookies) y lleva a los lectores de América (México incluido, mientras no haya etiqueta de amazon.com.mx) a amazon.com con la etiqueta de EE. UU., con la búsqueda del libro por título y autor. España y el resto siguen en amazon.es.

## Guía de lectura (resumen) de cada obra

Si `textos/<slug>.json` tiene la clave `guide`, `lectura_completa.py` genera `/leer/<slug>/resumen/`: resumen breve, de qué trata, resumen por capítulos (`guide.chapters`, con enlace a cada capítulo), personajes, ideas principales, frases destacadas y preguntas frecuentes (con datos estructurados `FAQPage`). Cada frase de `guide.quotes` debe aparecer literalmente en el capítulo que indica; si no, el script se detiene. `pulir.py` añade el enlace «Resumen y personajes» en la ficha del libro.

## Páginas de frases

`textos/frases/paginas.json` define las páginas `/frases/<slug>/` (por personaje con `by` o por autor de la obra con `author`). `lectura_completa.py` las genera con las citas comprobadas de las guías (`guide.quotes`, cada una con `by`, quién la dice) y escribe `build/frases.json`. Después, `node frases.mjs` crea una imagen 1080×1080 por frase en `public/frases/img/` para compartir en redes y borra las que ya no se usan.

## Menú e índices

El menú principal se define en `navigation()` de `migrate.py` y `pulir.py` lo aplica a todas las páginas ya generadas, así que para cambiarlo basta con editar esa función y volver a ejecutar `pulir.py`. El menú enlaza solo a índices, nunca a libros sueltos: Leer gratis (`/leer/`, `/resumenes/`, `/frases/`), Libros PDF, Autores, Historia y Artículos. `lectura_completa.py` regenera esos tres índices con todas las obras que tengan lectura, guía o página de frases, de modo que crecen solos al añadir libros. `pulir.py` también enlaza la lectura online, el resumen y las frases desde la ficha de cada libro, desde la página de su autor y desde los artículos que indica `link_from` en `textos/frases/paginas.json`.

Orden completo: `python lectura_completa.py && python pulir.py && node portadas.mjs && python comprimir.py && node frases.mjs && python fichas_antiguas.py` (comprimir.py necesita `pip install pikepdf`).

Obras divididas en subpáginas en Wikisource (novelas, por ejemplo): `python wikisource.py "Marianela" marianela-benito-perez-galdos --autor "Benito Pérez Galdós" --capitulos`, que crea un capítulo por subpágina. Los textos de las fichas de los clásicos en español están en `textos/fichas/clasicos.py`.

`fichas_antiguas.py` pasa las fichas heredadas de WordPress al formato de ficha única (resumen, personajes, ideas, preguntas frecuentes con FAQPage, título y h1 nuevos) con los textos de `textos/fichas/antiguas/*.py`, una entrada por ruta. Reescribe todo el cuerpo con la estructura nueva (resumen, cita, personajes, ideas, contexto, datos del libro, Amazon, preguntas y lecturas relacionadas). De WordPress solo aprovecha la cita (si está en `CITAS_VERIFICADAS`), la ficha técnica, el contexto, los recuadros de Amazon y los enlaces internos, que la primera vez guarda en `textos/fichas/antiguas/extraido.json`; así es idempotente. No borres ese archivo: el texto antiguo ya no está en `public/`.

`textos/fichas/lectura_antiguas.py` da lectura online a libros que ya tenían ficha antigua (Cándido, Zadig, la Fundamentación de Kant, Así va el mundo…): tras descargar el texto con `wikisource.py`, copia a su JSON los datos de `textos/fichas/antiguas/*.py` y numera los capítulos. Desde entonces la ficha de esa URL la genera `lectura_completa.py` y `fichas_antiguas.py` la salta.

Los libros con `ficha` en su JSON tienen una sola página principal, la ficha (`book_route`): `/leer/<slug>/` redirige a ella (lo escribe `lectura_completa.py` en vercel.json) y «Leer online» lleva a la primera parte. `wikisource.py` descarga una obra de Wikisource al formato de `textos/`; los textos editoriales de cada lote están en `textos/fichas/`.
