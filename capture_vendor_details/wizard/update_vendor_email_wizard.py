from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class UpdateVendorEmailWizard(models.TransientModel):
    _name = 'update.vendor.email.wizard'
    _description = 'Update Vendor Email Wizard'

    def _get_partner_id(self):
        partner_id = False
        if self._context.get('active_id') and self._context.get('active_model') == 'res.partner':
            partner_id = self.env['res.partner'].browse([self._context.get('active_id')])
        return partner_id
    def _get_email(self):
        email = ''
        if self._context.get('active_id') and self._context.get('active_model') == 'res.partner':
            email = self.env['res.partner'].browse([self._context.get('active_id')]).email
        return email
    
    email = fields.Char(string="Email ID", required=True, default=_get_email)
    partner_id = fields.Many2one('res.partner', default=_get_partner_id)

    def update_email(self):
        # Fetch the email template recordset
        template = self.env['mail.template'].browse(
            self.env.ref('capture_vendor_details.email_template_update_vendor').id
        )

        if template:
            template = template.with_context(object=self.partner_id)
            # Debug log the email values
            _logger.info(f'Sending email to: {self.email}')
            _logger.info(f'Email subject: {template.subject}')
            _logger.info(f'Email body: {template.body_html}')

            extra_arg = f"?partner_id={self.partner_id.id}" if self.partner_id else ""
            # Construct custom HTML body
            body_html = f"""
            <p>Hello,</p>
            <p>This is a notification that your vendor details have been updated.</p>
            <p>Please click the link below to view or update your details:</p>
            <p>
                <a href="/vendor-form{extra_arg}"
                style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; 
                background-color: #007bff; text-decoration: none; border-radius: 5px;">
                View Vendor Form
                </a>
            </p>
            <p>Best regards,</p>
            <p>Your Company</p>
            """

            # Log the custom email content
            _logger.info(f'Custom Email body: {body_html}')

            # Create the email content using the template and provided email
            mail_values = {
                'subject': template.subject,
                'body_html': body_html,
                'email_to': self.email,
                'email_from': self.env.user.email or '',
                'auto_delete': True,
                'message_type': 'email',
            }

            # Ensure email address is valid
            if not self.email or '@' not in self.email:
                _logger.error(f'Invalid email address: {self.email}')
                return {
                    'type': 'ir.actions.act_window_close'
                }

            # Send the email
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()
            _logger.info(f'Email sent successfully to: {self.email}')
            
            if self.partner_id:
                self.partner_id.active = False

        
        return {
            'type': 'ir.actions.act_window_close'
        }
