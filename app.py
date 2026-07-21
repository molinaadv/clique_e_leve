from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from urllib.parse import quote

import pandas as pd
import streamlit as st

import database as db
from styles import apply_styles, hero, metric_card, status_badge


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
    left, center, right = st.columns([1, 1.15, 1])
    with center:
        st.markdown("<div style='height:8vh'></div>", unsafe_allow_html=True)
        hero("Clique&Leve", "Marketplace interno e rede privada de confiança.")
        with st.form("login"):
            st.subheader("Acessar plataforma")
            email = st.text_input("E-mail", placeholder="voce@empresa.com")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        if submitted:
            try:
                db.login(email.strip(), password)
                st.rerun()
            except Exception as exc:
                show_error(exc)
        st.caption("A conta deve ser criada previamente no Supabase Authentication.")


def dashboard(profile, seller) -> None:
    hero(
        f"Olá, {profile.get('full_name', 'usuário')}",
        "Controle de vendas, crédito e confiança em uma única operação.",
    )
    if profile["role"] == "vendedor" and seller:
        products = db.rows("products", seller_id=seller["id"])
        customers = db.rows("seller_customer_credit", seller_id=seller["id"])
        receivables = db.rows("receivables", seller_id=seller["id"])
        open_total = sum(float(r["balance_due"]) for r in receivables if r["status"] != "cancelada")
        overdue = sum(
            float(r["balance_due"])
            for r in receivables
            if r["status"] == "vencida"
        )
        cols = st.columns(4)
        with cols[0]: metric_card("Produtos", str(len(products)))
        with cols[1]: metric_card("Clientes com crédito", str(len(customers)))
        with cols[2]: metric_card("Total em aberto", money(open_total))
        with cols[3]: metric_card("Total vencido", money(overdue))
    elif profile["role"] == "administrador":
        sellers = db.rows("sellers")
        products = db.rows("products")
        customers = db.rows("customers")
        cols = st.columns(3)
        with cols[0]: metric_card("Vendedores ativos", str(len([x for x in sellers if x["active"]])))
        with cols[1]: metric_card("Clientes cadastrados", str(len(customers)))
        with cols[2]: metric_card("Produtos publicados", str(len([x for x in products if x["active"]])))
    else:
        products = db.rows("products", active=True)
        metric_card("Produtos disponíveis", str(len(products)))

    st.markdown("### Visão da plataforma")
    st.info(
        "O crédito é concedido diretamente por cada vendedor. "
        "Outros vendedores enxergam apenas o status, nunca o valor da dívida."
    )


def marketplace_page() -> None:
    hero("Marketplace", "Descubra produtos e serviços da comunidade Clique&Leve.")
    products = db.rows(
        "products",
        "id,name,description,price,stock_quantity,image_url,origin,seller_id,active",
        active=True,
    )
    sellers = {x["id"]: x for x in db.rows("sellers", "id,store_name,whatsapp")}
    if not products:
        st.info("Nenhum produto publicado.")
        return

    search = st.text_input("Buscar produto ou loja", placeholder="Empada, bebida, serviço...")
    filtered = []
    for product in products:
        store = sellers.get(product["seller_id"], {}).get("store_name", "")
        hay = f"{product['name']} {product.get('description','')} {store}".lower()
        if search.lower() in hay:
            filtered.append(product)

    for i in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, product in zip(cols, filtered[i:i+3]):
            with col:
                store = sellers.get(product["seller_id"], {})
                with st.container(border=True):
                    st.subheader(product["name"])
                    st.caption(store.get("store_name", "Loja"))
                    st.write(product.get("description") or "Produto disponível na plataforma.")
                    st.markdown(f"### {money(product['price'])}")
                    st.caption(f"Estoque: {product['stock_quantity']} · {product['origin']}")
                    phone = store.get("whatsapp")
                    if phone:
                        msg = quote(f"Olá! Vi o produto {product['name']} no Clique&Leve.")
                        st.link_button(
                            "Falar com vendedor",
                            f"https://wa.me/{phone}?text={msg}",
                            use_container_width=True,
                        )


