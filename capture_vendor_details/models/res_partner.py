from odoo import _, models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    vat_certificate_ids = fields.Many2many('ir.attachment',  relation='partner_vat_certificate_rel',
        column1='partner_id',
        column2='attachment_id',string="VAT Certificates")
    
    def button_approve(self):
        for rec in self:
            if not rec.active:
                rec.active = True
