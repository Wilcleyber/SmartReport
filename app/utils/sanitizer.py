import pandas as pd
import re

class Sanitizer:
    # Lista de termos comuns que indicam dados sensíveis (expansível)
    SENSITIVE_KEYWORDS = [
        'cpf', 'rg', 'nome', 'email', 'telefone', 'celular', 
        'endereco', 'salario', 'remuneracao', 'matricula', 'id_funcionario'
    ]

    @classmethod
    def mask_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Identifica e mascara colunas sensíveis para conformidade com LGPD.
        """
        sanitized_df = df.copy()
        
        for col in sanitized_df.columns:
            # Normaliza o nome da coluna para facilitar a busca (minúsculo e sem espaços)
            col_normalized = str(col).lower().replace("_", "").replace(" ", "")
            
            # Verifica se o nome da coluna contém alguma palavra-chave sensível
            if any(keyword in col_normalized for keyword in cls.SENSITIVE_KEYWORDS):
                # Se for uma coluna de identificação (texto), trocamos por "HIDDEN_ID_X"
                if sanitized_df[col].dtype == 'object':
                    sanitized_df[col] = [f"DADO_ANONIMIZADO_{i+1}" for i in range(len(sanitized_df))]
                # Se for dado financeiro ou numérico sensível, podemos aplicar uma máscara genérica
                else:
                    sanitized_df[col] = 0.0  # Ou outro valor que não revele o dado real
        
        return sanitized_df

    @staticmethod
    def clean_text_for_ai(text: str) -> str:
        """
        Remove padrões de texto que pareçam CPF ou e-mail caso tenham escapado.
        """
        # Remove CPFs (000.000.000-00)
        text = re.sub(r'\d{3}\.\d{3}\.\d{3}-\d{2}', '[CPF_REMOVIDO]', text)
        # Remove E-mails
        text = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL_REMOVIDO]', text)
        return text