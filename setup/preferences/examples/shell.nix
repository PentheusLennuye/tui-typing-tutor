# For developers on NixOS
# Developers on other OSes may ignore this file
with import <nixpkgs> {};
let
  blue = "\\e[0;94m";
  me = "tui-typing-tutor";
  reset="\\e[0m";
in
pkgs.mkShell {
  name = "${me}";
  NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [
    stdenv.cc.cc
    enchant
  ];

  NIX_LD = lib.fileContents "${stdenv.cc}/nix-support/dynamic-linker";

  packages = with pkgs; [
    bc
    python313
    poetry
  ];

  shellHook = ''
     export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH

     # Define PS1 every return -----------------------------------------------------------
     ahead=
     behind=
     ahead_behind() {
        git branch -vv | grep -q origin || return
        ahead=$([ `git rev-list --count @{u}..HEAD` -gt 0 ] && echo -n "⇡")
        behind=$([ `git rev-list --count HEAD..@{u}` -gt 0 ] && echo -n "⇣")
     }

     git_prompt() {
        dc="${blue}"
        rs="${reset}"


        dir="$dc\nnix-shell:…/\$(pwd | sed 's/.*\(${me}\)/\1/')"
        untracked=$([ `git ls-files -o --exclude-standard | wc -l` -gt 0 ] && echo -n "?")
        deleted=$([ `git ls-files -d | wc -l` -gt 0 ] && echo -n "x")
        modified=$([ `git ls-files -m | wc -l` -gt 0 ] && echo -n "!")
        staged=$([ `git diff --staged --name-only | wc -l` -gt 0 ] && echo -n "+")

        branch="$(git status 2>/dev/null | grep 'On branch' | sed 's/On branch //')"
        ahead_behind $branch
        dbranch=" $branch"

        PS1="$dir $rs$dbranch [$modified$deleted$staged$untracked$ahead$behind]\n> "
     }

     update_prompt() {
        if [ $(pwd | grep "${me}") ]; then
            git_prompt
        fi
     }

     export PROMPT_COMMAND=update_prompt
   '';
}



