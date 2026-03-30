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

2. **Owner** (dataclass) - Stores owner information and defines scheduling constraints through available_time and preferences. The available_time determines the daily time budget for the scheduler.

3. **Task** (dataclass) - Represents individual care tasks with name, duration, priority, and task_type. Each task knows its own duration and priority, which the scheduler uses to make decisions.

4. **Scheduler** - Manages a list of tasks and implements the scheduling algorithm. It uses the owner's time constraints to generate a daily schedule by prioritizing tasks that fit within the available time.


I used dataclasses for Pet, Owner, and Task because they primarily hold data. Scheduler is a regular class because it contains the core scheduling logic and algorithm.

**b. Design changes**

Yes. During implementation, I realized the original design was missing some important relationships between classes.

I updated `Owner` to store a list of pets so the system clearly represents who owns which pets. I also updated `Task` to include a `pet_name`, which connects each task to the correct pet. This makes the design more realistic and avoids leaving `Pet` disconnected from the scheduling logic.

I changed task removal to use a `task_id` instead of the task name, because names are not always unique. These changes made the system easier to organize and reduced ambiguity in the logic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

One tradeoff my scheduler makes is that it uses a simple approach instead of finding the perfect schedule. It picks the most important tasks that fit in the available time.

This is reasonable because the app is supposed to help pet owners make quick daily plans. A simple scheduler is easier to understand and works well for this project.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
