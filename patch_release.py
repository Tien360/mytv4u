import io

with io.open('tools/release.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace:
# await stdout.addStream(buildProcess.stdout);
# await stderr.addStream(buildProcess.stderr);
# With:
# buildProcess.stdout.pipe(stdout);
# buildProcess.stderr.pipe(stderr);

content = content.replace('await stdout.addStream(buildProcess.stdout);\n    await stderr.addStream(buildProcess.stderr);', 
                          'buildProcess.stdout.pipe(stdout);\n    buildProcess.stderr.pipe(stderr);')

with io.open('tools/release.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched tools/release.dart')
