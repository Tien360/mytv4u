import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

financial_box_code = """
  Widget _buildFinancialBox(int budget, int revenue) {
    final bool profitable = revenue > budget;
    final String budgetStr = '\\$${(budget / 1000000).toStringAsFixed(1)} Triệu';
    final String revenueStr = '\\$${(revenue / 1000000).toStringAsFixed(1)} Triệu';
    
    final double ratio = budget > 0 ? revenue / budget : 0;
    final String ratioStr = 'x${ratio.toStringAsFixed(1)}';

    return GlassContainer(
      padding: const EdgeInsets.all(16),
      borderRadius: 12,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.monetization_on_outlined, color: Colors.greenAccent, size: 20),
              const SizedBox(width: 8),
              const Text(
                'Hiệu quả Thương mại',
                style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
              ),
              const Spacer(),
              if (profitable)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.greenAccent.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.greenAccent.withOpacity(0.5)),
                  ),
                  child: Text(
                    'Lãi $ratioStr',
                    style: const TextStyle(color: Colors.greenAccent, fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                )
              else 
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.redAccent.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.redAccent.withOpacity(0.5)),
                  ),
                  child: const Text(
                    'Lỗ',
                    style: TextStyle(color: Colors.redAccent, fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                )
            ],
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Kinh phí', style: TextStyle(color: Colors.white70, fontSize: 14)),
              Text(budgetStr, style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold)),
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
                    height: 6,
                    width: budgetWidth,
                    decoration: BoxDecoration(
                      color: Colors.white30,
                      borderRadius: BorderRadius.circular(3),
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
              const Text('Doanh thu', style: TextStyle(color: Colors.white70, fontSize: 14)),
              Text(revenueStr, style: const TextStyle(color: Colors.greenAccent, fontSize: 14, fontWeight: FontWeight.bold)),
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
                    height: 6,
                    width: revenueWidth,
                    decoration: BoxDecoration(
                      color: profitable ? Colors.greenAccent : Colors.redAccent,
                      borderRadius: BorderRadius.circular(3),
                      boxShadow: [
                        BoxShadow(
                          color: profitable ? Colors.greenAccent.withOpacity(0.4) : Colors.redAccent.withOpacity(0.4),
                          blurRadius: 8,
                        )
                      ]
                    ),
                  ),
                ],
              );
            },
          ),
        ],
      ),
    );
  }
"""

if "Widget _buildFinancialBox(int budget, int revenue)" not in content:
    content = content.replace("Widget _buildBadge(String text, Color color) {", financial_box_code + "\n  Widget _buildBadge(String text, Color color) {")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed _buildFinancialBox insertion!")
else:
    print("Already inserted.")
