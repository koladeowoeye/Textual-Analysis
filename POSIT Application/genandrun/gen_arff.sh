#!/bin/bash

## Usage Method

## This script was developed to classify the ICCRC data, which has 3 classifications: POSITIVE, NEUTRAL, NEGATIVE.
## One fourth classification type was included to classify the UNKNOWN data based on the initial dataset provided by ICCRC

## So to generate an ARFF file for the ICCRC data you need to use the following command:
### ->> ./gen_arff.sh full_directory_of_the_output_of_the_already_processed_posit_files
## In which the full directory must have the following tree structure

## After you generate all the files with the run_all.sh scripts, new folders with "-output" at the end will be created, so if you want to organize your directory structure better like I did, you can move all the new folders to a new one, like the following, in which I moved the *-output* folders to a new general Output folder, that contains only the posit output structure.

# emanuel@emanuel-PC $ tree -d -L 2 /home/emanuel/ICCRC/Output
#
#.
#├── Negative-output
#│   ├── jqj0kwbA
#│   └── nm37h6iN
#├── Neutral-output
#│   ├── 08ngDNKQ
#│   ├── 0fgVDQGB
#│   └── 0J9pdTyp
#└── Positive-output
#    ├── 0qsmtj82
#    ├── 1Ku4CbQS
#    ├── 2u0gnV3L
#    └── 3gRipcqn

# emanuel@emanuel-PC $ ./gen_arff.sh /home/efds/ICCRC/Output 
# Will generate the extremist.arff file with the correct classification

### ATTENTION !!! ###

## So, if you're using a data that is UNKONW, you have to specify it in the arguments as follow:
# ./gen_arff.sh full_directory_of_the_output_of_the_already_processed_posit_files UNKNOWN

echo "@RELATION ICCRC" > extremists.arff
echo >> extremists.arff
unk_class=$2


#SUMMARY
echo "@ATTRIBUTE classification {NEGATIVE, POSITIVE, NEUTRAL, UNKNOWN}" >> extremists.arff
echo "@ATTRIBUTE total_words NUMERIC" >> extremists.arff
echo "@ATTRIBUTE total_unique_words NUMERIC" >> extremists.arff
echo "@ATTRIBUTE ttr NUMERIC" >> extremists.arff
echo "@ATTRIBUTE number_of_sentences NUMERIC" >> extremists.arff
echo "@ATTRIBUTE asl NUMERIC" >> extremists.arff
echo "@ATTRIBUTE number_of_chars NUMERIC" >> extremists.arff
echo "@ATTRIBUTE awl NUMERIC" >> extremists.arff

#TOKENS
tokens="$noun_types, $verb_types, $adjective_types, $preposition_types, $possessive_types, $personal_types, $determiner_types, $adverb_types, $particle_types, $interjection_types"
	

echo "@ATTRIBUTE noun_types NUMERIC" >> extremists.arff
echo "@ATTRIBUTE verb_types NUMERIC" >> extremists.arff
echo "@ATTRIBUTE adjective_types NUMERIC" >> extremists.arff
echo "@ATTRIBUTE preposition_types NUMERIC" >> extremists.arff
echo "@ATTRIBUTE possessive_types NUMERIC" >> extremists.arff

echo "@ATTRIBUTE personal_types NUMERIC" >> extremists.arff
echo "@ATTRIBUTE determiner_types NUMERIC" >> extremists.arff
echo "@ATTRIBUTE adverb_types NUMERIC" >> extremists.arff
echo "@ATTRIBUTE particle_types NUMERIC" >> extremists.arff
echo "@ATTRIBUTE interjection_types NUMERIC" >> extremists.arff

#TYPES
types="$verbs, $nouns, $prepositions, $possessive, $personal, $particles, $interjections, $determiners, $adverbs, $adjectives"

