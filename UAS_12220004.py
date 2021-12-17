##------------------------------------------LIBRARY-------------------------------------------------------##
from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
##-----------------------------------------DATA SOURCE----------------------------------------------------##
dataset_country=pd.read_json('kode_negara_lengkap.json')
dataset_production=pd.read_csv("produksi_minyak_mentah.csv")
dfc=pd.DataFrame (dataset_country)
dfp=pd.DataFrame (dataset_production)
df_merge = pd.merge(dfp,dfc,left_on='kode_negara',right_on='alpha-3')
#-------------------------------------------FUNCTION-------------------------------------------------------#
def search_country_in_data(Country_Full_Name):
    dfc2=df_merge[df_merge.name==Country_Full_Name]
    index=pd.DataFrame(dfc2).index
    return index
def Chart_data1(index_negara):
    data=df_merge.loc[index_negara]
    plot_graph=data.iloc[:,1:3]
    return plot_graph
def Graph_Display1(data,judul):
    chart=px.scatter(data_frame=data,x="tahun",y="produksi",color="produksi",title=(judul+' Oil Production'))
    st.write(chart)
    return chart
def maxprod_yearsort(year):
    data=df_merge.loc[df_merge['tahun']==year]
    data_produksi_terbesar=data.sort_values(by='produksi',ascending=False)
    return data_produksi_terbesar
def Chart_data2(x,rank):
    databesar=x.head(rank)
    databesar_plot=databesar.iloc[:,2:4]
    return databesar_plot
def Chart_data3(a,b,c,d,e,v,w,x,y,z):
    column1=a['produksi'].max()
    column2=b['produksi'].max()
    column3=c['produksi'].max()
    column4=d['produksi'].max()
    column5=e['produksi'].max()
    column={'Production':[column1,column2,column3,column4,column5],'Country':[v,w,x,y,z]}
    df=pd.DataFrame(data=column)
    return df
##---------------------------------------GUI DEVELOPMENT--------------------------------------------------##
############################################################################################################
#-------------------------------------------MAIN MENU------------------------------------------------------#
List=["MAIN MENU","OIL PRODUCTION OF A COUNTRY (1971-2015)","TOP PRODUCTION IN A YEAR","TOP PRODUCTION OF EACH COUNTRY","HIGHEST OIL PRODUCTION IN A YEAR"]
add_selectbox=st.sidebar.selectbox(label='CHOOSE',options=List)
if add_selectbox=='OIL PRODUCTION OF A COUNTRY (1971-2015)':
    st.subheader("Global Oil Production Website")
    st.caption("Data from 1971-2015")
    Nama_Negara=dfc.iloc[:,0]
    negara=st.selectbox("CHOOSE YOUR COUNTRY",Nama_Negara)
    st.caption("** If the graphic is empty, means we dont have the data, sorry:(")
    st.caption("*** Try to input another country :D")
    index_negara=search_country_in_data(negara)
    data_plot=Chart_data1(index_negara)
    Graph_Display1(data_plot,negara)
elif add_selectbox=='TOP PRODUCTION IN A YEAR':
    st.subheader("Global Oil Production Website")
    st.caption("Data from 1971-2015")
    year=st.slider("Pick A Year",min_value=1971,max_value=2015,key='nomor2')
    dataprod_yearsort=maxprod_yearsort(year)
    rank=st.number_input(("TOP 10 COUNTRY PRODUCTION IN "+str(year)),min_value=1,max_value=10)
    plot_data2=Chart_data2(dataprod_yearsort,rank)
    bar_top10=px.bar(plot_data2,x='name',y='produksi',color='produksi',labels={'name':'Country','produksi':'Production'})
    st.write(bar_top10)
elif add_selectbox=='TOP PRODUCTION OF EACH COUNTRY':
    st.subheader("Global Oil Production Website")
    st.caption("Data from 1971-2015")
    countryname=dfc.iloc[:,0]
    negara1=st.selectbox("Choose Your 1st Country",countryname)
    negara2=st.selectbox('Choose Your 2nd Country',countryname)
    negara3=st.selectbox('Choose Your 3rd Country',countryname)
    negara4=st.selectbox('Choose your 4th Country',countryname)
    negara5=st.selectbox('Choose Yoyr 5th Country',countryname)
    listnegara=[negara1,negara2,negara3,negara4,negara5]
    data1=search_country_in_data(negara1)
    data2=search_country_in_data(negara2)
    data3=search_country_in_data(negara3)
    data4=search_country_in_data(negara4)
    data5=search_country_in_data(negara5)
    cd1=Chart_data1(data1)
    cd2=Chart_data1(data2)
    cd3=Chart_data1(data3)
    cd4=Chart_data1(data4)
    cd5=Chart_data1(data5)
    df3=Chart_data3(cd1,cd2,cd3,cd4,cd5,negara1,negara2,negara3,negara4,negara5)
    bar_top5=px.bar(df3,x='Country',y='Production',color='Production',title='Top Production of Each Country')
    st.write(bar_top5)
elif add_selectbox=='HIGHEST OIL PRODUCTION IN A YEAR':
    st.subheader("Global Oil Production Website")
    st.caption("Data from 1971-2015")
    namacountry=df_merge.iloc[:,3]
    kodecountry=df_merge.iloc[:,0]
    region_subregion=df_merge.iloc[:,8:10]
    produksi=df_merge.iloc[:,2]
    tahun=st.slider("Pick A Year",min_value=1971,max_value=2015,key='nomor4')
    tahun_sort=maxprod_yearsort(tahun)
    tahun_sort=tahun_sort[tahun_sort['produksi']!=0]
    kecil=tahun_sort.nsmallest(1,'produksi')
    column_max=[tahun_sort.iloc[0,3],tahun_sort.iloc[0,2],tahun_sort.iloc[0,8],tahun_sort.iloc[0,9]]
    column_min=[kecil.iloc[0,3],kecil.iloc[0,2],kecil.iloc[0,8],kecil.iloc[0,9]]
    st.write('Highest Oil Production in ',str(tahun),' was from ',column_max[0],',',column_max[3],',',column_max[2],'. With production at ',str(column_max[1]),' BO.')
    st.write('Lowest Oil Production in ',str(tahun),' was from ',column_min[0],',',column_min[3],',',column_min[2],'. With production at ',str(column_min[1]),' BO.')
elif add_selectbox=='MAIN MENU':
    col1,col2,col3=st.columns(3)
    with col2:
        logo=Image.open('IMG_1581.png')
        st.title('WELCOME')
    with col1:
        st.image(logo,width=500)
        st.empty()
else:
    col1,col2,col3=st.columns(3)
    with col2:
        logo=Image.open('IMG_1581.png')
        st.title('WELCOME')
    with col1:
        st.image(logo,width=500)
        st.empty()