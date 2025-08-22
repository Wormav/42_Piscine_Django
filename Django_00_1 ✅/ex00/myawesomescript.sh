#!/bin/sh

# Vcheck arg
if [ -z "$1" ]; then
    echo "Usage: $0 <bit.ly url>"
    exit 1
fi

# use curl for redirect url
# filter grep
# cut url
# display final url
curl -s "$1" | grep -o 'href="[^"]*"' | cut -d '"' -f 2
