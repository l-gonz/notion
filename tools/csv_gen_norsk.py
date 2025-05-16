# Re-import and re-convert after environment reset
# import json
import pandas
from datetime import date, timedelta

# Reconstruct the data from earlier

# Generate the 6-week plan starting from the next Monday
def next_monday(from_date):
    days_ahead = 0 - from_date.weekday() + 7
    return from_date + timedelta(days=days_ahead)

start_date = next_monday(date.today())

# Weekly plan
weekly_plan = [
    {
        "Week #": f"Week {i+1}",
        "Start Date": (start_date + timedelta(weeks=i)).isoformat(),
        "Theme": theme,
        "Goals": goals,
        "Focus Grammar": grammar,
        "Speaking Challenge": speaking,
        "Real-World Task": real_world,
        "Reflection": ""
    }
    for i, (theme, goals, grammar, speaking, real_world) in enumerate([
        ("Comfort & Consistency", 
         "Build routine, reduce anxiety, increase exposure", 
         "Present tense & sentence structure", 
         "Short self-introduction with tutor", 
         "Say one phrase in Norwegian during shopping"),
        ("Comfort & Consistency", 
         "Continue daily habits, start writing more", 
         "Definite/indefinite nouns", 
         "Talk about your weekend", 
         "Ask a coworker a simple question"),
        ("Challenge & Output", 
         "Expand spoken vocabulary, speak longer sentences", 
         "Modal verbs (kan, skal, vil)", 
         "Describe your day unscripted", 
         "Use Norwegian in a full store interaction"),
        ("Challenge & Output", 
         "Reduce mental translation, more free expression", 
         "Subordinate clauses", 
         "Talk about your opinion on something simple", 
         "Start a short convo in Norwegian"),
        ("Immersion Push", 
         "Use mostly Norwegian in daily life", 
         "Adjective agreement & word order", 
         "Tell a story from your life", 
         "Speak Norwegian all day in low-stakes settings"),
        ("Immersion Push", 
         "Natural speech & connectors, spontaneous response", 
         "Past tense (preterite vs present perfect)", 
         "Debate or explain pros/cons of something", 
         "Default to Norwegian for entire day")
    ])
]

# Daily practice routine
weekly_routine = [
    ("Monday", "30 min listening practice (with repeat/shadowing) + 5 min self-talk"),
    ("Tuesday", "15-30 min language exchange + 15 min write a few sentences about your day"),
    ("Wednesday", "15 min read short article/novel + 15 min write short response to it + 5 min note down few words"),
    ("Thursday", "10 min journaling + use Norwegian in public"),
    ("Friday", "Grammar drill (focus of the week) + use grammar with a few sentences"),
    ("Saturday", "Review week vocabulary + 20 min talk to yourself (opt: record it)"),
    ("Sunday", "Watch native content with subtitles + note down some expressions")
]

# Generate practice tracker with instructions
detailed_tracker = []
for week in range(6):
    for i, (day_name, instructions) in enumerate(weekly_routine):
        entry_date = start_date + timedelta(days=week * 7 + i)
        detailed_tracker.append({
            "Date": entry_date.isoformat(),
            "Day": day_name + f" (Week {week + 1})",
            "Practice Focus": instructions,
            "Listening (min)": 0,
            "Speaking (min)": 0,
            "Writing (min)": 0,
            "Vocabulary learned": 0,
            "New phrases used": "",
            "Grammar focus": "",
            "Real-world use?": False,
            "Notes / Reflection": ""
        })

# Convert to DataFrames
weekly_df = pandas.DataFrame(weekly_plan)
practice_df = pandas.DataFrame(detailed_tracker)

# Export to CSV
weekly_csv_path = "./Weekly_Overview.csv"
practice_csv_path = "./Practice_Tracker.csv"

weekly_df.to_csv(weekly_csv_path, index=False)
practice_df.to_csv(practice_csv_path, index=False)

weekly_csv_path, practice_csv_path
