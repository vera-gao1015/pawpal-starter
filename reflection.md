# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

**Three Core Actions:**

1. **Add a pet** - Enter basic owner and pet information.
2. **Schedule a walk** - Add and manage pet care tasks with time and priority.
3. **See today's tasks** - View the generated daily plan and task schedule.

**UML Design:**
The initial design includes four main classes:

1. **Pet** (dataclass) - Stores pet information (name, type, age). Provides methods to get and update pet details.

2. **Owner** (dataclass) - Stores owner information and defines scheduling constraints through available_time. The available_time determines the daily time budget for the scheduler.

3. **Task** (dataclass) - Represents individual care tasks with a unique `task_id`, description, duration, frequency, priority, and scheduling details. Each task knows its own duration and priority, which the scheduler uses to make decisions.

4. **Scheduler** - Manages a list of tasks and implements the scheduling algorithm. It uses the owner's time constraints to generate a daily schedule by prioritizing tasks that fit within the available time.


I used dataclasses for Pet, Owner, and Task because they primarily hold data. Scheduler is a regular class because it contains the core scheduling logic and algorithm.

**b. Design changes**

Yes. During implementation, I realized the original design was missing some important relationships between classes.

I updated `Owner` to store a list of pets so the system clearly represents who owns which pets. I kept tasks attached to each `Pet` instead of storing a separate task list inside `Scheduler`, which makes the ownership relationship clearer and avoids disconnecting `Pet` from the scheduling logic.

I changed task removal to use a `task_id` instead of the task name, because names are not always unique. These changes made the system easier to organize and reduced ambiguity in the logic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers:
- **Available time** - The owner's daily time budget (hard limit)
- **Task priority** - Higher priority tasks (1-3) are scheduled first
- **Task duration** - How many minutes each task needs
- **Scheduled time** - Fixed times like "08:00" for organizing the day

Priority and available time matter most because they solve the core problem: limited time and focusing on what's important.

**b. Tradeoffs**

The scheduler uses a greedy algorithm: sort by priority (high to low), then pick tasks until time runs out. It's simple and fast, but might miss better combinations of tasks.

This works well for daily pet care planning because it's easy to understand and runs instantly. For this use case, prioritizing high-priority tasks makes more sense than finding the mathematically perfect schedule.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools for:
- **Design brainstorming** - Discussing which classes to create and how they should relate
- **Implementation** - Writing the scheduling algorithm and conflict detection logic
- **UI layout** - Converting from centered layout to wide dual-column design with visual separators
- **Debugging** - Fixing issues with recurring task creation and task ID uniqueness

The most helpful prompts were specific and contextual, like "implement conflict detection for overlapping scheduled times" rather than "make my code better." Clear requirements led to better suggestions.

**b. Judgment and verification**

When implementing the UI layout, AI initially suggested adding compact CSS styling to shrink tables and text. After reviewing the changes, I asked to revert them because the interface felt too cramped and harder to read.

I evaluated the suggestion by mentally visualizing how the compressed spacing would look and comparing it to the user experience goal of "easy to browse." I prioritized readability over space efficiency, which felt more appropriate for a daily planning tool.

---

## 4. Testing and Verification

**a. What you tested**

I tested 14 core behaviors:
- **Task sorting** by scheduled time (with blank times last)
- **Filtering tasks** by completion status and pet name
- **Recurring tasks** - daily and weekly tasks create next occurrence when completed
- **Conflict detection** - overlapping scheduled times, invalid times, back-to-back tasks
- **Plan generation** - respects available time, prioritizes correctly, tracks unscheduled tasks
- **Task uniqueness** - task IDs are unique, preventing accidental duplicates
- **Pet management** - adding/removing pets, rejecting duplicate names

These tests are important because they cover the most critical user workflows: scheduling tasks, completing them, and getting a workable daily plan. They also prevent common bugs like duplicate tasks or scheduling conflicts.

**b. Confidence**

I'm 4/5 confident the scheduler works correctly. The backend logic has strong test coverage with 14 passing tests. The core scheduling algorithm, conflict detection, and recurring task behavior all work as expected.

I'm not 5/5 because:
- No end-to-end UI testing (only backend unit tests)
- Limited testing of invalid inputs or extreme cases (like 1000 tasks or 0 available time)

If I had more time, I would test:
- What happens when available time is 0 or negative
- Very long task lists (100+ tasks) to check performance
- Edge cases in time parsing (like "25:00" or "08:60")
- UI interactions (like rapidly clicking Complete button multiple times)

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the dual-column UI layout. Switching from centered to wide layout with a visual separator made the app much easier to browse. Pet management on the left and task management on the right creates a clear separation of concerns that matches how users think about their workflow.

The test coverage also went well - having 14 tests gave me confidence to refactor code and add features without breaking existing functionality.

**b. What you would improve**

If I had another iteration, I would:
- Add the ability to edit existing tasks (currently you can only add/remove)
- Improve the scheduling algorithm to handle task dependencies (e.g., "walk must happen before feeding")
- Add calendar integration so users can see plans for future dates, not just today
- Create visual timeline or gantt chart showing when tasks happen throughout the day

**c. Key takeaway**

The most important thing I learned is that **designing the system first with UML saves time later**. When I had a clear class structure before coding, implementation was much smoother. Changes I made during coding (like adding task_id and storing pets in Owner) were deliberate improvements, not desperate fixes.

Working with AI taught me that specific, contextual prompts work best. Instead of asking "improve my code," asking "add conflict detection for overlapping scheduled times" led to focused, useful suggestions I could evaluate and integrate.
