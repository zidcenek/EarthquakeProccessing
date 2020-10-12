#!/bin/bash
for i in {1..80}
do 
	if test -f "output/${i}_1.csv"; then 
		if diff output/${i}_0.csv output/${i}_1.csv; then
			echo "Files ${i} are the same"
		else 
			echo "Files ${i} are different"
		fi
	fi
done
