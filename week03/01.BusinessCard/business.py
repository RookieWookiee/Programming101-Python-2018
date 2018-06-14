import json
import sys

def check(thing):
    if thing is None:
        raise ValueError('JSON is not in the expected format')


def gen_head(person_d):
    first_name = person_d.get('first_name')
    last_name = person_d.get('last_name')
    check(first_name)
    check(last_name)

    return ['<head>',
            f'<title>{first_name} {last_name}</title>',
            '<link rel="stylesheet" type="text/css" href="styles.css">',
            '</head>']


def gen_base_info(person_d):
    check(person_d.get('age'))
    check(person_d.get('birth_date'))
    check(person_d.get('birth_place'))

    return ['<div class="base-info">',
            f"<p>Age: {person_d.get('age')}</p>",
            f"<p>Birth date: {person_d.get('birth_date')}</p>",
            f"<p>Birth place: {person_d.get('birth_place')}</p>",
            f"<p>Gender: {person_d.get('gender')}</p>",
            '</div>']


def gen_interests(person_d):
    check(person_d.get('interests'))

    interests = ['<div class="interests">', '<h2>Interests:</h2>', '<ul>']
    interests.extend(f'<li>{x}</li>' for x in person_d['interests'])
    interests.extend(['</ul>', '</div>'])
    return interests


def gen_skills(person_d):
    check(person_d.get('skills'))

    skills = ['<div class="skills">', '<h2>Skills:</h2>', '<ul>']

    for entry in person_d['skills']:
        check(entry.get('name'))
        check(entry.get('level'))
        skills.append(f"<li>{entry['name']} - {entry['level']}</li>")

    skills.extend(['</ul>', '</div>'])


    return skills


def gen_body(person_d):
    check(person_d.get('gender'))
    check(person_d.get('first_name'))

    body = []
    gender = person_d['gender']
    body.extend(['<body>', f'<div class="business-card {gender}">'])

    full_name = f"{person_d['first_name']} {person_d['last_name']}"
    body.append(f'<h1 class="full-name">{full_name}</h1>')

    avatar_path = f'avatars/{person_d["first_name"].lower()}.png'
    body.append(f'<img class="avatar" src="{avatar_path}">')

    body.extend(gen_base_info(person_d))


    body.extend(gen_interests(person_d))
    body.extend(gen_skills(person_d))

    body.extend(['</div>', '</body>'])

    return body


def gen_html(person_d):
    html = ['<!DOCTYPE html>', '<html>']
    html.extend(gen_head(person_d))
    html.extend(gen_body(person_d))
    html.append('</html>')

    return html


def main(fname):
    with open(fname, 'r') as f:
        data = json.load(f)

    people = data.get('people')
    check(people)

    for p in people:
        gen_html(p)

    ivo = gen_html(data['people'][0])

    with open('result_ivo.html', 'w') as f:
        f.write('\n'.join(ivo))


if __name__ == '__main__':
    main(sys.argv[1])
