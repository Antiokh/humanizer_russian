# Compatibility with existing rules

Before implementing mechanics, inspect existing checker hooks for:

- register selection;
- markdown heading parsing;
- list/structure parsing;
- protected spans (URLs/code/brands);
- finding severity and JSON schema.

New legal rules should reuse those abstractions rather than add a parallel checker.
