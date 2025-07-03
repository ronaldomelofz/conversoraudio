/**
 * 🤖 CONFIGURAÇÃO WHISPER.JS
 * =========================
 * Configurações específicas para funcionamento do Whisper.js no Netlify
 * Inclui fallbacks e otimizações para diferentes navegadores
 */

// Configuração global do ambiente
window.WHISPER_CONFIG = {
    // CDN alternativo para modelos
    modelBasePath: 'https://huggingface.co/Xenova/',
    
    // Configurações de cache
    cacheEnabled: true,
    maxCacheSize: 500 * 1024 * 1024, // 500MB
    
    // Modelos disponíveis (ordenados por tamanho)
    availableModels: [
        {
            id: 'tiny',
            name: 'Whisper Tiny (39MB)',
            model: 'Xenova/whisper-tiny',
            size: '39MB',
            quality: 'Básica - Rápida'
        },
        {
            id: 'base',
            name: 'Whisper Base (74MB)', 
            model: 'Xenova/whisper-base',
            size: '74MB',
            quality: 'Boa - Balanceada'
        },
        {
            id: 'small',
            name: 'Whisper Small (244MB)',
            model: 'Xenova/whisper-small',
            size: '244MB',
            quality: 'Excelente - Precisa'
        }
    ],
    
    // Configurações de áudio
    audio: {
        sampleRate: 16000,
        channels: 1,
        maxDuration: 30 * 60, // 30 minutos máximo
        chunkSize: 30, // segundos por chunk
    },
    
    // Configurações de transcrição
    transcription: {
        language: 'auto', // detecção automática
        task: 'transcribe', // ou 'translate'
        returnTimestamps: true,
        wordTimestamps: false,
        temperature: 0.0,
        compressionRatio: 2.4
    },
    
    // URLs dos CDNs (fallbacks)
    cdnUrls: [
        'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.6.0',
        'https://unpkg.com/@xenova/transformers@2.6.0',
        'https://cdn.skypack.dev/@xenova/transformers@2.6.0'
    ],
    
    // Configurações WASM
    wasmPaths: [
        'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.14.0/dist/',
        'https://unpkg.com/onnxruntime-web@1.14.0/dist/'
    ]
};

// Função para detectar capacidades do navegador
window.detectBrowserCapabilities = function() {
    const capabilities = {
        webAssembly: typeof WebAssembly !== 'undefined',
        sharedArrayBuffer: typeof SharedArrayBuffer !== 'undefined',
        webWorkers: typeof Worker !== 'undefined',
        audioContext: typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined',
        mediaRecorder: typeof MediaRecorder !== 'undefined',
        fileAPI: typeof FileReader !== 'undefined'
    };
    
    console.log('🔍 Capacidades do navegador:', capabilities);
    return capabilities;
};

// Função para verificar se o Whisper.js pode funcionar
window.checkWhisperCompatibility = function() {
    const caps = window.detectBrowserCapabilities();
    
    const requirements = {
        webAssembly: caps.webAssembly,
        audioContext: caps.audioContext,
        fileAPI: caps.fileAPI
    };
    
    const isCompatible = Object.values(requirements).every(Boolean);
    
    if (!isCompatible) {
        console.warn('⚠️ Alguns recursos não estão disponíveis:', requirements);
        return {
            compatible: false,
            missing: Object.entries(requirements)
                .filter(([key, value]) => !value)
                .map(([key]) => key)
        };
    }
    
    console.log('✅ Navegador compatível com Whisper.js');
    return { compatible: true, missing: [] };
};

// Auto-verificação na inicialização
document.addEventListener('DOMContentLoaded', function() {
    const compatibility = window.checkWhisperCompatibility();
    
    if (!compatibility.compatible) {
        console.error('❌ Navegador incompatível. Recursos faltando:', compatibility.missing);
        
        // Mostrar mensagem de erro na interface
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #ff4757;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 10000;
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        errorDiv.innerHTML = `
            ⚠️ <strong>Navegador Incompatível</strong><br>
            Recursos faltando: ${compatibility.missing.join(', ')}<br>
            Use Chrome, Firefox ou Edge atualizado.
        `;
        
        document.body.appendChild(errorDiv);
        
        // Remover após 10 segundos
        setTimeout(() => errorDiv.remove(), 10000);
    }
});

export default window.WHISPER_CONFIG; 