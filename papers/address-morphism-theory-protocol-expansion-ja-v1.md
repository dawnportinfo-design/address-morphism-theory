# 住所写像論プロトコル増補

## 住所入力なし配送・住所非開示配送・国際配送・ペーパーレス運用への形式化

Version: 0.1.0  
Status: Draft / protocol-oriented expansion  
Date: 2026-06-28

## 要旨

本稿は、住所写像論（Address Morphism Theory, AMT）を、単なる住所解析・住所正規化の理論ではなく、住所を入力しない配送、住所を相手に知らせない配送、国際配送、機械可読な引渡し、ペーパーレスな配送受付へ接続するための増補である。

AMTの中核は、住所文字列を真の住所そのものとみなさず、住所可能対象、観測、証拠、制度、目的、時間、開示範囲の間にある条件付き写像として扱う点にある。本稿ではこの考えを拡張し、住所を「人間が読む文章」から「権限・目的・証拠・配送能力を持つプロトコル対象」へ移す。

結論は次の通りである。

1. AMT単体は完全な通信プロトコルではない。
2. しかしAMTは、AGID、AOID、Secure Address QR、配送レシート、ZK住所述語、国別住所パック、郵便番号生成モデルの意味論的な土台になれる。
3. 住所入力なし配送を成立させるには、住所対象を直接開示せず、役割別ビュー、配送可能性述語、国際配送述語、紙ラベル代替トークン、署名付き状態遷移、失効、再送防止を組み合わせる必要がある。
4. 「住所を見せない」は「誰も住所らしい情報を一切見ない」ではなく、「相手方・EC・POS・ホテル・中間システムには raw address を出さず、必要な権限を持つ配送主体だけが最小ビューを解決できる」という主張に限定すべきである。

この増補は、AMT本体、ZK住所述語論文、住所翻訳理論、住所機械翻訳理論、郵便番号生成理論、AGID実装をつなぐ中間層として設計する。

## 1. 問題設定

従来の住所処理は、次の前提に依存している。

- 利用者が住所文字列を入力する。
- EC事業者や受付担当者が人間可読の住所を保持する。
- 配送ラベルに住所が印字される。
- 郵便番号が地域識別の主要な補助線になる。
- 国ごとの住所制度差はフォーム側の項目差として処理される。

しかし、この前提は世界規模の配送では壊れやすい。理由は以下である。

- 郵便番号がない地域がある。
- 郵便番号はあるが、建物・道路・集落の解像度が不足する地域がある。
- 住所が行政住所、配送住所、地図検索住所、本人確認住所で一致しない。
- 住所の翻訳・ローマ字化で参照対象が変わることがある。
- ホテル、空港、港、ゴルフ場、スキー場、キャンプ、島、山岳、海域では、名前のある場所と荷物を渡せる点が異なる。
- 受取人は相手に住所を知らせたくない場合がある。
- 国際配送では、税関・制裁・危険物・配送会社ルールにより、相手には隠しても権限ある主体には限定開示が必要になる。

AMTはこれらを、住所文字列の誤りとしてではなく、写像の条件不足、証拠不足、目的不一致、開示範囲不一致として扱う。

## 2. 基本命題

本稿の基本命題は次である。

> 住所とは、場所を表す文章ではなく、特定の目的と権限のもとで住所可能対象へ到達するための、証拠付き・時間付き・制度付きの写像プロトコルである。

この命題を数式で弱く表すと、住所解決は単一関数ではなく、次の部分写像族である。

\[
R_{\chi,t,\rho,\sigma}: S_t \rightharpoonup
Q_t \times \mathsf{Status} \times \mathsf{Evidence} \times \mathsf{View}
\]

ここで、

