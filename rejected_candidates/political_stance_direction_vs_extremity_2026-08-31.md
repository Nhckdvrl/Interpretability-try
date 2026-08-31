question: Does an LLM factorize political stance direction (e.g. liberal vs conservative) from stance extremity/intensity, rather than encoding ideology on one scalar axis?
mother: ACL 2026 Understanding and Mitigating Political Stance Cross-topic Generalization in Large Language Models
semantic_aliases:
  - ideology direction vs strength
  - political polarity vs extremity
  - moderate vs extreme latent politics
  - stance sign vs magnitude
what_was_reviewed: mother extension + strongest-neighbor latent-ideology/steering literature
kill_class: F2
kill_evidence: Findings EMNLP 2025 work already learns continuous political-ideology directions from DW-NOMINATE scores and causally steers them across tasks. Its intervention explicitly varies scalar alpha to induce more intensive liberal versus conservative viewpoints; related multilingual political-steering work separately measures stance intensity. Thus sign/direction and magnitude/intensity of political latent directions are already operationalized and intervened upon, leaving little title-level novelty.
nearest_neighbor_warning: Do not revive by swapping ideology benchmark, party labels, language, model, or calling intensity certainty/extremity/commitment. Continuous political direction plus steering magnitude already occupies this scientific meaning.
resurrection_condition: Only reopen for a different natural property of the same political representation not reducible to topic specificity, ideological axes, polarity, intensity, or steering strength.
