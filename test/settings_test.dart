import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/screens/settings_screen.dart';
import '../lib/utils/l10n.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  testWidgets('SettingsScreen rendering test', (WidgetTester tester) async {
    SharedPreferences.setMockInitialValues({});
    await L10n.load('vi');
    
    await tester.pumpWidget(
      const MaterialApp(
        home: SettingsScreen(),
      ),
    );
    
    await tester.pumpAndSettle();
    
    expect(find.byType(SettingsScreen), findsOneWidget);
  });
}
