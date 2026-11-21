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

Por último ejecuta `node portadas.mjs`. Convierte la portada de cada obra en dos imágenes: `portada.png` (1000×1500, descargable desde el índice) y `social.png` (1200×630, la que se ve al compartir un enlace en redes o WhatsApp). El color y el número de cada portada se fijan en el campo `cover` del `.json`.

`revision-migracion.json` lista los recursos, enlaces y bloques pendientes. La vista de revisión deshabilita la indexación. Antes del lanzamiento deben resolverse esas incidencias, validar el contenido renderizado, revisar los enlaces a descargas e integrar y comprobar la configuración de AdSense y consentimiento. El argumento `--production` habilita el rastreo al regenerar. Conecta el dominio solo después de validar el entorno de Vercel.

Los datos privados y la configuración original se conservan en el WXR de origen. La versión estática muestra los comentarios aprobados que figuran como comentarios normales en WordPress. Los comentarios pendientes y los avisos automáticos de enlaces se conservan en el WXR. El sitio estático carece de formulario de comentarios y panel de edición.

## Vista previa en Vercel

Desde esta carpeta, inicia sesión con `npx vercel login` y ejecuta `npx vercel deploy`. Elige el equipo y el proyecto que correspondan. El despliegue de prueba usa `public/` y sirve `ads.txt` con el registro original. La configuración de revisión envía la cabecera `X-Robots-Tag: noindex`. Si el equipo ofrece protección de despliegue, actívala para limitar el acceso a la vista previa.

AdSense y la plataforma de consentimiento requieren configuración y prueba en el entorno de destino antes de conectar el dominio. El sitio incluye el archivo de autorización publicitaria. La carga de anuncios está pendiente.
