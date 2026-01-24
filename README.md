# journal-utils

Selected scripts (bash & python) for stuff mentioned in [njbrown.com/tags/journaling](https://www.njbrown.com/tags/journaling/), specifically articles 48, 67, and 73.

Basic overview:

```
/bash/.zshrc:
    alias "edj": edit daily journal entry
    alias "cje": cd into journalEntries directory
    alias "je": run je.sh (checker script)
    function "browse": page through journal entries
    function "search": grep for query (with highlighting)
/bash/je.sh:
    purposes:
    (1) ensure streak intact (no entries missing)
    (2) ensure no entries have non-ASCII characters
    (3) ensure no entries are <280 bytes long
/python/main.py:
    plot_avg_sizes: plot byte sizes of entries vs. time
    find_most_common_words: self-explanatory
    plot_string_occurrences_over_time: self-explanatory
```

The scripts & utilities make my life far more convenient and allow me to keep my 750+ daily journaling streak much more easily.

License: MIT
