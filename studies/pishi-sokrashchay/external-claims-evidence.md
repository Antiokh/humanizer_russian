# External evidence audit for PS-CL01..PS-CL32

Status: **2026-08-19 calibration pass**.

This file is deliberately separate from the primary-source study. `counterexamples-claims.md` records what the book says and how the project initially scoped it. This file asks a different question: **does outside empirical literature support the factual/causal claim strongly enough to affect runtime policy?**

The book remains the primary source for what Ilyakhov/Sarycheva argue. External research is used only to calibrate claims that reach beyond editorial method.

## Status vocabulary

- `SUPPORTED_BOUNDED` — external evidence supports a narrower, operationally useful version.
- `PARTIAL_CONDITIONAL` — an effect exists under some tasks/populations, but the book's wording is too broad.
- `CONTESTED` — credible evidence points in more than one direction.
- `UNVERIFIED` — no sufficiently direct evidence located in this pass.
- `COUNTEREVIDENCE` — the broad claim conflicts with relevant empirical evidence.
- `MODEL_OR_VALUE` — editorial model, project choice, or value judgment rather than an empirical fact.
- `SOURCE_INTERNAL` — can be handled from the source's own boundaries without external factual verification.
- `TOOL_SPECIFIC_STALE` — historical/tool-version claim; not portable to current runtime.

## Claim-by-claim audit

