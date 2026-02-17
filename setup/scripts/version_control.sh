#!/usr/bin/env bash
# Ensure that the source branch version is higher than the target branch version.


target_name=
branch_name=
branch_verson=
target_version=

get_branch_name() {
    branch_name=$(git symbolic-ref --short HEAD)
}

improper_branch_name() {
    echo $branch_name | grep -E '^main$|^develop$|^hotfix/|^feature/|^bugfix/|^doc/|^rc/'
    if [ $? -ne 0 ]; then
        echo "'$branch_name' is not an acceptable branch name"
        exit 1
    fi
    echo "branch name '$branch_name' is ok."
}

get_target_branch_name() {
    if [ "$branch_name" == "rc" ]; then
        target="main"
    elif [ `echo $branch_name | grep develop` ]; then  # rc shares the version w/ develop
        target="main"
    elif [ `echo $branch_name | grep hotfix` ]; then
        target="main"
    elif [ `echo $branch_name | grep feature` ]; then
        target="develop"
    elif [ `echo $branch_name | grep bugfix` ]; then
        target="develop"
    else
        target="stop"  # doc does not need any version change
    fi
}

check_changelog() {
    if [ ! `git diff --stat $target -- CHANGELOG.md | grep -q CHANGELOG.md` ]; then
        echo "!! Do not attempt a pull request without updating CHANGELOG.md"
    fi
}

check_pyproject_version() {
    branch_version=$(grep -E '^version\s*' pyproject.toml | sed 's/^version.*=.*"\(.*\)"/\1/')
    target_version=$(git show ${target}:pyproject.toml | grep -E '^version\s*' pyproject.toml \
        | sed 's/^version.*=.*"\(.*\)"/\1/')

    # The 'bc' calculator needs real floats to compare, not x.y.z
    branch_version_bc=$(echo $branch_version | sed -E 's/([0-9]+\.[0-9]+)\.([0-9]+$)/\1\2/')
    target_version_bc=$(echo $target_version | sed -E 's/([0-9]+\.[0-9]+)\.([0-9]+$)/\1\2/')

    if [ `echo "${branch_version_bc} <= ${target_version_bc}" | bc` ]; then
        echo "!! pyproject.toml version is ${branch_version}. Branch ${target}'s version is ${target_version}."
        echo "Upgrade pyproject.toml's version before submitting a pull request."
    fi
}

get_branch_name
improper_branch_name || exit 1
get_target_branch_name

if [ "$target" == "stop" ]; then
    echo "Branch ${branch_name} does not need to compare version numbers"
    exit 0
fi

check_changelog
check_pyproject_version

