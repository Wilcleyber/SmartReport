import matplotlib.pyplot as plt
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

class Visualizer:
    @staticmethod
    def generate_chart_base64(metrics: dict) -> str:
        labels = list(metrics.keys())
        values = [m['media'] for m in metrics.values()]

        plt.figure(figsize=(8, 4))
        plt.bar(labels, values, color='#005a8c')
        plt.title('Resumo de Médias por Indicador')
        plt.xlabel('Indicadores')
        plt.ylabel('Valor Médio')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_base64

    @staticmethod
    def generate_pdf(analysis_text: str, chart_base64: str, target_path: str) -> str:
        """
        Gera o PDF e salva no local especificado por target_path.
        Suporta múltiplas páginas para textos longos.
        """
        c = canvas.Canvas(target_path, pagesize=letter)
        width, height = letter

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "SmartReport - Análise Inteligente de Dados")
        
        c.setFont("Helvetica", 10)
        display_name = target_path.split("/")[-1]
        c.drawString(50, height - 70, f"Relatório Gerado: {display_name}")
        c.line(50, height - 80, width - 50, height - 80)

        # Inserindo o Gráfico
        if chart_base64:
            if "base64," in chart_base64:
                chart_base64 = chart_base64.split("base64,")[1]
            
            img_data = base64.b64decode(chart_base64)
            img_buffer = io.BytesIO(img_data)
            c.drawImage(ImageReader(img_buffer), 50, height - 350, width=500, height=250)

        # Inserindo o Texto da IA
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 380, "Insights do Analista IA:")
        
        c.setFont("Helvetica", 10)
        y_position = height - 400
        line_height = 14
        margin_bottom = 50

        lines = analysis_text.split('\n')
        for line in lines:
            # Quebra manual para não ultrapassar largura
            wrapped_line = line[:105]
            c.drawString(50, y_position, wrapped_line)
            y_position -= line_height

            # Se chegou perto do rodapé, cria nova página
            if y_position < margin_bottom:
                c.showPage()
                # Redefine fonte e cabeçalho da nova página
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, height - 50, "Insights do Analista IA (continuação):")
                c.setFont("Helvetica", 10)
                y_position = height - 80

        c.save()
        return target_path
