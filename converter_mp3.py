"""
Conversor MP3 para WAV usando métodos alternativos
"""

import os
import subprocess
import sys

def verificar_ffmpeg():
    """Verifica se FFmpeg está disponível"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def converter_com_ffmpeg(arquivo_mp3, arquivo_wav):
    """Converte MP3 para WAV usando FFmpeg"""
    try:
        cmd = [
            'ffmpeg', '-i', arquivo_mp3,
            '-ar', '16000',  # 16kHz
            '-ac', '1',      # mono
            '-y',            # sobrescrever
            arquivo_wav
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Erro ao converter com FFmpeg: {e}")
        return False

def main():
    arquivo_mp3 = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    arquivo_wav = "audio_convertido.wav"
    
    if not os.path.exists(arquivo_mp3):
        print(f"✗ Arquivo não encontrado: {arquivo_mp3}")
        return
    
    print(f"Convertendo {arquivo_mp3} para {arquivo_wav}")
    
    if verificar_ffmpeg():
        print("✓ FFmpeg encontrado")
        if converter_com_ffmpeg(arquivo_mp3, arquivo_wav):
            print(f"✅ Conversão concluída: {arquivo_wav}")
            
            # Verificar se o arquivo foi criado
            if os.path.exists(arquivo_wav):
                tamanho = os.path.getsize(arquivo_wav) / (1024 * 1024)
                print(f"📄 Tamanho do arquivo WAV: {tamanho:.2f} MB")
                
                # Agora podemos usar este arquivo WAV com Whisper
                print("\nAgora você pode usar o arquivo WAV com Whisper:")
                print(f"python transcricao_simples.py")
            else:
                print("✗ Arquivo WAV não foi criado")
        else:
            print("✗ Falha na conversão")
    else:
        print("✗ FFmpeg não encontrado")
        print("Instale FFmpeg usando:")
        print("winget install ffmpeg")
        print("Depois reinicie o terminal")

if __name__ == "__main__":
    main() 