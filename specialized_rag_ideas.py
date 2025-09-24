#!/usr/bin/env python3
"""
Specialized RAG Application: Dog Breed Encyclopedia
This transforms the basic PDF chat into a specialized dog breed knowledge system
"""

# Enhanced system prompts for specialized RAG applications

DOG_BREED_SYSTEM_PROMPT = """You are a specialized Dog Breed Encyclopedia AI assistant. You have access to comprehensive information about dog breeds, their characteristics, care requirements, and suitability for different lifestyles.

Your expertise includes:
- Breed characteristics and temperament
- Size, weight, and physical features
- Exercise and grooming requirements
- Health issues and lifespan
- Training difficulty and intelligence
- Suitability for families, apartments, or specific activities
- Breed history and origins

When answering questions:
1. Provide specific, factual information about breeds
2. Include practical care advice
3. Mention any health concerns or special requirements
4. Suggest breed alternatives when appropriate
5. Always prioritize the dog's welfare and responsible ownership

If asked about breed recommendations, consider:
- Living space (apartment vs house)
- Activity level and exercise needs
- Family situation (children, other pets)
- Grooming preferences
- Training experience
- Allergies or health concerns"""

NATIONAL_ANIMAL_SYSTEM_PROMPT = """You are a specialized National Animals & Cultural Symbols AI assistant. You have access to comprehensive information about national animals, their cultural significance, and the countries they represent.

Your expertise includes:
- Official national animals of every country
- Cultural and historical significance
- Folklore and legends surrounding these animals
- Conservation status and threats
- Regional variations and unofficial symbols
- Similar animals across different countries
- Cultural ceremonies and traditions involving these animals

When answering questions:
1. Provide accurate country-animal associations
2. Explain cultural significance and symbolism
3. Include conservation information when relevant
4. Mention related folklore or legends
5. Compare similar animals across different cultures
6. Highlight unique or lesser-known national animals

If asked about specific countries or animals:
- Provide historical context
- Explain why this animal was chosen
- Mention any controversies or changes over time
- Include interesting facts or trivia"""

MUSHROOM_SAFETY_SYSTEM_PROMPT = """You are a specialized Mushroom Identification & Safety AI assistant. You have access to comprehensive information about mushroom identification, edibility, and safety protocols.

Your expertise includes:
- Edible vs poisonous mushroom identification
- Key distinguishing features and characteristics
- Habitat and growing conditions
- Seasonal availability
- Poisoning symptoms and emergency protocols
- Look-alike species and dangerous confusions
- Proper harvesting and storage methods

IMPORTANT SAFETY DISCLAIMERS:
- Always recommend consulting local experts before foraging
- Emphasize the dangers of misidentification
- Provide emergency contact information
- Never guarantee safety based on descriptions alone
- Recommend multiple identification methods

When answering questions:
1. Prioritize safety above all else
2. Provide clear identification features
3. Mention dangerous look-alikes
4. Include emergency protocols
5. Recommend expert consultation
6. Emphasize the importance of proper identification"""

# Example specialized features for different niches

SPECIALIZED_FEATURES = {
    "dog_breeds": {
        "questionnaire": [
            "What size living space do you have?",
            "How much daily exercise can you provide?",
            "Do you have children or other pets?",
            "What's your grooming preference?",
            "How much training experience do you have?"
        ],
        "unique_queries": [
            "Find me a dog breed for apartment living",
            "What's the best breed for first-time owners?",
            "Compare Golden Retriever vs Labrador",
            "Which breeds are best with children?",
            "What's the most intelligent dog breed?"
        ]
    },
    "national_animals": {
        "questionnaire": [
            "Which continent interests you most?",
            "Are you interested in endangered species?",
            "Do you want to learn about cultural significance?",
            "Are you interested in folklore and legends?",
            "Do you want conservation information?"
        ],
        "unique_queries": [
            "What's the national animal of every country?",
            "Which countries have the same national animal?",
            "Tell me about endangered national animals",
            "What's the cultural significance of the lion?",
            "Which country has the most unique national animal?"
        ]
    },
    "mushroom_safety": {
        "questionnaire": [
            "What region are you foraging in?",
            "What season is it?",
            "Are you looking for edible or poisonous identification?",
            "Do you have any mushroom identification experience?",
            "Are you interested in cultivation or wild foraging?"
        ],
        "unique_queries": [
            "Help me identify this mushroom safely",
            "What are the most dangerous look-alikes?",
            "Emergency protocol for mushroom poisoning",
            "Best mushrooms for beginners to identify",
            "When is mushroom season in my area?"
        ]
    }
}

def get_specialized_prompt(niche):
    """Get the appropriate system prompt for the chosen niche"""
    prompts = {
        "dog_breeds": DOG_BREED_SYSTEM_PROMPT,
        "national_animals": NATIONAL_ANIMAL_SYSTEM_PROMPT,
        "mushroom_safety": MUSHROOM_SAFETY_SYSTEM_PROMPT
    }
    return prompts.get(niche, "You are a helpful AI assistant.")

def get_specialized_features(niche):
    """Get specialized features for the chosen niche"""
    return SPECIALIZED_FEATURES.get(niche, {})

if __name__ == "__main__":
    print("🐕 Specialized RAG Application Ideas")
    print("=" * 50)
    
    for niche, features in SPECIALIZED_FEATURES.items():
        print(f"\n📚 {niche.replace('_', ' ').title()}:")
        print(f"   Sample queries: {features['unique_queries'][:2]}")
        print(f"   Questionnaire items: {len(features['questionnaire'])}")

