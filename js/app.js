/**
 * 🎯 CONVERSOR DE ÁUDIO - APP PRINCIPAL
 * ===================================
 * Sistema de transcrição de áudio usando Whisper.js
 * 100% client-side, offline e seguro
 * 
 * Powered by: @xenova/transformers (Whisper.js)
 * Author: Ronaldo Melo
 * GitHub: https://github.com/ronaldomelofz/conversoraudio
 */

// Importar Whisper.js via CDN (versão estável)
import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.6.0';

// Configurações globais para funcionar no navegador
env.allowRemoteModels = true;
env.allowLocalModels = false;
env.backends.onnx.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.14.0/dist/';

class AudioTranscriber {
    constructor() {
        this.transcriber = null;
        this.currentModel = 'Xenova/whisper-tiny';
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.selectedFile = null;
        this.recordedBlob = null;
        
        this.initializeUI();
        this.setupEventListeners();
    }
    
    initializeUI() {
        console.log('🎯 Inicializando Conversor de Áudio...');
        this.updateStatus('Pronto para uso!');
    }
    
    setupEventListeners() {
        // Upload de arquivo
        const fileInput = document.getElementById('fileInput');
        fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        
        // Drag and drop
        const uploadSection = document.querySelector('.upload-section');
        uploadSection.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadSection.addEventListener('dragleave', this.handleDragLeave.bind(this));
        uploadSection.addEventListener('drop', this.handleDrop.bind(this));
        
        // Mudança de modelo
        const modelSelect = document.getElementById('modelSelect');
        modelSelect.addEventListener('change', this.handleModelChange.bind(this));
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.processSelectedFile(file);
        }
    }
    
    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('dragover');
    }
    
    handleDragLeave(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('dragover');
    }
    
    handleDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.processSelectedFile(files[0]);
        }
    }
    
    processSelectedFile(file) {
        // Validar tipo de arquivo
        const allowedTypes = [
            'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/m4a',
            'audio/ogg', 'audio/flac', 'audio/aac', 'audio/webm',
            'video/mp4', 'video/webm', 'video/ogg'
        ];
        
        const fileExtension = file.name.split('.').pop().toLowerCase();
        const audioExtensions = ['mp3', 'wav', 'm4a', 'ogg', 'flac', 'aac', 'webm', 'mp4'];
        
        if (!allowedTypes.includes(file.type) && !audioExtensions.includes(fileExtension)) {
            this.showError('Formato de arquivo não suportado. Use: MP3, WAV, M4A, OGG, FLAC, AAC, WebM, MP4');
            return;
        }
        
        // Validar tamanho (máximo 100MB para melhor performance)
        const maxSize = 100 * 1024 * 1024; // 100MB
        if (file.size > maxSize) {
            this.showError(`Arquivo muito grande (${(file.size / 1024 / 1024).toFixed(1)}MB). Máximo: 100MB`);
            return;
        }
        
        this.selectedFile = file;
        this.recordedBlob = null; // Limpar gravação anterior
        
        // Atualizar UI
        const fileName = document.getElementById('fileName');
        const sizeMB = (file.size / 1024 / 1024).toFixed(2);
        fileName.textContent = `📄 ${file.name} (${sizeMB} MB)`;
        
        // Mostrar seção de transcrição
        document.getElementById('transcribeSection').style.display = 'block';
        document.getElementById('resultSection').style.display = 'none';
        
        console.log('✅ Arquivo selecionado:', file.name);
    }
    
    handleModelChange(event) {
        const modelMap = {
            'tiny': 'Xenova/whisper-tiny',
            'base': 'Xenova/whisper-base',
            'small': 'Xenova/whisper-small'
        };
        
        this.currentModel = modelMap[event.target.value] || 'Xenova/whisper-tiny';
        
        // Reset transcriber para forçar reload do modelo
        this.transcriber = null;
        console.log('🤖 Modelo alterado para:', this.currentModel);
    }
    
    async initializeTranscriber() {
        if (this.transcriber) {
            return this.transcriber;
        }
        
        try {
            this.updateLoadingText('Carregando modelo Whisper...');
            this.updateProgress(10);
            
            console.log('🤖 Inicializando transcriber com modelo:', this.currentModel);
            
            this.transcriber = await pipeline(
                'automatic-speech-recognition',
                this.currentModel,
                {
                    progress_callback: (progress) => {
                        if (progress.status === 'downloading') {
                            const percent = Math.round((progress.loaded / progress.total) * 80) + 10;
                            this.updateProgress(percent);
                            this.updateLoadingText(`Baixando modelo: ${percent}%`);
                        } else if (progress.status === 'loading') {
                            this.updateProgress(95);
                            this.updateLoadingText('Carregando modelo na memória...');
                        }
                    }
                }
            );
            
            this.updateProgress(100);
            this.updateLoadingText('Modelo carregado com sucesso!');
            
            console.log('✅ Transcriber inicializado');
            return this.transcriber;
            
        } catch (error) {
            console.error('❌ Erro ao inicializar transcriber:', error);
            throw new Error(`Erro ao carregar modelo: ${error.message}`);
        }
    }
    
    async startTranscription() {
        const audioSource = this.selectedFile || this.recordedBlob;
        
        if (!audioSource) {
            this.showError('Selecione um arquivo de áudio ou grave um áudio primeiro');
            return;
        }
        
        try {
            // Mostrar loading
            this.showLoading();
            this.updateProgress(0);
            
            // Inicializar transcriber
            await this.initializeTranscriber();
            
            // Preparar áudio
            this.updateLoadingText('Processando áudio...');
            this.updateProgress(10);
            
            const audioBuffer = await this.processAudioFile(audioSource);
            
            // Configurar opções de transcrição
            const language = document.getElementById('languageSelect').value || undefined;
            const task = document.getElementById('taskSelect').value;
            
            const options = {
                task: task,
                language: language,
                return_timestamps: true,
                chunk_length_s: 30,
                stride_length_s: 5
            };
            
            console.log('🎵 Iniciando transcrição com opções:', options);
            this.updateLoadingText('Transcrevendo áudio com IA...');
            this.updateProgress(50);
            
            const startTime = Date.now();
            
            // Executar transcrição
            const result = await this.transcriber(audioBuffer, options);
            
            const endTime = Date.now();
            const processingTime = (endTime - startTime) / 1000;
            
            this.updateProgress(100);
            
            console.log('✅ Transcrição concluída:', result);
            
            // Mostrar resultado
            this.showResult(result, {
                processingTime,
                fileSize: audioSource.size || 0,
                fileName: audioSource.name || 'Gravação',
                model: this.currentModel,
                language: language || 'auto',
                task: task
            });
            
        } catch (error) {
            console.error('❌ Erro na transcrição:', error);
            this.showError(`Erro na transcrição: ${error.message}`);
        }
    }
    
    async processAudioFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = async (event) => {
                try {
                    const arrayBuffer = event.target.result;
                    
                    // Decodificar áudio
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
                    
                    // Converter para mono se necessário
                    let audioData;
                    if (audioBuffer.numberOfChannels === 1) {
                        audioData = audioBuffer.getChannelData(0);
                    } else {
                        // Misturar canais para mono
                        const leftChannel = audioBuffer.getChannelData(0);
                        const rightChannel = audioBuffer.getChannelData(1);
                        audioData = new Float32Array(leftChannel.length);
                        
                        for (let i = 0; i < leftChannel.length; i++) {
                            audioData[i] = (leftChannel[i] + rightChannel[i]) / 2;
                        }
                    }
                    
                    // Resample para 16kHz se necessário
                    const targetSampleRate = 16000;
                    if (audioBuffer.sampleRate !== targetSampleRate) {
                        audioData = this.resampleAudio(audioData, audioBuffer.sampleRate, targetSampleRate);
                    }
                    
                    resolve(audioData);
                    
                } catch (error) {
                    reject(new Error(`Erro ao processar áudio: ${error.message}`));
                }
            };
            
            reader.onerror = () => reject(new Error('Erro ao ler arquivo'));
            reader.readAsArrayBuffer(file);
        });
    }
    
    resampleAudio(audioData, originalSampleRate, targetSampleRate) {
        if (originalSampleRate === targetSampleRate) {
            return audioData;
        }
        
        const ratio = originalSampleRate / targetSampleRate;
        const newLength = Math.round(audioData.length / ratio);
        const resampled = new Float32Array(newLength);
        
        for (let i = 0; i < newLength; i++) {
            const originalIndex = i * ratio;
            const index = Math.floor(originalIndex);
            const fraction = originalIndex - index;
            
            if (index + 1 < audioData.length) {
                resampled[i] = audioData[index] * (1 - fraction) + audioData[index + 1] * fraction;
            } else {
                resampled[i] = audioData[index];
            }
        }
        
        return resampled;
    }
    
    showResult(result, metadata) {
        this.hideLoading();
        
        const resultSection = document.getElementById('resultSection');
        const transcriptionText = document.getElementById('transcriptionText');
        const metadataGrid = document.getElementById('metadataGrid');
        
        // Preparar texto baseado no formato selecionado
        const format = document.getElementById('formatSelect').value;
        let displayText = '';
        
        if (format === 'text') {
            displayText = result.text;
        } else if (format === 'detailed' && result.chunks) {
            displayText = result.chunks.map(chunk => 
                `[${this.formatTime(chunk.timestamp[0])} - ${this.formatTime(chunk.timestamp[1])}]\n${chunk.text}`
            ).join('\n\n');
        } else if (format === 'srt' && result.chunks) {
            displayText = this.generateSRT(result.chunks);
        } else {
            displayText = result.text;
        }
        
        transcriptionText.textContent = displayText;
        
        // Calcular estatísticas
        const words = result.text.split(/\s+/).filter(word => word.length > 0).length;
        const characters = result.text.length;
        const duration = metadata.fileSize ? Math.round(metadata.fileSize / (16000 * 2)) : 0; // Estimativa
        const speed = metadata.processingTime > 0 ? (duration / metadata.processingTime).toFixed(1) : 'N/A';
        
        // Mostrar metadados
        metadataGrid.innerHTML = `
            <div class="metadata-item">
                <div class="metadata-value">${metadata.processingTime.toFixed(1)}s</div>
                <div class="metadata-label">⏱️ Tempo de Processamento</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-value">${words}</div>
                <div class="metadata-label">📝 Palavras</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-value">${characters}</div>
                <div class="metadata-label">📊 Caracteres</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-value">${speed}x</div>
                <div class="metadata-label">🚀 Velocidade</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-value">${metadata.model.split('/')[1]}</div>
                <div class="metadata-label">🤖 Modelo</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-value">${metadata.language === 'auto' ? 'Auto' : metadata.language.toUpperCase()}</div>
                <div class="metadata-label">🌍 Idioma</div>
            </div>
        `;
        
        resultSection.style.display = 'block';
        resultSection.scrollIntoView({ behavior: 'smooth' });
        
        // Salvar resultado para download
        this.lastResult = {
            text: displayText,
            metadata: metadata,
            format: format
        };
    }
    
    formatTime(seconds) {
        const h = Math.floor(seconds / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        const s = Math.floor(seconds % 60);
        const ms = Math.floor((seconds % 1) * 1000);
        
        if (h > 0) {
            return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}.${ms.toString().padStart(3, '0')}`;
        } else {
            return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}.${ms.toString().padStart(3, '0')}`;
        }
    }
    
    generateSRT(chunks) {
        return chunks.map((chunk, index) => {
            const start = this.formatSRTTime(chunk.timestamp[0]);
            const end = this.formatSRTTime(chunk.timestamp[1]);
            return `${index + 1}\n${start} --> ${end}\n${chunk.text.trim()}\n`;
        }).join('\n');
    }
    
    formatSRTTime(seconds) {
        const h = Math.floor(seconds / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        const s = Math.floor(seconds % 60);
        const ms = Math.floor((seconds % 1) * 1000);
        
        return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')},${ms.toString().padStart(3, '0')}`;
    }
    
    showError(message) {
        this.hideLoading();
        
        const resultSection = document.getElementById('resultSection');
        const transcriptionText = document.getElementById('transcriptionText');
        const resultTitle = resultSection.querySelector('.result-title');
        
        resultSection.className = 'result-section error';
        resultTitle.innerHTML = '<span>❌</span><span>Erro na Transcrição</span>';
        transcriptionText.textContent = message;
        
        document.getElementById('metadataGrid').innerHTML = '';
        resultSection.style.display = 'block';
        resultSection.scrollIntoView({ behavior: 'smooth' });
        
        console.error('❌ Erro:', message);
    }
    
    showLoading() {
        document.getElementById('loadingSection').style.display = 'block';
        document.getElementById('resultSection').style.display = 'none';
        document.getElementById('transcribeBtn').disabled = true;
    }
    
    hideLoading() {
        document.getElementById('loadingSection').style.display = 'none';
        document.getElementById('transcribeBtn').disabled = false;
    }
    
    updateLoadingText(text) {
        document.getElementById('loadingText').textContent = text;
    }
    
    updateProgress(percent) {
        document.getElementById('progressFill').style.width = `${percent}%`;
    }
    
    updateStatus(status) {
        console.log('📊 Status:', status);
    }
    
    // Funcionalidades de gravação
    async toggleRecording(event) {
        event.stopPropagation();
        
        if (this.isRecording) {
            await this.stopRecording();
        } else {
            await this.startRecording();
        }
    }
    
    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    sampleRate: 16000,
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true
                } 
            });
            
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = () => {
                const blob = new Blob(this.audioChunks, { type: 'audio/webm' });
                this.handleRecordedAudio(blob);
                
                // Parar todas as tracks
                stream.getTracks().forEach(track => track.stop());
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            
            // Atualizar UI
            const recordBtn = document.querySelector('.record-btn');
            const recordingIndicator = document.getElementById('recordingIndicator');
            
            recordBtn.textContent = '⏹️ Parar Gravação';
            recordingIndicator.style.display = 'block';
            
            console.log('🎤 Gravação iniciada');
            
        } catch (error) {
            console.error('❌ Erro ao acessar microfone:', error);
            this.showError('Erro ao acessar microfone. Verifique as permissões.');
        }
    }
    
    async stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            // Atualizar UI
            const recordBtn = document.querySelector('.record-btn');
            const recordingIndicator = document.getElementById('recordingIndicator');
            
            recordBtn.textContent = '🎤 Gravar Áudio';
            recordingIndicator.style.display = 'none';
            
            console.log('⏹️ Gravação parada');
        }
    }
    
    handleRecordedAudio(blob) {
        this.recordedBlob = blob;
        this.selectedFile = null; // Limpar arquivo anterior
        
        // Criar um arquivo virtual para o blob
        const fileName = `gravacao_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.webm`;
        this.recordedBlob.name = fileName;
        this.recordedBlob.size = blob.size;
        
        // Atualizar UI
        const fileNameEl = document.getElementById('fileName');
        const sizeMB = (blob.size / 1024 / 1024).toFixed(2);
        fileNameEl.textContent = `🎤 ${fileName} (${sizeMB} MB)`;
        
        // Mostrar seção de transcrição
        document.getElementById('transcribeSection').style.display = 'block';
        document.getElementById('resultSection').style.display = 'none';
        
        console.log('✅ Áudio gravado:', fileName);
    }
}

