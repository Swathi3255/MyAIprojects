#!/usr/bin/env python3
"""
Specialized Color Psychology RAG Application
Custom system prompts and features for color psychology and cultural meanings
"""

# Specialized system prompt for Color Psychology RAG
COLOR_PSYCHOLOGY_SYSTEM_PROMPT = """You are a specialized Color Psychology and Cultural Meanings AI assistant. You have access to comprehensive information about color psychology, cultural symbolism, and the psychological effects of colors across different societies.

Your expertise includes:
- Psychological effects of colors on human behavior and emotions
- Cultural meanings and symbolism of colors across different societies
- Color psychology in marketing, branding, and design
- Color therapy and healing applications
- Gender and age-related color preferences
- Color combinations and their psychological effects
- Digital design and color psychology
- Interior design and color psychology

When answering questions about colors:
1. Provide specific psychological effects and cultural meanings
2. Include practical applications in design, marketing, and therapy
3. Mention cultural differences and sensitivities
4. Suggest appropriate color choices for specific contexts
5. Explain the science behind color psychology when relevant
6. Consider both universal and culture-specific meanings

If asked about color recommendations:
- Consider the target audience and cultural context
- Explain the psychological reasoning behind suggestions
- Mention any cultural sensitivities or considerations
- Provide alternatives for different contexts
- Include practical implementation tips

Always prioritize cultural sensitivity and provide accurate, evidence-based information about color psychology."""

# Specialized features for Color Psychology RAG
COLOR_PSYCHOLOGY_FEATURES = {
    "questionnaire": [
        "What is the target audience for your color choice?",
        "What cultural context should be considered?",
        "What emotional response are you trying to evoke?",
        "What is the intended use (marketing, design, therapy, etc.)?",
        "Are there any cultural sensitivities to consider?",
        "What age group is your target audience?",
        "What is the brand personality you want to convey?",
        "Are there any accessibility considerations?"
    ],
    "unique_queries": [
        "What colors should I use for a calming bedroom?",
        "Which colors are best for a children's learning environment?",
        "What colors should I avoid in different cultures?",
        "How do colors affect consumer purchasing decisions?",
        "What colors are most effective for healthcare environments?",
        "Which colors promote trust in financial services?",
        "What colors work best for food and restaurant branding?",
        "How do colors affect productivity in office spaces?",
        "What colors are most accessible for people with visual impairments?",
        "Which colors are associated with luxury and premium brands?"
    ],
    "color_analysis": {
        "red": {
            "psychological_effects": ["increases heart rate", "creates urgency", "stimulates appetite", "evokes passion"],
            "cultural_meanings": ["love in West", "luck in China", "life force in Africa"],
            "best_for": ["restaurants", "sale promotions", "emergency signals"],
            "avoid_in": ["bedrooms", "healthcare", "calming environments"]
        },
        "blue": {
            "psychological_effects": ["promotes trust", "calms the mind", "reduces blood pressure", "enhances focus"],
            "cultural_meanings": ["trust universally", "divine in India", "immortality in China"],
            "best_for": ["corporate branding", "healthcare", "financial services"],
            "avoid_in": ["food branding", "appetite stimulation"]
        },
        "green": {
            "psychological_effects": ["promotes balance", "reduces eye strain", "represents growth", "calms anxiety"],
            "cultural_meanings": ["nature universally", "paradise in Islam", "harmony in China"],
            "best_for": ["environmental brands", "healthcare", "educational settings"],
            "avoid_in": ["urgent situations", "high-energy environments"]
        },
        "yellow": {
            "psychological_effects": ["stimulates creativity", "increases energy", "promotes optimism", "enhances memory"],
            "cultural_meanings": ["happiness universally", "royalty in China", "cowardice in some contexts"],
            "best_for": ["educational materials", "creative spaces", "attention-grabbing"],
            "avoid_in": ["large areas", "calming environments"]
        },
        "purple": {
            "psychological_effects": ["promotes creativity", "represents luxury", "enhances spirituality", "stimulates imagination"],
            "cultural_meanings": ["royalty historically", "mystery universally", "wisdom in many cultures"],
            "best_for": ["luxury brands", "creative industries", "spiritual contexts"],
            "avoid_in": ["budget-conscious markets", "conservative environments"]
        },
        "orange": {
            "psychological_effects": ["stimulates appetite", "promotes enthusiasm", "encourages social interaction", "creates warmth"],
            "cultural_meanings": ["autumn universally", "change and transition", "adventure and risk"],
            "best_for": ["food branding", "social spaces", "energetic environments"],
            "avoid_in": ["calming environments", "professional settings"]
        }
    }
}

def get_color_psychology_prompt():
    """Get the specialized system prompt for color psychology"""
    return COLOR_PSYCHOLOGY_SYSTEM_PROMPT

def get_color_analysis(color_name):
    """Get detailed analysis for a specific color"""
    return COLOR_PSYCHOLOGY_FEATURES["color_analysis"].get(color_name.lower(), {})

def get_specialized_queries():
    """Get specialized query examples for color psychology"""
    return COLOR_PSYCHOLOGY_FEATURES["unique_queries"]

def get_questionnaire_items():
    """Get questionnaire items for color psychology consultation"""
    return COLOR_PSYCHOLOGY_FEATURES["questionnaire"]

# Example usage and testing
def test_color_psychology_features():
    """Test the color psychology features"""
    print("🎨 Color Psychology RAG Application Features")
    print("=" * 50)
    
    print("\n📋 Sample Questionnaire Items:")
    for i, item in enumerate(get_questionnaire_items(), 1):
        print(f"   {i}. {item}")
    
    print("\n🔍 Sample Specialized Queries:")
    for i, query in enumerate(get_specialized_queries(), 1):
        print(f"   {i}. {query}")
    
    print("\n🌈 Color Analysis Examples:")
    for color, analysis in COLOR_PSYCHOLOGY_FEATURES["color_analysis"].items():
        print(f"\n   {color.upper()}:")
        print(f"      Psychological Effects: {', '.join(analysis['psychological_effects'])}")
        print(f"      Cultural Meanings: {', '.join(analysis['cultural_meanings'])}")
        print(f"      Best For: {', '.join(analysis['best_for'])}")
        print(f"      Avoid In: {', '.join(analysis['avoid_in'])}")

if __name__ == "__main__":
    test_color_psychology_features()

