from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import streamlit as st
from supabase import Client, create_client


class AppError(RuntimeError):
    pass


def _secrets() -> tuple[str, str]:
    try:
        return st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
    except Exception as exc:
        raise AppError(
            "Configure SUPABASE_URL e SUPABASE_KEY nos Secrets do Streamlit."
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


def create_product(payload: dict[str, Any]) -> dict[str, Any]:
    result = get_client().table("products").insert(payload).execute()
    if not result.data:
        raise AppError("O produto não foi salvo.")
    return result.data[0]


def update_product(product_id: str, payload: dict[str, Any]) -> None:
    get_client().table("products").update(payload).eq("id", product_id).execute()


def delete_product_image(image_path: str | None) -> None:
    if not image_path:
        return
    try:
        get_client().storage.from_("product-images").remove([image_path])
    except Exception:
        pass


def upload_product_image(
    uploaded_file: Any,
    seller_id: str,
) -> tuple[str, str]:
    """
    Retorna (public_url, storage_path).
    A imagem é salva em product-images/<seller_id>/<uuid>.<ext>
    """
    if uploaded_file is None:
        raise AppError("Selecione uma foto.")

    suffix = Path(uploaded_file.name).suffix.lower() or ".jpg"
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise AppError("Use uma imagem JPG, JPEG, PNG ou WEBP.")

    storage_path = f"{seller_id}/{uuid4().hex}{suffix}"
    content = uploaded_file.getvalue()
    content_type = uploaded_file.type or "image/jpeg"

    get_client().storage.from_("product-images").upload(
        path=storage_path,
        file=content,
        file_options={
            "content-type": content_type,
            "upsert": "false",
        },
    )

    public_url = get_client().storage.from_("product-images").get_public_url(storage_path)
    return public_url, storage_path
