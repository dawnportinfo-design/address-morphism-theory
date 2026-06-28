# 住所翻訳理論
## Address Translation Theory over Address Morphism Theory

Status: Draft v1  
Date: 2026-06-27  
Repository: Address Morphism Theory  
Scope: 住所写像論の上に構築する住所翻訳・住所機械翻訳の理論。  

## Abstract

住所翻訳は通常の文章翻訳ではない。住所は物理空間、行政制度、郵便制度、配送経路、地名文化、履歴、建物・部屋・入口、自然地物を参照する表現である。したがって住所を翻訳するとは、単語を別言語へ置き換えることではなく、同一の住所対象を、目標言語、文字体系、国際配送形式、現地制度、配送文脈に合わせて安全に再表現することである。

本稿では、住所写像論（Address Morphism Theory, AMT）の上に、住所翻訳理論（Address Translation Theory, ATT）と住所機械翻訳理論（Address Machine Translation Theory, AMTT）を定義する。中心原理は、翻訳文字列の流暢さではなく、参照保存性である。すなわち、翻訳前後の表現が、同一の住所対象または同一の文脈的配送対象を指すことを第一条件とする。

本稿は、住所翻訳を、解析、候補展開、参照解決、構造化、目標形式レンダリング、検証ゲート、非回答状態からなる安全なパイプラインとして定式化する。特に、現地語住所、国際配送向け英語、ローマ字、ピンイン、Revised Romanization、広東語由来地名、ポルトガル語由来地名、多言語国家の公式名、方言由来地名、郵便番号・行政区・建物名の翻訳を、ひとつの文字列変換ではなく、参照保存的な表現写像として扱う。

## Keywords

住所翻訳、住所機械翻訳、住所写像論、参照保存、国際配送、ローマ字化、多言語住所、郵便住所、地名翻訳、AGID、AOID

## 1. Introduction

住所は、人間が空間を扱うための圧縮表現である。同じ場所であっても、日本語住所、英語住所、現地語住所、郵便住所、配送会社向け住所、観光名、旧地名、行政名、建物名、ローマ字表記は一致しないことが多い。

たとえば日本の住所を英語へ変換する場合、「東京都千代田区丸の内」は単に単語翻訳する対象ではない。配送ラベルとしては、建物名、階、部屋、丁目、番地、区、市区町村、都道府県、郵便番号、国名を、配送先国と配送会社が理解できる順序へ再構成する必要がある。

中国本土では、地名の多くは簡体字とHanyu Pinyinで扱うべきだが、Beijing / Peking や Guangzhou / Canton のような歴史的英語別名も物流や文献で残る。台湾ではHanyu Pinyinだけでは不十分で、TaipeiやKaohsiungのような慣用英語表記が配送上強い。香港では普通話ピンインではなく、広東語由来および英国式英語地名が重要である。マカオでは中国語、広東語、ポルトガル語、英語補助が重なる。

このような例は、住所翻訳が通常の機械翻訳よりも厳しいことを示す。住所翻訳の失敗は、文章の違和感ではなく、配送失敗、本人確認失敗、税関不備、緊急対応の遅延、地理的誤認につながる。

本稿の目的は、住所翻訳を、住所写像論の応用理論として定式化することである。

## 2. Boundary with Address Morphism Theory

住所写像論は、住所表現がどの住所対象を指すかを扱う。

\[
\operatorname{AMT}: \text{surface expression} \to \text{addressable referent}.
\]

住所翻訳理論は、解決済みまたは候補化された住所対象を、別の言語・文字・制度・配送文脈でどう表示するかを扱う。

\[
\operatorname{ATT}: \text{addressable referent} \to \text{target address rendering}.
\]

住所機械翻訳理論は、その処理を実装するためのデータ、モデル、検証ゲート、非回答状態を扱う。

\[
\operatorname{AMTT}: \text{sources + models + policies + gates}
\to
\text{safe translated address output}.
\]

したがって、住所翻訳はAMT本体を置き換えない。AMTが「何を指すか」を決め、ATTが「どう表記するか」を定義し、AMTTが「機械的に安全に生成できるか」を判定する。

