# 住所機械翻訳理論
## Address Machine Translation Theory over Address Morphism Theory

Status: Draft v1  
Date: 2026-06-27  
Repository: Address Morphism Theory  
Scope: 住所写像論と住所翻訳理論の上に構築する、安全な住所機械翻訳の理論。  

## Abstract

住所機械翻訳は、通常の自然言語機械翻訳とは異なる。一般文の翻訳では流暢さ、意味保存、文体が重視されるが、住所翻訳では参照先保存、住所成分保存、国別住所順序、郵便・配送互換性、出典信頼度、曖昧性検出、非回答能力が必要になる。住所機械翻訳が誤ると、配送失敗、税関不備、本人確認失敗、緊急対応遅延、プライバシー漏えいにつながる。

本稿は、住所機械翻訳理論（Address Machine Translation Theory, AMTT）を、住所写像論（Address Morphism Theory, AMT）と住所翻訳理論（Address Translation Theory, ATT）の実装・検証層として定式化する。中心原則は、機械翻訳モデルを直接住所ラベル生成器として使わず、解析、候補展開、参照解決、構造化、制約付きレンダリング、検証ゲート、非回答状態を経由することである。

本稿では、住所機械翻訳を、出典階層、ローマ字化規格、公式別名、国際配送レンダリング、ニューラル提案、候補検証、品質スコア、衝突検出、round-trip by referent、human-in-the-loop、conformance testsを持つ安全なパイプラインとして定義する。

## Keywords

住所機械翻訳、住所翻訳、住所写像論、制約付き翻訳、参照保存、国際配送、ローマ字化、地名翻訳、郵便住所、AGID、AOID

## 1. Introduction

住所を機械翻訳することは、住所文字列を別言語の自然な文字列へ変換することではない。住所は、言語表現であると同時に、地理対象、行政対象、郵便対象、配送対象、建物対象、自然地物対象を指す参照である。

一般的な機械翻訳モデルは、文脈に合う自然な出力を作ることに優れる。しかし住所では、自然さよりも、参照先と配送互換性が重要である。モデルが固有名詞を普通名詞として訳したり、住所順序を誤ったり、郵便番号を落としたり、行政区を別地域へ寄せたりすると、見た目は自然でも住所としては危険である。

したがって、住所機械翻訳は、自由生成ではなく、制約付き変換でなければならない。

\[
\text{free translation}
\neq
\text{safe address machine translation}.
\]

本稿は、住所機械翻訳に必要な数理モデル、実装パイプライン、検証ゲート、評価指標、失敗状態を定義する。

## 2. Relationship to AMT and ATT

AMTは、住所表現が何を指すかを扱う。

\[
\operatorname{AMT}:s\mapsto q.
\]

ATTは、対象 \(q\) を目標言語・文字・文脈でどう表記するかを扱う。

\[
\operatorname{ATT}:q\mapsto \hat{s}_v.
\]

AMTTは、これを機械的にどう安全に実行するかを扱う。

\[
\operatorname{AMTT}:
(s,\mathcal{D},\mathcal{M},\mathcal{P})
\to
(\hat{s}_v,\mathsf{status},\mathsf{evidence}).
\]

ここで、\(\mathcal{D}\) は出典集合、\(\mathcal{M}\) はモデル集合、\(\mathcal{P}\) はポリシー集合である。

AMTTは、AMTやATTを置き換えない。AMTTは、AMTの参照解決とATTの参照保存則を満たすための実行理論である。

## 3. Threat Model

住所機械翻訳には、通常の翻訳評価では見落とされる脅威がある。

| Threat | Example | Consequence |
| --- | --- | --- |
| proper-name mistranslation | 建物名を普通名詞に訳す | 配送先消失 |
| order error | 日本語順序を英語配送順へ直さない | 国際配送失敗 |
| component deletion | 部屋番号、階、入口を落とす | ラストマイル失敗 |
| alias collision | 同じローマ字が複数地名を指す | 誤配送 |
| official-name gap | 公式英語名を知らない | 表記不一致 |
| postal incompatibility | 郵便番号や地域順序が不正 | 郵便検証失敗 |
| over-normalization | 旧名や方言名を消す | 参照履歴喪失 |
| hallucinated place | モデルが存在しない地名を生成 | 致命的誤り |
| privacy leakage | 非公開成分を翻訳出力に混ぜる | 個人情報漏えい |

したがって、AMTTは、モデル出力を信じるのではなく、モデル出力を検証対象として扱う。

## 4. Formal Pipeline

住所機械翻訳パイプラインを次で定義する。

