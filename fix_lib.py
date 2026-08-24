with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("""        ],
      ),
    );
  }""", """        ],
      ),
    ),
    );
  }""")

with open("lib/screens/library_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed library_screen.dart")