- \(S_t\) は時刻 \(t\) における表面住所表現の空間である。
- \(Q_t\) は住所可能対象の空間である。
- \(\chi\) は利用目的、例えば配送、本人確認、地図検索、行政提出、匿名配送である。
- \(\rho\) は制度・配送会社・国別ルール・コンプライアンス方針である。
- \(\sigma\) は同意、権限、資格、署名、認可トークン、証明である。
- \(\mathsf{Status}\) は resolved, partial, ambiguous, unresolved, manualRequired, rejected などの状態である。
- \(\mathsf{Evidence}\) は郵便、行政、地理、言語、配送、鮮度、出典、プライバシーなどの証拠ベクトルである。
- \(\mathsf{View}\) は役割別に開示される情報である。

重要なのは、\(R\) が全域関数ではなく、条件付きの部分写像である点である。安全な理論は、すべてを解決するのではなく、解決できないときに安全な非回答を出す。

## 3. 住所対象の分解

AMTでは、配送に関係する対象を一つの点に潰さない。少なくとも次を分ける。

\[
q =
(q_{\mathrm{referent}},
q_{\mathrm{display}},
q_{\mathrm{admin}},
q_{\mathrm{postal}},
q_{\mathrm{access}},
q_{\mathrm{handoff}},
q_{\mathrm{route}},
q_{\mathrm{legal}})
\]

各成分の意味は次の通りである。

| 成分 | 意味 |
| --- | --- |
| \(q_{\mathrm{referent}}\) | 住所や地名が指す対象そのもの |
| \(q_{\mathrm{display}}\) | 地図や利用者画面で見せる代表点 |
| \(q_{\mathrm{admin}}\) | 行政区画上の所属 |
| \(q_{\mathrm{postal}}\) | 郵便制度上の所属 |
| \(q_{\mathrm{access}}\) | 実際に近づける入口、道路、港、ゲート、岸、駅 |
| \(q_{\mathrm{handoff}}\) | 荷物・鍵・QR・受付を渡せる点 |
| \(q_{\mathrm{route}}\) | 配送経路上のノードまたは区域 |
| \(q_{\mathrm{legal}}\) | 法令、本人確認、税関、管轄のための表現 |

例えば、山、島、港、ホテル、ゴルフ場、空港、大型施設では、表示点と引渡し点は一致しないことが多い。したがってAGIDやAOIDは、地理的な点だけでなく、これらの成分を束ねる参照対象として設計すべきである。

## 4. パンくず復元モデル

国別住所Repoや国別パックでは、住所をパンくずリスト型の階層として保存する方針が自然である。

\[
\mathsf{Path}(v) =
(v_0, v_1, \ldots, v_n)
\]

ただし、

\[
v_0 = \mathsf{Country},\quad
v_n = \mathsf{AddressableUnit}
\]

であり、各辺は親子関係を持つ。

\[
e_i : v_i \to v_{i+1}
\]

復元関数を次のように置く。

\[
\operatorname{Render}_{c,\ell,\chi}
(\mathsf{Path}(v), \pi)
\to
\mathsf{AddressExpression}
\]

ここで、

- \(c\) は国・地域モデルである。
- \(\ell\) は言語・文字体系である。
- \(\chi\) は用途である。
- \(\pi\) は開示ポリシーである。

このモデルの利点は、国ごとの制度差を保持したまま、共通のAGID側へ写像できる点である。日本の「都道府県から町丁目」への階層、米国の「州からStreet Address」への階層、中国の「省から社区・楼棟」への階層は同じ文字列形式に変換されるべきではないが、階層グラフとしては共通に扱える。

ただし、パンくず復元だけでは不十分な場合がある。

1. 建物入口が複数ある。
2. 行政上の親と配送上の親が異なる。
3. 郵便番号の区域と行政区画が一致しない。
4. 係争地域で複数の主張体系が存在する。
5. 山、海、砂漠、島しょ部では階層より近接・到達性が重要になる。

そのため、最終モデルは階層木ではなく、階層を主軸にした多重グラフである。

\[
G_c = (V_c, E_c, \tau_c, \lambda_c, \omega_c)
\]

ここで、

- \(V_c\) は住所要素ノード集合である。
- \(E_c\) は親子、隣接、包含、到達、翻訳、別名、継承、係争主張などの辺集合である。
- \(\tau_c\) はノード型である。
- \(\lambda_c\) は多言語ラベルである。
- \(\omega_c\) は出典、信頼度、時間範囲、ライセンスである。

