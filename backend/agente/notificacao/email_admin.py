import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import logging

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def enviar_email_admin(assunto: str, dados_resumo: Dict[str, Any]) -> bool:
    """
    Envia email de notificação ao admin.

    Em desenvolvimento: usa logs. Em produção: integrar com SMTP.
    """

    if settings.environment == "development":
        logger.info(f"[EMAIL SIMULADO] Para: {settings.admin_email}")
        logger.info(f"[EMAIL SIMULADO] Assunto: {assunto}")
        logger.info(f"[EMAIL SIMULADO] Dados: {dados_resumo}")
        return True

    try:
        # Construir corpo do email
        corpo_html = _construir_html_email(assunto, dados_resumo)

        # Conectar ao SMTP
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)

        # Preparar email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = assunto
        msg["From"] = settings.smtp_user
        msg["To"] = settings.admin_email

        msg.attach(MIMEText(corpo_html, "html"))

        # Enviar
        server.sendmail(settings.smtp_user, [settings.admin_email], msg.as_string())
        server.quit()

        logger.info(f"✓ Email enviado para {settings.admin_email}")
        return True

    except Exception as e:
        logger.error(f"Erro ao enviar email: {e}")
        return False


def _construir_html_email(assunto: str, dados: Dict[str, Any]) -> str:
    """Constrói HTML do email de notificação"""

    status = dados.get("status", "DESCONHECIDO")
    cor_status = "#22c55e" if status == "SUCESSO" else "#ef4444"

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 20px auto; background: white; padding: 20px; border-radius: 8px; }}
            .header {{ background: {cor_status}; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }}
            .content {{ padding: 20px; }}
            .status {{ font-size: 24px; font-weight: bold; margin: 20px 0; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
            .info-item {{ padding: 10px; background: #f9f9f9; border-radius: 4px; }}
            .info-label {{ font-weight: bold; color: #666; }}
            .info-value {{ color: #333; margin-top: 5px; }}
            .footer {{ text-align: center; padding-top: 20px; border-top: 1px solid #eee; color: #999; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>AINU-Narayama Notificação</h1>
                <p>{assunto}</p>
            </div>
            <div class="content">
                <div class="status">{status}</div>
    """

    # Adicionar dados dinamicamente
    html += '<div class="info-grid">'

    for chave, valor in dados.items():
        if chave not in ["status", "erro"]:
            label = chave.replace("_", " ").title()
            html += f"""
                <div class="info-item">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{valor}</div>
                </div>
            """

    html += "</div>"

    # Adicionar erro se houver
    if "erro" in dados:
        html += f"""
            <div style="background: #fee; padding: 10px; border-radius: 4px; margin: 20px 0; border-left: 4px solid #f00;">
                <strong>Erro:</strong> {dados['erro']}
            </div>
        """

    html += """
                <div class="footer">
                    <p>AINU-Narayama v3.1.0</p>
                    <p><em>Sistema automático de medição socioeconômica</em></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return html
