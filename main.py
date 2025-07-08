import streamlit as st

DEVICES = ['raidz2_sync', 'raidz2_async', 'raid6_xfs']
MODES   = ['bw', 'iops', 'lat']
special_beegfs = ['beegfs_1s_x_2s', 'beegfs_1s_x_storage_84', 'beegfs_2s_x_storage_avg']

def get_images(rw, blocksize, filter_type, machine, io_type):
    if machine == 'beegfs':
        imgs = []
        for n in [1, 2]:
            for mode in MODES:
                if rw == 'randrw':
                    imgs.append(
                        f"benchs/{machine}/beegfs_client_1c{n}s_{rw}_{filter_type}_{blocksize}_{mode}.png"
                    )
                else:
                    imgs.append(
                        f"benchs/{machine}/beegfs_client_1c{n}s_{rw}_{blocksize}_{mode}.png"
                    )
        return imgs

    if machine in special_beegfs:
        imgs = []
        rows = [
            ('randread', None),
            ('randwrite', None),
            ('randrw', 'read'),
            ('randrw', 'write')
        ]
        for rw_val, filt in rows:
            for mode in MODES:
                if rw_val == 'randrw':
                    imgs.append(
                        f"benchs/{machine}/{rw_val}/{blocksize}/"
                        f"{machine}_{rw_val}_{filt}_{blocksize}_{mode}.png"
                    )
                else:
                    imgs.append(
                        f"benchs/{machine}/{blocksize}/"
                        f"{machine}_{rw_val}_{blocksize}_{mode}.png"
                    )
        return imgs

    
    imgs = []
    for device in DEVICES:
        for mode in MODES:
            if rw == 'randrw':
                imgs.append(
                    f"benchs/{machine}/{io_type}/{device}/{rw}/{blocksize}/"
                    f"{device}_{rw}_{filter_type}_{blocksize}_{mode}.png"
                )
            else:
                imgs.append(
                    f"benchs/{machine}/{io_type}/{device}/{blocksize}/"
                    f"{device}_{rw}_{blocksize}_{mode}.png"
                )
    return imgs

# Configuração da página
st.set_page_config(layout="wide")
st.title("Grelha Dinâmica de Imagens")

with st.sidebar:
    machine = st.selectbox(
        "Escolha a máquina",
        ['83', '84', 'beegfs',
         'beegfs_1s_x_2s',
         'beegfs_1s_x_storage_84',
         'beegfs_2s_x_storage_avg']
    )

    io_type = None
    if machine not in ['beegfs',
                       'beegfs_1s_x_2s',
                       'beegfs_1s_x_storage_84',
                       'beegfs_2s_x_storage_avg']:
        all_io = ['sata-onboard', 'sata-sas', 'sas-sas']
        io_options = [io for io in all_io
                      if not (machine == '84' and io == 'sata-onboard')]
        io_type = st.selectbox("Escolha o controlador I/O", io_options)

    blocksize = st.selectbox("Escolha o blocksize", ["1M", "512k", "4k"])

    special_beegfs = ['beegfs_1s_x_2s',
                      'beegfs_1s_x_storage_84',
                      'beegfs_2s_x_storage_avg']

    if machine not in special_beegfs:
        rw = st.selectbox("Escolha o rw", ["randread", "randwrite", "randrw"])
    else:
        rw = None

    if rw == 'randrw':
        filter_type = st.selectbox("Escolha o filter", ["read", "write"])
    else:
        filter_type = None

# Monta lista apenas com opções que não são None
selecionadas = []
selecionadas.append(f"[{machine}]")
if io_type is not None:
    selecionadas.append(f"[{io_type}]")
if rw is not None:
    selecionadas.append(f"[{rw}]")
if blocksize is not None:
    selecionadas.append(f"[{blocksize}]")
if filter_type is not None:
    selecionadas.append(f"[{filter_type}]")

# Exibe apenas os pares existentes, separados por vírgula
st.write("**Opções selecionadas:** " + " ".join(selecionadas))

# Geração e exibição de imagens
images = get_images(rw, blocksize, filter_type, machine, io_type)
col_titles = ["Bandwidth", "IOPS", "Latência"]

if machine in special_beegfs:
    row_titles = ["randread", "randwrite", "randrw read", "randrw write"]
    for row_idx, row_title in enumerate(row_titles):
        st.markdown(f"### {row_title}")
        cols = st.columns(3)
        for col_idx, col_title in enumerate(col_titles):
            with cols[col_idx]:
                st.image(images[row_idx * 3 + col_idx], caption=col_title, width=300, use_container_width=True)

elif machine == 'beegfs':
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

# Rodapé
st.write("G.U. - J.R. - P.D // 2025 // v1.6")
