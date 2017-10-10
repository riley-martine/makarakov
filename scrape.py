from bs4 import BeautifulSoup
import re
import os
import pickle
import markovify


if not os.path.exists("lines.pickle"):
    with open('archive.html', 'r') as f:
        soup = BeautifulSoup(f, 'lxml')
    
    logs = soup.find_all("div", class_="log")
    # we gotta get colors too :( 
    logtypes = ["pesterlog", "spritelog", "dialoglog", "sriousbiz"]
    logfilter = lambda log: (log.button and log.button.string in logtypes) or not log.button
    logs_filtered = filter(logfilter, logs)
    
    logs_sections = [div.section for div in logs_filtered]
    
    sections_str = map(str, logs_sections)
    sections_br = [re.split("<br>|<br/>", section) for section in sections_str]
    sections_bs = [map(lambda span_s:BeautifulSoup(span_s, 'lxml'), span_s)  for span_s in sections_br]
    
    def get_span(html):
        body = html.body
        try:
            if body.span:
                while body.span.span:
                    body.span.span.unwrap()
                style = body.span["style"]
                index = style.index('color: ')
                color = style[index + 7:index+7+7+1]
                return str(color) + ':' +  str(body.span.string).replace("\xa0", ' ')
        except AttributeError:
            return ""
        except KeyError:
            return ''
        except ValueError:
            # Mostly inline transcripts
            return ''
    
    sections_spans = [map(get_span, bs) for bs in sections_bs]
    def merge(span_s):
        out = []
        for span in span_s:
            out += span
        return out
    
    sections_merged = merge(sections_spans)
   
    name_map = {
  	"Equius": ["#000056 CT", "#000056 EQUIUS"],
  	"Horuss": ["#000056 HORUSS"],
  	"Vriska": ["#005682 (VRISKA)", "#005682 VRISKA", "#005682 AG"],
  	"Aranea": ["#005682 ARANEA"],
  	"Kanaya": ["#008141 GA", "#008141 KANAYA"],
  	"Porrim": ["#008141 PORRIM"],
  	"Latula": ["#008282 LATULA"],
  	"Terezi": ["#008282 GC", "#008282 TEREZI"],
  	"Jane"  : ["#00d5f2 GG", "#00d5f2 JANE"],
  	"Nannasprite": ["#00d5f2 NANNASPRITE"],
  	"John"  : ["#0715cd EB", "#0715cd GT", "#0715cd JOHN"],
  	"Tavrosprite": ["#0715cd TAVROSPRITE"],
  	"Jadesprite": ["#1f9400 JADESPRITE"],
  	"Jake"  : ["#1f9400 GT", "#1f9400 JAKE"],
  	"Gamzee": ["#2b0057 TC", "#4200b0 TC"],
  	"Caliborn": ["#2ed73a uu", "#323232 uu"],
  	"Nepeta": ["#416600 AC"],
  	"Davepetasprite^2": ["#4ac925 DAVEPETASPRITE^2"],
  	"Nepetasprite": ["#4ac925 NEPETASPRITE"],
  	"Jade"  : ["#4ac925 ?GG", "#4ac925 GG", "#4ac925 JADE"],
  	"Karkat": ["#626262 ?CG", "#626262 CCG", "#626262 CG", "#626262 FCG", "#626262 KARKAT", "#626262 PCG", "#ff0000 CCG"],
  	"Eridan": ["#6a006a CA"],
  	"Cronus": ["#6a006a CRONUS"],
  	"Feferi": ["#77003c CC"],
  	"Meenah": ["#77003c MEENAH"],
  	"Calliope": ["#ff0000 CALLIOPE", "#929292 CALLIOPE", "#929292 UU"],
  	"Aradia": ["#a10000 AA", "#a10000 ARADIA"],
  	"Rufioh": ["#a15000 RUFIOH"],
  	"Tavros": ["#a15000 AT", "#a15000 TAVROS"],
  	"Sollux": ["#a1a100 SOLLUX", "#a1a100 TA"],
  	"Rose": ["#b536da ROSE", "#b536da TT"],
  	"Dave": ["#e00707 DAVE", "#e00707 TG", "#f2a400 TG"],
  	"Lil Hal": ["#e00707 TT"],
  	"Jaspersprite": ["#f141ef JASPERSPRITE"],
  	"Jasprosesprite^2": ["#f141ef JASPROSESPRITE^2"],
  	"Davesprite": ["#f2a400 DAVESPRITE"],
  	"Dirk": ["#f2a400 DIRK", "#f2a400 TT"],
  	"Kankri": ["#ff0000 KANKRI"],
  	"Roxy": ["#ff6ff2 ROXY", "#ff6ff2 TG"]
    }

    #exp = re.compile('\[..+\]')
    #logs_messages = filter(lambda x: not exp.search(x), logs_str)
    sections_splittable = filter(lambda x: x, sections_merged)
    logs_split = [log.split(':') for log in sections_splittable if len(log.split(':')) > 2]
    logs_joined = [[' '.join(log[0:2]), ''.join(log[2:]).strip()] for log in logs_split] # Deal with things like :3
   
    def get_name(s):
        for key in name_map.keys():
            if s[0] in name_map[key]:
                return [key, s[1]]
                
        return ''

    logs_names = map(get_name, logs_joined)
    #anything that starts with a space or star
    exp = re.compile("^([ |*])")
    logs_people = [log for log in logs_names if not (log == '' or exp.search(log[0]))]
    
    lines = {}
    for message in logs_people:
        if message[0] not in lines and message[1] != []:
            lines[message[0]] = []
        lines[message[0]].append(message[1])
    
    
    lines_small = { k:v for k,v in lines.items() if len(v) > 1000 }
    # Don't bother with characters we have < 1000 lines of dialog for
    # This supports going as low as 100

    with open("lines.pickle", 'wb') as f:
        pickle.dump(lines_small, f)
else:
    with open("lines.pickle", 'rb') as f:
        lines_small = pickle.load(f)

###############MARKOVING BELOW#############
class ListText(markovify.Text):
    def sentence_split(self, text):
        return text


if not os.path.isdir('models'):
    os.mkdir('models')
    os.chdir('models')

    models = {k: ListText(v, state_size=2) for k, v in lines_small.items()}
    # Change state size to 2 or 3 depending on what u r looking for
    models_json = {k: v.to_json() for k,v in models.items()}

    for k,v in models_json.items():
        with open(k + '.json', 'w') as f:
            f.write(v)
else:
    models = {}
    os.chdir('models')
    for filename in os.listdir():
        with open(filename, 'r') as f:
            contents = f.read()
            models[filename.split('.')[0]] = ListText.from_json(contents)

############USER INTERFACE BELOW################
key = ''
while key != "STOP":
    print('##########################################')
    print(list(models.keys()))
    print('##########################################')
    key = input("Select person to imitate from above list: ")
    print('##########################################')
    #TODO state size, some prettier printing, # of lines select
    try:
        for i in range(10):
            print(models[key].make_sentence(tries=100))
    except KeyError:
        print("Error: {} not in above list".format(key))
