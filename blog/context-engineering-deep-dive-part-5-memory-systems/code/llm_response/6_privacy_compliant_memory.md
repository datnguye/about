=== Privacy-Compliant Memory Demo ===

--- Granting User Consent ---
✅ Granted consent for user123: analytics, personalization
✅ Granted consent for user456: analytics
✅ Granted consent for user789: marketing, personalization

--- Storing Memories with Privacy Controls ---
🔒 Anonymized personal data: 'User prefers dark mode' -> 'User prefers dark mode'
✅ Stored memory efa27aeb96cc... (personal)
✅ Stored memory 2535b28a614a... (internal)
🔒 Anonymized personal data: 'Contact: john.doe@email.com for follow-up' -> 'Contact: [EMAIL] for follow-up'
✅ Stored memory 816e8334dd9d... (personal)
✅ Stored memory d0add335864b... (public)
❌ Storage denied: User user456 has not consented to personalization
✅ Stored memory 8360e692bc1f... (confidential)
🔒 Anonymized personal data: 'Phone number: 555-123-4567 for support' -> 'Phone number: [PHONE] for support'
✅ Stored memory ece0fac306f3... (personal)

✅ Successfully stored 6 out of 7 memories

--- Initial Privacy Compliance Report ---
Total Memories: 6
Total Users: 3
Classification Breakdown:
  - personal: 3
  - internal: 1
  - public: 1
  - confidential: 1
Consent Breakdown:
  - personalization: 3
  - analytics: 2
  - marketing: 1
Retention Status:
  - expired: 0
  - expiring_soon: 3
  - fresh: 3
Deletion Events: 0
Report Timestamp: 2025-08-22T21:44:41.361845

--- GDPR Compliance Demonstrations ---

1. Right to Data Portability (Article 20)
📤 Data export generated for user123: 3 memories
   Exported data contains:
   - 3 memories
   - Consent status: ['analytics', 'personalization']
   - Deletion history: 0 events

2. Consent Revocation
🗑️ Revoked personalization consent for user123: 2 memories deleted
   Result: 2 memories deleted due to consent revocation

3. Right to be Forgotten (Article 17)
🔥 Right to be forgotten executed for user456: 1 memories deleted
   Result: 1 memories completely erased

4. Automatic Retention Policy Enforcement
🕰️ Cleaned up 1 expired memories
   Result: 1 memories automatically deleted due to retention policies

--- Final Privacy Compliance Report ---
Total Memories: 2
Total Users: 2
Classification Breakdown:
  - internal: 1
  - confidential: 1
Consent Breakdown:
  - analytics: 1
  - marketing: 1
Retention Status:
  - expired: 0
  - expiring_soon: 0
  - fresh: 2
Deletion Events: 4
Report Timestamp: 2025-08-22T21:44:41.361884

--- Deletion Audit Log ---
1. 2025-08-22T21:44:41 - consent_revoked
   Memory: efa27aeb96cc... (personal)
   User: user123
2. 2025-08-22T21:44:41 - consent_revoked
   Memory: 816e8334dd9d... (personal)
   User: user123
3. 2025-08-22T21:44:41 - right_to_be_forgotten
   Memory: d0add335864b... (public)
   User: user456
4. 2025-08-22T21:44:41 - retention_period_expired
   Memory: ece0fac306f3... (personal)
   User: user789

Total audit entries: 4

=== PII Anonymization Demo ===
Original -> Anonymized:
'Contact John Smith at john.smith@company.com or 555-123-4567'
  -> '[NAME] Smith at [EMAIL] or [PHONE]'

'Credit card 4532-1234-5678-9012 was used for payment'
  -> 'Credit card [CREDIT_CARD] was used for payment'

'Jane Doe from accounting called about the invoice'
  -> '[NAME] from accounting called about the invoice'

'Email support@company.com for technical issues'
  -> 'Email [EMAIL] for technical issues'

'Customer phone: 1-800-555-0199 for urgent matters'
  -> 'Customer phone: 1-[PHONE] for urgent matters'

