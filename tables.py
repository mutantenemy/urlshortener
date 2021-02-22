""" THIS WAS MEANT TO BE A CLASS THAT FORMATED DATA INTO AN HTML TABLE """


# # import things
# from flask_table import Table, Col

# # Declare your table
# class ItemTable(Table):
#     code = Col('Code')
#     destiny = Col('Destiny')
#     calls = Col('Times Used')
#     born = Col('Created in')
#     lastUsed = Col('Last time Used')

# # Get some objects
# class Item(object):
#     def __init__(self, list):
#         self.code = list[0]
#         self.destiny = list[1]
#         self.calls = list[2]
#         self.born = list[3]
#         self.lastUsed = list[4]

# class MakeTable():

#     items = []

#     def makeTable(this, dictionary):
#         for key in dictionary.keys():
#             if type(dictionary[key]) == list:
#                 items.append(Item(dictionary[key][0],
#                                  (dictionary[key][1],
#                                  (dictionary[key][2],
#                                  (dictionary[key][3],
#                                  (dictionary[key][4]))

#         if items != None:
#             table = ItemTable(items)
#             return table.__html__()
#         else:
#             return None

# # items = [Item('Name1', 'Description1'),
# #          Item('Name2', 'Description2'),
# #          Item('Name3', 'Description3')]
# # # Or, equivalently, some dicts
# # items = [dict(name='Name1', description='Description1'),
# #          dict(name='Name2', description='Description2'),
# #          dict(name='Name3', description='Description3')]

# # Or, more likely, load items from your database with something like
# # items = ItemModel.query.all()

# # # Populate the table
# # table = ItemTable(items)

# # # Print the html
# # print(table.__html__())
# # or just {{ table }} from within a Jinja template