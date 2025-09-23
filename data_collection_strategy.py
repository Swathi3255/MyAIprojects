#!/usr/bin/env python3
"""
Data Collection Strategy for Specialized RAG Applications
This script helps you gather and organize data for your chosen niche
"""

import requests
import json
import os
from pathlib import Path

def collect_dog_breed_data():
    """Collect comprehensive dog breed data from various sources"""
    
    print("🐕 Collecting Dog Breed Data...")
    print("=" * 40)
    
    # Data sources for dog breeds
    data_sources = {
        "akc_breeds": "https://www.akc.org/dog-breeds/",
        "wikipedia_breeds": "https://en.wikipedia.org/wiki/List_of_dog_breeds",
        "vet_info": "https://vcahospitals.com/know-your-pet/dog-breeds",
        "training_info": "https://www.akc.org/expert-advice/training/"
    }
    
    # Sample data structure for dog breeds
    breed_template = {
        "name": "",
        "akc_group": "",
        "size": "",
        "weight_range": "",
        "height_range": "",
        "lifespan": "",
        "temperament": [],
        "exercise_needs": "",
        "grooming_needs": "",
        "training_difficulty": "",
        "intelligence_rank": "",
        "good_with_children": "",
        "good_with_other_pets": "",
        "apartment_suitable": "",
        "common_health_issues": [],
        "origin_country": "",
        "breed_history": "",
        "special_requirements": [],
        "best_for": []
    }
    
    # Create data directory
    data_dir = Path("specialized_data/dog_breeds")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample breeds to start with (most popular)
    popular_breeds = [
        "Golden Retriever", "Labrador Retriever", "German Shepherd",
        "French Bulldog", "Bulldog", "Poodle", "Beagle", "Rottweiler",
        "German Shorthaired Pointer", "Yorkshire Terrier"
    ]
    
    print(f"📊 Will collect data for {len(popular_breeds)} popular breeds")
    print("💡 Data collection strategy:")
    print("   1. Manual research from AKC website")
    print("   2. Wikipedia for breed history")
    print("   3. Veterinary sources for health info")
    print("   4. Training resources for behavior")
    
    return breed_template, popular_breeds

def collect_national_animals_data():
    """Collect national animals data from various countries"""
    
    print("🌍 Collecting National Animals Data...")
    print("=" * 40)
    
    # Sample data structure for national animals
    animal_template = {
        "country": "",
        "official_name": "",
        "animal_name": "",
        "scientific_name": "",
        "cultural_significance": "",
        "why_chosen": "",
        "conservation_status": "",
        "folklore_stories": [],
        "ceremonies_traditions": [],
        "similar_animals_other_countries": [],
        "interesting_facts": [],
        "year_established": "",
        "unofficial_symbols": []
    }
    
    # Countries with interesting national animals
    countries_with_animals = [
        {"country": "United States", "animal": "Bald Eagle"},
        {"country": "United Kingdom", "animal": "Lion"},
        {"country": "Australia", "animal": "Kangaroo"},
        {"country": "Canada", "animal": "Beaver"},
        {"country": "India", "animal": "Bengal Tiger"},
        {"country": "China", "animal": "Giant Panda"},
        {"country": "Russia", "animal": "Brown Bear"},
        {"country": "South Africa", "animal": "Springbok"},
        {"country": "New Zealand", "animal": "Kiwi"},
        {"country": "Brazil", "animal": "Jaguar"}
    ]
    
    print(f"📊 Will collect data for {len(countries_with_animals)} countries")
    print("💡 Data collection strategy:")
    print("   1. Official government sources")
    print("   2. Cultural and historical references")
    print("   3. Conservation status from IUCN")
    print("   4. Folklore and legend sources")
    
    return animal_template, countries_with_animals

