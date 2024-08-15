
```markdown
# Vendor Invitation and Approval Module

## Overview

This module allows users to invite vendors to fill out their details via a form. Once the vendor submits the form, an approver can review and approve the vendor in the backend. Upon approval, the vendor will be visible in the vendor page and other relevant places.

## Features

- Send an invitation email to vendors with a link to a form.
- Vendors can fill out their details including:
  - Name
  - Email
  - Phone
  - VAT
  - Address (city and country)
  - VAT Certificate attachments (with preview and multiple attachments)
- Backend approval page for approvers to review and approve vendor submissions.
- Separate menu for unapproved vendors.
- Button in the vendor form to update the details of existing vendors.
- Access control for users with Purchase/Administration rights.

## Installation

1. Download the module and keep it in the addons path
2. Update App list

3. Install the `Vendor Invitation and Approval` module from the Odoo Apps menu.

## Configuration

To ensure the link in the invitation email works perfectly, you need to either update the configuration file with the `db_name` or use the `-d` option in the terminal.

### Update Configuration File

1. Open your Odoo configuration file (e.g., `odoo.conf`).
2. Add or update the `db_name` parameter with your database name:
   ```
   db_name = your_database_name
   ```

### Using Terminal

If you are working directly through the terminal, add the `-d` option with your database name when starting the Odoo server:
```sh
./odoo-bin -d your_database_name
```

## Usage

### Sending an Invitation Email

1. Navigate to `Purchase` -> `Vendor Approver` -> `Send Email to Vendor`.
2. Click on the `Send Invitation` button.
3. Fill in the vendor's email address and click `Send`.

### Vendor Form

1. The vendor receives an email with a link to the form.
2. The vendor clicks the link and is redirected to a form where they can fill out their details:
   - Name
   - Email
   - Phone
   - VAT
   - Address (city and country)
   - VAT Certificate attachments (with preview and multiple attachments)
3. The vendor submits the form.

### Approval Process

1. Navigate to `Purchase` -> `Vendor Approver` -> `Approve Vendors`.
2. Review the submitted vendor details.
3. Click `Approve` to approve the vendor.
4. Once approved, the vendor will be visible in the vendor page and other relevant places.

### Updating Existing Vendor Details

1. Navigate to the vendor form.
2. Click the `Update Details` button.
3. Update the necessary details and save.

### Viewing Unapproved Vendors

1. Navigate to `Purchase` -> `Vendor Approver` -> `Approve Vendors`.
2. Unapproved vendors will be listed separately for review and approval.

## Access Control

- Only users with Purchase/Administration rights will have access to the `Vendor Approver` menu and its submenus.

## Technical Details

### Controllers

- **VendorFormController**: Handles the form submission and file uploads.

### Models

- **res.partner**: Extended to include fields for VAT Certificate attachments and approval status.

### Views

- **Vendor Form**: A form view for vendors to fill out their details.
- **Approval Page**: A backend view for approvers to review and approve vendor submissions.
- **Unapproved Vendors**: A view to list unapproved vendors separately.

### Email Templates

- **Invitation Email**: An email template with a link to the vendor form.


## Author
- **Shivam Soni**

