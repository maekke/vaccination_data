#!/bin/bash

cantons=(
	ai
	ar
	be
	bl
	bs
	ge
	so
	tg
	vd
	zg
)

for canton in ${cantons[*]} ; do
	echo "running canton: ${canton}"
	out_file="vaccination_data_${canton}.csv"
	if [[ ! -f ${out_file} ]] ; then
		echo "creating file: ${out_file}"
		python scrapers/print_header.py > ${out_file}
	fi
	python scrapers/scrape_${canton}_vaccinations.py > tmp.csv
	new_items=$(cut -d ',' -f 1-4 tmp.csv | sort -n | uniq)
	for new_item in ${new_items} ; do
		echo "removing items with: ${new_item}"
		sed -i -e "/^${new_item}/d" ${out_file}
	done

	cat tmp.csv >> ${out_file}
	head -n 1 ${out_file} > tmp.csv
	tail -n +2 ${out_file} | sort -n >> tmp.csv
	mv tmp.csv ${out_file}
done
