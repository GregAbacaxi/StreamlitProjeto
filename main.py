import streamlit as st

DEVICES = ['raidz2_sync', 'raidz2_async', 'raid6_xfs']
MODES = ['bw', 'iops', 'lat']

special_beegfs = [
    'beegfs_1s_x_2s',
    'beegfs_1s_x_storage_84',
    'beegfs_2s_x_storage_avg'
]
special_lustre = [
    'lustre_1s_x_2s',
    'lustre_1s_x_storage_83',
    'lustre_2s_x_storage_avg'
]

# Casos 2x3 fixos
special_clients = ['lustre_2_clients']
special_multi = ['lustre_2c_2s']
special_new = [
    'beegfs_2c_2s',
    'lustre_4c_2s',
    'lustre_4c_1s',
    'beegfs_2c_1s'   # 🔥 Novo caso
]


def get_images(rw, blocksize, filter_type, machine, io_type):
    # Caso beegfs/lustre "base"
    if machine in ['beegfs', 'lustre']:
        imgs = []
        for n in [1, 2]:
            for mode in MODES:
                if rw == 'randrw':
                    imgs.append(
                        f"benchs/{machine}/{machine}_client_1c{n}s_{rw}_{filter_type}_{blocksize}_{mode}.png"
                    )
                else:
                    imgs.append(
                        f"benchs/{machine}/{machine}_client_1c{n}s_{rw}_{blocksize}_{mode}.png"
                    )
        return imgs

    # Casos especiais beegfs/lustre com randrw read/write
    if machine in special_beegfs + special_lustre:
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

    # beegfs/lustre IOR
    if machine in ['beegfs_ior', 'lustre_ior']:
        imgs = []
        for n in ['1s', '2s']:
            for mode in MODES:
                imgs.append(
                    f"benchs/{machine}_{n}/{blocksize}/"
                    f"{machine}_{n}_{rw}_{blocksize}_{mode}.png"
                )
        return imgs

    # Casos fixos tipo 2x3 (read/write)
    if machine in special_clients + special_multi + special_new:
        imgs = []
        for rw_val in ["read", "write"]:
            for mode in MODES:
                imgs.append(
                    f"benchs/{machine}/"
                    f"{machine}_{rw_val}_{blocksize}_{mode}.png"
                )
        return imgs

    # Caso genérico ZFS/XFS
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


# Layout da página
st.set_page_config(layout="wide")
st.title("Grelha Dinâmica de Imagens")

with st.sidebar:
    machine = st.selectbox(
        "Escolha a máquina",
        ['83', '84', 'beegfs', 'lustre', 'beegfs_ior', 'lustre_ior']
        + special_beegfs + special_lustre + special_clients + special_multi + special_new
    )

    io_type = None
    if machine not in (
        ['beegfs', 'lustre', 'beegfs_ior', 'lustre_ior']
        + special_beegfs + special_lustre + special_clients + special_multi + special_new
    ):
        all_io = ['sata-onboard', 'sata-sas', 'sas-sas']
        io_options = [io for io in all_io if not (machine == '84' and io == 'sata-onboard')]
        io_type = st.selectbox("Escolha o controlador I/O", io_options)

    blocksize = st.selectbox("Escolha o blocksize", ["1M", "512k", "4k"])

    if machine in ['beegfs_ior', 'lustre_ior']:
        rw = st.selectbox("Escolha o rw", ["read", "write"])
    elif machine in special_clients + special_multi + special_new:
        rw = None
    elif machine not in special_beegfs + special_lustre:
        rw = st.selectbox("Escolha o rw", ["randread", "randwrite", "randrw"])
    else:
        rw = None

    if rw == 'randrw':
        filter_type = st.selectbox("Escolha o filter", ["read", "write"])
    else:
        filter_type = None

# Opções selecionadas
selecionadas = [f"[{machine}]"]
if io_type:        selecionadas.append(f"[{io_type}]")
if rw:             selecionadas.append(f"[{rw}]")
if blocksize:      selecionadas.append(f"[{blocksize}]")
if filter_type:    selecionadas.append(f"[{filter_type}]")

st.write("**Opções selecionadas:** " + " ".join(selecionadas))

# Fetch e exibição das imagens
images = get_images(rw, blocksize, filter_type, machine, io_type)
col_titles = ["Bandwidth", "IOPS", "Latência"]

if machine in special_beegfs + special_lustre:
    row_titles = ["randread", "randwrite", "randrw read", "randrw write"]
elif machine in ['beegfs', 'lustre', 'beegfs_ior', 'lustre_ior']:
    row_titles = ["1 Storage", "2 Storage"]
elif machine in special_clients + special_multi + special_new:
    row_titles = ["Read", "Write"]
else:
    row_titles = ["ZFS Sync", "ZFS Async", "XFS"]

for row_idx, row_title in enumerate(row_titles):
    st.markdown(f"### {row_title}")
    cols = st.columns(3)
    for col_idx, col_title in enumerate(col_titles):
        with cols[col_idx]:
            st.image(images[row_idx * 3 + col_idx], caption=col_title, width=300, use_container_width=True)

# Rodapé
st.write("G.U. - J.R. - P.D // 2025 // v1.9.1")
