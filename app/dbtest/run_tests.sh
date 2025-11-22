#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="/tmp/db-results.log"

: > "${LOG}"
echo "Test dir: ${DIR}" | tee -a "${LOG}"
shopt -s nullglob
files=( "${DIR}"/*.sql )

if [ ${#files[@]} -eq 0 ]; then
  echo "No SQL files found in ${DIR}" | tee -a "${LOG}"
  exit 1
fi

for file in "${files[@]}"; do
  echo
  echo "---- Running ${file} ----" | tee -a "${LOG}"
  if mysql -h db -u root -p123 tinder_mascotas < "${file}" 2>&1 | tee -a "${LOG}"; then
    echo "OK: ${file}" | tee -a "${LOG}"
  else
    echo "ERROR executing ${file}. See ${LOG}" | tee -a "${LOG}"
    exit 1
  fi
done

echo
echo "All SQL unit tests passed" | tee -a "${LOG}"
exit 0