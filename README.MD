![Logo]("AI Tuttor Forge-4.png")

#  🧠 AI Tutor Forge
## Gerador de Agentes de Aprendizado

> *Transforme qualquer tópico de estudo da área tech em um Professor IA Sênior personalizado usando o poder da LLM de sua preferência.*

![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![API](https://img.shields.io/badge/Google-Gemini%202.5-orange)
![License](https://img.shields.io/badge/license-GPLv3-green)


## 📖 Sobre o Projeto

O **AI Tutor Forge** é uma ferramenta CLI (Linha de Comando) desenvolvida em Python que atua como um "`Arquiteto de Educação`".

Em vez de apenas "`conversar com a IA`", este script entrevista o usuário a respeito de seus objetivos de aprendizado, sugere projetos práticos baseados no nível do aluno e, utilizando a API do **Google Gemini (modelo Flash)**, gera um **META-PROMPT (System Instruction)** altamente otimizado.

O resultado é um prompt que, quando inserido em uma LLM, cria um mentor virtual que aplica metodologia de ensino ativa (ensina conceitos, propõe exercícios e nunca entrega o código pronto).


## ✨ Funcionalidades

- **🔍 Consultor de Projetos:** Não sabe o que criar? A IA sugere 3 projetos práticos baseados no que você quer aprender.
- **🛡️ Compatibilidade Extrema:** Funciona nativamente no **Python 3.13+** utilizando chamadas REST puras (sem dependência de SDKs legados).
- **🚀 Modelo de IA Variável:** O script busca os modelos disponíveis na conta do usuário e irá buscar a opção mais otimizada para a atividade. Preferível o modelo `*flash`.
- **🔓 Safety Filter Bypass:** Configuração inteligente para evitar bloqueios indevidos em tópicos de programação inofensivos.
- **📝 Geração de Meta-Prompt:** Cria a "`persona`" perfeita para o seu professor virtual.


## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Conectividade:** Requests (REST API)
- **IA:** Google Gemini API (Generative Language v1beta)


## 🚀 Como Rodar


### Pré-requisitos
- Python instalado.
- Uma API Key do Google AI Studio. (o próprio agente ensina a gerar a chave)


### Instalação

1. Clone o repositório:
```bash
    git clone git@github.com:guedesindev/ai_tutor_forge.git
    cd ai_tutor_forge
```

2. Crie um ambiente virtual (Opcional, mas recomendado):
```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate

    # Linux/Mac:
    source venv/bin/activate
```

3. Atualize a versão do pip:
```bash
    python -m pip install --upgrade pip
```

4. Instale a dependência:
```bash
    pip install -r requirement.txt
```

5. Execute:
```bash
    python agente_final.py
```

🔮 Roadmap (Próximos Passos)

- [ ] Interface Gráfica (WEB) com FastAPI.<br>
- [ ] Integração de Login Social (Google).<br>
- [ ] Banco de Dados para salvar histórico de aprendizado.<br>


📃 Linceça

Este projeto está sob a licença GNU GPLv3 - Veja o arquivo [LICENSE](LICENSE) para detalhes.
