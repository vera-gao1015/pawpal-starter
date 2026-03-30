# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

**Three Core Actions:**

1. **Add a pet** - Enter basic owner and pet information.
2. **Schedule a walk** - Add and manage pet care tasks with time and priority.
3. **See today's tasks** - View the generated daily plan and task schedule.

**UML Design:**
The initial design includes five main classes:
1. **Pet** - Stores pet information (name, type, age). Responsible for representing the pet being cared for.
2. **Owner** - Stores owner information (name, available time per day, preferences). Responsible for defining constraints on scheduling.
3. **Task** - Represents a care task with properties (name, duration, priority, task type). Responsible for encapsulating individual care activities.
4. **Scheduler** - Contains the scheduling algorithm. Responsible for taking a list of tasks and constraints, then generating an optimized daily plan based on priority and available time.
5. **DailyPlan** - Represents the final schedule with ordered tasks and timing. Responsible for storing and displaying the generated plan with explanations.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
