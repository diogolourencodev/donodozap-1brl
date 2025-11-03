# Dono do Zap - Hack 1 BRL

Um script Python para interagir com a API do Dono do Zap, permitindo consultar contas vinculadas a números de telefone e gerar ordens de pagamento PIX.

## 📋 Funcionalidades

- **Consulta de Contas**: Lista todas as contas vinculadas a um número de telefone
- **Geração de Ordens PIX**: Cria ordens de pagamento PIX no valor de R$ 1,00
- **Monitoramento em Tempo Real**: Verifica o status do pagamento automaticamente
- **Interface Amigável**: Feedback visual com emojis e mensagens claras

## 🚀 Instalação

### Pré-requisitos
- Python 3.6 ou superior
- Pip (gerenciador de pacotes do Python)

### Dependências
Instale as dependências necessárias:

```bash
pip install requests
```

## 💻 Como Usar

### 1. Consulta Simples (Apenas Listar Contas)
```bash
python3 donodozap.py 11999999999
```

**Saída esperada:**
```
Contas encontradas: ['João Silva', 'Maria Santos']

📋 CONTAS DISPONÍVEIS:
  0: João Silva
  1: Maria Santos

💡 Para gerar uma ordem de pagamento, use:
   python script.py 11999999999 <ID>
   Exemplo: python script.py 11999999999 0
```

### 2. Consulta com Geração de Ordem PIX
```bash
python3 donodozap.py 11999999999 0
```

**Saída esperada:**
```
🔄 Criando ordem para: João Silva (ID: 0)
💰 Valor de pagamento: R$ 1,00
📝 Código gerado: 8e34f508-24b0-4efd-a1d5-22097bc6aea9

⏳ Verificando status do pagamento...
🔄 Tentativa 1: Status - WAITING_PAYMENT
⏰ Aguardando pagamento...
🔄 Tentativa 2: Status - PAID
✅ PAGAMENTO CONFIRMADO!
🔗 Resultado aqui:
   https://donodozap.com/results/a76d9e46-b07a-4489-bf9a-cf336ec07e3b
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição | Exemplo |
|-----------|-------------|-----------|---------|
| `numero` | ✅ | Número de telefone (apenas números, com DDD) | `11999999999` |
| `nome_id` | ❌ | ID da conta para gerar ordem PIX (0, 1, 2, ...) | `0` |

## 🔄 Fluxo do Script

1. **Validação de Argumentos** → Verifica se os parâmetros foram fornecidos corretamente
2. **Consulta à API** → Busca contas vinculadas ao número informado
3. **Listagem de Contas** → Mostra todas as contas disponíveis com seus IDs
4. **Geração de Ordem** (opcional) → Cria ordem PIX se ID for fornecido
5. **Monitoramento** → Verifica status do pagamento a cada 5 segundos
6. **Resultado Final** → Exibe link com os resultados quando pago

## ⚙️ Configuração

### Headers da Requisição
O script utiliza os seguintes headers para simular um navegador real:
```python
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}
```

### Endpoints da API
- **Verificação**: `POST https://donodozap.com/api/verify`
- **Criação de Ordem**: `POST https://donodozap.com/api/create-order`
- **Verificação de Status**: `GET https://donodozap.com/api/check-order?txid={txid}`

## 🎯 Exemplos Práticos

### Exemplo 1: Descobrir contas de um número
```bash
python3 donodozap.py 21988887777
```

### Exemplo 2: Gerar PIX para a primeira conta
```bash
python3 donodozap.py 21988887777 0
```

### Exemplo 3: Gerar PIX para a segunda conta
```bash
python3 donodozap.py 21988887777 1
```

## ⏱️ Configuração de Timeout

O script monitora o pagamento por até **75 segundos** (15 tentativas × 5 segundos):
```python
max_attempts = 15  # 75 segundos no total
```

## 🛠️ Solução de Problemas

### Erros Comuns

1. **"Nenhuma conta encontrada!"**
   - Verifique se o número está correto
   - Confirme se o formato é apenas números com DDD

2. **"ID X inválido"**
   - Use um ID entre 0 e o número total de contas -1
   - Execute primeiro sem ID para ver as contas disponíveis

3. **"Erro na requisição"**
   - Verifique sua conexão com a internet
   - Confirme se o site donodozap.com está acessível

### Códigos de Status
- `✅` - Sucesso
- `❌` - Erro
- `🔄` - Processamento
- `⏳` - Aguardando
- `💰` - Pagamento
- `📋` - Listagem
- `🔗` - Link

## 📄 Licença

Este projeto é para fins educacionais. Use com responsabilidade.

## ⚠️ Aviso Legal

Este script foi desenvolvido para fins educacionais e de testes. O uso deve estar em conformidade com os Termos de Serviço do Dono do Zap e leis aplicáveis. O desenvolvedor não se responsabiliza pelo uso indevido desta ferramenta.

---

**Desenvolvido para fins educacionais** 📚