\[
s
\xrightarrow{\pi}
T
\xrightarrow{\lambda}
L
\xrightarrow{\varepsilon_t}
C
\xrightarrow{\kappa}
q^\star
\xrightarrow{\sigma}
X
\xrightarrow{R_{v,\chi}}
\hat{s}_v
\xrightarrow{V}
\mathsf{Decision}.
\]

各段階は次を意味する。

- \(\pi\): tokenization and component parsing。
- \(\lambda\): language, script, and locale detection。
- \(\varepsilon_t\): alias, romanization, official-name, postal, and historical expansion。
- \(C\): candidate referent set。
- \(\kappa\): candidate clustering and selection。
- \(q^\star\): selected or unresolved referent。
- \(\sigma\): structured address component extraction。
- \(R_{v,\chi}\): target rendering under locale \(v\) and context \(\chi\)。
- \(V\): validation gate。
- \(\mathsf{Decision}\): emit, manualRequired, ambiguous, searchOnly, or reject。

このパイプラインでは、ニューラル翻訳は \(\varepsilon_t\)、\(R_{v,\chi}\)、候補補助に使えるが、単独で最終決定をしない。

## 5. Data and Authority Hierarchy

住所機械翻訳は、複数の出典を統合する。

\[
\mathcal{D}
=
\mathcal{D}_{official}
\cup
\mathcal{D}_{postal}
\cup
\mathcal{D}_{carrier}
\cup
\mathcal{D}_{geo}
\cup
\mathcal{D}_{community}
\cup
\mathcal{D}_{model}.
\]

出典階層は次の優先順位を持つ。

1. official address, administrative, and postal data。
2. official multilingual gazetteer。
3. carrier-accepted logistics format。
4. open geographic data with language tags。
5. community aliases and OSM names。
6. romanization standards。
7. neural or large language model proposals。
8. user or operator correction。

モデル提案は常に候補であり、権威ではない。

## 6. Constrained Decoding

住所機械翻訳では、自由デコーディングを避け、成分制約を使う。

構造化住所成分を

\[
X=(x_1,x_2,\ldots,x_n)
\]

とし、目標レンダリングを

\[
\hat{s}_v=R_{v,\chi}(X)
\]

とする。

レンダリング関数は、国・言語・配送文脈に応じて成分順序を制約する。

\[
R_{v,\chi}\in\mathcal{R}_{country,language,mode}.
\]

モデルが生成できる文字列は、次の制約を満たすものに限定する。

\[
\hat{s}_v\in \mathcal{L}_{allowed}(country,mode,\chi).
\]

この制約には、郵便番号位置、国名、行政階層、部屋番号、建物名、道路名、現地語併記などが含まれる。

## 7. Machine Translation as Proposal

ニューラル翻訳またはLLMの出力を

\[
m(s,v)=\tilde{s}_v
\]

とする。AMTTでは、\(\tilde{s}_v\) は最終出力ではなく提案である。

\[
\tilde{s}_v
\xrightarrow{parse}
\tilde{X}
\xrightarrow{validate}
\mathsf{Decision}.
\]

検証を通った場合のみ、

\[
\hat{s}_v=\operatorname{RepairOrAccept}(\tilde{s}_v,X,\mathcal{P})
\]

として採用する。

検証できない場合は、自然な訳文であっても出力しない。

## 8. Quality Vector

住所機械翻訳の品質は、単一スコアだけでは不十分である。品質ベクトルを定義する。

\[
\mathbf{Q}_{AMTT}
=
(q_{\mathrm{ref}},
q_{\mathrm{component}},
q_{\mathrm{order}},
q_{\mathrm{postal}},
q_{\mathrm{geo}},
q_{\mathrm{source}},
q_{\mathrm{collision}},
q_{\mathrm{privacy}},
q_{\mathrm{freshness}}).
\]

ここで、

- \(q_{\mathrm{ref}}\): 参照保存。
- \(q_{\mathrm{component}}\): 成分保存。
- \(q_{\mathrm{order}}\): 住所順序。
- \(q_{\mathrm{postal}}\): 郵便・配送互換性。
- \(q_{\mathrm{geo}}\): 地理的一貫性。
- \(q_{\mathrm{source}}\): 出典信頼度。
- \(q_{\mathrm{collision}}\): 別名・ローマ字衝突の低さ。
- \(q_{\mathrm{privacy}}\): 非公開成分漏えいの低さ。
- \(q_{\mathrm{freshness}}\): 出典鮮度。

文脈別ゲートは、

\[
G_{\chi}(\mathbf{Q}_{AMTT})\in\{0,1\}
\]

として定義する。

## 9. Decision Rule

決定規則を次で定義する。

\[
G_{\chi}(\mathbf{Q}_{AMTT})=1
\land
\operatorname{Separated}(q^\star,C)=1
\Rightarrow
\mathsf{emit}.
\]

