# Source inventory

## Identity

- Title in EPUB metadata: **Пиши, сокращай**
- Creators in EPUB metadata: **Максим Ильяхов**, **Людмила Сарычева**
- Language: `ru`
- Source format: EPUB
- EPUB identifier: `urn:uuid:1dc149a4-b64b-47a3-88a7-852caaad2085`
- SHA-256 of supplied file: `21eae50b5dfd29adfe60f9f52130494673b2e4231fab4d0f29827a392bacb38d`
- File size: 2,218,789 bytes
- Package document: `OPS/content.opf`
- Navigation document: `OPS/toc.ncx`

## Edition confidence

The supplied EPUB does not provide enough package metadata to establish the exact print-equivalent edition, publisher or publication date with confidence. The closing author note gives a writing period of November 2015 — July 2016; this is treated as an authorship-period statement, not as proof of a publication date.

Status: `edition_confidence = unknown` for print-equivalent bibliographic details.

## Locator strategy

The source is reflowable, so printed page numbers are not asserted.

Stable study locators use:

1. the exact internal NCX heading;
2. its EPUB content target in the form `xhtml#anchor`;
3. the sequential NCX node number used in `coverage.md`.

This is sufficient to return to the source location without publishing source prose.

## Structural inventory

- NCX navigation nodes: **211**
- leaf sections: **177**
- sequential reading completed: **177 / 177 leaf sections**
- NCX nodes accounted for in coverage map: **211 / 211**
- unread or inaccessible source sections: **0**

Container headings are marked `VERIFIED_STRUCTURE`; they are not counted as unread chapters because their descendants were read sequentially.

## Source handling policy

The EPUB is a research input, not a repository artifact. Public study files may contain:

- bibliographic metadata;
- stable source locators;
- independently worded concepts and rules;
- provenance classifications;
- project-authored counterexamples and evals;
- coverage/audit data.

The public repository must not contain:

- the EPUB itself;
- extracted chapter text;
- a quote corpus;
- close sequential paraphrase of the book;
- a recreated collection of the book's examples.

Raw source material and temporary extraction/search artifacts belong to the private or ephemeral source workspace.
