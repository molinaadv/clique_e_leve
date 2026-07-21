# Clique&Leve — Streamlit

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar

1. Crie um repositório no GitHub.
2. Envie `app.py`, `requirements.txt` e a pasta `.streamlit`.
3. No Streamlit Community Cloud, clique em **New app**.
4. Escolha o repositório e informe `app.py` como arquivo principal.
5. Clique em **Deploy**.

O protótipo usa dados demonstrativos e `st.session_state`. A próxima fase é conectar Supabase para usuários, produtos, estoque, pedidos, faturas, comissões e repasses.
