#!/bin/bash

if [ ! -f ./lang_models/lang_models.txt ]; then
    echo "File lang_models.txt is not found!"
    exit 1
fi

while IFS= read -r model || [ -n "$model" ]; do
    echo "Pulling model: $model"
    ollama pull "$model"
done < ./lang_models/lang_models.txt

echo "Ready!"