それ以外は、次のいずれかへ落とす。

\[
\mathsf{Decision}\in
\{\mathsf{manualRequired},
\mathsf{ambiguous},
\mathsf{searchOnly},
\mathsf{sourceGap},
\mathsf{reject}\}.
\]

AMTTにおいて、非回答は失敗ではない。誤配送や誤表示を防ぐための安全な出力である。

## 10. Referent Round-Trip Evaluation

通常の機械翻訳ではBLEUやCOMETのような指標が使われる。しかし住所翻訳では、文章類似度だけでは不十分である。

AMTTでは、参照往復評価を使う。

\[
s
\xrightarrow{AMTT}
\hat{s}_v
\xrightarrow{resolve}
\hat{q}
\]

が

\[
\hat{q}=q^\star
\]

を満たすかを見る。

これを referent round-trip accuracy と呼ぶ。

## 11. Component Preservation Evaluation

成分保存率を定義する。

\[
\mathrm{CPR}
=
\frac{|\operatorname{Components}(s)\cap \operatorname{Components}(\hat{s}_v)|}
{|\operatorname{RequiredComponents}(s,\chi)|}.
\]

ただし、単純な文字列一致ではなく、同一成分の別表記・ローマ字・公式別名を許す。

配送文脈では、建物、部屋、入口、郵便番号、地域、国名の欠落に重いペナルティを与える。

## 12. Collision Risk

翻訳・ローマ字化・別名展開による衝突を定義する。

\[
\operatorname{CR}(\hat{s}_v)
=
|\{q\in Q_t:\hat{s}_v\in \operatorname{NameSet}(q)\}|.
\]

\[
\operatorname{CR}(\hat{s}_v)>1
\]

なら、追加証拠なしに配送ラベルとして出力してはならない。

この指標は、ピンイン、ヘボン式、Revised Romanization、アラビア語ローマ字、キリル文字転写、方言由来地名で重要である。

## 13. Privacy Gate

住所機械翻訳は、必要以上に住所を露出してはならない。

出力ビューを

\[
\mathsf{View}_r(\hat{s}_v)
\]

とし、役割 \(r\) に応じて許可される成分を制限する。

\[
\operatorname{Allowed}(r,c_i,\chi,t)=1
\]

の成分だけを出力できる。

販売者向け、配送会社向け、税関向け、ラストマイル向け、ユーザー向けは同じ翻訳出力であってはならない。

## 14. Human-in-the-Loop

AMTTは、人手修正を安全に扱う必要がある。

修正データを

\[
h=(s,\hat{s}_v,q,\mathrm{reviewer},\mathrm{source},\mathrm{scope},t,\mathrm{status})
\]

とする。

人手修正は、次の場合に使う。

- sourceGap。
- aliasConflict。
- carrierFormatUnknown。
- disputedTerritory。
- buildingNameUnknown。
- local custom unknown。

人手修正は、国、言語、行政区、配送会社、時刻でスコープし、無制限に全世界へ適用してはならない。

## 15. Regional Model Policies

AMTTは、国・地域ごとのポリシーを持つ。

### Japan

日本語住所は国内形式と国際配送英語形式を分ける。ローマ字は原則ヘボン式だが、公式施設名・駅名・建物名・企業名を優先する。

### Mainland China

簡体字、Hanyu Pinyin、中国大陸行政区画を基礎にする。歴史的英語別名はaliasとして保持し、配送会社の受理形式で使う。

### Taiwan

繁体字、台湾慣用英語、台湾式ローマ字を優先する。Hanyu Pinyinは補助aliasとして扱う。

### Hong Kong

香港英語、広東語由来地名、繁体字を基礎にする。普通話ピンインへの単純変換は禁止する。

### Macao

ポルトガル語、中国語、広東語、英語補助を分離する。ポルトガル語地名を公式文化層として扱う。

### Korea

Revised Romanizationを基礎にし、公式英語名と既存慣用名をaliasとして保持する。

### Multilingual Europe

ベルギー、スイス、アイルランド、スペイン自治州、キプロス、マルタなどでは、住所に使われる公式言語と地域言語だけを住所レンダリング対象にする。アプリ言語の多さと住所言語の多さを混同しない。

## 16. Evaluation Metrics

AMTTの評価は次を含む。

| Metric | Meaning |
| --- | --- |
| referent accuracy | 翻訳後も同じ対象を指す割合 |
| component preservation | 必須成分が保持される割合 |
| order validity | 国別住所順序が正しい割合 |
| postal compatibility | 郵便・配送形式が通る割合 |
| collision rejection | 衝突時に出力しない割合 |
| manual routing accuracy | manualRequiredへ正しく落とす割合 |
| privacy leakage rate | 不要な成分を出さない割合 |
| source attribution coverage | 出典が付与される割合 |

