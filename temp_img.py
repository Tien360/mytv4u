import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("https://play-lh.googleusercontent.com/F_Nn433hK8qA29uB849T693Ff3WJt7XWc2tXyP2U8aX-o2R2tA-E03xU9mQv7P5tZzY=w512-h512", "https://play-lh.googleusercontent.com/D4s3L2P-uA6l2Qh6bTz7H2lXq7S1j-K3J_Y5_8T-M0D0sM-s1QZ0Y-7L0X0B_6F2W2U=w512-h512")

with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced image URL to Stealth Master")
