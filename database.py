from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import streamlit as st
from supabase import Client, create_client


class AppError(RuntimeError):
    pass


def _secrets() -> tuple[str, str]:
    try:
        return st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
    except Exception as exc:
        raise AppError(
            "Configure SUPABASE_URL e SUPABASE_KEY em .streamlit/secrets.toml."
        ) from exc


def new_client() -> Client:
    url, key = _secrets()
    return create_client(url, key)


def get_client() -> Client:
    if "supabase" not in st.session_state:
        st.session_state.supabase = new_client()
    return st.session_state.supabase


def login(email: str, password: str) -> dict[str, Any]:
    sb = new_client()
    response = sb.auth.sign_in_with_password({"email": email, "password": password})
    if not response.session or not response.user:
        raise AppError("Não foi possível iniciar a sessão.")
    st.session_state.supabase = sb
    st.session_state.user = response.user
    st.session_state.access_token = response.session.access_token
    st.session_state.refresh_token = response.session.refresh_token
    return get_my_profile()


def restore_session() -> bool:
    if st.session_state.get("user") and st.session_state.get("supabase"):
        return True
    access = st.session_state.get("access_token")
    refresh = st.session_state.get("refresh_token")
    if not access or not refresh:
        return False
    try:
        sb = new_client()
        result = sb.auth.set_session(access, refresh)
        st.session_state.supabase = sb
        st.session_state.user = result.user
        return bool(result.user)
    except Exception:
        return False


def logout() -> None:
    try:
        get_client().auth.sign_out()
    except Exception:
        pass
    for key in ("supabase", "user", "profile", "access_token", "refresh_token"):
        st.session_state.pop(key, None)


def get_my_profile() -> dict[str, Any]:
    user = st.session_state.get("user")
    if not user:
        raise AppError("Sessão não encontrada.")
    result = (
        get_client()
        .table("profiles")
        .select("*")
        .eq("id", str(user.id))
        .single()
        .execute()
    )
    profile = result.data
    st.session_state.profile = profile
    return profile


def current_seller() -> dict[str, Any] | None:
    profile = st.session_state.get("profile") or get_my_profile()
    result = (
        get_client()
        .table("sellers")
        .select("*")
        .eq("profile_id", profile["id"])
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def rows(table: str, select: str = "*", **filters: Any) -> list[dict[str, Any]]:
    query = get_client().table(table).select(select)
    for key, value in filters.items():
        if value is not None:
            query = query.eq(key, value)
    return query.execute().data or []


def create_customer(payload: dict[str, Any]) -> dict[str, Any]:
    result = get_client().table("customers").insert(payload).execute()
    return result.data[0]


def update_customer(customer_id: str, payload: dict[str, Any]) -> None:
    get_client().table("customers").update(payload).eq("id", customer_id).execute()


def create_product(payload: dict[str, Any]) -> dict[str, Any]:
    result = get_client().table("products").insert(payload).execute()
    return result.data[0]


def update_product(product_id: str, payload: dict[str, Any]) -> None:
    get_client().table("products").update(payload).eq("id", product_id).execute()


def upsert_credit(payload: dict[str, Any]) -> None:
    get_client().table("seller_customer_credit").upsert(
        payload, on_conflict="seller_id,customer_id"
    ).execute()


def create_receivable(payload: dict[str, Any]) -> dict[str, Any]:
    result = get_client().table("receivables").insert(payload).execute()
    return result.data[0]


def register_payment(payload: dict[str, Any]) -> None:
    get_client().table("payments").insert(payload).execute()


def shared_status(customer_id: str) -> list[dict[str, Any]]:
    result = get_client().rpc(
        "get_customer_shared_status", {"p_customer_id": customer_id}
    ).execute()
    return result.data or []


def create_seller(profile_id: str, store_name: str, whatsapp: str) -> None:
    sb = get_client()
    sb.table("profiles").update({"role": "vendedor"}).eq("id", profile_id).execute()
    sb.table("sellers").insert(
        {
            "profile_id": profile_id,
            "store_name": store_name,
            "whatsapp": whatsapp,
            "active": True,
        }
    ).execute()
