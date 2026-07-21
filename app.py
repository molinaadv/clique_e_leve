import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title='Clique&Leve', page_icon='🛍️', layout='wide')

st.markdown('''
<style>
.stApp{background:#F5F8FC;color:#152238}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#06182A,#0B2E54)}
section[data-testid="stSidebar"] *{color:white}
.block-container{max-width:1450px;padding-top:1.4rem}
.hero{background:linear-gradient(120deg,#071A2D,#0E4E93 68%,#1671EE);border-radius:28px;padding:30px;color:white;margin-bottom:18px;box-shadow:0 18px 50px rgba(11,38,73,.11)}
.hero h1{font-size:36px;line-height:1.08;margin:0 0 12px}.hero p{color:#C9DDF0;font-size:16px;max-width:760px}
.badge{display:inline-block;padding:7px 10px;border-radius:999px;background:rgba(255,255,255,.12);font-size:12px;font-weight:800;margin-bottom:12px}
.card{background:white;border:1px solid #E6ECF4;border-radius:20px;padding:17px;box-shadow:0 8px 24px rgba(24,54,88,.05)}
.product{background:white;border:1px solid #E6ECF4;border-radius:20px;padding:15px;min-height:300px;box-shadow:0 8px 25px rgba(30,62,96,.05)}
.emoji{font-size:60px;text-align:center;background:linear-gradient(145deg,#EDF5FF,#E8FBFB);border-radius:16px;padding:18px}.store{color:#1267F2;font-size:11px;font-weight:900;text-transform:uppercase;margin-top:12px}.name{font-size:17px;font-weight:800;margin:5px 0}.desc{color:#708096;font-size:12px;min-height:40px}.price{font-size:22px;font-weight:900;margin-top:9px}
.stButton>button{border-radius:12px;font-weight:700}
</style>
''', unsafe_allow_html=True)

if 'cart' not in st.session_state: st.session_state.cart=[]
if 'orders' not in st.session_state:
    st.session_state.orders=[
        {'Pedido':'#1048','Loja':'Empadas da Ana','Item':'2 empadas','Valor':24.0,'Status':'Pronto','Data':'Hoje'},
        {'Pedido':'#1041','Loja':'Vending','Item':'Snickers Dark','Valor':5.99,'Status':'Retirado','Data':'Ontem'},
    ]

products=[
 {'id':1,'emoji':'🥟','store':'Empadas da Ana','name':'Empada artesanal','desc':'Frango cremoso, produção do dia.','price':12.0,'stock':15,'category':'Alimentação'},
 {'id':2,'emoji':'🧹','store':'Clique&Leve','name':'Aspirador vertical','desc':'Prático, leve e ideal para limpeza rápida.','price':220.0,'stock':4,'category':'Casa'},
 {'id':3,'emoji':'🤖','store':'Clique&Leve','name':'Robô aspirador','desc':'Produto sob pedido.','price':89.0,'stock':8,'category':'Casa'},
 {'id':4,'emoji':'🛍️','store':'Clique&Leve','name':'Mini seladora','desc':'Recarregável, compacta e fácil de usar.','price':25.0,'stock':10,'category':'Casa'},
 {'id':5,'emoji':'🥤','store':'Vending Clique&Leve','name':'Coca-Cola','desc':'Gelada, retirada imediata.','price':5.49,'stock':28,'category':'Vending'},
 {'id':6,'emoji':'🍫','store':'Vending Clique&Leve','name':'Snickers Dark','desc':'Chocolate disponível para retirada.','price':5.99,'stock':20,'category':'Vending'},
 {'id':7,'emoji':'🥗','store':'Marmita Leve','name':'Marmita fit','desc':'Frango, arroz integral e legumes.','price':22.0,'stock':12,'category':'Alimentação'},
 {'id':8,'emoji':'🎂','store':'Doces da Mari','name':'Bolo sob encomenda','desc':'Personalizado para aniversários.','price':120.0,'stock':6,'category':'Encomendas'},
]

