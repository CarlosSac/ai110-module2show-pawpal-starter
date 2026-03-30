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

    Primarily for incremental implementation, adding methods one at a time, updating the UI to wire them in, and generating the test suite.

- What kinds of prompts or questions were most helpful?

    Mostly prompts that focuses in a single method or behavior worked better than open-ended ones. Prompts that referenced the actual class names and existing method signatures produced output that fit the codebase without needing much cleanup.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

    The initial next_occurrence() implementation calculated the next due date by adding a delta to self.due_date rather than date.today(). For a task that was overdue, this would marked the wrong date instead of resetting to tomorrow.

- How did you evaluate or verify what the AI suggested?

    Read the logic, noticed the base date was wrong, and asked for a correction. Then verified the fix and checking that completed daily tasks always produced a next occurrence dated today + 1, regardless of what the original due_date was.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

    Sorting tasks by start time, daily and weekly recurrence, conflict detection (same time, partial overlap, cross-pet), time budget boundary conditions (exact fit, one minute over), and empty-pet crash safety.

- Why were these tests important?

    These are the behaviors most likely to produce wrong output, a wrong recurrence date, or a missed cross-pet conflict would never cause a crash, so only tests catch them.

**b. Confidence**

- How confident are you that your scheduler works correctly?

    4/5. All 15 tests pass and cover the core logic thoroughly. The gap is the Streamlit UI session state behavior and the mark-complete flow have no automated coverage.

- What edge cases would you test next if you had more time?

    Completing the same task twice (duplicate next-occurrence), an owner with zero available minutes, and a task whose start_time is malformed for example "9:5" instead of "09:05".

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    The conflict detection system. It handles same-pet, cross-pet, and exact-same-time collisions in one pass without special cases, and returns warnings instead of crashing.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    Right now the app only supports one pet. A second iteration would store multiple pets in session state and let the owner add, switch between, and remove pets, which is what Owner and Scheduler already support in the backend, just not exposed in the UI.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    AI is most useful when you already have a clear mental model of what you're building. Prompts like "add a method that filters by completion status or pet name" produced good results immediately because the class structure was already well-defined. Vague prompts early in the design phase produced more drift. The clearer the spec, the more useful the AI output.
