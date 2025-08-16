"""
Role-Playing Prompts: Creating specialized expert personas

This script demonstrates how detailed role definitions dramatically
improve output quality compared to generic "expert" prompts.
"""

from os import getenv

from dotenv import load_dotenv
from litellm import completion

def blue_print(text):
    """Print text in blue color"""
    print(f"\033[94m{text}\033[0m")

# Load environment variables
load_dotenv()

def create_expert_analyzer(expertise_level: str = "senior"):
    """Create specialized SQL analyzer with detailed role definition"""

    roles = {
        "junior": """You are a junior developer learning SQL best practices.
        You focus on basic correctness and readability.
        You ask clarifying questions when unsure.""",

        "senior": """You are a senior database architect with 15 years optimizing Fortune 500 databases.
        You've worked with systems handling millions of records daily.
        You consider performance, maintainability, and scalability in every recommendation.""",

        "security": """You are a database security specialist focused on SQL injection prevention.
        You've seen countless breaches caused by poor SQL practices.
        Security is your top priority, followed by performance.""",

        "consultant": """You are a database consultant who bills $300/hour.
        Clients expect practical, business-focused solutions that save money.
        You always consider the business impact of your technical recommendations."""
    }

    def analyze(query: str, context: str = "") -> str:
        system_prompt = f"""
        {roles.get(expertise_level, roles['senior'])}
        
        Your approach:
        - Identify issues before suggesting fixes
        - Explain trade-offs, not just solutions
        - Consider the business context
        - Provide actionable recommendations
        
        Response format:
        1. ISSUES FOUND: [list]
        2. IMPACT: [business impact]
        3. RECOMMENDATIONS: [specific fixes]
        4. ALTERNATIVE APPROACHES: [if applicable]
        """

        response = completion(
            model="openrouter/openai/gpt-oss-20b:free",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            temperature=0.3
        )

        return response["choices"][0]["message"]["content"]

    return analyze

def create_industry_specialist(industry: str):
    """Create industry-specific database expert"""

    industry_contexts = {
        "ecommerce": """You are a database architect specializing in e-commerce platforms.
        You've scaled systems from startup to handling Black Friday traffic.
        You understand inventory management, order processing, and customer analytics.
        Performance during peak shopping periods is critical.""",

        "fintech": """You are a financial technology database expert.
        You've worked with trading systems requiring microsecond latency.
        Compliance (SOX, PCI-DSS) and audit trails are non-negotiable.
        Data consistency and ACID properties are paramount.""",

        "healthcare": """You are a healthcare database specialist.
        You understand HIPAA compliance and patient data protection.
        Uptime is critical - lives depend on system availability.
        Data integrity and audit trails are legally required.""",

        "gaming": """You are a database engineer for online gaming platforms.
        You've handled millions of concurrent players and real-time leaderboards.
        Low latency and high availability are essential for player experience.
        Anti-cheat measures and data analytics drive your decisions."""
    }

    def analyze_for_industry(query: str, context: str = "") -> str:
        system_prompt = f"""
        {industry_contexts.get(industry, industry_contexts['ecommerce'])}
        
        Consider industry-specific requirements:
        - Regulatory compliance
        - Performance characteristics
        - Business criticality
        - Risk tolerance
        
        Provide recommendations that fit this industry context.
        """

        response = completion(
            model="openrouter/openai/gpt-oss-20b:free",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            temperature=0.2
        )

        return response["choices"][0]["message"]["content"]

    return analyze_for_industry

def demonstrate_role_differences():
    """Compare how different roles analyze the same query"""

    vulnerable_query = "SELECT * FROM users WHERE username = '" + "user_input" + "'"
    context = "Public-facing login system with 10M users"

    print("=== ROLE-BASED ANALYSIS COMPARISON ===\n")
    print(f"Query: {vulnerable_query}")
    print(f"Context: {context}")
    print("="*60)

    roles = ["junior", "senior", "security", "consultant"]

    for role in roles:
        print(f"\n--- {role.upper()} PERSPECTIVE ---")
        analyzer = create_expert_analyzer(role)
        try:
            result = analyzer(vulnerable_query, context)
            blue_print(result)
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 40)

