import streamlit as st

DEVICES = ['raidz2_sync', 'raidz2_async', 'raid6_xfs']
MODES = ['bw', 'iops', 'lat']

# Geração de imagens tradicionais
def get_images(rw, blocksize, filter, machine, io_type):
    if machine == 'beegfs':
        lista_imagens = []
        for n in [1, 2]:
            for mode in MODES:
                if rw == 'randrw':
                    path = f"benchs/{machine}/beegfs_client_1cx{n}s_{rw}_{filter}_{blocksize}_{mode}.png"
                else:
                    path = f"benchs/{machine}/beegfs_client_1cx{n}s_{rw}_{blocksize}_{mode}.png"
                lista_imagens.append(path)
        return lista_imagens

    lista_imagens = []
    for device in DEVICES:
        for mode in MODES:
            if rw == 'randrw':
                lista_imagens.append(f"benchs/{machine}/{io_type}/{device}/{rw}/{blocksize}/{device}_{rw}_{filter}_{blocksize}_{mode}.png")
            else:
                lista_imagens.append(f"benchs/{machine}/{io_type}/{device}/{blocksize}/{device}_{rw}_{blocksize}_{mode}.png")
    return lista_imagens

st.set_page_config(layout="wide")
st.title("Grelha Dinâmica de Imagens")

with st.sidebar:
    machine = st.selectbox("Escolha a máquina", ['83', '84', 'beegfs'])
    io_type = None

    if machine != 'beegfs':
        all_io = ['sata-onboard', 'sata-sas', 'sas-sas']
        io_options = [io for io in all_io if not (machine == '84' and io == 'sata-onboard')]
        io_type = st.selectbox("Escolha o controlador I/O", io_options)

    rw = st.selectbox("Escolha o rw", ["randread", "randwrite", "randrw"])
    blocksize = st.selectbox("Escolha o blocksize", ["1M", "512k", "4k"])

    filter_type = None
    if rw == 'randrw':
        filter_type = st.selectbox("Escolha o filter", ["read", "write"])

# Exibição das opções escolhidas
st.write(
    f"**Opções selecionadas:** MV={machine}, " +
    (f"IO={io_type}, " if io_type else "") +
    f"RW={rw}, BS={blocksize}, FT={filter_type if filter_type else 'N/A'}"
)

images = get_images(rw, blocksize, filter_type, machine, io_type)
col_titles = ["Bandwidth", "IOPS", "Latência"]

if machine == 'beegfs':
    row_titles = ["1 Storage", "2 Storage"]
    for row_idx, row_title in enumerate(row_titles):
        st.markdown(f"### {row_title}")
        cols = st.columns(3)
        for col_idx, col_title in enumerate(col_titles):
            with cols[col_idx]:
                st.image(images[row_idx * 3 + col_idx], caption=col_title, width=300, use_container_width=True)
else:
    row_titles = ["ZFS Sync", "ZFS Async", "XFS"]
    for row_idx, row_title in enumerate(row_titles):
        st.markdown(f"### {row_title}")
        cols = st.columns(3)
        for col_idx, col_title in enumerate(col_titles):
            with cols[col_idx]:
                st.image(images[row_idx * 3 + col_idx], caption=col_title, width=300, use_container_width=True)

st.write("G.U. - J.R. - P.D // 2025 // v1.4")