パンくずはこのグラフ上の主要パスであり、唯一の構造ではない。

## 5. AGID互換性条件

AGIDは住所文字列のハッシュではない。AGIDは、住所可能対象または住所対象束への永続的識別子であるべきである。

AGID発行写像を次のように置く。

\[
I_{\chi,t}: Q_t \to \mathsf{AGID}
\]

ただし、発行には証拠ゲートが必要である。

\[
G_{\chi,t}(q,E)=1
\Rightarrow
I_{\chi,t}(q)=a
\]

ゲートが通らない場合、システムはAGIDを確定発行せず、候補、暫定ID、手動確認、または非回答を返す。

\[
G_{\chi,t}(q,E)=0
\Rightarrow
\mathsf{Status}\in
\{\mathsf{partial}, \mathsf{ambiguous}, \mathsf{manualRequired}, \mathsf{unresolved}\}
\]

AGID互換性は次の条件で定義する。

1. 構造保持: 住所階層を復元できること。
2. 目的保持: 配送用、本人確認用、地図検索用などの目的別ビューを生成できること。
3. 証拠保持: 発行時の出典、鮮度、信頼度を追跡できること。
4. 履歴保持: 行政変更、郵便番号変更、建物改名、統合・分割を追跡できること。
5. 開示制御: 権限のない主体に必要以上の住所成分を出さないこと。
6. 非回答保持: 危険なときに無理に解決しないこと。

## 6. 役割別ビュー束

住所非開示配送では、住所データを「見せるか見せないか」の二値で扱うと破綻する。実際には、役割ごとに必要なビューが異なる。

役割集合を次のように置く。

\[
\mathcal{R} =
\{
\mathsf{user},
\mathsf{merchant},
\mathsf{platform},
\mathsf{pos},
\mathsf{hotel},
\mathsf{carrier},
\mathsf{customs},
\mathsf{lastMile},
\mathsf{locker},
\mathsf{droneOps},
\mathsf{auditor}
\}
\]

開示写像は次である。

\[
\operatorname{View}_{r,\sigma,\chi,t}: \mathsf{DeliveryObject}
\to
\mathsf{RoleView}_r
\]

ここで、\(\sigma\) は同意・資格・署名・権限である。

ビューは全順序ではなく束である。

\[
\mathsf{View}_{merchant}
\not\subset
\mathsf{View}_{customs}
\]

かつ、

\[
\mathsf{View}_{locker}
\not\subset
\mathsf{View}_{lastMile}
\]

であることがある。税関は法令上の区域や申告情報を必要とし、ロッカーは開錠条件を必要とし、配送員は安全な停止点や引渡し条件を必要とする。これらは単純な「住所全文」の上位・下位ではない。

基本不変条件は次である。

\[
\mathsf{RawAddress}\notin\mathsf{View}_{merchant}
\]

ただし、利用者が明示的に通常住所共有モードを選んだ場合を除く。

## 7. Private Delivery Object

住所入力なし配送では、利用者が住所文字列を渡す代わりに、配送対象を表すオブジェクトを渡す。

\[
\mathsf{PDO} =
(
\mathsf{deliveryId},
\mathsf{agidRef},
\mathsf{aoidCommit},
\mathsf{alias},
\mathsf{policy},
\mathsf{routeHints},
\mathsf{credentialRefs},
\mathsf{expiry},
\mathsf{revocationRef},
\mathsf{receiptPolicy}
)
\]

このオブジェクトは、配送能力の照会と引渡しのための対象であって、住所全文の代替文字列ではない。

PDOの公開部は次を含めてよい。

- alias
- commitment
- delivery capability result
- allowed purpose
- expiry
- receipt identifier
- non-raw route class
- quality status

公開部に含めないものは次である。

- 個人が直接特定される住所全文
- 受取人名
- 部屋番号
- 電話番号
- 秘密鍵
- ZK witness
- 高精度な生座標

