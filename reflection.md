# PawPal+ Project Reflection

## 1. System Design
add a pet, schedule a walk, see today's tasks

**a. Initial design**

- Briefly describe your initial UML design.

Data about people/pets/tasks

Owner stores who the owner is, how much time they have, and preferences.
Pet stores pet profile details (name, species, age, special needs).
CareTask represents one care activity (walk, feeding, meds, etc.) with duration, priority, and other attributes.
Rules and limits for planning

ConstraintSet represents scheduling limits (daily time cap, blocked times, required/preferred categories).
TimeWindow is a helper for blocked time ranges and overlap checks.
What gets produced

DailyPlanItem is one scheduled task with start/end time plus a “why” reason.
DailyPlan is the full day’s schedule (list of plan items), including totals and explanation output.
Core planning behavior

Scheduler is the engine: it ranks tasks and builds a daily plan using priorities + constraints.
PlanExplainer creates human-readable reasoning for the chosen schedule.
Storage and app coordination

TaskRepository handles CRUD for tasks (add/edit/remove/list).
PawPalAppController ties everything together for the Streamlit UI: it receives inputs, asks the scheduler to build a plan, and returns plan + explanations.
How they relate:

An Owner can have one or more Pets.
A Pet can have many CareTasks.
The controller uses the repository + scheduler + explainer.
The scheduler uses constraints to build a DailyPlan, which contains many DailyPlanItems, each linked to a CareTask.
- What classes did you include, and what responsibilities did you assign to each?
Owner: Stores owner identity, daily time availability, and care preferences.
Pet: Stores pet profile data (name/species/age/special needs) used to inform task selection.
CareTask: Defines each care activity (duration, priority, category, frequency, required/optional) and basic validation/scoring helpers.
ConstraintSet: Holds scheduling rules (time limits, blocked windows, required/preferred categories) and validates tasks against those rules.

**b. Design changes**

- Did your design change during implementation?
no
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Time budget: Total task time must stay within max_daily_minutes (or owner available minutes).
Task priority: Higher-priority tasks are ranked first when allocating limited time.
Required vs optional tasks: is_required tasks should be included before optional ones whenever feasible.
Blocked time windows: Tasks should not be placed inside unavailable periods (TimeWindows).
Owner preferences: Preferred task categories are favored when choosing among similar candidates.
Must-include categories: Certain categories (e.g., meds/feeding) can be enforced as mandatory.
Task duration feasibility: Tasks too long for remaining time are skipped or deferred.
Pet-specific context: Special needs can influence which tasks become effectively higher priority or required.
- How did you decide which constraints mattered most?
First: feasibility constraints
Time budget and blocked windows come first because if a plan breaks these, it cannot be executed in real life.
Second: care-critical constraints
Required tasks and must-include categories (like meds/feeding) come next because missing them can impact pet health.
Third: optimization constraints
Priority helps choose what to keep when time is limited.
Fourth: personalization constraints
Owner preferences refine the plan quality (better fit, higher adherence), but should not override health/safety-critical needs.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
When daily time is limited, the scheduler may choose more short high-priority tasks instead of one long lower-priority enrichment task.
This improves essential coverage (more critical needs handled), but may reduce quality/depth in a single area (for example, less play/enrichment time).
- Why is that tradeoff reasonable for this scenario?
maximize critical task completion vs preserve longer, holistic activities.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used it for brainstorming the UML design, and once it was finalised, I asked it to implement the plan. I reviewed all the suggestions.
- What kinds of prompts or questions were most helpful?
I assigned the AI a role and then made the context clear and then gave it its objective.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
During designing the UML design, I prompted again and again until I understood the design.
- How did you evaluate or verify what the AI suggested?
No specific strategy.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Three core behaviors were tested across 34 automated tests:
  1. **Sorting correctness** — `Scheduler.sort_by_time` returns tasks in strict HH:MM chronological order, including ties and midnight-boundary edge cases.
  2. **Recurrence logic** — completing a `frequency="daily"` task adds a new task due the following day with a fresh ID and `is_complete=False`; `frequency="once"` tasks produce no successor.
  3. **Conflict detection** — `Scheduler.find_time_conflicts` produces exactly one warning per overlapping pair of plan slots and zero warnings for adjacent or non-overlapping slots.
  Additional tests covered the daily time-limit, blocked-window avoidance, priority/required-task ranking, and repository filtering.

- Why were these tests important?
These behaviors are the most safety-critical parts of the scheduler. If tasks are not ordered correctly, the displayed schedule is misleading. If recurrence silently fails, recurring care (meds, feeding) is dropped — which could harm the pet. If conflicts are not detected, the owner might unknowingly schedule two activities at the same time. Testing them ensured the core scheduling guarantees hold before connecting the logic to the Streamlit UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?
4 out of 5 stars. All 34 automated tests pass with no failures. The core scheduling behaviors — sorting, recurrence, conflict detection, time-limit enforcement, blocked-window avoidance, and priority ranking — are each verified by multiple tests including edge cases. The missing star reflects that the Streamlit UI layer (app.py) is not covered by automated tests, so end-to-end behavior (e.g., what happens when a user submits the form with invalid or boundary inputs) has not been verified programmatically.

- What edge cases would you test next if you had more time?
  1. **Overlapping blocked windows** — two blocked TimeWindows that themselves overlap; the scheduler should still find a valid slot without looping infinitely.
  2. **Task longer than the full day** — a single task with `duration_minutes` exactly equal to or greater than `max_daily_minutes`; it should be skipped cleanly with a reason message.
  3. **All tasks on the wrong date** — every task has `due_date` in the past or future; the plan should produce zero items rather than crash.
  4. **Must-include category with no available task** — `must_include_categories` contains a category for which no task exists in the repo; the explainer should note the gap.
  5. **Weekly recurrence crossing a month/year boundary** — completing a weekly task on Dec 29 should produce a task due Jan 5, not an invalid date.
  6. **Concurrent tasks for multiple pets** — verify that conflict warnings correctly name both pets when their tasks overlap.


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
It works fine. I tested it with multiple scenarios and it was abl

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
