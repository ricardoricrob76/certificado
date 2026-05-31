import streamlit as st
import hashlib
import json
import base64
from datetime import datetime
from io import BytesIO
import qrcode
from PIL import Image
import os

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Validador de Certificados - IADados",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS PERSONALIZADO - ESTILO PROFISSIONAL
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
    }

    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
    }

    .cert-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        max-width: 800px;
        margin: 0 auto;
    }

    .header-logo {
        text-align: center;
        margin-bottom: 30px;
    }

    .header-logo h1 {
        color: #1e3c72;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .header-logo .subtitle {
        color: #667eea;
        font-size: 1rem;
        font-weight: 500;
        margin-top: 5px;
    }

    .badge-valid {
        display: inline-block;
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }

    .badge-invalid {
        display: inline-block;
        background: linear-gradient(135deg, #eb3349, #f45c43);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(235, 51, 73, 0.4);
    }

    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin: 25px 0;
    }

    .info-item {
        background: #f8f9ff;
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #667eea;
    }

    .info-label {
        color: #6b7280;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .info-value {
        color: #1e3c72;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .qr-section {
        text-align: center;
        margin: 30px 0;
        padding: 20px;
        background: #f0f4ff;
        border-radius: 15px;
    }

    .footer-info {
        text-align: center;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 2px solid #e5e7eb;
        color: #6b7280;
        font-size: 0.85rem;
    }

    .search-box {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
        padding: 15px !important;
        font-size: 1rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        color: white;
    }

    .stat-item {
        text-align: center;
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
    }

    .stat-label {
        font-size: 0.75rem;
        opacity: 0.8;
    }

    /* Esconder elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    .success-animation {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS DOS 37 ALUNOS - TURMA T3 IAGEN
# ============================================================
ALUNOS_T3 = {
    "CERT-T3-001": {
        "nome": "Geraldo Camilo da Fonseca T. Vallencia",
        "email": "geraldovalencia@gmail.com",
        "cpf": "***.***.***-01",
        "nota": 9.5,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-002": {
        "nome": "Alexandre de Oliveira",
        "email": "alexandre.marq@gmail.com",
        "cpf": "***.***.***-02",
        "nota": 9.1,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-003": {
        "nome": "José Roberto Bernardino da Silva",
        "email": "jr.bnardino@gmail.com",
        "cpf": "***.***.***-03",
        "nota": 9.8,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-004": {
        "nome": "Silvestre Silva",
        "email": "silsuedcarvalho16@gmail.com",
        "cpf": "***.***.***-04",
        "nota": 9.7,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-005": {
        "nome": "Jordan Oliveira",
        "email": "jordandossantosoliveira@gmail.com",
        "cpf": "***.***.***-05",
        "nota": 9.5,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-006": {
        "nome": "José Nichollas",
        "email": "jnichollaslr@gmail.com",
        "cpf": "***.***.***-06",
        "nota": 9.8,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-007": {
        "nome": "Ester Marreiro da Rocha",
        "email": "estermarreiro13@hotmail.com",
        "cpf": "***.***.***-07",
        "nota": 9.9,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-008": {
        "nome": "Antonio Ramos Neto",
        "email": "antonioramos9@hotmail.com",
        "cpf": "***.***.***-08",
        "nota": 9.3,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-009": {
        "nome": "Diego Altenkirch Kabbaz",
        "email": "diegokabbaz@gmail.com",
        "cpf": "***.***.***-09",
        "nota": 9.7,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-010": {
        "nome": "Bruno Rodrigues",
        "email": "fidbrunorodrigues@gmail.com",
        "cpf": "***.***.***-10",
        "nota": 9.6,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-011": {
        "nome": "Jean Paixão",
        "email": "jeutdb@gmail.com",
        "cpf": "***.***.***-11",
        "nota": 9.9,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-012": {
        "nome": "Igor Pinheiro de Brito",
        "email": "igor_pbrito@hotmail.com",
        "cpf": "***.***.***-12",
        "nota": 9.6,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-013": {
        "nome": "Kayky Dias",
        "email": "kaykymiguel5710@gmail.com",
        "cpf": "***.***.***-13",
        "nota": 9.6,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-014": {
        "nome": "Bruno Evangelista Lima",
        "email": "ct.bruno.evangelista@gmail.com",
        "cpf": "***.***.***-14",
        "nota": 9.4,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-015": {
        "nome": "Guilherme Macena",
        "email": "gmma0408@gmail.com",
        "cpf": "***.***.***-15",
        "nota": 9.3,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-016": {
        "nome": "Cristian Alves",
        "email": "cristian.assis20@gmail.com",
        "cpf": "***.***.***-16",
        "nota": 9.9,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-017": {
        "nome": "Kevin Kilmer",
        "email": "kp827767@gmail.com",
        "cpf": "***.***.***-17",
        "nota": 9.2,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-018": {
        "nome": "Rafael Cirne",
        "email": "cirnerafael06@gmail.com",
        "cpf": "***.***.***-18",
        "nota": 9.5,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-019": {
        "nome": "Robson Lima Palmeira",
        "email": "astecapb02@gmail.com",
        "cpf": "***.***.***-19",
        "nota": 9.8,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-020": {
        "nome": "Arthur Freitas Palmeira",
        "email": "arturfpalmeira@hotmail.com",
        "cpf": "***.***.***-20",
        "nota": 9.5,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-021": {
        "nome": "Amanda de Almeida",
        "email": "economiaamanda@gmail.com",
        "cpf": "***.***.***-21",
        "nota": 9.7,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-022": {
        "nome": "Perilo Oliveira",
        "email": "perilojp@gmail.com",
        "cpf": "***.***.***-22",
        "nota": 9.2,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-023": {
        "nome": "Alysson Assis",
        "email": "mercadoassis11@gmail.com",
        "cpf": "***.***.***-23",
        "nota": 9.9,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-024": {
        "nome": "Carlos Eduardo Souza Oliveira",
        "email": "czoliveiraa@gmail.com",
        "cpf": "***.***.***-24",
        "nota": 9.3,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-025": {
        "nome": "João Gabriel ",
        "email": "jbarretofalcao@gmail.com",
        "cpf": "***.***.***-25",
        "nota": 9.5,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-026": {
        "nome": "Augusto Medeiros",
        "email": "augustomedeiros71@gmail.com",
        "cpf": "***.***.***-26",
        "nota": 9.7,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-027": {
        "nome": "Biel Aguiar",
        "email": "bielaguiar4@gmail.com",
        "cpf": "***.***.***-27",
        "nota": 9.7,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-028": {
        "nome": "Gabriel Lyra",
        "email": "br.gabrielyra@gmail.com",
        "cpf": "***.***.***-28",
        "nota": 9.6,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-029": {
        "nome": "Jeffson Luiz",
        "email": "jeffsonluiz11@gmail.com",
        "cpf": "***.***.***-29",
        "nota": 9.4,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-030": {
        "nome": "Julio Cesar",
        "email": "julioceasarcs@gmail.com",
        "cpf": "***.***.***-30",
        "nota": 9.3,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-031": {
        "nome": "Rafael Vieira",
        "email": "rafael.vieiraa02@gmail.com",
        "cpf": "***.***.***-31",
        "nota": 9.8,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-032": {
        "nome": "José Hermano Pereira Henrique",
        "email": "hermanojr04@gmail.com",
        "cpf": "***.***.***-32",
        "nota": 9.6,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-033": {
        "nome": "Jailson Pereira da Silva",
        "email": "fernanda.melo@email.com",
        "cpf": "***.***.***-33",
        "nota": 9.6,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-034": {
        "nome": "Darllyson Davyd Tavares Coutinho",
        "email": "gustavo.andrade@email.com",
        "cpf": "***.***.***-34",
        "nota": 9.8,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-035": {
        "nome": "Wesllen Albuquerque de Souza",
        "email": "helena.rocha@email.com",
        "cpf": "***.***.***-35",
        "nota": 9.7,
        "status": "Aprovado",
        "data_conclusao": "30/05/2026"
    },
    "CERT-T3-036": {
        "nome": "Igor Douglas Barbosa",
        "email": "igor.barbosa@email.com",
        "cpf": "***.***.***-36",
        "nota": 8.9,
        "status": "Aprovado",
        "data_conclusao": "07/03/2026"
    },
    "CERT-T3-038": {
        "nome": "Lucas Vieira Medeiros",
        "email": "igor.barbosa@email.com",
        "cpf": "***.***.***-36",
        "nota": 8.9,
        "status": "Aprovado",
        "data_conclusao": "07/03/2026"
    },
    "CERT-T3-037": {
        "nome": "Juliana Cristiane Costa",
        "email": "juliana.costa@email.com",
        "cpf": "***.***.***-37",
        "nota": 9.5,
        "status": "Aprovado",
        "data_conclusao": "07/03/2026"
    }
}

CURSO_INFO = {
    "nome": "Inteligência Artificial Generativa com RAG, Fine Tuning, Guardrails, Skills, MCP, A2A e Agentes de IA",
    "instituicao": "IADados Consultoria e Treinamento",
    "parceira": "UNICORP Faculdades",
    "instrutor": "Me. Ricardo Roberto de Lima",
    "periodo": "09/05/2026 a 30/05/2026",
    "carga_horaria": "20 horas",
    "turma": "T3 IAGEN"
}

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def gerar_hash_verificacao(cert_id, nome):
    """Gera hash único para validação do certificado"""
    dados = f"{cert_id}|{nome}|{CURSO_INFO['nome']}|{CURSO_INFO['periodo']}"
    return hashlib.sha256(dados.encode()).hexdigest()[:16].upper()

def gerar_qr_code(cert_id):
    """Gera QR Code para o certificado"""
    aluno = ALUNOS_T3.get(cert_id)
    if not aluno:
        return None

    # URL de validação (ajustar para domínio do Vercel)
    base_url = os.environ.get("VERCEL_URL", "https://certificado-hpvuhzigjtn6cahgki9fma.streamlit.app")
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"

    url_validacao = f"{base_url}?cert={cert_id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url_validacao)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#1e3c72", back_color="white")

    # Salvar em buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer

def validar_certificado(cert_id):
    """Valida se o certificado existe e retorna dados"""
    if cert_id in ALUNOS_T3:
        aluno = ALUNOS_T3[cert_id].copy()
        aluno["cert_id"] = cert_id
        aluno["hash"] = gerar_hash_verificacao(cert_id, aluno["nome"])
        aluno["valido"] = True
        return aluno
    return None

def render_card_valido(resultado):
    """Renderiza o card de certificado válido usando componentes Streamlit"""

    # Container principal do card
    with st.container():
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); border-radius: 20px; padding: 40px; 
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); 
                    max-width: 800px; margin: 0 auto;">
        """, unsafe_allow_html=True)

        # Header
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #1e3c72; font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                🎓 Certificado Válido
            </h1>
            <div style="color: #667eea; font-size: 1rem; font-weight: 500; margin-top: 5px;">
                IADados Consultoria e Treinamento | UNICORP Faculdades
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Badge
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <span style="display: inline-block; background: linear-gradient(135deg, #11998e, #38ef7d); 
                         color: white; padding: 8px 20px; border-radius: 50px; font-weight: 600; 
                         font-size: 0.9rem; box-shadow: 0 4px 15px rgba(17,153,142,0.4);">
                ✓ CERTIFICADO VERIFICADO
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Nome do aluno
        st.markdown(f"""
        <div style="text-align: center; margin: 25px 0; padding: 20px; 
                    background: linear-gradient(135deg, #f0f4ff, #e8eeff); border-radius: 15px;">
            <div style="color: #6b7280; font-size: 0.85rem; margin-bottom: 8px;">Certificamos que</div>
            <div style="color: #1e3c72; font-size: 1.6rem; font-weight: 700;">{resultado['nome']}</div>
            <div style="color: #667eea; font-size: 0.9rem; margin-top: 8px;">
                concluiu com aproveitamento {resultado['nota']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Grid de informações
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 25px 0;">
        """, unsafe_allow_html=True)

        info_items = [
            ("Curso", CURSO_INFO['nome']),
            ("Código", resultado['cert_id']),
            ("Período", CURSO_INFO['periodo']),
            ("Carga Horária", CURSO_INFO['carga_horaria']),
            ("Instrutor", CURSO_INFO['instrutor']),
            ("Status", resultado['status']),
            ("Data Conclusão", resultado['data_conclusao']),
            ("Hash Verificação", resultado['hash']),
        ]

        for label, value in info_items:
            st.markdown(f"""
            <div style="background: #f8f9ff; padding: 15px; border-radius: 12px; border-left: 4px solid #667eea;">
                <div style="color: #6b7280; font-size: 0.75rem; text-transform: uppercase; 
                            letter-spacing: 0.5px; font-weight: 600; margin-bottom: 4px;">
                    {label}
                </div>
                <div style="color: #1e3c72; font-size: 0.95rem; font-weight: 600;">
                    {value}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # QR Code section
        st.markdown("""
        <div style="text-align: center; margin: 30px 0; padding: 20px; background: #f0f4ff; border-radius: 15px;">
            <div style="color: #1e3c72; font-weight: 600; margin-bottom: 10px;">📱 QR Code de Validação</div>
            <div style="color: #6b7280; font-size: 0.85rem;">Escaneie para verificar a autenticidade deste certificado</div>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown(f"""
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; 
                    border-top: 2px solid #e5e7eb; color: #6b7280; font-size: 0.85rem;">
            <div style="font-weight: 600; color: #1e3c72;">AR CONSULTORIA EM BUSINESS INTELLIGENCE E BIG DATA</div>
            <div style="margin-top: 8px;">Validado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
            <div style="margin-top: 5px; font-size: 0.75rem;">Este documento é válido em todo território nacional</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

def render_card_invalido(termo_busca):
    """Renderiza o card de certificado inválido"""

    with st.container():
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); border-radius: 20px; padding: 40px; 
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); 
                    max-width: 800px; margin: 0 auto;">
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #eb3349; font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.5px;">
                ⚠️ Certificado Não Encontrado
            </h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <span style="display: inline-block; background: linear-gradient(135deg, #eb3349, #f45c43); 
                         color: white; padding: 8px 20px; border-radius: 50px; font-weight: 600; 
                         font-size: 0.9rem; box-shadow: 0 4px 15px rgba(235,51,73,0.4);">
                ✗ CÓDIGO INVÁLIDO
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: #fef2f2; border-radius: 15px; margin: 20px 0;">
            <div style="font-size: 3rem; margin-bottom: 15px;">🔍</div>
            <div style="color: #991b1b; font-size: 1.1rem; font-weight: 600;">
                Nenhum certificado encontrado para:<br>
                <span style="color: #dc2626;">"{termo_busca}"</span>
            </div>
            <div style="color: #6b7280; margin-top: 15px; font-size: 0.9rem;">
                Verifique se o código está correto ou entre em contato com a instituição.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #f8f9ff; padding: 20px; border-radius: 12px; margin-top: 20px;">
            <div style="font-weight: 600; color: #1e3c72; margin-bottom: 10px;">💡 Dicas:</div>
            <ul style="color: #6b7280; margin: 0; padding-left: 20px;">
                <li>O código deve seguir o formato: <b>CERT-T3-XXX</b></li>
                <li>Exemplo válido: CERT-T3-001</li>
                <li>Você também pode buscar pelo nome completo do aluno</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; 
                    border-top: 2px solid #e5e7eb; color: #6b7280; font-size: 0.85rem;">
            <div style="font-weight: 600; color: #1e3c72;">AR CONSULTORIA EM BUSINESS INTELLIGENCE E BIG DATA</div>
            <div style="margin-top: 8px;">Consulta realizada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# INTERFACE PRINCIPAL
# ============================================================

def main():
    # Verificar parâmetro de URL
    query_params = st.query_params
    cert_param = query_params.get("cert", "")

    # Header com estatísticas
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 5px;">🎓 Validador de Certificados</h1>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem;">IADados Consultoria e Treinamento</p>
    </div>
    """, unsafe_allow_html=True)

    # Barra de estatísticas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="text-align: center; background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; color: white;">
            <div style="font-size: 1.8rem; font-weight: 700;">{len(ALUNOS_T3)}</div>
            <div style="font-size: 0.75rem; opacity: 0.8;">Alunos</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align: center; background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; color: white;">
            <div style="font-size: 1.8rem; font-weight: 700;">{CURSO_INFO['carga_horaria']}</div>
            <div style="font-size: 0.75rem; opacity: 0.8;">Carga Horária</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        aprovados = sum(1 for a in ALUNOS_T3.values() if a["status"] == "Aprovado")
        st.markdown(f"""
        <div style="text-align: center; background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; color: white;">
            <div style="font-size: 1.8rem; font-weight: 700;">{aprovados}</div>
            <div style="font-size: 0.75rem; opacity: 0.8;">Aprovados</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="text-align: center; background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; color: white;">
            <div style="font-size: 1.8rem; font-weight: 700;">T3</div>
            <div style="font-size: 0.75rem; opacity: 0.8;">Turma IAGEN</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Caixa de busca
    st.markdown("""
    <div style="background: white; border-radius: 15px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
        <h3 style="color: #1e3c72; margin-bottom: 15px;">🔍 Validar Certificado</h3>
    </div>
    """, unsafe_allow_html=True)

    # Input de busca
    busca = st.text_input(
        "Digite o Código do Certificado ou Nome do Aluno:",
        value=cert_param,
        placeholder="Ex: CERT-T3-001 ou Fabiano Quirino da Silva",
        label_visibility="collapsed"
    )

    # Botão de validação
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        validar = st.button("✅ VALIDAR CERTIFICADO", use_container_width=True, type="primary")

    # Processar validação
    if validar or (cert_param and not busca.startswith("Ex:")):
        termo_busca = busca.strip() if busca else cert_param

        # Buscar certificado
        resultado = None
        if termo_busca.upper().startswith("CERT-T3-"):
            resultado = validar_certificado(termo_busca.upper())
        else:
            # Busca por nome
            for cert_id, dados in ALUNOS_T3.items():
                if termo_busca.lower() in dados["nome"].lower():
                    resultado = validar_certificado(cert_id)
                    break

        st.markdown("<br>", unsafe_allow_html=True)

        if resultado:
            # Certificado VÁLIDO - usar função de renderização
            render_card_valido(resultado)

            # Gerar e exibir QR Code
            qr_buffer = gerar_qr_code(resultado['cert_id'])
            if qr_buffer:
                col_qr1, col_qr2, col_qr3 = st.columns([1, 2, 1])
                with col_qr2:
                    st.image(qr_buffer, width=200)
        else:
            # Certificado INVÁLIDO
            render_card_invalido(termo_busca)

    # Lista de alunos (expansível)
    with st.expander("📋 Ver Lista Completa de Alunos (37)"):
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 15px;">
            <h3 style="color: #1e3c72; margin-bottom: 20px;">Turma T3 IAGEN - Alunos Matriculados</h3>
        </div>
        """, unsafe_allow_html=True)

        # Tabela de alunos
        dados_tabela = []
        for cert_id, aluno in ALUNOS_T3.items():
            dados_tabela.append({
                "Código": cert_id,
                "Nome": aluno["nome"],
                "Nota": aluno["nota"],
                "Status": aluno["status"]
            })

        st.dataframe(
            dados_tabela,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Código": st.column_config.TextColumn("Código", width="medium"),
                "Nome": st.column_config.TextColumn("Nome Completo", width="large"),
                "Nota": st.column_config.NumberColumn("Nota", format="%.1f"),
                "Status": st.column_config.TextColumn("Status")
            }
        )

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 30px 0; color: rgba(255,255,255,0.6); font-size: 0.8rem;">
        <div>© 2026 IADados Consultoria e Treinamento</div>
        <div style="margin-top: 5px;">Em parceria com UNICORP Faculdades</div>
        <div style="margin-top: 10px;">Sistema de Validação de Certificados v1.0</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
