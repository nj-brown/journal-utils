alias edj='vim "$HOME/Documents/journalEntries/$(date +%Y.%m.%d).txt"'
alias cje="cd ~/Documents/journalEntries"
alias je="$HOME/Documents/journal-utils/bash/je.sh"

browse() {
  cd ~/Documents/journalEntries/ || return
  vim 2024.* 2025.* 2026.* \
    -c "nnoremap ] :n<CR>" \
    -c "nnoremap [ :N<CR>"
}

search() {
    grep -rni --color=always "$*" ~/Documents/journalEntries \
    | sed "s|$HOME/Documents/journalEntries/||" \
    | less -R
}
