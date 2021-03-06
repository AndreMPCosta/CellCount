#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen

group_cells = ["Erythroid", "Myeloid", "Monocytic", "Megakaryocytic", "Limphoid", "Other"]

items = {group_cells[0]: [{"Erithroblast":["Proerythroblast","Basophilic Erythroblast",
                                           "Polychromatic Erythroblast", "Orthochromatic Erythroblast"]},
                          "Reticulocyte"],
         group_cells[1]: ["Myeloblast", "Promyelocyte", "Myelocyte", "Metamyelocyte", "Band",
                          {"Immature forms": ["Immature Neutrophil", "Immature Basophil", "Immature Eosinophil"]},
                          {"Mature forms": ["Neutrophil", "Basophil", "Eosinophil"]}],
         group_cells[2]: ["Monoblast", "Promonocyte", "Monocyte"],
         group_cells[3]: ["Megakaryoblast", "Promegakariocyte", "Megakariocyte"],
         group_cells[4]: ["Limphoblast", "Prolimphocyte", "Limphocyte", "Activated Limphocyte", "Plasma cell"],
         group_cells[5]: ["Mast cell", "ReticularEndothelial", "ExtraHemathopoietic", "Create other type"]}


group_cells_en = ["Erythroid", "Myeloid", "Monocytic", "Megakaryocytic", "Limphoid", "Other"]

items_en = {group_cells_en[0]: [{"Erithroblast":["Proerythroblast","Basophilic Erythroblast",
                                           "Polychromatic Erythroblast", "Orthochromatic Erythroblast"]},
                          "Reticulocyte"],
         group_cells_en[1]: ["Myeloblast", "Promyelocyte", "Myelocyte", "Metamyelocyte", "Band",
                          {"Immature forms": ["Immature Neutrophil", "Immature Basophil", "Immature Eosinophil"]},
                          {"Mature forms": ["Neutrophil", "Basophil", "Eosinophil"]}],
         group_cells_en[2]: ["Monoblast", "Promonocyte", "Monocyte"],
         group_cells_en[3]: ["Megakaryoblast", "Promegakariocyte", "Megakariocyte"],
         group_cells_en[4]: ["Limphoblast", "Prolimphocyte", "Limphocyte", "Activated Limphocyte", "Plasma cell"],
         group_cells_en[5]: ["Mast cell", "ReticularEndothelial", "ExtraHemathopoietic", "Create other type"]}

group_cells_pt = ["Eritróide", "Mielóide", "Monocitóide", "Megacariocítico", "Linfóide", "Outras"]

items_pt = {group_cells_en[0]: [{"Eritroblasto":["Pró-eritroblasto","Basofílico",
                                           "Policromático", "Ortocromático"]},
                          "Reticulócito"],
         group_cells_en[1]: ["Mieloblasto", "Promielócito", "Mielócito", "Metamielócito", "Banda",
                          {"Immature forms": ["I. neutrófilo", "I. basófilo", "I. eosinófilo"]},
                          {"Formas maduras": ["Neutrófilo", "Basófilo", "Eosinófilo"]}],
         group_cells_en[2]: ["Monoblasto", "Promonócito", "Monócito"],
         group_cells_en[3]: ["Megacarioblasto", "Promegacariócito", "Megacariócito"],
         group_cells_en[4]: ["Limfoblasto", "Prolinfócito", "Linfócito", "Linfócito ativado", "Plasmócito"],
         group_cells_en[5]: ["Mastócito", "Reticuloendotelial", "Extra-hematopoiético", "Criar outro tipo"]}

number_of_cols = 3

animation_type = 'in_circ'

languages={'en':{'group_cells':group_cells_en, 'items': items_en}, 'pt':{'group_cells':group_cells_pt, 'items': items_pt}}

main_colors = {'primary': 'Teal', 'accent': 'Red'}

md_colors = ['#ef5350', '#5c6bc0', '#26a69a', '#66bb6a', '#d4e157', '#ffa726', '#8d6e63', '#78909c', '#7e57c2',
             '#ff7043', '#00b8d4', '#006064']