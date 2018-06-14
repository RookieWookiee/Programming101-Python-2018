#!/bin/bash

now=`date '+%H_%M_%S'`;
input_file="/tmp/hack-bg-input-$now"
expected_output_file="/tmp/hack-bg-expected-$now"
actual_output_file="/tmp/hack-bg-actual-$now"

grep -e '^>\{1,3\}' $2 | sed -e 's/>>> //g' > $input_file
# -v negates the pattern -> match everything that doesn't start with >>>
grep -v -e '^>\{1,3\}' $2 > $expected_output_file

# Multi line assignments of variables
# https://stackoverflow.com/questions/3717772/regex-grep-for-multi-line-search-needed
# grep -Pz '(?s)^>>>.*?=.*?(?:>>>)' word_counter_tests

python3.6 -i $1 < $input_file 2> /dev/null > $actual_output_file

readarray expected_lines < $expected_output_file
readarray actual_lines < $actual_output_file

expected_lines_count=${#expected_lines[@]}
actual_lines_count=${#actual_lines[@]}

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo $2
for (( i=0; i <= $(( $expected_lines_count - 1 )); i++ ))
do
    echo -ne "Expected:\t"
    echo ${expected_lines[$i]}

    if [ "${expected_lines[$i]}" != "${actual_lines[$i]}" ]; then
        echo -ne "${RED}Actual${NC}:\t\t"
        echo ${actual_lines[$i]}
    else
        echo -ne "${GREEN}Actual${NC}:\t\t"
        echo ${actual_lines[$i]}
    fi
done

if [ $((expected_lines_count)) -ne $((actual_lines_count)) ]; then
    echo -n 'The number between expected and actual input differ'
fi

rm $input_file
rm $expected_output_file
rm $actual_output_file
