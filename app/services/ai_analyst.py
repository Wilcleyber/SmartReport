import os
from groq import Groq
from app.core.config import settings # Supondo que as configs estão aqui
from app.utils.sanitizer import Sanitizer
from dotenv import load_dotenv

load_dotenv()

class AIAnalyst:
    def __init__(self):
        # Inicializa o cliente da Groq com a chave do seu .env
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"  # O modelo mais potente da Groq atualmente, outra alternativa e "Llama 3.1-8B-Instant"

    async def generate_analysis(self, tech_summary: str) -> str:
        """
        Envia o resumo técnico para a IA e retorna o insight formatado.
        """
        
        # 🎭 SYSTEM PROMPT: O Roteiro do Especialista
        system_prompt = """
        VOCÊ É O 'SMARTREPORT AI', UM ENGENHEIRO SÊNIOR DE DADOS DA VALE S.A.
        
        SUA MISSÃO: Transformar dados brutos de planilhas em decisões estratégicas.
        
        DIRETRIZES DE ESTILO:
        1. TOM DE VOZ: Profissional, analítico e direto (estilo executivo).
        2. ESTRUTURA: Use títulos, negrito e listas (Markdown) para facilitar a leitura.
        3. FOCO EM OPERAÇÃO: Identifique gargalos, picos de produção ou falhas de manutenção.
        
        REGRAS CRÍTICAS:
        - Se houver queda de produtividade, tente sugerir uma causa provável baseada nos dados.
        - Priorize alertas de segurança ou anomalias operacionais.
        - Se os dados estiverem incompletos, solicite os campos faltantes de forma educada.
        - JAMAIS invente números que não estão no Resumo Técnico fornecido.
        """

        # 📊 USER PROMPT: Os dados reais da cena
        user_prompt = f"""
        Aqui está o Resumo Técnico da planilha processada:
        ---
        {tech_summary}
        ---
        Com base nestes indicadores, gere um relatório de insights destacando:
        1. Resumo Geral da Operação.
        2. Principais KPIs observados.
        3. Alertas ou Oportunidades de Melhoria.
        4. Recomendação Técnica Final.
        """

        try:
            # Chamada oficial para a API da Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=self.model,
                temperature=0.5, # Mantém a IA focada e menos "criativa/doida"
                max_tokens=1500,
            )
            
            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"Erro ao consultar a inteligência artificial: {str(e)}"