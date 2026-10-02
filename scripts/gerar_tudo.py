#!/usr/bin/env python3
"""Regera TODAS as peças do README. Rode depois de editar textos, cores ou projetos:
    pip install fonttools
    python3 scripts/gerar_tudo.py
As peças diárias (principio, telemetria) a Action já atualiza sozinha toda madrugada."""
import os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
for s in ["hero", "links_divisor", "manifesto", "stack_processo", "projetos", "footer", "principio"]:
    print(f"── {s}")
    subprocess.run([sys.executable, os.path.join(AQUI, s + ".py")], cwd=AQUI, check=True)
print("── telemetria (precisa de token; use --demo para testar sem rede)")
subprocess.run([sys.executable, os.path.join(AQUI, "telemetria.py")] + sys.argv[1:], cwd=AQUI)