## 3. Address Translation Is Not Sentence Translation

通常の文章翻訳では、意味がある程度保たれ、自然な文になれば目的を満たすことが多い。しかし住所翻訳では、次の性質が必要になる。

1. 参照先が変わらない。
2. 国・地域ごとの住所順序を守る。
3. 固有名詞を誤って普通名詞化しない。
4. 郵便番号、行政区、道路、建物、部屋、入口、配送引渡点を混同しない。
5. 現地語と国際配送英語の両方で使える。
6. 翻訳不能または危険な場合は非回答にできる。

したがって、住所翻訳は次の危険な写像ではない。

\[
\text{raw address string}
\to
\text{neural translation}
\to
\text{shipping label}.
\]

望ましい写像は次である。

\[
\text{parse}
\to
\text{resolve}
\to
\text{structure}
\to
\text{render}
\to
\text{validate}
\to
\text{emit or refuse}.
\]

## 4. Surface Expressions, Referents, and Locales

時刻 \(t\) における住所対象空間を \(Q_t\) とする。言語 \(L\)、文字体系 \(\Sigma\)、文脈 \(\chi\) における住所表現空間を

\[
S_{L,\Sigma,\chi,t}
\]

とする。

解析・解決写像を

\[
\rho_{L,\Sigma,\chi,t}:S_{L,\Sigma,\chi,t}\to \mathcal{P}(Q_t)
\]

とする。ここで \(\mathcal{P}(Q_t)\) としたのは、住所入力が曖昧であり、複数候補を返すことがあるためである。

住所翻訳写像は、単なる文字列写像ではなく、ロケール間の表現写像として定義する。

\[
\tau_{u\to v}:S_u\to S_v
\]

ただし、\(u=(L_u,\Sigma_u,\chi_u,t)\)、\(v=(L_v,\Sigma_v,\chi_v,t)\) である。

## 5. Referent Preservation Law

住所翻訳の中心法則は参照保存である。

翻訳前の表現 \(s\) が住所対象 \(q\) を指すとき、翻訳後の表現 \(\tau_{u\to v}(s)\) も同じ \(q\) を指す必要がある。

\[
q\in\rho_u(s)
\Rightarrow
q\in\rho_v(\tau_{u\to v}(s)).
\]

単一参照として解決済みの場合は、より強く次のように書ける。

\[
\operatorname{Ref}_t(s)
=
\operatorname{Ref}_t(\tau_{u\to v}(s)).
\]

この法則は、すべての語が翻訳可能であることを意味しない。むしろ、固有名詞、建物名、道路名、古い地名、方言由来名、港湾名、島名、山名は、翻訳せずに保持したり、公式別名を使ったり、ローマ字化したり、現地文字と英語補助を併記したりする。

## 6. Component-Preserving Translation

住所は線形文字列ではなく、構造化された成分の列である。

\[
c=
(c_{\mathrm{name}},
c_{\mathrm{organization}},
c_{\mathrm{building}},
c_{\mathrm{unit}},
c_{\mathrm{street}},
c_{\mathrm{block}},
c_{\mathrm{locality}},
c_{\mathrm{region}},
c_{\mathrm{postal}},
c_{\mathrm{country}},
c_{\mathrm{route}})
\]

住所翻訳は、語彙変換と順序変換の組である。

\[
\tau=(\tau_{\mathrm{lex}},\tau_{\mathrm{order}}).
\]

\(\tau_{\mathrm{lex}}\) は成分名、地名、道路名、建物名、行政名の表記を変換する。\(\tau_{\mathrm{order}}\) は目標国・目標文脈で正しい住所順序へ並べ替える。

この分離により、次の失敗を避ける。

- 語は英語になっているが、日本語順序のまま残る。
- 郵便番号が国際配送で読みにくい位置にある。
- 建物名と道路名の順序が逆になる。
- 市区町村と都道府県が入れ替わる。
- 現地語の建物名が消える。

## 7. Translation Modes

