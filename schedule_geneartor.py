#!/usr/bin/env python3
"""
Conference Schedule Generator - OPTIMIZED VERSION
Generates HTML schedule from metadata. Events automatically calculate their start times 
from previous event end times. You only specify the first event time for each day!

Usage:
    python3 schedule_generator.py

This will create schedule.html based on the metadata in SCHEDULE_METADATA.
"""

from datetime import datetime, timedelta
from typing import List, Dict

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

# Pixel-to-minute mapping
PX_PER_MINUTE = 0.93
SCHEDULE_START_HOUR = 9
SCHEDULE_START_MINUTE = 30
SCHEDULE_END_HOUR = 22
SCHEDULE_END_MINUTE = 0

TOTAL_MINUTES = (SCHEDULE_END_HOUR * 60 + SCHEDULE_END_MINUTE) - (SCHEDULE_START_HOUR * 60 + SCHEDULE_START_MINUTE)
TOTAL_HEIGHT_PX = 900

COLOR_CLASSES = {
    'monday': 'bg-monday', 'tuesday': 'bg-tuesday', 'wednesday': 'bg-wednesday',
    'thursday': 'bg-thursday', 'friday': 'bg-friday', 'coffee': 'bg-coffee',
    'lunch': 'bg-lunch', 'session1': 'bg-session1', 'session2': 'bg-session2',
    'break': 'bg-break', 'evening': 'bg-evening', 'checkin': 'bg-checkin',
    'transport': 'bg-transport', 'presentation': 'bg-presentation',
}

# ============================================================================
# METADATA CONFIGURATION - EDIT THIS TO CHANGE THE SCHEDULE
# ============================================================================

