# 🎵 Conversor de Áudio - Sistema Completo

Sistema avançado de conversão e transcrição de áudio desenvolvido com tecnologia web moderna.

## ✨ Funcionalidades

- 🎵 **Múltiplos Formatos**: MP3, WAV, M4A, OGG, FLAC, AAC, WMA, MP4
- 🎤 **Gravação de Microfone**: Grave áudio diretamente no navegador
- 🔄 **Processamento Local**: Sem envio de dados para servidores
- 📱 **Interface Responsiva**: Funciona em desktop, tablet e mobile
- ⚡ **Zero Dependências**: 100% HTML, CSS e JavaScript puro

## 🌐 Deploy no Netlify

### Status Atual
- **Repositório**: https://github.com/ronaldomelofz/conversoraudio
- **Branch**: main
- **Último commit**: ff164de (v2025010320)

### 🚀 Deploy Automático

1. **Acesse**: https://app.netlify.com
2. **Conecte GitHub**: Autorize acesso ao repositório
3. **Configurações de Deploy**:
   ```
   Repository: ronaldomelofz/conversoraudio
   Branch: main
   Build command: (deixar vazio)
   Publish directory: .
   ```

### ⚙️ Configurações Especiais

O projeto inclui configurações otimizadas para Netlify:

- **`netlify.toml`**: Configuração principal com bypass de dependências
- **`_headers`**: Headers HTTP otimizados e cache busting
- **`package.json`**: Vazio para evitar instalação de dependências

### 🛠️ Solução de Problemas

Se o build falhar:

1. **Verificar configurações**:
   - Build command: (vazio)
   - Publish directory: `.`
   
2. **Variáveis de ambiente** (opcional):
   ```
   SKIP_INSTALL=true
   DISABLE_YARN=true
   NODE_ENV=production
   ```

3. **Deploy manual**:
   - Faça download do repositório
   - Arraste a pasta para o Netlify

## 🏗️ Deploy Alternativo - Vercel

Para deploy rápido no Vercel:

```bash
npm install -g vercel
vercel --prod
```

## 📂 Estrutura do Projeto

```
conversoraudio/
├── index.html          # Aplicação principal
├── netlify.toml        # Configuração Netlify
├── _headers           # Headers HTTP
├── package.json       # Metadata (vazio)
├── vercel.json        # Configuração Vercel
└── README.md          # Documentação
```

## 🎯 Características Técnicas

- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **APIs Web**: MediaRecorder, FileReader, URL, Drag & Drop
- **Responsivo**: Grid CSS, Flexbox
- **PWA Ready**: Meta tags preparadas
- **SEO Otimizado**: Meta tags completas

## 🔧 Desenvolvimento Local

```bash
# Clone o repositório
git clone https://github.com/ronaldomelofz/conversoraudio.git

# Entre na pasta
cd conversoraudio

# Inicie servidor local
python -m http.server 8080

# Acesse http://localhost:8080
```

## 📝 Histórico de Versões

- **v2025010320**: Solução definitiva Netlify com sistema completo
- **v2025010319**: Migração para Vercel
- **v2025010318**: Tentativas de correção Netlify
- **v2025010317**: Sistema minimalista
- **v2025010316**: Build fix
- **v2025010315**: Força bruta rebuild

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Desenvolvedor

**Ronaldo Melo**
- GitHub: [@ronaldomelofz](https://github.com/ronaldomelofz)
- Email: ronaldomelofz@gmail.com

---

🚀 **Sistema 100% funcional e pronto para deploy!** 🚀 