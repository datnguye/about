from enum import Enum
from typing import Set, Optional, Dict, List
import hashlib
import re
from datetime import datetime, timedelta


class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    PERSONAL = "personal"


class PrivacyCompliantMemory:
    def __init__(self):
        self.memories: Dict[str, Dict] = {}
        self.user_consent: Dict[str, Set[str]] = {}  # user_id -> consent types
        self.retention_policies: Dict[str, timedelta] = {
            DataClassification.PUBLIC.value: timedelta(days=365),
            DataClassification.INTERNAL.value: timedelta(days=180),
            DataClassification.CONFIDENTIAL.value: timedelta(days=90),
            DataClassification.PERSONAL.value: timedelta(days=30),
        }
        self.deletion_log: List[Dict] = []

    def store_memory(
        self,
        user_id: str,
        content: str,
        classification: DataClassification,
        consent_type: str = "analytics",
    ) -> Optional[str]:
        """Store memory with privacy controls"""

        # Check consent
        if not self._has_consent(user_id, consent_type):
            print(
                f"❌ Storage denied: User {user_id} has not consented to {consent_type}"
            )
            return None

        # Hash PII if needed
        original_content = content
        if classification == DataClassification.PERSONAL:
            content = self._anonymize_content(content)
            print(f"🔒 Anonymized personal data: '{original_content}' -> '{content}'")

        memory_id = self._generate_memory_id(user_id, content)

        self.memories[memory_id] = {
            "user_id": user_id,
            "content": content,
            "original_content": original_content,  # Keep for demo purposes
            "classification": classification.value,
            "consent_type": consent_type,
            "created_at": datetime.now(),
            "expires_at": datetime.now()
            + self.retention_policies[classification.value],
        }

        print(f"✅ Stored memory {memory_id[:12]}... ({classification.value})")
        return memory_id

    def _has_consent(self, user_id: str, consent_type: str) -> bool:
        """Check if user has given consent for data processing"""
        return (
            user_id in self.user_consent and consent_type in self.user_consent[user_id]
        )

    def _anonymize_content(self, content: str) -> str:
        """Remove or hash PII from content"""
        # In production, use proper PII detection and anonymization
        # This is a simplified example

        # Remove email addresses
        content = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", content
        )

        # Remove phone numbers
        content = re.sub(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]", content)

        # Remove potential names (simple heuristic)
        content = re.sub(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "[NAME]", content)

        # Remove credit card numbers (simple pattern)
        content = re.sub(
            r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CREDIT_CARD]", content
        )

        return content

    def _generate_memory_id(self, user_id: str, content: str) -> str:
        """Generate deterministic but non-reversible ID"""
        combined = f"{user_id}:{content}:{datetime.now().date()}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def grant_consent(self, user_id: str, consent_types: Set[str]) -> None:
        """Grant user consent for data processing"""
        if user_id not in self.user_consent:
            self.user_consent[user_id] = set()

        new_consents = consent_types - self.user_consent[user_id]
        self.user_consent[user_id].update(consent_types)

        if new_consents:
            print(f"✅ Granted consent for {user_id}: {', '.join(new_consents)}")

    def revoke_consent(self, user_id: str, consent_type: str) -> int:
        """Revoke consent and delete related memories"""
        if user_id in self.user_consent:
            self.user_consent[user_id].discard(consent_type)

        # Delete memories that relied on this consent
        to_delete = [
            memory_id
            for memory_id, memory in self.memories.items()
            if memory["user_id"] == user_id and memory["consent_type"] == consent_type
        ]

        for memory_id in to_delete:
            self._delete_memory(memory_id, reason="consent_revoked")

        print(
            f"🗑️ Revoked {consent_type} consent for {user_id}: {len(to_delete)} memories deleted"
        )
        return len(to_delete)

    def right_to_be_forgotten(self, user_id: str) -> Dict[str, int]:
        """GDPR Article 17: Right to erasure"""
        memories_deleted = 0

        # Find all memories for this user
        user_memories = [
            memory_id
            for memory_id, memory in self.memories.items()
            if memory["user_id"] == user_id
        ]

        # Delete all memories
        for memory_id in user_memories:
            self._delete_memory(memory_id, reason="right_to_be_forgotten")
            memories_deleted += 1

        # Remove consent records
        if user_id in self.user_consent:
            del self.user_consent[user_id]

        result = {
            "user_id": user_id,
            "memories_deleted": memories_deleted,
            "deletion_timestamp": datetime.now().isoformat(),
        }

        print(
            f"🔥 Right to be forgotten executed for {user_id}: {memories_deleted} memories deleted"
        )
        return result

    def _delete_memory(self, memory_id: str, reason: str) -> None:
        """Delete memory with audit trail"""
        if memory_id in self.memories:
            # Log deletion for audit
            self.deletion_log.append(
                {
                    "memory_id": memory_id,
                    "reason": reason,
                    "deleted_at": datetime.now().isoformat(),
                    "user_id": self.memories[memory_id]["user_id"],
                    "classification": self.memories[memory_id]["classification"],
                }
            )

            # Actually delete
            del self.memories[memory_id]

    def cleanup_expired_memories(self) -> int:
        """Remove memories past their retention period"""
        now = datetime.now()
        expired = [
            memory_id
            for memory_id, memory in self.memories.items()
            if memory["expires_at"] < now
        ]

        for memory_id in expired:
            self._delete_memory(memory_id, reason="retention_period_expired")

        if expired:
            print(f"🕰️ Cleaned up {len(expired)} expired memories")

        return len(expired)

    def get_user_data_export(self, user_id: str) -> Dict:
        """GDPR Article 20: Right to data portability"""
        user_memories = {
            memory_id: {
                **memory,
                "created_at": memory["created_at"].isoformat(),
                "expires_at": memory["expires_at"].isoformat(),
            }
            for memory_id, memory in self.memories.items()
            if memory["user_id"] == user_id
        }

        export_data = {
            "user_id": user_id,
            "export_timestamp": datetime.now().isoformat(),
            "consent_status": list(self.user_consent.get(user_id, set())),
            "memories": user_memories,
            "deletion_history": [
                log for log in self.deletion_log if log["user_id"] == user_id
            ],
        }

        print(f"📤 Data export generated for {user_id}: {len(user_memories)} memories")
        return export_data

    def get_privacy_compliance_report(self) -> Dict:
        """Generate privacy compliance report"""
        now = datetime.now()

        # Classification breakdown
        classification_stats = {}
        consent_stats = {}
        retention_stats = {"expired": 0, "expiring_soon": 0, "fresh": 0}

        for memory in self.memories.values():
            # Classification
            classification = memory["classification"]
            classification_stats[classification] = (
                classification_stats.get(classification, 0) + 1
            )

            # Consent types
            consent_type = memory["consent_type"]
            consent_stats[consent_type] = consent_stats.get(consent_type, 0) + 1

            # Retention status
            days_until_expiry = (memory["expires_at"] - now).days
            if days_until_expiry < 0:
                retention_stats["expired"] += 1
            elif days_until_expiry < 30:
                retention_stats["expiring_soon"] += 1
            else:
                retention_stats["fresh"] += 1

        return {
            "total_memories": len(self.memories),
            "total_users": len(self.user_consent),
            "classification_breakdown": classification_stats,
            "consent_breakdown": consent_stats,
            "retention_status": retention_stats,
            "deletion_events": len(self.deletion_log),
            "report_timestamp": now.isoformat(),
        }


