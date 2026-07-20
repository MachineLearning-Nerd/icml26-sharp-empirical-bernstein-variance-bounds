# /// script
# dependencies = ["huggingface_hub>=0.34", "numpy>=2.0", "tqdm>=4.66"]
# ///
"""Execute and retain the unmodified released full author protocol on HF Jobs."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

from huggingface_hub import HfApi


COMMIT = "e36d2d779e04d52604337ca093071a1f3051f129"
REPO = Path("emp_bernstein_variance")
ARTIFACT_REPO = "DineshAI/oqkiE71wrC-artifacts"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


subprocess.run(
    ["git", "clone", "https://github.com/DMartinezT/emp_bernstein_variance.git", str(REPO)],
    check=True,
)
subprocess.run(["git", "-C", str(REPO), "checkout", COMMIT], check=True)
(REPO / "data").mkdir()
subprocess.run(["python", "main.py"], cwd=REPO, check=True)

files = sorted((REPO / "data").glob("*.npy"))
if [path.name for path in files] != ["beta.npy", "beta1.npy", "uniform.npy"]:
    raise RuntimeError(f"unexpected author output set: {[path.name for path in files]}")
manifest = {
    "paper": "oqkiE71wrC",
    "source_repository": "https://github.com/DMartinezT/emp_bernstein_variance.git",
    "commit": subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
    ).strip(),
    "entrypoint": "main.py",
    "protocol": "unmodified author source; n_experiments=100; sample_size_list=arange(100,5000,100); distributions=uniform,beta(2,6),beta(5,5)",
    "files": {
        path.name: {"bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in files
    },
}
Path("manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
api = HfApi(token=os.environ["HF_TOKEN"])
api.upload_folder(
    folder_path=str(REPO / "data"),
    repo_id=ARTIFACT_REPO,
    repo_type="dataset",
    path_in_repo="author_full_protocol",
    commit_message="Add full author empirical-Bernstein protocol outputs",
)
api.upload_file(
    path_or_fileobj="manifest.json",
    path_in_repo="author_full_protocol/manifest.json",
    repo_id=ARTIFACT_REPO,
    repo_type="dataset",
    commit_message="Add full author empirical-Bernstein protocol manifest",
)
print(json.dumps(manifest, sort_keys=True))
