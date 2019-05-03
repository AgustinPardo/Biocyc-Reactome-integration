#!/usr/bin/env python

def arrange_out(data):	
	element_label=[]	
	element_id=[]
	
	if isinstance(data,list):
		for element in data:
			
			if isinstance(element,dict):
				element_label.append(element['label'])
				element_id.append(element['frameid'])
			else:
				element_label=data[0]	
				element_id=data[1]
					
			
	elif isinstance(data,dict):
		element_label.append(data['label'])
		element_id.append(data['frameid'])
	else:
		element_label.append('')
		element_id.append('')

	
	return [element_label,element_id]

def extract_content(gene_names,gene_names_aux,pathways_names,reactions_names,biocyc_genes_dic):
	# Cuando los nombres vienen en forma de lista.
	# Creo un key para cada uno	
	key=None
	values=None
	
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
				pathways_names=arrange_out(pathways_names)
				reactions_names=arrange_out(reactions_names)
				
				key=gene['label']									
				values=pathways_names,reactions_names,synonyms_names_biocyc#
				
				check(key,values,biocyc_genes_dic)				
				
			else:				
				pathways_names=arrange_out(pathways_names)
				reactions_names=arrange_out(reactions_names)
				
				key=gene
				values=pathways_names,reactions_names,synonyms_names_biocyc
				check(key,values,biocyc_genes_dic)#
			
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
			pathways_names=arrange_out(pathways_names)
			reactions_names=arrange_out(reactions_names)
			
			key=gene_names['label']				
			values=pathways_names,reactions_names,synonyms_names_biocyc
			check(key,values,biocyc_genes_dic)#				
				
		else:
			if gene_names == None:				
				pathways_names=arrange_out(pathways_names)
				reactions_names=arrange_out(reactions_names)
				
				key=gene_names_aux
				values=pathways_names,reactions_names,[gene_names],synonyms_names_biocyc
				check(key,values,biocyc_genes_dic)#		
						
			else:				
				pathways_names=arrange_out(pathways_names)
				reactions_names=arrange_out(reactions_names)
					
				key=gene_names
				values=pathways_names,reactions_names,synonyms_names_biocyc
				check(key,values,biocyc_genes_dic)#	

	return 0
	
def combine_list(a,b):
	a=set(a)
	b=set(b)	
	c= a | b
	return list(c)	
	
def compare_label_id(arrA,arrB):
	arrA_0=arrA[0]
	arrB_0=arrB[0]	
	
	arrA_1=arrA[1]	
	arrB_1=arrB[1]
	
	return [combine_list(arrA_0,arrB_0),combine_list(arrA_1,arrB_1)]		
	
def check(key, values, dic):		
		if key in dic.keys():			
			new=values
			old=dic[key]			
			combined_paths=compare_label_id(new[0],old[0])
			combined_reacts=compare_label_id(new[1],old[1])
			combined_synonims=combine_list(new[2],old[2])		
			dic[key]=[combined_paths,combined_reacts,combined_synonims]						
		else:									
			dic[key]=values


