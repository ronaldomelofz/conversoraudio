/**
 * 🎯 CONVERSOR DE ÁUDIO - SERVICE WORKER
 * =====================================
 * Service Worker para cache offline e PWA
 * 
 * Funcionalidades:
 * - Cache de recursos estáticos
 * - Cache de modelos AI
 * - Funcionamento offline
 * - Push notifications (futuro)
 */

const CACHE_NAME = 'conversor-audio-v1.0.0';
const STATIC_CACHE = `${CACHE_NAME}-static`;
const DYNAMIC_CACHE = `${CACHE_NAME}-dynamic`;
const AI_MODELS_CACHE = `${CACHE_NAME}-ai-models`;

// Recursos essenciais para cache
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/js/app.js',
    '/manifest.json',
    // Não incluir CDN aqui - será cacheado dinamicamente
];

// Recursos de modelos AI (cache especial)
const AI_MODEL_PATTERNS = [
    /huggingface\.co.*\.onnx$/,
    /huggingface\.co.*\.json$/,
    /huggingface\.co.*tokenizer/,
    /cdn\.jsdelivr\.net.*transformers/,
];

// Recursos CDN importantes
const CDN_PATTERNS = [
    /cdn\.jsdelivr\.net/,
    /unpkg\.com/,
    /fonts\.googleapis\.com/,
    /fonts\.gstatic\.com/,
];

self.addEventListener('install', (event) => {
    console.log('🎯 Service Worker: Instalando...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('📦 Cache estático criado');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('✅ Service Worker instalado');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('❌ Erro na instalação:', error);
            })
    );
});

self.addEventListener('activate', (event) => {
    console.log('🚀 Service Worker: Ativando...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        // Remove caches antigos
                        if (cacheName.startsWith('conversor-audio-') && 
                            cacheName !== STATIC_CACHE && 
                            cacheName !== DYNAMIC_CACHE && 
                            cacheName !== AI_MODELS_CACHE) {
                            console.log('🗑️ Removendo cache antigo:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('✅ Service Worker ativado');
                return self.clients.claim();
            })
    );
});

self.addEventListener('fetch', (event) => {
    const request = event.request;
    const url = new URL(request.url);
    
    // Ignorar requests non-GET
    if (request.method !== 'GET') {
        return;
    }
    
    // Estratégia para diferentes tipos de recursos
    if (isAIModelRequest(url)) {
        event.respondWith(handleAIModelRequest(request));
    } else if (isCDNRequest(url)) {
        event.respondWith(handleCDNRequest(request));
    } else if (isStaticAsset(url)) {
        event.respondWith(handleStaticRequest(request));
    } else {
        event.respondWith(handleDynamicRequest(request));
    }
});

// Verifica se é request de modelo AI
function isAIModelRequest(url) {
    return AI_MODEL_PATTERNS.some(pattern => pattern.test(url.href));
}

// Verifica se é request de CDN
function isCDNRequest(url) {
    return CDN_PATTERNS.some(pattern => pattern.test(url.hostname));
}

// Verifica se é recurso estático
function isStaticAsset(url) {
    return url.origin === location.origin && (
        url.pathname.endsWith('.js') ||
        url.pathname.endsWith('.css') ||
        url.pathname.endsWith('.html') ||
        url.pathname.endsWith('.json') ||
        url.pathname === '/'
    );
}

// Handle requests de modelos AI - Cache-first com TTL longo
async function handleAIModelRequest(request) {
    try {
        const cache = await caches.open(AI_MODELS_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            console.log('🤖 Modelo AI do cache:', request.url);
            return cachedResponse;
        }
        
        console.log('📥 Baixando modelo AI:', request.url);
        const response = await fetch(request);
        
        if (response.ok) {
            // Cache apenas se o download foi bem-sucedido
            await cache.put(request, response.clone());
            console.log('💾 Modelo AI cacheado:', request.url);
        }
        
        return response;
    } catch (error) {
        console.error('❌ Erro ao buscar modelo AI:', error);
        throw error;
    }
}