住所翻訳には少なくとも以下のモードがある。

| Mode | Meaning | Use |
| --- | --- | --- |
| native | 現地語・国内配送形式 | 国内配送、行政、現地確認 |
| international-English | 国際配送向け英語 | 海外EC、国際配送ラベル |
| official-alias | 公式多言語名・政府別名 | 多言語国家、行政文書 |
| romanization | 規格化されたローマ字化 | 日本、中国、韓国、アラビア文字圏など |
| carrier | 配送会社が受理しやすい形式 | DHL、郵便、ラストマイル |
| search-expansion | 検索再現率向上用の別名展開 | 検索候補生成 |

重要なのは、search-expansionを配送ラベルとして使わないことである。検索用の別名は同名衝突を増やすため、最終表示には検証ゲートが必要である。

## 8. Romanization, Transliteration, Translation, and Alias

住所翻訳では、以下を区別しなければならない。

| Operation | Meaning | Risk |
| --- | --- | --- |
| translation | 意味を別言語へ変換する | 固有名詞の誤訳 |
| transliteration | 文字体系を写す | 発音・慣用名を失う |
| romanization | 規格に基づきラテン文字化する | 同音・同綴衝突 |
| official alias | 公式別名を使う | 時代・機関差 |
| carrier alias | 配送実務上強い別名を使う | 公式名と違う可能性 |
| historical alias | 旧名を使う | 現在の行政とずれる |

たとえば中国語圏では、同じ漢字文化圏でも方針は分ける必要がある。

- 中国本土: 簡体字、Hanyu Pinyin、大陸行政単位、必要に応じ英語別名。
- 台湾: 繁体字、台湾慣用ローマ字、台湾英語住所、Hanyu Pinyin別名。
- 香港: 繁体字、香港英語、広東語由来地名、歴史英語地名。
- マカオ: 繁体字、ポルトガル語、広東語、英語補助。

これは「中国語を英語へ翻訳する」という単純問題ではない。地域別レンダリングである。

## 9. Address Machine Translation Pipeline

住所機械翻訳は、次の制約付きパイプラインとして定義する。

\[
s
\xrightarrow{\pi}
T
\xrightarrow{\varepsilon_t}
C
\xrightarrow{\kappa}
q
\xrightarrow{R_{v,\chi}}
\hat{s}_v
\xrightarrow{V}
\{\mathrm{emit},\mathrm{manual},\mathrm{reject}\}.
\]

ここで、

- \(\pi\): 入力を言語タグ付き成分へ解析する。
- \(\varepsilon_t\): 別名、旧名、公式名、ローマ字、郵便補完を展開する。
- \(C\): 候補集合である。
- \(\kappa\): 候補をクラスタ化または選択する。
- \(q\): 解決済みまたは高信頼候補の住所対象である。
- \(R_{v,\chi}\): 目標ロケール・文脈のレンダリング関数である。
- \(V\): 郵便、地理、出典、構造、配送文脈の検証ゲートである。

このパイプラインの中心は、文字列から文字列へ直接翻訳しないことである。

## 10. Source Hierarchy

機械翻訳の出力は、出典階層を持つべきである。

1. 公式住所・郵便データ。
2. 政府系多言語地名データ。
3. 郵便事業者・配送会社の受理形式。
4. オープン地理データの言語タグ・別名。
5. コミュニティ地名辞書・OSM別名。
6. 標準ローマ字化規則。
7. 統計的・ニューラルモデルの提案。
8. 人手修正。

ニューラル翻訳やLLM出力は、権威ではなく提案である。配送ラベルへ採用するには、参照保存、住所順序、郵便互換性、出典の検証が必要である。

## 11. Quality Score for Address Translation

翻訳品質を、流暢さだけで評価してはならない。次の品質関数を定義する。

\[
Q_{\mathrm{tr}}(\hat{s}_v,q,v,\chi,t)
=
w_1R+w_2O+w_3P+w_4G+w_5C-w_6H-w_7A.
\]

ここで、

