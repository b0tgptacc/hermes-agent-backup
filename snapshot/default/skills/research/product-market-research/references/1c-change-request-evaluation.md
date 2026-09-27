# Evaluating 1C Change Requests and Vendor Quotes

Use this note when a vendor proposes a paid 1C change and the business suspects the outcome may already be available through user-mode configuration.

## First classify the requested outcome

Do not treat “add one more field/person” as a sufficient technical requirement. Separate:

1. **Storage only** — another value appears on a card.
2. **Manual routing** — a user can send an object to more people.
3. **Automatic routing** — the system determines recipients from roles or object attributes.
4. **Enforced workflow** — all required decisions, ordering, blocking, audit history, rejection, resubmission, notifications, and substitution work.

A user-mode additional requisite solves (1), but does not imply (2)–(4). Likewise, “several users are authorized to approve” is not equivalent to “every named user must approve.”

## Identify the real 1C object

“Supplier” may be a business label rather than an object. Determine whether the real target is:

- Counterparty (`Контрагент`);
- Partner (`Партнер`) with supplier relationship;
- Contract;
- Supplier order;
- Payment request;
- procurement document;
- document card in 1C:Document Management.

Record the configuration, edition, application release, platform release, deployment model, and whether the existing field is standard, an additional requisite, an extension, or a modified base-configuration attribute.

## Capability ladder: test cheapest reversible option first

1. **Existing setting or role assignment.** Inspect functional options, process templates, roles, and responsible-user lists.
2. **Additional requisite in Enterprise mode.** In BSP-based applications, inspect `Administration → General settings → Additional requisites and information`; use a typed reference to User/Employee rather than free text where possible.
3. **Built-in process template.** In Document Management and products with universal processes, test adding a user/role, sequential/parallel stages, conditions, auto-start, rejection, and substitution.
4. **Extension.** If code is genuinely required, prefer an extension over direct modification of the supported base configuration.
5. **Base-configuration modification.** Accept only with a written reason that an extension cannot implement the requirement and with an explicit update-maintenance plan.

Always test on a database copy before production.

## Configuration boundaries

- **1C:Document Management:** multiple approvers, users/roles, sequential, parallel, mixed, and conditional approval are normally process-template configuration.
- **1C:ERP. Holding Management:** universal processes support visual routes, conditional transitions, additional approvers, and address resolution from object attributes.
- **Regular 1C:ERP / Complex Automation:** individual documents such as supplier orders can have standard approval/status scenarios, but a list of authorized users may mean “any one may change status,” not two mandatory visas. Verify semantics.
- **1C:Accounting 3.0:** additional requisites are commonly available; do not assume a general multi-stage supplier-card workflow exists.
- **Customized databases:** if a singular “Approver” field already drives code, adding a second visible field does not make the algorithm multi-approver.

Primary references:

- https://v8.1c.ru/doc8/effektivnoe-upravlenie-protsessami/
- https://v8.1c.ru/cpm-erp/protsessy-zadachi-i-opoveshcheniya-cpm-erp
- https://v8.1c.ru/platforma/rasshireniya/
- https://its.1c.ru/db/erp25doc/bookmark/supplierorder/SupplierOrder

## Vendor challenge checklist

Before approving development, require the vendor to state:

- exact object and trigger;
- why user-mode additional requisites do not meet the need;
- why an existing process template or functional option does not meet it;
- whether one-of-many authorization or all-of-many approval is required;
- sequential versus parallel semantics;
- what is blocked pending approval;
- behavior on rejection, data change, resubmission, absence, and termination;
- implementation method: setting, extension, or base modification;
- itemized hours for analysis, implementation, tests, deployment, documentation, and warranty;
- source ownership, installation/rollback instructions, affected objects, and update compatibility.

A short paid diagnostic can be reasonable, but its deliverable must be a written capability finding and implementation decision—not merely a restatement of the request.

## Acceptance tests

Verify in a copy and again after deployment:

- both approvers are resolved for the correct business object;
- ordinary users cannot bypass the second mandatory decision;
- sequential/parallel behavior matches policy;
- each decision records identity, timestamp, result, and comment;
- rejection, return, and resubmission preserve history;
- changes to critical data retrigger approval when required;
- substitution prevents abandoned workflows;
- permissions disclose no extra data;
- existing documents, reports, and exchanges still work;
- backup, rollback, source, and post-update verification are documented.

## Pricing interpretation

Compare quotes by hours and deliverables, not only the hourly rate. A high total may be justified by legacy customization, access-right complexity, integrations, migration, or support across releases. Strong warning signs are no object-level diagnosis, no tested standard alternative, no decomposition, direct base modification without justification, and no source/rollback/update terms.
