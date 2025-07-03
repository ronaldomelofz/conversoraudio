# 🎯 GUIA COMPLETO - TRANSCRITOR AVANÇADO

## 📋 Visão Geral

Este projeto oferece um sistema completo de transcrição de áudio/vídeo para texto, inspirado nas melhores práticas de projetos GitHub e incorporando funcionalidades profissionais.

### ✅ Funcionalidades Implementadas

- **Interface CLI profissional** com argumentos estruturados
- **Suporte a múltiplos formatos** (MP3, MP4, WAV, M4A, OGG, FLAC, AAC, WMA, WebM)
- **Organização automática de arquivos** com labels e diretórios
- **Prevenção de sobrescrita** de arquivos existentes
- **Timestamps precisos** na transcrição
- **Estimativas de tempo** baseadas no tamanho do arquivo
- **Múltiplos idiomas** com detecção automática
- **Sistema sem FFmpeg** (usa Librosa diretamente)
- **Relatórios detalhados** com estatísticas completas

## 🚀 Instalação e Configuração

### 1. Dependências Principais
```bash
pip install librosa openai-whisper numpy
```

### 2. Verificar Instalação
```bash
python transcritor_avancado_cli.py --list-models
```

## 💻 Uso do Sistema

### Interface CLI Completa

#### Comando Básico
```bash
python transcritor_avancado_cli.py --file seu_arquivo.mp3
```

#### Exemplos Avançados

**Transcrição com label específico:**
```bash
python transcritor_avancado_cli.py --file reuniao.mp4 --label reuniao_board --model small
```

**Transcrição em inglês:**
```bash
python transcritor_avancado_cli.py --file podcast.wav --language en --out-dir ./podcasts
```

**Transcrição sem timestamps:**
```bash
python transcritor_avancado_cli.py --file aula.m4a --label aula01 --no-timestamps
```

**Modo silencioso:**
```bash
python transcritor_avancado_cli.py --file video.mp4 --quiet
```

### Argumentos Disponíveis

| Argumento | Abreviação | Descrição |
|-----------|------------|-----------|
| `--file` | `-f` | Arquivo de áudio/vídeo (obrigatório) |
| `--model` | `-m` | Modelo Whisper (tiny, base, small, medium, large) |
| `--label` | `-l` | Identificador para organização |
| `--out-dir` | `-o` | Diretório de saída |
| `--language` | `-lang` | Idioma do áudio (pt, en, es, etc.) |
| `--no-timestamps` | - | Desativa timestamps |
| `--temperature` | `-t` | Temperatura de sampling (0.0-1.0) |
| `--quiet` | `-q` | Modo silencioso |
| `--list-models` | - | Lista modelos disponíveis |
| `--version` | `-v` | Versão do sistema |

## 🤖 Modelos Whisper

### Recomendações por Uso

| Modelo | Tamanho | Velocidade | Precisão | Uso Recomendado |
|--------|---------|------------|----------|-----------------|
| `tiny` | ~39 MB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Testes rápidos |
| `base` | ~74 MB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | **Uso geral** |
| `small` | ~244 MB | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Alta qualidade |
| `medium` | ~769 MB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Precisão máxima |
| `large` | ~1550 MB | ⚡ | ⭐⭐⭐⭐⭐ | Profissional |

### Estimativas de Tempo (por MB)

- **tiny**: ~5 segundos/MB
- **base**: ~9 segundos/MB *(recomendado)*
- **small**: ~21 segundos/MB
- **medium**: ~42 segundos/MB
- **large**: ~84 segundos/MB

## 📁 Organização de Arquivos

### Estrutura de Saída
```
transcricoes/
├── label1/
│   ├── arquivo1_label1_transcricao.txt
│   └── arquivo2_label1_transcricao_1.txt
├── label2/
│   └── arquivo3_label2_transcricao.txt
└── arquivo_sem_label_transcricao.txt
```

### Formato do Arquivo de Saída

```
🎯 TRANSCRIÇÃO AVANÇADA COM CLI
================================================================================
📁 Arquivo Original: reuniao.mp4
🤖 Modelo Whisper: base
🌍 Idioma Detectado: pt
🏷️  Label: reuniao_board
📅 Data/Hora: 15/01/2025 14:30:45
⏱️  Tempo Processamento: 120.5s (2.0 min)
🎵 Duração Áudio: 600.0s (10.0 min)
⚡ Velocidade: 5.0x tempo real
📊 Arquivo: 15.2 MB
📊 Estatísticas: 5,234 chars, 891 palavras
================================================================================

TRANSCRIÇÃO COMPLETA:
------------------------------------------------------------
Bem-vindos à reunião do conselho...

TRANSCRIÇÃO COM TIMESTAMPS:
------------------------------------------------------------
[00:00 - 00:05] Bem-vindos à reunião do conselho
[00:05 - 00:12] Vamos iniciar com o primeiro item da pauta
...
```

