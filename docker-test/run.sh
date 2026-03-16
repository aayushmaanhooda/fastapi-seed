#!/bin/bash
# Run from project root: bash docker-test/run.sh

echo ""
echo "========================================"
echo " TEST 1: no uv installed"
echo " Expected: uv is not installed error"
echo "========================================"
docker build -f docker-test/Dockerfile.no-uv -t seed-test-no-uv . -q
docker run --rm seed-test-no-uv

echo ""
echo "========================================"
echo " TEST 2: no git installed"
echo " Expected: git is not installed error"
echo "========================================"
docker build -f docker-test/Dockerfile.no-git -t seed-test-no-git . -q
docker run --rm seed-test-no-git

echo ""
echo "========================================"
echo " TEST 3: full happy path (uv + git)"
echo " Expected: full scaffolding works"
echo "========================================"
docker build -f docker-test/Dockerfile.full -t seed-test-full . -q
docker run --rm -it seed-test-full