// Handle requests de CDN - Cache-first
async function handleCDNRequest(request) {
    try {
        const cache = await caches.open(DYNAMIC_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            // Retorna do cache e tenta atualizar em background
            updateCacheInBackground(request, cache);
            return cachedResponse;
        }
        
        const response = await fetch(request);
        
        if (response.ok) {
            await cache.put(request, response.clone());
        }
        
        return response;
    } catch (error) {
        console.error('❌ Erro em request CDN:', error);
        
        // Tenta retornar do cache mesmo com erro
        const cache = await caches.open(DYNAMIC_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        throw error;
    }
}

// Handle recursos estáticos - Cache-first
async function handleStaticRequest(request) {
    try {
        const cache = await caches.open(STATIC_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        const response = await fetch(request);
        
        if (response.ok) {
            await cache.put(request, response.clone());
        }
        
        return response;
    } catch (error) {
        console.error('❌ Erro em recurso estático:', error);
        
        // Para navegação, retorna index.html
        if (request.mode === 'navigate') {
            const cache = await caches.open(STATIC_CACHE);
            return cache.match('/index.html');
        }
        
        throw error;
    }
}

// Handle requests dinâmicos - Network-first
async function handleDynamicRequest(request) {
    try {
        const response = await fetch(request);
        
        if (response.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            await cache.put(request, response.clone());
        }
        
        return response;
    } catch (error) {
        console.error('❌ Erro em request dinâmico:', error);
        
        const cache = await caches.open(DYNAMIC_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Para navegação offline, retorna página principal
        if (request.mode === 'navigate') {
            const staticCache = await caches.open(STATIC_CACHE);
            return staticCache.match('/index.html');
        }
        
        throw error;
    }
}

// Atualiza cache em background
async function updateCacheInBackground(request, cache) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            await cache.put(request, response);
            console.log('🔄 Cache atualizado em background:', request.url);
        }
    } catch (error) {
        console.log('⚠️ Falha ao atualizar cache em background:', error.message);
    }
}

// Gerenciamento de mensagens do app
self.addEventListener('message', (event) => {
    const { type, payload } = event.data;
    
    switch (type) {
        case 'SKIP_WAITING':
            self.skipWaiting();
            break;
            
        case 'CLEAR_CACHE':
            clearAllCaches().then(() => {
                event.ports[0].postMessage({ success: true });
            });
            break;
            
        case 'CACHE_AI_MODEL':
            cacheAIModel(payload.url).then(() => {
                event.ports[0].postMessage({ success: true });
            });
            break;
            
        case 'GET_CACHE_INFO':
            getCacheInfo().then((info) => {
                event.ports[0].postMessage({ success: true, data: info });
            });
            break;
    }
});

// Limpa todos os caches
async function clearAllCaches() {
    const cacheNames = await caches.keys();
    await Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
    );
    console.log('🗑️ Todos os caches limpos');
}

// Pre-cache um modelo AI específico
async function cacheAIModel(url) {
    try {
        const cache = await caches.open(AI_MODELS_CACHE);
        const response = await fetch(url);
        
        if (response.ok) {
            await cache.put(url, response);
            console.log('💾 Modelo AI pré-cacheado:', url);
        }
    } catch (error) {
        console.error('❌ Erro ao pre-cachear modelo:', error);
    }
}

// Informações sobre cache
async function getCacheInfo() {
    const cacheNames = await caches.keys();
    const info = {};
    
    for (const cacheName of cacheNames) {
        const cache = await caches.open(cacheName);
        const keys = await cache.keys();
        info[cacheName] = {
            count: keys.length,
            urls: keys.map(req => req.url)
        };
    }
    
    return info;
}

// Notificações push (preparação para futuro)
self.addEventListener('push', (event) => {
    if (event.data) {
        const data = event.data.json();
        
        const options = {
            body: data.body || 'Transcrição concluída!',
            icon: '/icons/icon-192.png',
            badge: '/icons/badge-72.png',
            tag: 'transcription',
            renotify: true,
            requireInteraction: false,
            actions: [
                {
                    action: 'view',
                    title: 'Ver Resultado'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification(
                data.title || '🎯 Conversor de Áudio',
                options
            )
        );
    }
});

// Clicks em notificações
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.action === 'view' || !event.action) {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Sync em background (para futuras funcionalidades offline)
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-transcription') {
        event.waitUntil(doBackgroundTranscription());
    }
});

async function doBackgroundTranscription() {
    console.log('🔄 Sync em background executado');
    // Implementar transcrição offline no futuro
}

console.log('🎯 Service Worker carregado - Versão:', CACHE_NAME); 