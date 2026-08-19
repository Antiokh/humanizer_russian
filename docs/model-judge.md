# Model-judge contract

Future semantic/native eval automation should pass the judge:

- source text;
- user task;
- candidate rewrite;
- scenario expectations;
- optional genre/author context.

The judge scores dimensions separately:

1. semantic preservation;
2. norm correctness;
3. native naturalness;
4. editorial quality;
5. author compatibility when applicable;
6. unsupported additions;
7. destructive over-editing.

Do not give the judge one reference rewrite as a string-match target. Russian word order and style often admit several good outputs.