| id | external status | evidence / boundary | runtime consequence |
|---|---|---|---|
| PS-CL01 | UNVERIFIED | Reader/task relevance is well established as a design concern, but this pass did not locate evidence for the universal psychological formulation that readers are primarily occupied with their own tasks and are little interested in the author's tasks. | Keep as an audience/task heuristic, never as a psychological law. |
| PS-CL02 | SUPPORTED_BOUNDED | Experimental reading research supports a processing cost for **syntactic complexity**. DeDe (2013) found longer reading/listening times for more complex object-cleft structures; Norman, Kemper & Kynette (1992) found complex syntax interacts with working-memory limits. This does **not** establish `shorter sentence = always easier`. | Keep cognitive-load framing; do not create a sentence-length hard threshold. |
| PS-CL03 | SOURCE_INTERNAL | The book itself supplies functional exceptions to its stop-word rhetoric. | Candidate-test only; no delete list. |
| PS-CL04 | PARTIAL_CONDITIONAL | Self-persuasion research shows that self-generated arguments can change attitudes/importance and sometimes behavior (Briñol et al. 2012; Baldwin et al. 2013; Lemmen et al. 2020), but effects depend on target, topic, values and task. It does not directly prove that a reader `trusts a conclusion more because they inferred it`. | Preserve the weaker operation: show grounds and allow inference where appropriate; do not encode a universal trust rule. |
| PS-CL05 | UNVERIFIED | A study of parenthetical material in survey questions (Schaeffer et al. 2016) found that reading parentheticals could reduce respondent processing problems; this does not support a general `parentheses = unimportant` interpretation. | No mechanical penalty for parentheses. |
| PS-CL06 | UNVERIFIED | No evidence found for a broad part-of-speech claim that Russian participles or gerunds as classes usually impair reading. General syntactic-complexity evidence is not enough to justify a POS ban. | Remains model-only/contextual; inspect actual dependency load. |
| PS-CL07 | PARTIAL_CONDITIONAL | Passive/non-canonical constructions can cost more processing in some tasks and populations (e.g. sentence-comprehension studies), but effects depend on structure, working memory, hearing/reading population and discourse function. | Passive remains legitimate; no passive detector as defect. |
| PS-CL08 | MODEL_OR_VALUE | `One new thought per sentence` is an editorial operationalization, not a directly testable universal cognitive unit. | Already refined to audience-dependent cognitive load. |
| PS-CL09 | SUPPORTED_BOUNDED | Eye-tracking work on skimming supports nonuniform inspection and a higher probability of reading material near the starts of pages/paragraphs under time pressure (Duggan & Payne 2011); other work shows skimming changes fixation/skip patterns rather than creating a universal F-pattern. | Keep as information-text review heuristic only. Never assume all readers scan all genres this way. |
| PS-CL10 | MODEL_OR_VALUE | `One topic per paragraph` is a composition model. External heading/structure research supports the usefulness of explicit topic structure, not a universal one-topic count. | Keep `dominant topic` formulation. |
| PS-CL11 | MODEL_OR_VALUE | `Change in the reader's head` is an authorial communication model. | No factual status needed. |
| PS-CL12 | MODEL_OR_VALUE | `Useful goal > useless goal` is a value/genre decision. | Scope to applied informational text. |
| PS-CL13 | SUPPORTED_BOUNDED | Headings/signals can improve representation of topic structure, recall and transfer in expository/learning tasks (Lorch et al. 2001; Sanchez et al. 2001; Beege et al. 2021). This supports `structure can aid comprehension/navigation`, not the blanket claim that it always makes text `more interesting`. | Use structure by task/genre; do not score `interest`. |
| PS-CL14 | CONTESTED | Multimedia research has strong boundary conditions. Pictures can help when they carry task-relevant/spatial information, while irrelevant or badly matched visuals can be neutral or harmful; text and pictures serve different functions. | Keep only `choose the medium that carries the information best`; never rank image > text globally. |
| PS-CL15 | UNVERIFIED | No evidence found for a universal hierarchy `personal experience/demonstration > illustration > text`. Demonstrations can be powerful, but medium/task/audience matter. | Model-only and genre-specific. |
| PS-CL16 | COUNTEREVIDENCE | Approach/avoidance and regulatory-focus research supports multiple motivational modes, including promotion, prevention, hedonic and utilitarian goals. This is incompatible with reducing **all** purchasing motivation to one two-item taxonomy unless `benefit/harm` is defined so broadly that it becomes unfalsifiable. | Do not encode as a psychological truth; retain only as a commercial brainstorming heuristic. |
| PS-CL17 | SUPPORTED_BOUNDED | Marketing communication can influence attitudes/intentions/behavior, but conversion and sales have many other causes. Nothing in the project requires a fixed effect size. | Preserve causal humility: text may contribute; never promise sales. |
| PS-CL18 | UNVERIFIED | `Recommendations and repeat sales are the two main sources of customers` is business-model dependent and not needed for editing. | Exclude from runtime. |
| PS-CL19 | UNVERIFIED | `Good work brings clients better than any advertising` is an overbroad business-causal claim. | Exclude from runtime. |
| PS-CL20 | SUPPORTED_BOUNDED | The psycholinguistic `concreteness effect` is well documented: concrete words are often recognized/recalled faster or more accurately than abstract words. Reviews also stress task/context effects and disagreement about mechanisms. | Keep `give abstractions accessible grounding when useful`; never ban abstraction. |
| PS-CL21 | SUPPORTED_BOUNDED | Numerical-information studies show large individual differences in numeracy and that those differences alter how numeric information is processed and used. This supports an audience-relative number-comprehension model, but not a single sensory-experience mechanism. | Keep audience/numeracy check; no automatic simplification of numbers. |
| PS-CL22 | CONTESTED | Precision can be interpreted as confidence, and precise forecasts can attract preference; excessive precision can also backfire with experts when it signals incompetence. Uncertainty-expression experiments also show only small/contextual trust effects. | Correct project rule is provenance/measurement review, not `precise number = distrust`. |
| PS-CL23 | UNVERIFIED | No sufficiently direct evidence found in this pass that adjacent numbers automatically cause readers to compute ratios. | Keep only as layout/design review; never infer a cognitive reaction. |
| PS-CL24 | COUNTEREVIDENCE | Employment interviews have criterion validity, especially when structured, but that does not imply that an experienced recruiter rapidly detects lies. Meta-analysis of unaided human deception judgments finds about **54%** accuracy; interview impression-management tactics also affect ratings. | Keep honesty/evidence requirement; remove any predictive claim about recruiter lie detection. |
| PS-CL25 | SOURCE_INTERNAL | The book itself lists external hiring factors, so `good response does not guarantee invitation` is already safely scoped. | Keep causal humility. |
| PS-CL26 | MODEL_OR_VALUE | Explicit author stance about where individuality lives. | Preserve as attributed editorial philosophy only. |
| PS-CL27 | TOOL_SPECIFIC_STALE | Historical claims about Главред version behavior/score thresholds cannot be generalized to current versions. | No runtime threshold; at most historical provenance. |
| PS-CL28 | UNVERIFIED | No basis found for profiling readers' education or thoughtfulness from attraction to a `shouting` headline. | Do not encode demographic/intelligence stereotypes. |
| PS-CL29 | UNVERIFIED | Motive attribution (`cowardice`, desire to hide truth) cannot be recovered reliably from euphemistic form alone. | Test factual transparency, not author psychology. |
| PS-CL30 | PARTIAL_CONDITIONAL | Unstructured discourse can increase comprehension cost in task-oriented expository reading, but stream-of-consciousness is a legitimate genre device. | Genre/context rule only. |
| PS-CL31 | UNVERIFIED | The broad causal thesis that language simplification cannot contribute to cognitive degradation and that only content changes cognition is not established by the book and is unnecessary for editing. | Exclude from runtime. |
| PS-CL32 | SUPPORTED_BOUNDED | Syntactic complexity can increase reading/processing cost, but `number of commas` is only a crude surface correlate. Research on complex syntax does not validate comma count as a defect score. | Keep comma/multi-comma density `METRIC_ONLY`; no threshold warning. |

## Evidence notes

The strongest changes from the initial claim audit are:

1. **PS-CL04** moves from generic `UNVERIFIED` to `PARTIAL_CONDITIONAL`: self-persuasion is real, but `self-inferred conclusion → more trust` is still too specific.
2. **PS-CL09** moves to `SUPPORTED_BOUNDED`: skimming research supports start-of-unit attention under task/time pressure, not a universal reading pattern.
3. **PS-CL13** moves to `SUPPORTED_BOUNDED`: headings/signaling can improve topic representation, recall and transfer in expository learning.
4. **PS-CL20** moves to `SUPPORTED_BOUNDED`: concreteness effects are real, with important context/task boundaries.
5. **PS-CL22** becomes `CONTESTED`: precision can increase perceived confidence or preference and can also backfire when it looks unjustified.
6. **PS-CL24** gets explicit `COUNTEREVIDENCE`: hiring expertise does not justify an assumption of rapid lie detection.
7. **PS-CL32** is supported only at the latent-construct level (syntactic load), not at the comma-count proxy level.

