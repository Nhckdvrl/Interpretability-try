# V0 provenance audit

## Pinned code and response artifacts

- Official repository `uw-nsl/Temporal_Forgetting`: `7ca18b6370e5fc9bcbc3388f33e6fc5c1316ec0e`.
- The repository includes `sampling_64_responses.zip` (29,451,932 bytes). This is the secondary stochastic 64-sample artifact, not the primary greedy-decoding transition table required by the project README.

## Released Qwen2.5-7B RL checkpoints

| Step | Hugging Face revision |
|---:|---|
| 32 | `f46f9eac9908013a502735b7e882821f492ca61e` |
| 64 | `d57afa929761825af618c6545ab7f7a5b28b3dc1` |
| 96 | `5164cb6d7dcace900aed6a961cea33de40f2b6dc` |
| 128 | `27d9d8455a50c0cb0af37e9676bac4e2a1ecddec` |
| 160 | `d8df8a5d6290bcc7b4b5fa108121cc5b9808bf58` |
| 192 | `cb3f9bda37c44699246d04b9af21df41879e0ac3` |
| 224 | `1833fa4e7beea19c2451e1f7a4dfe3068454edaf` |
| 256 | `7667ad787966f5733fdca3d2b240452d7095ff95` |

None of these eight checkpoint weights is currently in the local Hugging Face cache. In accordance with repository policy, no roughly eight-checkpoint download was started. V0 can ingest a released greedy artifact if located; otherwise checkpoint download should be authorized as a deliberate storage/compute decision before re-running greedy inference.
