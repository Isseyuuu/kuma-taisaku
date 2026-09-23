# Codex → Claude Code：クマサイト再設計の返却

Task ID: KUMA-REGION-2026-09-23
Status: READY_FOR_CLAUDE_REVIEW
Next owner/action: Claude Code が公開前の事実・安全表現・表示を検証し、採否と push を判断する。

## 実施内容

- 外国人旅行者を主対象とし、英語の地域選択ページ `en/where-to-hike.html` と日本語版 `articles/where-to-hike.html` を追加。北海道・本州・四国・九州を最初の分岐にし、続いて具体的な山の自治体・登山道管理者で最新情報を確認する流れにした。島ごとの分布は登山道ごとのリアルタイム出没情報ではないと明示。
- 両トップの見出し・ナビゲーション・CTAを地域選択優先に変更。長野県の当日警報を全国の代表値として置かない構成へ変更。`about.html` の目的も整合させた。
- 既存の長野県ベースの行動案内には、ツキノワグマ向けであり北海道のヒグマへの適用は未確認と明記。未確認の差異は `FACTCHECK` として残した。
- `sitemap.xml` に新ページを追加。英日 `hreflang` 相互リンクと `x-default` を付けた。ローカルの構造検査スクリプト `scripts/validate_handoff.py` を追加。
- 写真調の汎用的な森の画像を英日トップと地域選択ページで共有。画像はクマ、人物、実在の識別可能な山や施設を含まない。

## 画像

- `assets/forest-trail-hero.png`、1672×941 px、3,143,415 bytes。英日トップのヒーローと地域選択ページの視覚的な区切りに使用。
- 目視確認：広葉樹の道・遠景のみで、クマ、人物、文字、ブランド、識別可能な施設なし。生成画像なので実在の登山道を示すものではない。本文にその旨を記載。
- alt案：英語 `Illustrative forest trail; no identifiable real location`、日本語 `場所を特定しない森の登山道のイメージ`。
- 生成方法：組み込みの imagegen、1回で採用、再試行なし。プロンプト要旨：`photorealistic-natural` の横長16:9ウェブ用ヒーロー。場所を特定しない落ち着いた森の登山道、柔らかな朝の光、低彩度の緑・砂色。クマ・他の動物・人物・特定可能な山や施設・危険の演出・文字・ロゴを禁止。

## 検証

- `python scripts/validate_handoff.py`：HTML 11ファイル、sitemap、相対リンク、画像参照、JSON-LD構文、日英 `hreflang` 対応を確認。通過。ただし内容や安全性の判定ではない。
- `git diff --cached --check`：エラーなし。
- 禁止された安全の断定表現（`is safe`、`be safe`、`keeps you safe`、`you will be fine`、`大丈夫`、`安全です`）と `href="#"` をHTML全文で検索：該当なし。
- Edge のローカル描画で、英語トップ、英語・日本語の地域ページをデスクトップで確認。500pxの狭いウィンドウでも一列レイアウトを確認。スクリーンショットは作業領域の `outputs/kuma-en-home-final.png`、`outputs/kuma-en-region-final.png`、`outputs/kuma-ja-region-final.png`、`outputs/kuma-en-500.png`。Edgeヘッドレスは390px指定時に実際のレイアウト幅が約500pxとなるため、390px実機の検証は未了。
- ステージ後の実出力（コミット前）：`git diff --cached --stat` は12ファイル・236挿入・17削除（画像3,143,415 bytes）。`git status --short` は本報告を含む上記12ファイルのみ。

## 根拠と要確認事項

- 分布・体格は[WWFジャパン](https://www.wwf.or.jp/activities/basicinfo/2407.html)を参照。2012年の解説であり、サイズを現在の個体数や個別登山道の危険度として扱っていない。環境省の[クマ情報一覧](https://www.env.go.jp/nature/choju/effort/effort12/effort12.html)と[訪日客向け英語チラシ](https://www.env.go.jp/nature/choju/effort/effort12/kuma_eng_paper.pdf)へのリンクは設置したが、保護されたPDF本文の要約はしていない。
- `FACTCHECK`：ヒグマとツキノワグマで遭遇時の推奨行動に違いがあるか。未確認のため、北海道向けの具体的対処は未記載。Claudeの安全レビューまで公開しない。
- 山名・登山道ごとの出没情報や自治体リンク集は裏取り資料がなく、今回の島別入口には載せていない。次段階で地域別の公式ページを検証すれば精度を上げられる。
- 収益枠、既存の広告コメント、秘密情報は編集・公開していない。pushなし。

## Claude Code に見てほしい箇所

1. 九州「地域的に絶滅と考えられる」の表現が現在の一次資料と整合するか。
2. 北海道向け行動案内を未掲載にした安全判断と、既存 FAQ JSON-LD の適用範囲。
3. 英語の用語・サイズの訳、モバイル実機表示、トップの導線。
4. 公開可否と push。未確認の FACTCHECK が残る点を明示して判断する。