- \(R\): 参照保存スコア。
- \(O\): 目標住所順序の正しさ。
- \(P\): 郵便・配送互換性。
- \(G\): 地理的一貫性。
- \(C\): 出典信頼度。
- \(H\): ローマ字・同綴衝突リスク。
- \(A\): 別名曖昧性リスク。

出力規則は次である。

\[
Q_{\mathrm{tr}}\ge \theta_{\mathrm{emit}}
\Rightarrow
\mathrm{emit}.
\]

\[
\theta_{\mathrm{manual}}\le Q_{\mathrm{tr}}<\theta_{\mathrm{emit}}
\Rightarrow
\mathrm{manualRequired}.
\]

\[
Q_{\mathrm{tr}}<\theta_{\mathrm{manual}}
\Rightarrow
\mathrm{rejectOrSearchOnly}.
\]

これにより、翻訳不能や危険な翻訳を無理に出さない。

## 12. Round-Trip by Referent

機械翻訳では逆翻訳がよく使われる。

\[
s\to \hat{s}_v\to \hat{s}_u.
\]

しかし住所では、文字列一致を要求すると厳しすぎ、逆に誤った自然な翻訳を見逃すことがある。重要なのは、文字列の往復一致ではなく、参照先の往復一致である。

\[
\operatorname{Ref}_t(s)
=
\operatorname{Ref}_t(\hat{s}_u).
\]

これを referent round-trip と呼ぶ。

## 13. Failure States

住所機械翻訳は、失敗状態を明示するべきである。

| State | Meaning |
| --- | --- |
| `language_gap` | 対象言語・文字の信頼できる出典が不足している。 |
| `alias_conflict` | 目標別名が複数対象を指す。 |
| `romanization_collision` | ローマ字化で複数名が同じ表記になる。 |
| `postal_order_uncertain` | 目標国の住所順序が検証できない。 |
| `carrier_format_unknown` | 配送会社が受理する国際形式が不明。 |
| `proper_name_risk` | 固有名詞を誤訳する危険がある。 |
| `source_gap` | 公式または高信頼出典が不足している。 |
| `manual_required` | 人手確認または権威ある出典が必要。 |

これらは単なるエラーではない。誤配送を防ぐ安全状態である。

## 14. Regional Policy Examples

### 14.1 Japan

日本語住所は、国内向けには大きい単位から小さい単位へ進む。国際配送向け英語では、建物・部屋・町名・区市町村・都道府県・郵便番号・国のように、配送事業者が読める順へ整える。

日本の地名は原則としてヘボン式ローマ字を基礎にする。ただし、公式英語名、駅名、施設名、建物名、企業名は既存の公式表記を優先する。

### 14.2 Mainland China

中国本土では、簡体字、Hanyu Pinyin、中国大陸行政単位を基礎にする。方言由来地名や歴史英語名が残る場合は、英語別名DBとして保持する。

### 14.3 Taiwan

台湾では、繁体字、台湾慣用ローマ字、台湾英語住所を重視する。Hanyu Pinyinは別名として保持できるが、配送上の主表記は慣用英語が強い場合がある。

### 14.4 Hong Kong

香港では、繁体字、香港英語、広東語由来地名、歴史英語地名を基礎にする。普通話ピンインへ単純変換してはならない。

### 14.5 Macao

マカオでは、繁体字、ポルトガル語、広東語、英語補助を分ける。ポルトガル語地名は正式文化として強く、英語だけへ寄せるべきではない。

### 14.6 Korea

朝鮮半島では、韓国の国際表記にはRevised Romanizationを基礎にする。ただし、北朝鮮、歴史名、公式英語名、地名慣用表記は別ポリシーとして扱う。

### 14.7 Arabic-Script Regions

アラビア文字圏では、アラビア語、フランス語、英語、現地ローマ字化が国により異なる。北アフリカではフランス語が強い国があり、湾岸では英語配送形式が強い場合がある。国別ポリシーが必要である。

### 14.8 Multilingual Europe

