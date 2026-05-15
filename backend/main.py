#!/usr/bin/env python3
"""
Entry point para executar o backend AINU-Narayama.

Uso:
  python main.py                    # Modo desenvolvimento (reload)
  python main.py --prod             # Modo produção
  python main.py --host 0.0.0.0     # Custom host
"""

import uvicorn
import argparse
from app.config import get_settings

settings = get_settings()


def main():
    parser = argparse.ArgumentParser(description="AINU-Narayama Backend")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--prod", action="store_true", help="Modo produção (sem reload)")
    parser.add_argument("--workers", type=int, default=1, help="Número de workers")

    args = parser.parse_args()

    reload = not args.prod

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=reload,
        workers=args.workers if args.prod else 1,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
