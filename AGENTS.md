# Project Agent Instructions

These instructions apply to work in this repository. Read this file before starting each task.

## Environment

- Prefer an existing local virtual environment. The repository currently contains `.venv-vllm`; inspect and use it when it fits the task.
- Do not create a new virtual environment by default. Only create one if the existing environments cannot satisfy the task because of a genuine dependency or compatibility conflict, and state the reason first.
- Before installing packages, inspect the existing environment and project dependency files. Avoid unnecessary upgrades or changes to the environment.

## Models and Hugging Face assets

- Prefer model weights already present in the local Hugging Face cache.
- Before downloading any model, inspect the local cache and repository configuration/scripts for available model paths or identifiers.
- Do not download duplicate weights when a compatible cached copy exists. If a download is genuinely necessary, make that explicit and use the smallest suitable model/configuration.

## Repository hygiene

- Preserve existing user changes and do not reset, discard, or overwrite unrelated work.
- Keep generated logs, datasets, and model outputs out of commits unless the task explicitly requires them.
- Verify changes with the narrowest relevant tests or checks before reporting completion.
