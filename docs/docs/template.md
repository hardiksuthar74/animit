# Module Name

## 1. Overview

Brief description of the module.

- What problem it solves
- Where it is used (frontend, backend, CMS)
- Why it exists

---

## 2. Scope

Defines what is included and excluded in this module.

### Included

- Feature responsibilities
- Core flows

### Excluded

- Out-of-scope items (handled in other modules)

---

## 3. User Flows

Describe how users interact with this feature.

### Example Flows

- User action → System response
- Step-by-step interaction

---

## 4. Data Models (Schema)

Define database structure related to this module.

### Tables

#### table_name

| Field | Type | Description |
| ----- | ---- | ----------- |
| id    | UUID | Primary key |

### Relationships

- One-to-many / many-to-many relations
- Dependencies with other modules

---

## 5. API Endpoints (Backend)

List all backend APIs for this module.

### Example

#### POST /:module/create

- Description: Create resource

#### GET /:module/:id

- Description: Get details

#### PUT /:module/:id

- Description: Update resource

#### DELETE /:module/:id

- Description: Delete resource

---

## 6. Frontend Integration

How frontend interacts with this module.

### Pages / Screens

- List of pages where this feature appears

### Components

- UI components involved

### State Management

- What state is stored (local/global)

### API Usage

- Which endpoints are used
- When they are called

---

## 7. CMS Integration

Defines what parts of this module are manageable via CMS.

### CMS Capabilities

- Create / Update / Delete
- View data
- Trigger actions

### CMS Views

- Tables / dashboards
- Forms / editors

> Note: CMS user roles and permissions are handled separately.

---

## 8. Business Logic

Core logic and rules.

### Examples

- Validation rules
- Status transitions
- Constraints

---

## 9. Real-Time Behavior (If Applicable)

- Live updates
- WebSocket / polling behavior
- Event triggers

---

## 10. Error Handling

### Common Errors

- Invalid input
- Not found
- Unauthorized

### Response Format

```json
{
  "error": "message"
}
```

## 11. Security Considerations

- Authentication requirements
- Authorization rules
- Sensitive data handling
- Abuse prevention (rate limits, validation)

## 12. Edge Cases

- Invalid states
- Partial data scenarios
- Race conditions
- Failure handling

## 13. Dependencies

- Other modules this depends on
- External services (if any)
