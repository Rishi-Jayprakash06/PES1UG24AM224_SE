# Use-Case Flow Specification

## Use Case: Record Grant Expense

**Primary Actor:** Faculty Researcher

**Goal:** Record a research-related expense against an active grant and update the remaining grant balance.

### Preconditions

1. The Faculty Researcher is authenticated in the system.
2. A valid research grant exists and is active.
3. The Faculty Researcher has permission to record expenses for the selected grant.
4. The selected grant is within its funding period and is available for expense recording.

### Postconditions

1. The expense is recorded against the selected research grant.
2. The total expenditure for the grant is updated.
3. The remaining grant balance is recalculated.
4. The transaction is recorded in the audit ledger.

### Main Success Scenario

1. The Faculty Researcher selects an active research grant.
2. The system displays the grant allocation, total expenditure, and remaining balance.
3. The Faculty Researcher selects **Record Expense**.
4. The Faculty Researcher enters the expense details, including category, description, amount, and date.
5. The system validates the entered expense information.
6. The system checks that the expense does not exceed the available grant balance.
7. The system records the expense against the selected grant.
8. The system updates the total expenditure and calculates the remaining grant balance.
9. The system records the transaction in the audit ledger.
10. The system displays the updated grant balance to the Faculty Researcher.

### Alternate Flow: Expense Exceeds Available Balance

**A1.** At Step 6, the system determines that the entered expense exceeds the available grant balance.

**A2.** The system rejects the expense and displays an appropriate message.

**A3.** The grant expenditure and remaining balance remain unchanged.

**A4.** The Faculty Researcher may modify the expense amount and resubmit it or cancel the operation.
