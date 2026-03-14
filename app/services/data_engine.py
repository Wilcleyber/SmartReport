import pandas as pd
import io
from fastapi import HTTPException

class DataEngine:
    @staticmethod
    async def process_file(file_content: bytes, file_extension: str):
        try:
            # 1. Leitura Dinâmica (CSV ou Excel)
            if file_extension == '.csv':
                df = pd.read_csv(io.BytesIO(file_content))
            else:
                df = pd.read_excel(io.BytesIO(file_content))

            if df.empty:
                raise ValueError("A planilha está vazia.")

            # 2. Limpeza Básica
            df = df.dropna(how='all')  # Remove linhas totalmente vazias
            
            # 3. Cálculo de Métricas (Ouro para o Dashboard)
            # Filtramos apenas colunas numéricas para não quebrar o cálculo
            numeric_df = df.select_dtypes(include=['number'])
            
            metrics = {}
            if not numeric_df.empty:
                for col in numeric_df.columns:
                    metrics[col] = {
                        "media": round(float(numeric_df[col].mean()), 2),
                        "max": round(float(numeric_df[col].max()), 2),
                        "min": round(float(numeric_df[col].min()), 2),
                        "soma": round(float(numeric_df[col].sum()), 2)
                    }

            # 4. Geração do Resumo Técnico (Input para a Groq)
            # Isso resume a planilha em texto para a IA não precisar ler 1000 linhas
            rows, cols = df.shape
            tech_summary = f"Planilha com {rows} linhas e {cols} colunas. "
            tech_summary += f"Colunas encontradas: {', '.join(df.columns)}. "
            tech_summary += f"Métricas principais: {metrics}"

            return df, metrics, tech_summary

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao processar dados: {str(e)}")