## 8. 配送可能性述語

配送は「住所が存在する」だけでは成立しない。配送可能性を別の述語として定義する。

\[
P_{\mathrm{deliver}}(q,\rho,\chi,t)=
\mathsf{state}
\]

返り値はブール値ではなく状態である。

\[
\mathsf{state}\in
\{
\mathsf{doorDeliverable},
\mathsf{buildingEntrance},
\mathsf{lockerAvailable},
\mathsf{pudoAvailable},
\mathsf{portOrShoreHandoff},
\mathsf{vehicleStopCandidate},
\mathsf{manualRequired},
\mathsf{cannotReach},
\mathsf{notSupported}
\}
\]

これにより、座標や地名を「配送可能」と誤って断定しない。特に、海、山、砂漠、災害地域、離島、大型施設、空港、スキー場、ゴルフ場ではこの分離が重要である。

## 9. 国際配送述語

国際配送では、配送可能性と法令・税関・制裁・危険物・配送会社ルールを分ける必要がある。

\[
P_{\mathrm{intl}}(o,d,i,\rho,t)=
\mathsf{intlState}
\]

ここで、

- \(o\) は発送元の管轄または区域である。
- \(d\) は配送先の管轄または配送区域である。
- \(i\) は品目クラスである。
- \(\rho\) は配送会社・税関・法令方針である。
- \(t\) は時刻である。

返り値は次のような状態である。

\[
\mathsf{intlState}\in
\{
\mathsf{accepted},
\mathsf{acceptedWithScopedDisclosure},
\mathsf{customsReview},
\mathsf{restrictedItem},
\mathsf{serviceUnavailable},
\mathsf{manualRequired}
\}
\]

この述語は、EC事業者に住所全文を返す必要はない。EC事業者には「配送可否」「必要な申告状態」「receipt」「alias」を返し、配送会社または税関には権限に応じた最小ビューを返す。

## 10. ペーパーレス・ラベルトークン

紙の住所ラベルを前提にしない場合、荷物や受付には人間可読住所ではなく、機械可読トークンを載せる。

\[
\mathsf{LabelToken}
=
H(
\mathsf{deliveryId}
\parallel
\mathsf{carrierScope}
\parallel
\mathsf{epoch}
\parallel
n
)
\]

このトークンはQR、NFC、バーコード、API応答、POSレシート、ホテルPMS出力、ロッカー引渡しコードとして表現できる。ただし、トークン自体に住所全文を埋め込まない。

安全な主張は次である。

> ペーパーレスとは、人間可読の住所全文を標準出力しないことである。配送会社が対応する範囲では、荷物は機械可読トークンでルーティングされる。

これは「世界中で一切の紙やラベルが不要」という主張ではない。現実の制度や配送会社の能力に応じて段階的に成立する。

## 11. 状態遷移とレシート

配送対象は状態機械として扱う。

\[
\mathsf{quote}
\to
\mathsf{reserved}
\to
\mathsf{accepted}
\to
\mathsf{inTransit}
\to
\mathsf{handoffReady}
\to
\mathsf{delivered}
\]

失敗状態と保留状態も第一級に扱う。

\[
\mathsf{manualRequired},\quad
\mathsf{carrierOnlyDisclosureRequired},\quad
\mathsf{cannotReach},\quad
\mathsf{revoked},\quad
\mathsf{expired},\quad
\mathsf{returned}
\]

各遷移は署名付きレシートを生成する。

\[
s_i
\xrightarrow{\tau_i,\operatorname{sig}_i}
s_{i+1}
\]

\(\tau_i\) には、住所全文ではなく、状態、時刻、役割、スコープ、deliveryId、非個人情報化された結果、必要に応じた監査参照を含める。

## 12. 可換図式

### 12.1 住所表現から目的別ビューへ

