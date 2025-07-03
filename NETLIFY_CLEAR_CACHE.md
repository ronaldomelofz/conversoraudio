# 🚨 INSTRUÇÕES URGENTES - LIMPEZA MANUAL DO NETLIFY

## ⚠️ PROBLEMA DETECTADO
O erro "Unsupported model type: whisper" persiste mesmo após reset completo do projeto.

## 🔧 SOLUÇÃO MANUAL NECESSÁRIA

### 1. ACESSE O PAINEL DO NETLIFY
- Site: https://app.netlify.com
- Login: conta vinculada ao GitHub ronaldomelofz/conversoraudio

### 2. LIMPE O CACHE MANUALMENTE
```
Site Settings → Build & deploy → Build settings
```
- Clique em "Clear cache"
- Clique em "Trigger deploy"

### 3. FORCE REDEPLOY
```
Deploys → Trigger deploy → Clear cache and deploy site
```

### 4. VERIFIQUE VARIÁVEIS DE AMBIENTE
```
Site Settings → Environment variables
```
- Remova qualquer variável relacionada a Whisper
- Adicione: NODE_VERSION=18

### 5. REBUILD HOOKS
```
Site Settings → Build hooks → Add build hook
```
- Nome: "Force Rebuild"
- Branch: main

## 🎯 RESULTADO ESPERADO
Após essas ações, o site deve carregar:
- Interface com "FORÇA BRUTA v2025010315"
- Sistema funcional sem erros Whisper
- Cache completamente limpo

## 📞 CONTATO TÉCNICO
Se o problema persistir, entre em contato:
- Email: ronaldomelofz@gmail.com
- GitHub: issues no repositório 