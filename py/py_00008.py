# Comment: Expand shell variables of form $var and ${var}.  Unknown variables
are left unchanged.
def expandvars(source, environ=None):
    
    if source is None:
        return source
    if environ is None:
        environ=os.environ
        #os.path.expandvars(path)
    global _varprog, _varprogb
    if isinstance(source, bytes):
        if b'$' not in source:
            return source
        if not _varprogb:
            import re
            #_varprogb = re.compile(br'\$(\w+|\{[^}]*\})', re.ASCII)
            _varprogb = re.compile(br'\$(\w+|\{[^}]*\})')
        search = _varprogb.search
        start = b'{'
        end = b'}'
    elif isinstance(source, str):
        if '$' not in source:
            return source
        if not _varprog:
            import re
            #_varprog = re.compile(r'\$(\w+|\{[^}]*\})', re.ASCII)
            _varprog = re.compile(r'\$(\w+|\{[^}]*\})')
        search = _varprog.search
        start = '{'
        end = '}'
    else:
        return source
    i = 0
    while True:
        m = search(source, i)
        if not m:
            break
        i, j = m.span(0)
        name = m.group(1)
        if name.startswith(start) and name.endswith(end):
            name = name[1:-1]
        if isinstance(name, bytes):
            name = str(name)
        if name in environ.keys():
            tail = source[j:]
            value = str(environ[name])
            try:
                parts=value.split('\\')
            except Exception as e:
                print(name, value, ':', repr(e))
                raise
            value=os.path.join(*parts)
            if isinstance(source, bytes):
                value = value.encode('ASCII')
            source = source[:i] + value
            i = len(source)
            source += tail
        else:
            i = j
    #return os.path.normpath(source)    
    return source



# Comment: Expand shell variables of form $var and ${var}.  Unknown variables
are left unchanged.
def pathhasvars(source):
    
    global _varprog, _varprogb
    if isinstance(source, bytes):
        if b'$' not in source:
            return False
        if not _varprogb:
            import re
            #_varprogb = re.compile(br'\$(\w+|\{[^}]*\})', re.ASCII)
            _varprogb = re.compile(br'\$(\w+|\{[^}]*\})')
        search = _varprogb.search
        start = b'{'
        end = b'}'
    else:
        if '$' not in source:
            return False
        if not _varprog:
            import re
            #_varprog = re.compile(r'\$(\w+|\{[^}]*\})', re.ASCII)
            _varprog = re.compile(r'\$(\w+|\{[^}]*\})')
        search = _varprog.search
        start = '{'
        end = '}'
    i = 0
    m = search(source, i)
    return not (not m)  


