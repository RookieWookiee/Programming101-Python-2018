import sys
import json


def parse_json(fname):
    with open(fname, 'r') as f:
        data = json.load(f)
    return data


def extract_people(d):
    data = d.get('people')
    if data is None:
        raise ValueError('Malformed: JSON data is not in the expected form')

    return [x for x in data]


def extract_languages(people_l):
    def check(thing):
        if thing is None:
            raise ValueError('Malformed JSON: data is not in the expected format')

    languages = {}
    for p in people_l:
        check(p.get('skills'))

        curr_skills = p.get('skills')
        for skill in curr_skills:
            check(skill.get('name'))
            check(p.get('first_name'))
            check(p.get('last_name'))
            check(p.get('last_name'))

            curr_lang = skill.get('name')
            if curr_lang not in languages:
                languages[curr_lang] = []

            person_info = (f"{p['first_name']} {p['last_name']}", skill['level'])
            languages[curr_lang].append(person_info)

    return languages

def get_best_people(languages):
    def max_by(p): return p[1]

    return {x: max(languages[x], key=max_by)[0]  for x in languages.keys()}


if __name__ == '__main__':
    data = parse_json(sys.argv[1])
    people = extract_people(data)
    languages = extract_languages(people)
    best_by_language = get_best_people(languages)

    [print(lang, '-', best) for lang, best in best_by_language.items()]