SCHEDULE_METADATA = {
    "conference_title": "SOTA Conference 2025",
    "conference_dates": "November 25-29, 2025",
    "days": [
        {
            "day_name": "Monday",
            "date": "25th",
            "start_time": "09:30",  # Only specify this! Rest calculate automatically.
            "events": [
                {
                    "title": "Visita CVC",
                    "duration_minutes": 90,
                    "color": "monday",
                    "link": "TBA"
                },
                {
                    "title": "Transport to Vall de Núria",
                    "duration_minutes": 60,
                    "color": "transport",
                    "link": "TBA"
                },
                {
                    "title": "Check In",
                    "duration_minutes": 30,
                    "color": "checkin",
                    "link": "TBA"
                },
                {
                    "title": "Lunch",
                    "duration_minutes": 45,
                    "color": "lunch",
                    "link": "TBA"
                },
                {
                    "title": "Break the Ice",
                    "duration_minutes": 45,
                    "color": "break",
                    "link": "TBA"
                },
                {
                    "title": "Coffee",
                    "duration_minutes": 30,
                    "color": "coffee",
                    "link": "TBA"
                },
                {
                    "title": "Intro SOTA",
                    "duration_minutes": 30,
                    "color": "session2",
                    "link": "TBA"
                },
                {
                    "title": "Social Activities",
                    "duration_minutes": 90,
                    "color": "evening",
                    "link": "TBA"
                },
                {
                    "title": "Dinner",
                    "duration_minutes": 60,
                    "color": "lunch",
                    "link": "TBA"
                }
            ]
        },
        {
            "day_name": "Tuesday",
            "date": "26th",
            "start_time": "9:30",
            "events": [
                {"title": "Vision and Language", "duration_minutes": 90, "color": "tuesday", "link": "TBA"},
                {"title": "Coffee", "duration_minutes": 30, "color": "coffee", "link": "TBA"},
                {"title": "Foundation Models", "duration_minutes": 90, "color": "tuesday", "link": "TBA"},
                {"title": "Lab Session - VLMs", "duration_minutes": 30, "color": "session1", "link": "TBA"},
                {"title": "Lunch", "duration_minutes": 60, "color": "lunch", "link": "TBA"},
                {"title": "Student Presentations", "duration_minutes": 60, "color": "break", "link": "TBA"},
                {"title": "Coffee", "duration_minutes": 30, "color": "coffee", "link": "TBA"},
                {"title": "Student Poster Session", "duration_minutes": 90, "color": "break", "link": "TBA"},
                {"title": "Social Activities", "duration_minutes": 90, "color": "evening", "link": "TBA"},
                {"title": "Dinner", "duration_minutes": 90, "color": "lunch", "link": "TBA"}
            ]
        },
        {
            "day_name": "Wednesday",
            "date": "27th",
            "start_time": "9:30",
            "events": [
                {"title": "Hiking", "duration_minutes": 240, "color": "wednesday", "link": "TBA", "font_weight": "bold"},
                {"title": "Lunch", "duration_minutes": 60, "color": "lunch", "link": "TBA"},
                {"title": "Trends on Trustworthy Doc Analysis", "duration_minutes": 30, "color": "session2", "link": "TBA"},
                {"title": "Coffee", "duration_minutes": 30, "color": "coffee", "link": "TBA"},
                {"title": "Learning on Graphs: GNNs in Document Analysis", "duration_minutes": 90, "color": "session2", "link": "TBA"},
                {"title": "Lab Session - GNNs (includes coffee)", "duration_minutes": 60, "color": "session1", "link": "TBA"},
                {"title": "Open Lab: Finetuning A Low Resource VLM with synthetic Data", "duration_minutes": 60, "color": "evening", "link": "TBA"},
                {"title": "Dinner", "duration_minutes": 90, "color": "lunch", "link": "TBA"}
            ]
        },
        {
            "day_name": "Thursday",
            "date": "28th",
            "start_time": "9:30",
            "events": [
                {"title": "Knowledge Graph Embeddings and Knowledge Representation", "duration_minutes": 90, "color": "thursday", "link": "TBA"},
                {"title": "Coffee", "duration_minutes": 30, "color": "coffee", "link": "TBA"},
                {"title": "Agentic: RAG, GraphRAG & Co.", "duration_minutes": 30, "color": "thursday", "link": "TBA"},
                {"title": "Lab Session - Agentic GraphRAG", "duration_minutes": 90, "color": "session1", "link": "TBA"},
                {"title": "Lunch", "duration_minutes": 60, "color": "lunch", "link": "TBA"},
                {"title": "Trends on Historical Doc Analysis", "duration_minutes": 60, "color": "session2", "link": "TBA"},
                {"title": "Coffee", "duration_minutes": 30, "color": "coffee", "link": "TBA"},
                {"title": "Open Lab: Building A Knowledge Graph from a finetuned VLM", "duration_minutes": 90, "color": "session1", "link": "TBA"},
                {"title": "Gala Dinner", "duration_minutes": 90, "color": "evening", "link": "TBA", "font_weight": "bold", "font_size": "1.05rem"}
            ]
        },
        {
            "day_name": "Friday",
            "date": "29th",
            "start_time": "9:30",
            "events": [
                {"title": "Open Lab: Results Presentation", "duration_minutes": 90, "color": "presentation", "link": "TBA"},
                {"title": "Closing Ceremony", "duration_minutes": 30, "color": "thursday", "link": "TBA"},
                {"title": "Transport to Vall de Núria", "duration_minutes": 600, "color": "transport", "link": "TBA"}
            ]
        }
    ]
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def time_to_minutes(time_str: str) -> int:
    """Convert HH:MM format to minutes since start of day."""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_offset_px(minutes_since_schedule_start: int) -> float:
    """Convert minutes since schedule start to pixel offset."""
    return minutes_since_schedule_start * PX_PER_MINUTE

def duration_to_height_px(duration_minutes: int) -> float:
    """Convert duration in minutes to height in pixels."""
    return duration_minutes * PX_PER_MINUTE

def calculate_event_position(event_start_time: str) -> tuple:
    """Calculate the top position (px) and time offset for an event."""
    event_minutes = time_to_minutes(event_start_time)
    schedule_start_minutes = time_to_minutes(f"{SCHEDULE_START_HOUR:02d}:{SCHEDULE_START_MINUTE:02d}")
    minutes_since_start = event_minutes - schedule_start_minutes
    top_px = minutes_to_offset_px(minutes_since_start)
    return top_px, minutes_since_start

# ============================================================================
# HTML GENERATION
# ============================================================================

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
:root {{
  --color-white: rgba(255, 255, 255, 1);
  --color-black: rgba(0, 0, 0, 1);
  --color-cream-50: rgba(252, 252, 249, 1);
  --color-cream-100: rgba(255, 255, 253, 1);
  --color-gray-200: rgba(245, 245, 245, 1);
  --color-gray-300: rgba(167, 169, 169, 1);
  --color-gray-400: rgba(119, 124, 124, 1);
  --color-slate-500: rgba(98, 108, 113, 1);
  --color-brown-600: rgba(94, 82, 64, 1);
  --color-charcoal-700: rgba(31, 33, 33, 1);
  --color-charcoal-800: rgba(38, 40, 40, 1);
  --color-slate-900: rgba(19, 52, 59, 1);
  --color-teal-300: rgba(50, 184, 198, 1);
  --color-teal-400: rgba(45, 166, 178, 1);
  --color-teal-500: rgba(33, 128, 141, 1);
  --color-teal-600: rgba(29, 116, 128, 1);
  --color-teal-700: rgba(26, 104, 115, 1);
  --color-teal-800: rgba(41, 150, 161, 1);
  --color-red-400: rgba(255, 84, 89, 1);
  --color-red-500: rgba(192, 21, 47, 1);
  --color-orange-400: rgba(230, 129, 97, 1);
  --color-orange-500: rgba(168, 75, 47, 1);

  --color-brown-600-rgb: 94, 82, 64;
  --color-teal-500-rgb: 33, 128, 141;
  --color-slate-900-rgb: 19, 52, 59;
  --color-slate-500-rgb: 98, 108, 113;
  --color-red-500-rgb: 192, 21, 47;
  --color-red-400-rgb: 255, 84, 89;
  --color-orange-500-rgb: 168, 75, 47;
  --color-orange-400-rgb: 230, 129, 97;

  --color-background: var(--color-cream-50);
  --color-surface: var(--color-cream-100);
  --color-text: var(--color-slate-900);
  --color-text-secondary: var(--color-slate-500);
  --color-primary: var(--color-teal-500);
  --color-primary-hover: var(--color-teal-600);
  --color-primary-active: var(--color-teal-700);
  --color-secondary: rgba(var(--color-brown-600-rgb), 0.12);
  --color-secondary-hover: rgba(var(--color-brown-600-rgb), 0.2);
  --color-secondary-active: rgba(var(--color-brown-600-rgb), 0.25);
  --color-border: rgba(var(--color-brown-600-rgb), 0.2);
  --color-btn-primary-text: var(--color-cream-50);
  --color-card-border: rgba(var(--color-brown-600-rgb), 0.12);
  --color-card-border-inner: rgba(var(--color-brown-600-rgb), 0.12);
  --color-error: var(--color-red-500);
  --color-success: var(--color-teal-500);
  --color-warning: var(--color-orange-500);
  --color-info: var(--color-slate-500);
  --color-focus-ring: rgba(var(--color-teal-500-rgb), 0.4);
  --color-select-caret: rgba(var(--color-slate-900-rgb), 0.8);

  --font-family-base: "FKGroteskNeue", "Geist", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-family-mono: "Berkeley Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  --font-size-xs: 11px;
  --font-size-sm: 12px;
  --font-size-base: 14px;
  --font-size-md: 14px;
  --font-size-lg: 16px;
  --font-size-xl: 18px;
  --font-size-2xl: 20px;
  --font-size-3xl: 24px;
  --font-size-4xl: 30px;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 550;
  --font-weight-bold: 600;
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --letter-spacing-tight: -0.01em;

  --space-0: 0;
  --space-1: 1px;
  --space-2: 2px;
  --space-4: 4px;
  --space-6: 6px;
  --space-8: 8px;
  --space-10: 10px;
  --space-12: 12px;
  --space-16: 16px;
  --space-20: 20px;
  --space-24: 24px;
  --space-32: 32px;

  --radius-sm: 6px;
  --radius-base: 8px;
  --radius-md: 10px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.02);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02);

  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --ease-standard: cubic-bezier(0.16, 1, 0.3, 1);
}}