スイス、ベルギー、アイルランド、キプロス、マルタ、ルクセンブルク、スペイン自治州、フランス海外領などでは、住所に使われる言語だけを住所タブにする。アプリ言語と住所言語は分ける。

## 15. Proper Nouns and Non-Translation Rule

住所翻訳では、固有名詞をむやみに翻訳してはならない。

たとえば、建物名、ホテル名、道路名、駅名、港名、空港名、山名、島名、寺社名、大学名は、公式英語名または公式ローマ字名がある場合はそれを使う。ない場合は、現地表記とローマ字を併記する方が安全である。

一般原則:

\[
\text{proper noun}
\Rightarrow
\text{retain or official alias, not free translation}.
\]

## 16. Address Translation and International Shipping

国際配送向け英語住所は、英語として自然であることよりも、配送会社が読めることが重要である。

したがって、国際配送レンダリングは次の条件を満たす必要がある。

1. 国名が明確である。
2. 郵便番号が配送国の形式で保持される。
3. 行政階層が配送上必要な粒度で表示される。
4. 建物・部屋・入口が失われない。
5. 現地語固有名が必要な場合は保持される。
6. 配送会社が受理しやすい順序で並ぶ。

国際配送英語は、単なるEnglishタブではなく、international-English modeとして扱う。

## 17. Compatibility Between Native and English Forms

多言語住所では、母国語住所と国際配送英語が互換でなければならない。互換性は、文字列一致ではなく、成分対応で確認する。

\[
\operatorname{Comp}(s_{\mathrm{native}},s_{\mathrm{intl}})
=1
\]

とは、次が成立することを意味する。

- 同一対象を指す。
- 郵便番号が一致または制度上対応する。
- 行政階層が矛盾しない。
- 建物・部屋・入口情報が失われていない。
- 国際配送に必要な成分が存在する。

互換性が不十分な場合、システムは翻訳を出すのではなく、差分を表示し、補完または手動確認に落とす。

## 18. Human Correction and Governance

人手修正は重要だが、公式データを無制限に上書きしてはならない。修正は次の形で管理する。

\[
h=(\hat{s}_v,q,\mathrm{source},\mathrm{scope},t,\mathrm{reviewStatus}).
\]

修正は、国、地域、言語、対象種別、出典、時刻、レビュー状態でスコープされるべきである。配送成功履歴や現地利用実績がある場合、翻訳候補の信頼度を上げることができる。

## 19. Conformance Tests

住所翻訳理論の実装は、少なくとも次をテストする。

1. 参照保存テスト。
2. 成分保存テスト。
3. 住所順序テスト。
4. 郵便番号形式テスト。
5. 建物名・部屋番号保持テスト。
6. ローマ字衝突テスト。
7. 別名衝突テスト。
8. 国際配送英語レンダリングテスト。
9. 母国語住所と英語住所の互換テスト。
10. source gap時のmanualRequiredテスト。

特に重要なのは、翻訳ができることだけでなく、翻訳しない判断ができることである。

## 20. Relationship to AGID and AOID

AGIDは、地理・住所・地物の参照識別子として機能する。AOIDは、所有、同意、配送、秘匿、委譲、受領に関わる私的操作識別子として機能する。

住所翻訳理論は、AGID/AOIDに対し、次を提供する。

- AGIDが指す対象の多言語表示。
- AOIDで秘匿された配送先の国際配送レンダリング。
- raw住所を出さないalias表示。
- carrier-only disclosure時の配送会社向け表記。
- 住所QRに含めるべき表示言語の選択。

ただし、住所翻訳理論は暗号プロトコルではない。秘匿、ZK証明、nullifier、署名付きreceiptは別論文または別仕様で扱う。

## 21. Theorem: Safe Translation Emission

候補集合 \(C_t(s)\) が有限であり、対象 \(q^\star\) が文脈 \(\chi\) において十分に分離され、翻訳レンダリング \(\hat{s}_v\) が参照保存、成分保存、郵便互換性、出典ゲートを満たすとする。

