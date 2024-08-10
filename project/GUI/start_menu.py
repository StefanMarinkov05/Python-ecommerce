import sys
from nicegui import ui

BRAND_NAME = "BuyCar"

def start_page(session):
    ui.page_title(BRAND_NAME)

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



    # @ui.page('/page_layout')
    # def page_layout():
    #     ui.label('CONTENT')
    #     [ui.label(f'Line {i}') for i in range(100)]
    #     with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    #         ui.label('HEADER')
    #         ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
    #     with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
    #         ui.label('LEFT DRAWER')
    #     with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
    #         ui.label('RIGHT DRAWER')
    #     with ui.footer().style('background-color: #3874c8'):
    #         ui.label('FOOTER')

    # def print_brands_models():
    #     # Your implementation here
    #     pass

    # def print_cars():
    #     # Your implementation here
    #     pass

    # def exit_application():
    #     # Your implementation here
    #     pass

    # with ui.dialog() as dialog:
    #     ui.card().style('padding: 16px;')
    #     ui.label('Are you sure?')
    #     ui.input()
    #     with ui.row():
    #         ui.button('Yes', on_click=lambda: dialog.submit('Yes'))
    #         ui.button('No', on_click=lambda: dialog.submit('No'))

    # async def login_popup():
    #     result = await dialog
    #     ui.notify(f'You chose {result}')

    # async def register_popup():
    #     result = await dialog
    #     ui.notify(f'You chose {result}')

    # async def open_login_popup():
    #     await login_popup()

    # async def open_register_popup():
    #     await register_popup()

    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        ui.label('Pick an action')
        with ui.column().classes('space-y-4').style('align-items: center'):
            ui.button('Log in', on_click=lambda: ui.notify(1)).classes('w-full max-w-xs')
            ui.button('Register', on_click=lambda: ui.notify(1)).classes('w-full max-w-xs')
            ui.button('View all brands', on_click=lambda: ui.notify(1)).classes('w-full max-w-xs')
            ui.button('View all cars', on_click=lambda: ui.notify(1)).classes('w-full max-w-xs')
            ui.button('Exit', on_click=lambda: sys.exit()).classes('w-full max-w-xs')

    # with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    #     ui.label('Pick an action')
    #     with ui.column().classes('space-y-4').style('align-items: center'):
    #         ui.button('Log in', on_click=lambda: ui.run_task(open_login_popup)).classes('w-full max-w-xs')
    #         ui.button('Register', on_click=lambda: ui.run_task(open_register_popup)).classes('w-full max-w-xs')
    #         ui.button('View all brands', on_click=lambda: ui.notify(1)).classes('w-full max-w-xs')
    #         ui.button('View all cars', on_click=lambda: ui.notify(1)).classes('w-full max-w-xs')
    #         ui.button('Exit', on_click=lambda: sys.exit()).classes('w-full max-w-xs')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
