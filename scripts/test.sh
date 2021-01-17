#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

test_example() {
  (
    cd example

    sed 's/.*journal.*/../' requirements.txt \
      | diff - ../scripts/requirements.txt

    python3 -m venv .venv
    # shellcheck disable=SC1091
    source .venv/bin/activate
    pip install --requirement ../scripts/requirements.txt

    journal --help
    journal test
    journal test_in_isolation

    python -m ipykernel install --user
    journal generate src/notebooks/uncertainty.py

    deactivate
  )
}

main() {
  local -r script_folder="$(dirname "$(readlink --canonicalize "$0")")"
  local -r project_folder="$(dirname "${script_folder}")"
  cd "${project_folder}"

  docker run --entrypoint sh --rm --volume "$(pwd)":/workdir \
    evolutics/travel-kit:0.6.0 -c \
    'git ls-files -z | xargs -0 travel-kit check --'

  test_example
}

main "$@"
