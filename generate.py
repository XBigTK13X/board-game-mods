import os
import sys
import yaml

page_template = '''
<html>
  <head>
    <title>Lofty Snowman's Board Game Mods</title>
    <style>
      body {
        margin: 2em 3em;
        font-size: 1.25em;
      }
      li {
        margin-top: 1em;
      }
    </style>
  </head>
  <body>
    <h1>Lofty Snowman's Board Game Mods</h1>
    ---stats---
    <p>Shown with the newest mods first.</p>
    ---entries---
  </body>
</html>
'''
entry_template = '''
    <h2>---name---</h2> ---created------updated---
    <p>---description---</p>
    <ul>
    ---forum_link---
    ---bgg_file_link---
    ---gdrive_link---
    </ul>
'''
def li_href(text, link):
    return f'''
        <li><a href="{link}">{text}</a></li>
    '''

yaml_data = None
with open("info.yaml") as yaml_fp:
    yaml_data = yaml.safe_load(yaml_fp)
entries_block = ''
stats = {}
stat_keys = []
yaml_data['mods'].reverse()
for mod in yaml_data['mods']:
    if not mod['kind'] in stats:
        stats[mod['kind']] = 0
        stat_keys.append(mod['kind'])
    stats[mod['kind']] += 1
    entry = entry_template.replace('---name---',mod['name'])
    entry = entry.replace('---description---',mod['desc'])
    entry = entry.replace('---created---',f"Created: {mod['created']}")
    entry = entry.replace('---updated---',f" / Updated: {mod['updated']}" if 'updated' in mod else '')
    entry = entry.replace('---forum_link---',li_href("BoardGameGeek Forum Thread",mod['links']['forum']) if 'forum' in mod['links'] else '')
    entry = entry.replace('---bgg_file_link---',li_href("BoardGameGeek File Page",mod['links']['file'] if 'file' in mod['links'] else ''))
    entry = entry.replace('---gdrive_link---',li_href("Google Drive File Page",mod['links']['drive'] if 'drive' in mod['links'] else ''))
    entries_block += entry + "<br/>"
stat_keys.sort()
stat_block = ', '.join(f'{x} [{stats[x]}]' for x in stat_keys)
stat_block = f'<h3>{stat_block}</h3>'
page = page_template.replace('---stats---',stat_block)
page = page.replace('---entries---',entries_block)
with open('./docs/index.html','w') as html_fp:
    html_fp.write(page)


