#!/bin/sh

# Vérifi qu'un argument est fournis si non renvoie une erreur
if [ -z "$1" ]; then
    echo "Usage: $0 <bit.ly url>"
    exit 1
fi

# Utilise curl pour obtenir l'URL de redirection
# Filtre avec grep pour obtenir la ligne contenant l'URL
# Utilise cut pour extraire uniquement l'URL
# Affiche l'URL finale
curl -s "$1" | grep -o 'href="[^"]*"' | cut -d '"' -f 2
