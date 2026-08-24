with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "if (_tmdbDetails != null) ...[" in line and "status" not in line:
        # Check if the next lines contain `_tmdbDetails!['status']`
        if i+1 < len(lines) and "_tmdbDetails!['status']" in lines[i+1]:
            start_idx = i
            break

if start_idx != -1:
    # Find the closing `],` for this block
    # It ends after the budget/revenue block
    for j in range(start_idx, start_idx+100):
        if "]," in lines[j] and j+1 < len(lines) and "]," in lines[j+1] and "]" in lines[j+2]:
             # Wait, how many closing brackets?
             # Let's just look for the first `],` after budget.
             pass
    
    # Better yet, let's find the budget block end
    budget_idx = -1
    for j in range(start_idx, start_idx+100):
        if "if (_tmdbDetails!['budget'] != null &&" in lines[j]:
            budget_idx = j
            break
            
    if budget_idx != -1:
        for j in range(budget_idx, budget_idx+20):
            if "]," in lines[j]:
                # The line after `],` is another `],` for the `if (_tmdbDetails != null) ...[` block?
                if "]," in lines[j+1]:
                    end_idx = j+1
                else:
                    # sometimes it might have spaces or newlines
                    for k in range(j+1, j+5):
                        if "]," in lines[k]:
                            end_idx = k
                            break
                break

if start_idx != -1 and end_idx != -1:
    block = lines[start_idx:end_idx+1]
    lines = lines[:start_idx] + lines[end_idx+1:]
    
    dir_start = -1
    insert_idx = -1
    for i, line in enumerate(lines):
        if "if (_directorsTmdb.isNotEmpty) ...[" in line:
            dir_start = i
        if dir_start != -1 and i > dir_start and "]," in line:
            insert_idx = i + 1
            break
            
    if insert_idx != -1:
        lines = lines[:insert_idx] + ["\n                                              const SizedBox(height: 32),\n"] + block + lines[insert_idx:]
        with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("Successfully moved TMDB details to right column!")
    else:
        print("Could not find insert index!")
else:
    print(f"Could not find block! start={start_idx}, end={end_idx}")
