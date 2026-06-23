# 🚀 Como Executar o IADvogado

## Passo 1: Instalar Dependências

```bash
cd iadvogado
pip install -r requirements.txt
```

## Passo 2: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as configurações:

```bash
# Copiar exemplo
cp iadvogado/config/env_example.txt .env
```

Abra o arquivo `.env` e configure as seguintes variáveis essenciais:
- `OPENROUTER_API_KEY`: Necessária para que a IA (Llama 3.3 via nuvem) gere as simplificações de textos. Sem ela, o sistema responderá com textos estáticos de fallback.
- `DATAJUD_API_KEY`: Necessária para consultar processos reais pelo número do processo (integração CNJ).

**Nota**: Embora o sistema inicie sem essas chaves usando fallbacks locais, a experiência real do chatbot requer que essas duas chaves estejam devidamente preenchidas.

## Passo 3: Iniciar o Servidor

### Opção A: Da raiz do projeto (Recomendado)
```bash
# Na raiz do projeto (IADvogado/)
python run_server.py
```

### Opção B: Usando o script dentro de iadvogado
```bash
# Na raiz do projeto (IADvogado/)
python iadvogado/run.py
```

### Opção C: Usando uvicorn diretamente
```bash
# Na raiz do projeto (IADvogado/)
uvicorn iadvogado.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Passo 4: Acessar o Chatbot

Depois que o servidor iniciar, acesse:

- **Chatbot**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## ⚠️ Solução de Problemas

### Erro: `ModuleNotFoundError: No module named 'iadvogado'`

**Causa**: Executando de dentro da pasta `iadvogado/`

**Solução**: Execute sempre da **raiz do projeto** (pasta `IADvogado/`)

```bash
# ❌ ERRADO (dentro de iadvogado/)
cd iadvogado
python run.py

# ✅ CORRETO (da raiz)
cd IADvogado
python run_server.py
```

### Erro: `ModuleNotFoundError: No module named 'uvicorn'`

**Solução**: Instale as dependências
```bash
cd iadvogado
pip install -r requirements.txt
```

### Erro ao carregar configurações

**Solução**: Crie o arquivo `.env` na raiz com as variáveis necessárias, ou o sistema usará valores padrão.

## 📝 Notas Importantes

- O servidor inicia em `http://0.0.0.0:8000` por padrão
- O modo `reload=True` está ativo para desenvolvimento
- Certifique-se de estar na **raiz do projeto** antes de executar

