#!/usr/bin/env bash
# Download the immutable full-scale author output before running the gate.
set -euo pipefail

hf download DineshAI/oqkiE71wrC-artifacts author_full_protocol/manifest.json author_full_protocol/uniform.npy author_full_protocol/beta.npy author_full_protocol/beta1.npy --repo-type dataset --local-dir outputs
