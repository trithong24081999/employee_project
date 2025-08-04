#!/bin/bash
cd ..
cd employee_app
npm run build
mkdir -p ../backend/dist
rm -rf ../backend/dist/
cp -r dist/ ../backend/dist/

INDEX_FILE="../backend/dist/index.html"

sed -i '' 's|/assets/|/static/|g' "$INDEX_FILE"

echo "Replacement done in $INDEX_FILE. Original backed up as ${INDEX_FILE}"