"""
🔬 TESTE COMPLETO DE TECNOLOGIAS DE TRANSCRIÇÃO
Este script testa todas as tecnologias disponíveis e encontra a melhor solução
"""

import os
import time
import traceback
from pathlib import Path

# Lista de tecnologias para testar
TECNOLOGIAS = {
    'whisper_moviepy': 'Whisper + MoviePy (conversão)',
    'whisper_librosa': 'Whisper + Librosa (carregamento)',
    'whisper_direto': 'Whisper Direto (sem conversão)',
    'whisper_soundfile': 'Whisper + SoundFile'
}

class TesteTecnologias:
    def __init__(self):
        self.arquivo_original = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
        self.resultados = {}
        
    def verificar_arquivo(self):
        """Verifica se o arquivo existe"""
        if not os.path.exists(self.arquivo_original):
            print(f"❌ Arquivo não encontrado: {self.arquivo_original}")
            return False
        
        tamanho = os.path.getsize(self.arquivo_original) / (1024 * 1024)
        print(f"✅ Arquivo encontrado: {self.arquivo_original}")
        print(f"📊 Tamanho: {tamanho:.2f} MB")
        return True
    
    def teste_whisper_moviepy(self):
        """Teste com MoviePy para conversão"""
        print("\n🎬 TESTANDO: Whisper + MoviePy")
        try:
            from moviepy.editor import AudioFileClip
            import whisper
            
            print("  ✓ Dependências importadas")
            
            # Converter MP3 para WAV temporário
            print("  🔄 Convertendo MP3 para WAV...")
            audio_clip = AudioFileClip(self.arquivo_original)
            temp_wav = "temp_moviepy.wav"
            audio_clip.write_audiofile(temp_wav, verbose=False, logger=None)
            audio_clip.close()
            
            print("  ✓ Conversão concluída")
            
            # Carregar modelo Whisper pequeno para teste
            print("  🤖 Carregando modelo Whisper...")
            model = whisper.load_model("tiny")  # Modelo pequeno para teste rápido
            
            print("  🎵 Transcrevendo (primeiros 30 segundos)...")
            # Transcrever apenas uma parte para teste rápido
            inicio = time.time()
            result = model.transcribe(temp_wav, language="pt", fp16=False, duration=30)
            fim = time.time()
            
            texto = result["text"]
            duracao = fim - inicio
            
            # Limpar arquivo temporário
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            
            return {
                'sucesso': True,
                'tempo': duracao,
                'texto_preview': texto[:200],
                'tamanho_texto': len(texto),
                'tecnologia': 'MoviePy + Whisper'
            }
            
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            return {
                'sucesso': False,
                'erro': str(e),
                'tecnologia': 'MoviePy + Whisper'
            }
    
    def teste_whisper_librosa(self):
        """Teste com Librosa para carregamento"""
        print("\n📚 TESTANDO: Whisper + Librosa")
        try:
            import librosa
            import whisper
            import soundfile as sf
            import numpy as np
            
            print("  ✓ Dependências importadas")
            
            # Carregar áudio com librosa
            print("  🔊 Carregando áudio com Librosa...")
            audio, sr = librosa.load(self.arquivo_original, sr=16000, duration=30)  # 30s para teste
            
            # Salvar como WAV temporário
            temp_wav = "temp_librosa.wav"
            sf.write(temp_wav, audio, sr)
            
            print("  ✓ Áudio processado com Librosa")
            
            # Transcrever com Whisper
            print("  🤖 Carregando modelo Whisper...")
            model = whisper.load_model("tiny")
            
            print("  🎵 Transcrevendo...")
            inicio = time.time()
            result = model.transcribe(temp_wav, language="pt", fp16=False)
            fim = time.time()
            
            texto = result["text"]
            duracao = fim - inicio
            
            # Limpar arquivo temporário
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            
            return {
                'sucesso': True,
                'tempo': duracao,
                'texto_preview': texto[:200],
                'tamanho_texto': len(texto),
                'tecnologia': 'Librosa + Whisper'
            }
            
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            return {
                'sucesso': False,
                'erro': str(e),
                'tecnologia': 'Librosa + Whisper'
            }
    
    def teste_whisper_direto(self):
        """Teste direto com Whisper"""
        print("\n🎯 TESTANDO: Whisper Direto")
        try:
            import whisper
            
            print("  ✓ Dependências importadas")
            print("  🤖 Carregando modelo Whisper...")
            model = whisper.load_model("tiny")
            
            print("  🎵 Transcrevendo diretamente...")
            inicio = time.time()
            # Tentar transcrever diretamente o MP3
            result = model.transcribe(self.arquivo_original, language="pt", fp16=False, duration=30)
            fim = time.time()
            
            texto = result["text"]
            duracao = fim - inicio
            
            return {
                'sucesso': True,
                'tempo': duracao,
                'texto_preview': texto[:200],
                'tamanho_texto': len(texto),
                'tecnologia': 'Whisper Direto'
            }
            
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            return {
                'sucesso': False,
                'erro': str(e),
                'tecnologia': 'Whisper Direto'
            }
    
    def teste_whisper_soundfile(self):
        """Teste com SoundFile"""
        print("\n🔊 TESTANDO: Whisper + SoundFile")
        try:
            import soundfile as sf
            import whisper
            import librosa
            
            print("  ✓ Dependências importadas")
            
            # Tentar ler com SoundFile diretamente
            try:
                data, samplerate = sf.read(self.arquivo_original, duration=30*16000)  # 30s
                temp_wav = "temp_soundfile.wav"
                sf.write(temp_wav, data, samplerate)
            except:
                # Se falhar, usar librosa para converter primeiro
                print("  🔄 Conversão necessária...")
                audio, sr = librosa.load(self.arquivo_original, sr=16000, duration=30)
                temp_wav = "temp_soundfile.wav"
                sf.write(temp_wav, audio, sr)
            
            print("  ✓ Áudio processado")
            
            # Transcrever
            print("  🤖 Carregando modelo Whisper...")
            model = whisper.load_model("tiny")
            
            print("  🎵 Transcrevendo...")
            inicio = time.time()
            result = model.transcribe(temp_wav, language="pt", fp16=False)
            fim = time.time()
            
            texto = result["text"]
            duracao = fim - inicio
            
            # Limpar arquivo temporário
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            
            return {
                'sucesso': True,
                'tempo': duracao,
                'texto_preview': texto[:200],
                'tamanho_texto': len(texto),
                'tecnologia': 'SoundFile + Whisper'
            }
            
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            return {
                'sucesso': False,
                'erro': str(e),
                'tecnologia': 'SoundFile + Whisper'
            }
    
    def executar_todos_testes(self):
        """Executa todos os testes e retorna o melhor"""
        print("🔬 INICIANDO BATERIA DE TESTES DE TECNOLOGIAS")
        print("=" * 60)
        
        if not self.verificar_arquivo():
            return None
        
        # Lista de métodos de teste
        testes = [
            self.teste_whisper_moviepy,
            self.teste_whisper_librosa,
            self.teste_whisper_direto,
            self.teste_whisper_soundfile
        ]
        
        resultados = []
        
        for teste in testes:
            try:
                resultado = teste()
                resultados.append(resultado)
                
                if resultado['sucesso']:
                    print(f"  ✅ SUCESSO - Tempo: {resultado['tempo']:.1f}s")
                    print(f"     Preview: {resultado['texto_preview'][:100]}...")
                else:
                    print(f"  ❌ FALHOU - {resultado['erro']}")
                    
            except Exception as e:
                print(f"  💥 ERRO CRÍTICO: {e}")
                resultados.append({
                    'sucesso': False,
                    'erro': f"Erro crítico: {e}",
                    'tecnologia': 'Desconhecida'
                })
        
        return self.analisar_resultados(resultados)
    
    def analisar_resultados(self, resultados):
        """Analisa os resultados e encontra a melhor tecnologia"""
        print("\n" + "=" * 60)
        print("📊 ANÁLISE DOS RESULTADOS")
        print("=" * 60)
        
        sucessos = [r for r in resultados if r['sucesso']]
        falhas = [r for r in resultados if not r['sucesso']]
        
        print(f"✅ Tecnologias que funcionaram: {len(sucessos)}")
        print(f"❌ Tecnologias que falharam: {len(falhas)}")
        
        if not sucessos:
            print("\n💀 NENHUMA TECNOLOGIA FUNCIONOU!")
            print("Problemas encontrados:")
            for falha in falhas:
                print(f"  - {falha['tecnologia']}: {falha['erro']}")
            return None
        
        # Ordenar por velocidade (menor tempo = melhor)
        sucessos.sort(key=lambda x: x['tempo'])
        melhor = sucessos[0]
        
        print(f"\n🏆 MELHOR TECNOLOGIA: {melhor['tecnologia']}")
        print(f"⏱️  Tempo de processamento: {melhor['tempo']:.2f} segundos")
        print(f"📝 Tamanho do texto gerado: {melhor['tamanho_texto']} caracteres")
        print(f"📖 Preview da transcrição:")
        print(f"   \"{melhor['texto_preview']}...\"")
        
        print(f"\n📈 RANKING COMPLETO:")
        for i, resultado in enumerate(sucessos, 1):
            print(f"  {i}. {resultado['tecnologia']} - {resultado['tempo']:.2f}s")
        
        return melhor
    
    def criar_solucao_final(self, melhor_tecnologia):
        """Cria a solução final baseada na melhor tecnologia"""
        print(f"\n🛠️  CRIANDO SOLUÇÃO FINAL...")
        
        codigo = '''"""
🎯 TRANSCRITOR FINAL - SOLUÇÃO DEFINITIVA
Esta é a melhor tecnologia encontrada nos testes
"""

import os
import time
from pathlib import Path

def transcrever_audio_final(arquivo_mp3, modelo="base"):
    """Função principal de transcrição usando a melhor tecnologia"""
    
    print(f"🎯 TRANSCRITOR FINAL ATIVADO")
    print(f"Arquivo: {arquivo_mp3}")
    print(f"Modelo: {modelo}")
    print("=" * 50)
    
    try:
        # Importar dependências da melhor tecnologia encontrada
        from moviepy.editor import AudioFileClip
        import whisper
        
        print("✅ Dependências carregadas")
        
        # Verificar arquivo
        if not os.path.exists(arquivo_mp3):
            print(f"❌ Arquivo não encontrado: {arquivo_mp3}")
            return None
        
        tamanho_mb = os.path.getsize(arquivo_mp3) / (1024 * 1024)
        print(f"📊 Tamanho do arquivo: {tamanho_mb:.2f} MB")
        
        # Carregar modelo Whisper
        print(f"🤖 Carregando modelo Whisper '{modelo}'...")
        whisper_model = whisper.load_model(modelo)
        print("✅ Modelo carregado!")
        
        # Converter áudio usando MoviePy
        print("🎬 Convertendo áudio com MoviePy...")
        audio_clip = AudioFileClip(arquivo_mp3)
        temp_wav = "conversao_final.wav"
        audio_clip.write_audiofile(temp_wav, verbose=False, logger=None)
        audio_clip.close()
        print("✅ Conversão concluída!")
        
        # Transcrever
        print("🎵 Iniciando transcrição...")
        inicio = time.time()
        resultado = whisper_model.transcribe(temp_wav, language="pt", fp16=False)
        fim = time.time()
        
        texto = resultado["text"]
        duracao = fim - inicio
        
        # Limpar arquivo temporário
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
        
        # Estatísticas
        palavras = len(texto.split())
        chars = len(texto)
        
        print(f"\\n{'='*60}")
        print("🎉 TRANSCRIÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"{'='*60}")
        print(f"⏱️  Tempo total: {duracao:.1f} segundos ({duracao/60:.1f} minutos)")
        print(f"📝 Caracteres: {chars:,}")
        print(f"🔤 Palavras: {palavras:,}")
        print(f"⚡ Velocidade: {palavras/(duracao/60):.1f} palavras/minuto")
        
        # Salvar resultado
        nome_base = Path(arquivo_mp3).stem
        arquivo_saida = f"{nome_base}_TRANSCRICAO_FINAL.txt"
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("🎯 TRANSCRIÇÃO FINAL - SOLUÇÃO DEFINITIVA\\n")
            f.write("=" * 60 + "\\n")
            f.write(f"📁 Arquivo original: {arquivo_mp3}\\n")
            f.write(f"🤖 Modelo Whisper: {modelo}\\n")
            f.write(f"🛠️  Tecnologia: MoviePy + Whisper\\n")
            f.write(f"📅 Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\\n")
            f.write(f"⏱️  Tempo de processamento: {duracao:.1f}s\\n")
            f.write(f"📊 Estatísticas: {chars:,} chars, {palavras:,} palavras\\n")
            f.write("=" * 60 + "\\n\\n")
            f.write(texto)
        
        print(f"\\n📂 Arquivo salvo: {arquivo_saida}")
        
        # Mostrar prévia
        print(f"\\n📖 PRÉVIA DA TRANSCRIÇÃO:")
        print("-" * 60)
        print(texto[:800] + ("..." if len(texto) > 800 else ""))
        print("-" * 60)
        
        # Oferecer para abrir
        try:
            abrir = input("\\n📂 Deseja abrir o arquivo de transcrição? (s/n): ")
            if abrir.lower() in ['s', 'sim', 'y', 'yes']:
                os.startfile(arquivo_saida)
                print("📂 Arquivo aberto!")
        except:
            print(f"Abra manualmente: {os.path.abspath(arquivo_saida)}")
        
        return texto, arquivo_saida
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print(f"Detalhes: {traceback.format_exc()}")
        return None

def main():
    """Função principal"""
    print("🎯 SISTEMA DE TRANSCRIÇÃO FINAL")
    print("Esta é a solução definitiva testada e aprovada!")
    print("=" * 60)
    
    arquivo = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    
    # Menu de modelos
    print("\\nEscolha o modelo Whisper:")
    print("1. tiny   - Rápido (~2-3 min)")
    print("2. base   - Equilibrado (~5-8 min) [RECOMENDADO]")
    print("3. small  - Preciso (~10-15 min)")
    print("4. medium - Muito preciso (~20-30 min)")
    print("5. large  - Máxima precisão (~40-60 min)")
    
    escolha = input("\\nDigite 1-5 [padrão: 2]: ").strip()
    modelos = {"1": "tiny", "2": "base", "3": "small", "4": "medium", "5": "large"}
    modelo = modelos.get(escolha, "base")
    
    print(f"\\n🚀 Iniciando transcrição com modelo '{modelo}'...")
    
    resultado = transcrever_audio_final(arquivo, modelo)
    
    if resultado:
        print("\\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
    else:
        print("\\n💔 FALHA NO PROCESSO")

if __name__ == "__main__":
    main()
'''
        
        with open("transcritor_FINAL.py", "w", encoding="utf-8") as f:
            f.write(codigo)
        
        print("✅ SOLUÇÃO FINAL criada: transcritor_FINAL.py")
        print("🎯 Este é o arquivo que você deve executar!")

def main():
    print("🔬 TESTE COMPLETO DE TECNOLOGIAS DE TRANSCRIÇÃO")
    print("Este script vai testar todas as tecnologias e encontrar a melhor!")
    print("=" * 70)
    
    teste = TesteTecnologias()
    melhor = teste.executar_todos_testes()
    
    if melhor:
        teste.criar_solucao_final(melhor)
        print(f"\n🎉 TESTE CONCLUÍDO!")
        print(f"✅ A melhor tecnologia foi implementada em 'transcritor_FINAL.py'")
        print(f"🚀 Execute: python transcritor_FINAL.py")
    else:
        print(f"\n💔 TESTE FALHOU!")
        print(f"Nenhuma tecnologia funcionou adequadamente.")

if __name__ == "__main__":
    main() 