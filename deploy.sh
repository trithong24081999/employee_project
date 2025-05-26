#!/bin/bash
cd ..
cd employee_app
npm run build
mkdir -p ../employee_project/dist
rm -rf ../employee_project/dist/
cp -r dist/ ../employee_project/dist/

INDEX_FILE="../employee_project/dist/index.html"

sed -i '' 's|/assets/|/static/|g' "$INDEX_FILE"

echo "Replacement done in $INDEX_FILE. Original backed up as ${INDEX_FILE}"