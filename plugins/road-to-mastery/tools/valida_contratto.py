"""Verifica che una cartella-studente rispetti il contratto del file system
(Road to Mastery, spec §3).

Uso: python3 valida_contratto.py [cartella]   (default: cartella corrente)
Esce 0 se conforme, 1 se ci sono problemi.
"""
import os
import sys

FILE_GLOBALI = ["CLAUDE.md", "stato/progressi.md", "stato/preferenze.md"]
FILE_MATERIA = [
    "materiali",
    "programma.md",
    "programma-micro.md",
    "sessione_corrente.md",
    "domande.md",
    "sincronizzazione.md",
]


def problemi(root):
    out = []
    for rel in FILE_GLOBALI:
        if not os.path.exists(os.path.join(root, rel)):
            out.append(f"manca: {rel}")

    materie_dir = os.path.join(root, "materie")
    materie = []
    if os.path.isdir(materie_dir):
        materie = [d for d in os.listdir(materie_dir)
                   if os.path.isdir(os.path.join(materie_dir, d))]

    if not materie:
        out.append("nessuna materia: serve almeno una cartella in materie/<slug>/")

    for m in materie:
        for rel in FILE_MATERIA:
            if not os.path.exists(os.path.join(materie_dir, m, rel)):
                out.append(f"manca: materie/{m}/{rel}")

    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    probs = problemi(root)
    if not probs:
        print("✓ Contratto rispettato.")
        sys.exit(0)
    print("✗ Problemi nel contratto del file system:")
    for p in probs:
        print(f"  - {p}")
    sys.exit(1)


if __name__ == "__main__":
    main()
