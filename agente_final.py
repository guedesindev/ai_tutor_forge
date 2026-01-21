import json
import requests
from time import sleep
from escolher_modelo import escolher_modelo


title = "AGENTE CONSTRUTOR DE JORNADAS DE APRENDIZADO"

print("*" * len(title))
print(title)
print("-" * len(title))

# Configuração
print("Olá serei o teu guia para construirmos sua jornada de aprendizado")


# def escolher_modelo(api_key):
#     # 1. Endpoint para listar modelos
#     url_list = "https://generativelanguage.googleapis.com/v1beta/models"

#     try:
#         response = requests.get(url_list, params={"key": api_key})

#         if response.status_code != 200:
#             print(f"❌ Erro ao listar modelos: {response.status_code}")
#             print(response.text)
#             exit()

#         dados = response.json()

#         # 2. Filtra modelos que servem para gerar texto (generateContent)
#         modelos_disponiveis = []
#         print("\n🔎 Modelos encontrados na sua conta:")

#         # if "models" in dados:
#         #     for m in dados["models"]:
#         #         # Verifica se o modelo serve para gerar conteúdo
#         #         if "generateContent" in m.get("supportedGenerationMethods", []):
#         #             nome_limpo = m["name"].replace("models/", "")
#         #             print(f" - {nome_limpo}")
#         #             modelos_disponiveis.append(nome_limpo)
#         # else:
#         #     print(
#         #         "Nenhum modelo encontrado. Verifique se a API está ativada no console."
#         #     )

#         # 3. Tenta usar o primeiro modelo da lista que funcionou
#         if modelos_disponiveis:
#             modelo_escolhido = modelos_disponiveis[0]
#             # Dá preferência ao Flash se ele existir, pois é mais rápido
#             for m in modelos_disponiveis:
#                 if "flash" in m:
#                     modelo_escolhido = m
#                     break

#             print(f"\n🧪 Testando conexão com o modelo: '{modelo_escolhido}' ...")

#             url_teste = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_escolhido}:generateContent"

#             payload = {"contents": [{"parts": [{"text": "Diga apenas: FUNCIONOU"}]}]}

#             resp_teste = requests.post(url_teste, params={"key": api_key}, json=payload)

#             if resp_teste.status_code == 200:
#                 print(
#                     f"\n✅ SUCESSO ABSOLUTO! O modelo correto para você é: {modelo_escolhido}"
#                 )

#                 return modelo_escolhido
#             else:
#                 print(f"❌ Erro ao testar {modelo_escolhido}: {resp_teste.text}")

#         else:
#             print("\n❌ Nenhum modelo compatível encontrado.")

#     except Exception as e:
#         print(f"Erro fatal: {e}")


def obter_chave_api():
    API_KEY = input(
        "Para começarmos cole sua API KEY do Google Geminai\n(se não tiver uma digite 1 e te ensinarei como obter a sua grátis): "
    ).strip()

    return API_KEY


while True:
    API_KEY = obter_chave_api()

    if API_KEY != "1":
        break

    passos = [
        "Para usar este agente você precisará de uma conta google.",
        "Acesso o site: https://aistudio.google.com/welcome",
        "Clique em 'Get started' no canto superior direito.",
        "Faça login com sua conta google. Se não tiver uma crie gratuitamente.",
        "No menu lateral na parte inferior esquerda você verá 'Get API key', clique ali.",
        "No canto superior direito tem 'Criar chave de API'",
        "Dê o nome 'Agente de Aprendizado' em 'Escolha um projeto importado' escolha 'Criar projeto'",
        "Dé o Nome 'Agente de Aprendizado' ou outro nome que você queira e clique em 'Criar projeto'.",
        "Agora crie em 'Criar chave'.",
        "Agora que você tem a sua Chave de API nos ícones à direita clique em 'Cpoy API key', parece com duas folhas de papel uma sobre a outra.",
    ]

    for text in passos:
        print(text)
        sleep(1.5)


MODELO = escolher_modelo(API_KEY)


