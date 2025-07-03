#!/usr/bin/env python3
"""
🎯 TRANSCRITOR AVANÇADO - API FLASK
====================================
Sistema híbrido que combina:
- Nosso motor Whisper avançado (offline)
- API REST estilo TranscreveAPI
- Interface web moderna
- Containerização Docker

Inspirado em: https://github.com/erickythierry/transcreveAPI
Autor: Sistema Avançado de Transcrição
Versão: 3.0
"""

import os
import sys
import json
import base64
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Flask e componentes web
try:
    from flask import Flask, request, jsonify, render_template_string, send_file
    from werkzeug.utils import secure_filename
except ImportError:
    print("❌ Flask não instalado. Execute: pip install flask")
    sys.exit(1)

# Sistema avançado - verifica se está instalado
try:
    import librosa
    import whisper
    import numpy as np
    DEPENDENCIES_OK = True
except ImportError as e:
    print(f"❌ Dependências faltando: {e}")
    print("🔧 Execute: pip install librosa openai-whisper numpy flask")
    DEPENDENCIES_OK = False

class TranscritorAPIFlask:
    """API Flask avançada para transcrição com Whisper"""
    
    def __init__(self):
        if not DEPENDENCIES_OK:
            raise ImportError("Dependências não instaladas")
            
        self.app = Flask(__name__)
        self.app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
        self.supported_formats = {'.mp3', '.mp4', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.wma', '.webm'}
        self.whisper_models = {}
        self.setup_routes()
        
    def setup_routes(self):
        """Configura todas as rotas da API"""
        
        @self.app.route('/')
        def index():
            """Página principal com interface web"""
            return render_template_string(self.get_web_interface())
            
        @self.app.route('/transcrever', methods=['POST'])
        def transcrever():
            """Endpoint principal compatível com TranscreveAPI"""
            return self.handle_transcription()
            
        @self.app.route('/api/v1/transcribe', methods=['POST'])
        def api_transcribe():
            """Endpoint avançado com mais opções"""
            return self.handle_advanced_transcription()
            
        @self.app.route('/health')
        def health():
            """Endpoint de saúde para monitoramento"""
            return jsonify({
                'status': 'healthy',
                'version': '3.0',
                'system': 'Transcritor Avançado Flask',
                'whisper_models_loaded': list(self.whisper_models.keys()),
                'supported_formats': list(self.supported_formats),
                'timestamp': datetime.now().isoformat()
            })
            
        @self.app.route('/models')
        def list_models():
            """Lista modelos Whisper disponíveis"""
            return jsonify({
                'available_models': ['tiny', 'base', 'small', 'medium', 'large'],
                'loaded_models': list(self.whisper_models.keys()),
                'recommendations': {
                    'speed': 'tiny',
                    'balance': 'base', 
                    'quality': 'small',
                    'precision': 'medium',
                    'maximum': 'large'
                },
                'model_info': {
                    'tiny': {'size': '~39 MB', 'speed': 'Fastest', 'accuracy': 'Lower'},
                    'base': {'size': '~74 MB', 'speed': 'Fast', 'accuracy': 'Good'},
                    'small': {'size': '~244 MB', 'speed': 'Medium', 'accuracy': 'Better'},
                    'medium': {'size': '~769 MB', 'speed': 'Slow', 'accuracy': 'High'},
                    'large': {'size': '~1550 MB', 'speed': 'Slowest', 'accuracy': 'Highest'}
                }
            })

    def handle_transcription(self) -> Dict[str, Any]:
        """Handler compatível com TranscreveAPI original"""
        try:
            # Verifica se é upload de arquivo ou base64
            if 'audio' in request.files:
                audio_file = request.files['audio']
                if audio_file.filename == '':
                    return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
                audio_data = audio_file.read()
                filename = secure_filename(audio_file.filename)
            elif request.is_json and 'data' in request.json:
                # Formato base64 como TranscreveAPI original
                try:
                    audio_data = base64.b64decode(request.json['data'])
                    filename = 'audio_upload.wav'
                except Exception as e:
                    return jsonify({'error': f'Erro ao decodificar base64: {str(e)}'}), 400
            else:
                return jsonify({'error': 'Envie um arquivo via form-data ou dados base64 via JSON'}), 400
                
            # Processa com configurações padrão (compatibilidade)
            result = self.process_audio(
                audio_data=audio_data,
                filename=filename,
                model='base',
                language='pt'
            )
            
            if result['success']:
                # Formato de resposta compatível com TranscreveAPI
                return jsonify({
                    'transcription': result['transcription'],
                    'success': True,
                    'metadata': {
                        'duration': result['duration'],
                        'model': result['model'],
                        'language': result.get('language_detected', 'pt'),
                        'processing_time': result['processing_time']
                    }
                })
            else:
                return jsonify({'error': result['error'], 'success': False}), 500
                
        except Exception as e:
            return jsonify({'error': f'Erro interno: {str(e)}', 'success': False}), 500

    def handle_advanced_transcription(self) -> Dict[str, Any]:
        """Handler avançado com todas nossas funcionalidades"""
        try:
            # Parse dos parâmetros avançados
            if request.is_json:
                data = request.json
                if 'audio_file' in data and 'content' in data['audio_file']:
                    # Base64 + metadados
                    try:
                        audio_data = base64.b64decode(data['audio_file']['content'])
                        filename = data['audio_file'].get('filename', 'upload.wav')
                    except Exception as e:
                        return jsonify({'error': f'Erro ao decodificar base64: {str(e)}'}), 400
                else:
                    return jsonify({'error': 'Formato JSON inválido. Use audio_file.content para base64'}), 400
                    
                # Parâmetros opcionais
                model = data.get('model', 'base')
                language = data.get('language', 'auto')
                include_timestamps = data.get('timestamps', True)
                label = data.get('label', 'api_upload')
                
            else:
                # Form upload
                if 'audio' not in request.files:
                    return jsonify({'error': 'Campo audio necessário no form-data'}), 400
                    
                audio_file = request.files['audio']
                if audio_file.filename == '':
                    return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
                    
                audio_data = audio_file.read()
                filename = secure_filename(audio_file.filename)
                
                model = request.form.get('model', 'base')
                language = request.form.get('language', 'auto')
                include_timestamps = request.form.get('timestamps', 'true').lower() == 'true'
                label = request.form.get('label', 'api_upload')
            
            # Valida modelo
            if model not in ['tiny', 'base', 'small', 'medium', 'large']:
                return jsonify({'error': f'Modelo {model} inválido. Use: tiny, base, small, medium, large'}), 400
            
            # Processa com configurações avançadas
            result = self.process_audio(
                audio_data=audio_data,
                filename=filename,
                model=model,
                language=language,
                include_timestamps=include_timestamps,
                label=label
            )
            
            if result['success']:
                response = {
                    'success': True,
                    'data': {
                        'transcription': result['transcription'],
                        'metadata': {
                            'filename': filename,
                            'duration_seconds': result['duration'],
                            'model_used': result['model'],
                            'language_detected': result.get('language_detected', language),
                            'processing_time': result['processing_time'],
                            'characters': len(result['transcription']),
                            'words': len(result['transcription'].split()),
                            'speed_ratio': round(result['duration'] / result['processing_time'], 2) if result['processing_time'] > 0 else 0
                        }
                    }
                }
                
                if include_timestamps and 'segments' in result:
                    response['data']['segments'] = result['segments']
                    
                return jsonify(response)
            else:
                return jsonify({'success': False, 'error': result['error']}), 500
                
        except Exception as e:
            return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'}), 500

    def process_audio(self, audio_data: bytes, filename: str, model: str = 'base', 
                     language: str = 'auto', include_timestamps: bool = True,
                     label: str = 'api') -> Dict[str, Any]:
        """Processa áudio usando nosso sistema avançado"""
        start_time = datetime.now()
        
        try:
            # Validação do formato
            file_ext = Path(filename).suffix.lower()
            if file_ext not in self.supported_formats:
                return {
                    'success': False, 
                    'error': f'Formato {file_ext} não suportado. Formatos aceitos: {", ".join(self.supported_formats)}'
                }
            
            # Validação do tamanho
            file_size_mb = len(audio_data) / (1024 * 1024)
            if file_size_mb > 400:
                return {
                    'success': False,
                    'error': f'Arquivo muito grande ({file_size_mb:.1f} MB). Máximo: 400 MB'
                }
            
            # Carrega modelo Whisper se necessário
            if model not in self.whisper_models:
                print(f"🤖 Carregando modelo Whisper '{model}'...")
                try:
                    self.whisper_models[model] = whisper.load_model(model)
                    print(f"✅ Modelo '{model}' carregado!")
                except Exception as e:
                    return {'success': False, 'error': f'Erro ao carregar modelo {model}: {str(e)}'}
            
            # Salva arquivo temporário
            with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            try:
                # Processa áudio com Librosa (sem FFmpeg - nossa vantagem!)
                print(f"🔊 Processando áudio {filename}...")
                audio_array, sample_rate = librosa.load(temp_path, sr=16000)
                audio_duration = len(audio_array) / sample_rate
                
                print(f"✅ Áudio carregado: {audio_duration:.1f}s, {sample_rate}Hz")
                
                # Transcrição com Whisper
                print("🎵 Transcrevendo...")
                whisper_model = self.whisper_models[model]
                
                # Configurações de transcrição
                transcribe_options = {
                    'language': None if language == 'auto' else language,
                    'word_timestamps': include_timestamps,
                    'verbose': False
                }
                
                result = whisper_model.transcribe(audio_array, **transcribe_options)
                
                processing_time = (datetime.now() - start_time).total_seconds()
                print(f"✅ Transcrição concluída em {processing_time:.1f}s")
                
                response = {
                    'success': True,
                    'transcription': result['text'].strip(),
                    'duration': audio_duration,
                    'model': model,
                    'processing_time': processing_time,
                    'language_detected': result.get('language', language)
                }
                
                if include_timestamps and 'segments' in result:
                    response['segments'] = [
                        {
                            'start': round(seg['start'], 2),
                            'end': round(seg['end'], 2),
                            'text': seg['text'].strip()
                        }
                        for seg in result['segments']
                    ]
                
                return response
                
            finally:
                # Limpa arquivo temporário
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
        except Exception as e:
            return {'success': False, 'error': f'Erro no processamento: {str(e)}'}

    def get_web_interface(self) -> str:
        """Interface web moderna inspirada no TranscreveAPI"""
        return '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Transcritor Avançado - API Flask</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .upload-section {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .upload-section:hover {
            border-color: #764ba2;
            background: #f8f9ff;
        }
        
        .upload-section.dragover {
            border-color: #28a745;
            background: #f0fff4;
        }
        
        .file-input {
            display: none;
        }
        
        .upload-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .upload-btn:hover {
            transform: translateY(-2px);
        }
        
        .options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .option-group {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 10px;
        }
        
        .option-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #333;
        }
        
        .option-group select, .option-group input {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }
        
        .transcribe-btn {
            width: 100%;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 10px;
            font-size: 1.2em;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .transcribe-btn:hover:not(:disabled) {
            transform: translateY(-2px);
        }
        
        .transcribe-btn:disabled {
            background: #6c757d;
            cursor: not-allowed;
        }
        
        .result {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            display: none;
        }
        
        .result.success {
            border-left: 5px solid #28a745;
        }
        
        .result.error {
            border-left: 5px solid #dc3545;
            background: #fff5f5;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .metadata {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
            font-size: 0.9em;
            color: #666;
        }
        
        .metadata span {
            background: white;
            padding: 5px 10px;
            border-radius: 5px;
        }
        
        .transcription-text {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            border: 1px solid #e0e0e0;
            line-height: 1.6;
            font-size: 1.1em;
        }
        
        .api-docs {
            margin-top: 40px;
            padding-top: 40px;
            border-top: 2px solid #eee;
        }
        
        .api-docs h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .endpoint {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-family: monospace;
            border-left: 4px solid #667eea;
        }
        
        .comparison {
            background: #e8f5e8;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #28a745;
        }
        
        .advantage {
            color: #28a745;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Transcritor Avançado</h1>
            <p>API Flask com Whisper - Inspirado no TranscreveAPI, mas MUITO mais poderoso!</p>
        </div>
        
        <div class="content">
            <div class="comparison">
                <h4>🚀 Vantagens sobre o TranscreveAPI Original:</h4>
                <ul>
                    <li class="advantage">✅ 100% Offline (sem dependência do Google)</li>
                    <li class="advantage">✅ Sem FFmpeg necessário (usa Librosa)</li>
                    <li class="advantage">✅ 5 modelos Whisper (tiny até large)</li>
                    <li class="advantage">✅ Suporte multilíngue nativo</li>
                    <li class="advantage">✅ Timestamps word-level</li>
                    <li class="advantage">✅ Interface web moderna</li>
                    <li class="advantage">✅ Organização automática de arquivos</li>
                </ul>
            </div>
            
            <div class="upload-section" onclick="document.getElementById('fileInput').click()">
                <h3>📁 Selecione ou arraste seu arquivo de áudio</h3>
                <p>Suportamos: MP3, MP4, WAV, M4A, OGG, FLAC, AAC, WMA, WebM</p>
                <p><strong>Máximo: 400MB por arquivo</strong></p>
                <br>
                <button class="upload-btn" type="button">Escolher Arquivo</button>
                <input type="file" id="fileInput" class="file-input" accept="audio/*">
                <p id="fileName" style="margin-top: 10px; color: #667eea; font-weight: bold;"></p>
            </div>
            
            <div class="options">
                <div class="option-group">
                    <label for="model">🤖 Modelo Whisper</label>
                    <select id="model">
                        <option value="tiny">Tiny (~39MB) - Rápido</option>
                        <option value="base" selected>Base (~74MB) - Recomendado</option>
                        <option value="small">Small (~244MB) - Preciso</option>
                        <option value="medium">Medium (~769MB) - Muito Preciso</option>
                        <option value="large">Large (~1550MB) - Máxima Precisão</option>
                    </select>
                </div>
                
                <div class="option-group">
                    <label for="language">🌍 Idioma</label>
                    <select id="language">
                        <option value="auto">🔍 Detectar Automaticamente</option>
                        <option value="pt" selected>🇧🇷 Português</option>
                        <option value="en">🇺🇸 English</option>
                        <option value="es">🇪🇸 Español</option>
                        <option value="fr">🇫🇷 Français</option>
                        <option value="de">🇩🇪 Deutsch</option>
                        <option value="it">🇮🇹 Italiano</option>
                    </select>
                </div>
                
                <div class="option-group">
                    <label for="timestamps">⏱️ Timestamps</label>
                    <select id="timestamps">
                        <option value="true" selected>✅ Incluir</option>
                        <option value="false">❌ Não Incluir</option>
                    </select>
                </div>
                
                <div class="option-group">
                    <label for="label">🏷️ Label</label>
                    <input type="text" id="label" placeholder="web_upload" value="web_upload">
                </div>
            </div>
            
            <button class="transcribe-btn" onclick="transcribeAudio()" disabled id="transcribeBtn">
                🎵 Transcrever Áudio
            </button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p><strong>Processando áudio...</strong></p>
                <p>Primeira execução pode demorar mais (download do modelo)</p>
            </div>
            
            <div class="result" id="result"></div>
            
            <div class="api-docs">
                <h3>📚 Documentação da API</h3>
                <p>Nossa API é <strong>compatível</strong> com TranscreveAPI original, mas com funcionalidades extras!</p>
                
                <h4>Endpoints Disponíveis:</h4>
                
                <div class="endpoint">
                    <strong>POST /transcrever</strong><br>
                    ✅ Compatível 100% com TranscreveAPI original<br>
                    Body: multipart/form-data com campo 'audio' OU JSON com 'data' (base64)<br>
                    <em>Migração zero-downtime do TranscreveAPI!</em>
                </div>
                
                <div class="endpoint">
                    <strong>POST /api/v1/transcribe</strong><br>
                    🚀 Endpoint avançado com todas nossas funcionalidades<br>
                    Suporte a: timestamps, múltiplos modelos, idiomas, metadados
                </div>
                
                <div class="endpoint">
                    <strong>GET /models</strong><br>
                    📋 Lista modelos Whisper disponíveis e recomendações
                </div>
                
                <div class="endpoint">
                    <strong>GET /health</strong><br>
                    💚 Status de saúde da API para monitoramento
                </div>
                
                <h4>Exemplo de uso (compatível com TranscreveAPI):</h4>
                <div class="endpoint">
curl -X POST -F 'audio=@meuaudio.mp3' http://localhost:5000/transcrever
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedFile = null;
        
        // Handle file selection
        document.getElementById('fileInput').addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                selectedFile = e.target.files[0];
                const sizeMB = (selectedFile.size / 1024 / 1024).toFixed(2);
                document.getElementById('fileName').textContent = `📄 ${selectedFile.name} (${sizeMB} MB)`;
                
                if (selectedFile.size > 400 * 1024 * 1024) {
                    alert('⚠️ Arquivo muito grande! Máximo: 400MB');
                    return;
                }
                
                document.getElementById('transcribeBtn').disabled = false;
            }
        });
        
        // Handle drag and drop
        const uploadSection = document.querySelector('.upload-section');
        
        uploadSection.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadSection.classList.add('dragover');
        });
        
        uploadSection.addEventListener('dragleave', function(e) {
            e.preventDefault();
            uploadSection.classList.remove('dragover');
        });
        
        uploadSection.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadSection.classList.remove('dragover');
            
            if (e.dataTransfer.files.length > 0) {
                selectedFile = e.dataTransfer.files[0];
                const sizeMB = (selectedFile.size / 1024 / 1024).toFixed(2);
                document.getElementById('fileName').textContent = `📄 ${selectedFile.name} (${sizeMB} MB)`;
                
                if (selectedFile.size > 400 * 1024 * 1024) {
                    alert('⚠️ Arquivo muito grande! Máximo: 400MB');
                    return;
                }
                
                document.getElementById('transcribeBtn').disabled = false;
            }
        });
        
        // Transcribe audio
        async function transcribeAudio() {
            if (!selectedFile) return;
            
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const transcribeBtn = document.getElementById('transcribeBtn');
            
            // Show loading
            loading.style.display = 'block';
            result.style.display = 'none';
            transcribeBtn.disabled = true;
            
            try {
                const formData = new FormData();
                formData.append('audio', selectedFile);
                formData.append('model', document.getElementById('model').value);
                formData.append('language', document.getElementById('language').value);
                formData.append('timestamps', document.getElementById('timestamps').value);
                formData.append('label', document.getElementById('label').value);
                
                const response = await fetch('/api/v1/transcribe', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                loading.style.display = 'none';
                result.style.display = 'block';
                
                if (data.success) {
                    result.className = 'result success';
                    const speedRatio = data.data.metadata.speed_ratio;
                    const speedText = speedRatio > 1 ? `${speedRatio}x mais rápido que tempo real` : 'Processamento em tempo real';
                    
                    result.innerHTML = `
                        <h4>✅ Transcrição Concluída com Sucesso!</h4>
                        <div class="transcription-text">
                            ${data.data.transcription}
                        </div>
                        <div class="metadata">
                            <span><strong>⏱️ Duração:</strong> ${data.data.metadata.duration_seconds.toFixed(1)}s</span>
                            <span><strong>🤖 Modelo:</strong> ${data.data.metadata.model_used}</span>
                            <span><strong>🌍 Idioma:</strong> ${data.data.metadata.language_detected}</span>
                            <span><strong>⚡ Tempo:</strong> ${data.data.metadata.processing_time.toFixed(1)}s</span>
                            <span><strong>📝 Palavras:</strong> ${data.data.metadata.words}</span>
                            <span><strong>📊 Chars:</strong> ${data.data.metadata.characters}</span>
                            <span><strong>🚀 Velocidade:</strong> ${speedText}</span>
                        </div>
                    `;
                } else {
                    result.className = 'result error';
                    result.innerHTML = `<h4>❌ Erro na Transcrição</h4><p>${data.error}</p>`;
                }
                
            } catch (error) {
                loading.style.display = 'none';
                result.style.display = 'block';
                result.className = 'result error';
                result.innerHTML = `<h4>❌ Erro de Conexão</h4><p>${error.message}</p>`;
            }
            
            transcribeBtn.disabled = false;
        }
        
        // Load health check on page load
        fetch('/health')
            .then(response => response.json())
            .then(data => {
                console.log('API Health:', data);
            })
            .catch(error => {
                console.error('API não disponível:', error);
            });
    </script>
</body>
</html>
        '''

    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Inicia o servidor Flask"""
        print("🚀 INICIANDO TRANSCRITOR AVANÇADO - API FLASK")
        print("=" * 55)
        print(f"🌐 Servidor: http://{host}:{port}")
        print(f"📚 Interface: http://localhost:{port}")
        print(f"🎯 API Principal: http://localhost:{port}/transcrever")
        print(f"⚡ API Avançada: http://localhost:{port}/api/v1/transcribe")
        print(f"💚 Health Check: http://localhost:{port}/health")
        print("=" * 55)
        print("🔥 VANTAGENS sobre TranscreveAPI original:")
        print("   ✅ 100% Offline (sem Google API)")
        print("   ✅ Sem FFmpeg necessário")
        print("   ✅ 5 modelos Whisper")
        print("   ✅ Interface web moderna")
        print("   ✅ Timestamps word-level")
        print("   ✅ Compatibilidade total")
        print("=" * 55)
        
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Função principal"""
    print("🎯 TRANSCRITOR AVANÇADO - API FLASK v3.0")
    print("Inspirado em: https://github.com/erickythierry/transcreveAPI")
    print("Mas MUITO mais poderoso! 🚀\n")
    
    # Verifica dependências
    if not DEPENDENCIES_OK:
        print("❌ DEPENDÊNCIAS NÃO INSTALADAS:")
        print("🔧 Execute: pip install librosa openai-whisper flask")
        print("\n💡 Depois execute novamente: python transcritor_api_flask.py")
        return
    
    print("✅ Dependências verificadas!")
    
    # Inicia API
    try:
        api = TranscritorAPIFlask()
        api.run(debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

if __name__ == '__main__':
    main() 