def demonstrate_industry_perspectives():
    """Show how industry context changes recommendations"""

    query = """
    SELECT user_id, COUNT(*) as transaction_count, SUM(amount) as total_amount
    FROM transactions 
    WHERE created_at > NOW() - INTERVAL 1 DAY
    GROUP BY user_id
    HAVING total_amount > 10000
    """

    context = "Daily suspicious activity report"

    print("=== INDUSTRY-SPECIFIC ANALYSIS ===\n")
    print(f"Query: {query}")
    print(f"Context: {context}")
    print("="*60)

    industries = ["fintech", "ecommerce", "gaming", "healthcare"]

    for industry in industries:
        print(f"\n--- {industry.upper()} INDUSTRY ---")
        analyzer = create_industry_specialist(industry)
        try:
            result = analyzer(query, context)
            blue_print(result)
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 40)

def create_persona_with_background(name: str, background: dict):
    """Create a detailed persona with specific background"""

    def analyze_with_persona(query: str, context: str = "") -> str:
        persona_prompt = f"""
        You are {name}, a {background['title']} at {background['company']}.
        
        Background:
        - Experience: {background['experience']}
        - Specialties: {', '.join(background['specialties'])}
        - Previous roles: {', '.join(background['previous_roles'])}
        - Notable achievements: {background['achievements']}
        
        Your personality:
        - Communication style: {background['style']}
        - Risk tolerance: {background['risk_tolerance']}
        - Primary concerns: {', '.join(background['concerns'])}
        
        Approach this analysis as {name} would, considering your background and personality.
        """

        response = completion(
            model="openrouter/openai/gpt-oss-20b:free",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=[
                {"role": "system", "content": persona_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            temperature=0.4  # Slightly higher for personality
        )

        return response["choices"][0]["message"]["content"]

    return analyze_with_persona

def demonstrate_detailed_personas():
    """Show how detailed personas affect analysis"""

    query = "SELECT * FROM user_activity WHERE session_duration > 3600"
    context = "Analyzing user engagement patterns"

    personas = {
        "Alex Chen": {
            "title": "Senior Data Engineer",
            "company": "TechCorp",
            "experience": "12 years in high-scale systems",
            "specialties": ["Real-time analytics", "Stream processing", "Data pipelines"],
            "previous_roles": ["Netflix", "Uber", "Airbnb"],
            "achievements": "Built analytics platform handling 1B events/day",
            "style": "Direct and practical, focuses on scalability",
            "risk_tolerance": "Conservative with production changes",
            "concerns": ["Performance", "Reliability", "Cost optimization"]
        },
        "Morgan Taylor": {
            "title": "Lead Security Engineer",
            "company": "SecureFinance",
            "experience": "8 years in financial services security",
            "specialties": ["SQL injection prevention", "Data privacy", "Compliance"],
            "previous_roles": ["JPMorgan Chase", "Goldman Sachs"],
            "achievements": "Zero security incidents in 3 years",
            "style": "Methodical and thorough, questions everything",
            "risk_tolerance": "Extremely risk-averse",
            "concerns": ["Security", "Compliance", "Audit trails"]
        }
    }

    print("=== DETAILED PERSONA ANALYSIS ===\n")
    print(f"Query: {query}")
    print(f"Context: {context}")
    print("="*60)

    for name, background in personas.items():
        print(f"\n--- {name.upper()} ({background['title']}) ---")
        analyzer = create_persona_with_background(name, background)
        try:
            result = analyzer(query, context)
            blue_print(result)
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 40)

if __name__ == "__main__":
    print("Role-Playing Prompts Demo\n")

    # Compare different expertise levels
    demonstrate_role_differences()

    print("\n" + "="*80 + "\n")

    # Compare industry perspectives
    demonstrate_industry_perspectives()

    print("\n" + "="*80 + "\n")

    # Detailed persona demonstration
    demonstrate_detailed_personas()
