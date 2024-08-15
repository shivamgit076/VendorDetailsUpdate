import base64
from werkzeug.utils import secure_filename
from odoo import http
from odoo.http import request


class VendorFormController(http.Controller):

    @http.route('/vendor-form', type='http', auth='public', website=True, csrf=True)
    def vendor_form(self, **kwargs):
        # Ensure partner_id is provided and is a valid integer
        p_id = request.params.get('partner_id')
        if p_id:
            try:
                partner = request.env['res.partner'].sudo().browse(int(p_id))
            except ValueError:
                partner = None
        else:
            partner = None
            
        # Fetch the list of countries
        countries = request.env['res.country'].sudo().search([])
        vat_certificate_ids = False
        if partner and partner.vat_certificate_ids:
            vat_certificate_ids = partner.vat_certificate_ids

        return request.render('capture_vendor_details.vendor_form_template', {
            'partner_id': partner,
            'vat_certificate_ids': vat_certificate_ids,
            'countries':countries
            })

    @http.route('/vendor-form/submit', type='http', auth='public', website=True, csrf=True)
    def vendor_form_submit(self, **post):
        partner_id = post.get('partner_id')
        partner = self._get_partner(partner_id)
        attachment_ids = self._handle_uploaded_files(partner_id)

        if post:
            self._update_or_create_partner(post, partner, attachment_ids)

        return request.render('capture_vendor_details.vendor_form_success', {})

    def _get_partner(self, partner_id):
        if partner_id:
            return request.env['res.partner'].sudo().browse(int(partner_id))
        return False

    def _handle_uploaded_files(self, partner_id):
        uploaded_files = request.httprequest.files.getlist('vat_certificate_ids')
        attachment_ids = []

        if uploaded_files:
            for uploaded_file in uploaded_files:
                attachment_id = self._create_attachment(uploaded_file, partner_id)
                attachment_ids.append(attachment_id)

            if partner_id:
                partner = request.env['res.partner'].sudo().browse(int(partner_id))
                partner.sudo().write({'vat_certificate_ids': [(4, aid) for aid in attachment_ids]})

        return attachment_ids

    def _create_attachment(self, uploaded_file, partner_id):
        file_name = secure_filename(uploaded_file.filename)
        file_content = uploaded_file.read()

        attachment = request.env['ir.attachment'].sudo().create({
            'name': file_name,
            'datas': base64.b64encode(file_content),
            'res_model': 'res.partner',
            'res_id': partner_id or False,
            'type': 'binary',
        })
        return attachment.id

    def _update_or_create_partner(self, post, partner, attachment_ids):
        partner_data = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'street': post.get('street1'),
            'street2': post.get('street2'),
            'city': post.get('city'),
            'zip': post.get('zip'),
            'country_id': int(post.get('country')),
            'active': False,
            'supplier_rank': 1 if post.get('is_supplier') else 0,
        }

        if partner and partner.exists():
            partner.sudo().write(partner_data)
        else:
            partner_data.update({
                'vat': post.get('VAT'),
                'supplier_rank': 1,
            })
            new_partner = request.env['res.partner'].sudo().create(partner_data)
            new_partner.sudo().write({'vat_certificate_ids': [(4, aid) for aid in attachment_ids]})
