import sys
import lib


def tips():
    print('param: file path (.json or .lua)')
    exit(-1)

if len(sys.argv) == 1:
    tips()

path = sys.argv[1]

is_lua = path[-4:] == '.lua'
is_json = path[-5:] == '.json'

if not is_lua and not is_json:
    tips()

f = open(path, 'r')
content = f.read()
f.close()

if is_json:
    content = lib.json_to_lua(content)
    path = path.replace(".json", ".lua")
else:
    content = lib.lua_to_json(content)
    path = path.replace(".lua", ".json")

f = open(path, 'w')
f.write(content)
f.close()

print("The converted file has been saved to " + path)
