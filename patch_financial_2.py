import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to find where _buildFinancialBox starts and ends.
# It starts with "Widget _buildFinancialBox(int budget, int revenue) {" and ends before "Widget _buildBadge(String text, Color color) {"
pattern = re.compile(r"Widget _buildFinancialBox\(int budget, int revenue\) \{.*?(?=Widget _buildBadge\(String text, Color color\) \{)", re.DOTALL)

new_box = """Widget _buildFinancialBox(int budget, int revenue) {
    final bool profitable = revenue > budget;
    final String budgetStr = '\\$${(budget / 1000000).toStringAsFixed(1)}M';
    final String revenueStr = '\\$${(revenue / 1000000).toStringAsFixed(1)}M';
    
    final double ratio = budget > 0 ? revenue / budget : 0;
    final String ratioStr = 'x${ratio.toStringAsFixed(1)}';

    return GestureDetector(
      onTap: () {
        setState(() {
          _isFinancialExpanded = !_isFinancialExpanded;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeOutQuart,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: _isFinancialExpanded ? Colors.white.withOpacity(0.08) : Colors.white.withOpacity(0.03),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: profitable 
                ? Colors.greenAccent.withOpacity(_isFinancialExpanded ? 0.5 : 0.2)
                : Colors.redAccent.withOpacity(_isFinancialExpanded ? 0.5 : 0.2),
          ),
          boxShadow: _isFinancialExpanded && profitable ? [
            BoxShadow(color: Colors.greenAccent.withOpacity(0.1), blurRadius: 10, spreadRadius: 1)
          ] : [],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.monetization_on_outlined, color: profitable ? Colors.greenAccent : Colors.redAccent, size: 20),
                const SizedBox(width: 8),
                const Text(
                  'Hiệu quả Thương mại',
                  style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color: profitable ? Colors.greenAccent.withOpacity(0.2) : Colors.redAccent.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    profitable ? 'Lãi $ratioStr' : 'Lỗ',
                    style: TextStyle(
                      color: profitable ? Colors.greenAccent : Colors.redAccent,
                      fontSize: 12,
                      fontWeight: FontWeight.bold
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                AnimatedRotation(
                  turns: _isFinancialExpanded ? 0.5 : 0,
                  duration: const Duration(milliseconds: 300),
                  child: const Icon(Icons.keyboard_arrow_down, color: Colors.white54, size: 20),
                ),
              ],
            ),
            AnimatedCrossFade(
              firstChild: const SizedBox(height: 0, width: double.infinity),
              secondChild: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Kinh phí', style: TextStyle(color: Colors.white70, fontSize: 13)),
                      Text(budgetStr, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  const SizedBox(height: 6),
                  LayoutBuilder(
                    builder: (context, constraints) {
                      final double maxVal = (budget > revenue ? budget : revenue).toDouble();
                      final double budgetWidth = maxVal > 0 ? (budget / maxVal) * constraints.maxWidth : 0;
                      return Row(
                        children: [
                          AnimatedContainer(
                            duration: const Duration(milliseconds: 800),
                            curve: Curves.easeOutQuart,
                            height: 4,
                            width: budgetWidth,
                            decoration: BoxDecoration(
                              color: Colors.white30,
                              borderRadius: BorderRadius.circular(2),
                            ),
                          ),
                        ],
                      );
                    },
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Doanh thu', style: TextStyle(color: Colors.white70, fontSize: 13)),
                      Text(revenueStr, style: const TextStyle(color: Colors.greenAccent, fontSize: 13, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  const SizedBox(height: 6),
                  LayoutBuilder(
                    builder: (context, constraints) {
                      final double maxVal = (budget > revenue ? budget : revenue).toDouble();
                      final double revenueWidth = maxVal > 0 ? (revenue / maxVal) * constraints.maxWidth : 0;
                      return Row(
                        children: [
                          AnimatedContainer(
                            duration: const Duration(milliseconds: 800),
                            curve: Curves.easeOutQuart,
                            height: 4,
                            width: revenueWidth,
                            decoration: BoxDecoration(
                              color: profitable ? Colors.greenAccent : Colors.redAccent,
                              borderRadius: BorderRadius.circular(2),
                            ),
                          ),
                        ],
                      );
                    },
                  ),
                ],
              ),
              crossFadeState: _isFinancialExpanded ? CrossFadeState.showSecond : CrossFadeState.showFirst,
              duration: const Duration(milliseconds: 300),
            ),
          ],
        ),
      ),
    );
  }

  """

content = pattern.sub(new_box, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated financial box to be compact and expandable!")
