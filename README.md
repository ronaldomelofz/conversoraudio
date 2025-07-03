# Sistema de Transcrição de Áudio

Este sistema permite transcrever arquivos de áudio MP3 (e outros formatos) para texto usando diferentes tecnologias de reconhecimento de voz.

## 🚀 Características

- **Suporte a MP3 e outros formatos de áudio**
- **Dois métodos de transcrição:**
  - **Whisper (OpenAI)**: Mais preciso, funciona offline
  - **Google Speech Recognition**: Requer conexão com internet
- **Processamento inteligente**: Divide arquivos grandes em segmentos
- **Conversão automática**: Converte MP3 para WAV automaticamente
- **Salvamento automático**: Salva transcrições em arquivos de texto
- **Interface em português**

## 📋 Pré-requisitos

### Python
- Python 3.7 ou superior

### FFmpeg (obrigatório)
O FFmpeg é necessário para processar arquivos de áudio.

#### Windows:
```bash
# Opção 1: Usando winget
winget install ffmpeg

# Opção 2: Usando chocolatey
choco install ffmpeg

# Opção 3: Download manual
# Baixe de https://ffmpeg.org/download.html
# Extraia e adicione à variável PATH
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### macOS:
```bash
brew install ffmpeg
```

## 🛠️ Instalação

### Método 1: Instalação Automática
```bash
python instalar_dependencias.py
```

### Método 2: Instalação Manual
```bash
# Instalar dependências
pip install -r requirements.txt

# Ou instalar individualmente:
pip install speechrecognition==3.10.0
pip install pydub==0.25.1
pip install openai-whisper
pip install torch
pip install torchaudio
```

## 🎯 Como Usar

### 1. Executar o Sistema
```bash
python transcricao_audio.py
```

### 2. Escolher Método de Transcrição
O sistema oferece três opções:
- **Opção 1**: Whisper (recomendado) - Mais preciso, funciona offline
- **Opção 2**: Google Speech Recognition - Requer internet
- **Opção 3**: Ambos os métodos para comparação

### 3. Arquivo de Teste
O sistema está configurado para processar o arquivo:
`Carros Elétricos em Condomínios - Diretriz Nacional.mp3`

Certifique-se de que este arquivo está na pasta raiz do projeto.

## 📁 Estrutura dos Arquivos

```
projeto/
├── transcricao_audio.py          # Sistema principal
├── instalar_dependencias.py      # Instalador automático
├── requirements.txt              # Dependências Python
├── README.md                     # Este arquivo
└── Carros Elétricos em Condomínios - Diretriz Nacional.mp3  # Arquivo de teste
```

## 📤 Arquivos de Saída

O sistema gera automaticamente:
- `[nome_do_arquivo]_transcricao.txt` - Transcrição completa
- Inclui metadados (arquivo original, data da transcrição)

## ⚙️ Configurações Avançadas

### Usar com Outros Arquivos
Para transcrever outros arquivos, modifique a variável `arquivo_mp3` no arquivo `transcricao_audio.py`:

```python
arquivo_mp3 = "caminho/para/seu/arquivo.mp3"
```

### Ajustar Segmentação
Para arquivos muito longos, o sistema divide em segmentos de 60 segundos. Para alterar:

```python
# No método transcrever_arquivo
segmentos = self.dividir_audio(caminho_wav, duracao_segmento=120)  # 120 segundos
```

### Modelos Whisper Disponíveis
- `tiny` - Mais rápido, menos preciso
- `base` - Padrão, bom equilíbrio
- `small` - Mais preciso que base
- `medium` - Ainda mais preciso
- `large` - Máxima precisão, mais lento

Para alterar o modelo:
```python
self.modelo_whisper = whisper.load_model("small")  # Ou outro modelo
```

## 🔧 Solução de Problemas

### Erro: "FFmpeg not found"
- Certifique-se de que FFmpeg está instalado e no PATH
- Reinicie o terminal após a instalação

### Erro: "Module not found"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de memória com arquivos grandes
- O sistema divide automaticamente em segmentos
- Para arquivos muito grandes, reduza o tamanho dos segmentos

### Google Speech Recognition não funciona
- Verifique sua conexão com internet
- O serviço Google pode ter limitações de uso

## 📈 Performance

### Whisper
- **Vantagens**: Mais preciso, funciona offline, suporta muitos idiomas
- **Desvantagens**: Requer mais recursos computacionais

### Google Speech Recognition
- **Vantagens**: Rápido, pouco uso de recursos
- **Desvantagens**: Requer internet, limitações de uso

## 🤝 Contribuição

Sinta-se livre para melhorar este sistema:
1. Adicionar suporte a mais formatos
2. Implementar interface gráfica
3. Adicionar mais opções de configuração
4. Otimizar performance

## 📄 Licença

Este projeto é open source e está disponível sob a licença MIT. 