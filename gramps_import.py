import os
import json 
import datetime
import hashlib
from dateutil.relativedelta import relativedelta
from pathlib import Path
from PIL import Image

filename_in = "Untitled_1.json"
filename_out = "data.js"

base_media = ""
thumb_media = ""

BIRTH = "Geburt"
DEATH = "Tod"
BIRTHNAME = "Geburtsname"
JOB = "Beruf"

EVENT_NONE = 0
EVENT_BIRTH = 1
EVENT_DEATH = 2

events = {}
persons = {}
families = {}
places = {}
medias = {}

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def convert_json(config, **kwargs):
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    if 'gramps_import' in config:
        if 'filename_in' in config['gramps_import']:
            filename_in = config['gramps_import']['filename_in']
        if 'filename_out' in config['gramps_import']:
            filename_out = config['gramps_import']['filename_out']
        if 'base_media' in config['gramps_import']:
            base_media = config['gramps_import']['base_media']
        if 'thumb_media' in config['gramps_import']:
            thumb_media = config['gramps_import']['thumb_media']
            Path(cur_dir + '/' + thumb_media).mkdir(parents=True, exist_ok=True)
            thumb_dir, thumb_subdir = (thumb_media.split('/', 1) + [None])[:2]
        if 'string_birth' in config['gramps_import']:
            BIRTH = config['gramps_import']['string_birth']
        if 'string_death' in config['gramps_import']:
            DEATH = config['gramps_import']['string_death']
        if 'string_birthname' in config['gramps_import']:
            BIRTHNAME = config['gramps_import']['string_birthname']
        if 'string_job' in config['gramps_import']:
            JOB = config['gramps_import']['string_job']
        if 'start' in config['gramps_import']:
            START = config['gramps_import']['start']
        else:
            START = 'I0000'
        if 'openup' in config['gramps_import']:
            OPENUP = config['gramps_import']['openup']
        else:
            OPENUP = None
    else:
        logger.error('please configure gramps_import fist!')
        os._exit(1)

    with open(filename_in) as file:
        for line in file:
            jl = json.loads(line)
            handle = jl['handle']
            if jl['_class'] == 'Event':
                events[handle] = {}
                events[handle]['place'] = jl['place']

                if 'date' in jl and jl['date']:
                    if jl['date']['dateval'][2] > 0:
                        events[handle]['year'] = jl['date']['dateval'][2]
                        if jl['date']['dateval'][1] > 0 and jl['date']['dateval'][0] > 0:
                            events[handle]['date'] =  datetime.datetime(jl['date']['dateval'][2], jl['date']['dateval'][1], jl['date']['dateval'][0])
                        else:
                            events[handle]['date'] =  datetime.datetime(jl['date']['dateval'][2], 1, 1)

                if BIRTH == jl['type']['string']:
                    events[handle]['type'] = EVENT_BIRTH
                elif DEATH == jl['type']['string']:
                    events[handle]['type'] = EVENT_DEATH
                else:
                    events[handle]['type'] = EVENT_NONE
            elif jl['_class'] == 'Person':
                persons[handle] = {}
                persons[handle]['id'] = jl['gramps_id']
                found_birthname = BIRTHNAME == jl['primary_name']['type']['string']

                persons[handle]['surname'] = '?' #unknown surename
                for surname in jl['primary_name']['surname_list']:
                    if surname['primary']:
                        persons[handle]['surname'] = surname['surname']

                if jl['alternate_names']:
                    for name in jl['alternate_names']:
                        if BIRTHNAME == name['type']['string']:
                            found_birthname = True
                            for surname in name['surname_list']:
                                if surname['primary']:
                                    persons[handle]['birthname'] = surname['surname']

                if not found_birthname:
                    persons[handle]['birthname'] = "?"

                if 'nick' in jl['primary_name'] and jl['primary_name']['nick']:
                    persons[handle]['firstname'] = jl['primary_name']['nick']
                elif 'call' in jl['primary_name'] and jl['primary_name']['call']:
                    persons[handle]['firstname'] = jl['primary_name']['call']
                else:
                    persons[handle]['firstname'] = jl['primary_name']['first_name']
                persons[handle]['givenname'] = jl['primary_name']['first_name']
                persons[handle]['title'] = jl['primary_name']['title']

                persons[handle]['events'] = []
                for event in jl['event_ref_list']:
                    persons[handle]['events'].append(event['ref'])

                persons[handle]['families'] = []
                for family in jl['parent_family_list']:
                    persons[handle]['families'].append(family)

                if jl['gender'] == 0:
                    persons[handle]['sex'] = 'f';
                elif jl['gender'] == 1:
                    persons[handle]['sex'] = 'm';
                else:
                    persons[handle]['sex'] = '?';

                if jl['media_list']:
                    if jl['media_list'][0]['_class'] == 'MediaRef':
                        persons[handle]['media_handle'] = jl['media_list'][0]['ref']

                if jl['attribute_list']:
                    for attr in jl['attribute_list']:
                        if 'string' in attr['type']:
                            if attr['type']['string'] == JOB:
                                if 'job' in persons[handle]:
                                    persons[handle]['job'] = persons[handle]['job'] + ', ' + attr['value']
                                else:
                                    persons[handle]['job'] = attr['value']

            elif jl['_class'] == 'Family':
                families[handle] = {}
                families[handle]['id'] = jl['gramps_id']

                if 'father_handle' in jl:
                    families[handle]['father'] = jl['father_handle']

                if 'mother_handle' in jl:
                    families[handle]['mother'] = jl['mother_handle']

                families[handle]['children'] = []
                for child in jl['child_ref_list']:
                    families[handle]['children'].append(child['ref'])

            elif jl['_class'] == 'Place':
                places[handle] = {}
                places[handle]['name'] = jl['name']['value']

            elif jl['_class'] == 'Media':
                medias[handle] = {}
                medias[handle]['id'] = jl['gramps_id']
                medias[handle]['filepath'] = Path(base_media + '/' + jl['path'])

    persons_out = {}
    persons_temp = {}
    for handle in persons:
        id = persons[handle]['id']
        persons_out[id] = {}
        persons_out[id]['id'] = id

        persons_temp[handle] = {}
        persons_temp[handle]['id'] = id

        persons_out[id]['name'] = persons[handle]['firstname'] + ' ' + persons[handle]['surname']
        persons_out[id]['longname'] = persons[handle]['givenname'] + ' ' + persons[handle]['surname']
        if persons[handle]['title']:
            persons_out[id]['longname'] = persons[handle]['title'] + ' ' + persons_out[id]['longname']

        if 'birthname' in persons[handle]:
            persons_out[id]['name'] = persons_out[id]['name'] + ' (' + persons[handle]['birthname'] + ')'
            persons_out[id]['birthname'] = persons[handle]['birthname']

        birthdate = None
        deathdate = None
        for handle2 in persons[handle]['events']:
            if EVENT_BIRTH == events[handle2]['type']:
                if 'date' in events[handle2]:
                    birthdate = events[handle2]['date']
                if 'year' in events[handle2]:
                    persons_out[id]['birthyear'] = events[handle2]['year']
                if events[handle2]['place']:
                    handle3 = events[handle2]['place']
                    persons_out[id]['birthplace'] = places[handle3]['name']
            elif EVENT_DEATH == events[handle2]['type']:
                if 'date' in events[handle2]:
                    deathdate = events[handle2]['date']
                if 'year' in events[handle2]:
                    persons_out[id]['deathyear'] = events[handle2]['year']
                if events[handle2]['place']:
                    handle3 = events[handle2]['place']
                    persons_out[id]['deathplace'] = places[handle3]['name']
                elif 'year' not in events[handle2]:
                    persons_out[id]['deathplace'] = '?' #make sure deathplace is set, so missing deathyear won't make someone immortal
        if birthdate and deathdate:
            persons_out[id]['age'] = relativedelta(deathdate, birthdate).years

        persons_temp[handle]['birthdate'] = birthdate
        persons_temp[handle]['deathdate'] = deathdate

        persons_out[id]['own_unions'] = []
        for handle2 in families:
            #person is the child of a family
            if handle in families[handle2]['children']:
                persons_out[id]['parent_union'] = families[handle2]['id']
                if families[handle2]['father']:
                    persons_temp[handle]['fhandle'] = families[handle2]['father']
                if families[handle2]['mother']:
                    persons_temp[handle]['mhandle'] = families[handle2]['mother']

            #person has own families
            if ((families[handle2]['father'] and handle in families[handle2]['father']) or
                (families[handle2]['mother'] and handle in families[handle2]['mother']) ):
                persons_out[id]['own_unions'].append(families[handle2]['id'])

        persons_out[id]['sex'] = persons[handle]['sex']

        if 'job' in persons[handle]:
            persons_out[id]['job'] = persons[handle]['job']

        if thumb_media and 'media_handle' in persons[handle]:
            handle2 = persons[handle]['media_handle']
            inpath = medias[handle2]['filepath']
            try:
                image = Image.open(inpath)
                image_hash = hashlib.md5(image.tobytes()).hexdigest()
                image.thumbnail((90,90))
                out_img = medias[handle2]['id'] + '_' + image_hash +'.jpg'
                if thumb_subdir:
                    out_img = thumb_subdir + '/' + out_img
                outpath = Path(cur_dir + '/' + thumb_dir + '/' + out_img)
                if not outpath.is_file():
                    image.save(outpath)
                persons_out[id]['thumb'] = out_img
            except:
                print("Couldn't create thumb from image "+str(inpath))

    unions_out = {}
    links_out = []
    for handle in families:
        id = families[handle]['id']

        unions_out[id] = {}

        unions_out[id]['id'] = id

        unions_out[id]['partner'] = []
        if families[handle]['father']:
            handle2 = families[handle]['father']
            unions_out[id]['partner'].append(persons[handle2]['id'])
            links_out.append([persons[handle2]['id'],id])
        if families[handle]['mother']:
            handle2 = families[handle]['mother']
            unions_out[id]['partner'].append(persons[handle2]['id'])
            links_out.append([persons[handle2]['id'],id])

        unions_out[id]['children'] = []
        for child in families[handle]['children']:
            handle2 = child
            unions_out[id]['children'].append(persons[handle2]['id'])
            links_out.append([id,persons[handle2]['id']])

    for handle in persons_temp:
        id = persons_temp[handle]['id']
        birthdate = persons_temp[handle]['birthdate']
        if 'fhandle' in persons_temp[handle]:
            handle2 = persons_temp[handle]['fhandle']
            if handle2 in persons_temp:
                parent_birthdate = persons_temp[handle2]['birthdate']
                if birthdate and parent_birthdate:
                    persons_out[id]['fageab'] = relativedelta(birthdate, parent_birthdate).years
        if 'mhandle' in persons_temp[handle]:
            handle2 = persons_temp[handle]['mhandle']
            if handle2 in persons_temp:
                parent_birthdate = persons_temp[handle2]['birthdate']
                if birthdate and parent_birthdate:
                    persons_out[id]['mageab'] = relativedelta(birthdate, parent_birthdate).years

    jsoncontent = {}
    jsoncontent['start'] = START
    if OPENUP:
        jsoncontent['openup'] = OPENUP
    jsoncontent['persons'] = persons_out
    jsoncontent['unions'] = unions_out
    jsoncontent['links'] = links_out
    filecontent = 'data = ' + json.dumps(jsoncontent) + ";"
    with open(Path(cur_dir + '/' + filename_out), 'w') as file:
        file.write(filecontent)
