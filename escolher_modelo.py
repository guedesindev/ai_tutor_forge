import requests
import json

# print("--- LISTANDO MODELOS DISPONÍVEIS ---")
# API_KEY = input("Cole sua API Key: ").strip()


def escolher_modelo(api_key):
    # 1. Endpoint para listar modelos
    url_list = "https://generativelanguage.googleapis.com/v1beta/models"

    try:
        response = requests.get(url_list, params={"key": api_key})

        if response.status_code != 200:
            print(f"❌ Erro ao listar modelos: {response.status_code}")
            print(response.text)
            exit()

        dados = response.json()

        # 2. Filtra modelos que servem para gerar texto (generateContent)
        modelos_disponiveis = []
        print("\n🔎 Modelos encontrados na sua conta:")

        if "models" in dados:
            for m in dados["models"]:
                # Verifica se o modelo serve para gerar conteúdo
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    nome_limpo = m["name"].replace("models/", "")
                    # print(f" - {nome_limpo}")
                    modelos_disponiveis.append(nome_limpo)
        else:
            print(
                "Nenhum modelo encontrado. Verifique se a API está ativada no console."
            )

        # 3. Tenta usar o primeiro modelo da lista que funcionou
        if modelos_disponiveis:
            modelo_escolhido = modelos_disponiveis[0]
            # Dá preferência ao Flash se ele existir, pois é mais rápido
            for m in modelos_disponiveis:
                if "flash" in m:
                    modelo_escolhido = m
                    break

            print(f"\n🧪 Testando conexão com o modelo: '{modelo_escolhido}' ...")

            url_teste = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_escolhido}:generateContent"

            payload = {"contents": [{"parts": [{"text": "Diga apenas: FUNCIONOU"}]}]}

            resp_teste = requests.post(url_teste, params={"key": api_key}, json=payload)

            if resp_teste.status_code == 200:
                print(
                    f"\n✅ SUCESSO ABSOLUTO! O modelo correto para você é: {modelo_escolhido}"
                )

                return modelo_escolhido
            else:
                print(f"❌ Erro ao testar {modelo_escolhido}: {resp_teste.text}")

        else:
            print("\n❌ Nenhum modelo compatível encontrado.")

    except Exception as e:
        print(f"Erro fatal: {e}")


# escolher_modelo(API_KEY) TESTE do script