def customers_page(seller) -> None:
    hero("Meus clientes", "Cadastre clientes e administre sua própria relação de crédito.")
    tab1, tab2 = st.tabs(["Clientes", "Novo cliente"])

    with tab2:
        with st.form("new_customer"):
            name = st.text_input("Nome completo *")
            cpf = st.text_input("CPF")
            phone = st.text_input("Telefone / WhatsApp *")
            email = st.text_input("E-mail")
            notes = st.text_area("Observação interna")
            submitted = st.form_submit_button("Cadastrar cliente")
        if submitted:
            if not name.strip() or not phone.strip():
                st.warning("Informe nome e telefone.")
            else:
                try:
                    db.create_customer(
                        {
                            "full_name": name.strip(),
                            "cpf": cpf.strip() or None,
                            "phone": phone.strip(),
                            "email": email.strip() or None,
                            "notes": notes.strip() or None,
                            "created_by_seller_id": seller["id"],
                        }
                    )
                    st.success("Cliente cadastrado.")
                    st.rerun()
                except Exception as exc:
                    show_error(exc)

    with tab1:
        customers = db.rows(
            "customers",
            "id,full_name,cpf,phone,email,active,created_at",
            created_by_seller_id=seller["id"],
        )
        if not customers:
            st.info("Nenhum cliente cadastrado por esta loja.")
            return
        selected = st.selectbox(
            "Selecione o cliente",
            customers,
            format_func=lambda x: f"{x['full_name']} · {x.get('phone') or ''}",
        )
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(f"### {selected['full_name']}")
            st.write(f"**Telefone:** {selected.get('phone') or '—'}")
            st.write(f"**CPF:** {selected.get('cpf') or '—'}")
            st.write(f"**E-mail:** {selected.get('email') or '—'}")
        with c2:
            try:
                statuses = db.shared_status(selected["id"])
                st.markdown("### Status com outros vendedores")
                if not statuses:
                    st.caption("Sem histórico financeiro na plataforma.")
                for item in statuses:
                    st.markdown(
                        f"**{item['store_name']}** &nbsp; "
                        f"{status_badge(item['financial_status'])}",
                        unsafe_allow_html=True,
                    )
                    if item.get("whatsapp"):
                        st.link_button(
                            "Conversar",
                            f"https://wa.me/{item['whatsapp']}",
                            key=f"wa_{item['seller_id']}",
                        )
            except Exception as exc:
                show_error(exc)


def products_page(seller) -> None:
    hero("Produtos", "Gerencie sua vitrine, preços e estoque.")
    categories = db.rows("categories", "id,name", active=True)
    cat_map = {x["name"]: x["id"] for x in categories}
    tab1, tab2 = st.tabs(["Catálogo", "Novo produto"])
    with tab2:
        with st.form("new_product"):
            name = st.text_input("Nome do produto *")
            description = st.text_area("Descrição")
            category_name = st.selectbox("Categoria", list(cat_map.keys()))
            origin = st.selectbox("Origem", ["marketplace", "vending"])
            price = st.number_input("Preço de venda", min_value=0.0, step=0.50)
            stock = st.number_input("Estoque inicial", min_value=0, step=1)
            allow_credit = st.checkbox("Permitir venda no crédito deste vendedor", value=True)
            submit = st.form_submit_button("Cadastrar produto")
        if submit:
            if not name.strip() or price <= 0:
                st.warning("Informe nome e preço válido.")
            else:
                try:
                    db.create_product(
                        {
                            "seller_id": seller["id"],
                            "category_id": cat_map.get(category_name),
                            "name": name.strip(),
                            "description": description.strip() or None,
                            "origin": origin,
                            "price": price,
                            "stock_quantity": int(stock),
                            "allow_seller_credit": allow_credit,
                            "active": True,
                        }
                    )
                    st.success("Produto cadastrado.")
                    st.rerun()
                except Exception as exc:
                    show_error(exc)
    with tab1:
        products = db.rows("products", seller_id=seller["id"])
        if not products:
            st.info("Nenhum produto cadastrado.")
        else:
            df = pd.DataFrame(products)
            display = df[["name", "origin", "price", "stock_quantity", "active"]].copy()
            display.columns = ["Produto", "Origem", "Preço", "Estoque", "Ativo"]
            st.dataframe(display, use_container_width=True, hide_index=True)


