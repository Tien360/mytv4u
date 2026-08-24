with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract the block to move
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "if (_tmdbDetails!['status'] != null &&" in line:
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if "_buildRichText('Doanh thu: '" in lines[i] or "_buildRichText('Revenue: '" in lines[i]:
            # The next line is `const SizedBox(height: 8),` or `],`
            for j in range(i, i+5):
                if "]," in lines[j]:
                    end_idx = j
                    break
            break

if start_idx != -1 and end_idx != -1:
    block = lines[start_idx:end_idx+1]
    # Remove from middle column
    lines = lines[:start_idx] + lines[end_idx+1:]
    
    # Find where to insert in right column (under Directors)
    # The right column has:
    # if (_directorsTmdb.isNotEmpty) ...[
    #    ...
    #    Wrap( ... )
    # ],
    
    insert_idx = -1
    dir_start = -1
    for i, line in enumerate(lines):
        if "if (_directorsTmdb.isNotEmpty) ...[" in line:
            dir_start = i
        if dir_start != -1 and i > dir_start and "]," in line:
            insert_idx = i + 1
            break
            
    if insert_idx != -1:
        # Insert the block
        # Wait, the block uses `if (...) ...[` so it can just be placed at insert_idx.
        # Let's add a top margin before the block
        lines = lines[:insert_idx] + ["\n                                              const SizedBox(height: 32),\n"] + block + lines[insert_idx:]
        
        with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("Successfully moved info to right column!")
    else:
        print("Could not find insert index!")
else:
    print("Could not find start/end index of block to move!")