重要なのは、出力率だけを最大化しないことである。

\[
\text{high emission rate}
\neq
\text{safe AMTT}.
\]

## 17. Conformance Tests

実装は次のテストセットを持つべきである。

1. 日本語住所から国際配送英語への変換。
2. 中国本土の簡体字からHanyu Pinyinと英語別名への変換。
3. 台湾・香港・マカオの地域別レンダリング。
4. 韓国住所のRevised Romanization。
5. アラビア文字圏の国別ローマ字・英語・フランス語補助。
6. 多言語ヨーロッパの公式言語別レンダリング。
7. 建物名・部屋番号・入口の保持。
8. 郵便番号・行政区の順序検証。
9. alias collision時のmanualRequired。
10. sourceGap時の非回答。
11. privacy gate違反の拒否。
12. referent round-trip評価。

## 18. Theorem: Safe Machine Translation Emission

住所表現 \(s\)、目標ロケール \(v\)、文脈 \(\chi\) に対して、候補集合 \(C_t(s)\) が有限で、対象 \(q^\star\) が分離され、品質ベクトルがゲートを満たし、プライバシー制約が破られていないとする。

\[
\left[
\begin{array}{c}
C_t(s)\ \mathrm{finite}\\
\operatorname{Separated}(q^\star,C_t(s))=1\\
G_{\chi}(\mathbf{Q}_{AMTT})=1\\
\operatorname{PrivacySafe}(\hat{s}_v,r,\chi)=1
\end{array}
\right]
\Rightarrow
\operatorname{Emit}(\hat{s}_v).
\]

そうでなければ、

\[
\operatorname{Decision}
\in
\{\mathsf{manualRequired},
\mathsf{ambiguous},
\mathsf{searchOnly},
\mathsf{sourceGap},
\mathsf{reject}\}.
\]

この定理は、機械翻訳が常に正しいことを主張しない。安全に出力できる条件を明示する。

## 19. Limitations

AMTTには限界がある。

- 公式出典が古い場合。
- 配送会社の受理形式が公開されていない場合。
- 紛争地域の名称が複数存在する場合。
- 建物内部情報が非公開の場合。
- ユーザー入力が虚偽の場合。
- 自然地物や島しょ部で配送点が不明な場合。
- 税関・法制度により開示が必要な場合。

AMTTの責任は、これらを完全自動で解決することではなく、誤って解決済みにしないことである。

## 20. Conclusion

住所機械翻訳は、通常の機械翻訳ではなく、参照保存、成分保存、住所順序、郵便互換性、出典信頼度、プライバシー制約を満たす制約付き変換である。

中心原則は次である。

\[
\text{models propose; gates decide}.
\]

AMTTでは、モデルは候補を出す。最終判断は、AMTの参照解決、ATTの参照保存則、郵便・地理・出典・プライバシーゲートが行う。この設計により、住所機械翻訳は、多言語住所、国際配送、AGID/AOID、住所QR、秘匿配送、郵便番号補完、地名ローマ字化に安全に接続できる。

## Appendix A. Core Notation

| Symbol | Meaning |
| --- | --- |
| \(s\) | 入力住所表現 |
| \(T\) | 解析済みトークン集合 |
| \(L\) | 言語・文字・ロケール情報 |
| \(C_t(s)\) | 時刻 \(t\) の候補集合 |
| \(q^\star\) | 選択または高信頼候補対象 |
| \(X\) | 構造化住所成分 |
| \(R_{v,\chi}\) | 目標ロケール・文脈レンダリング |
| \(\hat{s}_v\) | 生成された目標住所表現 |
| \(V\) | 検証ゲート |
| \(\mathbf{Q}_{AMTT}\) | AMTT品質ベクトル |
| \(G_{\chi}\) | 文脈別出力ゲート |

## Appendix B. Minimal AMTT API Shape

```json
{
  "status": "emit | manualRequired | ambiguous | searchOnly | sourceGap | reject",
  "targetLocale": "en",
  "mode": "international-English",
  "rendered": "structured address rendering",
  "components": {},
  "qualityVector": {
    "referent": 0.0,
    "component": 0.0,
    "order": 0.0,
    "postal": 0.0,
    "geo": 0.0,
    "source": 0.0,
    "collision": 0.0,
    "privacy": 0.0,
    "freshness": 0.0
  },
  "sources": [],
  "warnings": []
}
```

このAPIは、モデルが何を出したかだけでなく、なぜ出してよいか、またはなぜ出してはいけないかを返す。

