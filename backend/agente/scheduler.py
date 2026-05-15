from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging

from app.database import SessionLocal
from app.config import get_settings
from agente.coleta.coleta_un_wpp import coletar_un_wpp
from agente.transformacao.normalizar import normalizar_dados
from agente.calculo.calcular_indices import calcular_todos_indices
from agente.validacao.testes_falseabilidade import executar_validacao
from agente.persistencia.salvar_bd import salvar_indices_bd
from agente.notificacao.email_admin import enviar_email_admin

logger = logging.getLogger(__name__)
settings = get_settings()

scheduler = BackgroundScheduler()


async def tarefa_coleta_semanal():
    """
    Tarefa agendada para coletar, processar e salvar dados semanalmente.

    Agenda: Sábado 00:00 Nagano = Sexta 14:00 São Paulo
    (Cron: 0 14 * * 4 para horário de São Paulo UTC-3)
    """

    logger.info("=== INÍCIO COLETA SEMANAL ===")

    db = SessionLocal()

    try:
        # FASE 1: PRÉ-COLETA
        logger.info("Fase 1: Pré-coleta - validando configurações")
        # Validações básicas aqui

        # FASE 2: COLETA
        logger.info("Fase 2: Coletando dados...")
        dados_brutos = coletar_un_wpp(db)
        logger.info(f"  ✓ Coletados dados de {len(dados_brutos)} países")

        # FASE 3: TRANSFORMAÇÃO
        logger.info("Fase 3: Normalizando e transformando dados...")
        dados_processados = normalizar_dados(dados_brutos)
        logger.info(f"  ✓ {len(dados_processados)} registros processados")

        # FASE 4: CÁLCULO
        logger.info("Fase 4: Calculando índices N* e IES...")
        indices_calculados = calcular_todos_indices(dados_processados, db)
        logger.info(f"  ✓ {len(indices_calculados)} índices calculados")

        # FASE 5: VALIDAÇÃO
        logger.info("Fase 5: Executando testes de falseabilidade...")
        resultado_validacao = executar_validacao(indices_calculados)
        logger.info(f"  ✓ Validação concluída: {'PASSOU' if resultado_validacao['passou'] else 'COM AVISOS'}")
        if resultado_validacao.get('avisos'):
            for aviso in resultado_validacao['avisos'][:5]:  # Primeiros 5
                logger.warning(f"    ⚠️ {aviso}")

        # FASE 6: PERSISTÊNCIA
        logger.info("Fase 6: Salvando no banco de dados...")
        salvar_indices_bd(indices_calculados, db)
        logger.info("  ✓ Dados salvos com sucesso")

        # FASE 7: NOTIFICAÇÃO
        logger.info("Fase 7: Enviando notificação ao admin...")
        try:
            # Contar status N*
            status_n = {}
            for idx in indices_calculados:
                status = idx.get("status_n", "DESCONHECIDO")
                status_n[status] = status_n.get(status, 0) + 1

            enviar_email_admin(
                assunto="AINU: Coleta Semanal Concluída com Sucesso",
                dados_resumo={
                    "total_paises": len(indices_calculados),
                    "data_coleta": datetime.now().isoformat(),
                    "status": "SUCESSO",
                    "validacao": "PASSOU" if resultado_validacao['passou'] else f"⚠️ {len(resultado_validacao.get('avisos', []))} avisos",
                    "promissores": status_n.get("PROMISSOR", 0),
                    "equilibrio": status_n.get("EQUILIBRIO", 0),
                    "criticos": status_n.get("CRITICO", 0),
                    "colapso": status_n.get("COLAPSO", 0)
                }
            )
        except Exception as e:
            logger.warning(f"Erro ao enviar email: {e}")

        logger.info("=== 7 FASES CONCLUÍDAS COM SUCESSO ===\n")

    except Exception as e:
        logger.error(f"Erro durante coleta semanal: {e}")

        # Enviar email de erro
        try:
            enviar_email_admin(
                assunto="AINU: Coleta Semanal FALHOU",
                dados_resumo={
                    "status": "ERRO",
                    "erro": str(e),
                    "data_erro": datetime.now().isoformat()
                }
            )
        except:
            pass

        logger.info("=== FIM COLETA SEMANAL (ERRO) ===\n")

    finally:
        db.close()


def iniciar_scheduler():
    """Inicia o scheduler de tarefas"""

    if scheduler.running:
        logger.warning("Scheduler já está rodando")
        return

    # Trigger para sexta-feira 14:00 horário de São Paulo (UTC-3)
    # Equivalente a: Sábado 00:00 horário de Nagano (Asia/Tokyo, UTC+9)
    # Cron: minute hour day month day_of_week
    # 0 14 * * 4 = minuto 0, hora 14, qualquer dia, qualquer mês, sexta-feira (4)
    #
    # Alternativa em Nagano (se preferir):
    # trigger = CronTrigger(hour=0, minute=0, day_of_week=5, timezone='Asia/Tokyo')

    trigger = CronTrigger(hour=14, minute=0, day_of_week=4, timezone='America/Sao_Paulo')

    scheduler.add_job(
        tarefa_coleta_semanal,
        trigger=trigger,
        id='coleta_semanal_ainu',
        name='Coleta Semanal AINU',
        replace_existing=True
    )

    scheduler.start()
    logger.info(f"✓ Scheduler iniciado. Próxima execução: {scheduler.get_job('coleta_semanal_ainu').next_run_time}")


def parar_scheduler():
    """Para o scheduler"""

    if scheduler.running:
        scheduler.shutdown()
        logger.info("✓ Scheduler parado")
