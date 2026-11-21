// Devuelve el país del visitante (cabecera que añade Vercel) para elegir la tienda de Amazon.
// No guarda nada ni usa cookies.
export const config = { runtime: 'edge' }

export default function handler(request) {
  const country = request.headers.get('x-vercel-ip-country') || ''
  return new Response(JSON.stringify({ country }), {
    headers: { 'content-type': 'application/json', 'cache-control': 'private, no-store' },
  })
}
