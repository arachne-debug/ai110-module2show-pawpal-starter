# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

- What classes did you include, and what responsibilities did you assign to each?

My initial UML design centered on four main classes: `Owner`, `Pet`, `ServiceRequest`, and `Scheduler`.

- `Owner`: represents the client who has one or more pets and sets preferences such as preferred service windows and priority. It also manages pet ownership and creates requests.
- `Pet`: represents the animal being cared for. It stores identifying information, pet needs (for example walking or medication), and any special constraints or notes.
- `ServiceRequest`: represents a specific care task. It tracks the owner, pet, service type, time window, duration, and whether it is urgent or emergency-level.
- `Scheduler`: is responsible for matching service requests to feasible time slots while respecting availability, duration limits, and scheduling priorities.

The design keeps the data models simple and gives the scheduling logic a single place to enforce constraints and resolve conflicts.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. Based on the AI review of the skeleton, I refined the model by making the `Pet`-to-`Owner` relationship more explicit and adding scheduling metadata to `ServiceRequest`.

I changed `Pet` to include an `owner_id` field and updated `Owner.add_pet()` so it links the pet back to the owner. I also added `priority` and `assigned_slot` to `ServiceRequest`, and `scheduled_slots` to `Scheduler`. This was important because the initial design had a loose relationship between owners and pets, and it did not clearly model scheduling conflicts or priority ordering. With these changes, the scheduler can better handle high-priority and emergency requests without overbooking the same slot.

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
