"""
🎯 TRANSCRITOR DEFINITIVO - SOLUÇÃO FINAL TESTADA
Esta é a melhor solução encontrada e testada com as tecnologias disponíveis
Usa: Librosa + SoundFile + Whisper
"""

import os
import time
import traceback
from pathlib import Path

def verificar_dependencias():
    """Verifica se todas as dependências estão disponíveis"""
    print("🔍 Verificando dependências...")
    
    try:
        import librosa
        print("✅ Librosa")
    except ImportError:
        print("❌ Librosa não encontrado")
        return False
    
    try:
        import soundfile as sf
        print("✅ SoundFile")
    except ImportError:
        print("❌ SoundFile não encontrado")
        return False
    
    try:
        import whisper
        print("✅ Whisper")
    except ImportError:
        print("❌ Whisper não encontrado")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy")
    except ImportError:
        print("❌ NumPy não encontrado")
        return False
    
    print("✅ Todas as dependências OK!")
    return True

def transcrever_audio_definitivo(arquivo_mp3, modelo="base", salvar_wav=False):
    """
    Função principal de transcrição usando a melhor tecnologia testada
    """
    
    print("🎯 TRANSCRITOR DEFINITIVO ATIVADO")
    print("=" * 60)
    print(f"📁 Arquivo: {arquivo_mp3}")
    print(f"🤖 Modelo: {modelo}")
    print("🛠️  Tecnologia: Librosa + SoundFile + Whisper")
    print("=" * 60)
    
    try:
        # Importar dependências
        import librosa
        import soundfile as sf
        import whisper
        import numpy as np
        
        # Verificar se o arquivo existe
        if not os.path.exists(arquivo_mp3):
            print(f"❌ Arquivo não encontrado: {arquivo_mp3}")
            return None
        
        tamanho_mb = os.path.getsize(arquivo_mp3) / (1024 * 1024)
        print(f"📊 Tamanho do arquivo: {tamanho_mb:.2f} MB")
        
        # Carregar modelo Whisper
        print(f"\n🤖 Carregando modelo Whisper '{modelo}'...")
        whisper_model = whisper.load_model(modelo)
        print("✅ Modelo Whisper carregado!")
        
        # Processar áudio com Librosa
        print("\n🔊 Processando áudio com Librosa...")
        print("  📥 Carregando arquivo MP3...")
        
        # Carregar o áudio completo
        audio_data, sample_rate = librosa.load(arquivo_mp3, sr=16000)
        
        duracao_segundos = len(audio_data) / sample_rate
        print(f"  ✅ Áudio carregado: {duracao_segundos:.1f} segundos")
        print(f"  📊 Taxa de amostragem: {sample_rate} Hz")
        print(f"  📊 Amostras: {len(audio_data):,}")
        
        # Salvar como WAV temporário
        temp_wav = "audio_processado_librosa.wav"
        print(f"  💾 Salvando como WAV temporário: {temp_wav}")
        sf.write(temp_wav, audio_data, sample_rate)
        print("  ✅ Conversão concluída!")
        
        # Transcrever com Whisper
        print(f"\n🎵 Iniciando transcrição com Whisper...")
        print("  ⏳ Este processo pode demorar alguns minutos...")
        
        inicio = time.time()
        resultado = whisper_model.transcribe(
            temp_wav, 
            language="pt", 
            fp16=False,
            verbose=True,
            word_timestamps=True
        )
        fim = time.time()
        
        texto = resultado["text"]
        segmentos = resultado.get("segments", [])
        duracao_processamento = fim - inicio
        
        # Limpar arquivo temporário (se não quiser manter)
        if not salvar_wav and os.path.exists(temp_wav):
            os.remove(temp_wav)
            print("  🗑️  Arquivo temporário removido")
        elif salvar_wav:
            print(f"  💾 Arquivo WAV mantido: {temp_wav}")
        
        # Estatísticas
        palavras = len(texto.split())
        chars = len(texto)
        
        print(f"\n{'='*60}")
        print("🎉 TRANSCRIÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"{'='*60}")
        print(f"⏱️  Tempo de processamento: {duracao_processamento:.1f}s ({duracao_processamento/60:.1f} min)")
        print(f"🎵 Duração do áudio: {duracao_segundos:.1f}s ({duracao_segundos/60:.1f} min)")
        print(f"⚡ Fator de velocidade: {duracao_segundos/duracao_processamento:.1f}x")
        print(f"📝 Caracteres: {chars:,}")
        print(f"🔤 Palavras: {palavras:,}")
        print(f"📊 Palavras por minuto: {palavras/(duracao_segundos/60):.1f}")
        print(f"🚀 Velocidade de processamento: {palavras/(duracao_processamento/60):.1f} palavras/min")
        
        # Salvar resultado completo
        nome_base = Path(arquivo_mp3).stem
        arquivo_saida = f"{nome_base}_TRANSCRICAO_DEFINITIVA.txt"
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("🎯 TRANSCRIÇÃO DEFINITIVA - SOLUÇÃO FINAL\n")
            f.write("=" * 70 + "\n")
            f.write(f"📁 Arquivo original: {arquivo_mp3}\n")
            f.write(f"🤖 Modelo Whisper: {modelo}\n")
            f.write(f"🛠️  Tecnologia: Librosa + SoundFile + Whisper\n")
            f.write(f"📅 Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"⏱️  Tempo de processamento: {duracao_processamento:.1f}s ({duracao_processamento/60:.1f} min)\n")
            f.write(f"🎵 Duração do áudio: {duracao_segundos:.1f}s ({duracao_segundos/60:.1f} min)\n")
            f.write(f"📊 Estatísticas: {chars:,} caracteres, {palavras:,} palavras\n")
            f.write(f"⚡ Fator de velocidade: {duracao_segundos/duracao_processamento:.1f}x\n")
            f.write(f"🚀 Velocidade: {palavras/(duracao_processamento/60):.1f} palavras/min\n")
            f.write("=" * 70 + "\n\n")
            
            # Transcrição principal
            f.write("TRANSCRIÇÃO COMPLETA:\n")
            f.write("-" * 50 + "\n")
            f.write(texto)
            f.write("\n\n")
            
            # Segmentos com timestamps (se disponíveis)
            if segmentos:
                f.write("\nTRANSCRIÇÃO COM TIMESTAMPS:\n")
                f.write("-" * 50 + "\n")
                for i, segmento in enumerate(segmentos, 1):
                    inicio_seg = segmento.get('start', 0)
                    fim_seg = segmento.get('end', 0)
                    texto_seg = segmento.get('text', '')
                    
                    min_inicio = int(inicio_seg // 60)
                    seg_inicio = int(inicio_seg % 60)
                    min_fim = int(fim_seg // 60)
                    seg_fim = int(fim_seg % 60)
                    
                    f.write(f"[{min_inicio:02d}:{seg_inicio:02d} - {min_fim:02d}:{seg_fim:02d}] {texto_seg.strip()}\n")
        
        print(f"\n📂 Transcrição salva em: {arquivo_saida}")
        print(f"📍 Localização completa: {os.path.abspath(arquivo_saida)}")
        
        # Mostrar prévia
        print(f"\n📖 PRÉVIA DA TRANSCRIÇÃO:")
        print("=" * 60)
        preview = texto[:1000] if len(texto) > 1000 else texto
        print(preview)
        if len(texto) > 1000:
            print("...")
        print("=" * 60)
        
        # Mostrar alguns segmentos com timestamp
        if segmentos and len(segmentos) > 0:
            print(f"\n🕐 PRIMEIROS SEGMENTOS COM TEMPO:")
            print("-" * 50)
            for i, segmento in enumerate(segmentos[:5], 1):
                inicio_seg = segmento.get('start', 0)
                texto_seg = segmento.get('text', '')
                min_s = int(inicio_seg // 60)
                seg_s = int(inicio_seg % 60)
                print(f"{i}. [{min_s:02d}:{seg_s:02d}] {texto_seg.strip()}")
            print("-" * 50)
        
        # Oferecer para abrir arquivo
        print(f"\n📂 Deseja abrir o arquivo de transcrição?")
        try:
            resposta = input("Digite 's' para abrir ou qualquer tecla para continuar: ").strip().lower()
            if resposta in ['s', 'sim', 'y', 'yes']:
                os.startfile(arquivo_saida)
                print("📂 Arquivo aberto!")
        except:
            print(f"Abra manualmente: {arquivo_saida}")
        
        return {
            'texto': texto,
            'arquivo_saida': arquivo_saida,
            'estatisticas': {
                'duracao_audio': duracao_segundos,
                'duracao_processamento': duracao_processamento,
                'palavras': palavras,
                'caracteres': chars,
                'velocidade': duracao_segundos/duracao_processamento
            },
            'segmentos': segmentos
        }
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE A TRANSCRIÇÃO:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print(f"\nDetalhes técnicos:")
        print(traceback.format_exc())
        
        # Limpar arquivos temporários em caso de erro
        temp_files = ["audio_processado_librosa.wav"]
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"🗑️  Arquivo temporário removido: {temp_file}")
                except:
                    pass
        
        return None

def main():
    """Função principal"""
    print("🎯 SISTEMA DE TRANSCRIÇÃO DEFINITIVO")
    print("Esta é a solução final testada e aprovada!")
    print("=" * 70)
    
    # Verificar dependências
    if not verificar_dependencias():
        print("\n❌ Dependências faltando. Execute:")
        print("pip install librosa soundfile openai-whisper")
        return
    
    # Verificar arquivo
    arquivo = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    
    if not os.path.exists(arquivo):
        print(f"\n❌ Arquivo não encontrado: {arquivo}")
        print("Certifique-se de que o arquivo está nesta pasta")
        return
    
    tamanho_mb = os.path.getsize(arquivo) / (1024 * 1024)
    print(f"\n✅ Arquivo encontrado: {arquivo}")
    print(f"📊 Tamanho: {tamanho_mb:.2f} MB")
    
    # Menu de modelos com estimativas de tempo
    print(f"\n🤖 ESCOLHA DO MODELO WHISPER:")
    print("=" * 40)
    print(f"Para arquivo de {tamanho_mb:.1f} MB:")
    print("1. tiny   - ~2-4 min  | Velocidade máxima")
    print("2. base   - ~5-10 min | Equilibrado [RECOMENDADO]")
    print("3. small  - ~10-20 min| Boa precisão")
    print("4. medium - ~20-40 min| Alta precisão")
    print("5. large  - ~40-80 min| Máxima precisão")
    
    escolha = input(f"\nDigite 1-5 [padrão: 2]: ").strip()
    modelos = {
        "1": "tiny", 
        "2": "base", 
        "3": "small", 
        "4": "medium", 
        "5": "large"
    }
    modelo = modelos.get(escolha, "base")
    
    # Confirmação para modelos grandes
    if modelo in ["medium", "large"]:
        print(f"\n⚠️  AVISO: O modelo '{modelo}' pode demorar muito tempo!")
        confirmar = input("Deseja continuar? (s/n): ").strip().lower()
        if confirmar not in ['s', 'sim', 'y', 'yes']:
            print("Operação cancelada.")
            return
    
    # Perguntar se quer manter arquivo WAV
    print(f"\n💾 Deseja manter o arquivo WAV convertido?")
    manter_wav = input("(útil para reutilizar) (s/n) [padrão: n]: ").strip().lower()
    salvar_wav = manter_wav in ['s', 'sim', 'y', 'yes']
    
    print(f"\n🚀 INICIANDO TRANSCRIÇÃO...")
    print(f"Modelo: {modelo}")
    print(f"Manter WAV: {'Sim' if salvar_wav else 'Não'}")
    print("=" * 60)
    
    # Executar transcrição
    resultado = transcrever_audio_definitivo(arquivo, modelo, salvar_wav)
    
    if resultado:
        print(f"\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print(f"📂 Arquivo de transcrição: {resultado['arquivo_saida']}")
        print(f"⚡ Velocidade: {resultado['estatisticas']['velocidade']:.1f}x tempo real")
    else:
        print(f"\n💔 FALHA NO PROCESSO")
        print("Verifique os erros acima e tente novamente")

if __name__ == "__main__":
    main() 