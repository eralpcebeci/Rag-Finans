# ADR-0001: Katmanlı ve arayüz tabanlı mimari

**Durum:** Kabul edildi

**Karar:** Embedder, VectorStore ve LLM soyut arayüzlerin arkasında tutulur (`providers/base.py`).

**Gerekçe:** Proje bir öğrenme laboratuvarı. Parser, embedding modeli, vektör DB ve LLM'i
tek dosyalık değişiklikle takas edip aynı değerlendirme setiyle karşılaştırmak istiyoruz.

**Sonuç:** Framework bağımlılığı (LangChain vb.) yok; her deney `.env` ile yapılandırılır.