def money(v):
    return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X','.')

def product_card(p, prefix):
    st.markdown(f'''<div class="product"><div class="emoji">{p['emoji']}</div><div class="store">{p['store']}</div><div class="name">{p['name']}</div><div class="desc">{p['desc']}</div><div class="price">{money(p['price'])}</div><div style="color:#708096;font-size:12px">{p['stock']} disponíveis</div></div>''', unsafe_allow_html=True)
    if st.button('Adicionar ao pedido', key=f'{prefix}_{p["id"]}', use_container_width=True):
        st.session_state.cart.append(p); st.success(f'{p["name"]} adicionado.')

with st.sidebar:
    st.markdown('## 🛍️ Clique&Leve')
    st.caption('O marketplace exclusivo da sua empresa')
    role=st.selectbox('Perfil',['Membro','Parceiro','Administrador'])
    pages={
      'Membro':['Início','Marketplace','Meus pedidos','Minha conta','Níveis e benefícios','Preciso comprar'],
      'Parceiro':['Painel do parceiro','Produtos da minha loja','Pedidos da minha loja','Repasses'],
      'Administrador':['Dashboard administrativo','Parceiros','Financeiro','Controle de crédito']
    }
    page=st.radio('Navegação',pages[role])

if page=='Início':
    st.markdown('''<div class="hero"><div class="badge">ECONOMIA INTERNA • EXCLUSIVO PARA MEMBROS</div><h1>Compre de quem está perto.<br>Fortaleça quem faz parte.</h1><p>Produtos, alimentação, serviços, vending e oportunidades em um único ambiente, com controle de limite e pagamento no fechamento mensal.</p></div>''', unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    a.metric('Fatura atual','R$ 19,00','Vence em 10/08'); b.metric('Limite disponível','R$ 31,00','Nível Bronze'); c.metric('Pontos do clube','74','+18 neste mês'); d.metric('Pedidos ativos','3','1 pronto')
    st.subheader('Feito por gente daqui')
    cols=st.columns(4)
    partners=[('🥟','Empadas da Ana','Alimentação • 4,9 ★'),('🍰','Doces da Mari','Sobremesas • 4,8 ★'),('🥗','Marmita Leve','Refeições • 4,7 ★'),('🎁','Ateliê 360','Presentes • 5,0 ★')]
    for col,(e,n,s) in zip(cols,partners):
        col.markdown(f'<div class="card"><div style="font-size:34px">{e}</div><b>{n}</b><br><span style="color:#708096;font-size:12px">{s}</span></div>',unsafe_allow_html=True)
    st.subheader('Destaques de hoje')
    cols=st.columns(4)
    for col,p in zip(cols,products[:4]):
        with col: product_card(p,'home')

elif page=='Marketplace':
    st.title('Marketplace'); st.caption('Produtos próprios, parceiros, vending, serviços e usados.')
    categories=['Todas']+sorted(set(p['category'] for p in products)); cat=st.selectbox('Categoria',categories); q=st.text_input('Buscar')
    filtered=[p for p in products if (cat=='Todas' or p['category']==cat) and (not q or q.lower() in (p['name']+' '+p['store']+' '+p['category']).lower())]
    for i in range(0,len(filtered),4):
        cols=st.columns(4)
        for col,p in zip(cols,filtered[i:i+4]):
            with col: product_card(p,'market')
    if st.session_state.cart:
        st.divider(); st.subheader('Seu pedido')
        total=sum(i['price'] for i in st.session_state.cart)
        for i in st.session_state.cart: st.write(f"• {i['name']} — {money(i['price'])}")
        st.markdown(f'### Total: {money(total)}'); payment=st.selectbox('Pagamento',['Fechamento mensal','PIX'])
        if st.button('Confirmar pedido',type='primary'):
            st.session_state.orders.append({'Pedido':f'#{1050+len(st.session_state.orders)}','Loja':'Marketplace','Item':f'{len(st.session_state.cart)} item(ns)','Valor':total,'Status':'Confirmado','Data':date.today().strftime('%d/%m/%Y')}); st.session_state.cart=[]; st.success('Pedido confirmado.')

elif page=='Meus pedidos':
    st.title('Meus pedidos'); df=pd.DataFrame(st.session_state.orders); df['Valor']=df['Valor'].apply(money); st.dataframe(df,use_container_width=True,hide_index=True)

elif page=='Minha conta':
    st.title('Minha conta'); c1,c2=st.columns([1.4,1])
    with c1:
        st.subheader('Fatura do mês'); st.metric('Total atual','R$ 19,00'); df=pd.DataFrame([{'Descrição':'Coca-Cola','Categoria':'Vending','Valor':'R$ 5,49'},{'Descrição':'Empada artesanal','Categoria':'Parceiro','Valor':'R$ 12,00'},{'Descrição':'Água','Categoria':'Vending','Valor':'R$ 1,51'}]); st.dataframe(df,hide_index=True,use_container_width=True)
    with c2:
        st.subheader('Limite de confiança'); st.metric('Nível Bronze','R$ 50,00','R$ 31,00 disponível'); st.progress(.38); st.caption('2 de 3 ciclos para alcançar o nível Prata.')

elif page=='Níveis e benefícios':
    st.title('Níveis do Clube'); cols=st.columns(4); levels=[('🥉 Bronze','R$ 50','Nível inicial'),('🥈 Prata','R$ 100','Bom histórico'),('🥇 Ouro','R$ 150','Cliente recorrente'),('💎 Black','R$ 300','Máxima confiança')]
    for col,(n,v,s) in zip(cols,levels): col.markdown(f'<div class="card"><span>{n}</span><div style="font-size:24px;font-weight:900;margin:8px 0">{v}</div><small>{s}</small></div>',unsafe_allow_html=True)

elif page=='Preciso comprar':
    st.title('Preciso comprar'); c1,c2=st.columns([1.3,1])
    with c1: st.dataframe(pd.DataFrame([{'Pedido':'Notebook usado para estudos','Orçamento':'Até R$ 2.000','Prazo':'7 dias','Propostas':4},{'Pedido':'Bolo para aniversário','Orçamento':'Até R$ 180','Prazo':'Sexta-feira','Propostas':3}]),hide_index=True,use_container_width=True)
    with c2:
        with st.form('need'):
            st.text_input('O que você precisa?'); st.text_input('Orçamento máximo'); st.date_input('Prazo'); st.text_area('Detalhes')
            if st.form_submit_button('Enviar aos parceiros',type='primary'): st.success('Solicitação enviada.')

elif page=='Painel do parceiro':
    st.title('Painel do parceiro'); a,b,c,d=st.columns(4); a.metric('Vendas do mês','R$ 1.248','+18%'); b.metric('Valor a receber','R$ 998,40'); c.metric('Comissão','R$ 249,60','20%'); d.metric('Pedidos pendentes','11')
    c1,c2=st.columns([1.4,1])
    with c1: st.dataframe(pd.DataFrame([{'Cliente':'Fernanda','Produto':'Empada de frango','Qtd.':2,'Líquido':'R$ 20,00','Status':'Produzir'},{'Cliente':'Marcos','Produto':'Empada de carne','Qtd.':1,'Líquido':'R$ 10,00','Status':'Pronto'}]),hide_index=True,use_container_width=True)
    with c2:
        net=st.number_input('Preço líquido desejado',0.0,10.0,.5); commission=st.number_input('Comissão (%)',0.0,20.0,1.0); final=net/(1-commission/100) if commission<100 else 0; st.text_input('Preço final calculado',money(final),disabled=True)
        if st.button('Salvar disponibilidade',type='primary'): st.success('Atualizado.')

elif page=='Produtos da minha loja':
    st.title('Produtos da minha loja'); st.dataframe(pd.DataFrame([{'Produto':'Empada de frango','Estoque':15,'Preço líquido':'R$ 10,00','Preço final':'R$ 12,50','Status':'Ativo'},{'Produto':'Empada de carne','Estoque':8,'Preço líquido':'R$ 10,00','Preço final':'R$ 12,50','Status':'Ativo'}]),hide_index=True,use_container_width=True)

elif page=='Pedidos da minha loja':
    st.title('Pedidos da minha loja'); st.dataframe(pd.DataFrame([{'Pedido':'#223','Cliente':'Fernanda','Produto':'2 empadas','Total':'R$ 24,00','Seu líquido':'R$ 20,00','Status':'Produzir'}]),hide_index=True,use_container_width=True)

elif page=='Repasses':
    st.title('Repasses'); st.metric('Saldo disponível','R$ 998,40'); st.dataframe(pd.DataFrame([{'Período':'Julho/2026','Venda bruta':'R$ 1.248,00','Comissão':'R$ 249,60','Líquido':'R$ 998,40','Previsão':'05/08','Status':'Programado'}]),hide_index=True,use_container_width=True)

elif page=='Dashboard administrativo':
    st.title('Gestão Clique&Leve'); a,b,c,d=st.columns(4); a.metric('GMV do mês','R$ 18.420','+21%'); b.metric('Receita da plataforma','R$ 3.112','+17%'); c.metric('Membros ativos','186','82% compraram'); d.metric('Parceiros ativos','14','38 produtos')
    c1,c2=st.columns([1.4,1])
    with c1: st.subheader('Vendas por semana'); st.bar_chart(pd.DataFrame({'Semana':['S1','S2','S3','S4','S5'],'Vendas':[2400,3650,5210,4620,6540]}).set_index('Semana'))
    with c2: st.subheader('Receita por origem'); st.metric('Comissões','R$ 1.460'); st.metric('Margem própria','R$ 1.087'); st.metric('Vending','R$ 565')

elif page=='Parceiros':
    st.title('Parceiros'); st.dataframe(pd.DataFrame([{'Parceiro':'Empadas da Ana','Categoria':'Alimentação','Vendas':'R$ 1.248','Comissão':'20%','Avaliação':'4,9','Status':'Ativo'},{'Parceiro':'Doces da Mari','Categoria':'Doces','Vendas':'R$ 820','Comissão':'15%','Avaliação':'4,8','Status':'Ativo'}]),hide_index=True,use_container_width=True)

elif page=='Financeiro':
    st.title('Financeiro'); df=pd.DataFrame([{'Parceiro':'Empadas da Ana','Venda bruta':'R$ 1.248,00','Comissão':'R$ 249,60','Líquido':'R$ 998,40','Repasse':'05/08','Status':'Programado'},{'Parceiro':'Doces da Mari','Venda bruta':'R$ 820,00','Comissão':'R$ 123,00','Líquido':'R$ 697,00','Repasse':'05/08','Status':'Conferido'}]); st.dataframe(df,hide_index=True,use_container_width=True); st.download_button('Baixar relatório CSV',df.to_csv(index=False).encode('utf-8'),file_name='financeiro_clique_leve.csv',mime='text/csv')

elif page=='Controle de crédito':
    st.title('Controle de crédito'); st.dataframe(pd.DataFrame([{'Membro':'Ana Souza','Nível':'Bronze','Limite':'R$ 50','Usado':'R$ 19','Disponível':'R$ 31','Status':'Regular'},{'Membro':'Carlos Lima','Nível':'Prata','Limite':'R$ 100','Usado':'R$ 68','Disponível':'R$ 32','Status':'Regular'},{'Membro':'João Silva','Nível':'Ouro','Limite':'R$ 150','Usado':'R$ 150','Disponível':'R$ 0','Status':'Bloqueado'}]),hide_index=True,use_container_width=True)

st.markdown('---'); st.caption('Clique&Leve • A economia da empresa acontece aqui.')
