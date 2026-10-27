import flet as ft
import colors as cr
import json
import os
import datetime
from typing import Dict

# Where save the user
def user_file_path() -> str:
    data_dir = os.getenv("FLET_APP_STORAGE_DATA")
    if data_dir:
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "users.json")

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json")
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, "users.json")

# Load user or creat file emply if don't there
def load_user() -> Dict[str, str]:
    caminho = user_file_path()
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# Save user in file
def save_user(usuarios: Dict[str, str]):
    caminho = user_file_path()
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

def main(page: ft.Page):
    page.title = 'Kamba Serviços'
    page.bgcolor = ft.Colors.LIGHT_BLUE_50
    page.window.width = 320
    page.window.height = 682
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.adaptive = True
    
# ============================================= Back-End =============================================
    # Load the exits users
    usuarios = load_user()
    usuario_logado = [None]
    # ------------------------------- DEF SIGN ---------------------------
    warning_sign = ft.Text(color=ft.Colors.RED_700, size=13)
    modal = ft.AlertDialog(
        modal=True,
        content=ft.Row([ft.Icon(icon=ft.Icons.CHECK_CIRCLE_OUTLINE),ft.Text('Conta criada com sucesso!')], ),
        actions=[ft.TextButton('Ok', on_click=lambda e: page.pop_dialog())]
    )
    def sign(e):
        # warning_sign.value='',
        user = sign_user.value.strip()
        password = sign_pass.value
        conf_password = sign_conf_pass.value
        
        if not user or not password:
            warning_sign.value = 'Preencha o campo do usuário e senha.'
            page.update()
            return
        
        if password != conf_password:
            warning_sign.value = 'Não há sincronização na senha.'
            page.update()
            return
        
        if user in usuarios :
            warning_sign.value = 'A conta já existe!'
            page.update()
            return
        
        # Save new user
        usuarios[user] = password
        save_user(usuarios)
        
        page.show_dialog(modal)
        sign_user.value = ''
        sign_email.value = ''
        sign_pass.value = ''    
        sign_conf_pass.value = ''
        # modal
        page.update()
        
    # ----------------------------- DEF LOGIN -----------------------------
    warning_login = ft.Text(' ',color=ft.Colors.RED_700, size=13)
    def do_login(e):
        user = login_email.value.strip()
        password = login_pass.value
        
        if user in usuarios and usuarios[user] == password:
            usuario_logado[0] = user
            show_layout()
        else:
            warning_login.value = 'Usuário ou senha Incorreta!'
            page.update()
            return

        login_email.value =''
        login_pass.value=''
        warning_login.value=''
        page.update()
        
    def show_layout():
        page.floating_action_button = floating_btn
        page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
        page.bottom_appbar = appbar
        switcher.content = ft.Column([
            space,
            header,
            seach,
            widget_destaques(),
            conteudos[0],
        ], expand=True)
        switcher.transition = ft.AnimatedSwitcherTransition.FADE
        switcher.update()
        
        on_resize(None)

    def perfil():
        return ft.Column([
            ft.Container(
                bgcolor=cr.Colors.BG_DARK,
                border=ft.Border.all(2, cr.Colors.TERCIARIA),
                border_radius=20,
                padding=20,
                width=500,
                content=ft.Column([
                    ft.CircleAvatar(scale=1.5,content= ft.Icon(icon=ft.Icons.PERSON)),
                    ft.Text(f'{usuario_logado[0] or "Não logado"}', size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=15),
                    ft.Text(f'Criado em: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', size=14, color=ft.Colors.WHITE),
                    ft.Container(height=30),
                    ft.Button(
                        "Sair",
                        icon=ft.Icons.LOGOUT,
                        width=100,
                        height=50,
                        on_click=logout,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED_400, 
                            color=ft.Colors.WHITE,
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    def logout(e):
        usuario_logado[0] = None
        page.bottom_appbar = None
        page.floating_action_button = None
        page.clean()
        page.add(session)
        
    # --------------------------- DEF CHANGE  --------------------
    def start():
        switcher.content = session
        switcher.transition = ft.AnimatedSwitcherTransition.FADE
        switcher.update()

    def change_display(indice):
        title.value = name_title[indice]
        page.clean()
        if indice == 3:
            page.add(space, header, perfil())
        elif indice == 0:
            page.add(space, header, seach, widget_destaques(), conteudos[indice])
        else:
            page.add(space, header, conteudos[indice])
            page.show_dialog(ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.BLUE_50,
                actions=[ft.TextButton('OK', on_click=lambda e: page.pop_dialog())],
                content=ft.Text(f'{name_title[indice]} ainda não está Disponivel. Estará disponivel brevemente', color='Black')
            ))
        page.update()

    def linkar_display(indice):
        title.value = 'Linkar'
        page.clean()
        page.add(space, header, linkar[indice])
        page.show_dialog(ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.BLUE_50,
            actions=[ft.TextButton('OK', on_click=lambda e: page.pop_dialog())],
            content=ft.Text('Linkar ainda não está Disponivel. Estará disponivel brevemente', color='Black')
        ))
        page.update()

# ============================================= Front-End =============================================
    space = ft.Container(height=20)
    title = ft.Text('Explorar', size=20, weight=ft.FontWeight.BOLD, color=cr.Colors.DESTAQUE)
    name_title = ['Explorar', 'Serviços', 'Favoritos', 'Perfil']
    seach = ft.SearchBar(
        bar_hint_text="Seach...",
    )

    header = ft.Container(
        padding=20,
        content= ft.Column([
            title,
        ], align=ft.Alignment.CENTER_LEFT)
    )


    # ------------------------ LOGIN Var -------------------------
    login_email = ft.TextField(
        label='Email/Username',
        border_radius=20,
        width=500,
        prefix_icon=ft.Icons.PERSON,
        border_color=cr.Colors.SECURARIA,
        label_style=ft.TextStyle(color=cr.Colors.SECURARIA),
        text_style=ft.TextStyle(color='White'),
    )

    login_pass = ft.TextField(
        label='Password',
        border_radius=20,
        width=500,
        password=True,
        can_reveal_password=True,
        border_color=cr.Colors.SECURARIA,
        label_style=ft.TextStyle(color=cr.Colors.SECURARIA),
        text_style=ft.TextStyle(color='White'),
    )

    # ------------------------ SIGN Var -------------------------
    sign_user = ft.TextField(
        label='Username',
        border_radius=20,
        width=500,
        prefix_icon=ft.Icons.PERSON,
        border_color=cr.Colors.SECURARIA,
        label_style=ft.TextStyle(color=cr.Colors.SECURARIA),
        text_style=ft.TextStyle(color='White')
    )

    sign_email = ft.TextField(
        label='Email',
        border_radius=20,
        width=500,
        prefix_icon=ft.Icons.EMAIL,
        border_color=cr.Colors.SECURARIA,
        label_style=ft.TextStyle(color=cr.Colors.SECURARIA),
        text_style=ft.TextStyle(color='White')
    )

    sign_pass = ft.TextField(
        label='Password',
        border_radius=20,
        width=500,
        password=True,
        can_reveal_password=True,
        border_color=cr.Colors.SECURARIA,
        label_style=ft.TextStyle(color=cr.Colors.SECURARIA),
        text_style=ft.TextStyle(color='White')
    )

    sign_conf_pass = ft.TextField(
        label='Confirmar Password',
        border_radius=20,
        width=500,
        password=True,
        can_reveal_password=True,
        border_color=cr.Colors.SECURARIA,
        label_style=ft.TextStyle(color=cr.Colors.SECURARIA),
        text_style=ft.TextStyle(color='White')
    )


    # ------------------------ LOGIN ----------------------------
    login = ft.Container(
        aspect_ratio=9/12,
        padding=30,
        alignment=ft.Alignment.CENTER,
        blur=5,
        bgcolor=cr.Colors.BG_DARK,
        border=ft.Border.all(2, cr.Colors.TERCIARIA),
        border_radius=20,
        content=ft.Column([
            ft.Text('Faça login para continuar sua jornada', weight=ft.FontWeight.BOLD, color='white'),
            ft.Tabs(
                selected_index=0,
                length=2,
                content=ft.Column([
                    ft.TabBar(
                        tab_alignment=ft.TabAlignment.CENTER,
                        indicator_animation=ft.TabIndicatorAnimation.ELASTIC,
                        indicator_size=ft.TabBarIndicatorSize.LABEL,
                        indicator=ft.UnderlineTabIndicator(border_side=ft.BorderSide(color=cr.Colors.TERCIARIA, width=3)),
                        tabs=[
                            ft.Tab(label='Login'),
                            ft.Tab(label='Sign')
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Column([
                                    ft.Container(height=20),
                                    login_email,
                                    login_pass,
                                    warning_login,
                                    ft.Button(
                                        'Entrar',
                                        icon=ft.Icons.LOGIN,
                                        width=500,
                                        on_click=do_login,
                                        style=ft.ButtonStyle(
                                            padding=20,
                                            color=ft.Colors.WHITE,
                                            bgcolor={
                                                ft.ControlState.DEFAULT: cr.Colors.TERCIARIA,
                                                ft.ControlState.HOVERED: ft.Colors.GREY_400
                                            },
                                        )
                                    )
                                ])
                            ),

                            ft.Container(
                                content=ft.Column([
                                    ft.Container(height=20),
                                    sign_user,
                                    sign_pass,
                                    sign_conf_pass,
                                    warning_sign,
                                    ft.Button(
                                        'Cadastrar',
                                        icon=ft.Icons.PERSON_ADD,
                                        width=500,
                                        on_click=sign,
                                        style=ft.ButtonStyle(
                                            padding=20,
                                            color=ft.Colors.WHITE,
                                            bgcolor={
                                                ft.ControlState.DEFAULT: cr.Colors.TERCIARIA,
                                                ft.ControlState.HOVERED: ft.Colors.GREY_400
                                            },
                                        )
                                    )
                                ])
                            )
                        ]
                    )
                ])
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )


    # ----------------------------------------- MENU -------------------------------------------
    linkar = [
        ft.Column([
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
    ]

    def info():
        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.BLUE_50,
                actions=[ft.TextButton('Ok', on_click=lambda e: page.pop_dialog())],
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.CircleAvatar(scale=1.5, content= ft.Icon(icon=ft.Icons.PERSON)),
                        ft.Text('Emanuel Simão Gomes', size=18, weight='Bold', color='BLACK'),
                        ft.Row(
                            col={'xs': 12, 'sm': 6},
                            wrap=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.STAR, 
                                    color=ft.Colors.AMBER if _ <4 else ft.Colors.WHITE,
                                ) for _ in range(5)
                            ]
                        ),
                        ft.Text('Ut  omnis neque sed autem hic at perspiciatis deleniti. Numquam voluptatem et nostrum officiis eos sunt ipsum. Est voluptatem modi corrupti aspernatur adipisci quasi cupiditate reprehenderit earum. Non itaque tenetur iusto ea consequatur alias et et rerum.', color=ft.Colors.BLACK_87),
                    ]
                )
            )
        )
        page.update()
        
    def criar_cartao_destaque(titulo, nome, profissao):
        return ft.Container(
            border_radius=18,
            padding=16,
            blur=50,
            border=ft.Border.all(2, cr.Colors.TERCIARIA),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10,
                controls=[
                    ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(ft.Icons.CIRCLE, size=10, color=ft.Colors.WHITE70),
                            ft.Icon(ft.Icons.CIRCLE, size=10, color=ft.Colors.WHITE70),
                        ],
                    ),
                    ft.Text(
                        titulo,
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(nome, size=12, color=ft.Colors.WHITE),
                            ft.Text(profissao, size=10, color=ft.Colors.WHITE70),
                        ],
                    ),
                ],
            ),
        )


    def widget_destaques():
        return ft.Container(
            bgcolor=cr.Colors.BG_DARK,
            height=150,
            border_radius=24,
            padding=16,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Container(
                        height=120,
                        content=ft.PageView(
                            expand=True,
                            viewport_fraction=0.82,
                            selected_index=0,
                            horizontal=True,
                            controls=[
                                criar_cartao_destaque("Informático", "Emanuel Gomes", "Serviços de informática"),
                                criar_cartao_destaque("Programador", "Paulo António", "Desenvolvimento de software"),
                                criar_cartao_destaque("Eletricista", "João Manuel", "Instalações elétricas"),
                                criar_cartao_destaque("Canalizadora", "Maria José", "Canalização"),
                                criar_cartao_destaque("Redes", "Carlos Silva", "Técnico de redes"),
                                criar_cartao_destaque("Designer", "Ana Pedro", "Design"),
                            ],
                        ),
                    ),
                ],
            ),
        )
    
    def criar_cartao_usuario(nome, profissao, imagem="team.jpg"):
        return ft.Container(
            width=1000,
            height=200,
            border_radius=20,
            border=ft.Border.all(2, cr.Colors.TERCIARIA),
            on_click=info,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Stack(
                controls=[
                    ft.Image(
                        src="image/team.jpg",
                        height=200,
                        width=1000,
                        fit=ft.BoxFit.COVER,
                    ),

                    ft.Container(
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment.TOP_CENTER,
                            end=ft.Alignment.BOTTOM_CENTER,
                            colors=[
                                ft.Colors.with_opacity(
                                    0.0,
                                    ft.Colors.BLACK,
                                ),
                                ft.Colors.with_opacity(
                                    1.0,
                                    ft.Colors.BLACK,
                                ),
                            ],
                        ),
                        height=80,
                        bottom=0,
                        left=0,
                        right=0,
                    ),

                    ft.Container(
                        bottom=18,
                        left=8,
                        padding=5,
                        content=ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    nome,
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    profissao,
                                    size=10,
                                    color=ft.Colors.WHITE,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )
    cartoes_usuarios = [
        criar_cartao_usuario("Emanuel Gomes", "Informático"),
        criar_cartao_usuario("João Manuel", "Eletricista"),
        criar_cartao_usuario("Maria José", "Canalizadora",),
        criar_cartao_usuario("Carlos Silva", "Técnico de redes",),
        criar_cartao_usuario("Ana Pedro", "Designer",),
        criar_cartao_usuario("Paulo António","Programador",),
        criar_cartao_usuario("Paulo António","Programador",),
        criar_cartao_usuario("Paulo António","Programador",),
        criar_cartao_usuario("Paulo António","Programador",),
        criar_cartao_usuario("Paulo António","Programador",),
        criar_cartao_usuario("Paulo António","Programador",),
    ]
    
    conteudos = [
        ft.ResponsiveRow(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=16,
            run_spacing=16,
            controls=[
                ft.Container(
                    col={
                        ft.ResponsiveRowBreakpoint.XS: 12,
                        ft.ResponsiveRowBreakpoint.MD: 6,
                        ft.ResponsiveRowBreakpoint.LG: 4,
                    },
                    content=cartoes_usuarios[_],
                ) for _ in range(len(cartoes_usuarios))
            ]
        ),
        
        ft.Column([
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
        
        ft.Column([
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
        
    ]

    menu = [
        ft.TextButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.EXPLORE), ft.Text('Explorar')],
                spacing=4,
                tight=True
            ),
            style=ft.ButtonStyle(color=cr.Colors.TERCIARIA),
            on_click=lambda e: change_display(0),
        ),
        ft.TextButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.BUILD), ft.Text('Serviços')],
                spacing=4,
                tight=True
            ),
            style=ft.ButtonStyle(color=cr.Colors.TERCIARIA),
            on_click=lambda e: change_display(1)
        ),
        ft.TextButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.FAVORITE), ft.Text('Favoritos')],
                spacing=4,
                tight=True
            ),
            style=ft.ButtonStyle(color=cr.Colors.TERCIARIA),
            on_click=lambda e: change_display(2)
        ),
        ft.TextButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.PERSON), ft.Text('Perfil')],
                spacing=4,
                tight=True
            ),
            style=ft.ButtonStyle(color=cr.Colors.TERCIARIA),
            on_click=lambda e: change_display(3)
        ),
    ]
    
    def on_resize(e):
        is_small = page.width < 600
        for btn in menu:
            btn.content.controls[1].visible = not is_small
        page.update()
    page.on_resize = on_resize
        
    floating_btn = ft.FloatingActionButton(
        bgcolor=cr.Colors.TERCIARIA,
        shape=ft.CircleBorder(),
        on_click=lambda _: linkar_display(0),
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color=ft.Colors.WHITE) ],
            spacing=4,
            tight=True
        ),
    )
        
    appbar = ft.BottomAppBar(
        border_radius=ft.BorderRadius.all(30),
        bgcolor=cr.Colors.BG_DARK,
        shape=ft.CircularRectangleNotchShape(),
        content=ft.Row(controls=menu, spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    )

    session = ft.Stack(
        width=900,
        alignment=ft.Alignment.CENTER,
        expand=True,
        controls=[
            ft.Image(
                src="image/team.jpg",
                height=800,
                width=800,
                scale=1.3,
                fit=ft.BoxFit.COVER,
                opacity=0.1,
                expand=True,
            ),login,
        ]
    )
    
    
    show = ft.Container(
        blur=3,
        border_radius=20,
        padding=20,
        border=ft.Border.all(2, ft.Colors.WHITE),
        content=ft.Column(
            controls=[
                ft.Image(
                    src='icon.png',
                    height=200,
                    width=200,
                ),
                ft.Text('Kamba Serviços', size=20, weight='bold', color='Black'),
                ft.Text('Bem-vindo à nossa plataforma! Um lugar onde você pode encontrar os melhores serviços perto da sua localidade em apenas um clique, continua para saber mais!', color='black'),
                ft.Container(height=150),
                ft.Button(
                    'Vamos Começar!',
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=start,
                    align=ft.Alignment.BOTTOM_RIGHT,
                    style=ft.ButtonStyle(
                        padding=20,
                        color='white',
                        bgcolor={
                            ft.ControlState.DEFAULT: cr.Colors.BG_DARK,
                            ft.ControlState.HOVERED: ft.Colors.GREY_400
                        }
                    )
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    capa = ft.Stack(
        width=900,
        alignment=ft.Alignment.CENTER,
        expand=True,
        controls=[
            ft.Image(
                src="image/team.jpg",
                height=800,
                width=800,
                scale=1.3,
                fit=ft.BoxFit.COVER,
                opacity=0.1,
                expand=True,
            ),show
        ]
    )
    
    switcher = ft.AnimatedSwitcher(
        content=capa,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=800,
        reverse_duration=500,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
        expand=True
    )
    page.add(switcher)
    on_resize(None)
if __name__ == '__main__':
    ft.run(main, assets_dir="assets")