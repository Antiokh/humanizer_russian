# Why detector score is not the optimization target

AI detectors change. Their correlations are model-, genre-, language- and date-dependent. Optimizing prose directly for a detector can reward edits that make Russian worse: deleting normative punctuation, fragmenting coherent syntax, injecting artificial irregularity or replacing precise repeated terms with weaker synonyms.

The project therefore treats detector output as an external diagnostic only.

A detector result may motivate review, but it cannot override:

1. semantic preservation;
2. Russian norm;
3. native naturalness;
4. confirmed author voice.

If a detector penalizes a correct em dash or a normal `не X, а Y` contrast, the detector is not allowed to define the language rule.
