"""
Sistema de Transcrição Direto - Sem FFmpeg
Versão que carrega arquivos de áudio diretamente
"""

import os
import time
import tempfile
from pathlib import Path

try:
    import whisper
    import torch
    import numpy as np
    print("✓ Dependências importadas com sucesso")
except ImportError as e:
    print(f"✗ Erro de importação: {e}")
    print("Execute: pip install openai-whisper torch")
    exit(1)

class TranscritorDireto:
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
    
    def transcrever_arquivo(self, caminho_arquivo):
        """Transcreve arquivo de áudio usando método direto"""
        if not self.modelo:
            print("Modelo não carregado!")
            return None
        
        if not os.path.exists(caminho_arquivo):
            print(f"✗ Arquivo não encontrado: {caminho_arquivo}")
            return None
        
        print(f"Transcrevendo: {caminho_arquivo}")
        print("Aguarde... Este processo pode levar alguns minutos.")
        print("NOTA: Usando método direto que não requer FFmpeg")
        
        try:
            # Tentar transcrever diretamente
            resultado = self.modelo.transcribe(
                caminho_arquivo, 
                language="pt",
                fp16=False,  # Usar FP32 para compatibilidade
                verbose=True  # Mostrar progresso
            )
            return resultado["text"]
        except Exception as e:
            print(f"✗ Erro na transcrição: {e}")
            print("Tentando método alternativo...")
            
            try:
                # Método alternativo: especificar parâmetros de áudio
                resultado = self.modelo.transcribe(
                    caminho_arquivo,
                    language="pt",
                    fp16=False,
                    temperature=0,
                    best_of=1,
                    beam_size=1,
                    patience=1.0,
                    length_penalty=1.0,
                    suppress_tokens="-1",
                    initial_prompt=None,
                    condition_on_previous_text=True,
                    compression_ratio_threshold=2.4,
                    logprob_threshold=-1.0,
                    no_speech_threshold=0.6
                )
                return resultado["text"]
            except Exception as e2:
                print(f"✗ Método alternativo também falhou: {e2}")
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
                f.write(f"Método: Whisper Direto (sem FFmpeg)\n")
                f.write("=" * 50 + "\n\n")
                f.write(texto)
            
            print(f"✓ Transcrição salva em: {arquivo_saida}")
            return arquivo_saida
        except Exception as e:
            print(f"✗ Erro ao salvar: {e}")
            return None

def verificar_sistema():
    """Verifica se o sistema está configurado corretamente"""
    print("=== VERIFICAÇÃO DO SISTEMA ===")
    
    # Verificar PyTorch
    try:
        import torch
        print(f"✓ PyTorch versão: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"✓ CUDA disponível: {torch.cuda.get_device_name()}")
        else:
            print("ℹ️  CUDA não disponível - usando CPU")
    except:
        print("✗ PyTorch não encontrado")
    
    # Verificar Whisper
    try:
        import whisper
        print("✓ Whisper disponível")
    except:
        print("✗ Whisper não encontrado")
    
    print()

def main():
    print("=== TRANSCRITOR DIRETO (SEM FFMPEG) ===\n")
    
    verificar_sistema()
    
    # Arquivo para transcrever
    arquivo_audio = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    
    if not os.path.exists(arquivo_audio):
        print(f"✗ Arquivo não encontrado: {arquivo_audio}")
        print("Certifique-se de que o arquivo está na pasta atual")
        return
    
    # Verificar tamanho do arquivo
    tamanho_mb = os.path.getsize(arquivo_audio) / (1024 * 1024)
    print(f"✓ Arquivo encontrado: {arquivo_audio}")
    print(f"  Tamanho: {tamanho_mb:.2f} MB")
    
    # Criar transcritor
    transcritor = TranscritorDireto()
    
    # Menu de modelos com aviso sobre tempo
    print("\n=== ESCOLHA DO MODELO ===")
    print("IMPORTANTE: Arquivos grandes demoram mais para processar")
    print(f"Seu arquivo tem {tamanho_mb:.1f} MB\n")
    
    print("Modelos disponíveis:")
    print("1. tiny   - ~2-3 min  | Menos preciso")
    print("2. base   - ~5-8 min  | Equilibrado [RECOMENDADO]")
    print("3. small  - ~10-15 min| Mais preciso")
    print("4. medium - ~20-30 min| Muito preciso")
    print("5. large  - ~40-60 min| Máxima precisão")
    
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
    
    # Confirmação para modelos grandes
    if modelo_escolhido in ["medium", "large"]:
        confirmar = input(f"O modelo '{modelo_escolhido}' pode demorar muito. Continuar? (s/n): ")
        if confirmar.lower() not in ['s', 'sim', 'y', 'yes']:
            print("Operação cancelada.")
            return
    
    # Carregar modelo
    print(f"\n{'='*60}")
    print("CARREGANDO MODELO")
    print(f"{'='*60}")
    
    if not transcritor.carregar_modelo(modelo_escolhido):
        print("Falha ao carregar modelo")
        return
    
    # Transcrever
    print(f"\n{'='*60}")
    print("INICIANDO TRANSCRIÇÃO")
    print(f"{'='*60}")
    print("💡 Dica: Este processo roda em segundo plano. Seja paciente!")
    
    inicio = time.time()
    texto = transcritor.transcrever_arquivo(arquivo_audio)
    fim = time.time()
    
    if texto:
        duracao = fim - inicio
        print(f"\n{'='*60}")
        print("🎉 TRANSCRIÇÃO CONCLUÍDA!")
        print(f"⏱️  Tempo: {duracao:.1f} segundos ({duracao/60:.1f} minutos)")
        print(f"{'='*60}")
        
        # Estatísticas do texto
        palavras = len(texto.split())
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"📝 Caracteres: {len(texto):,}")
        print(f"🔤 Palavras: {palavras:,}")
        print(f"⚡ Velocidade: {palavras/(duracao/60):.1f} palavras/minuto")
        
        # Mostrar prévia
        print(f"\n📖 PRÉVIA (primeiros 500 caracteres):")
        print("-" * 60)
        print(texto[:500] + "..." if len(texto) > 500 else texto)
        print("-" * 60)
        
        # Salvar
        arquivo_saida = transcritor.salvar_transcricao(texto, arquivo_audio)
        
        if arquivo_saida:
            print(f"\n✅ SUCESSO COMPLETO!")
            print(f"📄 Arquivo salvo: {arquivo_saida}")
            print(f"📂 Localização: {os.path.abspath(arquivo_saida)}")
            
            # Oferecer para abrir o arquivo
            abrir = input(f"\nDeseja abrir o arquivo de transcrição? (s/n): ")
            if abrir.lower() in ['s', 'sim', 'y', 'yes']:
                try:
                    os.startfile(arquivo_saida)  # Windows
                    print("📂 Arquivo aberto!")
                except:
                    print(f"Abra manualmente: {arquivo_saida}")
        else:
            print("✗ Erro ao salvar transcrição")
    else:
        print("✗ Falha na transcrição")
        print("\n🔧 SOLUÇÕES:")
        print("1. Tente um modelo menor (tiny ou base)")
        print("2. Verifique se há espaço em disco suficiente")
        print("3. Converta o arquivo para WAV e tente novamente")

if __name__ == "__main__":
    main() 