#!/bin/env bash

remote_dir=https://github.com/kernel-panic96/Programming101-Python-2018.git
sub_dir=week05/02-MusicPlayer/
remote_branch=my-solutions


if (( $# == 0 )); then
    read -p "Clone into $(pwd)/pmp/ [Y/n]:" answer
    if [ "$answer" == "" ]; then answer="Y"; fi

    case "$answer" in
        y|yes|Y|YES|Yes)
            local_repo="pmp-git"
            ;;
        *)
            read -p "Provide a dir name for the git repo:" local_repo
            ;;
    esac
fi

echo $local_repo
remote_repo=https://github.com/kernel-panic96/Programming101-Python-2018.git

mkdir -p .$local_repo && cd $_

echo $(pwd)
git init
git remote add origin $remote_repo
git config core.sparseCheckout true

echo $sub_dir >> .git/info/sparse-checkout
git fetch
git merge origin/$remote_branch

pwd
cd ..
echo "./.$local_repo/$sub_dir"

ln -s ./.$local_repo/$sub_dir/ $local_repo
cd $local_repo
pip3 install --user -r requirements.txt
pip3 install --editable .
