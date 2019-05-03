import requests
import xml.etree.ElementTree as ET  

def request_evidenceCode(reaction_frameid):

	url	= 'https://websvc.biocyc.org/getxml?human:'

	def request(url):
		request = requests.get(url)
		request = request.text
		return request
	try:
		root = ET.fromstring(request(url+reaction_frameid))
		enzr = root.findall('./Reaction/enzymatic-reaction/Enzymatic-Reaction')[0] 
		enzr_frameid = enzr.get('frameid')

		root2 = ET.fromstring(request(url+enzr_frameid))

		try:
			evidence_code=root2.findall('./Enzymatic-Reaction/evidence/Evidence-Code')[0]
			evidence_code_id = evidence_code.get('frameid')
			
		except:
			evidence_code_id = ''
		
	except:
		evidence_code_id = ''

	return evidence_code_id


def dict_evidence_refPos(evidence_list):
	dict_out={}
	i=0
	for elemnt in evidence_list:
		dict_out[elemnt]=i
		i=i+1		
	return dict_out

def string_evidence_code(reaction_list, dict_reaction_evidence_code, evidence_list, evidence_refPos_dic):
	aux_list=[]
	a=['']*len(evidence_refPos_dic)
	
	for react in reaction_list:
		evidence=dict_reaction_evidence_code[react]
		
		if evidence !='':
			position=evidence_refPos_dic[evidence]
			if a[position] != '':
				aux=a[position]
				aux=aux+','+react
				a[position]=aux
			else:
				a[position]=react
	string_out = ('\t').join(a)			
	
	return string_out
	
