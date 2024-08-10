#!/usr/bin/env python3
from nicegui import ui, binding, app
from datetime import datetime
from random import random

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('A')
        ui.tab('B')
        ui.tab('C')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Side menu')
    with ui.button_group():
        ui.button('One', on_click=lambda: ui.notify('You clicked Button 1!'))
        ui.button('Two', on_click=lambda: ui.notify('You clicked Button 2!'))
        ui.button('Three', on_click=lambda: ui.notify('You clicked Button 3!'))

dark = ui.dark_mode()
ui.label('Switch mode:')
ui.button('Dark', on_click=dark.enable)
ui.button('Light', on_click=dark.disable)



@ui.page('/other_page')
def other_page():
    ui.label('Welcome to the other side')

@ui.page('/dark_page', dark=True)
def dark_page():
    ui.label('Welcome to the dark side')

ui.link('Visit other page', other_page)
ui.link('Visit dark page', dark_page)



@ui.page('/page_layout')
def page_layout():
    ui.label('CONTENT')
    [ui.label(f'Line {i}') for i in range(100)]
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('HEADER')
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
        ui.label('LEFT DRAWER')
    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
        ui.label('RIGHT DRAWER')
    with ui.footer().style('background-color: #3874c8'):
        ui.label('FOOTER')

ui.link('show page with fancy layout', page_layout)

ui.page_title('New Title')

with ui.row():
    ui.button('Back', on_click=ui.navigate.back)
    ui.button('Forward', on_click=ui.navigate.forward)
    ui.button(icon='savings',
              on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug'))




with ui.row():
    with ui.scroll_area().classes('w-32 h-32 border'):
        ui.label('I scroll. ' * 20)
    # with ui.column().classes('p-4 w-32 h-32 border'):
    #     ui.label('I will not scroll. ' * 10)



ui.number(label='Number', value=3.1415927, format='%.2f',
          on_change=lambda e: result.set_text(f'you entered: {e.value}'))
result = ui.label()

grid = ui.aggrid({
    'defaultColDef': {'flex': 1},
    'columnDefs': [
        {'headerName': 'Name', 'field': 'name'},
        {'headerName': 'Age', 'field': 'age'},
        {'headerName': 'Parent', 'field': 'parent', 'hide': True},
    ],
    'rowData': [
        {'name': 'Alice', 'age': 18, 'parent': 'David'},
        {'name': 'Bob', 'age': 21, 'parent': 'Eve'},
        {'name': 'Carol', 'age': 42, 'parent': 'Frank'},
    ],
    'rowSelection': 'multiple',
}).classes('max-h-40')

def update():
    grid.options['rowData'][0]['age'] += 1
    grid.update()

ui.button('Update', on_click=update)
ui.button('Select all', on_click=lambda: grid.run_grid_method('selectAll'))
ui.button('Show parent', on_click=lambda: grid.run_column_method('setColumnVisible', 'parent', True))

m = ui.leaflet(center=(51.505, -0.09))
ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')

with ui.grid(columns=2):
    ui.button('London', on_click=lambda: m.set_center((51.505, -0.090)))
    ui.button('Berlin', on_click=lambda: m.set_center((52.520, 13.405)))
    ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))
    ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))


ui.aggrid({
    'columnDefs': [
        {'headerName': 'Name', 'field': 'name', 'filter': 'agTextColumnFilter', 'floatingFilter': True, 'sortable': True},
        {'headerName': 'Age', 'field': 'age', 'filter': 'agNumberColumnFilter', 'floatingFilter': True, 'sortable': True},
    ],
    'rowData': [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol', 'age': 42},
    ],
}).classes('max-h-40')




ui.run()