// Instanciar aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.audioTranscriber = new AudioTranscriber();
});

// Funções globais para os botões
window.startTranscription = function() {
    window.audioTranscriber.startTranscription();
};

window.toggleRecording = function(event) {
    window.audioTranscriber.toggleRecording(event);
};

window.copyToClipboard = function() {
    if (window.audioTranscriber.lastResult) {
        navigator.clipboard.writeText(window.audioTranscriber.lastResult.text).then(() => {
            // Feedback visual
            const btn = event.target;
            const originalText = btn.textContent;
            btn.textContent = '✅ Copiado!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        }).catch(err => {
            console.error('Erro ao copiar:', err);
            // Fallback para seleção manual
            const textArea = document.createElement('textarea');
            textArea.value = window.audioTranscriber.lastResult.text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        });
    }
};

window.downloadTranscription = function() {
    if (window.audioTranscriber.lastResult) {
        const result = window.audioTranscriber.lastResult;
        const extension = result.format === 'srt' ? 'srt' : 'txt';
        const filename = `transcricao_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.${extension}`;
        
        const blob = new Blob([result.text], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
        
        console.log('💾 Download iniciado:', filename);
    }
};

window.newTranscription = function() {
    // Reset da aplicação
    window.audioTranscriber.selectedFile = null;
    window.audioTranscriber.recordedBlob = null;
    window.audioTranscriber.lastResult = null;
    
    // Reset da UI
    document.getElementById('fileName').textContent = '';
    document.getElementById('transcribeSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('fileInput').value = '';
    
    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    console.log('🔄 Nova transcrição iniciada');
};

// Log de inicialização
console.log(`
🎯 CONVERSOR DE ÁUDIO - v1.0
============================
✨ Powered by Whisper.js
🔒 100% Offline & Seguro
🚀 Sem Limites
📱 Responsivo

GitHub: https://github.com/ronaldomelofz/conversoraudio
`);

// Service Worker registration para PWA (opcional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registrado com sucesso:', registration.scope);
            })
            .catch(registrationError => {
                console.log('SW registration failed:', registrationError);
            });
    });
} 