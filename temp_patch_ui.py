content = open('lib/widgets/optimizer_dialog.dart', 'r', encoding='utf-8').read()

old_cb = """                CheckboxListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(L10n.t('opt_apply_all') ?? 'Bật TOÀN BỘ hiệu ứng rực rỡ nhất', style: const TextStyle(color: Colors.white)),"""

new_cb = """                CheckboxListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(L10n.t('opt_apply_audio') ?? 'Tắt hiệu ứng Trình phát Nhạc (Tiết kiệm pin)', style: const TextStyle(color: Colors.white)),
                  subtitle: Text(L10n.t('opt_apply_audio_sub') ?? 'Tắt Sóng âm và Đĩa than xoay giúp giảm tải CPU/GPU, kéo dài thời lượng sử dụng pin.', style: const TextStyle(color: Colors.white54, fontSize: 13)),
                  value: _recDisableAudioEffects,
                  activeColor: Colors.blueAccent,
                  onChanged: (v) => setState(() {
                    _recDisableAudioEffects = v!;
                    if (v) _recAllEffects = false;
                  }),
                ),
                CheckboxListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(L10n.t('opt_apply_all') ?? 'Bật TOÀN BỘ hiệu ứng rực rỡ nhất', style: const TextStyle(color: Colors.white)),"""

content = content.replace(old_cb, new_cb)
open('lib/widgets/optimizer_dialog.dart', 'w', encoding='utf-8').write(content)
