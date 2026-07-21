from __future__ import annotations

import pandas as pd
import streamlit as st

import database as db
from styles import apply_styles, hero, metric_grid


st.set_page_config(
    page_title="Clique&Leve",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()


def money(value) -> str:
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def show_error(exc: Exception) -> None:
    message = str(exc)
    if "Invalid login credentials" in message:
        message = "E-mail ou senha incorretos."
    st.error(message)


def login_page() -> None:
    left, center, right = st.columns([1, 1.05, 1])
    with center:
        st.markdown("<div style='height:7vh'></div>", unsafe_allow_html=True)
        hero("Entre na sua comunidade", "Compre, venda e gerencie relações de confiança em um só lugar.")
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


def section(title: str, subtitle: str) -> None:
    st.markdown(
        f"<div class='section-head'><div><h2>{title}</h2><p>{subtitle}</p></div></div>",
        unsafe_allow_html=True,
    )


def quick_cards(items: list[tuple[str, str, str]]) -> None:
    html = "".join(
        f"<div class='quick-card'><div class='quick-icon'>{icon}</div><h3>{title}</h3><p>{text}</p></div>"
        for icon, title, text in items
    )
    st.markdown(f"<div class='quick-grid'>{html}</div>", unsafe_allow_html=True)


def admin_home(profile: dict) -> None:
    products = db.rows("products")
    active_products = [p for p in products if p.get("active")]
    sellers = db.rows("sellers")
    customers = db.rows("customers")
    receivables = db.rows("receivables")

    open_amount = sum(
        float(r.get("amount_due") or r.get("amount") or 0)
        for r in receivables
        if str(r.get("status", "")).lower() not in {"quitada", "cancelada"}
    )

    hero(
        f"Olá, {profile.get('full_name', 'Administrador')}",
        "Visão executiva do ecossistema Clique&Leve: comércio, parceiros, clientes e confiança.",
        "PAINEL ADMINISTRATIVO",
    )
    metric_grid([
        ("Produtos ativos", str(len(active_products)), "Catálogo publicado"),
        ("Parceiros", str(len(sellers)), "Lojas na comunidade"),
        ("Clientes", str(len(customers)), "Base cadastrada"),
        ("Em aberto", money(open_amount), "Recebíveis consolidados"),
    ])

    section("Centro de comando", "Acesse os módulos que fazem a plataforma crescer.")
    quick_cards([
        ("🏪", "Gestão de parceiros", "Acompanhe lojas, responsáveis, status e desempenho."),
        ("📦", "Catálogo inteligente", "Audite produtos, fotos, preços, margem e estoque."),
        ("🤝", "Rede de confiança", "Visualize clientes, crédito por vendedor e comportamento financeiro."),
        ("💳", "Financeiro", "Controle vendas no fim do mês, recebimentos e inadimplência."),
        ("📊", "Inteligência", "Identifique categorias, vendedores e produtos com maior potencial."),
        ("🛡️", "Auditoria", "Rastreie operações sensíveis e preserve a governança da plataforma."),
    ])

    section("Pulso da plataforma", "Indicadores para decisões rápidas.")
    c1, c2 = st.columns([1.35, .65])
    with c1:
        if products:
            df = pd.DataFrame(products)
            if "seller_id" in df.columns:
                chart = df.groupby("seller_id").size().sort_values(ascending=False).head(10)
                st.bar_chart(chart)
        else:
            st.info("Cadastre parceiros e produtos para ativar os indicadores.")
    with c2:
        st.markdown(
            """
            <div class="quick-card">
              <div class="quick-icon">⚡</div>
              <h3>Próxima ação recomendada</h3>
              <p>Cadastre o primeiro parceiro vendedor e publique produtos com foto para ativar o marketplace real.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def seller_home(profile: dict, seller: dict) -> None:
    products = db.rows("products", seller_id=seller["id"])
    stock = sum(int(p.get("stock_quantity") or 0) for p in products)
    cost = sum(float(p.get("cost_price") or 0) * int(p.get("stock_quantity") or 0) for p in products)
    potential = sum(
        max(float(p.get("price") or 0) - float(p.get("cost_price") or 0), 0)
        * int(p.get("stock_quantity") or 0)
        for p in products
    )
    hero(
        f"Olá, {profile.get('full_name', 'Vendedor')}",
        f"Painel da loja {seller.get('store_name', '')}: produtos, margem e estoque.",
        "PAINEL DO VENDEDOR",
    )
    metric_grid([
        ("Produtos", str(len(products)), "Itens cadastrados"),
        ("Estoque", str(stock), "Unidades disponíveis"),
        ("Capital em estoque", money(cost), "Custo imobilizado"),
        ("Lucro potencial", money(potential), "Projeção sobre o estoque"),
    ])
    section("Ações rápidas", "Tudo o que sua loja precisa em uma única tela.")
    quick_cards([
        ("➕", "Cadastrar produto", "Adicione foto, custo, preço, estoque e condições de pagamento."),
        ("📸", "Fortalecer catálogo", "Produtos com boa imagem geram mais confiança e conversão."),
        ("📈", "Acompanhar margem", "Proteja sua rentabilidade antes de liberar qualquer oferta."),
    ])


def client_home(profile: dict) -> None:
    hero(
        f"Olá, {profile.get('full_name', 'Cliente')}",
        "Descubra produtos da sua comunidade e compre com uma experiência simples e confiável.",
        "SUA COMUNIDADE",
    )
    section("Feito para você", "Explore produtos e parceiros próximos.")
    quick_cards([
        ("🛍️", "Marketplace", "Produtos, alimentos e serviços da comunidade."),
        ("📦", "Meus pedidos", "Acompanhe solicitações, entregas e histórico."),
        ("❤️", "Favoritos", "Guarde lojas e produtos para encontrar mais rápido."),
    ])
    # O card de nível não aparece aqui por padrão.
    # Ele só deve ser mostrado quando existir crédito ativo para pagamento no fim do mês.


def marketplace_page() -> None:
    hero("Marketplace", "Produtos e serviços selecionados da comunidade Clique&Leve.", "EXPERIÊNCIA DE COMPRA")
    products = db.rows(
        "products",
        "id,name,description,price,stock_quantity,image_url,origin,seller_id,active",
        active=True,
    )
    sellers = {s["id"]: s for s in db.rows("sellers", "id,store_name,whatsapp", active=True)}

    search = st.text_input("Buscar", placeholder="Busque produtos, lojas e serviços...")
    filtered = []
    for p in products:
        store = sellers.get(p["seller_id"], {}).get("store_name", "")
        text = f"{p.get('name','')} {p.get('description','')} {store}".lower()
        if search.lower() in text:
            filtered.append(p)

    if not filtered:
        st.info("Nenhum produto publicado ainda.")
        return

    for start in range(0, len(filtered), 4):
        cols = st.columns(4)
        for col, product in zip(cols, filtered[start:start + 4]):
            store = sellers.get(product["seller_id"], {})
            with col:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                if product.get("image_url"):
                    st.image(product["image_url"], use_container_width=True)
                else:
                    st.markdown(
                        "<div style='height:180px;background:#e9f5ff;display:grid;place-items:center;font-size:55px'>🛍️</div>",
                        unsafe_allow_html=True,
                    )
                st.markdown('<div class="product-body">', unsafe_allow_html=True)
                st.markdown(f"<div class='store-label'>{store.get('store_name','LOJA')}</div>", unsafe_allow_html=True)
                st.subheader(product["name"])
                st.caption(product.get("description") or "Produto disponível.")
                st.markdown(f"<div class='price'>{money(product['price'])}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='muted'>Estoque: {product.get('stock_quantity',0)}</div>", unsafe_allow_html=True)
                st.markdown("</div></div>", unsafe_allow_html=True)


def seller_products_page(seller: dict) -> None:
    hero("Minha loja", "Cadastre produtos com foto, custo, preço, margem e estoque.", "GESTÃO DO CATÁLOGO")
    tab_catalog, tab_new = st.tabs(["Catálogo e resultado", "Cadastrar produto"])

    with tab_new:
        categories = db.rows("categories", "id,name", active=True)
        category_map = {c["name"]: c["id"] for c in categories}
        with st.form("new_product", clear_on_submit=True):
            c1, c2 = st.columns([1.2, .8])
            with c1:
                name = st.text_input("Nome do produto *")
                description = st.text_area("Descrição")
                category_name = st.selectbox("Categoria", list(category_map.keys()) if category_map else ["Sem categoria"])
                origin = st.selectbox("Origem", ["marketplace", "vending"], format_func=lambda v: {"marketplace":"Marketplace","vending":"Vending Machine"}[v])
                image = st.file_uploader("Foto do produto *", type=["jpg","jpeg","png","webp"])
            with c2:
                cost_price = st.number_input("Custo unitário", min_value=0.0, step=.50, format="%.2f")
                sale_price = st.number_input("Preço de venda *", min_value=0.0, step=.50, format="%.2f")
                stock = st.number_input("Estoque inicial", min_value=0, step=1)
                allow_credit = st.checkbox("Permitir compra no fim do mês", value=True)
                active = st.checkbox("Publicar no marketplace", value=True)
                profit = sale_price - cost_price
                margin = profit / sale_price * 100 if sale_price > 0 else 0
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
                    image_url, image_path = db.upload_product_image(image, seller["id"])
                    db.create_product({
                        "seller_id": seller["id"],
                        "category_id": category_map.get(category_name),
                        "name": name.strip(),
                        "description": description.strip() or None,
                        "origin": origin,
                        "cost_price": float(cost_price),
                        "price": float(sale_price),
                        "stock_quantity": int(stock),
                        "allow_seller_credit": allow_credit,
                        "image_url": image_url,
                        "image_path": image_path,
                        "active": active,
                    })
                    st.success("Produto cadastrado.")
                    st.rerun()
                except Exception as exc:
                    show_error(exc)

    with tab_catalog:
        products = db.rows("products", seller_id=seller["id"])
        if not products:
            st.info("Nenhum produto cadastrado.")
            return
        rows = []
        for p in products:
            cost = float(p.get("cost_price") or 0)
            price = float(p.get("price") or 0)
            stock = int(p.get("stock_quantity") or 0)
            profit = price - cost
            rows.append({
                "Produto": p["name"], "Custo": cost, "Venda": price,
                "Lucro unitário": profit,
                "Margem %": round((profit / price * 100) if price else 0, 1),
                "Estoque": stock, "Lucro potencial": profit * stock,
                "Publicado": bool(p.get("active"))
            })
        st.dataframe(
            pd.DataFrame(rows), use_container_width=True, hide_index=True,
            column_config={
                "Custo": st.column_config.NumberColumn(format="R$ %.2f"),
                "Venda": st.column_config.NumberColumn(format="R$ %.2f"),
                "Lucro unitário": st.column_config.NumberColumn(format="R$ %.2f"),
                "Lucro potencial": st.column_config.NumberColumn(format="R$ %.2f"),
                "Margem %": st.column_config.NumberColumn(format="%.1f%%"),
            }
        )


def placeholder_page(title: str, subtitle: str) -> None:
    hero(title, subtitle, "MÓDULO EM EVOLUÇÃO")
    st.info("A estrutura visual deste módulo já está preparada para a próxima etapa funcional.")


def main() -> None:
    if not db.restore_session():
        login_page()
        return

    try:
        profile = st.session_state.get("profile") or db.get_my_profile()
        seller = db.current_seller() if profile["role"] == "vendedor" else None
    except Exception as exc:
        show_error(exc)
        return

    role = profile["role"]

    with st.sidebar:
        st.markdown(
            "<div class='brand'><div class='brand-mark'>⚡</div><span>Clique&Leve</span></div>"
            "<div class='sidebar-sub'>Marketplace interno premium</div>",
            unsafe_allow_html=True,
        )
        st.divider()

        if role == "administrador":
            options = ["Visão executiva", "Marketplace", "Parceiros", "Produtos", "Clientes", "Financeiro", "Auditoria"]
        elif role == "vendedor":
            options = ["Início", "Marketplace", "Minha loja", "Clientes", "Financeiro"]
        else:
            options = ["Início", "Marketplace", "Meus pedidos", "Favoritos", "Minha conta"]

        page = st.radio("Navegação", options, label_visibility="collapsed")
        st.divider()
        st.caption(profile.get("full_name", "Usuário"))
        st.caption(role.capitalize())
        if st.button("Sair", use_container_width=True):
            db.logout()
            st.rerun()

    if role == "administrador" and page == "Visão executiva":
        admin_home(profile)
    elif role == "vendedor" and page == "Início":
        seller_home(profile, seller)
    elif role not in {"administrador", "vendedor"} and page == "Início":
        client_home(profile)
    elif page == "Marketplace":
        marketplace_page()
    elif page == "Minha loja":
        if seller:
            seller_products_page(seller)
        else:
            st.error("Seu usuário ainda não está vinculado a uma loja.")
    else:
        placeholder_page(page, "Módulo organizado de acordo com o perfil e a governança do Clique&Leve.")


if __name__ == "__main__":
    main()
