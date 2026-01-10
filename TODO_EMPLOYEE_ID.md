# Employee ID Implementation Plan

## Task: Add unique employee_id field with format `ahn_role_joiningmonthyear_uniqueid`

### Steps:

1. [x] Add `employee_id` field to EmployeeProfile model
   - Add unique CharField with max_length=50
   - Add helper method to generate the ID

2. [x] Update signals.py to generate employee_id on creation
   - The ID is now generated in the model's save() method

3. [x] Add search by employee_id functionality
   - Updated EmployeeListView to search by employee_id

4. [x] Display employee ID in header
   - Updated base.html to show employee_id in top header for authenticated users

5. [x] Create and run migration
   - Generated migration for the new field
   - Ran migration to apply changes

6. [x] Backfill existing records
   - Created management command `backfill_employee_ids`
   - Generated employee_id for existing EmployeeProfile records

## ID Format:
- Format: `ahn_{role}_{MMYYYY}_{######}`
- Example: `AHN_ADMIN_062024_000001` or `AHN_EMPLOYEE_062024_000001`
- 6-digit sequence number (can be expanded to more digits later)

## Fields Modified:
- `employee_mgmt/apps/organization/models.py` - Add employee_id field
- `employee_mgmt/apps/organization/views.py` - Add search by employee_id
- `employee_mgmt/templates/base.html` - Display employee ID in header
- `employee_mgmt/templates/organization/employee_list.html` - Show and search by employee_id
- `employee_mgmt/static/css/style.css` - Add styles for employee ID badge
- `employee_mgmt/apps/organization/management/commands/backfill_employee_ids.py` - Backfill command

