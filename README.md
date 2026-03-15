# journal-utils

Selected scripts for articles in [njbrown.com/tags/journaling](https://www.njbrown.com/tags/journaling/).

Basic overview:

```
/shell/zshrc:
    alias "edj": edit daily journal entry
    alias "cje": cd into journalEntries directory
    alias "je": run je.sh (checker script)
    function "browse": page through journal entries
    function "search": grep for query (with highlighting)
/shell/je.sh:
    purposes:
    (1) ensure streak intact (no entries missing)
    (2) ensure no entries have non-ASCII characters
    (3) ensure no entries are <280 bytes long
/python/main.py:
    plot_avg_sizes: plot byte sizes of entries vs. time
    find_most_common_words: self-explanatory
    plot_string_occurrences_over_time: self-explanatory
```

The scripts are convenient and help me keep my 800-day+ daily journaling streak more easily.

License: MIT