@font-face {{
  font-family: 'FKGroteskNeue';
  src: url('https://r2cdn.perplexity.ai/fonts/FKGroteskNeue.woff2') format('woff2');
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: var(--font-family-base);
  background-color: var(--color-background);
  color: var(--color-text);
  line-height: var(--line-height-normal);
  padding: var(--space-20);
  -webkit-font-smoothing: antialiased;
}}

.header {{
  text-align: center;
  margin-bottom: var(--space-32);
}}

.header h1 {{
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin-bottom: var(--space-8);
  letter-spacing: var(--letter-spacing-tight);
}}

.header p {{
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}}

.schedule-container {{
  max-width: 1400px;
  margin: 0 auto;
  overflow-x: auto;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--space-20);
}}

.schedule-grid {{
  display: grid;
  grid-template-columns: 105px repeat(5, 1fr);
  gap: var(--space-8);
  min-width: 900px;
}}

.time-column {{
  position: relative;
}}

.time-label {{
  height: 45px;
  display: flex;
  align-items: center;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
  padding-left: var(--space-8);
  background: rgba(var(--color-brown-600-rgb), 0.03);
  border-radius: var(--radius-sm);
  margin-bottom: var(--space-2);
}}

.day-column {{
  position: relative;
  min-height: {total_height_px}px;
}}

