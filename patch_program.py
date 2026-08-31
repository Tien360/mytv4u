import re

path = r"T:\Project\Phim\tv_web_player\Program.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_args = """if (args.Length >= 1) url = args[0];
            if (args.Length >= 2) title = args[1];
            if (args.Length >= 6)
            {
                int.TryParse(args[2], out x);
                int.TryParse(args[3], out y);
                int.TryParse(args[4], out width);
                int.TryParse(args[5], out height);
            }
            if (args.Length >= 7) subtitlePath = args[6];"""

new_args = """Func<string, string> DecodeArg = (arg) => {
                if (arg.StartsWith("b64:")) {
                    try { return System.Text.Encoding.UTF8.GetString(Convert.FromBase64String(arg.Substring(4))); } catch { return arg; }
                }
                return arg;
            };

            if (args.Length >= 1) url = DecodeArg(args[0]);
            if (args.Length >= 2) title = DecodeArg(args[1]);
            if (args.Length >= 6)
            {
                int.TryParse(args[2], out x);
                int.TryParse(args[3], out y);
                int.TryParse(args[4], out width);
                int.TryParse(args[5], out height);
            }
            if (args.Length >= 7) subtitlePath = DecodeArg(args[6]);"""

content = content.replace(old_args, new_args)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done patching Program.cs")
