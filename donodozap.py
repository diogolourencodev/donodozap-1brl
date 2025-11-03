import requests
import json
import sys
import random
import string
import time
import uuid

if len(sys.argv) < 2:
    print("Uso: python3 donodozap.py <numero> [nome_id]")
    print("Exemplos:")
    print("  python3 donodozao.py 11999999999          # Apenas consulta")
    print("  python3 donodozap.py 11999999999 0        # Consulta e gera ordem para ID 0")
    sys.exit(1)

numero = sys.argv[1]

if len(sys.argv) >= 3:
    nome_id = sys.argv[2]
    id_bruto = int(nome_id)
    id_nome = id_bruto
    gerar_ordem = True
else:
    gerar_ordem = False
    id_nome = None

url = "https://donodozap.com/api/verify"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

data = {
    "phone": f"55{numero}",
    "code": "",
    "amount": 1,
    "method": "PIX"
}

try:
    req = requests.post(url, headers=header, json=data)
    req.raise_for_status()

    print(f"Status Code: {req.status_code}")

    def formatar(json_req):
        res = []
        if isinstance(json_req, dict):
            accounts = json_req.get("accounts", [])
            for item in accounts:
                if isinstance(item, dict):
                    nome = item.get("NOME")
                    if nome:
                        res.append(nome)
        return res

    nomes = formatar(req.json())
    print(f"Contas encontradas: {nomes}")

    if not nomes:
        print("Nenhuma conta encontrada!")
        sys.exit(1)

    print("\n📋 CONTAS DISPONÍVEIS:")
    for idx, nome in enumerate(nomes):
        print(f'  {idx}: {nome}')

    if not gerar_ordem:
        print(f"\n💡 Para gerar uma ordem de pagamento, use:")
        print(f"   python script.py {numero} <ID>")
        print(f"   Exemplo: python script.py {numero} 0")
        sys.exit(0)

    if id_nome >= len(nomes) or id_nome < 0:
        print(f"\n❌ Erro: ID {id_nome} inválido.")
        print(f"   Use um ID entre 0 e {len(nomes)-1}")
        sys.exit(1)

    nf = f"55{numero}"
    selected_name = nomes[id_nome]

    create_order = "https://donodozap.com/api/create-order"

    code_random = str(uuid.uuid4())

    order_data = {
        "code": code_random,
        "amount": 1,
        "method": "PIX",
        "client_name": selected_name,
        "client_document": "",
        "phone": nf,
        "selectedIndex": id_nome,
        "client_email": f"test{id_nome}@test.com"
    }

    print(f"\n🔄 Criando ordem para: {selected_name} (ID: {id_nome})\n💰 Valor de pagamento: R$ 1,00")
    print(f"📝 Código gerado: {code_random}")

    create = requests.post(create_order, headers=header, json=order_data)
    print(f"📊 Status Code Create Order: {create.status_code}")

    if create.status_code == 200:
        try:
            create_json = create.json()
            code_value = create_json.get("code")
            txid = create_json.get("txid")

            print(f"🔑 Code: {code_value}")
            print(f"🆔 TXID: {txid}")

            if txid:
                print("\n⏳ Verificando status do pagamento...")
                result_url = ""
                attempts = 0
                max_attempts = 15

                while result_url == "" and attempts < max_attempts:
                    time.sleep(5)
                    attempts += 1

                    try:
                        check_req = requests.get(f"https://donodozap.com/api/check-order?txid={txid}", headers=header)
                        check_json = check_req.json()

                        print(f"🔄 Tentativa {attempts}: Status - {check_json.get('status', 'UNKNOWN')}")

                        result_url = check_json.get('resultsUrl', '')

                        if result_url:
                            result = f"✅ PAGAMENTO CONFIRMADO!\n🔗 Resultado aqui:\n   https://donodozap.com{result_url}"
                            print(f"\n{result}")
                            break

                        if check_json.get('status') == 'PAID' and not result_url:
                            print("💰 Pagamento confirmado, aguardando resultsUrl...")
                            continue

                        if check_json.get('status') == 'WAITING_PAYMENT':
                            print("⏰ Aguardando pagamento...")
                            continue

                    except requests.exceptions.RequestException as e:
                        print(f"❌ Erro na verificação: {e}")
                        continue
                    except json.JSONDecodeError:
                        print("❌ Erro ao decodificar JSON de verificação")
                        continue

                if not result_url:
                    print(f"\n⏰ Tempo esgotado. Pagamento não confirmado após {max_attempts * 5} segundos")

            else:
                print("❌ TXID não encontrado na resposta")

        except json.JSONDecodeError:
            print("❌ Erro: Resposta não é um JSON válido")
            print("Response text:", create.text)
    else:
        print("❌ Erro na criação da ordem")
        print("Response:", create.text)

except requests.exceptions.RequestException as e:
    print(f"❌ Erro na requisição: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
