#!/bin/bash --login
echo "--------------------------------------------"
echo "Checkout to latest tag"
echo "--------------------------------------------"
git checkout v4.16.2 -f
echo "--------------------------------------------"
echo "Describing Head"
echo "--------------------------------------------"
git describe > HEAD
echo "____________________________________________"
echo "Removing Gemfile.lock"
echo "____________________________________________"
rm Gemfile.lock
echo "____________________________________________"
echo "Installing Local Gems"
echo "____________________________________________"
bundle install --local
echo "--------------------------------------------"
echo "running bin_update art"
echo "____________________________________________"
./bin/update_art_metadata.sh development
echo "--------------------------------------------"
