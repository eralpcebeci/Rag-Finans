# Gold Evaluation Protocol

## 1. Amaç

Bu veri setinin amacı, RAG sisteminin finansal raporlardaki bilgileri
doğru şekilde bulma, ilişkilendirme ve cevaplama başarısını ölçmektir.

Evaluation dataset, sistemi geliştirmek için kullanılan parser, retriever
veya generation pipeline tarafından otomatik olarak doğru kabul edilen
çıktılardan oluşturulmamalıdır.

Her VERIFIED eval case, orijinal kaynak doküman üzerinden insan tarafından
kontrol edilmelidir.


## 2. Eval Case Kabul Kriterleri

Bir EvalCase VERIFIED kabul edilebilmesi için:

- Soru açık ve tek anlamlı olmalıdır.
- Soru kaynak dokümandan cevaplanabilir olmalıdır.
- Reference answer kaynak doküman tarafından desteklenmelidir.
- Evidence, reference answer için yeterli kanıt sağlamalıdır.
- Evidence sayfası doğru olmalıdır.
- Dış bilgi gerektirmemelidir.
- AnswerType doğru etiketlenmelidir.
- ReasoningType doğru etiketlenmelidir.
- Sorunun cevabı yalnızca tahmine veya yoruma dayanmamalıdır.


## 3. Eval Case Red Kriterleri

Aşağıdaki durumlardan biri varsa case reddedilir:

- Soru birden fazla şekilde yorumlanabiliyorsa.
- Reference answer dokümanda doğrulanamıyorsa.
- Evidence cevabı tam olarak desteklemiyorsa.
- Sorunun cevabı için doküman dışı bilgi gerekiyorsa.
- Soru gereksiz derecede belirsizse.
- Soru kaynak cümlenin anlamını bozuyorsa.
- Doğru cevabın ne olduğu konusunda insan doğrulayıcı emin olamıyorsa.


## 4. Evidence Kuralları

Her EvalCase en az bir evidence içermelidir.

Evidence:

- Kaynak dokümanı belirtmelidir.
- Doğru sayfa numarasını taşımalıdır.
- Reference answer'ı gerçekten destekleyen metni içermelidir.
- Gereksiz derecede büyük bir metin bloğu olmamalıdır.
- Gerekiyorsa birden fazla evidence kullanılabilir.

EvidenceRole kullanımı:

- PRIMARY:
  Cevabı doğrudan destekleyen ana kanıt.

- SUPPORTING:
  Ana cevabı açıklayan veya destekleyen ek kanıt.

- CALCULATION_INPUT:
  Reference answer'ın hesaplanması için kullanılan kaynak değer.


## 5. Soru ve Reasoning Türleri

### DIRECT

Cevap evidence içinde doğrudan bulunabilir.

Örnek:

Soru:
Akbank'ın 2025 yılı net dönem kârı kaç TL'dir?

Evidence:
2025 yılı net dönem kârı X TL olarak gerçekleşmiştir.


### CALCULATION

Cevap dokümanda doğrudan verilmez.
Evidence içindeki değerlerden deterministik bir hesaplama yapılması gerekir.

Örnek:

2024 net kâr = X
2025 net kâr = Y

Soru:
2024'ten 2025'e net kâr yüzde kaç artmıştır?


### COMPARISON

İki veya daha fazla bilgi karşılaştırılarak cevap oluşturulur.

Örnek:

Soru:
2024 ve 2025 dönemlerindeki aktif büyüklüklerini karşılaştırınız.


## 6. Soru Tasarım Kuralları

Sorular doğal kullanıcı diline yakın olmalıdır.

Kaynak cümlenin birebir soru formuna dönüştürülmesinden mümkün olduğunca
kaçınılmalıdır.

Sorular retrieval sistemine yapay şekilde ipucu vermemelidir.

Kötü örnek:

"2025 yılında net dönem kârı ne kadar gerçekleşmiştir?"

Kaynak metne fazla benzerdir.

Daha iyi örnek:

"Akbank'ın 2025 yılı net kârı kaç milyar TL'dir?"

Sorunun cevabı yine aynı evidence ile doğrulanabilir, ancak lexical eşleşme
daha azdır.


## 7. Human Verification Süreci

Bir case oluşturulduğunda:

1. Orijinal PDF açılır.
2. Soru kontrol edilir.
3. Reference answer kontrol edilir.
4. Evidence'ın doğru sayfadan geldiği doğrulanır.
5. Evidence'ın cevabı gerçekten desteklediği kontrol edilir.
6. AnswerType ve ReasoningType kontrol edilir.
7. Tüm kontroller başarılıysa status VERIFIED yapılır.
8. Emin olunamayan case düzeltilir veya REJECTED yapılır.


## 8. Pilot Dataset

İlk aşamada yaklaşık 10 case oluşturulacaktır.

