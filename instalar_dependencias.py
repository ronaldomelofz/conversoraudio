import subprocess
import sys
import os

def instalar_ffmpeg():
    """Instala FFmpeg necessário para pydub"""
    print("=== Instalando FFmpeg ===")
    
    if sys.platform.startswith('win'):
        print("Para Windows, por favor instale FFmpeg manualmente:")
        print("1. Baixe FFmpeg de: https://ffmpeg.org/download.html")
        print("2. Extraia e adicione à variável PATH do sistema")
        print("3. Ou use chocolatey: choco install ffmpeg")
        print("4. Ou use winget: winget install ffmpeg")
    elif sys.platform.startswith('linux'):
        print("Instalando FFmpeg no Linux...")
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'])
    elif sys.platform.startswith('darwin'):
        print("Instalando FFmpeg no macOS...")
        subprocess.run(['brew', 'install', 'ffmpeg'])

def instalar_dependencias_python():
    """Instala as dependências Python"""
    print("=== Instalando dependências Python ===")
    
    dependencias = [
        "speechrecognition==3.10.0",
        "pydub==0.25.1",
        "openai-whisper",
        "torch",
        "torchaudio"
    ]
    
    for dep in dependencias:
        print(f"Instalando {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} instalado com sucesso")
        except subprocess.CalledProcessError as e:
            print(f"✗ Erro ao instalar {dep}: {e}")

def verificar_instalacao():
    """Verifica se as dependências foram instaladas corretamente"""
    print("\n=== Verificando instalação ===")
    
    try:
        import speech_recognition as sr
        print("✓ speech_recognition instalado")
    except ImportError:
        print("✗ speech_recognition não encontrado")
    
    try:
        from pydub import AudioSegment
        print("✓ pydub instalado")
    except ImportError:
        print("✗ pydub não encontrado")
    
    try:
        import whisper
        print("✓ whisper instalado")
    except ImportError:
        print("✗ whisper não encontrado")
    
    try:
        import torch
        print("✓ torch instalado")
    except ImportError:
        print("✗ torch não encontrado")

def main():
    print("=== INSTALADOR DO SISTEMA DE TRANSCRIÇÃO ===\n")
    
    # Atualizar pip
    print("Atualizando pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Instalar dependências Python
    instalar_dependencias_python()
    
    # Verificar instalação
    verificar_instalacao()
    
    # Instruções sobre FFmpeg
    print("\n=== IMPORTANTE ===")
    instalar_ffmpeg()
    
    print("\n=== INSTALAÇÃO CONCLUÍDA ===")
    print("Para usar o sistema:")
    print("1. Certifique-se de que FFmpeg está instalado")
    print("2. Execute: python transcricao_audio.py")
    print("3. Escolha o método de transcrição desejado")

if __name__ == "__main__":
    main() 