def clean(name):
    import re
    return re.sub(r'[^a-z0-9]', '', name.lower().replace('hd', '').replace('vinhlong', 'vl'))

print(clean('SCTV1 HD'))
print(clean('SCTV 1'))
