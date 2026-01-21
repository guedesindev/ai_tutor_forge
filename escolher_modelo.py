import requests
import json
import re

# print("--- LISTANDO MODELOS DISPONÍVEIS ---")
# API_KEY = input("Cole sua API Key: ").strip()


def escolher_modelo(api_key):
    """
    Busca dinâmica: Prioriza qualquer modelo 'Flash', depois qualquer 'Pro'.

    :param api_key: api key do google gemini
    """

    print("\n🔍 Analisando modelos disponíveis na sua conta...")

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
        candidatos = []

        if "models" in dados:
            for m in dados["models"]:
                # Verifica se o modelo serve para gerar conteúdo
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    nome_limpo = m["name"].replace("models/", "")
                    # print(f" - {nome_limpo}")
                    candidatos.append(nome_limpo)

        if not candidatos:
            print(f"\n❌ Nenhum modelo de geração de texto encontrado na sua conta.")
            exit()

        # 3. Lógica Dinâmica baseada no NOME (Flash > Pro > Resto)
        modelos_flash = [
            m for m in candidatos if "flash" in m.lower() and not "preview" in m.lower()
        ]
        modelos_pro = [
            m for m in candidatos if "pro" in m.lower() and not "preview" in m.lower()
        ]

        # ---------- Função de Pontuação de modelos ----------
        def calcular_score(nome_modelo):
            score = 0.0

            match = re.search(r"gemini-(\d+(?:\.\d+)?)", nome_modelo)
            if match:
                score = float(match.group(1))

            if "lite" in nome_modelo:
                score -= 0.1

            return score

        modelo_escolhido = None

        if modelos_flash:
            # Ordenar reverso para buscar versões mais atuais
            modelos_flash.sort(key=calcular_score, reverse=True)
            modelo_escolhido = modelos_flash[0]
            print(f"⚡ Melhor modelo Flash encontrado: {modelo_escolhido}")

        elif modelos_pro:
            modelos_pro.sort(key=calcular_score, reverse=True)
            modelo_escolhido = modelos_pro[0]
            print(f"🧠 `Melhor modelo Pro encontrado: {modelo_escolhido}")

        # 4. Testando conexão com o modelo escolhido.

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

    except Exception as e:
        print(f"Erro fatal: {e}")


# escolher_modelo(API_KEY) TESTE do script