Pilot dataset'in amacı nihai performans ölçmek değil:

- EvalCase modelinin yeterli olup olmadığını görmek,
- evidence yapısını doğrulamak,
- soru tasarım kurallarını test etmek,
- eksik domain kavramlarını keşfetmektir.

Pilot set farklı soru türleri içermelidir.


## 9. Gold Dataset

Pilot süreç tamamlandıktan sonra yaklaşık 40-60 insan doğrulamalı case
oluşturulması hedeflenmektedir.

Kalite, soru sayısından daha önemlidir.


## 10. Dev ve Holdout Politikası

Gold dataset'in tamamı sistem geliştirme sırasında sürekli kullanılmamalıdır.

DEV SET:

- Chunking geliştirme
- Retrieval geliştirme
- Prompt geliştirme
- Hata analizi

için kullanılabilir.

HOLDOUT / TEST SET:

- Geliştirme sırasında mümkün olduğunca görülmez.
- Milestone sonunda gerçek performans ölçümünde kullanılır.

Amaç benchmark'a overfit olmayı önlemektir.


## Open Domain Discoveries

### Entity / Reporting Scope

Pilot Gold dataset hazırlanırken aynı finansal metriğin farklı
entity ve raporlama kapsamlarında farklı değerler taşıyabildiği görüldü.

Örnekler:

- Akbank sermaye yeterlilik oranı: %19,0
- Akbank AG sermaye yeterlilik oranı: %33,6
- Türk bankacılık sektörü sermaye yeterlilik oranı: %19,7
- Akbank düzenlemeler hariç sermaye yeterlilik oranı: %16,8

Bu nedenle yalnızca `category` alanı, bir metriğin bağlamını
tanımlamak için ileride yetersiz kalabilir.

Değerlendirilecek olası domain alanları:

- `subject` / `entity`
- `reporting_scope`
- metric subtype / metric definition

Pilot dataset tamamlanmadan schema değişikliği yapılmayacaktır.

### Metric Semantics

Aynı finansal konu altında farklı anlam taşıyan değerler bulunabilir.

Örnek:

- Sermaye yeterlilik oranı
- Çekirdek sermaye yeterlilik oranı
- Düzenlemeler hariç sermaye yeterlilik oranı
- Düzenleyici eşik

Bu değerler aynı metric olarak değerlendirilmemelidir.


## Pilot Gold v1 Retrospective

Pilot Gold v1, 10 insan doğrulamalı EvalCase ile tamamlandı.

Bu pilot sırasında mevcut evaluation domain kontratının bazı alanlarda yeterli,
bazı alanlarda ise ileride genişlemeye ihtiyaç duyabileceği görüldü.

### Mevcut kontratın yeterli olduğu alanlar

- Bir EvalCase birden fazla evidence taşıyabiliyor.
- Cross-page evidence, farklı `page` değerleriyle temsil edilebiliyor.
- DIRECT, CALCULATION ve COMPARISON reasoning türleri pilot set için yeterli oldu.

### EvalCase v2 için güçlü aday: tags

Bazı özellikler reasoning türü değildir ancak evaluation sonuçlarını capability
bazında analiz etmek için önemlidir.

Örnek tag adayları:

- `table_heavy`
- `cross_page`
- `multi_evidence`
- `semantic_paraphrase`

Bu nedenle ileride EvalCase'e aşağıdaki gibi bir alan eklenmesi değerlendirilecektir:

`tags: list[str]`

### Açık Domain Keşifleri

Aşağıdaki ihtiyaçlar gerçek doküman üzerinde gözlemlendi ancak henüz domain
kontratına eklenmeyecektir:

- `entity / subject`
  - Akbank
  - Akbank AG
  - AKLease
  - Türk bankacılık sektörü

- `reporting_scope`
  - consolidated
  - unconsolidated
  - subsidiary
  - sector

- metric semantics
  - sermaye yeterlilik oranı
  - çekirdek sermaye yeterlilik oranı
  - düzenlemeler hariç sermaye yeterlilik oranı
  - düzenleyici eşik

- multi-label reasoning ihtiyacı
  - örneğin ileride `CALCULATION + COMPARISON`

Bu alanlar, daha fazla Gold EvalCase üretildikten ve tekrar eden ihtiyaç oldukları
görüldükten sonra domain modeline eklenecektir.

### Tasarım İlkesi

Gerçek eval soruları domain modelini şekillendirmelidir.

Tek bir örnek görüldüğünde hemen yeni abstraction eklemek yerine:

1. İhtiyaç kaydedilir.
2. Yeni Gold case'lerde tekrar edip etmediği gözlemlenir.
3. Tekrar eden ihtiyaçsa domain kontratı genişletilir.
4. Dataset yeni schema sürümüne migrate edilir.