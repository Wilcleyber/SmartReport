import matplotlib.pyplot as plt
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

class Visualizer:
    @staticmethod
    def generate_chart_base64(metrics: dict) -> str:
        """
        Gera um gráfico de barras baseado nas médias das métricas e retorna em Base64.
        """
        # Extrai apenas as médias para o gráfico
        labels = list(metrics.keys())
        values = [m['media'] for m in metrics.values()]

        plt.figure(figsize=(8, 4))
        plt.bar(labels, values, color='#005a8c') # Azul aproximado ao tom corporativo
        plt.title('Resumo de Médias por Indicador')
        plt.xlabel('Indicadores')
        plt.ylabel('Valor Médio')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Salva o gráfico em um buffer de memória (sem criar arquivo no disco)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # Converte para Base64 para o Frontend exibir direto na tag <img>
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close() # Importante para não consumir memória do servidor
        return img_base64

    @staticmethod
    def generate_pdf(analysis_text: str, chart_base64: str, file_name: str) -> str:
        """
        Cria um PDF profissional contendo a análise da IA e o gráfico.
        """
        pdf_path = f"app/uploads/relatorio_{file_name}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "SmartReport - Análise Inteligente de Dados")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Arquivo analisado: {file_name}")
        c.line(50, height - 80, width - 50, height - 80)

        # Inserindo o Gráfico
        if chart_base64:
            img_data = base64.b64decode(chart_base64)
            img_buffer = io.BytesIO(img_data)
            c.drawImage(ImageReader(img_buffer), 50, height - 350, width=500, height=250)

        # Inserindo o Texto da IA (Tratamento básico de quebra de linha)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 380, "Insights do Analista IA:")
        
        c.setFont("Helvetica", 10)
        text_object = c.beginText(50, height - 400)
        text_object.setLeading(14)
        
        # Divide o texto em linhas para não ultrapassar a borda do PDF
        lines = analysis_text.split('\n')
        for line in lines:
            text_object.textLine(line[:100]) # Limita largura simples
            
        c.drawText(text_object)

        c.save()
        return pdf_path