.day-header {{
  position: sticky;
  top: 0;
  background: #114e71;
  color: var(--color-white);
  padding: var(--space-12);
  text-align: center;
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-base);
  border-radius: var(--radius-base);
  margin-bottom: var(--space-16);
  z-index: 10;
  box-shadow: var(--shadow-sm);
}}

.events-container {{
  position: relative;
  height: {total_height_px}px;
  background: rgba(var(--color-brown-600-rgb), 0.02);
  border-radius: var(--radius-base);
}}

.event {{
  position: absolute;
  left: 0;
  right: 0;
  padding: var(--space-8) var(--space-10);
  border-left: 5px solid #114e71;
  border-radius: 7px;
  box-shadow: var(--shadow-sm);
  font-size: var(--font-size-sm);
  line-height: 1.3;
  overflow: hidden;
  transition: transform var(--duration-fast) var(--ease-standard), box-shadow var(--duration-fast) var(--ease-standard);
  cursor: pointer;
}}

.event:hover {{
  transform: translateX(2px);
  box-shadow: var(--shadow-md);
  z-index: 5;
}}

.event a {{
  color: inherit;
  text-decoration: none;
  display: block;
}}

.event a:hover {{
  text-decoration: underline;
}}

.event-time {{
  display: none;
  font-size: calc(var(--font-size-xs) - 1px);
  opacity: 0.8;
  margin-top: var(--space-4);
  font-weight: var(--font-weight-semibold);
}}

.event:hover .event-time {{
  display: block;
}}