echo "@ATTRIBUTE verbs NUMERIC" >> extremists.arff
echo "@ATTRIBUTE nouns NUMERIC" >> extremists.arff
echo "@ATTRIBUTE preposition NUMERIC" >> extremists.arff
echo "@ATTRIBUTE possessive NUMERIC" >> extremists.arff
echo "@ATTRIBUTE personal NUMERIC" >> extremists.arff

echo "@ATTRIBUTE particles NUMERIC" >> extremists.arff
echo "@ATTRIBUTE interjections NUMERIC" >> extremists.arff
echo "@ATTRIBUTE determiners NUMERIC" >> extremists.arff
echo "@ATTRIBUTE adverbs NUMERIC" >> extremists.arff
echo "@ATTRIBUTE adjectives NUMERIC" >> extremists.arff

echo >> extremists.arff
echo "@DATA" >> extremists.arff
for file in $(find $1 -type d -maxdepth 2)
#for file in $(du $1 | awk '{print $2}')
do

	for arq in $(ls $file | grep summary.txt)
	do


		arquivo=$(cat $file/$arq | grep '.txt' | cut -d "[" -f 2 | cut -d "]" -f 1)
				
		class=$(echo $file | rev | cut -d "/" -f 2| rev | cut -f 1 -d '-')
		class=${class^^}

		totalWords=$(cat $file/$arq | grep 'Total words' | cut -d ":" -f 1| cut -d " " -f 1)
#		echo $totalWords	

		totalUniqueWords=$(cat $file/$arq | grep 'Total unique words' | cut -d ":" -f 1 | cut -d " " -f 1)
#		echo $totalUniqueWords

		ttr=$(cat $file/$arq | grep '(TTR)' | cut -d ":" -f 1 | cut -d " " -f 1)
#		echo $ttr

		numberSentences=$(cat $file/$arq | grep 'Number of sentences' | cut -d ":" -f 1 | cut -d " " -f 1)
#		echo $numberSentences

		asl=$(cat $file/$arq | grep '(ASL)' | cut -d ":" -f 1 | cut -d " " -f 1)
#		echo $asl

		numberOfChars=$(cat $file/$arq | grep 'Number of characters' | cut -d ":" -f 1 | cut -d " " -f 1)
#		echo $numberOfChars

		awl=$(cat $file/$arq | grep '(AWL)' | cut -d ":" -f 1 | cut -d " " -f 1)
#		echo $awl


		if [ "$totalWords" = "" ]
		then
			totalWords=0
		fi

		if [ "$totalUniqueWords" = "" ]
		then
			totalUniqueWords=0
		fi

		if [ "$ttr" = "" ]
		then
			ttr=0
		fi
		
		if [ "$numberSentences" = "" ]
		then
			numberSentences=0
		fi

		if [ "$asl" = "" ]
		then
			asl=0
		fi

		if [ "$numberOfChars" = "" ]
		then
			numberOfChars=0
		fi

		if [ "$awl" = "" ]
		then
			awl=0
		fi
		
		summary="$totalWords, $totalUniqueWords, $ttr, $numberSentences, $asl, $numberOfChars, $awl"