def chamar_gemini(prompt_texto):
    """
    Função que envia o texto para o Google via HTTP.

    :param prompt_texto: Description
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"

    headers = {"Content-Type": "application/json"}

    # errors = []

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
    ]

    payload = {
        "contents": [{"parts": [{"text": prompt_texto}]}],
        "safetySettings": safety_settings,
    }

    try:
        response = requests.post(url, params={"key": API_KEY}, json=payload)

        # Verifica se deu erro na requisição (ex: chave inválida)
        if response.status_code != 200:
            print(f"\n[ERRO DE API] Status: {response.status_code}")
            print(f"Detalhes: {response.text}")
            return None

        dados = response.json()

        if "candidates" in dados and len(dados["candidates"]) > 0:
            candidato = dados["candidates"][0]

            if candidato.get("finishReason") == "SAFATY":
                print(
                    "\n[BLOQUEIO] O Google bloqueou a resposta por motivos de segurança."
                )
                print("Tente reformular o pedido ou usar um tópico menos sensível")
                return None

            if "content" in candidato and "parts" in candidato["content"]:
                return candidato["content"]["parts"][0]["text"]
            else:
                print("\n[ERRO] A resposta veio vazia (sem texto).")
                print(f"Dump da resposta: {dados}")
                return None
        else:
            print(f"\n[ERRO] Formato de resposta inesperado")

    except Exception as e:
        print(f"\n[ERRO CRÍTICO] Falha na execução: {e}")
        return None


def main():
    # 1. entrevista inicial
    print("\n[PASSO 1] Configuração do Estudo")
    topico = input(
        "O que você deseja aprender? (Ex: Python, SQL, JavaScript, NodeJS): "
    ).strip()

    print("\nVocê já tem uma ideia de projeto:")
    print("1. Sim, eu tenho.")
    print("2. Não, sugira 3 projetos")

    escolha = input("Escolha (1 ou 2): ").strip()

    projeto_escolhido = ""

    if escolha == "1":
        projeto_escolhido = input("Qual é o seu projeto? ")
    else:
        print("\nConstulando a IA para sugestões...")
        prompt_sugestão = f""" Aja como professor de tecnologia. 
        Liste 3 ideas de projetos práticos para iniciantes aprenderem {topico}.
        Responda APENAS com uma lista numerada simples, sem introdução ou conclusão.
        """

        sugestoes = chamar_gemini(prompt_sugestão)

        if not sugestoes:
            print("\nEncerrando programa devido ao erro anterior")
            return

        print(f"\n{sugestoes}")
        print("-" * 30)
        selecao = input("Digite o NÚMERO ou o NOME do projeto escolhido: ")
        projeto_escolhido = selecao

    print("\n" + "=" * 50)
    print("Gerando seu META-PROMPT... Aguarde...")
    print("=" * 50)

    # 2. Criação do Prompt Gigante
    meta_prompt_request = f"""
    Aja como um Engenheiro de Prompt Especialista em Educação.
    
    Crie um PROMPT DE SISTEMA (SYSTEM PROMPT) altamente detalhado que o usuário irá copiar e colar na LLM de sua preferência versão Web.
    
    OBJETIVO DO PROMPT: Fazer a IA agir como um Professor Sênior ensinando {topico}.
    PROJETO GUIA SERÁ: {projeto_escolhido}.
    
    REGRAS OBRIGATÓRIAS PARA O PROMPT GERADO:
    1. Persona: Mentor paciente, didático, que usa analogias.
    2. Metodologia: NUNCA dar o código pronto inteiro. Explicar o conceito, dar exemplo pequeno, pedir para o aluno fazer.
    3. Estrutura: Começar perguntando o nível do aluno. Dividir o projeto em fases (Setup, MVP, Polimento).
    4. Interatividade: A cada resposta do aluno, dar feedback construtivo antes de avançar.
    5. Criar comandos para o aluno tirar dúvidas, solicitar ajuda, pedir revisão ou pedir resumo.
    6. Criar comandos que você julgar necessário para aprimorar o aprendizado.
    7. O foco do curso deve ser aprender o {topico} com autonomia, para que o estudante sinta-se capaz de criar outras soluções.
    
    A SAÍDA DEVE SER APENAS O TEXTO DO PROMPT, SEM COMENTÁRIOS EXTRAS PRONTO PARA COPIAR.
    """

    resultado_final = chamar_gemini(meta_prompt_request)

    if resultado_final:
        print("\n" + "#" * 50)
        print(
            "✨ SUCESSO! COPIE O TEXTO ABAIXO E COLE NO CHAT DA LLM DE TUA PREFERÊNCIA 'CHATGPT, GEMINI, CLAUDE AI, COPILOT'"
        )
        print("#" * 60 + "\n")
        print(resultado_final)
        print("\n" + "#" * 60)


if __name__ == "__main__":
    main()
