import pandas as pd
import numpy as np
import simplejson as json

salida = open('uncurated_proteins_found_in_biocyc.tsv','w')

# Creo una lista de los genes no curados(puede haber mas de uno por fila del archivo)
uncurated_file = pd.read_csv('uncurated_proteins.csv')
uncurated_file = uncurated_file[uncurated_file['Actual release'].isnull()]
genes_uncurated_list = uncurated_file['Gene name'].values  

with open('HS_genes.json') as json.file:
	data = json.load(json.file)
	
# Creo un diccionario donde la key es el gen y el value los pathways asociados de Biocyc
biocyc_genes_dic={}

# Recorro el json. Cada row es un gen.
# Creo lista de listas con los genes sinonimos de Biocyc

for row in data['rows']:
		
	gene_names = row[3]
	
	pathways_names = row[5]
	
	reactions_names = row[6]

	if pathways_names != '' or reactions_names != '':
		# Cuando los nombres vienen en forma de lista.
		# Creo un key para cada uno	
		
		if isinstance(gene_names,list):
			
			synonyms_names_biocyc=[]
						
			for gene in gene_names:
				if isinstance(gene,dict):
					name=gene['label']
					synonyms_names_biocyc.append(name)
				else:
					synonyms_names_biocyc.append(gene)								
			
															
			for gene in gene_names:
				# Cuando el nombre viene como diccionario (caso raro)				
				if isinstance(gene,dict):
					name=gene['label']
					
					inside=[pathways_names,reactions_names,synonyms_names_biocyc]#
										
					biocyc_genes_dic[name]=inside		
					
				else:
					inside=[pathways_names,reactions_names,synonyms_names_biocyc]#
					
					biocyc_genes_dic[gene]=inside
					
		# Cuando los nombres vienen en como un string suelto 	
		else:					
			synonyms_names_biocyc=[]
			if isinstance(gene_names,dict):
				name=gene_names['label']
				synonyms_names_biocyc.append(name)
			else:
				synonyms_names_biocyc.append(gene_names)	
		
							
			# Cuando el nombre viene como diccinario (caso raro)			
			if isinstance(gene_names,dict):
				name=gene_names['label']				
				inside=[pathways_names,reactions_names,synonyms_names_biocyc]#				
				biocyc_genes_dic[name]=inside				
			else:					
				inside=[pathways_names,reactions_names,synonyms_names_biocyc]#
				biocyc_genes_dic[gene_names]=inside		
				
# Creo el header del archivo de salida
salida.write('Uncurated-gene-id'+'\t'+'Uncurated-gene-synonims'+'\t'+'Biocyc-gene-sinomys'+\
'\t'+'Pathway-Biocyc-label'+'\t'+'Pathway-Biocyc-id'+'\t'+'Reaction-Biocyc-label'+'\t'\
+'Reaction-Biocyc-id'+"\n")	

# Comparo la lista de genes no curados y el diccionario de biocyc
for genes_uncurated in genes_uncurated_list:
	genes_uncurated=genes_uncurated.split(' ')	
	found=False
	i=0
	while found==False and len(genes_uncurated)>i:
		
			found=biocyc_genes_dic.get(genes_uncurated[i],False)
			
			if found != False:
								
				found_paths=found[0]
				
				path_label=[]
				path_id=[]
				
				found_reacts=found[1]
				
				react_label=[]	
				react_id=[]				
				
				found_gene_sinomys=found[-1]									

				# Arreglo la salida de pathways, id y label
				
				if isinstance(found_paths,list):
					for path in found_paths:
						path_label.append(path['label'])
						path_id.append(path['frameid'])
				elif isinstance(found_paths,dict):
					path_label.append(found_paths['label'])
					path_id.append(found_paths['frameid'])
				else:
					path_label.append('')
					path_id.append('')
					
				path_label=(',').join(path_label)
				path_id=(',').join(path_id)						
					
				# Arreglo la salida de reactions, id y label
				
				if isinstance(found_reacts,list):
					for react in found_reacts:
						react_id.append(react['frameid'])
						react_label.append(react['label'])
				elif isinstance(found_reacts,dict):
					react_id.append(found_reacts['frameid'])
					react_label.append(found_reacts['label'])
				else:
					react_id.append('')
				
				react_id=(',').join(react_id)								
				react_label=(',').join(react_label)								

				
				# Escribo en la salida el resultado de la iteracion	
				salida.write(genes_uncurated[0]+'\t'+str(genes_uncurated)\
				+'\t'+str(found_gene_sinomys)+'\t'+path_label+'\t'+path_id\
				+'\t'+react_label+'\t'+react_id+"\n")			
			else:
				i=i+1			
salida.close()
		
		