def demo_privacy_compliance():
    print("=== Privacy-Compliant Memory Demo ===")

    privacy_memory = PrivacyCompliantMemory()

    # Grant consent for different users
    print("\n--- Granting User Consent ---")
    privacy_memory.grant_consent("user123", {"analytics", "personalization"})
    privacy_memory.grant_consent("user456", {"analytics"})
    privacy_memory.grant_consent("user789", {"personalization", "marketing"})

    # Store different types of memories
    print("\n--- Storing Memories with Privacy Controls ---")
    memory_examples = [
        (
            "user123",
            "User prefers dark mode",
            DataClassification.PERSONAL,
            "personalization",
        ),
        (
            "user123",
            "User asked about Python tutorials",
            DataClassification.INTERNAL,
            "analytics",
        ),
        (
            "user123",
            "Contact: john.doe@email.com for follow-up",
            DataClassification.PERSONAL,
            "personalization",
        ),
        (
            "user456",
            "Public FAQ: How to install Python",
            DataClassification.PUBLIC,
            "analytics",
        ),
        (
            "user456",
            "User prefers email notifications",
            DataClassification.PERSONAL,
            "personalization",
        ),  # Should fail
        (
            "user789",
            "Customer interested in premium features",
            DataClassification.CONFIDENTIAL,
            "marketing",
        ),
        (
            "user789",
            "Phone number: 555-123-4567 for support",
            DataClassification.PERSONAL,
            "personalization",
        ),
    ]

    stored_count = 0
    for user_id, content, classification, consent_type in memory_examples:
        memory_id = privacy_memory.store_memory(
            user_id, content, classification, consent_type
        )
        if memory_id:
            stored_count += 1

    print(
        f"\n✅ Successfully stored {stored_count} out of {len(memory_examples)} memories"
    )

    # Show initial compliance report
    print("\n--- Initial Privacy Compliance Report ---")
    report = privacy_memory.get_privacy_compliance_report()
    for key, value in report.items():
        if isinstance(value, dict):
            print(f"{key.replace('_', ' ').title()}:")
            for subkey, subvalue in value.items():
                print(f"  - {subkey}: {subvalue}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

    # Demonstrate GDPR requests
    print("\n--- GDPR Compliance Demonstrations ---")

    # 1. Data export (Article 20)
    print("\n1. Right to Data Portability (Article 20)")
    export_data = privacy_memory.get_user_data_export("user123")
    print("   Exported data contains:")
    print(f"   - {len(export_data['memories'])} memories")
    print(f"   - Consent status: {export_data['consent_status']}")
    print(f"   - Deletion history: {len(export_data['deletion_history'])} events")

    # 2. Consent revocation
    print("\n2. Consent Revocation")
    revoked_count = privacy_memory.revoke_consent("user123", "personalization")
    print(f"   Result: {revoked_count} memories deleted due to consent revocation")

    # 3. Right to be forgotten (Article 17)
    print("\n3. Right to be Forgotten (Article 17)")
    forgotten_result = privacy_memory.right_to_be_forgotten("user456")
    print(
        f"   Result: {forgotten_result['memories_deleted']} memories completely erased"
    )

    # 4. Automatic retention cleanup
    print("\n4. Automatic Retention Policy Enforcement")

    # Simulate some memories expiring (for demo, we'll manually expire some)
    for memory_id, memory in list(privacy_memory.memories.items()):
        if memory["classification"] == "personal":
            # Make personal data expire (simulate time passing)
            memory["expires_at"] = datetime.now() - timedelta(days=1)

    expired_count = privacy_memory.cleanup_expired_memories()
    print(
        f"   Result: {expired_count} memories automatically deleted due to retention policies"
    )

    # Final compliance report
    print("\n--- Final Privacy Compliance Report ---")
    final_report = privacy_memory.get_privacy_compliance_report()
    for key, value in final_report.items():
        if isinstance(value, dict):
            print(f"{key.replace('_', ' ').title()}:")
            for subkey, subvalue in value.items():
                print(f"  - {subkey}: {subvalue}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

    # Show deletion audit log
    print("\n--- Deletion Audit Log ---")
    for i, log_entry in enumerate(
        privacy_memory.deletion_log[-5:], 1
    ):  # Last 5 entries
        print(f"{i}. {log_entry['deleted_at'][:19]} - {log_entry['reason']}")
        print(
            f"   Memory: {log_entry['memory_id'][:12]}... ({log_entry['classification']})"
        )
        print(f"   User: {log_entry['user_id']}")

    print(f"\nTotal audit entries: {len(privacy_memory.deletion_log)}")

    return privacy_memory


def demo_anonymization_techniques():
    """Demonstrate PII anonymization"""
    print("\n=== PII Anonymization Demo ===")

    privacy_memory = PrivacyCompliantMemory()

    test_texts = [
        "Contact John Smith at john.smith@company.com or 555-123-4567",
        "Credit card 4532-1234-5678-9012 was used for payment",
        "Jane Doe from accounting called about the invoice",
        "Email support@company.com for technical issues",
        "Customer phone: 1-800-555-0199 for urgent matters",
    ]

    print("Original -> Anonymized:")
    for text in test_texts:
        anonymized = privacy_memory._anonymize_content(text)
        print(f"'{text}'")
        print(f"  -> '{anonymized}'")
        print()


if __name__ == "__main__":
    demo_privacy_compliance()
    demo_anonymization_techniques()
