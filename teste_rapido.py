"""
Script de teste rápido para o sistema de transcrição
Use este script para testar rapidamente se tudo está funcionando
"""

import os
import sys

def verificar_arquivo():
    """Verifica se o arquivo MP3 está presente"""
    arquivo = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
    if os.path.exists(arquivo):
        print(f"✓ Arquivo encontrado: {arquivo}")
        # Mostrar informações do arquivo
        tamanho = os.path.getsize(arquivo) / (1024 * 1024)  # MB
        print(f"  Tamanho: {tamanho:.2f} MB")
        return True
    else:
        print(f"✗ Arquivo não encontrado: {arquivo}")
        return False

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    print("Verificando dependências...")
    
    deps = [
        ('speech_recognition', 'SpeechRecognition'),
        ('pydub.AudioSegment', 'PyDub'),
        ('whisper', 'OpenAI Whisper'),
        ('torch', 'PyTorch')
    ]
    
    instaladas = []
    faltando = []
    
    for modulo, nome in deps:
        try:
            if '.' in modulo:
                # Para imports como 'pydub.AudioSegment'
                parts = modulo.split('.')
                module = __import__(parts[0])
                for part in parts[1:]:
                    module = getattr(module, part)
            else:
                __import__(modulo)
            print(f"✓ {nome}")
            instaladas.append(nome)
        except (ImportError, AttributeError):
            print(f"✗ {nome} - NÃO INSTALADO")
            faltando.append(nome)
    
    return len(faltando) == 0, instaladas, faltando

def teste_whisper_simples():
    """Teste básico do Whisper com um arquivo pequeno"""
    print("\n=== TESTE WHISPER (MÉTODO RECOMENDADO) ===")
    
    try:
        import whisper
        from transcricao_audio import TranscritorAudio
        
        print("Carregando modelo Whisper (base)...")
        transcritor = TranscritorAudio()
        
        arquivo = "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
        
        print("Iniciando transcrição...")
        print("NOTA: Este processo pode demorar alguns minutos dependendo do tamanho do arquivo")
        print("      e da velocidade do seu computador.\n")
        
        # Transcrever sem dividir em segmentos para teste mais rápido
        transcricao = transcritor.transcrever_arquivo(arquivo, usar_whisper=True, dividir=False)
        
        if transcricao:
            print("=== TRANSCRIÇÃO CONCLUÍDA ===")
            print(f"Primeiros 200 caracteres:\n{transcricao[:200]}...")
            
            # Salvar resultado
            arquivo_saida = transcritor.salvar_transcricao(transcricao, arquivo)
            print(f"\nTranscrição completa salva em: {arquivo_saida}")
            
            return True
        else:
            print("✗ Falha na transcrição")
            return False
            
    except Exception as e:
        print(f"✗ Erro no teste: {e}")
        return False

def main():
    print("=== TESTE RÁPIDO DO SISTEMA DE TRANSCRIÇÃO ===\n")
    
    # Verificar arquivo
    if not verificar_arquivo():
        print("\nColoque o arquivo MP3 na pasta raiz e tente novamente.")
        return
    
    print()
    
    # Verificar dependências
    deps_ok, instaladas, faltando = verificar_dependencias()
    
    if not deps_ok:
        print(f"\n✗ Dependências faltando: {', '.join(faltando)}")
        print("Execute: python instalar_dependencias.py")
        return
    
    print(f"\n✓ Todas as dependências estão instaladas!")
    
    # Perguntar se quer fazer teste
    print("\nDeseja fazer um teste de transcrição? (s/n): ", end="")
    resposta = input().lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\nINICIANDO TESTE...")
        print("=" * 50)
        
        sucesso = teste_whisper_simples()
        
        if sucesso:
            print("\n" + "=" * 50)
            print("✓ TESTE CONCLUÍDO COM SUCESSO!")
            print("O sistema está funcionando corretamente.")
            print("Use 'python transcricao_audio.py' para o sistema completo.")
        else:
            print("\n" + "=" * 50)
            print("✗ TESTE FALHOU")
            print("Verifique as dependências e tente novamente.")
    else:
        print("\nTeste cancelado. Use 'python transcricao_audio.py' quando estiver pronto.")

if __name__ == "__main__":
    main() 