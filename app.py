from __future__ import annotations

import pandas as pd
import streamlit as st

import database as db
from styles import apply_styles, html_block

st.set_page_config(page_title="Clique&Leve", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
apply_styles()


def money(value) -> str:
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def show_error(exc: Exception) -> None:
    msg = str(exc)
    if "Invalid login credentials" in msg:
        msg = "E-mail ou senha incorretos."
    st.error(msg)


def topbar(initials: str = "AB") -> None:
    html_block(
        f"""<div class="topbar">
        <div class="searchbox">⌕ &nbsp;&nbsp; Busque produtos, lojas e serviços...</div>
        <div class="top-icons">
          <div class="top-icon">🔔</div>
          <div class="top-icon">🛒</div>
          <div class="top-icon">{initials}</div>
        </div>
        </div>"""
    )


def hero() -> None:
    html_block(
        """<section class="hero-main">
        <div>
          <div class="hero-kicker">COMÉRCIO INTERNO + CONFIANÇA</div>
          <h1>Compre de pessoas próximas. Pague com flexibilidade.</h1>
          <p>Uma rede privada onde vendedores, colaboradores e serviços locais se conectam com segurança, conveniência e reputação compartilhada.</p>
          <div class="hero-buttons">
            <span class="hero-btn">Explorar marketplace</span>
            <span class="hero-btn secondary">Quero vender</span>
          </div>
        </div>
        <div class="hero-stats">
          <div class="hero-stat"><strong>24</strong><span>parceiros ativos</span></div>
          <div class="hero-stat"><strong>138</strong><span>produtos disponíveis</span></div>
          <div class="hero-stat"><strong>96%</strong><span>pagamentos em dia</span></div>
          <div class="hero-stat"><strong>4,9★</strong><span>média da comunidade</span></div>
        </div>
        </section>"""
    )


def level_card() -> None:
    html_block(
        """<section class="level-card">
        <div class="level-label">Seu nível atual</div>
        <div class="level-name">🥉 Bronze</div>
        <div class="level-value">R$ 50,00</div>
        <div class="level-muted">Limite total</div>
        <div class="level-track"><div class="level-progress"></div></div>
        <div class="level-foot"><span>Disponível: <b>R$ 31,00</b></span><span>Usado: <b>R$ 19,00</b></span></div>
        <div class="level-actions">
          <div class="level-action">Ver histórico</div>
          <div class="level-action light">Como subir de nível</div>
        </div>
        </section>"""
    )


def section_title(title: str, subtitle: str) -> None:
    html_block(f'<div class="section-title"><h2>{title}</h2><p>{subtitle}</p></div>')


def categories() -> None:
    items = [("🥤","Vending"),("🥟","Alimentação"),("🏠","Casa"),("👕","Moda"),("💼","Serviços"),("♻️","Usados")]
    cards = "".join(f'<div class="category-card"><div class="category-icon">{i}</div><strong>{n}</strong></div>' for i,n in items)
    html_block(f'<div class="category-grid">{cards}</div>')


def partners() -> None:
    items = [
        ("🥟","Empadas da Ana","Alimentação • 4,9 ★"),
        ("🍰","Doces da Mari","Sobremesas • 4,8 ★"),
        ("🥗","Marmita Leve","Refeições • 4,7 ★"),
        ("🎁","Ateliê 360","Presentes • 5,0 ★"),
    ]
    cards = "".join(
        f'<div class="partner-card"><div class="partner-icon">{i}</div><div><strong>{n}</strong><br><span>{s}</span></div></div>'
        for i,n,s in items
    )
    html_block(f'<div class="partner-wrap">{cards}</div>')


def metric_grid(items) -> None:
    cards = "".join(
        f'<div class="metric-card"><div class="metric-label">{a}</div><div class="metric-value">{b}</div><div class="metric-note">{c}</div></div>'
        for a,b,c in items
    )
    html_block(f'<div class="metric-grid">{cards}</div>')


def member_home(show_level: bool) -> None:
    topbar()
    hero()
    if show_level:
        level_card()
    section_title("Explore por categoria", "Um shopping interno completo.")
    categories()
    section_title("Feito por gente daqui", "Parceiros da própria comunidade.")
    partners()
    section_title("Destaques de hoje", "Produtos selecionados para você.")
    products = db.rows("products", active=True)
    if not products:
        st.info("Os produtos publicados aparecerão aqui.")
    else:
        render_products(products[:8])


def admin_home(profile: dict) -> None:
    topbar("AB")
    hero()
    products = db.rows("products")
    sellers = db.rows("sellers")
    customers = db.rows("customers")
    receivables = db.rows("receivables")
    open_amount = sum(float(x.get("amount_due") or x.get("amount") or 0) for x in receivables if str(x.get("status","")).lower() not in {"quitada","cancelada"})
    section_title("Visão executiva", "O pulso completo do ecossistema Clique&Leve.")
    metric_grid([
        ("Produtos ativos", str(len([p for p in products if p.get("active")])), "Catálogo publicado"),
        ("Parceiros", str(len(sellers)), "Lojas cadastradas"),
        ("Clientes", str(len(customers)), "Base da comunidade"),
        ("Em aberto", money(open_amount), "Recebíveis consolidados"),
    ])
    section_title("Centro de comando", "Gestão de parceiros, produtos, clientes e financeiro.")
    html_block(
        '<div class="category-grid">'
        '<div class="category-card"><div class="category-icon">🏪</div><strong>Parceiros</strong></div>'
        '<div class="category-card"><div class="category-icon">📦</div><strong>Produtos</strong></div>'
        '<div class="category-card"><div class="category-icon">👥</div><strong>Clientes</strong></div>'
        '<div class="category-card"><div class="category-icon">💳</div><strong>Financeiro</strong></div>'
        '<div class="category-card"><div class="category-icon">📊</div><strong>Inteligência</strong></div>'
        '<div class="category-card"><div class="category-icon">🛡️</div><strong>Auditoria</strong></div>'
        '</div>'
    )


def render_products(products) -> None:
    sellers = {s["id"]: s for s in db.rows("sellers", "id,store_name", active=True)}
    for start in range(0, len(products), 4):
        cols = st.columns(4)
        for col, p in zip(cols, products[start:start+4]):
            with col:
                if p.get("image_url"):
                    st.image(p["image_url"], use_container_width=True)
                html_block(
                    f'<div class="product-card"><div class="product-body">'
                    f'<div class="store-label">{sellers.get(p.get("seller_id"),{}).get("store_name","LOJA")}</div>'
                    f'<h3>{p.get("name","Produto")}</h3>'
                    f'<div class="price">{money(p.get("price",0))}</div>'
                    f'<div class="muted">Estoque: {p.get("stock_quantity",0)}</div>'
                    f'</div></div>'
                )


def marketplace_page() -> None:
    topbar()
    hero()
    section_title("Explore por categoria", "Um shopping interno completo.")
    categories()
    section_title("Feito por gente daqui", "Parceiros da própria comunidade.")
    partners()
    section_title("Todos os produtos", "Catálogo publicado pelos vendedores.")
    products = db.rows("products", active=True)
    if products:
        render_products(products)
    else:
        st.info("Nenhum produto publicado ainda.")


def seller_products_page(seller: dict) -> None:
    topbar()
    section_title("Minha loja", "Cadastre produtos com foto, custo, preço, margem e estoque.")
    tab_catalog, tab_new = st.tabs(["Catálogo e resultado", "Cadastrar produto"])
    with tab_new:
        categories_db = db.rows("categories", "id,name", active=True)
        category_map = {c["name"]: c["id"] for c in categories_db}
        with st.form("new_product", clear_on_submit=True):
            c1,c2 = st.columns([1.2,.8])
            with c1:
                name = st.text_input("Nome do produto *")
                description = st.text_area("Descrição")
                category_name = st.selectbox("Categoria", list(category_map) if category_map else ["Sem categoria"])
                origin = st.selectbox("Origem", ["marketplace","vending"], format_func=lambda x: "Marketplace" if x=="marketplace" else "Vending Machine")
                image = st.file_uploader("Foto do produto *", type=["jpg","jpeg","png","webp"])
            with c2:
                cost_price = st.number_input("Custo unitário", min_value=0.0, step=.50)
                sale_price = st.number_input("Preço de venda *", min_value=0.0, step=.50)
                stock = st.number_input("Estoque inicial", min_value=0, step=1)
                allow_credit = st.checkbox("Permitir compra no fim do mês", value=True)
                active = st.checkbox("Publicar no marketplace", value=True)
                profit = sale_price-cost_price
                margin = profit/sale_price*100 if sale_price else 0
                st.metric("Lucro unitário", money(profit))
                st.metric("Margem", f"{margin:.1f}%")
            submit = st.form_submit_button("Cadastrar e publicar", use_container_width=True)
        if submit:
            if not name.strip() or sale_price <= 0 or image is None:
                st.warning("Preencha nome, preço e foto.")
            elif cost_price > sale_price:
                st.warning("O custo está acima do preço de venda.")
            else:
                try:
                    image_url,image_path = db.upload_product_image(image,seller["id"])
                    db.create_product({
                        "seller_id":seller["id"],"category_id":category_map.get(category_name),
                        "name":name.strip(),"description":description.strip() or None,
                        "origin":origin,"cost_price":float(cost_price),"price":float(sale_price),
                        "stock_quantity":int(stock),"allow_seller_credit":allow_credit,
                        "image_url":image_url,"image_path":image_path,"active":active
                    })
                    st.success("Produto cadastrado.")
                    st.rerun()
                except Exception as exc:
                    show_error(exc)
    with tab_catalog:
        products = db.rows("products", seller_id=seller["id"])
        if not products:
            st.info("Nenhum produto cadastrado.")
        else:
            rows=[]
            for p in products:
                cost=float(p.get("cost_price") or 0); price=float(p.get("price") or 0); stock=int(p.get("stock_quantity") or 0)
                profit=price-cost
                rows.append({"Produto":p["name"],"Custo":cost,"Venda":price,"Lucro unitário":profit,"Margem %":round(profit/price*100 if price else 0,1),"Estoque":stock,"Lucro potencial":profit*stock})
            st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)





