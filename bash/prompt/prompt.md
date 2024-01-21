# Custom Bash Prompt

## Purpose

Quick-loading and lightweight custom prompt written in Bash with git branch detection for your linux machine without the need for large libraries.

## Instructions

1. Give execute permissions to prompt eg. chmod +x /path/to/prompt.sh
2. Add the following lines (without leading #s) to your ~/.bashrc or ~/.bash_profile to include prompt.

```
prompt=/path/to/prompt.sh
if [ -f $prompt ]; then . $prompt; fi
```

3. Restart terminal for changes to take effect.
