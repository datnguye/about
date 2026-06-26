LIGHTRAG GRAPH RAG DEMONSTRATION
Using DeepSeek API for LLM and Local Embeddings
INFO:nano-vectordb:Init {'embedding_dim': 384, 'metric': 'cosine', 'storage_file': './lightrag_demo/vdb_entities.json'} 0 data
INFO:nano-vectordb:Init {'embedding_dim': 384, 'metric': 'cosine', 'storage_file': './lightrag_demo/vdb_relationships.json'} 0 data
INFO:nano-vectordb:Init {'embedding_dim': 384, 'metric': 'cosine', 'storage_file': './lightrag_demo/vdb_chunks.json'} 0 data
Rerank is enabled but no rerank_model_func provided. Reranking will be skipped.
✓ LightRAG initialized at ./lightrag_demo
Building knowledge graph from 5 documents...
✓ Knowledge graph built

Testing Graph RAG Query Modes:

Query (local): 'Who developed the core algorithms for SmartAnalytics?'

Answer: Lisa Wang developed the core machine learning algorithms for SmartAnalytics. She serves as the Lead ML Engineer on the SmartAnalytics team and her algorithmic innovations have been instrumental in the platform's success, contributing significantly to TechCorp's revenue growth and reducing data processing time for major clients.

**References:**  
[KG] unknown_source  
[DC] unknown_source

Query (global): 'How did the Series B funding impact TechCorp's growth strategy?'

Answer: Based on the provided knowledge base, the Series B funding had a significant impact on TechCorp's growth strategy across multiple dimensions:

## Strategic Expansion and Development

The $50 million Series B funding, secured in Q3 2023 and led by VentureCapital Partners, was critical for TechCorp's growth strategy. This funding enabled the company to pursue strategic expansion initiatives that were central to their development plans.

## Engineering Capability Enhancement

A major impact was the significant expansion of TechCorp's engineering capabilities. The funding allowed the company to grow its engineering team from 15 to 45 engineers under VP of Engineering Mike Johnson's leadership. This enhanced technical capacity directly supported the company's product development goals.

## Market Expansion and Product Development

The Series B funding is being strategically invested to expand SmartAnalytics into European markets. Additionally, the funding supports the development of SmartAnalytics 2.0 with advanced predictive analytics features, led by Lisa Wang's team. This product evolution is projected to double the company's revenue by 2025.

## Supporting Revenue Growth Trajectory

The funding builds upon TechCorp's impressive revenue growth, which increased from $5 million in 2021 to $25 million in 2023. By enabling both market expansion and product innovation, the Series B funding positions the company to continue this strong growth trajectory.

**References:**
[KG] unknown_source (Growth Strategy-Series B Funding relationship)
[KG] unknown_source (Engineering Capabilities expansion)
[DC] unknown_source (European market expansion and SmartAnalytics 2.0 development)
[DC] unknown_source (Engineering team growth details)
[KG] unknown_source (Revenue growth context)

Query (hybrid): 'What's the connection between Sarah Chen and the company's revenue growth?'

Answer: Based on the provided knowledge base, Sarah Chen's connection to TechCorp's revenue growth is primarily through her leadership role and strategic initiatives that have enabled the company's expansion and financial success.

Sarah Chen serves as CEO of TechCorp and has been instrumental in securing critical funding for the company's growth. She successfully secured $50 million in Series B funding led by VentureCapital Partners in Q3 2023, which was described as "critical for the company's growth strategy." This funding has enabled significant expansion of engineering capabilities and is being strategically invested to expand SmartAnalytics into European markets.

While the knowledge base doesn't directly attribute specific revenue growth numbers to Sarah Chen's actions, it shows she created the conditions for growth by recruiting key talent (including Mike Johnson from CloudNet in 2021) and securing the substantial funding that supports the company's expansion plans. The revenue growth itself (from $5 million in 2021 to $25 million in 2023) is attributed to algorithmic innovations in SmartAnalytics developed by Lisa Wang's team.

**References:**
[KG] unknown_source (Sarah Chen entity description and relationships)
[KG] unknown_source (Series B Funding entity description)
[DC] unknown_source (Document chunk 1 - Sarah Chen's leadership and funding)
[DC] unknown_source (Document chunk 3 - Strategic investment of funding)
[KG] unknown_source (Revenue Growth entity description)

Comparing Query Modes:

Question: 'How did Sarah Chen's leadership decisions impact TechCorp's success?'

Local: Based on the provided knowledge base, Sarah Chen's leadership decisions had significant positive impacts on TechCorp's success through strategic hiring, funding acquisition, and product development.

## Strategic Recruitment and Team Building

Sarah Chen recruited Mike Johnson from CloudNet in 2021 ...

Global: Based on the provided knowledge base, Sarah Chen's leadership decisions significantly impacted TechCorp's success through strategic hiring, funding acquisition, and overall company direction.

**Strategic Hiring and Team Building**
Sarah Chen recruited Mike Johnson from CloudNet in 2021 to lead Tech...

Hybrid: Based on the provided knowledge base, Sarah Chen's leadership decisions had significant positive impacts on TechCorp's success through strategic hiring, funding acquisition, and product development.

**Strategic Recruitment and Team Building**
Sarah Chen recruited Mike Johnson from CloudNet in 2021 ...
