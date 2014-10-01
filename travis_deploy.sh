#!/usr/bin/env bash
SOURCE_BRANCH=writing
GH_BRANCH=master
TARGET_REPO=mgaitan/mgaitan.github.com.git
NIKOLA_OUTPUT_FOLDER=output


if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
    echo -e "Starting to deploy to Github Pages\n"
    if [ "$TRAVIS" == "true" ]; then
        git config --global user.email "travis@travis-ci.org"
        git config --global user.name "Travis"
    fi
    nikola build
    git add .
    git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to Github Pages"
    git push -fq https://${GH_TOKEN}@github.com/$TARGET_REPO $SOURCE_BRANCH > /dev/null
    git subtree push --prefix=$NIKOLA_OUTPUT_FOLDER https://${GH_TOKEN}@github.com/$TARGET_REPO $GH_BRANCH
    echo -e "Deploy completed\n"
fi