\[
\left[
\begin{array}{c}
C_t(s)\ \mathrm{finite}\\
q^\star\in C_t(s)\\
\forall q\neq q^\star,\ D_{\chi,t}(q^\star,q)>\delta_{\chi,t}\\
G_{\mathrm{ref}}(s,\hat{s}_v,q^\star)=1\\
G_{\mathrm{component}}(s,\hat{s}_v)=1\\
G_{\mathrm{postal}}(\hat{s}_v,\chi)=1\\
G_{\mathrm{source}}(\hat{s}_v)=1
\end{array}
\right]
\Rightarrow
\operatorname{Emit}(\hat{s}_v).
\]

いずれかの条件が満たされない場合、

\[
\operatorname{Status}(\hat{s}_v)
\in
\{\mathrm{manualRequired},\mathrm{ambiguous},\mathrm{searchOnly},\mathrm{rejected}\}.
\]

この定理は、すべての住所が翻訳できることを主張しない。安全に翻訳を出してよい条件を定義する。

## 22. Limitations

住所翻訳理論にも限界がある。

- 公式データが誤っている場合。
- 現地語名と英語名の権威が分裂している場合。
- 紛争地域で地名主張が複数ある場合。
- 建物内部や部屋番号が非公開の場合。
- 配送会社ごとの受理形式が公開されていない場合。
- 税関や法制度が特定情報の開示を要求する場合。
- 災害や行政変更でデータが急速に古くなる場合。

したがって、ATT/AMTTは完全自動翻訳理論ではない。安全な翻訳、限定的な自動化、非回答、出典表示、手動確認を含む理論である。

## 23. Conclusion

住所翻訳は、文章翻訳ではなく、参照保存的な住所レンダリングである。住所写像論が住所対象を定義し、住所翻訳理論がその対象を言語・文字・制度・配送文脈に応じて再表現し、住所機械翻訳理論が安全な生成と検証を行う。

本稿の中心原則は次である。

\[
\text{resolve first, translate second, validate before emitting}.
\]

この原則により、住所翻訳は、単なる多言語表示ではなく、国際配送、住所QR、AGID/AOID、秘匿配送、郵便番号補完、地理検索、多言語国家の住所互換性を支える基盤になる。

## Appendix A. Core Notation

| Symbol | Meaning |
| --- | --- |
| \(Q_t\) | 時刻 \(t\) における住所対象空間 |
| \(S_{L,\Sigma,\chi,t}\) | 言語・文字・文脈付き住所表現空間 |
| \(\rho\) | 住所表現から候補対象への解析・解決写像 |
| \(\tau_{u\to v}\) | ロケール \(u\) から \(v\) への住所翻訳写像 |
| \(\tau_{\mathrm{lex}}\) | 語彙・表記変換 |
| \(\tau_{\mathrm{order}}\) | 住所成分順序変換 |
| \(R_{v,\chi}\) | 目標ロケール・文脈レンダリング関数 |
| \(V\) | 検証ゲート |
| \(Q_{\mathrm{tr}}\) | 翻訳品質スコア |
| \(\theta_{\mathrm{emit}}\) | 自動出力しきい値 |
| \(\theta_{\mathrm{manual}}\) | 手動確認しきい値 |

## Appendix B. Minimal Implementation Interface

住所翻訳APIは、少なくとも次を返すべきである。

```json
{
  "status": "emit | manualRequired | ambiguous | searchOnly | rejected",
  "mode": "native | international-English | official-alias | romanization | carrier",
  "targetLocale": "en | ja | zh-Hant | ...",
  "renderedAddress": "string or structured lines",
  "components": {},
  "referentId": "AGID/PID/AOID alias if available",
  "quality": {
    "referentPreservation": 0.0,
    "componentPreservation": 0.0,
    "postalCompatibility": 0.0,
    "sourceConfidence": 0.0,
    "collisionRisk": 0.0
  },
  "sources": [],
  "warnings": []
}
```

このインターフェースは、raw住所を必ず返すことを要求しない。AGID/AOID alias、commitment、carrier-only viewと組み合わせることで、住所非公開配送にも接続できる。

