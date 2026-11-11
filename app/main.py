import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(
    title="Bot Clínica Odontológica - Agendamento",
    description="API com FastAPI e Google Gemini para automação de agendamentos e atendimento",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """Rota de verificação de integridade da API (Health Check)."""
    return {
        "status": "online",
        "service": "bot-clinica-agendamento",
        "version": "1.0.0",
    }


@app.get("/teste-ia")
def teste_ia():
    """Simula uma mensagem de paciente e utiliza o Gemini para classificar a intenção."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "sua_chave_gemini_aqui":
        raise HTTPException(
            status_code=400,
            detail=(
                "GEMINI_API_KEY não foi configurada no arquivo .env. "
                "Gere sua chave em https://aistudio.google.com/ e adicione-a no .env."
            ),
        )

    # Mensagem simulada de um paciente
    mensagem_paciente = "Oi, gostaria de saber quanto custa a limpeza."

    # Prompt estruturado para classificação de intenção
    prompt = f"""
Você é um assistente de triagem para uma clínica odontológica.
Classifique a intenção da mensagem enviada pelo paciente em exatamente UMA das seguintes categorias:
- preco (se pergunta sobre valores, preços ou orçamentos)
- agendamento (se deseja marcar consulta ou verificar horários)
- cancelamento (se deseja cancelar ou remarcar)
- localizacao (se pergunta sobre endereço ou como chegar)
- outros (se for outra dúvida geral)

Responda APENAS o nome da categoria, em letras minúsculas, sem pontuação extra.

Mensagem do paciente: "{mensagem_paciente}"
""".strip()

    try:
        # Inicializa o cliente oficial do Google GenAI SDK
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )

        intencao = response.text.strip().lower() if response.text else "indefinido"

        return {
            "status": "sucesso",
            "mensagem_paciente": mensagem_paciente,
            "intencao_identificada": intencao,
            "modelo_utilizado": "gemini-1.5-flash",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na comunicação com o Gemini: {str(e)}",
        )
