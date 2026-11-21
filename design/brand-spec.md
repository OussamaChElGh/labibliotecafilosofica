# Biblioteca editorial — muestra v0

Estado: dirección confirmada; pendiente de aprobación visual de la muestra.
Modo: rediseño integral de presentación, preservando contenido y rutas.
Audiencia: lectores y estudiantes que buscan libros e introducciones a la filosofía.
Diales: composición 7, movimiento 5 (reservado para v1), densidad 6, recursos reales 8, fidelidad 8.

## Sistema y recursos
- Logotipo original recuperado de wp-content/uploads/2023/07/logo-comprs.png; copia en public/diseno-v0/assets/logo-original.png. No se redibuja.
- Portadas: recursos reales locales del WordPress exportado, enlazados desde las tres páginas.
- Tipografías locales: public/fonts/fraunces.woff2 y inter.woff2. Fraunces es sustitución permitida por DESIGN.md.
- Colores: crema #f7f4ee, verde #064c37, tinta #161015 y azul #43a1d7. Tonos auxiliares derivados de estos.
- Referencia: DESIGN.md, tokens.json, variables.css, theme.css facilitados por el usuario y Fable.
- Capturas de la versión anterior: work/fable-home-1440.png y work/fable-home-360.png.

## Composición
Portada: búsqueda antes de la decoración, obra protagonista, seis portadas, recorrido histórico.
Catálogo: navegación lateral por categorías, versión horizontal en móvil y seis obras de muestra.
Ficha: portada y datos a ambos lados, descarga real original, sinopsis y enlaces al análisis completo.
Tres variantes disponibles en Tweaks: editorial, lectura tranquila, más expresiva. Ajuste independiente de espaciado.

## Límites de esta entrega
Muestra aislada en /diseno-v0/, /diseno-v0/libros/ y /diseno-v0/la-republica/.
No modifica las plantillas anteriores ni las direcciones de contenido.
Sin animación definitiva: se incorpora tras aprobar v0.
Catálogo de muestra parcial, señalado en pantalla; enlaces al catálogo existente.
Búsqueda y enlaces fuera de las tres vistas abren la versión existente.
No se ha ejecutado aceptación automatizada en navegador en esta fase; revisión estática de HTML, enlaces y recursos.

## Implementación editorial extendida
Dirección editorial aprobada por el usuario. Aplicada al generador: portada con buscador y obra protagonista; categorías con navegación lateral y adaptación horizontal en móvil; fichas con portada y acciones separadas del análisis; lectura con anchura limitada; cuadros Amazon con títulos completos disponibles.
Se conserva el contenido exportado y los IDs existentes. Se eliminan encabezados vacíos sin identificador visible para corregir espacios heredados.
GSAP local: entrada escalonada de cabecera, portada, estanterías, grupos de productos y navegación. Sin bucles decorativos. La carga respeta prefers-reduced-motion; el HTML permanece visible si JavaScript falla.
Validación: comprobaciones estáticas de publicaciones, medios, destinos internos y sintaxis JavaScript. No se ha ejecutado una nueva prueba visual automatizada en navegador en esta fase.

## Ficha compacta y biblioteca local
Recuperada la composición compacta anterior (portada 180 px, acciones junto al título, superficie verde suave), conservando las reglas móviles y GSAP. Eliminada la frase genérica.
Ruta nueva /mi-biblioteca/ con noindex: libros guardados solo en localStorage bajo biblioteca.saved-books.v1. Se persisten únicamente rutas; los títulos, portadas y enlaces proceden del generador. No se interpreta HTML de almacenamiento. Sin cuentas ni sincronización remota; sincronización entre pestañas del mismo origen mediante storage.
Estados: vacío, guardado, quitado, almacenamiento no disponible o datos inválidos. Foco recuperado al quitar una ficha. GSAP confirma guardar/quitar si está disponible y el usuario permite movimiento.
Verificación: pruebas de lógica de persistencia, errores, listado, eliminación y foco; 264 publicaciones, 1424 medios, 62 redirecciones, 52 tarjetas Amazon, sin destinos internos ausentes. Sin nueva aceptación visual en navegador.

## Refinamiento con Awwwards MCP
Referencias obtenidas mediante search_sites (colección Typography) y get_site_details:
- MONOLOG: https://www.awwwards.com/sites/monolog ; https://bymonolog.com/ . Ficha y captura: tipografía protagonista, composición del pie, galería. Adaptación propia: pie con invitación y navegación útil, escala tipográfica editorial y selección asimétrica de lecturas.
- PP Neue Montreal: https://www.awwwards.com/sites/pp-neue-montreal ; https://neuemontreal.com/ . Ficha y captura: presentación como guía, navegación e interacciones. Adaptación propia: menú con jerarquía y catálogo Portadas/Lista.
No se copian recursos gráficos, código ni tipografías de las referencias. Se mantiene la paleta y el contenido de la biblioteca.
Limitaciones: búsquedas books/editorial sin resultados en el corpus; galería de elementos vacía. analyze_page_structure no pudo ejecutarse porque el MCP no dispone de su dependencia opcional Playwright. No se atribuyen mecanismos concretos de movimiento a esas webs más allá de las fichas devueltas.
Comprobaciones de implementación: sintaxis, navegación interna, integridad de publicaciones y pruebas de biblioteca local y selector de presentación. Sin nueva aceptación visual automatizada.
