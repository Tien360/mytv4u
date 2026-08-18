import os
import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the closing brackets of build method
old_ending = '''
                          const SizedBox(height: 64), // Extra bottom padding
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      const Positioned(
        top: 0, left: 0, right: 0,
        child: CustomTitleBar(),
      ),
    ],
  ),
);
}
'''

new_ending = '''
                          const SizedBox(height: 64), // Extra bottom padding
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
'''
# Actually wait, let's just trace the exact brackets we need!
# 1. Scaffold(
# 2.   body: Stack(
# 3.     children: [
# 4.       SafeArea(
# 5.         child: Row(
# 6.           children: [
# 7.             Expanded(
# 8.               child: Column(
# 9.                 children: [
# 10.                  Expanded(
# 11.                    child: SingleChildScrollView(
# 12.                      child: Center(
# 13.                        child: ConstrainedBox(
# 14.                          child: Column(
# 15.                            children: [ ... 
#                                  const SizedBox(height: 64),
#                                ], // closes 15
#                              ), // closes 14
#                            ), // closes 13
#                          ), // closes 12
#                        ), // closes 11
#                      ), // closes 10
#                    ], // closes 9
#                  ), // closes 8
#                ), // closes 7
#              ], // closes 6
#            ), // closes 5
#          ), // closes 4
#          const Positioned( ... CustomTitleBar() ... ),
#        ], // closes 3
#      ), // closes 2
#    ); // closes 1
#  }

correct_ending = '''
                          const SizedBox(height: 64), // Extra bottom padding
                        ], // closes Column
                      ), // closes ConstrainedBox
                    ), // closes Center
                  ), // closes SingleChildScrollView
                ), // closes Expanded
              ], // closes Column
            ), // closes Column
          ), // closes Expanded
        ], // closes Row
      ), // closes Row
    ), // closes SafeArea
    const Positioned(
      top: 0, left: 0, right: 0,
      child: CustomTitleBar(),
    ),
  ],
),
);
}
'''
# I need to use regex to replace everything from const SizedBox(height: 64), // Extra bottom padding to CustomTitleBar(),\n      ),\n    ],\n  ),\n);\n}

text = re.sub(
    r'const SizedBox\(height: 64\), // Extra bottom padding[\s\S]*?child: CustomTitleBar\(\),\n      \),\n    \],\n  \),\n\);\n}',
    '''const SizedBox(height: 64), // Extra bottom padding
                                ], // 15
                              ), // 14
                            ), // 13
                          ), // 12
                        ), // 11
                      ), // 10
                    ], // 9
                  ), // 8
                ), // 7
              ], // 6
            ), // 5
          ), // 4
          const Positioned(
            top: 0, left: 0, right: 0,
            child: CustomTitleBar(),
          ),
        ], // 3
      ), // 2
    ); // 1
  }''',
    text
)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

