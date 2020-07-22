#!/bin/bash

## Usage method.
## The directory path should not contain the last / (forward slash)

## It must be like this:
## ./run_all.sh /home/emanuel/ICCRC/Positive
## and not like this
## ./run_all.sh /home/emanuel/ICCRC/Positive/  (WRONG!)


#### ATTENTION !!! ####
## You have to run it in every subdirectory classification, i.e.:

## ./run_all.sh /home/emanuel/ICCRC/Positive 
## ./run_all.sh /home/emanuel/ICCRC/Negative
## ./run_all.sh /home/emanuel/ICCRC/Neutral

## You cannot run the script like this:
## ./run_all.sh /home/emanuel/ICCRC (WRONG!!!!!!!)

## ./run_all.sh full_directory_of_the_text_files 

input_dir=$1
output_dir=$input_dir-output

echo "##################"

echo
echo "INPUT DIRECTORY: $input_dir"

echo
echo "##################"
echo
echo "OUTPUT DIRECTORY: $output_dir"

echo


## This script basically runs all the text files within the directories.
## It may take some time


count=1
#Input files

echo "LET THE GAMES BEGIN!!!!"
sleep 5
echo "Warning: It may take some time, just be patient..."

for full_file_directory in $(find $input_dir -type f -iname 'http*'|grep -E -v  '\s|arabic|francais|shahamat\.info|shahamat\-(arabic|farsi|movie|urdu)|kavkazcenter\.(com|info|net)\_80\_\_(rus|arab|tur)|\_arabic\.|\_80\_\_(africa\_|asia|bits|china)|cnnmexico|cnnespanol\.cnn|mexico\.cnn|\_quebec\.|cnn\.co\.jp|cnnturk|\_(fr|ar|es|pa|ru|tu|ur|so|sw|zh)\_|\-fr\_|fra\.aspx|hamas|french')
do

	echo $full_file_directory

	file=$(echo $full_file_directory | rev | cut -f 1 -d "/" | rev)
	echo $file
	sub_folder_file=$(echo $file | cut -f 2 -d '[' | cut -f 1 -d ']')
	echo $sub_folder_file	
	output_sub_dir=$output_dir/$sub_folder_file/
	echo $output_dir/$sub_folder_file/
			
	~/posit/./pos_all.sh $full_file_directory



	echo
	echo "################################# Input file: $full_file_directory" 

	echo
	echo "################################# Output file $count) $output_sub_dir"

	echo

	echo
	mkdir -p $output_sub_dir
	mv $PWD/results/* $output_sub_dir
	rm $output_sub_dir/ASL.dat $output_sub_dir/chars.dat $output_sub_dir/pos_summary.dat $output_sub_dir/pos_totals.csv $output_sub_dir/pos_totals.dat $output_sub_dir/type_token_count.txt
	count=$((count+1))

done

echo "DONE!"