None of these evidence updates justifies promoting a source rule to `HARD_GATE`.

## External references used in this pass

Primary/empirical sources are preferred below; review/meta-analytic sources are used where the claim is itself broad.

- DeDe G. *Reading and Listening in People with Aphasia: Effects of Syntactic Complexity*. 2013. DOI: https://doi.org/10.1044/1058-0360(2013/12-0111)
- Norman S, Kemper S, Kynette D. *Adults' reading comprehension: effects of syntactic complexity and working memory*. 1992. DOI: https://doi.org/10.1093/geronj/47.4.P258
- Briñol P, McCaslin MJ, Petty RE. *Self-generated persuasion: effects of the target and direction of arguments*. 2012. DOI: https://doi.org/10.1037/a0027231
- Baldwin AS et al. *Examining causal components and a mediating process underlying self-generated health arguments*. 2013. DOI: https://doi.org/10.1037/a0029937
- Lemmen N et al. *Convince Yourself to Do the Right Thing*. 2020. DOI: https://doi.org/10.3389/fpsyg.2020.613418
- Schaeffer NC et al. *The Impact of Parenthetical Phrases on Interviewers' and Respondents' Processing of Survey Questions*. 2016. PubMed: https://pubmed.ncbi.nlm.nih.gov/31467801/
- Duggan GB, Payne SJ. *Skim reading by satisficing: Evidence from eye tracking*. CHI 2011. DOI: https://doi.org/10.1145/1978942.1979114
- Strukelj A, Niehorster DC. *One page of text: Eye movements during regular and thorough reading, skimming, and spell checking*. 2018. DOI: https://doi.org/10.16910/jemr.11.1.1
- Lorch RF Jr et al. *Effects of Headings on Text Summarization*. 2001. DOI: https://doi.org/10.1006/ceps.1999.1037
- Sanchez RP, Lorch EP, Lorch RF Jr. *Effects of Headings on Text Processing Strategies*. 2001. DOI: https://doi.org/10.1006/ceps.2000.1056
- Beege M et al. *The effect of signaling in dependence on the extraneous cognitive load in learning environments*. 2021. PubMed: https://pubmed.ncbi.nlm.nih.gov/33108548/
- Schnotz W, Bannert M. *Influence of the type of visualization on the construction of mental models during picture and text comprehension*. 1999. PubMed: https://pubmed.ncbi.nlm.nih.gov/10474324/
- Schüler A et al. *Specifying the boundary conditions of the multimedia effect*. 2018. DOI: https://doi.org/10.1111/bjop.12341
- Recchia G / related concreteness literature summarized in: *Semantic Neighborhood Effects for Abstract versus Concrete Words*. 2016. DOI: https://doi.org/10.3389/fpsyg.2016.01034
- Harpaintner M et al. *Concrete vs. Abstract Semantics: From Mental Representations to Functional Brain Mapping*. 2019. DOI: https://doi.org/10.3389/fnhum.2019.00267
- Jerez-Fernandez A, Angulo AN, Oppenheimer DM. *Show me the numbers: precision as a cue to others' confidence*. 2014. DOI: https://doi.org/10.1177/0956797613504301
- Loschelder DD et al. *The Too-Much-Precision Effect*. 2016. DOI: https://doi.org/10.1177/0956797616666074
- van der Bles AM et al. *The effects of communicating uncertainty on public trust in facts and numbers*. 2020. DOI: https://doi.org/10.1073/pnas.1913678117
- Hartwig M, Bond CF. *Why do lie-catchers fail? A lens model meta-analysis of human lie judgments*. 2011. DOI: https://doi.org/10.1037/a0023589
- Bond CF, DePaulo BM. *Accuracy of deception judgments*. 2006. PubMed: https://pubmed.ncbi.nlm.nih.gov/16859438/
- Sackett PR et al. *Revisiting meta-analytic estimates of validity in personnel selection*. 2022. DOI: https://doi.org/10.1037/apl0000994
- Levashina-related interview evidence: Wilhelmy et al./interview impression-management meta-analysis, PubMed: https://pubmed.ncbi.nlm.nih.gov/28261135/

## Policy conclusion

External evidence strengthens the project's existing architecture rather than the book's strongest rhetoric:

`empirical support for a latent effect` ≠ `permission to detect that effect with a cheap surface proxy`.

In particular:

- syntax complexity evidence does not validate sentence-length/comma thresholds;
- self-persuasion evidence does not validate a universal trust rule;
- concreteness evidence does not validate an anti-abstraction rule;
- multimedia evidence does not validate `image > text`;
- interview validity does not validate `recruiter detects lies`;
- precision effects do not validate `oddly exact number = suspicious` without context.
