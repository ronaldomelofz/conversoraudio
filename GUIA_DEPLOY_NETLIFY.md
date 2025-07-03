# 🚀 Guia Completo: Deploy Manual no Netlify 2025

## 📋 Resumo Executivo

Este guia mostra **3 métodos diferentes** para fazer deploy do seu projeto no Netlify, desde o mais simples (arrastar e soltar) até o automático via GitHub.

---

## 🎯 Método 1: Deploy Manual (Drag & Drop) - **MAIS RÁPIDO**

### ✅ Quando Usar
- Projeto HTML/CSS/JS puro
- Teste rápido
- Sem necessidade de Git

### 📝 Passos Detalhados

1. **Acesse o Netlify**
   - Vá para: https://app.netlify.com
   - Faça login (pode usar conta GitHub)

2. **Inicie o Deploy Manual**
   - Clique em **"Add new project"**
   - Selecione **"Deploy manually"**

3. **Arraste e Solte**
   - Arraste sua pasta do projeto inteira
   - OU clique para selecionar
   - Aguarde o upload (barra de progresso)

4. **Deploy Concluído**
   - URL gerada automaticamente (ex: `amazing-site-123.netlify.app`)
   - Site ativo em segundos!

### ⚠️ Importante
- Arquivo principal deve se chamar `index.html`
- Máximo 100MB por deploy
- Para updates: repita o processo

---

## 🔄 Método 2: GitHub + Deploy Automático - **RECOMENDADO**

### ✅ Quando Usar
- Projetos contínuos
- Colaboração em equipe
- Versionamento necessário

### 📝 Passos Detalhados

1. **Prepare o Repositório GitHub**
   ```bash
   # Se ainda não tem Git no projeto:
   git init
   git add .
   git commit -m "🚀 Deploy inicial Netlify"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
   git push -u origin main
   ```

2. **Conecte ao Netlify**
   - Acesse: https://app.netlify.com
   - **"Add new project"** → **"Import an existing project"**
   - Escolha **"GitHub"**
   - Autorize a conexão

3. **Configure o Deploy**
   ```
   Repository: seu-repo-name
   Branch to deploy: main
   Build command: (deixar VAZIO)
   Publish directory: . (ponto)
   ```

4. **Deploy Automático**
   - Clique **"Deploy site"**
   - A cada push no GitHub = novo deploy!

---

## ⚙️ Método 3: Projeto com Configurações Especiais

### 📁 Estrutura Necessária

```
meu-projeto/
├── index.html          # Página principal
├── netlify.toml        # Configurações
├── _headers           # Headers HTTP
├── _redirects         # Redirecionamentos
└── package.json       # Metadados (opcional)
```

### 📄 Arquivos de Configuração

#### `netlify.toml`
```toml
[build]
  command = ""
  publish = "."
  ignore = "exit 0"

[build.environment]
  SKIP_INSTALL = "true"
  DISABLE_YARN = "true"

[[headers]]
  for = "/*"
  [headers.values]
    Cache-Control = "no-store, no-cache, must-revalidate"
    X-Frame-Options = "DENY"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### `_headers`
```
/*
  Cache-Control: no-store, no-cache, must-revalidate
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Permissions-Policy: microphone=(self)

/*.html
  Content-Type: text/html; charset=utf-8
```

---

## 🛠️ Solução de Problemas Comuns

### ❌ Problema: "Build Failed"
**Solução**:
```toml
# No netlify.toml:
[build]
  command = ""
  ignore = "exit 0"
```

### ❌ Problema: "Page Not Found" 
**Solução**:
- Arquivo principal deve ser `index.html`
- Ou configure redirect em `_redirects`:
```
/   /sua-pagina.html   200
```

### ❌ Problema: "Multiple build commands found"
**Solução**:
- Remova `config.toml`, `hugo.toml`, etc.
- Ou especifique no `netlify.toml`:
```toml
[build]
  command = "echo 'No build needed'"
```

---

## 🎨 Personalização Avançada

### 🌐 Domínio Personalizado
1. **Site Settings** → **Domain management**
2. **Add custom domain**
3. Configure DNS (A record para 75.2.60.5)

### 📊 Variáveis de Ambiente
```
Site Settings → Environment Variables
→ Add variable: API_KEY = seu-valor
```

### 🔐 Headers de Segurança
```
# _headers
/*
  Content-Security-Policy: default-src 'self'
  Strict-Transport-Security: max-age=31536000
```

---

## 🚨 Dicas Pro

### ⚡ Deploy Instantâneo
```bash
# CLI Netlify (avançado)
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir .
```

### 🔄 Auto-Deploy com Webhook
- **Site Settings** → **Build hooks**
- **Add build hook** → URL gerada
- Use para trigger deploys externos

### 📱 Preview Branches
- Branches automáticos geram preview URLs
- Teste antes de merge para main

---

## ✅ Checklist Final

- [ ] `index.html` existe na raiz
- [ ] Projeto funciona localmente (`python -m http.server 8080`)
- [ ] Arquivos de configuração criados
- [ ] Repository GitHub atualizado
- [ ] Deploy testado e funcionando
- [ ] URL personalizada configurada (opcional)

---

## 🆘 Suporte

- **Documentação**: https://docs.netlify.com
- **Fórum**: https://answers.netlify.com
- **Status**: https://netlifystatus.com

---

**🎉 Pronto! Seu site está no ar!**

*Deploy realizado com sucesso ✨* 