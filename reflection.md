# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design used four classes. Owner holds a reference to one or more Pet objects. Scheduler depends on both Owner and Pet as inputs, and selects from a list of Task objects to produce a daily plan.

    - Owner: who is scheduling; holds the daily time budget
    - Pet: whose needs drive the tasks; knows its species and special needs
    - Task: a single care activity with a title, duration, and priority
    - Scheduler: the logic engine; selects and orders tasks within the owner's time constraints

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    - Yes. I added a ScheduledTask class during implementation. Originally I planned to have Scheduler return a plain list of Task objects, but I needed a way to store each task's assigned start time and explanation alongside it. Rather than cluttering Task with scheduling-specific data, I created ScheduledTask to hold that output separately.

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
