"""
WorshipFlow AI - A Streamlit web app for generating structured praise and worship plans.
Helps worship leaders create worship sets based on service themes.
"""

import streamlit as st
import os
import json
from datetime import datetime
import random
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="WorshipFlow AI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, modern theme
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: 800; color: #1e3a5f; text-align: center; margin-bottom: 0.5rem;}
    .sub-header {font-size: 1.1rem; color: #4a6fa5; text-align: center; margin-bottom: 2.5rem; font-weight: 400;}
    .section-header {font-size: 1.3rem; font-weight: 700; color: #1e3a5f; margin-top: 1.5rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 3px solid #4a6fa5; display: flex; align-items: center; gap: 0.5rem;}
    .section-header.praise {border-bottom-color: #e67e22; color: #d35400;}
    .section-header.worship {border-bottom-color: #27ae60; color: #1e8449;}
    .section-header.new-songs {border-bottom-color: #27ae60; color: #1e8449;}
    .section-header.theme {border-bottom-color: #3498db; color: #2980b9;}
    .section-header.selection {border-bottom-color: #9b59b6; color: #8e44ad;}
    .section-header.transition {border-bottom-color: #e67e22; color: #d35400;}
    .section-header.rehearsal {border-bottom-color: #e74c3c; color: #c0392b;}
    .card {background: white; border-radius: 10px; padding: 1.25rem; margin: 0.75rem 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border: 1px solid #e0e0e0;}
    .card.praise-card {border-left: 4px solid #e67e22;}
    .card.worship-card {border-left: 4px solid #27ae60;}
    .card.theme-card {border-left: 4px solid #3498db; background: #f8fbfd;}
    .card.transition-card {border-left: 4px solid #9b59b6; background: #fbf8fd;}
    .card.rehearsal-card {border-left: 4px solid #e67e22; background: #fefcf8;}
    .card.selection-notes {border-left: 4px solid #9b59b6; background: #fbf8fd;}
    .song-item {background: #f8f9fa; border-radius: 8px; padding: 0.875rem 1rem; margin: 0.5rem 0; border: 1px solid #e9ecef;}
    .song-number {display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 50%; background: #4a6fa5; color: white; font-weight: 700; font-size: 0.8rem; margin-right: 0.5rem;}
    .song-title {font-weight: 700; color: #1e3a5f; font-size: 1.05rem; display: inline;}
    .song-meta {color: #666; font-size: 0.85rem; margin-top: 0.35rem; line-height: 1.5;}
    .song-meta strong {color: #444;}
    .duration-badge {display: inline-block; background: #e3f2fd; color: #1565c0; padding: 0.15rem 0.5rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-left: 0.5rem;}
    .new-badge {display: inline-block; background: #27ae60; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; margin-left: 0.5rem;}
    .info-box {background: #f0f7ff; border: 1px solid #b3d4fc; border-radius: 8px; padding: 0.875rem 1rem; margin: 0.75rem 0; color: #1e407c; font-size: 0.9rem;}
    .bullet-point {display: flex; align-items: flex-start; margin: 0.4rem 0; line-height: 1.5; font-size: 0.9rem;}
    .bullet-point::before {content: "•"; color: #4a6fa5; font-weight: bold; font-size: 1.2rem; margin-right: 0.4rem;}
    .stButton>button {background: linear-gradient(135deg, #4a6fa5 0%, #1e3a5f 100%) !important; color: white !important; font-weight: 700 !important; padding: 0.75rem 2rem !important; border: none !important; border-radius: 8px !important; font-size: 1.05rem !important; box-shadow: 0 2px 8px rgba(30, 58, 95, 0.3) !important; transition: all 0.2s ease !important; width: 100%;}
    .stButton>button:hover {transform: translateY(-1px); box-shadow: 0 4px 12px rgba(30, 58, 95, 0.4) !important;}
    .footer {text-align: center; color: #888; font-size: 0.8rem; margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid #e0e0e0;}
    .footer-quote {font-style: italic; color: #666; margin-top: 0.35rem;}
    .success-banner {background: #d4edda; color: #155724; padding: 0.875rem 1.25rem; border-radius: 8px; margin: 0.75rem 0; font-weight: 600; border: 1px solid #c3e6cb;}
    .warning-banner {background: #fff3cd; color: #856404; padding: 0.875rem 1.25rem; border-radius: 8px; margin: 0.75rem 0; font-weight: 600; border: 1px solid #ffeaa7;}
    .youtube-link {color: #4a6fa5; text-decoration: none; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.25rem; margin-top: 0.5rem;}
    .youtube-link:hover {text-decoration: underline;}
</style>
""", unsafe_allow_html=True)

# Expanded Song databases
PRAISE_SONGS = [
    # Contemporary Praise
    {"title": "Awesome God", "artist": "Rich Mullins", "tempo": "Upbeat", "energy": 9, "key": "D", "duration": 3.8, "year": 1988, "familiarity": "High", "style": ["Contemporary", "Blended"]},
    {"title": "The Stand", "artist": "Hillsong", "tempo": "Upbeat", "energy": 9, "key": "E", "duration": 5.0, "year": 2004, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Raise a Hallelujah", "artist": "Bethel Music", "tempo": "Upbeat", "energy": 9, "key": "D", "duration": 4.8, "year": 2019, "familiarity": "High", "style": ["Contemporary", "Charismatic"]},
    {"title": "Forever", "artist": "Chris Tomlin", "tempo": "Upbeat", "energy": 8, "key": "D", "duration": 4.0, "year": 2006, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "God's Not Dead", "artist": "Newsboys", "tempo": "Upbeat", "energy": 9, "key": "E", "duration": 3.8, "year": 2011, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "My Victory", "artist": "Bethel Music", "tempo": "Upbeat", "energy": 9, "key": "D", "duration": 4.2, "year": 2019, "familiarity": "Medium", "style": ["Contemporary", "Charismatic"]},
    {"title": "Death Was Arrested", "artist": "North Point Worship", "tempo": "Upbeat", "energy": 9, "key": "E", "duration": 4.0, "year": 2014, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Resurrecting", "artist": "Elevation Worship", "tempo": "Upbeat", "energy": 8, "key": "D", "duration": 4.5, "year": 2017, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Victory", "artist": "Elevation Worship", "tempo": "Upbeat", "energy": 9, "key": "E", "duration": 4.0, "year": 2019, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Glorious Day", "artist": "Casting Crowns", "tempo": "Upbeat", "energy": 8, "key": "G", "duration": 4.2, "year": 2010, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "Celebration", "artist": "Hillsong", "tempo": "Upbeat", "energy": 9, "key": "D", "duration": 4.0, "year": 2015, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Shout to the Lord", "artist": "Darlene Zschech", "tempo": "Upbeat", "energy": 8, "key": "D", "duration": 4.5, "year": 1994, "familiarity": "High", "style": ["Contemporary", "Blended"]},
    # Gospel Praise
    {"title": "Amazing Love", "artist": "Don Moen", "tempo": "Mid-tempo", "energy": 6, "key": "F", "duration": 4.0, "year": 2000, "familiarity": "High", "style": ["Gospel", "Contemporary"]},
    {"title": "Stand in Your Love", "artist": "Josh Baldwin", "tempo": "Mid-tempo", "energy": 7, "key": "E", "duration": 4.0, "year": 2018, "familiarity": "Medium", "style": ["Gospel", "Contemporary"]},
    {"title": "Way Maker", "artist": "Sinach", "tempo": "Mid-tempo", "energy": 7, "key": "C", "duration": 4.5, "year": 2015, "familiarity": "High", "style": ["Contemporary", "Gospel"]},
    {"title": "Break Every Chain", "artist": "Tasha Cobbs", "tempo": "Upbeat", "energy": 9, "key": "F", "duration": 4.8, "year": 2013, "familiarity": "High", "style": ["Gospel", "Contemporary"]},
    {"title": "Won't He Do It", "artist": "Koryn Hawthorne", "tempo": "Upbeat", "energy": 8, "key": "G", "duration": 3.8, "year": 2018, "familiarity": "Medium", "style": ["Gospel"]},
    {"title": "Speak the Name", "artist": "Kari Jobe", "tempo": "Upbeat", "energy": 8, "key": "D", "duration": 4.2, "year": 2020, "familiarity": "Medium", "style": ["Gospel", "Contemporary"]},
    {"title": "Praise", "artist": "Elevation Worship", "tempo": "Upbeat", "energy": 9, "key": "E", "duration": 4.0, "year": 2023, "familiarity": "Medium", "style": ["Gospel", "Contemporary"]},
    {"title": "Hallelujah Here Below", "artist": "Elevation Worship", "tempo": "Upbeat", "energy": 8, "key": "D", "duration": 4.5, "year": 2021, "familiarity": "Medium", "style": ["Gospel", "Contemporary"]},
    # African Praise
    {"title": "Omo Oba", "artist": "Nathaniel Bassey", "tempo": "Upbeat", "energy": 9, "key": "F", "duration": 4.5, "year": 2018, "familiarity": "Medium", "style": ["African", "Gospel"]},
    {"title": "Imela", "artist": "Dunsin Oyekan", "tempo": "Upbeat", "energy": 9, "key": "G", "duration": 5.0, "year": 2019, "familiarity": "Low", "style": ["African", "Afrobeat"]},
    {"title": "Agbara Re", "artist": "Tope Alabi", "tempo": "Upbeat", "energy": 10, "key": "C", "duration": 4.5, "year": 2017, "familiarity": "Low", "style": ["African", "Nigerian Gospel"]},
    {"title": "Je Kabiyesi", "artist": "Nathaniel Bassey", "tempo": "Upbeat", "energy": 9, "key": "D", "duration": 4.0, "year": 2020, "familiarity": "Low", "style": ["African", "Nigerian Gospel"]},
    {"title": "Higher", "artist": "Dunsin Oyekan", "tempo": "Upbeat", "energy": 8, "key": "E", "duration": 4.5, "year": 2021, "familiarity": "Low", "style": ["African", "Afrobeat"]},
    {"title": "Jehovah Overdo", "artist": "Sinach", "tempo": "Upbeat", "energy": 9, "key": "F", "duration": 4.0, "year": 2016, "familiarity": "Medium", "style": ["African", "Gospel"]},
    {"title": "Obinasom", "artist": "Dunsin Oyekan", "tempo": "Upbeat", "energy": 8, "key": "G", "duration": 4.5, "year": 2021, "familiarity": "Low", "style": ["African", "Afrobeat"]},
    {"title": "Iba", "artist": "Nathaniel Bassey", "tempo": "Upbeat", "energy": 9, "key": "F", "duration": 4.8, "year": 2019, "familiarity": "Low", "style": ["African", "Nigerian Gospel"]},
    {"title": "Ebi O Da", "artist": "Nathaniel Bassey", "tempo": "Upbeat", "energy": 8, "key": "G", "duration": 4.2, "year": 2020, "familiarity": "Low", "style": ["African", "Nigerian Gospel"]},
    {"title": "Yeshua", "artist": "Dunsin Oyekan", "tempo": "Upbeat", "energy": 9, "key": "E", "duration": 5.0, "year": 2020, "familiarity": "Low", "style": ["African", "Afrobeat"]},
    # Charismatic Praise
    {"title": "Lion and the Lamb", "artist": "Bethel Music", "tempo": "Mid-tempo", "energy": 7, "key": "G", "duration": 4.3, "year": 2016, "familiarity": "High", "style": ["Contemporary", "Charismatic"]},
    {"title": "Who You Say I Am", "artist": "Hillsong", "tempo": "Mid-tempo", "energy": 6, "key": "D", "duration": 4.5, "year": 2018, "familiarity": "High", "style": ["Contemporary", "Charismatic"]},
    {"title": "No Longer Slaves", "artist": "Bethel Music", "tempo": "Mid-tempo", "energy": 6, "key": "B", "duration": 5.2, "year": 2015, "familiarity": "High", "style": ["Contemporary", "Charismatic"]},
    {"title": "Spirit Break Out", "artist": "Bethel Music", "tempo": "Upbeat", "energy": 8, "key": "D", "duration": 4.5, "year": 2014, "familiarity": "Medium", "style": ["Charismatic", "Contemporary"]},
    # Blended Praise
    {"title": "10,000 Reasons (Bless the Lord)", "artist": "Matt Redman", "tempo": "Mid-tempo", "energy": 6, "key": "G", "duration": 4.5, "year": 2011, "familiarity": "High", "style": ["Contemporary", "Blended"]},
    {"title": "How Great Is Our God", "artist": "Chris Tomlin", "tempo": "Mid-tempo", "energy": 6, "key": "C", "duration": 4.2, "year": 2004, "familiarity": "High", "style": ["Contemporary", "Blended"]},
    {"title": "Mighty to Save", "artist": "Hillsong", "tempo": "Mid-tempo", "energy": 6, "key": "Bb", "duration": 4.5, "year": 2006, "familiarity": "High", "style": ["Contemporary", "Blended"]},
    {"title": "Blessed Be Your Name", "artist": "Matt Redman", "tempo": "Mid-tempo", "energy": 6, "key": "A", "duration": 4.2, "year": 2002, "familiarity": "High", "style": ["Contemporary", "Blended"]},
    {"title": "Great Are You Lord", "artist": "All Sons & Daughters", "tempo": "Mid-tempo", "energy": 5, "key": "C", "duration": 4.8, "year": 2013, "familiarity": "High", "style": ["Contemporary", "Blended"]},
    # High Energy / Mixed
    {"title": "This Is Amazing Grace", "artist": "Phil Wickham", "tempo": "Mid-tempo", "energy": 7, "key": "F#", "duration": 4.3, "year": 2013, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "King of Kings", "artist": "Hillsong", "tempo": "Mid-tempo", "energy": 7, "key": "D", "duration": 5.5, "year": 2019, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Build My Life", "artist": "Housefires", "tempo": "Mid-tempo", "energy": 6, "key": "D", "duration": 4.5, "year": 2017, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "What a Beautiful Name", "artist": "Hillsong", "tempo": "Mid-tempo", "energy": 6, "key": "B", "duration": 4.2, "year": 2016, "familiarity": "High", "style": ["Contemporary"]},
]

WORSHIP_SONGS = [
    {"title": "Goodness of God", "artist": "Jenn Johnson", "tempo": "Slow", "energy": 3, "key": "G", "duration": 4.8, "year": 2018, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "Jireh", "artist": "Elevation Worship & Maverick City", "tempo": "Slow", "energy": 3, "key": "F", "duration": 5.2, "year": 2021, "familiarity": "Medium", "style": ["Contemporary", "Gospel"]},
    {"title": "Promises", "artist": "Maverick City Music", "tempo": "Slow", "energy": 3, "key": "Eb", "duration": 5.0, "year": 2019, "familiarity": "Medium", "style": ["Gospel", "Contemporary"]},
    {"title": "No Longer Slaves", "artist": "Bethel Music", "tempo": "Slow", "energy": 4, "key": "B", "duration": 5.2, "year": 2015, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "So Will I (100 Billion X)", "artist": "Hillsong United", "tempo": "Slow", "energy": 3, "key": "C", "duration": 5.5, "year": 2017, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Holy Spirit", "artist": "Jesus Culture", "tempo": "Slow", "energy": 3, "key": "C", "duration": 5.0, "year": 2012, "familiarity": "Medium", "style": ["Contemporary", "Charismatic"]},
    {"title": "Come Away", "artist": "Hillsong", "tempo": "Slow", "energy": 2, "key": "D", "duration": 4.5, "year": 2010, "familiarity": "Low", "style": ["Contemporary"]},
    {"title": "I Surrender", "artist": "Hillsong", "tempo": "Slow", "energy": 3, "key": "E", "duration": 4.8, "year": 2002, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Speak O Lord", "artist": "Keith & Kristyn Getty", "tempo": "Slow", "energy": 3, "key": "F", "duration": 4.2, "year": 2005, "familiarity": "Medium", "style": ["Traditional", "Blended"]},
    {"title": "In Christ Alone", "artist": "Keith & Kristyn Getty", "tempo": "Slow", "energy": 3, "key": "F", "duration": 4.5, "year": 2001, "familiarity": "High", "style": ["Traditional", "Blended"]},
    {"title": "Be Still My Soul", "artist": "Traditional", "tempo": "Slow", "energy": 2, "key": "D", "duration": 4.0, "year": 1853, "familiarity": "High", "style": ["Traditional", "Blended"]},
    {"title": "It Is Well", "artist": "Traditional", "tempo": "Slow", "energy": 2, "key": "F", "duration": 4.5, "year": 1873, "familiarity": "High", "style": ["Traditional", "Blended"]},
    {"title": "O Come to the Altar", "artist": "Elevation Worship", "tempo": "Mid-tempo", "energy": 5, "key": "B", "duration": 4.3, "year": 2015, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "Reckless Love", "artist": "Cory Asbury", "tempo": "Mid-tempo", "energy": 5, "key": "G", "duration": 4.5, "year": 2017, "familiarity": "High", "style": ["Contemporary"]},
    {"title": "Living Hope", "artist": "Phil Wickham", "tempo": "Mid-tempo", "energy": 5, "key": "C", "duration": 4.5, "year": 2018, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "Graves Into Gardens", "artist": "Elevation Worship", "tempo": "Mid-tempo", "energy": 5, "key": "D", "duration": 4.7, "year": 2020, "familiarity": "Medium", "style": ["Contemporary"]},
    {"title": "The Way (New Horizon)", "artist": "Phil Wickham", "tempo": "Mid-tempo", "energy": 4, "key": "G", "duration": 4.3, "year": 2021, "familiarity": "Low", "style": ["Contemporary"]},
    {"title": "Wait on You", "artist": "Maverick City Music", "tempo": "Slow", "energy": 3, "key": "Eb", "duration": 5.5, "year": 2020, "familiarity": "Medium", "style": ["Gospel"]},
    {"title": "Fear", "artist": "Maverick City Music", "tempo": "Slow", "energy": 3, "key": "F", "duration": 5.0, "year": 2020, "familiarity": "Low", "style": ["Gospel"]},
    {"title": "Man of Your Word", "artist": "Maverick City Music", "tempo": "Mid-tempo", "energy": 5, "key": "G", "duration": 4.5, "year": 2020, "familiarity": "Medium", "style": ["Gospel"]},
    {"title": "Obinasom", "artist": "Dunsin Oyekan", "tempo": "Slow", "energy": 3, "key": "F", "duration": 5.0, "year": 2020, "familiarity": "Low", "style": ["African"]},
    {"title": "Ebi O Da", "artist": "Nathaniel Bassey", "tempo": "Slow", "energy": 3, "key": "G", "duration": 4.5, "year": 2019, "familiarity": "Low", "style": ["African", "Nigerian Gospel"]},
    {"title": "Iwalewa", "artist": "Tope Alabi", "tempo": "Slow", "energy": 3, "key": "C", "duration": 4.0, "year": 2018, "familiarity": "Low", "style": ["African", "Nigerian Gospel"]},
]

NEW_SONGS = [
    {"title": "Praise", "artist": "Elevation Worship", "year": 2023, "style": "Contemporary"},
    {"title": "Trust in God", "artist": "Elevation Worship", "year": 2022, "style": "Contemporary"},
    {"title": "Same God", "artist": "Elevation Worship", "year": 2022, "style": "Contemporary"},
    {"title": "I Thank God", "artist": "Maverick City Music", "year": 2022, "style": "Gospel"},
    {"title": "Kingdom", "artist": "Maverick City Music", "year": 2023, "style": "Gospel"},
    {"title": "Holy Water", "artist": "Maverick City Music", "year": 2021, "style": "Gospel"},
    {"title": "The Blessing", "artist": "Elevation Worship", "year": 2020, "style": "Contemporary"},
    {"title": "Won't Stop Praying", "artist": "Elevation Worship", "year": 2023, "style": "Contemporary"},
    {"title": "Your Blood", "artist": "Elevation Worship", "year": 2023, "style": "Contemporary"},
    {"title": "Spearhead", "artist": "Elevation Worship", "year": 2023, "style": "Contemporary"},
]

THEME_SONGS = {
    "grace": ["Amazing Grace (My Chains Are Gone)", "Grace Like Rain", "Tis So Sweet"],
    "redemption": ["Redeemed", "The Cross Has the Final Word", "Man of Sorrows"],
    "praise": ["10,000 Reasons", "Bless the Lord", "How Great Thou Art"],
    "surrender": ["I Surrender All", "Take My Life", "Have Thine Own Way"],
    "healing": ["Healer", "Jesus We Just Want to Thank You", "Healing Rain"],
    "hope": ["Hope of the Nations", "Cornerstone", "Hope in Front of Me"],
    "love": ["Oh How He Loves", "The Love of God", "God So Loved"],
    "faith": ["Faith", "Great Is Thy Faithfulness", "Faithful Now"],
    "thanksgiving": ["Give Thanks", "Thank You Lord", "Now Thank We All Our God"],
    "easter": ["Christ Arose", "Up From the Grave", "He Is Risen"],
    "christmas": ["O Come Let Us Adore Him", "Silent Night", "O Holy Night"],
    "pentecost": ["Spirit of the Living God", "Holy Spirit Thou Art Welcome", "Breathe"],
    "communion": ["Because He Lives", "The Blood Will Never Lose Its Power"],
    "missions": ["Send Me", "Here I Am Send Me", "Go Light Your World"],
    "default": ["Amazing Grace", "Great Is Thy Faithfulness", "Holy Holy Holy"]
}


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except ImportError:
        return None


def generate_songs_with_gpt(client, style, song_type, count, theme="", 
                             praise_style="", worship_style="", familiarity="",
                             medley_instructions="", recent_songs="", 
                             preferred_praise="", preferred_worship=""):
    """Use GPT to generate additional song suggestions when internal pool is insufficient.
    
    Args:
        client: OpenAI client
        style: The style being targeted (e.g., "African Praise", "Contemporary")
        song_type: "praise" or "worship"
        count: Number of songs to generate
        theme: Service theme
        praise_style: Praise style selection
        worship_style: Worship style selection
        familiarity: Familiarity preference
        medley_instructions: Leader notes
        recent_songs: Recently used songs
        preferred_praise: Preferred praise songs
        preferred_worship: Preferred worship songs
    
    Returns:
        List of song dictionaries in the app's format
    """
    if not client:
        return []
    
    is_praise = song_type == "praise"
    duration = 2.0 if is_praise else 4.5
    tempo = "Upbeat" if is_praise else "Slow"
    energy_range = "7-10" if is_praise else "2-5"
    
    # Build context from user inputs
    context_parts = []
    if theme:
        context_parts.append(f"Service Theme: {theme}")
    if praise_style and is_praise:
        context_parts.append(f"Praise Style: {praise_style}")
    if worship_style and not is_praise:
        context_parts.append(f"Worship Style: {worship_style}")
    if familiarity:
        context_parts.append(f"Familiarity: {familiarity}")
    if medley_instructions:
        context_parts.append(f"Leader Notes: {medley_instructions}")
    if recent_songs:
        context_parts.append(f"Recently Used: {recent_songs}")
    if preferred_praise and is_praise:
        context_parts.append(f"Preferred Praise: {preferred_praise}")
    if preferred_worship and not is_praise:
        context_parts.append(f"Preferred Worship: {preferred_worship}")
    
    context = "\n".join(context_parts) if context_parts else "No specific preferences provided"
    
    # Special instructions for African/Nigerian styles
    african_instruction = ""
    if "African" in style or "Nigerian" in style or "Afrobeat" in style:
        african_instruction = """
IMPORTANT: Focus on African and Nigerian gospel praise songs. Consider:
- Songs by Nathaniel Bassey, Dunsin Oyekan, Tope Alabi, Sinach
- Afrobeat praise songs with high energy
- Nigerian gospel praise medley songs
- Call-and-response friendly songs
- Songs commonly used in live African church services
"""
    
    prompt = f"""You are an expert worship leader and song curator. I need you to suggest {count} {song_type} songs for a worship service.

Style requested: {style}
{african_instruction}
{context}

Requirements:
- Each song should be a real, known worship song
- For praise medley segments, suggest songs that work well as 2-minute segments
- For worship songs, suggest full 4-5 minute songs
- Energy level should be in range {energy_range}
- If you know the artist, include it; otherwise use "Unknown / verify on YouTube"
- Prioritize songs that fit the style and context provided

Return your suggestions as a JSON array of objects with these fields:
- title: song title
- artist: artist name (or "Unknown / verify on YouTube" if unsure)
- key: musical key (or "Unknown")
- tempo: "{tempo}"
- energy: number 1-10 ({energy_range} range)
- familiarity: "Medium"
- duration: {duration}
- source: "GPT-generated"

Example format:
[
  {{"title": "Song Name", "artist": "Artist Name", "key": "D", "tempo": "{tempo}", "energy": 8, "familiarity": "Medium", "duration": {duration}, "source": "GPT-generated"}},
  ...
]

Only return the JSON array, no other text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert worship leader and song curator with deep knowledge of contemporary, gospel, and African/Nigerian worship music."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON from response
        import json
        # Try to extract JSON from the response (might have markdown formatting)
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        songs_data = json.loads(result_text)
        
        # Convert to app format with YouTube search URLs
        generated_songs = []
        for song_data in songs_data:
            song = {
                "title": song_data.get("title", "Unknown Song"),
                "artist": song_data.get("artist", "Unknown / verify on YouTube"),
                "key": song_data.get("key", "Unknown"),
                "tempo": song_data.get("tempo", tempo),
                "energy": song_data.get("energy", 5),
                "familiarity": song_data.get("familiarity", "Medium"),
                "duration": song_data.get("duration", duration),
                "year": 2024,
                "style": [style],
                "source": "GPT-generated",
                "youtube_search_url": make_youtube_link(
                    song_data.get("title", ""), 
                    song_data.get("artist", "")
                )
            }
            generated_songs.append(song)
        
        return generated_songs
        
    except Exception as e:
        st.error(f"GPT song generation error: {e}")
        return []


def generate_with_openai(client, theme, service_type, segment_type, worship_style,
                         praise_style, familiarity, recent_songs, preferred_songs,
                         praise_duration, worship_duration):
    recent_list = parse_song_list(recent_songs)
    preferred_list = parse_song_list(preferred_songs)
    recent_formatted = ", ".join(recent_list) if recent_list else "None specified"
    preferred_formatted = ", ".join(preferred_list) if preferred_list else "None specified"
    max_worship = 2 if "Sunday" in service_type else 3
    
    prompt = f"""You are an expert worship leader. Create a worship plan:

Theme: {theme}
Service: {service_type}
Segment: {segment_type}
Worship Style: {worship_style}
Praise Style: {praise_style}
Familiarity: {familiarity}
Praise: {praise_duration} min | Worship: {worship_duration} min
Max Worship Songs: {max_worship}

PREFERRED SONGS TO CONSIDER: {preferred_formatted}
RECENTLY USED SONGS (deprioritize unless also preferred): {recent_formatted}

Generate:
1. PRAISE MEDLEY ({praise_duration} min, 4-6 upbeat songs for {praise_style})
2. WORSHIP SET ({worship_duration} min, max {max_worship} slow songs for {worship_style})
3. THEME ALIGNMENT
4. TRANSITION NOTES
5. NEW SONG SUGGESTIONS (1-2)
6. REHEARSAL PREPARATION

Prioritize preferred songs when they fit the style. Deprioritize recently used songs unless they are also in the preferred list. Format clearly."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Experienced worship leader creating thoughtful worship plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return None


def filter_songs_by_familiarity(songs, familiarity):
    if familiarity == "Well-known favorites":
        return [s for s in songs if s["familiarity"] == "High"]
    elif familiarity == "Mix of familiar and new":
        return songs
    elif familiarity == "Mostly new songs":
        return [s for s in songs if s["familiarity"] in ["Low", "Medium"]]
    return songs


def filter_songs_by_style(songs, style):
    style_map = {
        "Contemporary Praise": ["Contemporary"], "Contemporary": ["Contemporary"],
        "Gospel Praise": ["Gospel"], "Gospel": ["Gospel"],
        "African Praise": ["African"], "Nigerian Gospel": ["Nigerian Gospel", "African"],
        "Caribbean / Reggae Praise": ["Caribbean", "Reggae"],
        "Afrobeat Praise": ["Afrobeat", "African"],
        "Charismatic Praise": ["Charismatic", "Contemporary"], "Charismatic": ["Charismatic", "Contemporary"],
        "Blended Praise": ["Blended", "Contemporary"], "Blended": ["Blended", "Contemporary"],
        "Traditional Hymns": ["Traditional"], "Liturgical": ["Traditional", "Blended"],
    }
    style_keywords = style_map.get(style, ["Contemporary"])
    return [s for s in songs if any(sk in s.get("style", []) for sk in style_keywords)]


def clean_song_title(title):
    """Clean a potential song title by removing emojis, headings, and non-song text.
    
    Returns the cleaned title or None if it's not a valid song title.
    """
    if not title or not title.strip():
        return None
    
    # Strip whitespace
    cleaned = title.strip()
    
    # Remove emojis (common emoji patterns)
    import re
    # Remove most common emoji ranges
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
        "]+", flags=re.UNICODE)
    cleaned = emoji_pattern.sub('', cleaned).strip()
    
    # Skip if it's a heading or label (common patterns)
    lower_cleaned = cleaned.lower()
    
    # Skip headings like "Praise Songs", "Worship Songs", "Praise:", "Worship:"
    skip_patterns = [
        r'^praise\s*(songs|song)?\s*[:\(]?',
        r'^worship\s*(songs|song)?\s*[:\(]?',
        r'^new\s*(songs|song)?\s*[:\(]?',
        r'^suggested\s*(songs|song)?\s*[:\(]?',
        r'^select',
        r'^choose',
        r'^enter',
        r'^type',
        r'^add',
        r'^include',
    ]
    
    for pattern in skip_patterns:
        if re.match(pattern, lower_cleaned, re.IGNORECASE):
            return None
    
    # Skip if it contains explanatory phrases (too long or has certain keywords)
    explanatory_keywords = [
        'these express', 'these carry', 'these are', 'this expresses',
        'this carries', 'this is', 'for', 'about', 'describing',
        'meaning', 'theme', 'concept', 'idea', 'note', 'notes',
        'example', 'such as', 'including', 'like',
    ]
    
    # If it's a long sentence with explanatory keywords, skip it
    if len(cleaned) > 50 or any(keyword in lower_cleaned for keyword in explanatory_keywords):
        return None
    
    # Skip if it's just a theme description
    theme_words = ['grace', 'redemption', 'healing', 'hope', 'love', 'faith', 'thanksgiving', 
                   'worship', 'praise', 'celebration', 'devotion', 'adoration', 'surrender',
                   'victory', 'joy', 'testimony', 'goodness']
    # If it's a long phrase that's just describing themes, skip it
    if len(cleaned.split()) > 6 and any(word in lower_cleaned for word in theme_words):
        return None
    
    # Parse artist name if separated by dash or em dash
    artist = None
    if ' — ' in cleaned:  # em dash
        parts = cleaned.split(' — ', 1)
        cleaned = parts[0].strip()
        artist = parts[1].strip() if len(parts) > 1 else None
    elif ' - ' in cleaned:  # regular dash with spaces
        parts = cleaned.split(' - ', 1)
        cleaned = parts[0].strip()
        artist = parts[1].strip() if len(parts) > 1 else None
    
    # Remove any remaining parentheses with descriptions
    cleaned = re.sub(r'\s*\([^)]*(express|carry|describe|meaning|theme|note|example|such as)[^)]*\)', '', cleaned, flags=re.IGNORECASE).strip()
    
    # Final check: must have at least 2 characters and not be just numbers
    if len(cleaned) < 2 or cleaned.isdigit():
        return None
    
    return {'title': cleaned, 'artist': artist}


def parse_song_list(songs_str):
    """Parse comma-separated song titles into a clean list of validated song titles.
    
    Returns a list of song title strings (lowercase for matching).
    """
    if not songs_str or not songs_str.strip():
        return []
    
    # Split by comma
    raw_items = songs_str.split(',')
    
    valid_songs = []
    for item in raw_items:
        cleaned = clean_song_title(item)
        if cleaned:
            # Extract just the title string from the dict
            valid_songs.append(cleaned['title'])
    
    return valid_songs


def parse_song_list_with_details(songs_str):
    """Parse comma-separated song titles into a list of song dictionaries with title and optional artist.
    
    Returns a list of dicts: [{'title': str, 'artist': str or None}, ...]
    """
    if not songs_str or not songs_str.strip():
        return []
    
    # Split by comma
    raw_items = songs_str.split(',')
    
    valid_songs = []
    for item in raw_items:
        cleaned = clean_song_title(item)
        if cleaned:
            valid_songs.append(cleaned)
    
    return valid_songs


def find_matching_song(title, song_database):
    """Find a song in the database that matches the given title (partial match)."""
    title_lower = title.lower()
    for song in song_database:
        song_title_lower = song["title"].lower()
        if title_lower in song_title_lower or song_title_lower in title_lower:
            return song
    return None


def classify_song_for_selection(song, preferred_list, recent_list):
    """Classify a song based on preferred and recent lists.
    Returns: (category, match_reason)
    """
    title_lower = song["title"].lower()
    is_preferred = False
    is_recent = False
    
    for pref in preferred_list:
        if pref in title_lower or title_lower in pref:
            is_preferred = True
            break
    
    for recent in recent_list:
        if recent in title_lower or title_lower in recent:
            is_recent = True
            break
    
    if is_preferred and is_recent:
        return 'both', 'Preferred (also recently used)'
    elif is_preferred:
        return 'preferred', 'Preferred'
    elif is_recent:
        return 'recent', 'Recently used (deprioritized)'
    else:
        return 'normal', None


def order_songs_for_praise(songs, medley_instructions=""):
    """Order praise songs for optimal energy flow.
    
    Default flow: High energy → very high energy → peak → slight drop → strong close
    Can be overridden by medley_instructions.
    """
    if not songs:
        return songs
    
    instructions_lower = medley_instructions.lower() if medley_instructions else ""
    
    # Check for custom ordering instructions
    if "start slow" in instructions_lower or "build up" in instructions_lower:
        # Build up: start lower energy, peak in middle, end strong
        sorted_by_energy = sorted(songs, key=lambda x: x.get("energy", 5))
        if len(sorted_by_energy) >= 3:
            # Reorder: low → mid → high → peak → strong
            result = []
            lows = [s for s in sorted_by_energy if s.get("energy", 5) <= 6]
            mids = [s for s in sorted_by_energy if 6 < s.get("energy", 5) <= 8]
            highs = [s for s in sorted_by_energy if s.get("energy", 5) > 8]
            result.extend(lows[:1])
            result.extend(mids[:1])
            result.extend(highs)
            result.extend(mids[1:])
            result.extend(lows[1:])
            return [s for s in result if s in songs]
        return sorted_by_energy
    elif "peak early" in instructions_lower or "start high" in instructions_lower:
        # Start at peak, then maintain
        return sorted(songs, key=lambda x: x.get("energy", 5), reverse=True)
    elif "african" in instructions_lower and "high energy" in instructions_lower:
        # Put African songs first if instructed
        african_songs = [s for s in songs if any(st in str(s.get("style", [])) for st in ["African", "Afrobeat", "Nigerian"])]
        other_songs = [s for s in songs if s not in african_songs]
        african_sorted = sorted(african_songs, key=lambda x: x.get("energy", 5), reverse=True)
        other_sorted = sorted(other_songs, key=lambda x: x.get("energy", 5), reverse=True)
        return african_sorted + other_sorted
    else:
        # Default: High energy → very high energy → peak → slight drop → strong close
        # Sort by energy descending but with some variation for natural flow
        sorted_songs = sorted(songs, key=lambda x: x.get("energy", 5), reverse=True)
        
        # Create a more natural arc: start high, build to peak, end strong
        if len(sorted_songs) >= 4:
            # Opening: high energy (not the peak)
            # Middle: build to peak
            # End: strong close
            opening = sorted_songs[1:3]  # High but not peak
            peak = sorted_songs[:1]  # Peak energy
            closing = sorted_songs[3:]  # Remaining, still strong
            
            result = []
            result.extend(opening)
            result.extend(peak)
            result.extend(closing)
            return result
        
        return sorted_songs


def order_songs_for_worship(songs, medley_instructions=""):
    """Order worship songs for optimal spiritual flow.
    
    Default flow: Medium → slow → deep → intimate
    Can be overridden by medley_instructions.
    """
    if not songs:
        return songs
    
    instructions_lower = medley_instructions.lower() if medley_instructions else ""
    
    # Default: build from medium to most intimate
    return sorted(songs, key=lambda x: x.get("energy", 3))


def determine_praise_song_count(praise_duration, target_count=None):
    """Determine the target number of praise songs based on duration.
    
    If target_count is provided, use it. Otherwise, calculate intelligently.
    Average song duration is ~4 minutes, so:
    - 10 min → 3-4 songs
    - 15 min → 4 songs
    - 18 min → 5 songs
    - 20+ min → 5-6 songs
    """
    if target_count is not None and target_count > 0:
        return target_count
    
    # Intelligent calculation based on duration
    if praise_duration <= 12:
        return 3
    elif praise_duration <= 15:
        return 4
    elif praise_duration <= 20:
        return 5
    else:
        return 6


def get_generation_mode(preferred_list, recent_list):
    """Determine which generation mode to use based on user input.
    
    MODE A: Preferred Songs Provided - Use preferred songs as primary source
    MODE B: Recent Songs Remix - Use recently used songs as reusable pool
    MODE C: Full Generation - Generate from internal song pools
    """
    if preferred_list:
        return 'preferred', 'Preferred Songs Mode'
    elif recent_list:
        return 'recent_remix', 'Recent Songs Remix Mode'
    else:
        return 'full_generation', 'Full Generation Mode'


def select_praise_medley(praise_duration, praise_style, familiarity, recent_songs_str, preferred_songs_str, 
                         target_song_count=None, medley_instructions=""):
    """Select praise medley songs with robust fallback logic to always fill the count."""
    recent_list = parse_song_list(recent_songs_str)
    preferred_list = parse_song_list(preferred_songs_str)
    
    # Determine generation mode
    mode, mode_name = get_generation_mode(preferred_list, recent_list)
    
    # Determine target song count - STRICTLY respect user's selection
    song_count = determine_praise_song_count(praise_duration, target_song_count)
    
    # Ensure we always have a valid song count (minimum 1 if user wants songs)
    if song_count <= 0:
        song_count = determine_praise_song_count(praise_duration, None)  # Use auto calculation
    
    # Track selection notes
    selection_notes = {
        'preferred_songs_used': [],
        'recent_songs_used': [],
        'newly_generated': [],
        'preferred_and_recent': [],
        'excluded_preferred': [],
        'total_available': 0,
        'mode_used': mode_name,
        'flow_strategy': '',
        'target_song_count': song_count
    }
    
    used_titles = set()
    selected = []
    
    # STEP 1: Process preferred songs FIRST (highest priority)
    # These are MEDLEY SEGMENTS, not full songs (approx 1.5-2.5 min each)
    if preferred_list:
        for pref in preferred_list:
            matched_song = find_matching_song(pref, PRAISE_SONGS)
            if matched_song and matched_song["title"] not in used_titles:
                # Create a medley segment version (shorter duration)
                segment_song = dict(matched_song)
                segment_song["duration"] = min(segment_song["duration"], 2.0)  # Cap at 2 min for medley
                selected.append(segment_song)
                used_titles.add(matched_song["title"])
                category, reason = classify_song_for_selection(matched_song, preferred_list, recent_list)
                if category == 'both':
                    selection_notes['preferred_and_recent'].append(matched_song["title"])
                else:
                    selection_notes['preferred_songs_used'].append(matched_song["title"])
            elif not matched_song:
                # Custom song not in database - create a medley segment placeholder
                custom_song = {
                    "title": pref.title(),
                    "artist": "Custom",
                    "tempo": "Upbeat",
                    "energy": 7,
                    "key": "C",
                    "duration": 2.0,  # Medley segment duration
                    "year": 2024,
                    "familiarity": "Low",
                    "style": ["Custom"]
                }
                selected.append(custom_song)
                used_titles.add(pref.title().lower())
                selection_notes['preferred_songs_used'].append(pref.title().lower())
    
    # Sort preferred songs by energy for best flow
    selected.sort(key=lambda x: x.get("energy", 5), reverse=True)
    
    # If more preferred songs than count, select the best ones
    if len(selected) > song_count:
        selection_notes['excluded_preferred'] = [s["title"] for s in selected[song_count:]]
        selected = selected[:song_count]
    
    # STEP 2: Fill remaining slots from selected praise style
    if len(selected) < song_count:
        style_songs = filter_songs_by_style(PRAISE_SONGS, praise_style)
        style_songs = [s for s in style_songs if s["title"] not in used_titles]
        style_songs.sort(key=lambda x: x.get("energy", 5), reverse=True)
        
        for song in style_songs:
            if len(selected) >= song_count:
                break
            selected.append(song)
            used_titles.add(song["title"])
            if song["title"] not in selection_notes.get('preferred_songs_used', []) and \
               song["title"] not in selection_notes.get('preferred_and_recent', []):
                selection_notes['newly_generated'].append(song["title"])
    
    # STEP 3: Fill remaining slots from general praise pool (all styles)
    if len(selected) < song_count:
        general_songs = [s for s in PRAISE_SONGS if s["title"] not in used_titles]
        general_songs.sort(key=lambda x: x.get("energy", 5), reverse=True)
        
        for song in general_songs:
            if len(selected) >= song_count:
                break
            selected.append(song)
            used_titles.add(song["title"])
            if song["title"] not in selection_notes.get('preferred_songs_used', []) and \
               song["title"] not in selection_notes.get('preferred_and_recent', []):
                selection_notes['newly_generated'].append(song["title"])
    
    # STEP 4: Final fallback - create placeholder songs if still not enough
    if len(selected) < song_count:
        placeholder_count = song_count - len(selected)
        for i in range(placeholder_count):
            placeholder = {
                "title": f"Praise Song {len(selected) + i + 1}",
                "artist": "Various",
                "tempo": "Upbeat",
                "energy": 7,
                "key": "C",
                "duration": 4.0,
                "year": 2024,
                "familiarity": "Medium",
                "style": ["Mixed"]
            }
            selected.append(placeholder)
            selection_notes['newly_generated'].append(placeholder["title"])
    
    # Update total available count
    selection_notes['total_available'] = len(PRAISE_SONGS)
    
    # Apply intelligent ordering based on medley instructions
    ordered_songs = order_songs_for_praise(selected, medley_instructions)
    
    # Ensure exact song count match
    ordered_songs = ordered_songs[:song_count]
    
    # Set flow strategy description
    instructions_lower = medley_instructions.lower() if medley_instructions else ""
    if "start slow" in instructions_lower or "build up" in instructions_lower:
        selection_notes['flow_strategy'] = "Building up: Started lower energy, built to peak in middle, ended strong"
    elif "peak early" in instructions_lower or "start high" in instructions_lower:
        selection_notes['flow_strategy'] = "Peak early: Started at highest energy, maintained momentum"
    elif "african" in instructions_lower and "high energy" in instructions_lower:
        selection_notes['flow_strategy'] = "African-first ordering: Led with African praise songs at high energy"
    else:
        selection_notes['flow_strategy'] = "Natural arc: Started high energy, built to peak, ended with strong close"
    
    total_duration = sum(s["duration"] for s in ordered_songs)
    
    return ordered_songs, total_duration, selection_notes


def select_worship_set(worship_duration, worship_style, familiarity, recent_songs_str, preferred_songs_str, service_type=""):
    """Select worship set songs with preferred song prioritization and recent song deprioritization."""
    recent_list = parse_song_list(recent_songs_str)
    preferred_list = parse_song_list(preferred_songs_str)
    
    # Get songs filtered by style and familiarity
    available = filter_songs_by_style(WORSHIP_SONGS, worship_style)
    available = filter_songs_by_familiarity(available, familiarity)
    
    # Track selection notes
    selection_notes = {
        'preferred_songs_used': [],
        'recent_songs_deprioritized': [],
        'preferred_and_recent': [],
        'total_available': len(available)
    }
    
    # First, check if any preferred songs match the database
    # Preferred songs are ALWAYS included regardless of style/familiarity filters
    preferred_matches = []
    used_titles = set()
    
    for pref in preferred_list:
        matched_song = find_matching_song(pref, WORSHIP_SONGS)
        if matched_song and matched_song["title"] not in used_titles:
            # Always include preferred songs - don't filter by style/familiarity
            preferred_matches.append(matched_song)
            used_titles.add(matched_song["title"])
            category, reason = classify_song_for_selection(matched_song, preferred_list, recent_list)
            if category == 'both':
                selection_notes['preferred_and_recent'].append(matched_song["title"])
            elif category == 'preferred':
                selection_notes['preferred_songs_used'].append(matched_song["title"])
    
    # Remove already used preferred songs from available pool
    available = [s for s in available if s["title"] not in used_titles]
    
    # Classify remaining songs
    classified_songs = []
    for song in available:
        category, reason = classify_song_for_selection(song, preferred_list, recent_list)
        classified_songs.append((song, category, reason))
        if category == 'recent':
            selection_notes['recent_songs_deprioritized'].append(song["title"])
    
    # Sort: preferred first, then by energy (lower energy first for worship)
    priority_order = {'preferred': 0, 'normal': 1, 'recent': 2, 'both': -1}
    classified_songs.sort(key=lambda x: (priority_order.get(x[1], 1), x[0].get("energy", 3)))
    
    max_worship_songs = 2 if "Sunday" in service_type else 3
    
    selected = list(preferred_matches)
    total_duration = sum(s["duration"] for s in selected)
    target_duration = worship_duration
    
    for song, category, reason in classified_songs:
        if len(selected) >= max_worship_songs:
            break
        if total_duration + song["duration"] <= target_duration + 2:
            if song not in selected:
                selected.append(song)
                total_duration += song["duration"]
    
    # Ensure at least 2 songs if possible
    if len(selected) < 2 and len(classified_songs) >= 2:
        for song, category, reason in classified_songs:
            if song not in selected:
                selected.append(song)
                total_duration += song["duration"]
                if len(selected) >= 2:
                    break
    
    return selected, total_duration, selection_notes


def generate_theme_alignment(theme, service_type, praise_songs, worship_songs, praise_style, worship_style):
    alignments = []
    theme_lower = theme.lower()
    
    theme_descriptions = {
        "grace": "The selected songs emphasize God's unmerited favor and transformative grace.",
        "redempt": "The selections focus on Christ's redemptive work on the cross.",
        "praise": "The songs create a progression from exuberant praise to intimate worship.",
        "worship": "The selections guide the congregation into deep communion with God.",
        "heal": "The songs emphasize God's heart to heal and restore.",
        "hope": "The selections point to our living hope in Christ.",
        "love": "The songs explore the depths of God's love through Christ's sacrifice.",
        "faith": "The selections encourage trusting in God's faithfulness.",
        "thank": "The songs create an atmosphere of gratitude.",
        "surrender": "The selections invite the congregation to yield fully to God.",
        "spirit": "The songs create space for the Holy Spirit to move.",
        "cross": "The selections focus on the power of Christ's sacrifice.",
        "resurrection": "The songs celebrate Christ's victory over death.",
    }
    
    matched = False
    for key, desc in theme_descriptions.items():
        if key in theme_lower:
            alignments.append(desc)
            matched = True
            break
    
    if not matched:
        alignments.append(f"The selections support and enhance the theme of '{theme}'.")
    
    if "African" in praise_style or "Nigerian" in praise_style or "Afrobeat" in praise_style:
        alignments.append("The praise medley incorporates African/Afrobeat elements for vibrant energy.")
    elif "Gospel" in praise_style:
        alignments.append("The praise features gospel-influenced songs for a joyful atmosphere.")
    
    alignments.append("The flow moves from celebration to contemplation.")
    alignments.append("Key lyrical themes connect to the service message.")
    
    return alignments


def generate_transitions(praise_songs, worship_songs):
    transitions = []
    
    if praise_songs:
        transitions.append(f"Open with '{praise_songs[0]['title']}' at full energy.")
    
    if len(praise_songs) > 1:
        p1, p2 = praise_songs[0], praise_songs[1]
        if p1["key"] == p2["key"]:
            transitions.append(f"Transition '{p1['title']}' to '{p2['title']}': Same key ({p1['key']}) - use drum fill.")
        else:
            transitions.append(f"Transition '{p1['title']}' ({p1['key']}) to '{p2['title']}' ({p2['key']}): Use modulation.")
    
    if len(praise_songs) > 2:
        transitions.append("Between upbeat songs, maintain momentum with minimal pauses.")
    
    if praise_songs and worship_songs:
        transitions.append(f"Transition to worship: After '{praise_songs[-1]['title']}', allow 3-5 seconds silence before '{worship_songs[0]['title']}'.")
        transitions.append("Consider a brief invitation to worship during the transition.")
    
    if len(worship_songs) > 1:
        transitions.append(f"Between '{worship_songs[0]['title']}' and '{worship_songs[1]['title']}': Use soft instrumental bridge.")
        transitions.append("Consider sharing brief scripture between worship songs.")
    
    transitions.append("Use consistent pad/ambient sounds throughout.")
    transitions.append("Volume: praise ~85-90dB, worship ~75-80dB.")
    
    return transitions


def generate_rehearsal_notes(praise_songs, worship_songs, theme, praise_style, worship_style):
    notes = [
        "Review all song keys and create a master chart.",
        "Practice transitions, especially tempo changes.",
        "Ensure vocalists know their parts and harmonies.",
        f"Discuss the theme of '{theme}' with the team.",
    ]
    
    if "African" in praise_style or "Nigerian" in praise_style:
        notes.append("For African/Afrobeat: Focus on groove - feel over perfect notes.")
        notes.append("Consider adding percussion (djembe, shaker).")
    elif "Gospel" in praise_style:
        notes.append("For Gospel: Emphasize soulful delivery and ad-libs.")
    elif "Caribbean" in praise_style or "Reggae" in praise_style:
        notes.append("For Reggae: Focus on off-beat rhythm and relaxed feel.")
    
    if "Traditional" in worship_style:
        notes.append("For traditional hymns: Respect the classic feel.")
    
    if praise_songs:
        keys = set(s["key"] for s in praise_songs)
        if len(keys) > 4:
            notes.append("Note: Multiple keys - practice transitions or transpose.")
    
    notes.extend([
        "Sound check: Balance vocals prominently.",
        "Prepare special arrangements in advance.",
        "Assign someone to cue lyrics/screens.",
        "Run through the full set at least twice.",
    ])
    
    return notes


def make_youtube_link(title, artist):
    """Create a YouTube search link for a song."""
    query = f"{title} {artist}"
    encoded = urllib.parse.quote(query)
    return f"https://www.youtube.com/results?search_query={encoded}"


def format_plan_output(plan, use_ai=False):
    if use_ai and isinstance(plan, str):
        st.markdown(plan.replace("\n", "  \n"))
        return
    
    # Praise Medley
    st.markdown('<div class="section-header praise">🎉 PRAISE MEDLEY</div>', unsafe_allow_html=True)
    praise_info = plan.get('praise_medley', {})
    st.markdown(f"""
    <div class="info-box">
        <strong>⏱ Duration:</strong> {praise_info.get('total_duration', 0):.1f} min &nbsp;|&nbsp; 
        <strong>🎵 Songs:</strong> {praise_info.get('song_count', 0)} &nbsp;|&nbsp;
        <strong>⚡ Style:</strong> {plan.get('praise_style', 'Contemporary')}
    </div>""", unsafe_allow_html=True)
    
    for i, song in enumerate(praise_info.get('songs', []), 1):
        yt_link = make_youtube_link(song['title'], song['artist'])
        st.markdown(f"""
        <div class="card praise-card"><div class="song-item">
            <span class="song-number">{i}</span>
            <span class="song-title">{song['title']}</span>
            <span class="duration-badge">{song['duration']:.1f} min</span>
            <div class="song-meta">
                <strong>Artist:</strong> {song['artist']} &nbsp;|&nbsp;
                <strong>Key:</strong> {song['key']} &nbsp;|&nbsp;
                <strong>Tempo:</strong> {song['tempo']} &nbsp;|&nbsp;
                <strong>Energy:</strong> {'⚡' * min(5, max(1, song.get('energy', 5) // 2))} &nbsp;|&nbsp;
                <strong>Familiarity:</strong> {song['familiarity']}
            </div>
            <div><a href="{yt_link}" target="_blank" class="youtube-link">▶ Listen / Search on YouTube</a></div>
        </div></div>""", unsafe_allow_html=True)
    
    # Worship Set
    st.markdown('<div class="section-header worship">🙏 WORSHIP SET</div>', unsafe_allow_html=True)
    worship_info = plan.get('worship_set', {})
    st.markdown(f"""
    <div class="info-box">
        <strong>⏱ Duration:</strong> {worship_info.get('total_duration', 0):.1f} min &nbsp;|&nbsp; 
        <strong>🎵 Songs:</strong> {worship_info.get('song_count', 0)} &nbsp;|&nbsp;
        <strong>🕊 Style:</strong> {plan.get('worship_style', 'Contemporary')}
    </div>""", unsafe_allow_html=True)
    
    for i, song in enumerate(worship_info.get('songs', []), 1):
        yt_link = make_youtube_link(song['title'], song['artist'])
        st.markdown(f"""
        <div class="card worship-card"><div class="song-item">
            <span class="song-number">{i}</span>
            <span class="song-title">{song['title']}</span>
            <span class="duration-badge">{song['duration']:.1f} min</span>
            <div class="song-meta">
                <strong>Artist:</strong> {song['artist']} &nbsp;|&nbsp;
                <strong>Key:</strong> {song['key']} &nbsp;|&nbsp;
                <strong>Tempo:</strong> {song['tempo']} &nbsp;|&nbsp;
                <strong>Energy:</strong> {'⚡' * min(5, max(1, song.get('energy', 5) // 2))} &nbsp;|&nbsp;
                <strong>Familiarity:</strong> {song['familiarity']}
            </div>
            <div><a href="{yt_link}" target="_blank" class="youtube-link">▶ Listen / Search on YouTube</a></div>
        </div></div>""", unsafe_allow_html=True)
    
    # New Song Suggestions (moved after Worship Set)
    if plan.get('new_suggestions', []):
        st.markdown('<div class="section-header new-songs">✨ New Song Suggestions</div>', unsafe_allow_html=True)
        for song in plan['new_suggestions']:
            yt_link = make_youtube_link(song['title'], song['artist'])
            st.markdown(f"""
            <div class="card"><div class="song-item">
                <span class="song-title">{song['title']} <span class="new-badge">NEW</span></span>
                <div class="song-meta"><strong>Artist:</strong> {song['artist']} ({song['year']}) &nbsp;|&nbsp; <strong>Style:</strong> {song['style']}</div>
                <div><a href="{yt_link}" target="_blank" class="youtube-link">▶ Listen / Search on YouTube</a></div>
            </div></div>""", unsafe_allow_html=True)
    
    # Theme Alignment
    st.markdown('<div class="section-header theme">📖 Theme Alignment</div>', unsafe_allow_html=True)
    st.markdown('<div class="card theme-card">', unsafe_allow_html=True)
    for a in plan.get('theme_alignment', []):
        st.markdown(f'<div class="bullet-point">{a}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Selection Notes
    selection_notes = plan.get('selection_notes', {})
    if selection_notes:
        st.markdown('<div class="section-header selection">📝 Selection Notes</div>', unsafe_allow_html=True)
        st.markdown('<div class="card selection-notes">', unsafe_allow_html=True)
        
        praise_notes = selection_notes.get('praise', {})
        if praise_notes:
            st.markdown('<strong>Praise Medley:</strong>', unsafe_allow_html=True)
            
            # Mode Used
            if praise_notes.get('mode_used'):
                st.markdown(f'<div class="bullet-point">🎯 Mode: {praise_notes["mode_used"]}</div>', unsafe_allow_html=True)
            
            # Source Breakdown
            st.markdown('<strong style="margin-top: 0.5rem; display: inline-block;">Source Breakdown:</strong>', unsafe_allow_html=True)
            if praise_notes.get('preferred_songs_used'):
                st.markdown(f'<div class="bullet-point">✅ {len(praise_notes["preferred_songs_used"])} from Preferred Songs: {", ".join(praise_notes["preferred_songs_used"])}</div>', unsafe_allow_html=True)
            if praise_notes.get('preferred_and_recent'):
                st.markdown(f'<div class="bullet-point">⭐ {len(praise_notes["preferred_and_recent"])} Prioritized (Preferred + Recent): {", ".join(praise_notes["preferred_and_recent"])}</div>', unsafe_allow_html=True)
            if praise_notes.get('recent_songs_used'):
                st.markdown(f'<div class="bullet-point">🔄 {len(praise_notes["recent_songs_used"])} from Recent Songs (remixed): {", ".join(praise_notes["recent_songs_used"])}</div>', unsafe_allow_html=True)
            if praise_notes.get('newly_generated'):
                st.markdown(f'<div class="bullet-point">🆕 {len(praise_notes["newly_generated"])} newly generated from song pool</div>', unsafe_allow_html=True)
            
            # Flow Strategy
            if praise_notes.get('flow_strategy'):
                st.markdown(f'<div class="bullet-point">🌊 Flow: {praise_notes["flow_strategy"]}</div>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="bullet-point">📊 Total songs available after filtering: {praise_notes.get("total_available", 0)}</div>', unsafe_allow_html=True)
        
        worship_notes = selection_notes.get('worship', {})
        if worship_notes:
            st.markdown('<strong style="margin-top: 0.5rem; display: inline-block;">Worship Set:</strong>', unsafe_allow_html=True)
            if worship_notes.get('preferred_songs_used'):
                st.markdown(f'<div class="bullet-point">✅ From Preferred Songs: {", ".join(worship_notes["preferred_songs_used"])}</div>', unsafe_allow_html=True)
            if worship_notes.get('preferred_and_recent'):
                st.markdown(f'<div class="bullet-point">⭐ Prioritized (Preferred + Recently Used): {", ".join(worship_notes["preferred_and_recent"])}</div>', unsafe_allow_html=True)
            if worship_notes.get('recent_songs_deprioritized'):
                st.markdown(f'<div class="bullet-point">⬇️ Deprioritized (Recently Used): {", ".join(worship_notes["recent_songs_deprioritized"])}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bullet-point">📊 Total songs available after filtering: {worship_notes.get("total_available", 0)}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Transitions
    st.markdown('<div class="section-header transition">🔄 Transition Notes</div>', unsafe_allow_html=True)
    st.markdown('<div class="card transition-card">', unsafe_allow_html=True)
    for t in plan.get('transitions', []):
        st.markdown(f'<div class="bullet-point">{t}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Rehearsal Notes
    st.markdown('<div class="section-header rehearsal">🎵 Rehearsal Preparation</div>', unsafe_allow_html=True)
    st.markdown('<div class="card rehearsal-card">', unsafe_allow_html=True)
    for n in plan.get('rehearsal_notes', []):
        st.markdown(f'<div class="bullet-point">✓ {n}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="main-header">🎵 WorshipFlow AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">AI-Powered Worship Planning for Modern Churches</div>', unsafe_allow_html=True)
    
    openai_client = get_openai_client()
    
    with st.sidebar:
        st.markdown("### ⚙️ Service Settings")
        st.markdown("---")
        
        theme = st.text_input("📖 Service Theme", placeholder="e.g., Grace, Redemption, Healing", help="Main theme of your service")
        
        col1, col2 = st.columns(2)
        with col1:
            service_type = st.selectbox("🏛 Service Type", ["Sunday Morning", "Sunday Evening", "Wednesday Night", "Special Event", "Youth Service", "Contemporary Service", "Traditional Service"])
        with col2:
            segment_type = st.selectbox("📋 Segment Type", ["Full Service", "Opening Praise & Worship", "Response Time", "Communion Service"])
        
        st.markdown("---")
        
        worship_style = st.selectbox("🕊 Worship Style (Worship Set)", ["Contemporary", "Traditional Hymns", "Blended", "Gospel", "Charismatic", "Liturgical"])
        praise_style = st.selectbox("⚡ Praise Style (Praise Medley)", ["Contemporary Praise", "African Praise", "Gospel Praise", "Nigerian Gospel", "Caribbean / Reggae Praise", "Afrobeat Praise", "Charismatic Praise", "Blended Praise"])
        
        st.markdown("---")
        
        familiarity = st.selectbox("👥 Familiarity Preference", ["Well-known favorites", "Mix of familiar and new", "Mostly new songs"])
        
        # Preferred Praise Songs input
        preferred_praise_songs = st.text_area(
            "🔥 Preferred Praise Songs",
            placeholder="Enter praise song titles you'd like to include, separated by commas (e.g., Awesome God, Raise a Hallelujah, Victory)",
            height=80,
            help="Add praise songs you would like to include in the praise medley."
        )
        
        # Preferred Worship Songs input
        preferred_worship_songs = st.text_area(
            "🌿 Preferred Worship Songs",
            placeholder="Enter worship song titles you'd like to include, separated by commas (e.g., Goodness of God, Jireh, No Longer Slaves)",
            height=80,
            help="Add worship songs you would like to include in the worship set."
        )
        
        # Medley Instructions input
        medley_instructions = st.text_area(
            "📝 Medley Instructions / Leader Notes",
            placeholder="Optional: Describe the flow, transitions, energy, or specific direction (e.g., 'start high energy, include African praise, transition into deep worship')",
            height=80,
            help="Optional: Describe the flow, transitions, energy, or specific direction you want for this set."
        )
        
        # Recently Used Songs input
        recent_songs = st.text_area(
            "🕐 Recently Used Songs (Reference Pool)",
            placeholder="Enter song titles separated by commas, e.g., Yeshua, Iba, Most High, Worthy of It All",
            height=80,
            help="Songs you've used recently. These serve as a reference pool for remixing when no preferred songs are provided."
        )
        
        # Parse preferred songs separately
        preferred_praise_list = parse_song_list(preferred_praise_songs)
        preferred_worship_list = parse_song_list(preferred_worship_songs)
        recent_list = parse_song_list(recent_songs)
        
        # Determine mode based on what's provided
        has_preferred = bool(preferred_praise_list or preferred_worship_list)
        if has_preferred:
            mode, mode_name = 'preferred', 'Preferred Songs Mode'
        elif recent_list:
            mode, mode_name = 'recent_remix', 'Recent Songs Remix Mode'
        else:
            mode, mode_name = 'full_generation', 'Full Generation Mode'
        
        # Display mode indicator
        st.markdown(f'<div style="font-size: 0.8rem; color: #4a6fa5; margin-top: -0.5rem; margin-bottom: 0.25rem;">🎯 Mode: {mode_name}</div>', unsafe_allow_html=True)
        
        # Show parsed praise songs
        if preferred_praise_list:
            st.markdown(f'<div style="font-size: 0.8rem; color: #e67e22; margin-bottom: 0.25rem;">🔥 Praise songs: {", ".join(preferred_praise_list[:5])}{"..." if len(preferred_praise_list) > 5 else ""}</div>', unsafe_allow_html=True)
        
        # Show parsed worship songs
        if preferred_worship_list:
            st.markdown(f'<div style="font-size: 0.8rem; color: #27ae60; margin-bottom: 0.25rem;">🌿 Worship songs: {", ".join(preferred_worship_list[:5])}{"..." if len(preferred_worship_list) > 5 else ""}</div>', unsafe_allow_html=True)
        
        if not has_preferred and recent_list:
            st.markdown(f'<div style="font-size: 0.8rem; color: #e67e22; margin-bottom: 0.25rem;">🔄 Will remix recent songs for fresh flow</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            praise_duration = st.number_input("⏱ Praise Duration (min)", min_value=10, max_value=30, value=18, step=1)
            praise_song_count = st.number_input("🎵 Praise Song Count", min_value=0, max_value=8, value=0, step=1, help="Set to 0 for automatic calculation based on duration, or enter 3-8 for a specific count")
        with col2:
            worship_duration = st.number_input("⏱ Worship Duration (min)", min_value=5, max_value=20, value=10, step=1)
        
        st.markdown("---")
        
        generate_clicked = st.button("🎵 Generate Worship Plan", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        if openai_client:
            st.success("✅ OpenAI API Connected")
        else:
            st.info("📋 Demo Mode Active")
        
        st.markdown("---")
        st.markdown("### About WorshipFlow AI")
        st.markdown("WorshipFlow AI helps worship leaders create thoughtful, themed worship sets in seconds.")
    
    if generate_clicked:
        if not theme:
            st.warning("⚠️ Please enter a service theme.")
        else:
            with st.spinner("🎵 Generating your worship plan..."):
                if openai_client:
                    # For AI mode, combine preferred songs for the prompt
                    all_preferred = ", ".join(preferred_praise_list + preferred_worship_list)
                    ai_result = generate_with_openai(openai_client, theme, service_type, segment_type, worship_style, praise_style, familiarity, recent_songs, all_preferred, praise_duration, worship_duration)
                    if ai_result:
                        st.markdown('<div class="success-banner">✅ Worship plan generated using AI!</div>', unsafe_allow_html=True)
                        st.markdown("---")
                        format_plan_output(ai_result, use_ai=True)
                    else:
                        st.markdown('<div class="warning-banner">⚠️ AI issue. Using fallback mode.</div>', unsafe_allow_html=True)
                        plan = generate_fallback_plan(theme, service_type, segment_type, worship_style, praise_style, familiarity, recent_songs, preferred_praise_songs, preferred_worship_songs, praise_duration, worship_duration)
                        st.markdown("---")
                        format_plan_output(plan)
                else:
                    plan = generate_fallback_plan(theme, service_type, segment_type, worship_style, praise_style, familiarity, recent_songs, preferred_praise_songs, preferred_worship_songs, praise_duration, worship_duration)
                    st.markdown("---")
                    format_plan_output(plan)
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("📋 Copy to Clipboard", use_container_width=True)
                with col2:
                    st.button("📄 Download as Text", use_container_width=True)
                with col3:
                    st.button("🔄 Generate New Plan", use_container_width=True)
    
    st.markdown('<div class="footer">WorshipFlow AI v3.0 | Built with ❤️ for worship leaders<div class="footer-quote">"Sing to the Lord a new song; sing to the Lord, all the earth." - Psalm 96:1</div></div>', unsafe_allow_html=True)


def generate_fallback_plan(theme, service_type, segment_type, worship_style, praise_style, familiarity, recent_songs, preferred_praise_songs, preferred_worship_songs, praise_duration, worship_duration):
    # Praise medley only uses preferred praise songs
    praise_songs, praise_total, praise_notes = select_praise_medley(praise_duration, praise_style, familiarity, recent_songs, preferred_praise_songs)
    # Worship set only uses preferred worship songs
    worship_songs, worship_total, worship_notes = select_worship_set(worship_duration, worship_style, familiarity, recent_songs, preferred_worship_songs, service_type)
    
    theme_lower = theme.lower()
    theme_suggestions = THEME_SONGS.get("default", [])
    for key in THEME_SONGS:
        if key in theme_lower:
            theme_suggestions = THEME_SONGS[key]
            break
    
    new_song_suggestions = random.sample(NEW_SONGS, min(2, len(NEW_SONGS)))
    
    return {
        "praise_medley": {"songs": praise_songs, "total_duration": praise_total, "song_count": len(praise_songs)},
        "worship_set": {"songs": worship_songs, "total_duration": worship_total, "song_count": len(worship_songs)},
        "praise_style": praise_style,
        "worship_style": worship_style,
        "theme_alignment": generate_theme_alignment(theme, service_type, praise_songs, worship_songs, praise_style, worship_style),
        "transitions": generate_transitions(praise_songs, worship_songs),
        "new_suggestions": new_song_suggestions,
        "rehearsal_notes": generate_rehearsal_notes(praise_songs, worship_songs, theme, praise_style, worship_style),
        "selection_notes": {
            "praise": praise_notes,
            "worship": worship_notes
        }
    }


if __name__ == "__main__":
    main()