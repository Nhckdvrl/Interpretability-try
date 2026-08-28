# Model/environment record

- Python: 3.12.13 (.venv-vllm/bin/python)
- torch: 2.13.0+cu130
- transformers: 5.16.1
- scorer: project exact continuation HFChoiceScorer; no API and no judge
- dtype requested: bfloat16 for GPU attempts
- Qwen3-8B cached revision: b968826d9c46dd6066d109eabc6255188de91218
- Qwen3-4B cached revision: 1cfa9a7208912126459214e8b04321603b3df60c
- Qwen3-1.7B cached revision: 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e
- Gemma3-4B cached revision: 093f9f388b31de276ce2de164bdc2081324b9767

The initial direct-weight-load attempt was terminated before a forward pass while
the GPUs were occupied by pre-existing vLLM processes. It was superseded by the
local vLLM endpoint scorer (`/v1/completions`, `echo=true`, exact final-token
log-probability). Qwen3-8B and Gemma3-12B endpoint raw probabilities and summaries
are saved under the corresponding active results directories. These are marked
EXPLORATORY-LOCAL; registry authorization was not changed.
