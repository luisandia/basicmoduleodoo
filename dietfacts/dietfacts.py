# -*- coding: utf-8 -*-
# Dietfacts application

from openerp import models, fields, api

# Extended product,template model with calories


class DietFacts_product_template(models.Model):
    # extend model product
    _name = 'product.template'
    _inherit = 'product.template'

    calories = fields.Integer('calories')
    servingsize = fields.Float('Serving size')
    lastupdated = fields.Date('Last Updated')
    dietitem = fields.Boolean('Diet Item')
    nutrient_ids = fields.One2many(
        'product.template.nutrient', 'product_id', 'Nutrients')

    @api.one
    @api.depends('nutrient_ids', 'nutrient_ids.value')
    def _calcscore(self):
        current_score = 0
        for nutrient_field in self.nutrient_ids:
           # if(nutrient_field.nutrient_id = 'Sodium')
            current_score = current_score + nutrient_field.value
        self.nutrition_score = current_score
    nutrition_score = fields.Float(
        string="Nutrition Score", store=False, compute="_calcscore")


class DietFacts_res_users_meal(models.Model):
    _name = 'res.users.meal'
    name = fields.Char('Meal Name')
    meal_date = fields.Datetime('Meal Date')
    items_ids = fields.One2many('res.users.mealitem', 'meal_id')
    user_id = fields.Many2one('res.users', 'Meal User')
    largemeal = fields.Boolean('Large Meal')

    @api.onchange('totalcalories')
    def check_total_calories(self):
        if self.totalcalories > 500:
            self.largemeal = True
        else:
            self.largemeal = False

    @api.one
    @api.depends('items_ids', 'items_ids.serving')
    def _calccalories(self):
        currentcalories = 0
        for mealitem in self.items_ids:
            currentcalories = currentcalories + \
                (mealitem.item_id.calories*mealitem.serving)
        self.totalcalories = currentcalories

    totalcalories = fields.Integer(
        string='Total Calories', store=True, compute='_calccalories')
    notes = fields.Text('Meal Notes')


class DietFacts_res_users_mealitem(models.Model):
    _name = 'res.users.mealitem'
    meal_id = fields.Many2one('res.users.meal')
    item_id = fields.Many2one('product.template', "Meal Item")
    serving = fields.Float('Servings')
    notes = fields.Text('Meal item notes')
    calories = fields.Integer(related="item_id.calories",
                              string="Calories Perserving", store=True, readonly=True)


class DietFacts_product_nutrient(models.Model):
    _name = "product.nutrient"
    name = fields.Char('Nutrient Name')
    uom_id = fields.Many2one('product.uom', 'Unit of Measure')
    description = fields.Text('Description')


class DietFacts_product_template_nutrient(models.Model):

    _name = 'product.template.nutrient'
    nutrient_id = fields.Many2one(
        'product.nutrient', string='Product Nutrient')
    product_id = fields.Many2one('product.template')

    uom_id = fields.Char(related='nutrient_id.uom_id.name',
                         string='UOM', readonly=True)

    value = fields.Float('Nutrient Value')
    dailypercent = fields.Float('Daily Recommended value')
