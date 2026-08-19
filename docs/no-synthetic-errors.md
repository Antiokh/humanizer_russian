# Do not synthesize human errors

Human-written corpora contain typos, missing commas, broken government and speech-recognition artifacts. That does not make deliberate error injection a valid generic humanization technique.

Default:

```json
{
  "imitate_errors": false,
  "correct_norm_errors": true
}
```

A raw-voice imitation mode may exist only when explicitly requested and separated from ordinary editing.
