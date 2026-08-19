# Roadmap

## Near term

- run/repair CI in the independent repository;
- add model-judge evaluation harness;
- collect a Russian human/LLM corpus by genre;
- add false-positive counterexamples for every native/AI heuristic;
- review `NATIVE_USAGE` rules with Russian philologists;
- extend author profiling beyond regex proxies.

## Editing sources

- incorporate additional Russian grammar/style references with precise source mapping;
- add a private analytical summary of legally available Ilyakhov material when supplied by the repository owner;
- keep Nora Gal rules as contextual semantic/editorial checks.

## Author layer

- genre-separated profiles;
- local/generational lexicon dictionaries;
- stable preferred/allowed/rare/avoid vocabulary sets;
- discourse-transition and self-repair metrics;
- reference-distance / explicitness measures;
- comparison between dictated/ASR and manually typed corpora.

## Linter

The deterministic linter remains intentionally conservative. New regex rules should not try to replace semantic or discourse analysis.
