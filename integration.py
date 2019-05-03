#!/usr/bin/env python

import pandas as pd
import simplejson as json
import parser
import biocyc_retrieve

salida = open('uncurated_proteins_found_in_biocyc.tsv','w')

# Creo una lista de los genes no curados(puede haber mas de uno por fila del archivo)
uncurated_file			=		pd.read_csv('/home/agustin/Downloads/Biocyc_integration/files/uncurated_proteins.csv')
uncurated_file 			= 		uncurated_file[uncurated_file['Actual release'].isnull()]
genes_uncurated_list 	= 		uncurated_file['Gene name'].unique()

with open('/home/agustin/Downloads/Biocyc_integration/files/HS_genes.json') as json.file:
	data = json.load(json.file)
	
# Creo un diccionario donde la key es el gen y el value los pathways asociados de Biocyc

biocyc_genes_dic = {}

# Recorro el json. Cada row es un gen.
# Creo lista de listas con los genes sinonimos de Biocyc
for row in data['rows']:
		
	gene_names			=		row[3]	
	gene_names_aux		=		row[4]		
	pathways_names		=		row[5]	
	reactions_names		=		row[6]

	if pathways_names != '' or reactions_names != '':		
		parser.extract_content(gene_names,gene_names_aux,pathways_names,reactions_names,biocyc_genes_dic)
				
# Comparo la lista de genes no curados y el diccionario de biocyc

reaction_list = [line.rstrip('\n') for line in open('reaction_list.txt')]
evidence_list = [line.rstrip('\n') for line in open('reaction_evidence_codes.txt')]

with open('reaction_evidence_codes_dict.json', 'r') as f:
	distros_dict = json.load(f)
	dict_reaction_evidence_code = dict((k.encode('utf8'), v.encode('utf8')) for k, v in distros_dict.items())

string_evidence = ('\t').join(evidence_list)

# Creo el header del archivo de salida
salida.write('Uncurated-gene-id'+'\t'+'Uncurated-gene-synonims'+'\t'+'Biocyc-gene-sinomys'+\
'\t'+'Pathway-Biocyc-label'+'\t'+'Pathway-Biocyc-id'+'\t'+'Reaction-Biocyc-label'+'\t'\
+'Reaction-Biocyc-id'+'\t'+string_evidence+"\n")	

evidence_refPos_dic=biocyc_retrieve.dict_evidence_refPos(evidence_list)

for genes_uncurated in genes_uncurated_list:
	
	genes_uncurated		=		genes_uncurated.split(' ')	
	found				=		False
	i=0
	
	while found == False and len(genes_uncurated)>i:
		
			found = biocyc_genes_dic.get(genes_uncurated[i],False)
			
			if found != False:			
								
				found_paths		=		found[0]				
				path_label		=		found_paths[0]
				path_id			=		found_paths[1]
				path_label		=		(',').join(path_label)
				path_id			=		(',').join(path_id)
				
				found_reacts	=		found[1]				
				react_label		=		found_reacts[0]
				react_id		=		found_reacts[1]							
				react_label		=		(',').join(react_label)
				react_id		=		(',').join(react_id)
				
				
				# Busco el Evidence code de cada reaccion				
				string_evidences = biocyc_retrieve.string_evidence_code(found_reacts[1], dict_reaction_evidence_code, evidence_list, evidence_refPos_dic)
								
				#				

				found_gene_sinomys=found[-1]
				
				# Escribo en la salida el resultado de la iteracion	
				salida.write(genes_uncurated[0]+'\t'+str(genes_uncurated)\
				+'\t'+str(found_gene_sinomys)+'\t'+path_label+'\t'+path_id\
				+'\t'+react_label+'\t'+react_id+'\t'+string_evidences+"\n")			
			else:
				i = i+1

salida.close()