def credit_page(seller, profile) -> None:
    hero("Crédito e confiança", "Cada limite pertence à relação entre sua loja e o cliente.")
    customers = db.rows(
        "customers",
        "id,full_name,phone",
        created_by_seller_id=seller["id"],
    )
    if not customers:
        st.info("Cadastre um cliente antes de conceder crédito.")
        return
    selected = st.selectbox(
        "Cliente",
        customers,
        format_func=lambda x: f"{x['full_name']} · {x.get('phone') or ''}",
    )
    existing = db.rows(
        "seller_customer_credit",
        seller_id=seller["id"],
        customer_id=selected["id"],
    )
    current = existing[0] if existing else {}
    with st.form("credit_form"):
        allow = st.checkbox(
            "Pode comprar a prazo com minha loja",
            value=current.get("can_buy_on_credit", False),
        )
        limit_value = st.number_input(
            "Limite concedido",
            min_value=0.0,
            value=float(current.get("credit_limit", 0)),
            step=10.0,
        )
        due_day = st.number_input(
            "Dia padrão de vencimento",
            min_value=1,
            max_value=28,
            value=int(current.get("due_day") or 10),
        )
        status = st.selectbox(
            "Status do crédito",
            ["liberado", "bloqueado", "suspenso"],
            index=["liberado", "bloqueado", "suspenso"].index(
                current.get("status", "bloqueado")
            ),
        )
        notes = st.text_area("Observação privada", value=current.get("private_notes") or "")
        submit = st.form_submit_button("Salvar política de crédito")
    if submit:
        try:
            db.upsert_credit(
                {
                    "seller_id": seller["id"],
                    "customer_id": selected["id"],
                    "can_buy_on_credit": allow,
                    "credit_limit": limit_value,
                    "due_day": int(due_day),
                    "status": status,
                    "private_notes": notes.strip() or None,
                    "granted_at": datetime.now().isoformat() if allow else None,
                }
            )
            st.success("Crédito atualizado.")
            st.rerun()
        except Exception as exc:
            show_error(exc)

    st.divider()
    st.subheader("Registrar venda a prazo")
    with st.form("new_receivable"):
        amount = st.number_input("Valor da venda", min_value=0.01, step=1.0)
        due = st.date_input("Vencimento")
        description = st.text_input("Descrição", placeholder="Empadas, produtos da vending...")
        submit_sale = st.form_submit_button("Gerar conta a receber")
    if submit_sale:
        open_rows = db.rows(
            "receivables",
            seller_id=seller["id"],
            customer_id=selected["id"],
        )
        open_balance = sum(
            float(x["balance_due"]) for x in open_rows if x["status"] != "cancelada"
        )
        credit_limit = float(current.get("credit_limit", 0))
        authorized = (
            current.get("can_buy_on_credit")
            and current.get("status") == "liberado"
            and open_balance + amount <= credit_limit
        )
        if not authorized:
            st.error("Venda não autorizada: verifique liberação, status e limite disponível.")
        else:
            try:
                db.create_receivable(
                    {
                        "seller_id": seller["id"],
                        "customer_id": selected["id"],
                        "original_amount": amount,
                        "balance_due": amount,
                        "due_date": due.isoformat(),
                        "status": "em_aberto",
                        "description": description.strip() or "Venda a prazo",
                        "created_by": profile["id"],
                    }
                )
                st.success("Venda lançada na conta do cliente.")
                st.rerun()
            except Exception as exc:
                show_error(exc)


