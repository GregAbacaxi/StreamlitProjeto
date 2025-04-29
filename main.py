import streamlit as st

DEVICES = ['raidz2_sync', 'raidz2_async', 'raid6_xfs']
MODES = ['bw', 'iops', 'lat']

def get_images(rw, blocksize, filter,machine, type):
    lista_imagens = []
    for device in DEVICES:
        for mode in MODES:
            if rw == 'randrw':
                lista_imagens.append(f"benchs/{machine}/{type}/{device}/{rw}/{blocksize}/{device}_{rw}_{filter}_{blocksize}_{mode}.png")
            else:
                lista_imagens.append(f"benchs/{machine}/{type}/{device}/{blocksize}/{device}_{rw}_{blocksize}_{mode}.png")
    return lista_imagens

st.set_page_config(layout="wide")
st.title("Grelha Dinâmica de Imagens")

with st.sidebar:
    machine = st.selectbox("Escolha a máquina", ['83', '84'])
    all_io = ['sata-onboard', 'sata-sas', 'sas-sas']
    io_options = [io for io in all_io if not (machine == '84' and io == 'sata-onboard')]
    io_type = st.selectbox("Escolha o controlador I/O", io_options)
    rw = st.selectbox("Escolha o rw", ["randread", "randwrite", "randrw"])
    blocksize = st.selectbox("Escolha o blocksize", ["1M", "512k", "4k"])
    filter_type = None
    if rw == 'randrw': 
        filter_type = st.selectbox("Escolha o filter", ["read", "write"])

st.write(
    f"**Opções selecionadas:** MV={machine}, IO={io_type}, RW={rw}, "
    f"BS={blocksize}, FT={filter_type if filter_type else 'N/A'}"
)
images = get_images(rw, blocksize, filter_type, machine, io_type)
col_titles = ["Bandwidth", "IOPS", "Latência"]
row_titles = ["ZFS Sync", "ZFS Async", "XFS"]

for row_idx, row_title in enumerate(row_titles):
    st.markdown(f"### {row_title}")
    cols = st.columns(3)
    for col_idx, col_title in enumerate(col_titles):
        with cols[col_idx]:
            st.image(images[row_idx * 3 + col_idx], caption=col_title, width=300, use_container_width=True)

st.title("Melhores em cenários de utilização real")
melhores_imagens = []
melhores_imagens.append(f"benchs/84/sas-sas/raidz2_async/randrw/4k/raidz2_async_randrw_read_4k_iops.png")
melhores_imagens.append(f"benchs/83/sas-sas/raidz2_async/randrw/1M/raidz2_async_randrw_read_1M_bw.png")
melhores_imagens.append(f"benchs/84/sata-sas/raidz2_async/randrw/4k/raidz2_async_randrw_read_4k_lat.png")
melhores_imagens.append(f"benchs/84/sas-sas/raidz2_async/randrw/4k/raidz2_async_randrw_write_4k_iops.png")
melhores_imagens.append(f"benchs/83/sas-sas/raidz2_async/randrw/512k/raidz2_async_randrw_write_512k_bw.png")
melhores_imagens.append(f"benchs/84/sata-sas/raidz2_async/randrw/4k/raidz2_async_randrw_write_4k_lat.png")
best_iops_r = melhores_imagens[0]  
best_bw_r = melhores_imagens[1]    
best_lat_r = melhores_imagens[2]   
best_iops_w = melhores_imagens[3]  
best_bw_w = melhores_imagens[4]    
best_lat_w = melhores_imagens[5]

st.markdown("### Melhor IOPS de Leitura")
st.image(best_iops_r, caption="Melhor IOPS de Leitura", width=300, use_container_width=True)

st.markdown("### Melhor Bandwidth de Leitura")
st.image(best_bw_r, caption="Melhor Bandwidth de Leitura", width=300, use_container_width=True)

st.markdown("### Melhor Latência de Leitura")
st.image(best_lat_r, caption="Melhor Latência de Leitura", width=300, use_container_width=True)

st.markdown("### Melhor IOPS de Escrita")
st.image(best_iops_w, caption="Melhor IOPS de Escrita", width=300, use_container_width=True)

st.markdown("### Melhor Bandwidth de Escrita")
st.image(best_bw_w, caption="Melhor Bandwidth de Escrita", width=300, use_container_width=True)

st.markdown("### Melhor Latência de Escrita")
st.image(best_lat_w, caption="Melhor Latência de Escrita", width=300, use_container_width=True)

st.write("G.U. - J.R. - P.D // 2025 // v1.3")