def collect_mushroom_safety_data():
    """Collect mushroom identification and safety data"""
    
    print("🍄 Collecting Mushroom Safety Data...")
    print("=" * 40)
    
    # Sample data structure for mushrooms
    mushroom_template = {
        "common_name": "",
        "scientific_name": "",
        "edibility": "",  # Edible, Poisonous, Unknown
        "key_identifying_features": [],
        "habitat": "",
        "season": "",
        "size_description": "",
        "cap_description": "",
        "stem_description": "",
        "gills_description": "",
        "spore_print_color": "",
        "dangerous_look_alikes": [],
        "poisoning_symptoms": [],
        "emergency_protocol": "",
        "geographic_distribution": "",
        "conservation_status": ""
    }
    
    # Common mushrooms to start with
    common_mushrooms = [
        {"name": "Chanterelle", "edibility": "Edible"},
        {"name": "Morel", "edibility": "Edible"},
        {"name": "Death Cap", "edibility": "Poisonous"},
        {"name": "Destroying Angel", "edibility": "Poisonous"},
        {"name": "Porcini", "edibility": "Edible"},
        {"name": "Fly Agaric", "edibility": "Poisonous"},
        {"name": "Oyster Mushroom", "edibility": "Edible"},
        {"name": "Shiitake", "edibility": "Edible"},
        {"name": "Jack O'Lantern", "edibility": "Poisonous"},
        {"name": "Lion's Mane", "edibility": "Edible"}
    ]
    
    print(f"📊 Will collect data for {len(common_mushrooms)} common mushrooms")
    print("💡 Data collection strategy:")
    print("   1. Mycology field guides")
    print("   2. Poison control center data")
    print("   3. University mycology departments")
    print("   4. Regional mushroom clubs")
    print("⚠️  IMPORTANT: Always verify with local experts!")
    
    return mushroom_template, common_mushrooms

def create_data_collection_guide():
    """Create a comprehensive guide for data collection"""
    
    guide = """
# Specialized RAG Data Collection Guide

## 🎯 Choosing Your Niche

### High-Value Niches:
1. **Dog Breeds** - Large, engaged community, practical utility
2. **National Animals** - Educational, cultural interest, unique angle
3. **Mushroom Safety** - Safety-critical, specialized knowledge
4. **Plant Toxicity** - Pet safety, gardening community
5. **Mythical Creatures** - Creative, entertainment value

## 📊 Data Collection Strategy

### Phase 1: Foundation Data
- Start with 20-50 core entries
- Focus on accuracy over quantity
- Include multiple verification sources

### Phase 2: Expansion
- Add 100-200 more entries
- Include regional variations
- Add user-generated content

### Phase 3: Specialization
- Add advanced features
- Include multimedia content
- Implement user feedback loops

## 🔍 Data Sources by Niche

### Dog Breeds:
- AKC (American Kennel Club)
- FCI (Fédération Cynologique Internationale)
- Veterinary databases
- Breed-specific clubs and organizations

### National Animals:
- Government official sources
- Cultural heritage organizations
- Conservation groups (IUCN, WWF)
- Academic cultural studies

### Mushroom Safety:
- Mycology societies
- Poison control centers
- University mycology departments
- Regional field guides

## ⚠️ Important Considerations

### Safety-Critical Applications:
- Always include disclaimers
- Recommend expert consultation
- Provide emergency protocols
- Regular data updates

### Legal Considerations:
- Verify data accuracy
- Include proper attributions
- Respect copyright laws
- Include liability disclaimers

## 🚀 Implementation Tips

1. **Start Small**: Begin with 10-20 high-quality entries
2. **User Feedback**: Implement rating and correction systems
3. **Regular Updates**: Keep data current and accurate
4. **Community Building**: Engage with niche communities
5. **Monetization**: Consider premium features or subscriptions
"""
    
    with open("specialized_data/collection_guide.md", "w") as f:
        f.write(guide)
    
    print("📚 Created comprehensive data collection guide!")
    print("   Location: specialized_data/collection_guide.md")

if __name__ == "__main__":
    print("🎯 Specialized RAG Data Collection Strategy")
    print("=" * 50)
    
    # Create data directory
    Path("specialized_data").mkdir(exist_ok=True)
    
    # Show examples for different niches
    print("\n🐕 Dog Breeds Example:")
    breed_template, breeds = collect_dog_breed_data()
    
    print("\n🌍 National Animals Example:")
    animal_template, countries = collect_national_animals_data()
    
    print("\n🍄 Mushroom Safety Example:")
    mushroom_template, mushrooms = collect_mushroom_safety_data()
    
    # Create the guide
    create_data_collection_guide()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Choose your niche")
    print("2. Start collecting data manually")
    print("3. Modify your app's system prompts")
    print("4. Add specialized features")
    print("5. Test with your target audience")
