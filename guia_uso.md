# 🎵 Guia de Uso - Sistema de Transcrição de Áudio

## ✅ Sistema Pronto!

O sistema de transcrição foi criado e está funcionando! Aqui está tudo que você precisa saber:

## 📁 Arquivos Criados

1. **`transcricao_simples.py`** - Sistema principal (RECOMENDADO)
2. **`transcricao_audio.py`** - Sistema completo com múltiplas opções
3. **`converter_mp3.py`** - Conversor MP3 para WAV
4. **`instalar_dependencias.py`** - Instalador automático
5. **`teste_rapido.py`** - Teste do sistema
6. **`requirements.txt`** - Lista de dependências

## 🚀 Como Usar (Método Mais Simples)

### Passo 1: Abra um novo terminal
**IMPORTANTE**: Abra um novo terminal/PowerShell para que o FFmpeg seja reconhecido.

### Passo 2: Execute o sistema
```bash
python transcricao_simples.py
```

### Passo 3: Escolha o modelo
- **Opção 1 (tiny)**: Mais rápido, para testes
- **Opção 2 (base)**: **RECOMENDADO** - Bom equilíbrio
- **Opção 3 (small)**: Mais preciso, mais lento

### Passo 4: Aguarde
O sistema irá:
1. Carregar o modelo Whisper
2. Transcrever o arquivo MP3
3. Salvar o resultado em um arquivo TXT

## 🔧 Se Houver Problemas com FFmpeg

### Solução A: Reiniciar Terminal
1. Feche completamente o terminal atual
2. Abra um novo PowerShell como Administrador
3. Navegue até a pasta do projeto
4. Execute: `python transcricao_simples.py`

### Solução B: Conversão Manual
Se o FFmpeg ainda não funcionar, use um conversor online:
1. Vá para https://convertio.co/mp3-wav/
2. Faça upload do arquivo "Carros Elétricos em Condomínios - Diretriz Nacional.mp3"
3. Baixe o arquivo WAV
4. Coloque o arquivo WAV na pasta do projeto
5. Modifique a linha no `transcricao_simples.py`:
   ```python
   arquivo_mp3 = "nome_do_arquivo.wav"  # Use o arquivo WAV convertido
   ```

### Solução C: Instalar FFmpeg Manualmente
1. Baixe FFmpeg de: https://ffmpeg.org/download.html
2. Extraia para `C:\ffmpeg`
3. Adicione `C:\ffmpeg\bin` ao PATH do Windows
4. Reinicie o computador

## 📊 Resultados Esperados

Após a execução bem-sucedida:
- ✅ Arquivo de transcrição será criado: `Carros Elétricos em Condomínios - Diretriz Nacional_transcricao.txt`
- ✅ Mostrará prévia da transcrição na tela
- ✅ Indicará tempo de processamento

## 🎯 Modelos Whisper - Guia de Escolha

| Modelo | Tamanho | Velocidade | Precisão | Recomendado para |
|--------|---------|------------|----------|------------------|
| tiny   | ~30 MB  | Muito rápido | Básica | Testes rápidos |
| base   | ~150 MB | Rápido | Boa | **Uso geral** |
| small  | ~500 MB | Médio | Muito boa | Arquivos importantes |
| medium | ~1.5 GB | Lento | Excelente | Máxima qualidade |
| large  | ~3 GB   | Muito lento | Perfeita | Uso profissional |

## ⚡ Tempo de Processamento Estimado

Para o arquivo de ~80 MB:
- **tiny**: ~2-3 minutos
- **base**: ~5-8 minutos  ⭐ **RECOMENDADO**
- **small**: ~10-15 minutos
- **medium**: ~20-30 minutos
- **large**: ~40-60 minutos

## 🆘 Solução de Problemas

### Erro: "Module not found"
```bash
pip install openai-whisper torch
```

### Erro: "FFmpeg not found"
- Abra novo terminal
- Ou use conversor online para WAV

### Erro: "Arquivo não encontrado"
- Verifique se o arquivo MP3 está na pasta correta
- Use caminho completo se necessário

### Arquivo muito grande
- Use modelo "tiny" para teste
- Divida o arquivo em partes menores

## 💡 Dicas

1. **Primeira vez**: Use modelo "base" para equilibrar velocidade e qualidade
2. **Internet**: Whisper funciona 100% offline
3. **Qualidade**: Arquivos com menos ruído = melhor transcrição
4. **Paciência**: Processo normal demora alguns minutos

## 🎉 Pronto para Usar!

Agora você tem um sistema completo de transcrição. Execute:

```bash
python transcricao_simples.py
```

E siga as instruções na tela! 🚀 