\[
\begin{tikzcd}
S_t
\arrow[r, "\operatorname{Parse}"]
\arrow[dr, "\operatorname{DirectRender}_{\ell,\chi}"']
& G_c
\arrow[r, "\operatorname{Resolve}_{\chi,t}"]
& Q_t
\arrow[d, "\operatorname{View}_{r,\sigma,\chi,t}"] \\
& \mathsf{AddressExpression}_{\ell,\chi}
\arrow[r, "\operatorname{Validate}"']
& \mathsf{RoleView}_{r}
\end{tikzcd}
\]

この図式は常に可換とは限らない。可換になるのは、解析・解決・検証が同じ参照対象を保持し、目的別ビューが同じ証拠境界を満たす場合だけである。

### 12.2 住所非開示配送

\[
\begin{tikzcd}
\mathsf{PDO}
\arrow[r, "\operatorname{Pred}_{deliver}"]
\arrow[d, "\operatorname{Disclose}_{carrier}"']
& \mathsf{MerchantReceipt}
\arrow[d, "\operatorname{AuditRef}"] \\
\mathsf{CarrierView}
\arrow[r, "\operatorname{Route}"]
& \mathsf{DeliveryReceipt}
\end{tikzcd}
\]

上段は相手方に見せる配送能力の証明であり、下段は配送会社が実際に使う限定ビューである。両者は同じdeliveryIdとcommitmentに結びつくが、同じ情報を含まない。

### 12.3 国際配送と限定開示

\[
\begin{tikzcd}
\mathsf{PDO}
\arrow[r, "P_{\mathrm{intl}}"]
\arrow[d, "\operatorname{Policy}"']
& \mathsf{IntlState}
\arrow[r, "\operatorname{MerchantDecision}"]
& \mathsf{AcceptedOrReview} \\
\mathsf{ComplianceView}
\arrow[r, "\operatorname{CustomsCheck}"']
& \mathsf{ScopedDisclosure}
\arrow[ur, "\operatorname{Receipt}"']
\end{tikzcd}
\]

この図式は、国際配送では相手方に全情報を開示せずとも、権限ある主体にだけ必要情報を渡す必要があることを示す。

### 12.4 AGID互換性

\[
\begin{tikzcd}
G_c
\arrow[r, "\operatorname{Emit}"]
\arrow[d, "\operatorname{Render}_{c,\ell,\chi}"']
& \mathsf{AGID}
\arrow[d, "\operatorname{Resolve}_{\chi,t}"] \\
\mathsf{AddressExpression}_{\ell,\chi}
\arrow[r, "\operatorname{Parse}"']
& Q_t
\end{tikzcd}
\]

この図式が完全可換である必要はない。必要なのは、同一性ではなく、指定目的に対する同じ参照対象または安全な非回答へ戻れることである。

## 13. 反例と境界

AMTをプロトコルに接続するとき、次の反例を明示的に扱う。

| 反例 | 破綻する素朴な主張 | 改良 |
| --- | --- | --- |
| 郵便番号がない国 | 郵便番号で全住所を補完できる | AGID主識別、行政区画、地理OSS、手動確認を併用 |
| 郵便番号が粗い国 | 郵便番号で建物まで分かる | 郵便番号は証拠の一部に限定 |
| 多言語国家 | 一つの言語形式で十分 | 住所に使われる言語だけをビュー化 |
| ローマ字衝突 | 翻訳すれば一意になる | collision budget と候補表示 |
| 大型施設 | 施設名が引渡し点である | access point と handoff point を分ける |
| 係争地域 | 一つの行政階層が正しい | viewpoint policy と claim layer を分ける |
| 海・山・砂漠 | 座標が住所である | named feature, access, route, safety state を分ける |
| 非公開住所 | 住所がない | 証拠は非公開、ビューだけ公開 |
| 国際配送 | 相手に住所を隠せば十分 | 税関・配送会社への限定開示を認める |
| 紙なし配送 | ラベルが不要 | 機械可読tokenとfallbackを持つ |

理論の強さは、これらを消すことではなく、危険な場合に状態として表現し、誤って resolved を出さないことである。

## 14. 信頼度ベクトル

住所品質は単一スコアだけでは足りない。証拠ベクトルで扱う。

\[
E(q)=
(e_{\mathrm{postal}},
e_{\mathrm{admin}},
e_{\mathrm{geo}},
e_{\mathrm{language}},
e_{\mathrm{source}},
e_{\mathrm{delivery}},
e_{\mathrm{freshness}},
e_{\mathrm{privacy}},
e_{\mathrm{compliance}})
\]

表示上は、利用者には短く次の状態で出せばよい。

\[
\mathsf{QualityStatus}\in
\{\mathsf{Verified},\mathsf{Partial},\mathsf{ManualRequired}\}
\]

開発者・監査者・研究者には、どの成分が弱いかを展開表示する。

## 15. 国別Repoと住所写像論

国別Repoは、単なるデータ置き場ではなく、AMTの実験可能な対象である。

各Repoは少なくとも次を持つべきである。

- country model
- administrative graph
- postal model
- AGID compatibility rules
- address format rules
- language and transliteration rules
- source index
- quality tests
- conformance fixtures
- lineage policy
- disputed or special-region policy

重いGISデータ、建物ポリゴン、検索インデックス、キャッシュ、衛星画像、PMTiles、FlatGeobufなどは外部ストレージまたはcountry packとして分離する。GitHubにはルール、軽量インデックス、出典、テスト、生成手順を置く。

## 16. 郵便番号生成理論との接続

郵便番号がない国または不十分な国では、AMTは郵便番号を「制度上の真実」として仮定しない。郵便番号は、住所グラフ上の圧縮写像である。

\[
Z_t: Q_t \to \mathsf{PostalZone}_t
\]

郵便番号生成は次の最適化問題として扱える。

\[
\min_{\mathcal{Z}}
\alpha C_{\mathrm{coverage}}
+ \beta C_{\mathrm{imbalance}}
+ \gamma C_{\mathrm{access}}
+ \delta C_{\mathrm{change}}
+ \eta C_{\mathrm{privacy}}
+ \theta C_{\mathrm{governance}}
\]

ただし、生成されたコードは公式郵便番号ではなく、状態を明示する。

\[
\mathsf{PostalCodeState}\in
\{
\mathsf{official},
\mathsf{carrier},
\mathsf{openData},
\mathsf{agidGenerated},
\mathsf{draft},
\mathsf{deprecated}
\}
\]

これにより、郵便番号のない地域でも、AGID、行政区画、配送拠点、道路到達性、地物、人口密度に基づく配送区画を作れる。ただし、公式制度と混同しない。

## 17. 住所翻訳理論との接続

住所翻訳は自然言語翻訳ではない。住所グラフから目的別ビューを生成する写像である。

\[
T_{c_1,c_2,\ell_1,\ell_2,\chi}:
\mathsf{AddressView}_{c_1,\ell_1}
\rightharpoonup
\mathsf{AddressView}_{c_2,\ell_2,\chi}
\]

正しい翻訳は、単語の意味対応ではなく、参照対象と配送能力を保持する。

\[
\operatorname{Resolve}_{c_1}(s)
\sim_{\chi}
\operatorname{Resolve}_{c_2}(T(s))
\]

ここで \(\sim_{\chi}\) は目的別同値関係である。国際配送用、本人確認用、地図検索用では同値関係が異なる。

## 18. ZK住所述語との境界

ZKは住所の真実を単独で証明しない。ZKは、AMTが定義した属性、出典、時刻、失効、目的、スコープに関する述語を、秘密を見せずに証明する。

AMT側は次を定義する。

- 住所対象
- 証拠ベクトル
- 品質ゲート
- 目的別属性
- 開示ビュー
- 非回答状態

ZK論文側は次を定義する。

- public statement
- private witness
- nullifier
- revocation root
- freshness root
- circuit
- proof bundle
- domain separation

両者の境界は次である。

\[
\begin{tikzcd}
\mathsf{AMTState}
\arrow[r, "\operatorname{Attribute}"]
& \mathsf{PredicateInput}
\arrow[r, "\operatorname{Prove}"]
& \mathsf{Proof}
\arrow[r, "\operatorname{Verify}"]
& \mathsf{PredicateResult}
\end{tikzcd}
\]

AMTは証明対象の意味を定義し、ZKは開示せずに検証するための暗号プロトコルを定義する。

## 19. 通信工学としての住所

住所は、通信工学的には宛先指定、ルーティング、権限、再送、到達性、名前解決、監査を持つ。

対応関係は次のように整理できる。

| 通信概念 | 住所プロトコル上の対応 |
| --- | --- |
| DNS | alias からAGID/AOID/配送対象を解決 |
| ルーティング | 配送拠点、港、ゲート、ロッカー、最終引渡し点 |
| TTL | alias, token, consent の有効期限 |
| mTLS | 事業者・配送会社・ホテル・PMS間の相互認証 |
| OAuth/OIDC | 住所利用権限の委任 |
| JWT | 短命の配送許可トークン |
| Webhook | 住所更新、配送受付、レシート発行通知 |
| DLQ | 失敗した住所検証・配送受付の隔離 |
| idempotency key | 二重登録・二重配送の防止 |
| replay prevention | QRやlabel tokenの再利用防止 |
| rate limit | 住所推測・大量照会防止 |
| E2E encryption | 相手方に見せず配送主体だけが限定ビューを取得 |

この観点では、住所は文字列ではなく、名前解決と配送能力を持つ通信対象である。

## 20. 実装可能なAPI境界

公開APIは raw address を標準で返さない。最小の形は次である。

```json
{
  "agid": "AGID_EXAMPLE",
  "alias": "ALIAS_EXAMPLE",
  "commitment": "COMMITMENT_EXAMPLE",
  "quality": "Partial",
  "deliverability": "manualRequired",
  "rawAddressReturned": false,
  "receipt": "RECEIPT_EXAMPLE"
}
```

住所を復元・翻訳・配送ラベル化するAPIは、目的、権限、国別モデル、出力粒度を必須にすべきである。

```json
{
  "agid": "AGID_EXAMPLE",
  "purpose": "international_shipping",
  "role": "carrier",
  "locale": "en",
  "disclosureScope": "carrier_minimum",
  "policy": "no_raw_to_merchant"
}
```

応答には次を含める。

- status
- quality
- warnings
- unverified fields
- source class
- postal match state
- delivery risk
- disclosure scope
- receipt

## 21. Conformance tests

AMTプロトコル増補の適合性テストは次を含む。

1. merchant view に raw address が含まれない。
2. carrier view は権限なしでは生成されない。
3. postal code がない地域でAGID主識別に切り替わる。
4. postal code が弱い地域で候補表示またはmanualRequiredになる。
5. 多言語住所が同じ参照対象へ戻るか、戻らない場合はcollision riskを出す。
6. 大型施設ではdisplay pointとhandoff pointを区別する。
7. 海、山、砂漠、島しょ部では座標だけでdoorDeliverableにしない。
8. 国際配送ではmerchant receiptとcompliance viewを分ける。
9. expired または revoked のPDOは配送受付不可になる。
10. 同じtokenの再利用は拒否または手動確認になる。
11. disputed region ではviewpoint policyが明示される。
12. sourceVersionが古い場合はfreshness warningを出す。

## 22. 定理の形

### 22.1 条件付き安全発行定理

候補集合 \(C_t(s)\) が有限であり、ある候補 \(q^\star\) が目的 \(\chi\) に関して十分に分離され、証拠ゲートが通るなら、resolverは resolved を出してよい。

\[
\left[
\begin{array}{c}
C_t(s)\ \mathrm{finite}\\
\exists q^\star\in C_t(s)\\
\forall q\neq q^\star,\ D_{\chi,t}(q^\star,q)>\delta_{\chi,t}\\
G_{\chi,t}(s,q^\star,E)=1
\end{array}
\right]
\Rightarrow
R_{\chi,t}(s)=\mathsf{resolved}(q^\star)
\]

それ以外では、resolverは非解決状態を出す。

\[
\neg \mathrm{Separated}
\lor
\neg G_{\chi,t}
\lor
\mathrm{SourceGap}
\Rightarrow
R_{\chi,t}(s)\in
\{\mathsf{partial},\mathsf{ambiguous},\mathsf{manualRequired},\mathsf{unresolved}\}
\]

### 22.2 開示単調性

権限が弱いビューは、強いビューの情報を超えてはならない。

\[
\sigma_1 \preceq \sigma_2
\Rightarrow
\operatorname{Info}(\mathsf{View}_{r,\sigma_1})
\subseteq
\operatorname{Info}(\mathsf{View}_{r,\sigma_2})
\]

ただし、役割が異なる場合は単純な包含関係ではなく、束上の比較になる。

### 22.3 目的別非一意性

同じ住所対象に対して、用途が異なれば正しい出力は一意ではない。

\[
\chi_1\neq \chi_2
\Rightarrow
\operatorname{Render}_{\chi_1}(q)
\not\equiv
\operatorname{Render}_{\chi_2}(q)
\]

したがって、住所翻訳APIや住所登録フォームは必ず目的を引数に持つべきである。

### 22.4 完全秘匿配送不可能性

すべての主体からすべての住所様情報を隠し、かつ任意の国際配送を常に成功させる一般プロトコルは存在しない。

より安全な主張は次である。

\[
\exists\ \mathsf{Protocol}:
\mathsf{MerchantView}\ \mathrm{is\ non\ raw}
\land
\mathsf{AuthorizedCarrierView}\ \mathrm{is\ sufficient}
\]

つまり、相手方には住所を見せず、権限ある配送主体には必要最小限の情報を与えるプロトコルなら構成可能である。

## 23. 実装ロードマップ

### Phase 1: Semantic package

- country model
- address graph
- breadcrumb reconstruction
- source and license index
- quality vector
- non-answer states

### Phase 2: AGID compatibility

- AGID emission gate
- AOID commitment
- alias
- lineage
- purpose-specific rendering
- no raw address release gate

### Phase 3: Private delivery

- PDO
- role view lattice
- merchant receipt
- carrier view resolver
- token expiry
- replay prevention

### Phase 4: International and field operations

- international predicate
- customs scoped disclosure
- vehicle stop candidate
- locker/PUDO handoff
- hotel/PMS preview
- POS receipt
- cannot-reach report

### Phase 5: Proof and audit

- ZK predicate bridge
- public statement registry
- revocation root
- audit log
- conformance vectors
- security review

## 24. 論文本文への入れ方

AMT本体にすべてを入れると、理論の焦点がぼやける。本文には短く次を入れるのがよい。

1. 住所はプロトコル対象であるという節。
2. role-based view latticeの定義。
3. delivery predicateとinternational predicateの境界。
4. AGID/AOID/ZK/配送プロトコルはAMT上の応用層であるという図。
5. 完全秘匿配送不可能性と限定開示可能性。

詳細なPDO、状態機械、通信API、レシート、再送防止は、AGID/AOID protocol paperまたはspecへ分離する。

## 25. 結論

住所写像論は、住所を単なる文字列から、証拠・制度・目的・開示・到達性を持つ写像対象へ引き上げる理論である。本増補により、AMTは住所入力なし配送、住所非開示配送、国際配送、ペーパーレス配送、郵便番号未整備地域、自然地理、機械可読引渡しを扱うための意味論的基盤として位置づけられる。

ただし、AMTはすべてを解く万能理論ではない。安全な最終主張は次である。

> AMTは、住所可能対象とその証拠・文脈・開示境界を定義する。AGID/AOIDプロトコルは、その上で住所を入力せず、相手に住所全文を見せず、配送可能性と引渡しレシートを機械可読に交換する。ZK住所述語は、必要な属性だけを秘匿証明する。

この分離により、住所写像論は、住所情報化、国際配送、プライバシー配送、郵便番号生成、国別住所Repo運営、ゼロ知識住所証明を支える中核理論として拡張できる。
