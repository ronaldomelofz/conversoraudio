import os
import sys
import speech_recognition as sr
from pydub import AudioSegment
from pathlib import Path
import whisper
import time

class TranscritorAudio:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.modelo_whisper = None
        
    def carregar_whisper(self, modelo="base"):
        """Carrega o modelo Whisper para transcrição"""
        print(f"Carregando modelo Whisper '{modelo}'...")
        try:
            self.modelo_whisper = whisper.load_model(modelo)
            print("Modelo Whisper carregado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao carregar modelo Whisper: {e}")
            return False
    
    def converter_mp3_para_wav(self, caminho_mp3):
        """Converte arquivo MP3 para WAV para melhor compatibilidade"""
        print(f"Convertendo {caminho_mp3} para WAV...")
        try:
            audio = AudioSegment.from_mp3(caminho_mp3)
            # Converter para mono e 16kHz para melhor performance
            audio = audio.set_channels(1).set_frame_rate(16000)
            
            caminho_wav = caminho_mp3.replace('.mp3', '_temp.wav')
            audio.export(caminho_wav, format="wav")
            print(f"Arquivo convertido: {caminho_wav}")
            return caminho_wav
        except Exception as e:
            print(f"Erro na conversão: {e}")
            return None
    
    def dividir_audio(self, caminho_audio, duracao_segmento=60):
        """Divide o áudio em segmentos menores para processamento"""
        print(f"Dividindo áudio em segmentos de {duracao_segmento} segundos...")
        try:
            audio = AudioSegment.from_wav(caminho_audio)
            duracao_total = len(audio)
            segmentos = []
            
            for i in range(0, duracao_total, duracao_segmento * 1000):
                segmento = audio[i:i + duracao_segmento * 1000]
                nome_segmento = f"segmento_{i//1000}_{(i + duracao_segmento * 1000)//1000}.wav"
                segmento.export(nome_segmento, format="wav")
                segmentos.append(nome_segmento)
            
            print(f"Áudio dividido em {len(segmentos)} segmentos")
            return segmentos
        except Exception as e:
            print(f"Erro ao dividir áudio: {e}")
            return []
    
    def transcrever_com_whisper(self, caminho_audio):
        """Transcreve áudio usando Whisper (mais preciso)"""
        if not self.modelo_whisper:
            if not self.carregar_whisper():
                return None
        
        print(f"Transcrevendo com Whisper: {caminho_audio}")
        try:
            resultado = self.modelo_whisper.transcribe(caminho_audio, language="pt")
            return resultado["text"]
        except Exception as e:
            print(f"Erro na transcrição com Whisper: {e}")
            return None
    
    def transcrever_com_google(self, caminho_audio):
        """Transcreve áudio usando Google Speech Recognition (alternativa)"""
        print(f"Transcrevendo com Google Speech Recognition: {caminho_audio}")
        try:
            with sr.AudioFile(caminho_audio) as source:
                audio_data = self.recognizer.record(source)
                texto = self.recognizer.recognize_google(audio_data, language="pt-BR")
                return texto
        except sr.UnknownValueError:
            print("Google Speech Recognition não conseguiu entender o áudio")
            return None
        except sr.RequestError as e:
            print(f"Erro no serviço Google Speech Recognition: {e}")
            return None
        except Exception as e:
            print(f"Erro na transcrição: {e}")
            return None
    
    def transcrever_arquivo(self, caminho_arquivo, usar_whisper=True, dividir=True):
        """Método principal para transcrever um arquivo de áudio"""
        print(f"=== Iniciando transcrição de: {caminho_arquivo} ===")
        
        if not os.path.exists(caminho_arquivo):
            print(f"Arquivo não encontrado: {caminho_arquivo}")
            return None
        
        # Converter MP3 para WAV se necessário
        if caminho_arquivo.lower().endswith('.mp3'):
            caminho_wav = self.converter_mp3_para_wav(caminho_arquivo)
            if not caminho_wav:
                return None
        else:
            caminho_wav = caminho_arquivo
        
        transcricao_completa = ""
        arquivos_temporarios = []
        
        try:
            if dividir:
                # Dividir em segmentos para arquivos grandes
                segmentos = self.dividir_audio(caminho_wav)
                arquivos_temporarios.extend(segmentos)
                
                for i, segmento in enumerate(segmentos):
                    print(f"\nProcessando segmento {i+1}/{len(segmentos)}: {segmento}")
                    
                    if usar_whisper:
                        texto = self.transcrever_com_whisper(segmento)
                    else:
                        texto = self.transcrever_com_google(segmento)
                    
                    if texto:
                        transcricao_completa += texto + " "
                        print(f"Segmento {i+1} transcrito com sucesso")
                    else:
                        print(f"Falha na transcrição do segmento {i+1}")
            else:
                # Transcrever arquivo inteiro
                if usar_whisper:
                    transcricao_completa = self.transcrever_com_whisper(caminho_wav)
                else:
                    transcricao_completa = self.transcrever_com_google(caminho_wav)
        
        finally:
            # Limpar arquivos temporários
            for arquivo_temp in arquivos_temporarios:
                try:
                    if os.path.exists(arquivo_temp):
                        os.remove(arquivo_temp)
                except:
                    pass
            
            # Remover arquivo WAV temporário se foi criado
            if caminho_wav != caminho_arquivo and os.path.exists(caminho_wav):
                try:
                    os.remove(caminho_wav)
                except:
                    pass
        
        return transcricao_completa.strip() if transcricao_completa else None
    
    def salvar_transcricao(self, transcricao, caminho_arquivo_original):
        """Salva a transcrição em um arquivo de texto"""
        if not transcricao:
            print("Nenhuma transcrição para salvar")
            return None
        
        nome_base = Path(caminho_arquivo_original).stem
        arquivo_saida = f"{nome_base}_transcricao.txt"
        
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write("=== TRANSCRIÇÃO DE ÁUDIO ===\n")
                f.write(f"Arquivo original: {caminho_arquivo_original}\n")
                f.write(f"Data da transcrição: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(transcricao)
            
            print(f"Transcrição salva em: {arquivo_saida}")
            return arquivo_saida
        except Exception as e:
            print(f"Erro ao salvar transcrição: {e}")
            return None

def main():
    print("=== SISTEMA DE TRANSCRIÇÃO DE ÁUDIO ===\n")
    
    # Arquivo MP3 encontrado na pasta raiz
    arquivo_mp3 = r"Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    
    if not os.path.exists(arquivo_mp3):
        print(f"Arquivo não encontrado: {arquivo_mp3}")
        print("Certifique-se de que o arquivo MP3 está na pasta raiz do projeto")
        return
    
    transcritor = TranscritorAudio()
    
    print("Escolha o método de transcrição:")
    print("1. Whisper (OpenAI) - Mais preciso, funciona offline")
    print("2. Google Speech Recognition - Requer internet")
    print("3. Ambos (para comparação)")
    
    escolha = input("\nDigite sua escolha (1, 2 ou 3): ").strip()
    
    if escolha == "1":
        print("\n=== Usando Whisper ===")
        transcricao = transcritor.transcrever_arquivo(arquivo_mp3, usar_whisper=True)
        if transcricao:
            print(f"\n=== TRANSCRIÇÃO COMPLETA ===\n{transcricao}")
            transcritor.salvar_transcricao(transcricao, arquivo_mp3)
        else:
            print("Falha na transcrição com Whisper")
    
    elif escolha == "2":
        print("\n=== Usando Google Speech Recognition ===")
        transcricao = transcritor.transcrever_arquivo(arquivo_mp3, usar_whisper=False)
        if transcricao:
            print(f"\n=== TRANSCRIÇÃO COMPLETA ===\n{transcricao}")
            transcritor.salvar_transcricao(transcricao, arquivo_mp3)
        else:
            print("Falha na transcrição com Google")
    
    elif escolha == "3":
        print("\n=== Comparando ambos os métodos ===")
        
        print("\n--- Whisper ---")
        transcricao_whisper = transcritor.transcrever_arquivo(arquivo_mp3, usar_whisper=True)
        
        print("\n--- Google Speech Recognition ---")
        transcricao_google = transcritor.transcrever_arquivo(arquivo_mp3, usar_whisper=False)
        
        if transcricao_whisper:
            print(f"\n=== TRANSCRIÇÃO WHISPER ===\n{transcricao_whisper}")
            transcritor.salvar_transcricao(transcricao_whisper, arquivo_mp3.replace('.mp3', '_whisper.mp3'))
        
        if transcricao_google:
            print(f"\n=== TRANSCRIÇÃO GOOGLE ===\n{transcricao_google}")
            transcritor.salvar_transcricao(transcricao_google, arquivo_mp3.replace('.mp3', '_google.mp3'))
    
    else:
        print("Escolha inválida")

if __name__ == "__main__":
    main() 