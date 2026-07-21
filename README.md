# Clique&Leve — MVP operacional

Primeira versão funcional conectada à base Supabase V2.0.

## Módulos disponíveis

- Login com Supabase Auth
- Dashboard por perfil
- Marketplace
- Administração de vendedores
- Cadastro de clientes
- Cadastro de produtos
- Crédito individual por vendedor
- Registro de venda a prazo
- Contas a receber
- Baixas totais e parciais
- Status compartilhado sem revelar valores
- Contato direto por WhatsApp

## 1. Configurar segredos

Copie:

`.streamlit/secrets.example.toml`

para:

`.streamlit/secrets.toml`

Preencha:

```toml
SUPABASE_URL = "https://..."
SUPABASE_KEY = "sb_publishable_..."
```

Não use Secret Key ou `service_role`.

## 2. Instalar

```bash
pip install -r requirements.txt
```

## 3. Executar

```bash
streamlit run app.py
```

## 4. Primeiro acesso

Use o usuário que já foi criado em:

**Supabase → Authentication → Users**

e promovido para `administrador` na tabela `profiles`.

## 5. Criar vendedores

Para o administrador transformar alguém em vendedor:

1. crie o usuário em Supabase Authentication;
2. entre no Clique&Leve como administrador;
3. abra **Administração**;
4. escolha o usuário;
5. informe o nome da loja e WhatsApp;
6. clique em **Ativar vendedor**.

## Observação sobre o MVP

Nesta primeira versão, o vendedor cadastra seus clientes. A futura versão terá
convite do cliente, carrinho, pedidos online, integração PIX e notificações.

## Direção visual

- Azul profundo
- Verde-lima como acento
- Tipografia limpa
- Atmosfera de fintech corporativa + marketplace premium
