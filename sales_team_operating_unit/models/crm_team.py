# -*- coding: utf-8 -*-
# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2017-TODAY Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CrmTeam(models.Model):

    _inherit = 'crm.team'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for team in self:
            if team.company_id and \
                    team.operating_unit_id and \
                    team.company_id != team.operating_unit_id.company_id:
                raise UserError(_('Configuration error!\n\nThe Company in the\
                Sales Team and in the Operating Unit must be the same.'))

    @api.multi
    @api.constrains('operating_unit_id', 'member_ids')
    def _check_member_operating_unit(self):
        for rec in self.member_ids:
            if (rec and self.operating_unit_id and
                    self.operating_unit_id not in rec.operating_unit_ids):
                    raise ValidationError(_('Configuration error. The user %s '
                                            'has not assigned the same '
                                            'Operating unit.' % rec.name))
