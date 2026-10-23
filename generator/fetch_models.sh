#!/usr/bin/env bash
# Downloads the open French voices (Piper, via sherpa-onnx releases) into generator/models.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p models && cd models
B=https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models
for m in vits-piper-fr_FR-siwis-medium vits-piper-fr_FR-tom-medium vits-piper-fr_FR-upmc-medium vits-piper-fr_FR-gilles-low; do
  [ -d "$m" ] || curl -sSL "$B/$m.tar.bz2" | tar xj
done
