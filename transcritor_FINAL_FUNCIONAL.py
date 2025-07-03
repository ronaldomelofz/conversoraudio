"""
🎯 TRANSCRITOR FINAL FUNCIONAL - SEM FFMPEG
Esta é a solução definitiva que contorna todos os problemas de FFmpeg
Passa os dados de áudio diretamente do Librosa para o Whisper
"""

import os
import time
import traceback
import numpy as np
from pathlib import Path

def verificar_dependencias():
    """Verifica dependências essenciais"""
    try:
        import librosa
        import whisper
        import numpy as np
        print("✅ Todas as dependências OK!")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def transcrever_audio_sem_ffmpeg(arquivo_mp3, modelo="base"):
    """
    Transcrição sem usar FFmpeg - passa dados diretamente para Whisper
    """
    
    print("🎯 TRANSCRITOR FINAL FUNCIONAL")
    print("=" * 60)
    print(f"📁 Arquivo: {arquivo_mp3}")
    print(f"🤖 Modelo: {modelo}")
    print("🛠️  Método: Librosa → NumPy → Whisper (SEM FFmpeg)")
    print("=" * 60)
    
    try:
        import librosa
        import whisper
        import numpy as np
        
        # Verificar arquivo
        if not os.path.exists(arquivo_mp3):
            print(f"❌ Arquivo não encontrado: {arquivo_mp3}")
            return None
        
        tamanho_mb = os.path.getsize(arquivo_mp3) / (1024 * 1024)
        print(f"📊 Tamanho: {tamanho_mb:.2f} MB")
        
        # Carregar modelo Whisper
        print(f"\n🤖 Carregando modelo Whisper '{modelo}'...")
        model = whisper.load_model(modelo)
        print("✅ Modelo carregado!")
        
        # Processar áudio com Librosa
        print(f"\n🔊 Carregando áudio com Librosa...")
        
        # Carregar áudio no formato que o Whisper espera
        audio_data, sr = librosa.load(arquivo_mp3, sr=16000)
        duracao = len(audio_data) / sr
        
        print(f"✅ Áudio processado:")
        print(f"  📊 Duração: {duracao:.1f} segundos ({duracao/60:.1f} minutos)")
        print(f"  📊 Taxa: {sr} Hz")
        print(f"  📊 Amostras: {len(audio_data):,}")
        
        # Normalizar áudio se necessário
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
        
        # Garantir que está no range correto
        audio_data = np.clip(audio_data, -1.0, 1.0)
        
        print(f"✅ Áudio normalizado para Whisper")
        
        # Transcrever diretamente com os dados de áudio
        print(f"\n🎵 Transcrevendo com Whisper...")
        print(f"⏳ Estimativa: {duracao/60*2:.1f} minutos")
        
        inicio = time.time()
        
        # Passar os dados de áudio diretamente para o Whisper
        resultado = model.transcribe(
            audio_data,  # Dados de áudio diretamente
            language="pt",
            fp16=False,
            verbose=False,
            word_timestamps=True,
            temperature=0
        )
        
        fim = time.time()
        
        texto = resultado["text"]
        segmentos = resultado.get("segments", [])
        duracao_processamento = fim - inicio
        
        # Estatísticas
        palavras = len(texto.split())
        chars = len(texto)
        
        print(f"\n{'='*60}")
        print("🎉 TRANSCRIÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"{'='*60}")
        print(f"⏱️  Tempo: {duracao_processamento:.1f}s ({duracao_processamento/60:.1f} min)")
        print(f"🎵 Áudio: {duracao:.1f}s ({duracao/60:.1f} min)")
        print(f"⚡ Velocidade: {duracao/duracao_processamento:.1f}x tempo real")
        print(f"📝 Caracteres: {chars:,}")
        print(f"🔤 Palavras: {palavras:,}")
        print(f"🚀 Velocidade: {palavras/(duracao_processamento/60):.1f} palavras/min")
        
        # Salvar resultado
        nome_base = Path(arquivo_mp3).stem
        arquivo_saida = f"{nome_base}_TRANSCRICAO_FINAL_FUNCIONAL.txt"
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("🎯 TRANSCRIÇÃO FINAL FUNCIONAL - SEM FFMPEG\n")
            f.write("=" * 70 + "\n")
            f.write(f"📁 Arquivo: {arquivo_mp3}\n")
            f.write(f"🤖 Modelo: {modelo}\n")
            f.write(f"🛠️  Método: Librosa → NumPy → Whisper (SEM FFmpeg)\n")
            f.write(f"📅 Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"⏱️  Processamento: {duracao_processamento:.1f}s ({duracao_processamento/60:.1f} min)\n")
            f.write(f"🎵 Duração áudio: {duracao:.1f}s ({duracao/60:.1f} min)\n")
            f.write(f"⚡ Velocidade: {duracao/duracao_processamento:.1f}x tempo real\n")
            f.write(f"📊 Estatísticas: {chars:,} chars, {palavras:,} palavras\n")
            f.write("=" * 70 + "\n\n")
            
            # Texto principal
            f.write("TRANSCRIÇÃO COMPLETA:\n")
            f.write("-" * 50 + "\n")
            f.write(texto)
            f.write("\n\n")
            
            # Segmentos com timestamps
            if segmentos:
                f.write("TRANSCRIÇÃO COM TIMESTAMPS:\n")
                f.write("-" * 50 + "\n")
                for segmento in segmentos:
                    inicio_seg = segmento.get('start', 0)
                    fim_seg = segmento.get('end', 0)
                    texto_seg = segmento.get('text', '')
                    
                    min_i = int(inicio_seg // 60)
                    seg_i = int(inicio_seg % 60)
                    min_f = int(fim_seg // 60)
                    seg_f = int(fim_seg % 60)
                    
                    f.write(f"[{min_i:02d}:{seg_i:02d} - {min_f:02d}:{seg_f:02d}] {texto_seg.strip()}\n")
        
        print(f"\n📂 Arquivo salvo: {arquivo_saida}")
        print(f"📍 Local: {os.path.abspath(arquivo_saida)}")
        
        # Prévia da transcrição
        print(f"\n📖 PRÉVIA DA TRANSCRIÇÃO:")
        print("=" * 60)
        preview = texto[:1200] if len(texto) > 1200 else texto
        print(preview)
        if len(texto) > 1200:
            print("\n... (transcrição completa no arquivo)")
        print("=" * 60)
        
        # Alguns segmentos com tempo
        if segmentos and len(segmentos) > 0:
            print(f"\n🕐 SEGMENTOS COM TIMESTAMPS (primeiros 5):")
            print("-" * 60)
            for i, seg in enumerate(segmentos[:5], 1):
                inicio_seg = seg.get('start', 0)
                texto_seg = seg.get('text', '')
                min_s = int(inicio_seg // 60)
                sec_s = int(inicio_seg % 60)
                print(f"{i}. [{min_s:02d}:{sec_s:02d}] {texto_seg.strip()}")
            print("-" * 60)
        
        # Oferecer para abrir
        print(f"\n📂 Abrir arquivo de transcrição?")
        try:
            resposta = input("Digite 's' para abrir: ").strip().lower()
            if resposta in ['s', 'sim']:
                os.startfile(arquivo_saida)
                print("📂 Arquivo aberto!")
        except:
            print(f"Abra manualmente: {arquivo_saida}")
        
        return {
            'sucesso': True,
            'texto': texto,
            'arquivo': arquivo_saida,
            'estatisticas': {
                'duracao_audio': duracao,
                'tempo_processamento': duracao_processamento,
                'velocidade': duracao/duracao_processamento,
                'palavras': palavras,
                'caracteres': chars
            }
        }
        
    except Exception as e:
        print(f"\n❌ ERRO:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print(f"\nDetalhes:")
        print(traceback.format_exc())
        return None

def main():
    """Função principal"""
    print("🎯 TRANSCRITOR FINAL FUNCIONAL")
    print("Solução definitiva sem dependência de FFmpeg!")
    print("=" * 60)
    
    # Verificar dependências
    if not verificar_dependencias():
        print("Execute: pip install librosa openai-whisper")
        return
    
    # Verificar arquivo
    arquivo = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return
    
    tamanho_mb = os.path.getsize(arquivo) / (1024 * 1024)
    print(f"✅ Arquivo: {arquivo}")
    print(f"📊 Tamanho: {tamanho_mb:.2f} MB")
    
    # Menu de modelos
    print(f"\n🤖 MODELOS WHISPER DISPONÍVEIS:")
    print("=" * 40)
    estimativa_base = tamanho_mb * 0.1  # Estimativa aproximada
    print(f"Estimativas para {tamanho_mb:.1f} MB:")
    print(f"1. tiny   - ~{estimativa_base*0.5:.0f} min  | Rápido")
    print(f"2. base   - ~{estimativa_base:.0f} min  | Equilibrado [RECOMENDADO]")
    print(f"3. small  - ~{estimativa_base*2:.0f} min  | Preciso")
    print(f"4. medium - ~{estimativa_base*4:.0f} min  | Muito preciso")
    
    escolha = input(f"\nEscolha (1-4) [padrão: 2]: ").strip()
    modelos = {"1": "tiny", "2": "base", "3": "small", "4": "medium"}
    modelo = modelos.get(escolha, "base")
    
    print(f"\n🚀 Iniciando transcrição com modelo '{modelo}'...")
    print("=" * 60)
    
    # Executar transcrição
    resultado = transcrever_audio_sem_ffmpeg(arquivo, modelo)
    
    if resultado and resultado['sucesso']:
        stats = resultado['estatisticas']
        print(f"\n🎉 MISSÃO CUMPRIDA!")
        print(f"✅ Transcrição completa em {stats['tempo_processamento']/60:.1f} minutos")
        print(f"⚡ Velocidade: {stats['velocidade']:.1f}x tempo real")
        print(f"📂 Arquivo: {resultado['arquivo']}")
        print(f"🎯 SUCESSO TOTAL!")
    else:
        print(f"\n💔 FALHA NA TRANSCRIÇÃO")

if __name__ == "__main__":
    main() 