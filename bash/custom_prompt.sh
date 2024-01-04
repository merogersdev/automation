#! /usr/bin/bash

# Version 1.0

function custom_prompt {
  git --version 2>&1 > /dev/null
  GIT_IS_AVAILABLE=$?

  # Set Colors
  local DIR_COLOR="\[\033[01;34m\]"
  local GIT_COLOR="\[\033[00;90m\]"
  local ARR_COLOR="\[\033[01;35m\]"
  local TEXT_COLOR="\[\033[00;00m\]"

  # Git Prompt Settings
  local GIT_FILES="GIT_PS1_SHOWUNTRACKEDFILES=1"
  local GIT_DIRTY="GIT_PS1_SHOWDIRTYSTATE=1"

  # Define Segments (Directory, Git Branch & Status, User Prompt)
  local DIRECTORY="$DIR_COLOR\w"
  local GIT_PROMPT="$GIT_COLOR\$($GIT_FILES $GIT_DIRTY __git_ps1)"
  local USER_PROMPT="\n$ARR_COLOR❯ $TEXT_COLOR"

  # Trim directory to only 1 level
  export PROMPT_DIRTRIM=1

  #Show prompt with git branch data if git is installed
  if (( $GIT_IS_AVAILABLE == 0 ))
  then
    export PS1="\n$DIRECTORY $GIT_PROMPT $USER_PROMPT"
  else
    export PS1="\n$DIRECTORY $USER_PROMPT"
  fi
}

# Use Prompt
custom_prompt