def finance_page(seller, profile) -> None:
    hero("Financeiro", "Acompanhe contas e registre baixas totais ou parciais.")
    receivables = db.rows(
        "receivables",
        "id,customer_id,original_amount,balance_due,due_date,status,description,created_at",
        seller_id=seller["id"],
    )
    customers = {x["id"]: x for x in db.rows("customers", "id,full_name,phone")}
    if not receivables:
        st.info("Nenhuma conta a receber.")
        return

    for r in sorted(receivables, key=lambda x: x["due_date"]):
        customer = customers.get(r["customer_id"], {})
        with st.expander(
            f"{customer.get('full_name','Cliente')} · {money(r['balance_due'])} · {r['status']}"
        ):
            st.markdown(status_badge(r["status"]), unsafe_allow_html=True)
            st.write(f"**Descrição:** {r.get('description') or '—'}")
            st.write(f"**Valor original:** {money(r['original_amount'])}")
            st.write(f"**Saldo:** {money(r['balance_due'])}")
            st.write(f"**Vencimento:** {r['due_date']}")
            if float(r["balance_due"]) > 0 and r["status"] != "cancelada":
                with st.form(f"payment_{r['id']}"):
                    amount = st.number_input(
                        "Valor recebido",
                        min_value=0.01,
                        max_value=float(r["balance_due"]),
                        value=float(r["balance_due"]),
                        step=1.0,
                        key=f"amount_{r['id']}",
                    )
                    method = st.selectbox(
                        "Forma de pagamento",
                        ["pix", "dinheiro", "cartao", "outro"],
                        key=f"method_{r['id']}",
                    )
                    submit = st.form_submit_button("Registrar baixa")
                if submit:
                    try:
                        db.register_payment(
                            {
                                "receivable_id": r["id"],
                                "seller_id": seller["id"],
                                "customer_id": r["customer_id"],
                                "amount": amount,
                                "method": method,
                                "registered_by": profile["id"],
                            }
                        )
                        st.success("Pagamento registrado.")
                        st.rerun()
                    except Exception as exc:
                        show_error(exc)


def admin_page() -> None:
    hero("Administração", "Ative vendedores e acompanhe a saúde do ecossistema.")
    profiles = db.rows("profiles", "id,full_name,phone,role,active,created_at")
    sellers = db.rows("sellers", "id,profile_id,store_name,whatsapp,active")
    seller_by_profile = {x["profile_id"]: x for x in sellers}

    st.subheader("Transformar usuário em vendedor")
    eligible = [p for p in profiles if p["role"] != "administrador" and p["id"] not in seller_by_profile]
    if eligible:
        selected = st.selectbox(
            "Usuário",
            eligible,
            format_func=lambda x: f"{x['full_name']} · {x['role']}",
        )
        with st.form("create_seller"):
            store = st.text_input("Nome da loja")
            whatsapp = st.text_input("WhatsApp com DDI", placeholder="5592999999999")
            submit = st.form_submit_button("Ativar vendedor")
        if submit:
            try:
                db.create_seller(selected["id"], store.strip(), whatsapp.strip())
                st.success("Vendedor ativado.")
                st.rerun()
            except Exception as exc:
                show_error(exc)
    else:
        st.caption("Não há usuários elegíveis no momento.")

    st.divider()
    st.subheader("Vendedores")
    if sellers:
        st.dataframe(
            pd.DataFrame(sellers)[["store_name", "whatsapp", "active"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Nenhum vendedor cadastrado.")


def main() -> None:
    if not db.restore_session():
        login_page()
        return

    try:
        profile = st.session_state.get("profile") or db.get_my_profile()
    except Exception as exc:
        show_error(exc)
        db.logout()
        return

    seller = db.current_seller() if profile["role"] == "vendedor" else None

    with st.sidebar:
        st.markdown("## ⚡ Clique&Leve")
        st.caption("Marketplace exclusivo")
        st.divider()
        options = ["Início", "Marketplace"]
        if profile["role"] == "vendedor":
            options += ["Meus clientes", "Produtos", "Crédito", "Financeiro"]
        if profile["role"] == "administrador":
            options += ["Administração"]
        page = st.radio("Navegação", options, label_visibility="collapsed")
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
    elif page == "Meus clientes":
        customers_page(seller)
    elif page == "Produtos":
        products_page(seller)
    elif page == "Crédito":
        credit_page(seller, profile)
    elif page == "Financeiro":
        finance_page(seller, profile)
    elif page == "Administração":
        admin_page()


if __name__ == "__main__":
    main()
