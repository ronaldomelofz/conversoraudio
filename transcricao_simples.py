"""
Sistema de Transcrição Simplificado - Apenas Whisper
Este script usa apenas o Whisper para transcrever arquivos MP3
"""

import os
import time
from pathlib import Path

try:
    import whisper
    print("✓ Whisper importado com sucesso")
except ImportError:
    print("✗ Erro: Whisper não instalado. Execute: pip install openai-whisper")
    exit(1)

class TranscritorSimples:
    def __init__(self):
        self.modelo = None
        
    def carregar_modelo(self, tamanho="base"):
        """Carrega o modelo Whisper"""
        print(f"Carregando modelo Whisper '{tamanho}'...")
        try:
            self.modelo = whisper.load_model(tamanho)
            print("✓ Modelo carregado com sucesso!")
            return True
        except Exception as e:
            print(f"✗ Erro ao carregar modelo: {e}")
            return False
    
    def transcrever(self, arquivo_audio):
        """Transcreve o arquivo de áudio"""
        if not self.modelo:
            print("Modelo não carregado!")
            return None
        
        if not os.path.exists(arquivo_audio):
            print(f"✗ Arquivo não encontrado: {arquivo_audio}")
            return None
        
        print(f"Transcrevendo: {arquivo_audio}")
        print("Aguarde... Este processo pode levar alguns minutos.")
        
        try:
            # Transcrever com Whisper
            resultado = self.modelo.transcribe(arquivo_audio, language="pt")
            return resultado["text"]
        except Exception as e:
            print(f"✗ Erro na transcrição: {e}")
            return None
    
    def salvar_transcricao(self, texto, arquivo_original):
        """Salva a transcrição em arquivo"""
        if not texto:
            print("Nenhum texto para salvar")
            return None
        
        nome_base = Path(arquivo_original).stem
        arquivo_saida = f"{nome_base}_transcricao.txt"
        
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write("=== TRANSCRIÇÃO DE ÁUDIO ===\n")
                f.write(f"Arquivo: {arquivo_original}\n")
                f.write(f"Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(texto)
            
            print(f"✓ Transcrição salva em: {arquivo_saida}")
            return arquivo_saida
        except Exception as e:
            print(f"✗ Erro ao salvar: {e}")
            return None

def main():
    print("=== TRANSCRITOR DE ÁUDIO SIMPLES ===\n")
    
    # Arquivo para transcrever
    arquivo_mp3 = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    
    if not os.path.exists(arquivo_mp3):
        print(f"✗ Arquivo não encontrado: {arquivo_mp3}")
        print("Certifique-se de que o arquivo está na pasta atual")
        return
    
    # Verificar tamanho do arquivo
    tamanho_mb = os.path.getsize(arquivo_mp3) / (1024 * 1024)
    print(f"✓ Arquivo encontrado: {arquivo_mp3}")
    print(f"  Tamanho: {tamanho_mb:.2f} MB")
    
    # Criar transcritor
    transcritor = TranscritorSimples()
    
    # Escolher modelo
    print("\nEscolha o modelo Whisper:")
    print("1. tiny   - Mais rápido, menos preciso (~30 MB)")
    print("2. base   - Equilibrado (~150 MB) [RECOMENDADO]")
    print("3. small  - Mais preciso (~500 MB)")
    print("4. medium - Muito preciso (~1.5 GB)")
    print("5. large  - Máxima precisão (~3 GB)")
    
    escolha = input("\nDigite sua escolha (1-5) [padrão: 2]: ").strip()
    
    modelos = {
        "1": "tiny",
        "2": "base", 
        "3": "small",
        "4": "medium",
        "5": "large"
    }
    
    modelo_escolhido = modelos.get(escolha, "base")
    print(f"\nUsando modelo: {modelo_escolhido}")
    
    # Carregar modelo
    if not transcritor.carregar_modelo(modelo_escolhido):
        print("Falha ao carregar modelo")
        return
    
    # Transcrever
    print(f"\n{'='*60}")
    print("INICIANDO TRANSCRIÇÃO")
    print(f"{'='*60}")
    
    inicio = time.time()
    texto = transcritor.transcrever(arquivo_mp3)
    fim = time.time()
    
    if texto:
        duracao = fim - inicio
        print(f"\n{'='*60}")
        print("TRANSCRIÇÃO CONCLUÍDA")
        print(f"Tempo: {duracao:.1f} segundos")
        print(f"{'='*60}")
        
        # Mostrar prévia
        print(f"\nPrévia (primeiros 300 caracteres):")
        print("-" * 50)
        print(texto[:300] + "...")
        print("-" * 50)
        
        # Salvar
        arquivo_saida = transcritor.salvar_transcricao(texto, arquivo_mp3)
        
        if arquivo_saida:
            print(f"\n✅ SUCESSO!")
            print(f"📄 Transcrição completa salva em: {arquivo_saida}")
            print(f"📊 Total de caracteres: {len(texto)}")
            print(f"⏱️  Tempo de processamento: {duracao:.1f}s")
        else:
            print("✗ Erro ao salvar transcrição")
    else:
        print("✗ Falha na transcrição")

if __name__ == "__main__":
    main() 