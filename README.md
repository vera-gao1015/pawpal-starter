# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available and priority)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## 📸 Demo

<a href="/course_images/ai110/Demo1.png" target="_blank"><img src='/course_images/ai110/Demo1.png' /></a>
*Pet management and task scheduling interface with dual-column layout*

<a href="/course_images/ai110/Demo2.png" target="_blank"><img src='/course_images/ai110/Demo2.png' /></a>
*Task overview showing sorted, pending, and completed tasks with daily plan generation*

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- Sorts tasks by time so the schedule is easier to read.
- Builds a daily plan based on task priority and available time.
- Shows warnings when two tasks overlap.
- Creates the next daily or weekly task when a recurring task is completed.
- Lets you view tasks by pet or by completion status.
- Explains the final plan in simple text.

## Smarter Scheduling

PawPal+ includes a few smarter scheduling features:

- Tasks can be sorted by scheduled time in `HH:MM` format.
- Tasks can be filtered by pet name or completion status.
- Daily and weekly tasks automatically create the next occurrence when completed.
- The scheduler detects overlapping timed tasks and returns warning messages instead of crashing.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing PawPal+

Run the test suite with:
```bash
python -m pytest
```

The tests cover the core scheduling behaviors in `pawpal_system.py`, including chronological task sorting, filtering by pet and completion status, recurring task creation for daily and weekly tasks, conflict detection for overlapping or duplicate scheduled times, and plan generation when the owner's available time is limited.

Reliability confidence: `4/5 stars`

This rating is based on the current test results, with 14 passing tests for the core backend scheduling logic. Confidence is high for task sorting, recurrence, conflict detection, filtering, and constrained plan generation, but it is not a full `5/5` because the project does not yet include end-to-end coverage for the Streamlit UI or broader invalid-input scenarios.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