## 🌍 Suporte a Idiomas

### Idiomas Suportados
- `pt` - Português (padrão)
- `en` - Inglês
- `es` - Espanhol
- `fr` - Francês
- `de` - Alemão
- `it` - Italiano
- `auto` - Detecção automática

### Dica de Uso
```bash
# Para detecção automática
python transcritor_avancado_cli.py --file arquivo.mp3 --language auto
```

## 🔧 Funcionalidades de Segurança

### Verificações Automáticas
- ✅ Validação de formato de arquivo
- ✅ Verificação de existência do arquivo
- ✅ Prevenção de sobrescrita acidental
- ✅ Numeração automática de arquivos duplicados
- ✅ Validação de dependências

### Tratamento de Erros
- Mensagens claras de erro
- Logs detalhados para debugging
- Rollback em caso de falha
- Verificação de integridade

## 📊 Comparação com Projeto GitHub

### Funcionalidades Herdadas do [Projeto Rafael Omodei](https://github.com/rafaelomodei/audio-to-text)

✅ **Implementadas:**
- Interface CLI profissional
- Sistema de labels/identificadores
- Organização em diretórios
- Prevenção de sobrescrita
- Suporte a múltiplos formatos
- Gestão de arquivos de saída

🔄 **Melhoradas:**
- **Sem dependência de FFmpeg** (nossa solução elimina esse problema)
- **Mais formatos suportados** (WebM, WMA, etc.)
- **Timestamps mais precisos** com word-level
- **Estimativas de tempo** mais accuradas
- **Interface mais rica** com estatísticas completas

🚀 **Inovações Próprias:**
- Pipeline Librosa→Whisper direto
- Sistema de estimativas avançado
- Relatórios com metadados completos
- Múltiplos modelos Whisper
- Detecção automática de idioma

## 🎯 Casos de Uso Práticos

### 1. Reuniões de Trabalho
```bash
python transcritor_avancado_cli.py --file reuniao_mensal.mp4 --label reuniao_janeiro --model base
```

### 2. Aulas/Palestras
```bash
python transcritor_avancado_cli.py --file aula_python.mp3 --label curso_python --out-dir ./aulas
```

### 3. Podcasts/Entrevistas
```bash
python transcritor_avancado_cli.py --file podcast_ep01.wav --label podcast --language auto --model small
```

### 4. Conteúdo Multilíngue
```bash
python transcritor_avancado_cli.py --file video_ingles.mp4 --language en --model medium
```

## 🛠️ Troubleshooting

### Problemas Comuns

**Erro de dependências:**
```bash
pip install librosa openai-whisper numpy --upgrade
```

**Arquivo não encontrado:**
- Verifique o caminho completo
- Use aspas em nomes com espaços: `--file "meu arquivo.mp3"`

**Modelo não baixa:**
- Verifique conexão com internet
- Modelos são baixados automaticamente na primeira execução

**Performance lenta:**
- Use modelo `tiny` para testes
- Considere usar `base` para equilíbrio
- Arquivo muito grande? Divida em partes menores

## 📈 Performance e Otimização

### Dicas de Performance
1. **Escolha o modelo adequado** ao seu hardware
2. **Use `base` para maioria dos casos**
3. **Considere dividir arquivos > 100MB**
4. **SSD melhora significativamente a velocidade**

### Recursos do Sistema
- **RAM mínima**: 4GB (recomendado: 8GB+)
- **Espaço**: ~2GB para modelos + espaço dos arquivos
- **CPU**: Qualquer processador moderno
- **GPU**: Opcional (acelera modelos large)

## 🤝 Contribuições e Melhorias

Este sistema foi desenvolvido com base em:
- [Projeto Rafael Omodei](https://github.com/rafaelomodei/audio-to-text)
- Melhores práticas da comunidade Python
- Feedback de testes com arquivos reais

### Próximas Funcionalidades Planejadas
- [ ] Interface gráfica (GUI)
- [ ] Processamento em lote
- [ ] Integração com APIs de nuvem
- [ ] Export para diferentes formatos (JSON, SRT, etc.)
- [ ] Sistema de plugins

---

**💡 Dica Final:** Use sempre o comando `--help` para ver todas as opções disponíveis!

```bash
python transcritor_avancado_cli.py --help
``` 