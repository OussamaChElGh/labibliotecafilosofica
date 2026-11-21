# Portada editorial 3D

Implementación del prompt aprobado en `docs/prompt-maestro-portada-biblioteca-3d.md`.

Modo: rediseño de portada. Contratos conservados: rutas, catálogo, búsqueda `q`, fichas de libro, datos guardados en el navegador, redirecciones y contenido migrado. La portada anterior se conserva como `legacy_home_intro()` y copia de seguridad en `work/folio-backup/migrate.py`.

Diseño: negro #000, papel #f7f4ee, tinta #161015, verde #064c37; Libre Caslon Display para la marca monumental e Inter para UI. Diales: variación 8, movimiento 7, densidad 4, recursos reales 9, marca 9. La escena es el escaparate, la búsqueda posterior es el acceso al catálogo.

Logo real: `public/wp-content/uploads/2023/07/logo-comprs.png`.
Fuente: `fonts/libre-caslon-display.ttf`, procedencia Google Fonts, licencia `fonts/libre-caslon-display-OFL.txt`. Inter: `fonts/inter.woff2`.
Recursos: `folio-books.json` registra 32 títulos, autores, fichas, portadas originales y derivadas. `folio-assets/` contiene versiones WebP preparadas por `work/prepare-folio-assets.py`; no modifica los originales. Algunas fuentes tienen resolución limitada y sus derivados no añaden detalle.

Three.js 0.160.0 y RoomEnvironment están en `vendor/`, con licencia MIT incluida. Se ajustó el import de RoomEnvironment para resolver el módulo local. GSAP utiliza el runtime ya existente. Referencias consultadas: https://threejs.org/docs/ y https://gsap.com/docs/v3/GSAP/gsap.context()/ .

Comportamiento: escena solo en escritorio con puntero fino; HTML deslizable en móvil, movimiento reducido, ahorro de datos y fallos WebGL. Render bajo demanda, suspendido fuera del viewport o con pestaña oculta; botón de pausa. Los 32 enlaces HTML siguen disponibles al foco del teclado en escritorio.

No se han implementado cuentas, premios, sincronización ni nuevas categorías. No se han modificado fichas ni políticas de anuncios. No se atribuyen mejoras de ingresos o SEO a este cambio sin medición.
