from dataclasses import dataclass, field
from typing import Dict, List, Set
from datetime import datetime


@dataclass
class Entity:
    name: str
    type: str  # "person", "project", "system", "concept"
    attributes: Dict = field(default_factory=dict)
    relationships: Dict = field(default_factory=dict)
    last_mentioned: datetime = field(default_factory=datetime.now)
    mention_count: int = 0
    importance_score: float = 1.0


class EntityMemory:
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[str, Set[str]] = {}

    def extract_and_store_entities(
        self, text: str, conversation_context: Dict = None
    ) -> List[str]:
        """Extract entities from text and store them"""
        # In production, use NER models like spaCy or custom extraction
        # For demo, we'll use simple keyword detection

        entity_patterns = {
            "person": [
                "user",
                "customer",
                "developer",
                "team member",
                "smith",
                "john",
                "jane",
            ],
            "project": ["app", "system", "platform", "service", "website", "api"],
            "technology": [
                "database",
                "postgresql",
                "django",
                "python",
                "redis",
                "aws",
            ],
            "concept": ["bug", "feature", "requirement", "issue", "error", "timeout"],
        }

        found_entities = []
        text_lower = text.lower()

        for entity_type, keywords in entity_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    entity_id = f"{entity_type}_{keyword.replace(' ', '_')}"
                    self._update_entity(entity_id, keyword, entity_type, text)
                    found_entities.append(entity_id)

        return found_entities

    def _update_entity(
        self, entity_id: str, name: str, entity_type: str, context: str
    ) -> None:
        """Update or create entity"""
        if entity_id in self.entities:
            entity = self.entities[entity_id]
            entity.mention_count += 1
            entity.last_mentioned = datetime.now()
            entity.importance_score += 0.1  # Increase importance with mentions

            # Update context in attributes
            if "recent_contexts" not in entity.attributes:
                entity.attributes["recent_contexts"] = []
            entity.attributes["recent_contexts"].append(
                {"context": context[:100], "timestamp": datetime.now().isoformat()}
            )
            # Keep only last 3 contexts
            entity.attributes["recent_contexts"] = entity.attributes["recent_contexts"][
                -3:
            ]
        else:
            entity = Entity(
                name=name,
                type=entity_type,
                attributes={
                    "first_context": context[:100],
                    "recent_contexts": [
                        {
                            "context": context[:100],
                            "timestamp": datetime.now().isoformat(),
                        }
                    ],
                },
                mention_count=1,
            )
            self.entities[entity_id] = entity

    def get_relevant_entities(self, query: str, top_k: int = 5) -> List[Entity]:
        """Get entities relevant to current query"""
        relevant = []
        query_lower = query.lower()

        for entity in self.entities.values():
            relevance_score = 0

            # Name match
            if entity.name.lower() in query_lower:
                relevance_score += 2.0

            # Type relevance
            if entity.type in query_lower:
                relevance_score += 1.0

            # Context relevance (check recent contexts)
            for context_item in entity.attributes.get("recent_contexts", []):
                context_text = context_item.get("context", "").lower()
                # Simple word overlap scoring
                query_words = set(query_lower.split())
                context_words = set(context_text.split())
                overlap = len(query_words.intersection(context_words))
                if overlap > 0:
                    relevance_score += overlap * 0.2

            # Recency boost
            hours_since_mention = (
                datetime.now() - entity.last_mentioned
            ).total_seconds() / 3600
            recency_boost = max(
                0, 1 - (hours_since_mention / 24)
            )  # Decay over 24 hours

            relevance_score += entity.importance_score * recency_boost

            if relevance_score > 0:
                relevant.append((entity, relevance_score))

        # Sort by relevance and return top_k
        relevant.sort(key=lambda x: x[1], reverse=True)
        return [entity for entity, score in relevant[:top_k]]

    def add_relationship(
        self, entity1_id: str, entity2_id: str, relationship_type: str
    ):
        """Add relationship between entities"""
        if entity1_id in self.entities and entity2_id in self.entities:
            # Add to entity relationships
            if entity1_id not in self.relationships:
                self.relationships[entity1_id] = set()
            self.relationships[entity1_id].add(f"{relationship_type}:{entity2_id}")

            # Add reverse relationship
            if entity2_id not in self.relationships:
                self.relationships[entity2_id] = set()
            self.relationships[entity2_id].add(f"related_to:{entity1_id}")

    def get_entity_network(self, entity_id: str) -> Dict:
        """Get entity and its related entities"""
        if entity_id not in self.entities:
            return {}

        entity = self.entities[entity_id]
        related_entities = []

        for relationship in self.relationships.get(entity_id, []):
            rel_type, related_id = relationship.split(":", 1)
            if related_id in self.entities:
                related_entities.append(
                    {"entity": self.entities[related_id], "relationship": rel_type}
                )

        return {"main_entity": entity, "related_entities": related_entities}


def demo_entity_memory():
    entity_memory = EntityMemory()

    print("=== Entity Memory Demo ===")
    print()

    # Simulate conversation with entity extraction
    conversation = [
        "The user mentioned their app has database performance issues",
        "The customer is using PostgreSQL with their Django app",
        "Developer Smith reported a bug in the authentication system",
        "The API service needs optimization for better performance",
        "John from the team fixed the timeout error in the PostgreSQL database",
        "The Django app is now working properly after Smith's bug fix",
    ]

    print("Processing conversation messages...")
    for i, message in enumerate(conversation):
        print(f"{i + 1}. {message}")
        entities = entity_memory.extract_and_store_entities(message)
        print(f"   Found entities: {entities}")
        print()

    # Add some relationships
    entity_memory.add_relationship("person_smith", "concept_bug", "reported")
    entity_memory.add_relationship("person_john", "concept_timeout", "fixed")
    entity_memory.add_relationship("technology_postgresql", "project_app", "used_in")

    print("=== Entity Storage Summary ===")
    for entity_id, entity in entity_memory.entities.items():
        print(
            f"- {entity.name} ({entity.type}): {entity.mention_count} mentions, importance: {entity.importance_score:.2f}"
        )

    print()
    print("=== Query Examples ===")

    # Test queries
    queries = [
        "Help optimize the database performance",
        "Who fixed the authentication bug?",
        "What technology does the app use?",
        "Tell me about recent errors",
    ]

    for query in queries:
        print(f"Query: '{query}'")
        relevant_entities = entity_memory.get_relevant_entities(query)

        if relevant_entities:
            print("Relevant entities:")
            for entity in relevant_entities:
                recent_context = ""
                if entity.attributes.get("recent_contexts"):
                    recent_context = entity.attributes["recent_contexts"][-1]["context"]
                print(
                    f"  - {entity.name} ({entity.type}) - mentioned {entity.mention_count} times"
                )
                print(f"    Recent context: {recent_context}")
        else:
            print("No relevant entities found")
        print()

    print("=== Entity Network Example ===")
    # Show entity network for Smith
    smith_network = entity_memory.get_entity_network("person_smith")
    if smith_network:
        main_entity = smith_network["main_entity"]
        print(f"Entity: {main_entity.name} ({main_entity.type})")
        print("Related entities:")
        for related in smith_network["related_entities"]:
            rel_entity = related["entity"]
            rel_type = related["relationship"]
            print(f"  - {rel_type}: {rel_entity.name} ({rel_entity.type})")

    return entity_memory


if __name__ == "__main__":
    demo_entity_memory()
