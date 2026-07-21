from __future__ import annotations

from decimal import Decimal

import pandas as pd
import streamlit as st

import database as db
from styles import apply_styles, hero, metric_card


st.set_page_config(
    page_title="Clique&Leve",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()


def money(value) -> str:
    try:
        return (
            f"R$ {float(value):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    except Exception:
        return "R$ 0,00"


def show_error(exc: Exception) -> None:
    message = str(exc)
    if "Invalid login credentials" in message:
        message = "E-mail ou senha incorretos."
    st.error(message)


def login_page() -> None:
    left, center, right = st.columns([1, 1.1, 1])
    with center:
        st.markdown("<div style='height:8vh'></div>", unsafe_allow_html=True)
        hero("Clique&Leve", "Marketplace interno e rede privada de confiança.")
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


def dashboard(profile: dict, seller: dict | None) -> None:
    hero(
        f"Olá, {profile.get('full_name', 'usuário')}",
        "Comércio interno, confiança e gestão em uma única experiência.",
    )

    if profile["role"] == "vendedor" and seller:
        products = db.rows("products", seller_id=seller["id"])
        total_stock = sum(int(p.get("stock_quantity") or 0) for p in products)
        inventory_cost = sum(
            float(p.get("cost_price") or 0) * int(p.get("stock_quantity") or 0)
            for p in products
        )
        potential_profit = sum(
            max(float(p.get("price") or 0) - float(p.get("cost_price") or 0), 0)
            * int(p.get("stock_quantity") or 0)
            for p in products
        )

        cols = st.columns(4)
        with cols[0]:
            metric_card("Produtos cadastrados", str(len(products)))
        with cols[1]:
            metric_card("Unidades em estoque", str(total_stock))
        with cols[2]:
            metric_card("Custo do estoque", money(inventory_cost))
        with cols[3]:
            metric_card("Lucro potencial", money(potential_profit))
    else:
        products = db.rows("products", active=True)
        cols = st.columns(3)
        with cols[0]:
            metric_card("Produtos ativos", str(len(products)))
        with cols[1]:
            metric_card("Parceiros", str(len(db.rows("sellers", active=True))))
        with cols[2]:
            metric_card("Experiência", "Premium")

    st.markdown("### Diretriz do sistema")
    st.info(
        "O custo e o lucro são informações privadas do vendedor e do administrador. "
        "O cliente visualiza somente preço, descrição, foto, estoque e condições de compra."
    )


def marketplace_page() -> None:
    hero("Marketplace", "Produtos e serviços da comunidade Clique&Leve.")

    products = db.rows(
        "products",
        "id,name,description,price,stock_quantity,image_url,origin,seller_id,active",
        active=True,
    )
    sellers = {
        s["id"]: s
        for s in db.rows("sellers", "id,store_name,whatsapp", active=True)
    }

    search = st.text_input(
        "Buscar",
        placeholder="Busque produtos, lojas e serviços...",
    )

    filtered = []
    for product in products:
        seller_name = sellers.get(product["seller_id"], {}).get("store_name", "")
        haystack = (
            f"{product.get('name','')} "
            f"{product.get('description','')} "
            f"{seller_name}"
        ).lower()
        if search.lower() in haystack:
            filtered.append(product)

    if not filtered:
        st.info("Nenhum produto encontrado.")
        return

    for start in range(0, len(filtered), 4):
        cols = st.columns(4)
        for col, product in zip(cols, filtered[start:start + 4]):
            seller = sellers.get(product["seller_id"], {})
            with col:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                if product.get("image_url"):
                    st.image(product["image_url"], use_container_width=True)
                else:
                    st.markdown(
                        "<div style='height:180px;background:#e8f8ff;"
                        "display:grid;place-items:center;font-size:54px'>🛍️</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown('<div class="product-body">', unsafe_allow_html=True)
                st.markdown(
                    f"<div class='store-label'>{seller.get('store_name','LOJA')}</div>",
                    unsafe_allow_html=True,
                )
                st.subheader(product["name"])
                st.caption(product.get("description") or "Produto disponível.")
                st.markdown(
                    f"<div class='price'>{money(product['price'])}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div class='muted'>Estoque: {product.get('stock_quantity',0)}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div></div>", unsafe_allow_html=True)


def seller_products_page(seller: dict) -> None:
    hero(
        "Minha loja",
        "Cadastre produtos com foto, custo, preço, margem e controle de estoque.",
    )

    tab_catalog, tab_new = st.tabs(["Catálogo e resultado", "Cadastrar produto"])

    with tab_new:
        categories = db.rows("categories", "id,name", active=True)
        category_map = {c["name"]: c["id"] for c in categories}

        with st.form("new_product", clear_on_submit=True):
            c1, c2 = st.columns([1.2, 0.8])

            with c1:
                name = st.text_input("Nome do produto *")
                description = st.text_area("Descrição")
                category_name = st.selectbox(
                    "Categoria",
                    list(category_map.keys()) if category_map else ["Sem categoria"],
                )
                origin = st.selectbox(
                    "Origem",
                    ["marketplace", "vending"],
                    format_func=lambda value: {
                        "marketplace": "Marketplace",
                        "vending": "Vending Machine",
                    }[value],
                )
                image = st.file_uploader(
                    "Foto do produto *",
                    type=["jpg", "jpeg", "png", "webp"],
                )

            with c2:
                cost_price = st.number_input(
                    "Custo unitário",
                    min_value=0.0,
                    step=0.50,
                    format="%.2f",
                )
                sale_price = st.number_input(
                    "Preço de venda *",
                    min_value=0.0,
                    step=0.50,
                    format="%.2f",
                )
                stock = st.number_input(
                    "Estoque inicial",
                    min_value=0,
                    step=1,
                )
                allow_credit = st.checkbox(
                    "Permitir compra no fim do mês",
                    value=True,
                )
                active = st.checkbox("Publicar no marketplace", value=True)

                unit_profit = sale_price - cost_price
                margin = (unit_profit / sale_price * 100) if sale_price > 0 else 0
                markup = (sale_price / cost_price) if cost_price > 0 else 0

                st.metric("Lucro unitário", money(unit_profit))
                st.metric("Margem sobre venda", f"{margin:.1f}%")
                st.metric("Multiplicador do custo", f"{markup:.2f}x")

            submit = st.form_submit_button(
                "Cadastrar e publicar",
                use_container_width=True,
            )

        if submit:
            if not name.strip():
                st.warning("Informe o nome do produto.")
            elif sale_price <= 0:
                st.warning("Informe um preço de venda válido.")
            elif image is None:
                st.warning("Adicione uma foto do produto.")
            elif cost_price > sale_price:
                st.warning(
                    "O custo está acima do preço de venda. "
                    "Revise os valores antes de publicar."
                )
            else:
                try:
                    image_url, image_path = db.upload_product_image(
                        image,
                        seller["id"],
                    )
                    db.create_product(
                        {
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
                        }
                    )
                    st.success("Produto cadastrado com foto e análise de lucro.")
                    st.rerun()
                except Exception as exc:
                    show_error(exc)

    with tab_catalog:
        products = db.rows("products", seller_id=seller["id"])

        if not products:
            st.info("Nenhum produto cadastrado.")
            return

        rows = []
        for product in products:
            cost = float(product.get("cost_price") or 0)
            price = float(product.get("price") or 0)
            stock = int(product.get("stock_quantity") or 0)
            unit_profit = price - cost
            margin = (unit_profit / price * 100) if price > 0 else 0

            rows.append(
                {
                    "Produto": product["name"],
                    "Custo": cost,
                    "Venda": price,
                    "Lucro unitário": unit_profit,
                    "Margem %": round(margin, 1),
                    "Estoque": stock,
                    "Lucro potencial": unit_profit * stock,
                    "Publicado": bool(product.get("active")),
                }
            )

        df = pd.DataFrame(rows)

        total_cost = (df["Custo"] * df["Estoque"]).sum()
        potential_profit = df["Lucro potencial"].sum()
        avg_margin = df["Margem %"].mean() if not df.empty else 0

        cols = st.columns(3)
        with cols[0]:
            metric_card("Custo total do estoque", money(total_cost))
        with cols[1]:
            metric_card("Lucro potencial", money(potential_profit))
        with cols[2]:
            metric_card("Margem média", f"{avg_margin:.1f}%")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Custo": st.column_config.NumberColumn(format="R$ %.2f"),
                "Venda": st.column_config.NumberColumn(format="R$ %.2f"),
                "Lucro unitário": st.column_config.NumberColumn(format="R$ %.2f"),
                "Lucro potencial": st.column_config.NumberColumn(format="R$ %.2f"),
                "Margem %": st.column_config.NumberColumn(format="%.1f%%"),
            },
        )

        st.markdown("### Visual dos produtos")
        for start in range(0, len(products), 3):
            cols = st.columns(3)
            for col, product in zip(cols, products[start:start + 3]):
                with col:
                    with st.container(border=True):
                        if product.get("image_url"):
                            st.image(product["image_url"], use_container_width=True)
                        st.subheader(product["name"])
                        cost = float(product.get("cost_price") or 0)
                        price = float(product.get("price") or 0)
                        profit = price - cost
                        st.write(f"**Custo:** {money(cost)}")
                        st.write(f"**Venda:** {money(price)}")
                        st.write(f"**Lucro unitário:** {money(profit)}")
                        st.caption(
                            f"Estoque: {product.get('stock_quantity', 0)}"
                        )


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

    with st.sidebar:
        st.markdown("## ⚡ Clique&Leve")
        st.caption("Marketplace interno premium")
        st.divider()

        options = ["Início", "Marketplace"]
        if profile["role"] == "vendedor":
            options.append("Minha loja")

        page = st.radio(
            "Navegação",
            options,
            label_visibility="collapsed",
        )

        st.divider()
        st.caption(profile.get("full_name", "Usuário"))
        st.caption(profile["role"].capitalize())

        if st.button("Sair", use_container_width=True):
            db.logout()
            st.rerun()

    if page == "Início":
        dashboard(profile, seller)
    elif page == "Marketplace":
        marketplace_page()
    elif page == "Minha loja":
        if not seller:
            st.error("Seu perfil ainda não está vinculado a uma loja.")
        else:
            seller_products_page(seller)


if __name__ == "__main__":
    main()
