import json
import pprint
import re
pp = pprint.PrettyPrinter(indent=4)

def cleanUpUnicode(string):
    replacements = {
        '\\u00C9': 'É',  
        '\\u00E7': 'ç', 
        '\\u00EF': 'ï', 
        '\\u00DC': 'Ü', 
        '\\u00DF': 'ß', 
        '\\u00E4': 'ä', 
        '\\u00EC': 'ì', 
        '\\u00EA': 'ê', 
        '\\u00F2': 'ò', 
        '\\u00F6': 'ö', 
        '\\u00FC': 'ü', 
        '\\u00E8': 'è', 
        '\\u00E2': 'â', 
        '\\u00E1': 'á', 
        '\\u00E9': 'é', 
        '\\u00ED': 'í', 
        '\\u00D6': 'Ö', 
        '\\u00E0': 'à', 
        '\\u00EE': 'î', 
        '\\u00F9': 'ù', 
        '\\u00F4': 'ô', 
        '\\u00B4': '´', 
        '\\u00C7': 'Ç', 
        '\\u00FB': 'û', 
        '\\u00EB': 'ë', 
        '\\u00F1': 'ñ',
        '\\u00C4': 'Ä',
        '\\u00C0': 'À', 
        '\\u2019': '’', 
        '\\u00CA': 'Ê'
    }
    string = string
    for k in replacements.keys():
        string = string.replace(k, replacements[k])
        
    return string


with open('iconclass.nt', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

json_store = {}
unicodechars = []




#<http://iconclass.org/0>
for line in lines:
    #cleanup unicode
    #line = cleanUpUnicode(line)
    triple = line.strip().split(' ')
    key = triple[0].strip()
    if key not in json_store.keys():
        json_store[key] = {}
    # <http://www.w3.org/2004/02/skos/core#inScheme>
    if 'skos/core#' in triple[1]:
        predicate = triple[1].strip().split('#')[-1].replace('>', '').strip()
                  
        if '#prefLabel' in triple[1]:
            if predicate not in json_store[key].keys():
                json_store[key][predicate] = { 'all': [] }
            objct = ' '.join(triple[2:]).replace(' .', '').replace('"', '').strip()
            if '\\u' in objct:
                objct = cleanUpUnicode(objct)
                for find in re.findall(r'\\u.{4}', objct):
                    unicodechars.append(find)
                    #print(string.replace(find, chr(int(find.replace('\\u', '')))))
            json_store[key][predicate]['all'].append(objct)

            objct_tuple = objct.split('@')
            string = objct_tuple[0].strip()#.replace('\\u', 'u')
            language_tag = objct_tuple[1].strip()
            if language_tag not in json_store[key][predicate].keys():
                json_store[key][predicate][language_tag] = ''
            json_store[key][predicate][language_tag] = string          
        else:
            if '#notation' in triple[1]:
                objct = ' '.join(triple[2:]).replace(' .', '').replace('"', '').strip()
                json_store[key][predicate] = objct
            else:
                if predicate not in json_store[key].keys():
                    json_store[key][predicate] = []
                objct = ' '.join(triple[2:]).replace(' .', '').replace('"', '').strip()
                json_store[key][predicate].append(objct)
    # <http://purl.org/dc/elements/1.1/subject> "Brutus (Lucius Junius)"@fi .
    if 'dc/elements/1.1/subject' in triple[1]:
        predicate = triple[1].strip().split('/')[-1].replace('>', '').strip()
        if predicate not in json_store[key].keys():
            json_store[key][predicate] = { 'all': [] }
        objct = ' '.join(triple[2:]).replace(' .', '').replace('"', '').strip()
        if '\\u' in objct:
            objct = cleanUpUnicode(objct)
            for find in re.findall(r'\\u.{4}', objct):
                unicodechars.append(find)
                #print(string.replace(find, chr(int(find.replace('\\u', '')))))
        json_store[key][predicate]['all'].append(objct)

        objct_tuple = objct.split('@')
        string = objct_tuple[0].strip()#.replace('\\u', 'u')
        language_tag = objct_tuple[1].strip()
        if language_tag not in json_store[key][predicate].keys():
            json_store[key][predicate][language_tag] = []
        json_store[key][predicate][language_tag].append(string)


        
print(set(unicodechars))
pp.pprint(json_store[list(json_store.keys())[20]])

with open('iconclass_single_object.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(json_store, indent=4, ensure_ascii=False))

json_lst = []
for k in json_store.keys():
    json_lst.append({ 
        'uri': k,
        'id': json_store[k]['notation'],
        'iconclass': json_store[k]
    })

with open('iconclass_list_of_objects.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(json_lst, indent=4, ensure_ascii=False))

