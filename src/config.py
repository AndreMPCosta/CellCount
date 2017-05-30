group_cells = ["Erythroid", "Myeloid", "Monocytic", "Megakaryocytic", "Limphoid", "Other"]

items = {group_cells[0]: [{"Erithroblast":["Proerythroblast","Basophilic",
                                           "Polychromatic", "Orthochromatic"]},
                          "Reticulocyte"],
         group_cells[1]: ["Myeloblast", "Promyelocyte", "Myelocyte", "Metamyelocyte", "Band",
                          {"Immature forms": ["I. neutrophil", "I. basophil", "I. eosinophil"]},
                          {"Mature forms": ["Neutrophil", "Basophil", "Eosinophil"]}],
         group_cells[2]: ["Monoblast", "Promonocyte", "Monocyte"],
         group_cells[3]: ["Megakaryoblast", "Promegakariocyte", "Megakariocyte"],
         group_cells[4]: ["Limphoblast", "Prolimphocyte", "Limphocyte", "Activated Limphocyte", "Plasma cell"],
         group_cells[5]: ["Mast cell", "Reticular-endothelial", "Extra-hemathopoietic", "Create other type"]}


main_colors = {'primary': 'Teal', 'accent': 'Red'}

md_colors = ['#ef5350', '#5c6bc0', '#26a69a', '#66bb6a']

# menus = { group_cells[0]:
#        [{'viewclass': 'MDMenuItem',
#          'text': 'Erithroblast'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Reticulocyte'},
#        ],
#         group_cells[1]:
#        [{'viewclass': 'MDMenuItem',
#          'text': 'Myeloblast'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Reticulocyte'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Myelocyte'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Metamyelocyte'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Band'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Immature forms'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Mature forms'},
#        ],
#         group_cells[2]:
#        [{'viewclass': 'MDMenuItem',
#          'text': 'Monoblast'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Promonocyte'},
#         {'viewclass': 'MDMenuItem',
#          'text': 'Monocyte'},
#        ],
# }