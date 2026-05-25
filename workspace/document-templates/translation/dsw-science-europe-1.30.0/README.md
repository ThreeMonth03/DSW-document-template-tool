# Translation Tree

This folder is the translator-facing tree exported from the expanded
template workspace.

- Each translation unit has its own `translation.md` file.
- Each file starts with a plain `Sentence (en)` section for
  translator review.
- Wrapper-level blocks from the expanded workspace are split into smaller
  translator-facing units whenever the source structure allows it.
- Edit only `Translation (zh_Hant)` sections.
- Keep every `{placeholder}` shown in the sentence. You may reorder
  placeholders for grammar; sync converts them back to Jinja variables.
- Source hashes in the metadata are machine guards; do not edit them.
- If a translation file is deleted or its markdown block is broken, run
  `make export-translation-tree` to rebuild the file skeleton.
- Run `make sync-translation-tree` to apply translator edits back into a
  generated template copy.
