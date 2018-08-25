#!/usr/bin/env bash

echo '-----------------------------------------------'
echo 'Setting up gitflow...'
echo '-----------------------------------------------'
git flow init -d
git config gitflow.feature.start.fetch TRUE
git config gitflow.feature.finish.fetch TRUE
git config gitflow.feature.finish.squash TRUE
git config gitflow.feature.finish.keep FALSE
git config gitflow.hotfix.start.fetch TRUE
git config gitflow.hotfix.finish.fetch TRUE
git config gitflow.hotfix.finish.squash TRUE
git config gitflow.hotfix.finish.keep FALSE
git config gitflow.release.start.fetch TRUE
git config gitflow.release.finish.fetch TRUE
git config gitflow.release.finish.keep FALSE