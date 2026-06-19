#!/usr/bin/env bash
# Crea la repo del team per l'hackathon: una repo, frontend/ + backend/,
# aggiunge il compagno come collaboratore, primo push.
set -euo pipefail

PROJECT_NAME="${1:-}"
TEAMMATE="${2:-}"
VISIBILITY="${3:---private}"  # --private (default) oppure --public

if [[ -z "$PROJECT_NAME" || -z "$TEAMMATE" ]]; then
  echo "Uso: bash setup.sh <nome-progetto> <username-github-compagno> [--private|--public]"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES="$SCRIPT_DIR/templates"

# controlli rapidi
command -v git >/dev/null || { echo "git non trovato. Installalo prima."; exit 1; }
command -v gh  >/dev/null || { echo "GitHub CLI 'gh' non trovata. Installa gh e fai 'gh auth login'."; exit 1; }

if [[ -e "$PROJECT_NAME" ]]; then
  echo "Esiste gia una cartella chiamata '$PROJECT_NAME'. Scegli un altro nome."; exit 1
fi

echo "==> Scaffolding in ./$PROJECT_NAME"
mkdir "$PROJECT_NAME"
cp -r "$TEMPLATES/." "$PROJECT_NAME/"
cd "$PROJECT_NAME"

echo "==> git init + primo commit (scheletro che cammina)"
git init -q
git add -A
git commit -qm "chore: scheletro iniziale (frontend + backend + Claude)"
git branch -M main

echo "==> Creo la repo su GitHub e pusho"
gh repo create "$PROJECT_NAME" "$VISIBILITY" --source=. --remote=origin --push

OWNER="$(gh api user --jq .login)"

echo "==> Aggiungo $TEAMMATE come collaboratore"
if gh api -X PUT "repos/$OWNER/$PROJECT_NAME/collaborators/$TEAMMATE" -f permission=push >/dev/null 2>&1; then
  echo "    OK: invito inviato a $TEAMMATE (deve accettarlo via email/GitHub)."
else
  echo "    ATTENZIONE: non sono riuscito ad aggiungere $TEAMMATE. Controlla lo username e aggiungilo a mano da GitHub > Settings > Collaborators."
fi

echo ""
echo "========================================================"
echo " Pronto! Repo creata e scheletro pushato."
echo " Tu e $TEAMMATE potete clonarla cosi:"
echo "     git clone https://github.com/$OWNER/$PROJECT_NAME.git"
echo ""
echo " Per avviare in locale leggi il README dentro il progetto."
echo " Ricorda: copia backend/.env.example in backend/.env e metti la chiave Claude."
echo "========================================================"