.bg-monday {{ background: #e8f4f8; color: #114e71; }}
.bg-tuesday {{ background: #fef3e8; color: #8b5a00; }}
.bg-wednesday {{ background: #e8f8f0; color: #0d5c2e; }}
.bg-thursday {{ background: #f5e8f8; color: #5a1070; }}
.bg-friday {{ background: #ffeef0; color: #8b1a2e; }}
.bg-coffee {{ background: #f5f0e8; color: #6b5a3d; }}
.bg-lunch {{ background: #ffe8dc; color: #8b4000; }}
.bg-session1 {{ background: #ffe8f0; color: #8b0040; }}
.bg-session2 {{ background: #e0f0ff; color: #00457a; }}
.bg-break {{ background: #fffae8; color: #8b7500; }}
.bg-evening {{ background: #f0e8ff; color: #4a0080; }}
.bg-checkin {{ background: #eeeeee; color: #4a4a4a; }}
.bg-transport {{ background: #f8f8f8; color: #666666; }}
.bg-presentation {{ background: #fff9e0; color: #8b7000; }}

@media (max-width: 1024px) {{
  .schedule-grid {{ grid-template-columns: 90px repeat(5, 1fr); min-width: 800px; }}
  .time-label {{ font-size: var(--font-size-xs); padding-left: var(--space-4); }}
  .day-header {{ font-size: var(--font-size-sm); padding: var(--space-8); }}
  .event {{ font-size: var(--font-size-xs); padding: var(--space-6) var(--space-8); }}
}}

@media (max-width: 768px) {{
  body {{ padding: var(--space-12); }}
  .header h1 {{ font-size: var(--font-size-3xl); }}
  .header p {{ font-size: var(--font-size-base); }}
  .schedule-container {{ padding: var(--space-12); }}
  .schedule-grid {{ grid-template-columns: 75px repeat(5, 1fr); min-width: 700px; gap: var(--space-4); }}
}}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>{dates}</p>
    </div>

    <div class="schedule-container">
        <div class="schedule-grid">
            <div class="time-column">
                <div class="day-header" style="visibility: hidden;">Time</div>
                {time_labels}
            </div>
            {day_columns}
        </div>
    </div>
</body>
</html>
'''

def generate_time_labels() -> str:
    """Generate time labels for the schedule."""
    labels = []
    current_minutes = time_to_minutes(f"{SCHEDULE_START_HOUR:02d}:{SCHEDULE_START_MINUTE:02d}")
    end_minutes = time_to_minutes(f"{SCHEDULE_END_HOUR:02d}:{SCHEDULE_END_MINUTE:02d}")

    while current_minutes <= end_minutes:
        hours = current_minutes // 60
        mins = current_minutes % 60
        label = f'<div class="time-label">{hours:02d}:{mins:02d}</div>'
        labels.append(label)
        current_minutes += 30

    return '\n                '.join(labels)

def generate_events_html(events: List[Dict], day_start_time: str = "09:30") -> str:
    """Generate event divs for a single day.

    Automatically calculates each event's start time from the previous event's end time.
    First event uses day_start_time.
    """
    event_divs = []
    current_time_minutes = time_to_minutes(day_start_time)

    for event in events:
        # Current time is this event's start time
        start_minutes = current_time_minutes
        duration = event['duration_minutes']
        end_minutes = start_minutes + duration

        # Convert minutes back to HH:MM format
        start_hours = start_minutes // 60
        start_mins = start_minutes % 60
        start_time = f"{start_hours:02d}:{start_mins:02d}"

        end_hours = end_minutes // 60
        end_mins = end_minutes % 60
        end_time = f"{end_hours:02d}:{end_mins:02d}"

        # Calculate position and height
        top_px, _ = calculate_event_position(start_time)
        height_px = duration_to_height_px(duration)
        color_class = COLOR_CLASSES.get(event['color'], 'bg-monday')

        # Build style attribute
        style_parts = [f"top: {top_px:.1f}px", f"height: {height_px:.2f}px"]

        # Add optional styling
        if event.get('font_weight'):
            style_parts.append(f"font-weight: {event['font_weight']}")
        if event.get('font_size'):
            style_parts.append(f"font-size: {event['font_size']}")

        style = "; ".join(style_parts)

        event_html = f'''<div class="event {color_class}" style="{style};"><a href="{event['link']}">{event['title']}</a><div class="event-time">{start_time} – {end_time}</div></div>'''
        event_divs.append(event_html)

        # Next event starts when this one ends
        current_time_minutes = end_minutes

    return '\n                    '.join(event_divs)

def generate_day_column(day: Dict) -> str:
    """Generate a complete day column."""
    day_start_time = day.get('start_time', "09:30")
    events_html = generate_events_html(day['events'], day_start_time)

    day_column = f'''<!-- {day['day_name']} Column -->
            <div class="day-column">
                <div class="day-header">{day['day_name']} {day['date']}</div>
                <div class="events-container">
                    {events_html}
                </div>
            </div>'''

    return day_column

def generate_full_html() -> str:
    """Generate the complete HTML document."""
    time_labels = generate_time_labels()
    day_columns = '\n\n            '.join([
        generate_day_column(day) for day in SCHEDULE_METADATA['days']
    ])

    html = HTML_TEMPLATE.format(
        title=SCHEDULE_METADATA['conference_title'],
        dates=SCHEDULE_METADATA['conference_dates'],
        total_height_px=TOTAL_HEIGHT_PX,
        time_labels=time_labels,
        day_columns=day_columns
    )

    return html

# ============================================================================
# MAIN - EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("Generating schedule...")
    html_output = generate_full_html()

    with open("schedule.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"✓ Schedule generated: schedule.html ({len(html_output)} bytes)")
    print()
    print("IMPORTANT CHANGES IN THIS VERSION:")
    print("  • Each day now has a 'start_time' property")
    print("  • Events NO LONGER need 'start_time' - they're calculated!")
    print("  • Just specify 'duration_minutes' for each event")
    print("  • Times auto-calculate: previous_end_time → next_start_time")
    print()
    print("Example:")
    print("""
    {
        "day_name": "Monday",
        "date": "25th",
        "start_time": "09:30",     ← Only time you specify!
        "events": [
            {"title": "Event 1", "duration_minutes": 90, ...},  ← 09:30-11:00
            {"title": "Event 2", "duration_minutes": 60, ...},  ← 11:00-12:00 (auto!)
            {"title": "Event 3", "duration_minutes": 30, ...},  ← 12:00-12:30 (auto!)
        ]
    }
    """)