#		echo $summary

		## TOKENS

		noun_types=$(cat $file/$arq | grep ':noun_types' | cut -d ":" -f 1 | cut -d " " -f 1)
		verb_types=$(cat $file/$arq | grep ':verb_types' | cut -d ":" -f 1 | cut -d " " -f 1)		
		adjective_types=$(cat $file/$arq | grep ':adjective_types' | cut -d ":" -f 1 | cut -d " " -f 1)
		preposition_types=$(cat $file/$arq | grep ':preposition_types' | cut -d ":" -f 1 | cut -d " " -f 1)
		possessive_types=$(cat $file/$arq | grep ':possessive_pronoun' | cut -d ":" -f 1 | cut -d " " -f 1)
		personal_types=$(cat $file/$arq | grep ':personal_pronoun' | cut -d ":" -f 1 | cut -d " " -f 1)
		determiner_types=$(cat $file/$arq | grep ':determiner_types' | cut -d ":" -f 1 | cut -d " " -f 1)
		adverb_types=$(cat $file/$arq | grep ':adverb_types' | cut -d ":" -f 1 | cut -d " " -f 1)
		particle_types=$(cat $file/$arq | grep ':particle_types' | cut -d ":" -f 1 | cut -d " " -f 1)
		interjection_types=$(cat $file/$arq | grep ':interjection_types' | cut -d ":" -f 1 | cut -d " " -f 1)

		if [ "$noun_types" = "" ]
		then
			noun_types=0
		fi
		
		if [ "$verb_types" = "" ]
		then
			verb_types=0
		fi
			
		if [ "$adjective_types" = "" ]
		then
			adjective_types=0
		fi


		if [ "$preposition_types" = "" ]
		then
			preposition_types=0
		fi


		if [ "$possessive_types" = "" ]
		then
			possessive_types=0
		fi

		if [ "$personal_types" = "" ]
		then
			personal_types=0
		fi

		if [ "$determiner_types" = "" ]
		then
			determiner_types=0
		fi

		if [ "$adverb_types" = "" ]
		then
			adverb_types=0
		fi

		if [ "$particle_types" = "" ]
		then
			particle_types=0
		fi

		if [ "$interjection_types" = "" ]
		then
			interjection_types=0
		fi


		tokens="$noun_types, $verb_types, $adjective_types, $preposition_types, $possessive_types, $personal_types, $determiner_types, $adverb_types, $particle_types, $interjection_types"
#		echo $tokens

		## Pos Types

		verbs=$(cat $file/$arq | grep ':verbs' | cut -d ":" -f 1 | cut -d " " -f 1)
		nouns=$(cat $file/$arq | grep ':nouns' | cut -d ":" -f 1 | cut -d " " -f 1)
		prepositions=$(cat $file/$arq | grep ':prepositions' | cut -d ":" -f 1 | cut -d " " -f 1)
		possessive=$(cat $file/$arq | grep ':possessive pronouns' | cut -d ":" -f 1 | cut -d " " -f 1)
		personal=$(cat $file/$arq | grep ':personal pronouns' | cut -d ":" -f 1 | cut -d " " -f 1)
		particles=$(cat $file/$arq | grep ':particles' | cut -d ":" -f 1 | cut -d " " -f 1)
		interjections=$(cat $file/$arq | grep ':interjections' | cut -d ":" -f 1 | cut -d " " -f 1)
		determiners=$(cat $file/$arq | grep ':determiners' | cut -d ":" -f 1 | cut -d " " -f 1)
		adverbs=$(cat $file/$arq | grep ':adverbs' | cut -d ":" -f 1 | cut -d " " -f 1)
		adjectives=$(cat $file/$arq | grep ':adjectives' | cut -d ":" -f 1 | cut -d " " -f 1)

		types="$verbs, $nouns, $prepositions, $possessive, $personal, $particles, $interjections, $determiners, $adverbs, $adjectives"
		#echo $types
		
		if [ "$verb" = "" ]
		then
			verbs=0
		fi
		
		if [ "$nouns" = "" ]
		then
			nouns=0
		fi
			
		if [ "$prepositions" = "" ]
		then
			prepositions=0
		fi


		if [ "$possessive" = "" ]
		then
			possessive=0
		fi


		if [ "$personal" = "" ]
		then
			personal=0
		fi

		if [ "$particles" = "" ]
		then
			particles=0
		fi

		if [ "$interjections" = "" ]
		then
			interjections=0
		fi

		if [ "$determiners" = "" ]
		then
			determiners=0
		fi

		if [ "$adverbs" = "" ]
		then
			adverbs=0
		fi

		if [ "$adjectives" = "" ]
		then
			adjectives=0
		fi

		res="$summary, $tokens, $types"	

		if [[ -z $unk_class ]]; then 

			res="$class, $summary, $tokens, $types"	
		else 
			res="UNKNOWN, $summary, $tokens, $types"	
		fi

		echo "$res"
		echo $res >> extremists.arff	

	done
done
