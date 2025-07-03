"""
🎯 SOLUÇÃO COMPLETA PARA TRANSCRIÇÃO
Este script oferece múltiplas soluções para transcrever seu arquivo MP3
"""

import os
import webbrowser
import time
from pathlib import Path

def verificar_arquivo_mp3():
    """Verifica se o arquivo MP3 original existe"""
    arquivo_mp3 = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    if os.path.exists(arquivo_mp3):
        tamanho = os.path.getsize(arquivo_mp3) / (1024 * 1024)
        print(f"✅ Arquivo MP3 encontrado: {arquivo_mp3}")
        print(f"📊 Tamanho: {tamanho:.2f} MB")
        return arquivo_mp3, tamanho
    else:
        print(f"❌ Arquivo MP3 não encontrado: {arquivo_mp3}")
        return None, 0

def verificar_arquivo_wav():
    """Verifica se já existe um arquivo WAV convertido"""
    possíveis_wavs = [
        "Carros Elétricos em Condomínios - Diretriz Nacional.wav",
        "audio_convertido.wav",
        "transcricao.wav"
    ]
    
    for wav in possíveis_wavs:
        if os.path.exists(wav):
            tamanho = os.path.getsize(wav) / (1024 * 1024)
            print(f"✅ Arquivo WAV encontrado: {wav}")
            print(f"📊 Tamanho: {tamanho:.2f} MB")
            return wav, tamanho
    
    return None, 0

def transcrever_whisper(arquivo_audio):
    """Transcreve usando Whisper"""
    try:
        import whisper
        
        print(f"\n{'='*60}")
        print("🎯 INICIANDO TRANSCRIÇÃO COM WHISPER")
        print(f"{'='*60}")
        
        # Escolher modelo
        print("Escolha o modelo:")
        print("1. tiny   - Rápido (~2-3 min)")
        print("2. base   - Equilibrado (~5-8 min) [RECOMENDADO]")
        print("3. small  - Preciso (~10-15 min)")
        
        escolha = input("Digite 1, 2 ou 3 [padrão: 2]: ").strip()
        modelos = {"1": "tiny", "2": "base", "3": "small"}
        modelo = modelos.get(escolha, "base")
        
        print(f"\n🔄 Carregando modelo '{modelo}'...")
        whisper_model = whisper.load_model(modelo)
        print("✅ Modelo carregado!")
        
        print(f"\n🎵 Transcrevendo arquivo: {arquivo_audio}")
        print("⏳ Aguarde... Este processo pode demorar alguns minutos.")
        
        inicio = time.time()
        resultado = whisper_model.transcribe(arquivo_audio, language="pt", fp16=False)
        fim = time.time()
        
        texto = resultado["text"]
        duracao = fim - inicio
        
        # Salvar resultado
        nome_base = Path(arquivo_audio).stem
        arquivo_saida = f"{nome_base}_transcricao_completa.txt"
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("=== 🎯 TRANSCRIÇÃO COMPLETA ===\n")
            f.write(f"📁 Arquivo: {arquivo_audio}\n")
            f.write(f"📅 Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"🤖 Modelo: Whisper {modelo}\n")
            f.write(f"⏱️  Tempo: {duracao:.1f}s ({duracao/60:.1f} min)\n")
            f.write("=" * 60 + "\n\n")
            f.write(texto)
        
        # Estatísticas
        palavras = len(texto.split())
        print(f"\n{'='*60}")
        print("🎉 TRANSCRIÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"{'='*60}")
        print(f"⏱️  Tempo total: {duracao:.1f} segundos ({duracao/60:.1f} minutos)")
        print(f"📝 Caracteres: {len(texto):,}")
        print(f"🔤 Palavras: {palavras:,}")
        print(f"⚡ Velocidade: {palavras/(duracao/60):.1f} palavras/min")
        
        # Prévia
        print(f"\n📖 PRÉVIA DA TRANSCRIÇÃO:")
        print("-" * 60)
        print(texto[:800] + ("..." if len(texto) > 800 else ""))
        print("-" * 60)
        
        print(f"\n✅ Arquivo salvo: {arquivo_saida}")
        
        # Oferecer para abrir
        if input("\n📂 Deseja abrir o arquivo? (s/n): ").lower() in ['s', 'sim']:
            try:
                os.startfile(arquivo_saida)
            except:
                print(f"Abra manualmente: {os.path.abspath(arquivo_saida)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na transcrição: {e}")
        return False

def abrir_conversor_online():
    """Abre conversores online no navegador"""
    print("\n🌐 ABRINDO CONVERSORES ONLINE...")
    
    conversores = [
        "https://convertio.co/pt/mp3-wav/",
        "https://online-audio-converter.com/pt/",
        "https://cloudconvert.com/mp3-to-wav"
    ]
    
    for i, conversor in enumerate(conversores, 1):
        print(f"{i}. {conversor}")
    
    try:
        # Abrir o primeiro conversor
        webbrowser.open(conversores[0])
        print(f"\n✅ Conversor aberto no navegador!")
    except:
        print("❌ Não foi possível abrir automaticamente")
    
    print("\n📋 INSTRUÇÕES:")
    print("1. Faça upload do arquivo MP3")
    print("2. Escolha formato WAV")
    print("3. Baixe o arquivo convertido")
    print("4. Coloque o arquivo WAV nesta pasta")
    print("5. Execute este script novamente")

def main():
    print("🎯 SISTEMA COMPLETO DE TRANSCRIÇÃO")
    print("=" * 50)
    
    # Verificar arquivos
    arquivo_mp3, tamanho_mp3 = verificar_arquivo_mp3()
    arquivo_wav, tamanho_wav = verificar_arquivo_wav()
    
    if not arquivo_mp3 and not arquivo_wav:
        print("❌ Nenhum arquivo de áudio encontrado!")
        print("Certifique-se de que o arquivo MP3 está nesta pasta.")
        return
    
    print("\n🎯 OPÇÕES DISPONÍVEIS:")
    
    if arquivo_wav:
        print("1. ✅ Transcrever arquivo WAV (RECOMENDADO)")
        
    if arquivo_mp3:
        print("2. 🔄 Converter MP3 para WAV online")
        print("3. 🎲 Tentar transcrever MP3 diretamente (pode falhar)")
    
    print("4. ❌ Sair")
    
    while True:
        escolha = input(f"\nEscolha uma opção: ").strip()
        
        if escolha == "1" and arquivo_wav:
            print(f"\n🎯 Usando arquivo WAV: {arquivo_wav}")
            if transcrever_whisper(arquivo_wav):
                break
                
        elif escolha == "2" and arquivo_mp3:
            abrir_conversor_online()
            print(f"\n⏳ Após converter, execute novamente este script")
            break
            
        elif escolha == "3" and arquivo_mp3:
            print(f"\n🎲 Tentando transcrever MP3 diretamente...")
            print("⚠️  AVISO: Pode falhar devido ao FFmpeg")
            if transcrever_whisper(arquivo_mp3):
                break
            else:
                print("\n💡 Recomendo usar a opção 2 (converter online)")
                
        elif escolha == "4":
            print("👋 Saindo...")
            break
            
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main() 