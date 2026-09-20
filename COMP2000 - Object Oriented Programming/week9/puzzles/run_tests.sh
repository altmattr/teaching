#!/bin/bash
set -e

cd "$(dirname "$0")"

CP="lib/junit-4.13.2.jar:lib/hamcrest-core-1.3.jar"

rm -rf out
mkdir -p out

javac -cp "$CP" -d out Puzzle*.java Puzzle*Test.java
java -cp "out:$CP" org.junit.runner.JUnitCore \
    Puzzle1Test Puzzle2Test Puzzle3Test Puzzle4Test Puzzle5Test Puzzle6Test

rm -rf out