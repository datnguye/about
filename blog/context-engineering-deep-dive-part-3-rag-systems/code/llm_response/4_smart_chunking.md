=== LangChain Text Splitter Comparison ===

SmartChunker initialized with LangChain text splitters
✅ Embedding model available for semantic chunking
Original text: 844 characters

CharacterTextSplitter (fixed_size):
------------------------------------------------------------
Chunking general document using fixed_size strategy
Number of chunks: 2
Average chunk size: 414 chars
Chunk boundaries:
  1. 'Natural Language Processing (NLP) is a s...' to '...ention mechanisms to understand context.'
  2. 'Applications of NLP are widespread. They...' to '...ted language understanding capabilities.'

RecursiveCharacterTextSplitter (content_aware):
------------------------------------------------------------
Chunking general document using content_aware strategy
Number of chunks: 1
Average chunk size: 834 chars
Chunk boundaries:
  1. 'Natural Language Processing (NLP) is a s...' to '...ted language understanding capabilities.'

TokenTextSplitter (token_based):
------------------------------------------------------------
Chunking general document using token_based strategy
Number of chunks: 1
Average chunk size: 844 chars
Chunk boundaries:
  1. 'Natural Language Processing (NLP) i...' to '...anguage understanding capabilities.'

SemanticChunker (semantic):
------------------------------------------------------------
Chunking general document using semantic strategy
Number of chunks: 13
Average chunk size: 60 chars
Chunk boundaries:
  1. 'Natural Language Processing (NLP) is a s...' to '...is a subfield of artificial intelligence'
  2. 'It focuses on enabling computers to unde...' to '...to understand and process human language'
  3. 'Key NLP techniques include tokenization,...' to '...ch tagging, and named entity recognition'
  4. 'These form the foundation for more compl...' to '...rm the foundation for more complex tasks'
  5. 'Modern NLP relies heavily on transformer...' to '...NLP relies heavily on transformer models'
  6. 'Models like BERT and GPT have revolution...' to '...RT and GPT have revolutionized the field'
  7. 'They use attention mechanisms to underst...' to '...tention mechanisms to understand context'
  8. 'Applications of NLP are widespread...' to '...Applications of NLP are widespread'
  9. 'They include machine translation, sentim...' to '...lation, sentiment analysis, and chatbots'
  10. 'These tools help bridge the gap between...' to '...communication and computer understanding'
  11. 'The future of NLP looks promising...' to '...The future of NLP looks promising'
  12. 'Advances in deep learning continue to im...' to '...learning continue to improve performance'
  13. 'We can expect even more sophisticated la...' to '...ated language understanding capabilities'


=== Document Type-Specific Chunking ===

SmartChunker initialized with LangChain text splitters
✅ Embedding model available for semantic chunking
CODE Document:
==================================================
Document type: code
Total chunks: 1
Chunk sizes: [1106] characters
Average size: 1106 chars
First chunk preview: def fibonacci(n):     """Calculate nth Fibonacci number using recursion"""     if n <= 0:         return 0     elif n == 1:         return 1     else:...

MARKDOWN Document:
==================================================
Document type: markdown
Total chunks: 8
Chunk sizes: [81, 74, 176, 56, 75, 83, 58, 168] characters
Average size: 96 chars
First chunk preview: The first step in any ML pipeline is collecting high-quality data. This involves:...

LEGAL Document:
==================================================
Document type: legal
Total chunks: 1
Chunk sizes: [1474] characters
Average size: 1474 chars
First chunk preview: ## Terms of Service Agreement  ### Section 1: Acceptance of Terms By accessing and using this service, you accept and agree to be bound by the terms a...