def login_page() -> None:
    st.markdown("<div style='height:6vh'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 0.85], gap="small")

    with left:
        st.markdown(
            """
            <div style="
                min-height:520px;
                display:flex;
                flex-direction:column;
                justify-content:space-between;
                padding:44px;
                border-radius:28px 0 0 28px;
                color:#ffffff;
                background:
                  radial-gradient(circle at 88% 4%,rgba(72,173,255,.28),transparent 30%),
                  linear-gradient(135deg,#07192d 0%,#0b3f73 52%,#1463ff 100%);
                box-shadow:0 24px 60px rgba(16,33,58,.14);
            ">
              <div>
                <div style="font-size:12px;letter-spacing:.16em;color:#9ddfff;font-weight:900">
                  COMÉRCIO INTERNO + CONFIANÇA
                </div>
                <h1 style="color:#fff;font-size:42px;line-height:1.06;margin:18px 0 22px;letter-spacing:-.04em">
                  Compre de pessoas próximas. Pague com flexibilidade.
                </h1>
                <p style="color:#d8e9fb;font-size:16px;line-height:1.65;max-width:680px">
                  Uma rede privada para vendedores, colaboradores e serviços locais se conectarem
                  com segurança, conveniência e reputação compartilhada.
                </p>
              </div>

              <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">
                <div style="background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px">
                  <strong style="display:block;font-size:24px">24</strong>
                  <span style="font-size:12px;color:#c7ddf2">parceiros ativos</span>
                </div>
                <div style="background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px">
                  <strong style="display:block;font-size:24px">138</strong>
                  <span style="font-size:12px;color:#c7ddf2">produtos disponíveis</span>
                </div>
                <div style="background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:16px">
                  <strong style="display:block;font-size:24px">96%</strong>
                  <span style="font-size:12px;color:#c7ddf2">pagamentos em dia</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        with st.container(border=True):
            st.markdown(
                """
                <div style="padding:20px 8px 12px">
                  <div style="display:flex;align-items:center;gap:12px;margin-bottom:28px">
                    <div style="
                      width:44px;height:44px;border-radius:14px;
                      background:linear-gradient(135deg,#27d6ff,#1463ff);
                      display:grid;place-items:center;color:#fff;font-weight:900
                    ">C&L</div>
                    <div>
                      <div style="font-size:18px;font-weight:900;color:#10213a">Clique&Leve</div>
                      <div style="font-size:12px;color:#6f7f94">Marketplace interno</div>
                    </div>
                  </div>
                  <div style="font-size:28px;font-weight:900;color:#10213a">Bem-vindo</div>
                  <div style="font-size:14px;color:#6f7f94;margin:5px 0 20px">
                    Entre para acessar sua comunidade.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form("login"):
                email = st.text_input("E-mail")
                password = st.text_input("Senha", type="password")
                submit = st.form_submit_button("Entrar", use_container_width=True)

            if submit:
                try:
                    db.login(email.strip(), password)
                    st.rerun()
                except Exception as exc:
                    show_error(exc)


def main() -> None:
    if not db.restore_session():
        login_page(); return
    try:
        profile=st.session_state.get("profile") or db.get_my_profile()
        role=profile["role"]
        seller=db.current_seller() if role=="vendedor" else None
    except Exception as exc:
        show_error(exc); return

    with st.sidebar:
        html_block(
            '<div class="brand">'
            '<div class="brand-mark">C&L</div>'
            '<div><div class="brand-title">Clique&Leve</div>'
            '<div class="brand-sub">Marketplace interno</div></div>'
            '</div>'
        )

        preview = role
        if role == "administrador":
            st.markdown(
                '<div class="role-title">VISUALIZAR COMO</div>',
                unsafe_allow_html=True,
            )
            preview_label = st.selectbox(
                "Visualizar como",
                ["Administrador", "Membro", "Vendedor"],
                index=0,
                label_visibility="collapsed",
                key="role_preview",
            )
            preview = {
                "Administrador": "administrador",
                "Membro": "cliente",
                "Vendedor": "vendedor",
            }[preview_label]

        st.markdown(
            '<div class="menu-title-clean">NAVEGAÇÃO</div>',
            unsafe_allow_html=True,
        )

        if preview == "administrador":
            menu_options = [
                "⌂  Início",
                "▦  Marketplace",
                "◎  Parceiros",
                "▣  Produtos",
                "◉  Clientes",
                "◉  Financeiro",
                "⚙  Auditoria",
            ]
        elif preview == "vendedor":
            menu_options = [
                "⌂  Início",
                "▦  Marketplace",
                "▣  Minha loja",
                "◎  Crédito",
                "◉  Clientes",
                "◉  Financeiro",
            ]
        else:
            menu_options = [
                "⌂  Início",
                "▦  Marketplace",
                "▤  Pedidos",
                "♡  Favoritos",
                "◇  Minha conta",
            ]

        selected = st.radio(
            "Navegação",
            menu_options,
            label_visibility="collapsed",
            key=f"menu_{preview}",
        )
        page = selected.split("  ", 1)[1]

        initials = "".join(
            part[0] for part in profile.get("full_name", "AB").split()[:2]
        ).upper()

        html_block(
            f'<div class="sidebar-profile">'
            f'<div class="profile-avatar">{initials}</div>'
            f'<div><div class="profile-name">{profile.get("full_name","Usuário")}</div>'
            f'<div class="profile-role">{preview.capitalize()}</div></div>'
            f'</div>'
        )

        if st.button("Sair", use_container_width=True, key="logout_button"):
            db.logout()
            st.rerun()

    if page=="Marketplace":
        marketplace_page()
    elif preview=="administrador" and page=="Início":
        admin_home(profile)
    elif preview=="vendedor" and page=="Minha loja":
        if seller:
            seller_products_page(seller)
        else:
            st.warning("Para testar o cadastro, vincule este usuário a uma loja.")
    elif preview=="vendedor" and page=="Início":
        topbar(); hero(); section_title("Painel da loja","Produtos, estoque e rentabilidade.")
    elif preview=="cliente" and page=="Início":
        # Enquanto administrador estiver pré-visualizando como membro, o card de nível fica oculto.
        # O card só deve aparecer para um cliente real com crédito ativo.
        member_home(show_level=False)
    else:
        topbar(); section_title(page,"Módulo preparado para a próxima etapa funcional.")
        st.info("A interface deste módulo já está alinhada ao novo visual.")


if __name__=="__main__":
    main()
