import json


def json_to_lua(content):
    content = json.dumps(json.loads(content), indent=4)
    lst = list(content)
    length = len(content)
    front_pos = -1

    for i in range(0, length):
        char = lst[i]
        if char == '[':
            lst[i] = '{'
        elif char == ']':
            lst[i] = '}'
        elif char == '"' and i < length - 1 and lst[i + 1] != ':':
            front_pos = i
        elif char == ':' and i >= 2 and lst[i - 1] == '"' and lst[i - 2] != ':' and front_pos > -1:
            lst[front_pos] = ''
            lst[i - 1] = ''
            lst[i] = " ="
            front_pos = -1

    return "return " + ''.join(lst)


def _parse(lst: list, pos: int, is_array: bool):
    while pos < len(lst):
        if lst[pos] == '{':
            v = lst[pos + 1] != '"'
            lst[pos] = '[' if v else '{'

            if pos == 0:
                is_array = v
            else:
                ret = _parse(lst, pos + 1, v)
                pos = ret
        elif lst[pos] == '}':
            if is_array:
                lst[pos] = ']'

            return pos

        pos += 1


def lua_to_json(content: str):
    content = content[7:]
    content = content.replace(' ', '')
    content = content.replace('\n', '')
    content = content.replace('=', '":')
    pos = -1

    while True:
        pos = content.find('":', pos + 1)

        if pos != -1:
            a = content.rfind('{', 0, pos)
            b = content.rfind(',', 0, pos)
            v = a if a > b else b
            v += 1
            content = content[:v] + '"' + content[v:]
            pos += 1
        else:
            break

    lst = list(content)
    _parse(lst, 0, 0)
    content = ''.join(lst)
    content = json.dumps(json.loads(content), indent=4)

    return content
