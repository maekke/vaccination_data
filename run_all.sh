#!/bin/bash

cantons=(
	ag
	ai
	# ar
	be
	bl
	bs
	fr
	ge
	# gl
	gr
	# ju
	lu
	ne
	nw
	# ow
	sg
	sh
	so
	# sz
	tg
	ti
	# ur
	vd
	vs
	zg
	zh
	fl
)

manual_cantons=(
	ar
	gl
	ju
	ow
	sz
	ur
)

err=""

total_file=vaccination_data_total.csv
total_tmp=vaccination_data_total.tmp
rm -f ${total_file} ${total_tmp}
python scrapers/print_header.py > ${total_file}

for canton in ${cantons[*]} ; do
	echo "running canton: ${canton}"
	out_file="vaccination_data_${canton}.csv"
	if [[ ! -f ${out_file} ]] ; then
		echo "creating file: ${out_file}"
		python scrapers/print_header.py > ${out_file}
	fi
	python scrapers/scrape_${canton}_vaccinations.py > tmp.csv || err="${err} ${canton}"
	new_items=$(cut -d ',' -f 1-4 tmp.csv | sort | uniq)
	for new_item in ${new_items} ; do
		echo "removing items with: ${new_item}"
		sed -i -e "/^${new_item}/d" ${out_file}
	done

	cat tmp.csv >> ${out_file}
	head -n 1 ${out_file} > tmp.csv
	tail -n +2 ${out_file} | sort --field-separator=',' -n -k 2,2 -k 4,4 -k 3,3 >> tmp.csv
	mv tmp.csv ${out_file}
	tail -n +2 ${out_file} >> ${total_tmp}
done

for canton in ${manual_cantons[*]} ; do
	out_file="vaccination_data_${canton}.csv"
	if [[ ! -f ${out_file} ]] ; then
		echo "manual canton file does not exist: ${out_file}"
	else
		echo "adding manual data from: ${canton}"
		tail -n +2 ${out_file} >> ${total_tmp}
	fi
done

sort --field-separator=',' -k 2,2 -k 4,4n -k 3,3n -k 1,1 ${total_tmp} >> ${total_file}
rm ${total_tmp}

if [[ -n ${err} ]] ; then
	echo "error in run_all.sh for ${err}"
	#exit 1
fi
