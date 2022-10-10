#!/bin/bash --login
echo "--------------------------------------------"
echo "Checkout to latest tag in Core"
echo "--------------------------------------------"
git checkout v1.4.2 -f
echo "--------------------------------------------"
echo "Describing Head"
echo "--------------------------------------------"
git describe > HEAD
echo "____________________________________________"
echo "Making changes to config.json"
echo "____________________________________________"
#cp config.json.example application.json
echo "____________________________________________"
