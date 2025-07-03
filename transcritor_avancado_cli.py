#!/usr/bin/env python3
"""
🎯 TRANSCRITOR AVANÇADO COM CLI
Versão melhorada inspirada nas melhores práticas de projetos GitHub
Mantém nossa abordagem sem FFmpeg + funcionalidades CLI profissionais
Autor: Sistema de Transcrição Inteligente
Data: 2025
"""

import os
import sys
import time
import argparse
import traceback
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Configurações padrão
FORMATOS_SUPORTADOS = ['.mp3', '.mp4', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.wma', '.webm']
MODELOS_WHISPER = ['tiny', 'base', 'small', 'medium', 'large']
DIRETORIO_SAIDA_PADRAO = "transcricoes"

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias = {'librosa': False, 'whisper': False, 'numpy': False}
    
    try:
        import librosa
        dependencias['librosa'] = True
    except ImportError:
        pass
    
    try:
        import whisper
        dependencias['whisper'] = True
    except ImportError:
        pass
    
    try:
        import numpy as np
        dependencias['numpy'] = True
    except ImportError:
        pass
    
    todas_ok = all(dependencias.values())
    
    if not todas_ok:
        print("❌ DEPENDÊNCIAS FALTANDO:")
        for dep, ok in dependencias.items():
            status = "✅" if ok else "❌"
            print(f"  {status} {dep}")
        
        print("\n🔧 Para instalar as dependências:")
        print("pip install librosa openai-whisper numpy")
        return False
    
    print("✅ Todas as dependências verificadas!")
    return True

def verificar_arquivo(caminho_arquivo: str) -> Dict:
    """Verifica se o arquivo existe e é válido"""
    resultado = {
        'valido': False,
        'caminho': caminho_arquivo,
        'tamanho_mb': 0,
        'extensao': '',
        'erro': ''
    }
    
    if not os.path.exists(caminho_arquivo):
        resultado['erro'] = f"Arquivo não encontrado: {caminho_arquivo}"
        return resultado
    
    caminho = Path(caminho_arquivo)
    extensao = caminho.suffix.lower()
    
    if extensao not in FORMATOS_SUPORTADOS:
        resultado['erro'] = f"Formato não suportado: {extensao}. Suportados: {', '.join(FORMATOS_SUPORTADOS)}"
        return resultado
    
    tamanho_bytes = os.path.getsize(caminho_arquivo)
    tamanho_mb = tamanho_bytes / (1024 * 1024)
    
    resultado.update({
        'valido': True,
        'tamanho_mb': tamanho_mb,
        'extensao': extensao,
        'tamanho_bytes': tamanho_bytes
    })
    
    return resultado

def criar_diretorio_saida(diretorio: str, label: str = "") -> Path:
    """Cria diretório de saída organizado"""
    if label:
        diretorio_final = Path(diretorio) / label
    else:
        diretorio_final = Path(diretorio)
    
    diretorio_final.mkdir(parents=True, exist_ok=True)
    return diretorio_final

def gerar_nome_arquivo_saida(arquivo_original: str, label: str, diretorio_saida: Path) -> str:
    """Gera nome único para arquivo de saída, evitando sobrescrever"""
    nome_base = Path(arquivo_original).stem
    
    if label:
        nome_arquivo = f"{nome_base}_{label}_transcricao.txt"
    else:
        nome_arquivo = f"{nome_base}_transcricao.txt"
    
    caminho_completo = diretorio_saida / nome_arquivo
    
    # Evitar sobrescrever arquivos existentes
    contador = 1
    while caminho_completo.exists():
        if label:
            nome_arquivo = f"{nome_base}_{label}_transcricao_{contador}.txt"
        else:
            nome_arquivo = f"{nome_base}_transcricao_{contador}.txt"
        caminho_completo = diretorio_saida / nome_arquivo
        contador += 1
    
    return str(caminho_completo)

def estimar_tempo_processamento(tamanho_mb: float, modelo: str) -> Dict:
    """Estima tempo de processamento baseado no tamanho do arquivo e modelo"""
    # Estimativas baseadas em testes (em minutos por MB)
    fatores = {
        'tiny': 0.08,
        'base': 0.15,
        'small': 0.35,
        'medium': 0.7,
        'large': 1.4
    }
    
    fator = fatores.get(modelo, 0.15)
    tempo_estimado = tamanho_mb * fator
    
    return {
        'minutos': tempo_estimado,
        'segundos': tempo_estimado * 60,
        'humano': f"{tempo_estimado:.1f} min" if tempo_estimado >= 1 else f"{tempo_estimado*60:.0f}s"
    }

def transcrever_audio_avancado(
    arquivo: str,
    modelo: str = "base",
    diretorio_saida: str = DIRETORIO_SAIDA_PADRAO,
    label: str = "",
    idioma: str = "pt",
    incluir_timestamps: bool = True,
    temperatura: float = 0.0,
    verboso: bool = True
) -> Optional[Dict]:
    """
    Função principal de transcrição com funcionalidades avançadas
    """
    
    if verboso:
        print("🎯 TRANSCRITOR AVANÇADO COM CLI")
        print("=" * 70)
        print(f"📁 Arquivo: {arquivo}")
        print(f"🤖 Modelo: {modelo}")
        print(f"🌍 Idioma: {idioma}")
        print(f"📂 Saída: {diretorio_saida}")
        if label:
            print(f"🏷️  Label: {label}")
        print("=" * 70)
    
    try:
        import librosa
        import whisper
        import numpy as np
        
        # Verificar arquivo
        verificacao = verificar_arquivo(arquivo)
        if not verificacao['valido']:
            print(f"❌ {verificacao['erro']}")
            return None
        
        if verboso:
            print(f"✅ Arquivo válido:")
            print(f"  📊 Tamanho: {verificacao['tamanho_mb']:.2f} MB")
            print(f"  📋 Formato: {verificacao['extensao']}")
        
        # Estimar tempo
        estimativa = estimar_tempo_processamento(verificacao['tamanho_mb'], modelo)
        if verboso:
            print(f"  ⏱️  Estimativa: {estimativa['humano']}")
        
        # Criar diretório de saída
        dir_saida = criar_diretorio_saida(diretorio_saida, label)
        arquivo_saida = gerar_nome_arquivo_saida(arquivo, label, dir_saida)
        
        if verboso:
            print(f"\n🤖 Carregando modelo Whisper '{modelo}'...")
        
        # Carregar modelo
        model = whisper.load_model(modelo)
        if verboso:
            print("✅ Modelo carregado!")
        
        # Processar áudio
        if verboso:
            print(f"\n🔊 Processando áudio...")
        
        audio_data, sr = librosa.load(arquivo, sr=16000)
        duracao = len(audio_data) / sr
        
        # Normalizar para Whisper
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
        audio_data = np.clip(audio_data, -1.0, 1.0)
        
        if verboso:
            print(f"✅ Áudio processado:")
            print(f"  📊 Duração: {duracao:.1f}s ({duracao/60:.1f} min)")
            print(f"  📊 Taxa: {sr} Hz")
            print(f"  📊 Amostras: {len(audio_data):,}")
        
        # Transcrever
        if verboso:
            print(f"\n🎵 Transcrevendo...")
            print(f"⏳ Aguarde ~{estimativa['humano']}")
        
        inicio = time.time()
        
        # Configurar opções de transcrição
        opcoes = {
            'language': idioma if idioma != 'auto' else None,
            'fp16': False,
            'verbose': False,
            'temperature': temperatura
        }
        
        if incluir_timestamps:
            opcoes['word_timestamps'] = True
        
        resultado = model.transcribe(audio_data, **opcoes)
        
        fim = time.time()
        duracao_processamento = fim - inicio
        
        # Extrair dados
        texto = resultado["text"]
        segmentos = resultado.get("segments", [])
        idioma_detectado = resultado.get("language", "desconhecido")
        
        # Estatísticas
        palavras = len(texto.split())
        chars = len(texto)
        velocidade = duracao / duracao_processamento if duracao_processamento > 0 else 0
        
        if verboso:
            print(f"\n{'='*70}")
            print("🎉 TRANSCRIÇÃO CONCLUÍDA!")
            print(f"{'='*70}")
            print(f"⏱️  Tempo: {duracao_processamento:.1f}s ({duracao_processamento/60:.1f} min)")
            print(f"🎵 Áudio: {duracao:.1f}s ({duracao/60:.1f} min)")
            print(f"⚡ Velocidade: {velocidade:.1f}x tempo real")
            print(f"🌍 Idioma detectado: {idioma_detectado}")
            print(f"📝 Caracteres: {chars:,}")
            print(f"🔤 Palavras: {palavras:,}")
        
        # Salvar resultado
        salvar_transcricao_completa(
            arquivo_saida, arquivo, modelo, texto, segmentos,
            {
                'duracao_audio': duracao,
                'tempo_processamento': duracao_processamento,
                'velocidade': velocidade,
                'palavras': palavras,
                'caracteres': chars,
                'idioma_detectado': idioma_detectado,
                'tamanho_arquivo_mb': verificacao['tamanho_mb']
            },
            label, incluir_timestamps
        )
        
        if verboso:
            print(f"\n📂 Resultado salvo em:")
            print(f"   {arquivo_saida}")
            
            # Prévia
            print(f"\n📖 PRÉVIA (primeiros 300 chars):")
            print("=" * 50)
            preview = texto[:300] + "..." if len(texto) > 300 else texto
            print(preview)
            print("=" * 50)
        
        return {
            'sucesso': True,
            'texto': texto,
            'arquivo_saida': arquivo_saida,
            'estatisticas': {
                'duracao_audio': duracao,
                'tempo_processamento': duracao_processamento,
                'velocidade': velocidade,
                'palavras': palavras,
                'caracteres': chars,
                'idioma_detectado': idioma_detectado
            }
        }
        
    except Exception as e:
        print(f"\n❌ ERRO NA TRANSCRIÇÃO:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        if verboso:
            print(f"\nDetalhes:")
            print(traceback.format_exc())
        return None

def salvar_transcricao_completa(arquivo_saida, arquivo_original, modelo, texto, segmentos, stats, label, incluir_timestamps):
    """Salva transcrição com metadados completos"""
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        # Cabeçalho
        f.write("🎯 TRANSCRIÇÃO AVANÇADA COM CLI\n")
        f.write("=" * 80 + "\n")
        f.write(f"📁 Arquivo Original: {arquivo_original}\n")
        f.write(f"🤖 Modelo Whisper: {modelo}\n")
        f.write(f"🌍 Idioma Detectado: {stats['idioma_detectado']}\n")
        if label:
            f.write(f"🏷️  Label: {label}\n")
        f.write(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"⏱️  Tempo Processamento: {stats['tempo_processamento']:.1f}s ({stats['tempo_processamento']/60:.1f} min)\n")
        f.write(f"🎵 Duração Áudio: {stats['duracao_audio']:.1f}s ({stats['duracao_audio']/60:.1f} min)\n")
        f.write(f"⚡ Velocidade: {stats['velocidade']:.1f}x tempo real\n")
        f.write(f"📊 Arquivo: {stats['tamanho_arquivo_mb']:.2f} MB\n")
        f.write(f"📊 Estatísticas: {stats['caracteres']:,} chars, {stats['palavras']:,} palavras\n")
        f.write("=" * 80 + "\n\n")
        
        # Transcrição principal
        f.write("TRANSCRIÇÃO COMPLETA:\n")
        f.write("-" * 60 + "\n")
        f.write(texto.strip())
        f.write("\n\n")
        
        # Timestamps se solicitado
        if incluir_timestamps and segmentos:
            f.write("TRANSCRIÇÃO COM TIMESTAMPS:\n")
            f.write("-" * 60 + "\n")
            for segmento in segmentos:
                inicio = segmento.get('start', 0)
                fim = segmento.get('end', 0)
                texto_seg = segmento.get('text', '').strip()
                
                min_i, seg_i = divmod(int(inicio), 60)
                min_f, seg_f = divmod(int(fim), 60)
                
                f.write(f"[{min_i:02d}:{seg_i:02d} - {min_f:02d}:{seg_f:02d}] {texto_seg}\n")
        
        f.write(f"\n" + "=" * 80 + "\n")
        f.write("Gerado por: Transcritor Avançado CLI v2.0\n")

def criar_parser():
    """Cria parser de argumentos CLI"""
    parser = argparse.ArgumentParser(
        description="🎯 Transcritor Avançado de Áudio para Texto",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python transcritor_avancado_cli.py --file audio.mp3
  python transcritor_avancado_cli.py --file video.mp4 --model small --label reuniao
  python transcritor_avancado_cli.py --file podcast.wav --out-dir ./transcricoes --language en
  python transcritor_avancado_cli.py --file aula.m4a --label aula01 --no-timestamps
  python transcritor_avancado_cli.py --list-models
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        help='Caminho do arquivo de áudio/vídeo para transcrever'
    )
    
    parser.add_argument(
        '--model', '-m',
        choices=MODELOS_WHISPER,
        default='base',
        help='Modelo Whisper a usar (padrão: base)'
    )
    
    parser.add_argument(
        '--label', '-l',
        default='',
        help='Label/identificador para organizar a saída'
    )
    
    parser.add_argument(
        '--out-dir', '-o',
        default=DIRETORIO_SAIDA_PADRAO,
        help=f'Diretório de saída (padrão: {DIRETORIO_SAIDA_PADRAO})'
    )
    
    parser.add_argument(
        '--language', '-lang',
        default='pt',
        help='Idioma do áudio (pt, en, es, etc. ou "auto" para detectar - padrão: pt)'
    )
    
    parser.add_argument(
        '--no-timestamps',
        action='store_true',
        help='Não incluir timestamps na transcrição'
    )
    
    parser.add_argument(
        '--temperature', '-t',
        type=float,
        default=0.0,
        help='Temperatura para sampling (0.0-1.0, padrão: 0.0)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Modo silencioso (menos output)'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='Lista modelos disponíveis e sai'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Transcritor Avançado CLI v2.0'
    )
    
    return parser

def main():
    """Função principal com CLI"""
    parser = criar_parser()
    args = parser.parse_args()
    
    # Listar modelos se solicitado
    if args.list_models:
        print("🤖 MODELOS WHISPER DISPONÍVEIS:")
        print("=" * 50)
        descrições = {
            'tiny': 'Mais rápido, menor precisão (~39 MB)',
            'base': 'Equilibrado, recomendado (~74 MB)',
            'small': 'Preciso, velocidade razoável (~244 MB)',
            'medium': 'Muito preciso (~769 MB)',
            'large': 'Máxima precisão (~1550 MB)'
        }
        
        for modelo in MODELOS_WHISPER:
            desc = descrições.get(modelo, '')
            print(f"  {modelo:<8} - {desc}")
        
        print("\n💡 DICA: Use 'base' para maioria dos casos")
        print("💡 DICA: Use 'small' ou 'medium' para máxima precisão")
        return
    
    # Verificar se arquivo foi especificado
    if not args.file:
        print("❌ ERRO: Especifique um arquivo com --file")
        print("Use --help para ver todas as opções")
        sys.exit(1)
    
    # Verificar dependências
    if not verificar_dependencias():
        sys.exit(1)
    
    # Executar transcrição
    resultado = transcrever_audio_avancado(
        arquivo=args.file,
        modelo=args.model,
        diretorio_saida=args.out_dir,
        label=args.label,
        idioma=args.language,
        incluir_timestamps=not args.no_timestamps,
        temperatura=args.temperature,
        verboso=not args.quiet
    )
    
    if resultado and resultado['sucesso']:
        if not args.quiet:
            print(f"\n🎉 SUCESSO TOTAL!")
            print(f"📂 Arquivo: {resultado['arquivo_saida']}")
        sys.exit(0)
    else:
        if not args.quiet:
            print(f"\n💔 FALHA NA TRANSCRIÇÃO")
        sys.exit(1)

if __name__ == "__main__":
    main() 