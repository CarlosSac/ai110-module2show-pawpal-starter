# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

    My initial design used four classes. Owner holds a reference to one or more Pet objects. Scheduler depends on both Owner and Pet as inputs, and selects from a list of Task objects to produce a daily plan.

- What classes did you include, and what responsibilities did you assign to each?
    - Owner: who is scheduling; holds the daily time budget
    - Pet: whose needs drive the tasks; knows its species and special needs
    - Task: a single care activity with a title, duration, and priority
    - Scheduler: the logic engine; selects and orders tasks within the owner's time constraints

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    - Yes. The initial design included a ScheduledTask class to wrap each task with an assigned start time and explanation. During implementation I removed it to keep the system simple and focused on the core requirements.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

    Priority: tasks are ranked high > medium > low and selected greedily in that order.
    Completion status: only pending tasks are eligible; done tasks are excluded from scheduling.
    Frequency: tasks carry a "daily" or "weekly" label that controls when the next occurrence is due after completion.

- How did you decide which constraints mattered most?
  Time and priority mattered the most because they directly determine whether a task makes it into the schedule at all. A high-priority task that exceeds the time budget is still excluded, because time is the hard ceiling. Priority is the tiebreaker, it decides which tasks fill the budget when not everything fits.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

    The scheduler picks tasks in priority order and adds each one if it fits, stopping as soon as a task doesn't fit rather than skipping it and trying smaller ones. This can leave time on the table. For example, if the time is 30 minutes and the remaining tasks are a high-priority 25-minute task followed by two low-priority 10-minute tasks, the scheduler takes the 25-minute task and leaves 5 minutes unused, even though two 10-minute tasks would fill the slot completely.

- Why is that tradeoff reasonable for this scenario?

    In a pet care app a missed high-priority task (medication, feeding) is meaningfully worse than unused time. The greedy approach encodes that judgment directly: the owner has already ranked tasks by importance, and the scheduler respects that ranking rather than trading a high-priority task for a better-fitting combination of lower-priority ones.

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
