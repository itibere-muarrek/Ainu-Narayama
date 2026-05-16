#!/usr/bin/env python3
"""
AINU.SYSTEMS - Diagnóstico Completo
Identifica todos os problemas antes de iniciar o app
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Verifica variáveis de ambiente críticas"""
    print("\n" + "="*60)
    print("🔍 DIAGNÓSTICO DE AMBIENTE")
    print("="*60)

    critical_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "ALGORITHM",
        "ACCESS_TOKEN_EXPIRE_HOURS"
    ]

    missing = []
    for var in critical_vars:
        value = os.getenv(var, "")
        status = "✅" if value else "❌"
        display_value = value[:50] + "..." if len(value) > 50 else value
        print(f"{status} {var}: {display_value}")
        if not value:
            missing.append(var)

    if missing:
        print(f"\n⚠️  FALTAM VARIÁVEIS: {', '.join(missing)}")

    return len(missing) == 0

def check_database():
    """Testa conexão com banco de dados"""
    print("\n" + "="*60)
    print("🗄️  DIAGNÓSTICO DE BANCO DE DADOS")
    print("="*60)

    try:
        database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
        print(f"DATABASE_URL: {database_url[:60]}...")

        if database_url.startswith("postgresql"):
            print("✅ PostgreSQL detectado")
            from sqlalchemy import create_engine, text
            try:
                engine = create_engine(database_url, echo=False)
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                    print("✅ Conexão com PostgreSQL bem-sucedida!")
                    return True
            except Exception as e:
                print(f"❌ Erro ao conectar: {str(e)[:100]}")
                return False
        else:
            print("⚠️  Usando SQLite (dados não persistem em produção)")
            return True
    except Exception as e:
        print(f"❌ Erro crítico: {str(e)}")
        return False

def check_dependencies():
    """Verifica se todos os pacotes estão instalados"""
    print("\n" + "="*60)
    print("📦 DIAGNÓSTICO DE DEPENDÊNCIAS")
    print("="*60)

    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "email_validator",
        "psycopg2",
        "python_jose",
        "passlib"
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NÃO INSTALADO")
            missing.append(package)

    if missing:
        print(f"\n⚠️  FALTAM PACOTES: {', '.join(missing)}")

    return len(missing) == 0

def check_routes():
    """Testa se os routers podem ser importados"""
    print("\n" + "="*60)
    print("🔌 DIAGNÓSTICO DE ROUTERS")
    print("="*60)

    try:
        print("Importando auth router...")
        from app.routers import auth
        print("✅ Auth router OK")

        print("Importando paises router...")
        from app.routers import paises
        print("✅ Paises router OK")

        print("Importando admin router...")
        from app.routers import admin
        print("✅ Admin router OK")

        return True
    except Exception as e:
        print(f"❌ Erro ao importar routers: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os diagnósticos"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " AINU.SYSTEMS v3.1.0 - DIAGNÓSTICO ".center(58) + "║")
    print("╚" + "="*58 + "╝")

    results = {
        "Ambiente": check_environment(),
        "Dependências": check_dependencies(),
        "Banco de Dados": check_database(),
        "Routers": check_routes(),
    }

    print("\n" + "="*60)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("="*60)

    all_ok = True
    for check, result in results.items():
        status = "✅ OK" if result else "❌ ERRO"
        print(f"{status}: {check}")
        if not result:
            all_ok = False

    print("\n" + "="*60)
    if all_ok:
        print("✅ TODOS OS DIAGNÓSTICOS PASSARAM - APP PODE INICIAR")
    else:
        print("❌ ERROS ENCONTRADOS - CORRIGIR ANTES DE INICIAR")
        sys.exit(1)
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
