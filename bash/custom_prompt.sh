#! /usr/bin/bash

# Version 1.1

function check_git_installed {
  if git --version &>/dev/null;
  then
      return 0
  else
      return 1
  fi
}

function get_git_prompt {
  line="--------------------------------"
  if [ ! -f ~/.git-prompt.sh ]; then
    echo $line
    echo "Getting Git Prompt"
    echo $line
    curl -o ~/.git-prompt.sh https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
    echo $line
    echo "Git Prompt Downloaded"
    echo $line
  fi
  source ~/.git-prompt.sh
}

function custom_prompt {
  # Set Colors
  local DIR_COLOR="\[\033[01;34m\]" # Blue
  local GIT_COLOR="\[\033[00;90m\]" # Gray
  local ARROW_COLOR="\[\033[01;35m\]" # Magenta
  local TEXT_COLOR="\[\033[00;00m\]" # White

  # Git Prompt Settings
  local GIT_FILES="GIT_PS1_SHOWUNTRACKEDFILES=1"
  local GIT_DIRTY="GIT_PS1_SHOWDIRTYSTATE=1"

  # Define Segments (Directory, Git Branch & Status, User Prompt)
  local DIRECTORY="$DIR_COLOR\w"
  local GIT_PROMPT="$GIT_COLOR\$($GIT_FILES $GIT_DIRTY __git_ps1)"
  local USER_PROMPT="\n$ARROW_COLOR❯ $TEXT_COLOR"

  # Trim directory to only 1 level
  export PROMPT_DIRTRIM=1

  # Show prompt with git branch data if git is installed
  if check_git_installed -eq 0;
  then
    get_git_prompt
    export PS1="\n$DIRECTORY $GIT_PROMPT $USER_PROMPT"
  else
    export PS1="\n$DIRECTORY $USER_PROMPT"
  fi
}

# Use Prompt
custom_prompt
