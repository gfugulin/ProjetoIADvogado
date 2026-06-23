const CACHE_NAME = 'iadvogado-cache-v1';
const ASSETS = [
  '/static/chatbot.html',
  '/static/manifest.json'
];

// Instalação do Service Worker e caching de recursos essenciais
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Ativação e limpeza de caches antigos
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Interceptação de requisições
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Evita interceptar chamadas da API de backend
  if (url.pathname.includes('/upload') || url.pathname.includes('/process-number') || url.pathname.includes('/health')) {
    e.respondWith(
      fetch(e.request).catch(() => {
        return new Response(
          JSON.stringify({
            success: false,
            detail: "Você está sem conexão com a internet. Verifique sua rede e tente novamente."
          }),
          {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
          }
        );
      })
    );
    return;
  }

  // Estratégia Cache First para os arquivos estáticos da interface
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(e.request);
    })
  );
});
